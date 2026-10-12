"""Discover and acquire design materials with durable, item-scoped provenance.

The host agent makes visual and licence judgments. Search metadata is a lead,
never a licence clearance. All requests are explicit; no network calls on import.
"""
from html import unescape
import json
from pathlib import Path
import re
import secrets
from urllib.parse import urlencode
import xml.etree.ElementTree as ET

from engine import EngineError, atomic_write, digest, identifier, now, require, text
from resource_http import fetch, fetch_json, public_url

KINDS = {"photo", "illustration", "icon", "texture", "pattern", "graphic", "font"}
PROVIDERS = {"openverse", "commons", "iconify", "met"}
CATALOG = Path(__file__).resolve().parents[1] / "assets/resource-libraries.json"


def libraries(kind=None):
    if kind:
        require(kind in KINDS, "Unknown resource kind.")
    values = json.loads(CATALOG.read_text(encoding="utf-8"))
    return [v for v in values if not kind or kind in v["kinds"]]


def clean(value, limit=3000):
    return unescape(re.sub(r"<[^>]*>", "", str(value or "")))[:limit].strip()


def url(value):
    public_url(value)
    return value


def candidate(provider, external_id, title, creator, source, download, license_name="Unknown", license_url="", **extra):
    value = {"provider": provider, "external_id": str(external_id), "title": clean(title) or "Untitled",
             "creator": clean(creator) or "Unknown", "source_url": source, "download_url": download,
             "license_name": clean(license_name) or "Unknown", "license_url": license_url or ""}
    value.update(extra)
    return value


def search_provider(provider, query, kind, limit):
    if provider == "openverse":
        data = fetch_json("https://api.openverse.org/v1/images/?" + urlencode({"q": query, "page_size": limit,
                         "license_type": "commercial,modification", "mature": "false"}))
        return [candidate(provider, v["id"], v.get("title"), v.get("creator"), v["foreign_landing_url"], v["url"],
                          " ".join(str(v.get(k) or "") for k in ("license", "license_version")).strip(), v.get("license_url"),
                          width=v.get("width"), height=v.get("height")) for v in data.get("results", [])[:limit]]
    if provider == "commons":
        params = {"action": "query", "format": "json", "generator": "search", "gsrsearch": query,
                  "gsrnamespace": 6, "gsrlimit": limit, "prop": "imageinfo", "iiprop": "url|size|extmetadata"}
        data = fetch_json("https://commons.wikimedia.org/w/api.php?" + urlencode(params))
        require("error" not in data, "Wikimedia search could not complete. Try a simpler query or browse the library.")
        results = []
        for v in sorted(data.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 0)):
            info = v.get("imageinfo", [{}])[0]
            meta = info.get("extmetadata", {})
            get = lambda k: meta.get(k, {}).get("value", "")
            if info.get("url") and info.get("descriptionurl"):
                results.append(candidate(provider, v["pageid"], v.get("title", "").removeprefix("File:"), get("Artist"),
                                         info["descriptionurl"], info["url"], get("LicenseShortName"), get("LicenseUrl"),
                                         width=info.get("width"), height=info.get("height")))
        return results[:limit]
    if provider == "iconify":
        data = fetch_json("https://api.iconify.design/search?" + urlencode({"query": query, "limit": max(32, limit)}))
        collections = data.get("collections", {})
        results = []
        for name in data.get("icons", [])[:limit]:
            if not re.fullmatch(r"[a-z0-9-]+:[a-z0-9-]+", name):
                continue
            prefix, icon = name.split(":")
            info = collections.get(prefix, {})
            lic = info.get("license", {})
            author = info.get("author", {})
            results.append(candidate(provider, name, name, author.get("name"),
                                     f"https://icon-sets.iconify.design/{prefix}/{icon}/", f"https://api.iconify.design/{prefix}/{icon}.svg",
                                     lic.get("title") or lic.get("spdx"), lic.get("url")))
        return results
    if provider == "met":
        data = fetch_json("https://collectionapi.metmuseum.org/public/collection/v1.1/search?" + urlencode({"q": query, "hasImages": "true", "limit": min(limit * 2, 12)}))
        results = []
        for key in (data.get("objectIDs") or [])[:min(limit * 2, 12)]:
            v = fetch_json("https://collectionapi.metmuseum.org/public/collection/v1/objects/" + str(int(key)))
            if v.get("isPublicDomain") is True and v.get("primaryImage"):
                results.append(candidate(provider, key, v.get("title"), v.get("artistDisplayName"), v["objectURL"],
                                         v["primaryImage"], "CC0 / Met Open Access", "https://www.metmuseum.org/policies/image-resources"))
                if len(results) == limit:
                    break
        return results
    raise EngineError("Choose openverse, commons, iconify or met. Other libraries can be browsed through the host.")


def save_candidate(ws, brand, value, actor):
    ws.get("brand", brand, "profile")
    require(isinstance(value, dict), "Resource candidate must be an object.")
    provider = text(value.get("provider", "web"), "provider", 100)
    source, download = url(value.get("source_url")), url(value.get("download_url"))
    kind = value.get("kind")
    require(kind in KINDS, "Choose a supported resource kind.")
    entry = {"provider": provider, "kind": kind, "title": text(value.get("title"), "resource title", 3000),
             "creator": text(value.get("creator", "Unknown"), "creator", 3000), "source_url": source,
             "download_url": download, "license_name": text(value.get("license_name") or "Unknown", "licence name", 500),
             "license_url": url(value["license_url"]) if value.get("license_url") else "",
             "query": text(value["query"], "query", 500) if value.get("query") else "",
             "style_fit": text(value["style_fit"], "style fit", 4000) if value.get("style_fit") else "Not yet assessed",
             "external_id": clean(value.get("external_id"), 300), "status": "CANDIDATE", "created": now(), "actor": text(actor, "actor", 200)}
    for dimension in ("width", "height"):
        if type(value.get(dimension)) is int and value[dimension] > 0:
            entry[dimension] = value[dimension]
    entry["id"] = "resource-" + digest({"source": source, "download": download})[:32]
    entry["hash"] = digest(entry)
    def apply():
        existing = ws.get("resource", brand, entry["id"], optional=True)
        if existing:
            return existing
        ws.put("resource", brand, entry["id"], entry)
        ws.audit(brand, "resource.discovered", entry["id"], {"provider": provider, "kind": kind})
        return entry
    return ws.transaction(apply)


def search(ws, brand, provider, query, kind, limit=8):
    ws.get("brand", brand, "profile")
    query = text(query, "search query", 500)
    require(provider in PROVIDERS and kind in KINDS, "Choose a supported provider and resource kind.")
    require(type(limit) is int and 1 <= limit <= 20, "Search limit must be 1-20.")
    require(kind != "font", "Use the font libraries through your host browser; built-in image searches do not return fonts.")
    require(provider != "iconify" or kind == "icon", "Iconify is an icon search; choose kind icon.")
    try:
        values = search_provider(provider, query, kind, limit)
        found, rejected = [], 0
        for v in values:
            try:
                found.append(save_candidate(ws, brand, {**v, "query": query, "kind": kind}, "resource-search"))
            except EngineError:
                rejected += 1
        return {"provider": provider, "query": query, "results": found, "skipped": rejected,
                "notice": "Candidates only. Inspect the original source, licence and actual material before use."}
    except EngineError:
        raise
    except (KeyError, TypeError, ValueError) as exc:
        raise EngineError("Resource service returned an unexpected response. Browse the original library or use another provider.") from exc


def review(ws, brand, key, value):
    require(isinstance(value, dict), "Resource review must be an object.")
    for name in ("commercial_allowed", "adaptations_allowed", "attribution_required"):
        require(type(value.get(name)) is bool, f"{name} must be an explicit boolean.")
    require(value["commercial_allowed"] and value["adaptations_allowed"], "This material is not cleared for commercial design adaptation. Keep it as a candidate/reference and choose another.")
    proof = {name: value[name] for name in ("commercial_allowed", "adaptations_allowed", "attribution_required")}
    for name in ("license_name", "evidence", "intended_use", "style_fit", "reviewer"):
        proof[name] = text(value.get(name), name, 10000)
    proof["license_url"] = url(value.get("license_url"))
    proof["attribution"] = text(value.get("attribution"), "attribution", 4000)
    proof["reviewed_at"] = now()
    def apply():
        entry = ws.get("resource", brand, key)
        require(value.get("resource_hash") == entry["hash"], "Resource changed; review the current candidate.")
        require(entry["status"] != "ACQUIRED", "Acquired provenance is immutable; add a new source/file for a revised licence.")
        entry.update(status="REVIEWED", rights_review=proof, style_fit=proof["style_fit"])
        entry["hash"] = digest({k: v for k, v in entry.items() if k != "hash"})
        ws.put("resource", brand, key, entry)
        ws.audit(brand, "resource.reviewed", key, {"reviewer": proof["reviewer"], "hash": entry["hash"]})
        return entry
    return ws.transaction(apply)


def safe_svg(raw):
    require(len(raw) <= 2 * 1024 * 1024, "SVG exceeds the 2 MB limit.")
    require(not re.search(br"<!DOCTYPE|<!ENTITY|<\?xml-stylesheet", raw, re.I), "SVG declarations or external stylesheets are not allowed.")
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        raise EngineError("Invalid SVG document.") from exc
    allowed = {"svg", "g", "defs", "path", "rect", "circle", "ellipse", "line", "polyline", "polygon", "title", "desc", "clipPath", "mask", "pattern", "linearGradient", "radialGradient", "stop", "use", "symbol", "text", "tspan"}
    require(root.tag.split("}")[-1] == "svg", "Expected an SVG root.")
    for element in root.iter():
        require(not element.tag.startswith("{") or element.tag.startswith("{http://www.w3.org/2000/svg}"), "SVG contains a foreign namespace.")
        require(element.tag.split("}")[-1] in allowed, "SVG contains an active or unsupported element; use a trusted static export.")
        for key, val in element.attrib.items():
            attr = key.split("}")[-1].lower()
            require(not attr.startswith("on") and attr not in {"style", "base"}, "SVG active attributes or CSS are not accepted.")
            if attr == "href":
                require(re.fullmatch(r"#[A-Za-z0-9_.:-]+", val), "SVG external references are not allowed.")
            if "url" in val.lower():
                require(re.fullmatch(r"url\(#[A-Za-z0-9_.:-]+\)", val), "SVG may reference only local fragment IDs.")
            require(not re.search(r"(?:https?:|data:|javascript:|@import|\\)", val, re.I), "SVG contains an external or active value.")
    return raw


def file_type(raw):
    if raw.startswith(b"\x89PNG\r\n\x1a\n") and len(raw) >= 24: return ".png"
    if raw.startswith(b"\xff\xd8\xff") and raw.endswith(b"\xff\xd9"): return ".jpg"
    if raw[:4] == b"RIFF" and raw[8:12] == b"WEBP": return ".webp"
    if raw[:4] == b"OTTO": return ".otf"
    if raw[:4] == b"\x00\x01\x00\x00": return ".ttf"
    if raw[:4] == b"wOFF": return ".woff"
    if raw[:4] == b"wOF2": return ".woff2"
    if raw.lstrip().startswith((b"<svg", b"<?xml")):
        safe_svg(raw)
        return ".svg"
    raise EngineError("Use an actual PNG, JPEG, WebP, static SVG or font file. HTML pages, archives and executables are not design materials.")


def acquire(ws, brand, key, expected_hash, actor, local_file=None):
    entry = ws.get("resource", brand, key)
    require(entry["hash"] == expected_hash, "Resource changed; use the current reviewed hash.")
    if entry["status"] == "ACQUIRED":
        return ws.asset_bytes(brand, entry["asset_id"])[0]
    require(entry["status"] == "REVIEWED", "Inspect the source and record a resource-review before downloading for production.")
    if local_file:
        path = Path(local_file).expanduser()
        require(path.is_absolute() and path.is_file() and not path.is_symlink(), "Choose an explicit local material file.")
        require(not any(p.startswith(".env") or p in {".ssh", ".aws", ".git", ".codex", ".claude"} for p in path.parts), "Credential files cannot be materials.")
        require(0 < path.stat().st_size <= 20 * 1024 * 1024, "Material must be at most 20 MB.")
        raw, final_url = path.read_bytes(), entry["download_url"]
    else:
        raw, _, final_url = fetch(entry["download_url"])
    require(len(raw) <= 20 * 1024 * 1024, "Material exceeds 20 MB.")
    ext = file_type(raw)
    provenance = {"resource_id": key, "resource_hash": entry["hash"], "provider": entry["provider"], "kind": entry["kind"],
                  "title": entry["title"], "creator": entry["creator"], "source_url": entry["source_url"], "download_url": entry["download_url"],
                  "retrieved_url": final_url, "retrieved_at": now(), "method": "local-import" if local_file else "public-https",
                  "rights_review": entry["rights_review"], "style_fit": entry["style_fit"]}
    staging = ws.safe_path("incoming/" + secrets.token_hex(16) + ext)
    atomic_write(staging, raw)
    try:
        # Recheck after network activity, before changing any stored resource state.
        def apply():
            current = ws.get("resource", brand, key)
            require(current["hash"] == expected_hash, "Resource changed during download; review it again.")
            if current["status"] == "ACQUIRED":
                return ws.asset_bytes(brand, current["asset_id"])[0]
            asset = ws.import_asset(brand, str(staging), "material", "licensed", entry["rights_review"]["evidence"], actor,
                                    display_name=entry["title"][:200] + ext, provenance=provenance, in_transaction=True)
            current.update(status="ACQUIRED", asset_id=asset["id"])
            ws.put("resource", brand, key, current)
            ws.audit(brand, "resource.acquired", key, {"asset_id": asset["id"], "sha256": asset["sha256"]})
            return asset
        return ws.transaction(apply)
    finally:
        staging.unlink(missing_ok=True)
