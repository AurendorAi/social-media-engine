"""Offline acquisition, provenance, isolation and public-network boundary tests."""
import copy
import io
import json
import socket
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch, MagicMock
from test_engine import RuntimeHarness, Workspace, EngineError, PROFILE
import resources
import resource_http

SVG = b'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"><path d="M0 0h24v24z" fill="currentColor"/></svg>'
CANDIDATE = dict(provider="fixture", title="Paper pattern", creator="Test Artist", kind="pattern",
                 source_url="https://example.com/pattern", download_url="https://example.com/pattern.svg",
                 license_name="Test licence", license_url="https://example.com/license")


def proof(candidate, attribution_required=False):
    return dict(resource_hash=candidate["hash"], commercial_allowed=True, adaptations_allowed=True,
                attribution_required=attribution_required, license_name="Fixture only",
                license_url="https://example.com/license", evidence="Synthetic rights evidence, only for tests.",
                intended_use="Background for a fictional coffee post", style_fit="Fine grain supports the quiet paper direction.",
                reviewer="test-source-reviewer", attribution="Pattern by Test Artist (fixture)")


class ResourceTests(RuntimeHarness):
    def setUp(self):
        super().setUp()
        self.ready()
        self.ws = Workspace(self.workspace)

    def tearDown(self):
        self.ws.close()
        super().tearDown()

    def acquire(self, attribution=False):
        c = resources.save_candidate(self.ws, "northstar", CANDIDATE, "tester")
        c = resources.review(self.ws, "northstar", c["id"], proof(c, attribution))
        with patch.object(resources, "fetch", return_value=(SVG, "image/svg+xml", c["download_url"])):
            a = resources.acquire(self.ws, "northstar", c["id"], c["hash"], "tester")
        return c, a

    def with_material(self, asset):
        item = self.draft()
        item["material_ids"] = [asset["id"]]
        item["creative"]["material_uses"] = [dict(asset_id=asset["id"], purpose="Test fixture", edits="Recolored in a test", credit_placement="Caption")]
        return item

    def test_acquisition_keeps_brand_and_existing_content_approved(self):
        old = self.approve_text()
        context = self.ws.context("northstar")
        c, a = self.acquire()
        self.assertEqual(self.ws.context("northstar"), context)
        self.assertEqual(self.ws.current_item("northstar", old["id"])["status"], "APPROVED")
        self.assertEqual(a["role"], "material")
        self.assertEqual(self.ws.asset_bytes("northstar", a["id"])[1], SVG)
        with patch.object(resources, "fetch", side_effect=AssertionError("Must not redownload")):
            self.assertEqual(resources.acquire(self.ws, "northstar", c["id"], c["hash"], "tester"), a)

    def test_review_required_and_stale_reviews_blocked(self):
        c = resources.save_candidate(self.ws, "northstar", CANDIDATE, "tester")
        with self.assertRaises(EngineError): resources.acquire(self.ws, "northstar", c["id"], c["hash"], "tester")
        for field in ("commercial_allowed", "adaptations_allowed"):
            p = proof(c); p[field] = False
            with self.assertRaises(EngineError): resources.review(self.ws, "northstar", c["id"], p)
        p = proof(c); p["resource_hash"] = "stale"
        with self.assertRaises(EngineError): resources.review(self.ws, "northstar", c["id"], p)
        c = resources.review(self.ws, "northstar", c["id"], proof(c))
        with self.assertRaises(EngineError): resources.acquire(self.ws, "northstar", c["id"], "old-hash", "tester")

    def test_cli_local_import_and_brand_isolation(self):
        c = self.call("resource-add", "--actor", "tester", body=CANDIDATE)
        c = self.call("resource-review", "--id", c["id"], body=proof(c))
        file = self.workspace / "pattern.svg"; file.write_bytes(SVG)
        a = self.call("resource-import", "--id", c["id"], "--hash", c["hash"], "--actor", "tester", "--file", file)
        self.assertEqual(a["provenance"]["method"], "local-import")
        self.ready("other")
        self.assertEqual(self.ws.list("resource", "other"), [])
        with self.assertRaises(EngineError): self.ws.asset_bytes("other", a["id"])
        self.call("asset-import", "--file", file, "--role", "material", "--rights", "licensed", "--note", "Bypass attempt", "--actor", "tester", ok=False)
        self.assertTrue(self.call("resource-libraries", "--kind", "texture"))
        selected = self.call("resource-libraries", "--id", "ambientcg")
        self.assertEqual([row["id"] for row in selected], ["ambientcg"])
        self.assertEqual(self.call("resource-libraries", "--id", "ambientcg", "--query", "NO-SUCH-TERM"), [])
        self.call("resource-libraries", "--id", "no-such-source", ok=False)

    def test_used_material_bytes_and_provenance_bind_content(self):
        _, a = self.acquire()
        item = self.ws.save_item("northstar", self.with_material(a))
        # Unused library additions do not affect the content hash.
        other = {**CANDIDATE, "download_url": "https://example.com/another.svg"}
        resources.save_candidate(self.ws, "northstar", other, "tester")
        self.assertEqual(self.ws.current_item("northstar", item["id"])["hash"], item["hash"])
        path = self.ws.safe_path(a["path"]); path.write_bytes(SVG + b' ')
        with self.assertRaises(EngineError): self.ws.current_item("northstar", item["id"])
        path.write_bytes(SVG)
        a["provenance"]["creator"] = "Changed"
        self.ws.put("asset", "northstar", a["id"], a)
        with self.assertRaises(EngineError): self.ws.current_item("northstar", item["id"])

    def test_required_credit_is_enforced_and_survives_export(self):
        _, a = self.acquire(attribution=True)
        item = self.with_material(a)
        with self.assertRaises(EngineError): self.ws.save_item("northstar", item)
        item["variants"][0]["caption"] += " " + a["provenance"]["rights_review"]["attribution"]
        saved = self.ws.save_item("northstar", item)
        self.review(saved, "editorial"); self.review(saved, "brand")
        self.ws.approve_item("northstar", saved["id"], saved["hash"], "Test Owner")
        output = self.ws.export_item("northstar", saved["id"])
        from pathlib import Path
        directory = Path(output["directory"])
        manifest = json.loads((directory / "content.json").read_text())
        self.assertEqual(manifest["materials"][0]["sha256"], a["sha256"])
        self.assertIn("Test Artist", (directory / "CREDITS.md").read_text())
        self.assertFalse(list(directory.glob("*.svg")), "Raw source files must not be redistributed")

    def test_material_cannot_be_published_as_finished_output(self):
        _, a = self.acquire()
        with self.assertRaises(EngineError):
            self.ws.save_item("northstar", self.draft(format="image", asset_ids=[a["id"]]))
        item = self.with_material(a); item["creative"]["material_uses"] = []
        with self.assertRaises(EngineError): self.ws.save_item("northstar", item)

    def test_html_payload_is_not_registered(self):
        c = resources.save_candidate(self.ws, "northstar", CANDIDATE, "tester")
        c = resources.review(self.ws, "northstar", c["id"], proof(c))
        with patch.object(resources, "fetch", return_value=(b'<html>Sign in</html>', "image/png", c["download_url"])):
            with self.assertRaises(EngineError): resources.acquire(self.ws, "northstar", c["id"], c["hash"], "tester")
        self.assertEqual(self.ws.list("asset", "northstar"), [])
        self.assertEqual(self.ws.get("resource", "northstar", c["id"])["status"], "REVIEWED")

    def test_search_metadata_does_not_clear_licence_or_style(self):
        with patch.object(resources, "search_provider", return_value=[CANDIDATE]):
            result = resources.search(self.ws, "northstar", "commons", "paper texture", "texture", 2)
        c = result["results"][0]
        self.assertEqual(c["status"], "CANDIDATE")
        self.assertNotIn("rights_review", c)
        self.assertEqual(c["query"], "paper texture")
        with self.assertRaises(EngineError): resources.search(self.ws, "northstar", "iconify", "paper", "photo")


class CatalogueTests(unittest.TestCase):
    def test_catalogue_has_item_scope_evidence_and_usable_filters(self):
        with patch.object(resources, "fetch", side_effect=AssertionError("Catalogue must remain offline")), patch.object(resources, "fetch_json", side_effect=AssertionError("Catalogue must remain offline")):
            entries = resources.libraries()
            self.assertGreaterEqual(len(entries), 20)
            ids = [entry["id"] for entry in entries]
            self.assertEqual(len(ids), len(set(ids)))
            required = {"name", "url", "kinds", "access", "notes", "license_url", "free_scope", "commercial_use", "attribution", "restrictions", "access_notes", "search_method", "use_when", "style_terms", "formats", "verified_date", "evidence", "scope_type"}
            for entry in entries:
                with self.subTest(library=entry["id"]):
                    self.assertTrue(required <= entry.keys(), required - entry.keys())
                    self.assertTrue(entry["kinds"])
                    self.assertLessEqual(set(entry["kinds"]), resources.KINDS)
                    self.assertIn(entry["access"], {"api", "browse"})
                    self.assertTrue(entry["url"].startswith("https://"))
                    self.assertTrue(entry["license_url"].startswith("https://"))
                    self.assertRegex(entry["verified_date"], r"^\d{4}-\d{2}-\d{2}$")
                    self.assertIsInstance(entry["restrictions"], str)
                    self.assertTrue(entry["evidence"])
                    for evidence in entry["evidence"]:
                        self.assertTrue(evidence["url"].startswith("https://"))
                        self.assertTrue(evidence["observed"].strip())
                    self.assertEqual(resources.libraries(library_id=entry["id"]), [entry])
            self.assertEqual(resources.libraries(query="no-such-source-zq019"), [])
            with self.assertRaises(EngineError):
                resources.libraries(library_id="no-such-source")
            with self.assertRaises(EngineError):
                resources.libraries(kind="not-a-kind")

    def test_common_category_words_find_expected_free_sources(self):
        cases = {
            "photography": {"pexels", "unsplash"},
            "photos": {"pexels", "unsplash"},
            "icons": {"lucide", "iconoir"},
            "fonts": {"googlefonts", "fontshare", "collletttivo"},
            "typography": {"googlefonts", "fontshare", "collletttivo"},
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                self.assertLessEqual(expected, {row["id"] for row in resources.libraries(query=query)})

    def test_filter_intersects_words_kind_and_exact_id_without_network(self):
        # Controlled examples distinguish AND from OR and casefold from lowercase.
        fixture = [
            {"id": "source-a", "name": "Straße Library", "kinds": ["texture"], "use_when": "Paper scenes", "style_terms": ["fine grain"]},
            {"id": "source-b", "name": "Paper Library", "kinds": ["pattern"], "use_when": "Other backgrounds", "style_terms": ["fine grain"]},
            {"id": "source-c", "name": "Other", "kinds": ["texture"], "use_when": "Paper scenes", "style_terms": ["bold"]},
        ]
        with tempfile.TemporaryDirectory() as folder:
            catalog = Path(folder) / "catalog.json"
            catalog.write_text(json.dumps(fixture))
            with patch.object(resources, "CATALOG", catalog), patch.object(socket, "getaddrinfo", side_effect=AssertionError("No network for catalogue filtering")):
                self.assertEqual(resources.libraries(query=" STRASSE  GRAIN "), [fixture[0]])
                self.assertEqual(resources.libraries(kind="texture", query="paper grain"), [fixture[0]])
                self.assertEqual(resources.libraries(library_id="source-b", query="paper"), [fixture[1]])
                self.assertEqual(resources.libraries(library_id="source-b", kind="texture"), [])
                self.assertEqual(resources.libraries(query="SOURCE-C"), [fixture[2]])
                self.assertEqual(resources.libraries(query="   "), fixture)


class NetworkBoundaryTests(unittest.TestCase):
    def test_disallowed_url_forms(self):
        for url in ['http://example.com/a', 'https://user:pass@example.com/a', 'https://localhost/a', 'https://home.local/a', 'https://example.com:8443/a', 'file:///etc/passwd', 'https://example.com/a?access_token=private', 'https://example.com/\r\nheader', 'https://example.com/a#fragment']:
            with self.subTest(url=url), self.assertRaises(EngineError): resource_http.public_url(url)

    def test_private_and_mixed_dns_are_rejected(self):
        for ip in ['127.0.0.1', '10.0.0.1', '169.254.169.254', '192.168.1.1', '::1', '::ffff:127.0.0.1', '224.0.0.1']:
            addresses = [(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('8.8.8.8',443)), (socket.AF_INET, socket.SOCK_STREAM, 6, '', (ip,443))]
            with self.subTest(ip=ip), patch.object(socket,'getaddrinfo',return_value=addresses), self.assertRaises(EngineError):
                resource_http.public_addresses('example.com')

    def test_redirect_to_private_scheme_is_not_followed(self):
        response = MagicMock(status=302); response.getheader.return_value = 'http://127.0.0.1/private'
        connection = MagicMock(); connection.getresponse.return_value = response
        with patch.object(resource_http,'PublicConnection',return_value=connection) as factory, self.assertRaises(EngineError):
            resource_http.fetch('https://example.com/public')
        self.assertEqual(factory.call_count, 1)
        connection.close.assert_called_once()

    def test_size_and_incomplete_responses_fail(self):
        for headers, body in [({'Content-Length':'100'}, b'x'), ({'Content-Length':'4'}, b'x'), ({},b'123456')]:
            response = MagicMock(status=200)
            response.getheader.side_effect = lambda key, default=None: headers.get(key, default)
            response.read.side_effect = io.BytesIO(body).read
            connection=MagicMock(); connection.getresponse.return_value=response
            with self.subTest(headers=headers), patch.object(resource_http,'PublicConnection',return_value=connection), self.assertRaises(EngineError):
                resource_http.fetch('https://example.com/a',max_bytes=5)

    def test_active_svg_and_external_references_are_refused(self):
        for part in [b'<script>alert(1)</script>', b'<foreignObject/>', b'<g xmlns="http://www.w3.org/1999/xhtml"/>', b'<image href="https://example.com/a"/>', b'<path onclick="alert(1)"/>', b'<use href="https://example.com/a"/>', b'<path style="fill:red"/>', b'<path fill="url(https://example.com/a)"/>', b'<animate attributeName="href"/>']:
            with self.subTest(part=part), self.assertRaises(EngineError): resources.safe_svg(b'<svg>'+part+b'</svg>')
        with self.assertRaises(EngineError): resources.safe_svg(b'<!DOCTYPE svg [<!ENTITY a "b">]><svg/>')
        self.assertEqual(resources.file_type(SVG), '.svg')
        for raw in [b'<html/>', b'PK\x03\x04archive', b'#!/bin/sh\nrun']:
            with self.assertRaises(EngineError): resources.file_type(raw)

    def test_provider_adapters(self):
        cases = [
            ('openverse','photo', {'results':[dict(id='x',title='Photo',creator='Artist',foreign_landing_url='https://example.com/source',url='https://example.com/a.jpg',license='by',license_version='4.0',license_url='https://example.com/license')]}),
            ('commons','texture', {'query':{'pages':{'1':dict(pageid=1,title='File:Texture',imageinfo=[dict(url='https://example.com/a.png',descriptionurl='https://example.com/source',extmetadata={'Artist':{'value':'<a>Artist</a>'},'LicenseShortName':{'value':'CC0'}})])}}}),
            ('iconify','icon', {'icons':['set:coffee'],'collections':{'set':{'author':{'name':'Artist'},'license':{'title':'MIT','url':'https://example.com/license'}}}}),
        ]
        for provider, kind, data in cases:
            with self.subTest(provider=provider), patch.object(resources,'fetch_json',return_value=data):
                results=resources.search_provider(provider,'coffee',kind,1)
                self.assertEqual(len(results),1)
                self.assertEqual(results[0]['creator'],'Artist')
        with patch.object(resources,'fetch_json',side_effect=[{'objectIDs':[1,2]}, {'isPublicDomain':False}, {'isPublicDomain':True,'primaryImage':'https://example.com/a.jpg','objectURL':'https://example.com/source','title':'Artwork'}]):
            self.assertEqual(len(resources.search_provider('met','flowers','pattern',2)),1)
