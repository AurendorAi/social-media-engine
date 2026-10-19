"""Brand discovery regressions; entirely fictional profiles and no network calls."""
import copy
from test_engine import RuntimeHarness, PROFILE


def board(profile_hash, key="first-directions"):
    base = {"colors": ["#173C34", "#F6EEDF"], "fonts": ["Owner-approved licensed serif"],
            "logo_policy": "Typeset the supplied name; do not invent a mark.",
            "visual_style": "Quiet editorial hierarchy with generous space.",
            "imagery_style": "Actual product photography with simple instructional diagrams."}
    return {"id": key, "brand_hash": profile_hash, "options": [
        {"id": "editorial", "title": "The quiet expert", "rationale": "Fits a thoughtful craft audience.",
         "tradeoff": "Requires strong original photography.", "profile": base},
        {"id": "graphic", "title": "A useful burst of color", "rationale": "Makes short lessons easy to notice.",
         "tradeoff": "Needs restraint to avoid visual noise.", "profile": {**base,
          "colors": ["#192B52", "#E7B33C"], "visual_style": "Bold diagrams with clear typographic contrast."}}
    ]}


class StyleDiscoveryTests(RuntimeHarness):
    def propose(self):
        profile = self.call("brand-update", "--actor", "Owner", body={"name": "A new craft studio", "identity_status": "new"})
        return self.call("style-propose", "--actor", "Designer", body=board(profile["hash"]))

    def test_no_identity_can_resume_and_choose_without_implicit_approval(self):
        proposal = self.propose()
        self.assertEqual(len(self.call("snapshot")["styles"]), 1)
        chosen = self.call("style-select", "--id", proposal["id"], "--option", "graphic",
                           "--hash", proposal["hash"], "--actor", "Owner")
        self.assertFalse(chosen["approved"])
        self.assertEqual(chosen["answers"]["name"], "A new craft studio")
        self.assertEqual(chosen["answers"]["colors"], ["#192B52", "#E7B33C"])
        self.assertEqual(self.call("status")["state"], "ONBOARDING_REQUIRED")
        self.call("context", ok=False)

    def test_changed_profile_rejects_old_directions_without_overwrite(self):
        proposal = self.propose()
        profile = self.call("brand-update", "--actor", "Owner", body={"design_personality": "Playful and expressive"})
        self.call("style-select", "--id", proposal["id"], "--option", "graphic", "--hash", proposal["hash"], "--actor", "Owner", ok=False)
        self.assertEqual(self.call("status")["profile"]["hash"], profile["hash"])

    def test_styles_are_brand_isolated(self):
        proposal = self.propose()
        self.ready("second")
        self.assertEqual(self.call("snapshot", brand="second")["styles"], [])
        self.call("style-select", "--id", proposal["id"], "--option", "graphic", "--hash", proposal["hash"], "--actor", "Owner", brand="second", ok=False)

    def test_style_choice_invalidates_approved_content(self):
        self.ready()
        item = self.approve_text()
        proposal = self.call("style-propose", "--actor", "Designer", body=board(self.call("status")["profile"]["hash"]))
        self.assertEqual(self.call("status")["state"], "READY", "Proposing must not change the brand")
        self.call("style-select", "--id", proposal["id"], "--option", "graphic", "--hash", proposal["hash"], "--actor", "Owner")
        self.assertEqual(self.call("status")["state"], "BRAND_REVIEW")
        self.assertEqual(self.call("snapshot")["items"][0]["effective_status"], "STALE")
        self.call("export", "--id", item["id"], ok=False)

    def test_unknown_direction_bad_hash_and_duplicate_board_rejected(self):
        proposal = self.propose()
        for option, expected in [("missing", proposal["hash"]), ("graphic", "old-hash")]:
            self.call("style-select", "--id", proposal["id"], "--option", option, "--hash", expected, "--actor", "Owner", ok=False)
        self.call("style-propose", "--actor", "Designer", body=board(proposal["brand_hash"]), ok=False)

    def test_invalid_visual_payloads_fail_without_mutation(self):
        profile = self.call("brand-update", "--actor", "Owner", body={"name": "New brand"})
        invalid = []
        for field, value in [("colors", ["red"]), ("fonts", []), ("approval_owner", "Attacker"), ("visual_style", "")]:
            value_board = board(profile["hash"])
            value_board["options"][0]["profile"][field] = value
            invalid.append(value_board)
        dup = board(profile["hash"]); dup["options"][1]["id"] = "editorial"; invalid.append(dup)
        short = board(profile["hash"]); short["options"] = short["options"][:1]; invalid.append(short)
        for value_board in invalid:
            self.call("style-propose", "--actor", "Designer", body=value_board, ok=False)
        self.assertEqual(self.call("snapshot")["styles"], [])
        self.assertEqual(self.call("status")["profile"]["hash"], profile["hash"])

    def test_existing_profiles_stay_ready_and_distinct_across_industries(self):
        for key, name, language, style in [("coffee", "Coffee studio", "en", "Warm photographic"),
                                          ("ceramics", "陶芸工房", "ja", "Material-led quiet"),
                                          ("education", "تعليم", "ar", "Clear illustrated")]:
            profile = copy.deepcopy(PROFILE)
            profile.update(name=name, languages=[language], visual_style=style)
            self.ready(key, profile)
            self.assertEqual(self.call("status", brand=key)["state"], "READY")
            self.assertEqual(self.call("context", brand=key)["profile"]["visual_style"], style)

    def test_invalid_identity_mode_rejected(self):
        self.call("brand-update", "--actor", "Owner", body={"identity_status": "auto-approved"}, ok=False)


def png_fixture(index):
    """Distinct decodable one-pixel PNGs, only for byte-integrity tests, not design samples."""
    import struct
    import zlib
    def chunk(kind, value):
        return struct.pack('!I', len(value)) + kind + value + struct.pack('!I', zlib.crc32(kind + value) & 0xffffffff)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('!2I5B', 1, 1, 8, 2, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(bytes([0, index, 50, 100]))) + chunk(b'IEND', b''))


def first_content_board(harness, count=10, brand='northstar'):
    catalog = harness.call('style-catalog')['styles']
    profile_hash = harness.call('status', brand=brand)['profile']['hash']
    visual = board(profile_hash)['options'][0]['profile']
    options = []
    for index, entry in enumerate(catalog[:count]):
        path = harness.workspace / ('sample-%s.png' % index)
        path.write_bytes(png_fixture(index))
        asset = harness.call('asset-import', '--file', path, '--role', 'output', '--rights', 'owned',
                             '--note', 'Original integrity-test fixture; not a quality example',
                             '--actor', 'Fixture author', brand=brand)
        options.append({'id': entry['id'], 'title': entry['title'], 'rationale': 'Authored use-case fit.',
                        'tradeoff': 'Requires relevant imagery.', 'profile': visual,
                        'sample_asset_ids': [asset['id']]})
    return {'id': 'first-content', 'brand_hash': profile_hash, 'mode': 'first-content',
            'use_case': 'Fictional home-brewing education.',
            'selection_basis': 'Audience, identity, script, useful variety and available materials.',
            'options': options}


class RenderedStyleDiscoveryTests(RuntimeHarness):
    def test_catalogue_is_exactly_the_27_requested_priorities(self):
        entries = self.call('style-catalog')['styles']
        self.assertEqual(len(entries), 27)
        self.assertEqual(len({x['id'] for x in entries}), 27)
        from pathlib import Path
        from test_engine import ROOT
        research = (ROOT / 'plugins/social-media-engine/skills/social-media-engine/references/research-findings.md').read_text()
        table = research.split('## Coverage of the 27 requested priorities')[1].split('## Conditional observations')[0]
        self.assertEqual({x['title'] for x in entries},
                         {line.split('|')[1].strip() for line in table.splitlines()
                          if line.startswith('| ') and 'Requested priority' not in line})
        self.assertEqual(self.call('brands'), [], 'Catalogue lookup must not invent a brand')

    def test_ten_rendered_choices_persist_and_reload_without_approving_posts(self):
        self.ready()
        self.assertEqual(self.call('status')['style_discovery']['state'], 'NEEDS_SAMPLES')
        value = first_content_board(self)
        proposal = self.call('style-propose', '--actor', 'Designer', body=value)
        self.assertEqual(self.call('status')['style_discovery']['state'], 'AWAITING_CHOICE')
        self.call('context', ok=False)
        self.assertEqual(len(self.call('snapshot')['styles'][0]['options']), 10)
        chosen = self.call('style-select', '--id', proposal['id'], '--option', 'mixed-media',
                           '--hash', proposal['hash'], '--actor', 'Owner')
        self.assertFalse(chosen['approved'])
        self.assertEqual(chosen['answers']['offers'], PROFILE['offers'])
        self.assertEqual(self.call('status')['style_discovery']['state'], 'SELECTED')
        self.call('context', ok=False)
        self.call('brand-approve', '--hash', chosen['hash'], '--actor', 'Owner')
        context = self.call('context')
        self.assertEqual(context['selected_style']['option']['id'], 'mixed-media')
        self.assertEqual(context['selected_style']['board_hash'], proposal['hash'])
        self.assertEqual(len(context['selected_style']['option']['samples'][0]['sha256']), 64)
        self.assertEqual(self.call('snapshot')['items'], [])
        self.assertEqual(len(self.call('snapshot')['styles']), 1, 'Reload does not create new discovery')

    def test_rejects_incomplete_unrendered_unknown_and_repeated_styles(self):
        self.ready()
        value = first_content_board(self)
        invalid = []
        short = copy.deepcopy(value); short['options'] = short['options'][:9]; invalid.append(short)
        no_sample = copy.deepcopy(value); no_sample['options'][0]['sample_asset_ids'] = []; invalid.append(no_sample)
        repeated = copy.deepcopy(value); repeated['options'][1]['sample_asset_ids'] = repeated['options'][0]['sample_asset_ids']; invalid.append(repeated)
        unknown = copy.deepcopy(value); unknown['options'][0]['id'] = 'invented-style'; invalid.append(unknown)
        duplicate = copy.deepcopy(value); duplicate['options'][1]['id'] = duplicate['options'][0]['id']; invalid.append(duplicate)
        no_fit = copy.deepcopy(value); del no_fit['selection_basis']; invalid.append(no_fit)
        for data in invalid:
            with self.subTest(data=data['options'][0]['id']):
                self.call('style-propose', '--actor', 'Designer', body=data, ok=False)
        self.assertEqual(self.call('snapshot')['styles'], [])
        self.assertTrue(self.call('status')['profile']['approved'])

    def test_changed_sample_bytes_reject_selection_and_later_context(self):
        self.ready()
        value = first_content_board(self)
        proposal = self.call('style-propose', '--actor', 'Designer', body=value)
        from engine import Workspace
        ws = Workspace(str(self.workspace))
        sample = ws.get('asset', 'northstar', proposal['options'][0]['sample_asset_ids'][0])
        path = ws.safe_path(sample['path']); original = path.read_bytes()
        path.write_bytes(original + b'tampered')
        self.call('style-select', '--id', proposal['id'], '--option', 'anthropomorphic',
                  '--hash', proposal['hash'], '--actor', 'Owner', ok=False)
        path.write_bytes(original)
        chosen = self.call('style-select', '--id', proposal['id'], '--option', 'anthropomorphic',
                           '--hash', proposal['hash'], '--actor', 'Owner')
        self.call('brand-approve', '--hash', chosen['hash'], '--actor', 'Owner')
        path.write_bytes(original + b'tampered')
        self.call('context', ok=False)
        ws.close()

    def test_cross_brand_sample_and_non_output_rights_are_rejected(self):
        self.ready()
        value = first_content_board(self)
        self.ready('other')
        foreign = copy.deepcopy(value); foreign['brand_hash'] = self.call('status', brand='other')['profile']['hash']
        self.call('style-propose', '--actor', 'Designer', body=foreign, brand='other', ok=False)
        source = self.workspace / 'unknown.png'; source.write_bytes(png_fixture(99))
        asset = self.call('asset-import', '--file', source, '--role', 'output', '--rights', 'unknown',
                          '--note', 'Uncleared fixture', '--actor', 'Fixture author')
        value['options'][0]['sample_asset_ids'] = [asset['id']]
        self.call('style-propose', '--actor', 'Designer', body=value, ok=False)
        self.assertEqual(self.call('snapshot')['styles'], [])

    def test_all_27_supported_and_stale_profile_cannot_be_overwritten(self):
        self.ready()
        value = first_content_board(self, 27)
        proposal = self.call('style-propose', '--actor', 'Designer', body=value)
        self.assertEqual(len(proposal['options']), 27)
        current = self.call('brand-update', '--actor', 'Owner', body={'visual_style': 'Updated identity constraint'})
        self.call('style-select', '--id', proposal['id'], '--option', 'y2k', '--hash', proposal['hash'], '--actor', 'Owner', ok=False)
        self.assertEqual(self.call('status')['profile']['hash'], current['hash'])
