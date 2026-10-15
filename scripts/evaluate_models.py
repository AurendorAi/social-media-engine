#!/usr/bin/env python3
"""Offline, paired social-design evaluation. Never calls providers or reads credentials."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import random
import re
import shutil
import contextlib
import io
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = {
    "caption": "Finished publishable caption in the brief's language",
    "alt_text": "Accessible description of the finished design",
    "design": {"format": "svg", "width": 1080, "height": 1350,
               "svg": "Complete editable standalone SVG with viewBox='0 0 1080 1350'. Use shapes, paths and editable text. No scripts, CSS/style elements, images, links, foreignObject or external references. Inline presentation attributes only; internal gradient references allowed. Root width/height must be 1080/1350 respectively or omitted."},
    "source_notes": ["Sources or supplied facts used; disclose unavailable assets"]}
PREAMBLE = "This is an isolated production-only evaluation with limited instruction context. The supplied synthetic brief is an approved evaluation fixture. No workspace or tools are available. Apply creative production guidance only; do not request onboarding, tool execution, or runtime approvals. Do not claim real owner approval or publishing. Return the requested finished artifact.\n\n"
SELECTED = ["SKILL.md", "references/brand-quality.md", "references/strategy-writing.md", "references/creative-production.md", "references/editorial-depth.md", "references/review.md", "references/design-patterns.md", "references/producer-revision-loop.md", "assets/design-patterns.json"]
OPTIONAL = set(SELECTED[-3:])
COMMON = "Create one finished professional social post from the supplied synthetic brief. Return only a JSON object matching this contract. The SVG itself must be the actual finished design, not a design plan. Do not include evaluator commentary or scores.\n"
TAGS = {"svg", "g", "defs", "rect", "circle", "ellipse", "line", "polyline", "polygon", "path", "text", "tspan", "linearGradient", "radialGradient", "stop", "clipPath", "title", "desc"}
ATTRS = set("id x y x1 y1 x2 y2 cx cy r rx ry width height viewBox d points fill stroke stroke-width stroke-linecap stroke-linejoin stroke-dasharray opacity fill-opacity stroke-opacity transform font-family font-size font-weight font-style letter-spacing text-anchor dominant-baseline direction unicode-bidi dx dy rotate gradientUnits gradientTransform offset stop-color stop-opacity clip-path fill-rule clip-rule preserveAspectRatio role aria-label aria-labelledby aria-describedby".split())


def digest(value):
    if isinstance(value, str):
        value = value.encode("utf-8")
    return hashlib.sha256(value).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_svg(svg):
    if not isinstance(svg, str) or len(svg.encode("utf-8")) > 500_000:
        raise ValueError("SVG absent or exceeds 500KB")
    if re.search(r"<!|<\?", svg):
        raise ValueError("XML declarations, entities and processing instructions prohibited")
    tree = ET.fromstring(svg)
    ns = "{http://www.w3.org/2000/svg}"
    if tree.tag != ns + "svg" or tree.attrib.get("viewBox") != "0 0 1080 1350":
        raise ValueError("SVG namespace and exact viewBox required")
    for name, expected in (("width", "1080"), ("height", "1350")):
        if name in tree.attrib and tree.attrib[name] != expected:
            raise ValueError("Root SVG " + name + " must equal " + expected + " or be omitted")
        tree.set(name, expected)
    nodes = list(tree.iter())
    if len(nodes) > 3000:
        raise ValueError("Too many SVG nodes")
    text_found = False
    for node in nodes:
        tag = node.tag.removeprefix(ns)
        if tag not in TAGS or node.tag != ns + tag:
            raise ValueError("Disallowed SVG element: " + str(node.tag))
        text_found |= tag in {"text", "tspan"} and bool((node.text or "").strip())
        for key, value in node.attrib.items():
            if key not in ATTRS:
                raise ValueError("Disallowed SVG attribute: " + key)
            if key == "role" and not re.fullmatch(r"[a-z][a-z-]*(?: [a-z][a-z-]*)*", value):
                raise ValueError("Invalid accessibility role")
            if key in {"aria-labelledby", "aria-describedby"} and not re.fullmatch(r"[A-Za-z_][\w.-]*(?: [A-Za-z_][\w.-]*)*", value):
                raise ValueError("Accessibility references must be local ID tokens")
            if key == "aria-label" and (len(value) > 4096 or any(ord(c) < 32 for c in value)):
                raise ValueError("Invalid accessibility label")
            if len(value) > 100_000 or re.search(r"https?:|data:|javascript:|file:|@|[\\]", value, re.I):
                raise ValueError("Unsafe SVG attribute value")
            if "url" in value.lower() and not re.fullmatch(r"url\(#[A-Za-z_][\w.-]*\)", value):
                raise ValueError("Only local fragment URL references allowed")
    if not text_found:
        raise ValueError("Editable SVG text required")
    # Re-serialize parsed allowlisted XML; never render the raw response.
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    return ET.tostring(tree, encoding="unicode")


def validate_output(value):
    if not isinstance(value, dict):
        raise ValueError("Output must be a JSON object")
    for field in ("caption", "alt_text"):
        if not isinstance(value.get(field), str) or not value[field].strip():
            raise ValueError(field + " must be nonempty text")
    if not isinstance(value.get("source_notes"), list) or not all(isinstance(x, str) for x in value["source_notes"]):
        raise ValueError("source_notes must be a string array")
    design = value.get("design", {})
    if not isinstance(design, dict) or (design.get("format"), design.get("width"), design.get("height")) != ("svg", 1080, 1350):
        raise ValueError("Expected SVG design at 1080x1350")
    return validate_svg(design.get("svg"))


def instruction_bundle(path):
    path = Path(path)
    if path.is_file():
        files = [(path.name, path)]
    else:
        base = path / "skills/social-media-engine"
        files = []
        for relative in SELECTED:
            source = base / relative
            if source.is_file():
                files.append((relative, source))
            elif relative not in OPTIONAL:
                raise ValueError("Missing required production instruction: " + str(source))
    manifest = [{"path": name, "sha256": digest(source.read_bytes())} for name, source in files]
    system = PREAMBLE + "\n\n".join("FILE: " + name + "\n" + source.read_text(encoding="utf-8") for name, source in files)
    return system, manifest


def instructions(path):
    return instruction_bundle(path)[0]


def prepare(args):
    out = Path(args.out)
    briefs = json.loads(Path(args.briefs).read_text(encoding="utf-8"))[:args.brief_count]
    if len(briefs) != args.brief_count or not briefs:
        raise ValueError("Requested brief count unavailable")
    if len(args.models) != len(set(args.models)):
        raise ValueError("Duplicate model IDs would create request ID collisions")
    brief_ids = [brief["id"] for brief in briefs]
    if len(brief_ids) != len(set(brief_ids)):
        raise ValueError("Duplicate brief IDs would create request ID collisions")
    out.mkdir(parents=True, exist_ok=False)
    write_json(out / "briefs.json", briefs)
    write_json(out / "contract.json", CONTRACT)
    requests = []
    manifest = {"scope": "limited-production-only", "preamble": PREAMBLE, "conditions": {}}
    for condition, source in (("baseline", args.baseline), ("candidate", args.candidate)):
        system, selected = instruction_bundle(source)
        manifest["conditions"][condition] = {"selected_files": selected, "instruction_sha256": digest(system)}
        (out / (condition + "-instructions.txt")).write_text(system, encoding="utf-8")
        for brief in briefs:
            user = COMMON + json.dumps(CONTRACT, ensure_ascii=False) + "\nSVG allowed elements: " + ", ".join(sorted(TAGS)) + ". Allowed attributes: " + ", ".join(sorted(ATTRS)) + ". Other elements and attributes are rejected. Accessibility ID references must be local tokens.\nBRIEF:\n" + json.dumps(brief, ensure_ascii=False)
            for model in args.models:
                rid = digest(json.dumps([condition, brief["id"], model, args.seed]))[:20]
                requests.append({"request_id": rid, "condition": condition, "brief_id": brief["id"], "model": model, "seed": args.seed,
                                 "instruction_sha256": digest(system), "prompt_sha256": digest(user),
                                 "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]})
    write_json(out / "instruction-manifest.json", manifest)
    (out / "requests.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in requests), encoding="utf-8")
    print(json.dumps({"requests": len(requests), "out": str(out)}))


def ingest(args):
    run = Path(args.run)
    requests = {r["request_id"]: r for r in map(json.loads, (run / "requests.jsonl").read_text().splitlines())}
    metadata = json.loads(Path(args.metadata).read_text())
    request = requests[metadata["request_id"]]
    for field in ("model", "seed"):
        if metadata.get(field) != request[field]:
            raise ValueError("Metadata mismatch: " + field)
    cost = metadata.get("cost_usd")
    if cost is not None and (isinstance(cost, bool) or not isinstance(cost, (float, int)) or not math.isfinite(cost) or cost < 0):
        raise ValueError("Invalid cost")
    dest = run / "outputs" / request["request_id"]
    dest.mkdir(parents=True, exist_ok=False)
    raw = Path(args.response).read_bytes()
    (dest / "raw-response.txt").write_bytes(raw)
    record = {k: request[k] for k in ("request_id", "condition", "brief_id", "model", "seed", "instruction_sha256", "prompt_sha256")}
    for field in ("elapsed_ms", "provider", "finish_reason", "tokens", "seed_supported", "error", "errors", "provider_request_id", "usage", "response_id", "served_model"):
        if field in metadata:
            record[field] = metadata[field]
    if "tokens" not in record and "usage" in record:
        record["tokens"] = record["usage"]
    if "provider_request_id" not in record and "response_id" in record:
        record["provider_request_id"] = record["response_id"]
    record.update({"cost_usd": cost, "provider_status": metadata.get("status"), "raw_sha256": digest(raw), "artifact_valid": False,
                   "professional_quality_proven": False, "visual_review_required": True})
    try:
        if metadata.get("status") != "success":
            raise ValueError("Provider did not succeed: " + str(metadata.get("error", metadata.get("status"))))
        value = json.loads(raw)
        svg = validate_output(value)
        (dest / "design.svg").write_text(svg, encoding="utf-8")
        write_json(dest / "content.json", {k: value[k] for k in ("caption", "alt_text", "source_notes")})
        record.update({"artifact_valid": True, "svg_sha256": digest(svg), "content_sha256": digest((dest / "content.json").read_bytes())})
    except (ValueError, TypeError, ET.ParseError, UnicodeError) as error:
        record["error"] = str(error)
    write_json(dest / "record.json", record)
    print(json.dumps(record))


def reprocess(args):
    """Uniformly validate original raw responses into a new run; no generation."""
    run, out = Path(args.run), Path(args.out)
    out.mkdir(parents=True, exist_ok=False)
    for source in run.iterdir():
        if source.is_file():
            shutil.copyfile(source, out / source.name)
    requests = list(map(json.loads, (run / "requests.jsonl").read_text().splitlines()))
    counts = {"scheduled": len(requests), "original_valid": 0, "reprocessed_valid": 0, "missing": 0}
    metadata_dir = out / "reprocess-metadata"
    metadata_dir.mkdir()
    for request in requests:
        rid = request["request_id"]
        src = run / "outputs" / rid
        if not (src / "record.json").is_file():
            counts["missing"] += 1
            continue
        original = json.loads((src / "record.json").read_text())
        if original.get("exploratory_salvage"):
            raise ValueError("Reprocess source must be original strict run")
        raw_path = src / "raw-response.txt"
        if digest(raw_path.read_bytes()) != original["raw_sha256"]:
            raise ValueError("Raw response hash mismatch: " + rid)
        provider_metadata = run / "provider" / (rid + ".json")
        if provider_metadata.is_file():
            metadata = json.loads(provider_metadata.read_text())
        else:
            metadata = dict(original, status=original.get("provider_status"))
        metadata_path = metadata_dir / (rid + ".json")
        write_json(metadata_path, metadata)
        with contextlib.redirect_stdout(io.StringIO()):
            ingest(argparse.Namespace(run=str(out), metadata=str(metadata_path), response=str(raw_path)))
        record_path = out / "outputs" / rid / "record.json"
        record = json.loads(record_path.read_text())
        record.update({"original_artifact_valid": bool(original.get("artifact_valid")),
                       "original_validation_error": original.get("error"), "validator_change": args.note})
        write_json(record_path, record)
        counts["original_valid"] += bool(original.get("artifact_valid"))
        counts["reprocessed_valid"] += bool(record.get("artifact_valid"))
    write_json(out / "reprocess-manifest.json", {"source_run": str(run.resolve()), "validator_change": args.note,
               "validator_sha256": digest(Path(__file__).read_bytes()), "requests_sha256": digest((out / "requests.jsonl").read_bytes()),
               "policy": "All original raw responses revalidated uniformly; no generation, prompt change, or JSON normalization", "counts": counts})
    print(json.dumps(counts))


def unwrap_json_fence(raw):
    """One exact complete JSON fence only: no surrounding prose or nested fences."""
    text = raw.decode("utf-8")
    match = re.fullmatch(r"\s*```json[ \t]*\r?\n(.*?)\r?\n```[ \t]*\s*", text, re.DOTALL)
    if not match or "```" in match.group(1):
        raise ValueError("Not exactly one complete json fence")
    return json.loads(match.group(1))


def salvage(args):
    """Create separate exploratory render run; never modify strict results."""
    run, out = Path(args.run), Path(args.out)
    out.mkdir(parents=True, exist_ok=False)
    for name in ("requests.jsonl", "briefs.json", "contract.json", "instruction-manifest.json", "baseline-instructions.txt", "candidate-instructions.txt"):
        if (run / name).is_file():
            shutil.copyfile(run / name, out / name)
    requests = list(map(json.loads, (run / "requests.jsonl").read_text().splitlines()))
    counts = {"scheduled": len(requests), "strict_valid": 0, "salvaged_for_visual_review": 0, "missing": 0}
    for request in requests:
        src = run / "outputs" / request["request_id"]
        if not (src / "record.json").is_file():
            counts["missing"] += 1
            continue
        record = json.loads((src / "record.json").read_text())
        raw = (src / "raw-response.txt").read_bytes()
        if digest(raw) != record["raw_sha256"]:
            raise ValueError("Raw response hash mismatch: " + request["request_id"])
        if record.get("exploratory_salvage"):
            raise ValueError("Salvage source must be original strict run")
        dest = out / "outputs" / request["request_id"]
        dest.mkdir(parents=True)
        (dest / "raw-response.txt").write_bytes(raw)
        strict = bool(record.get("artifact_valid"))
        record.update({"exploratory_salvage": True, "primary_strict_artifact_valid": strict,
                       "raw_contract_compliant": strict, "normalization": "none", "salvaged_for_visual_review": False})
        if strict:
            counts["strict_valid"] += 1
            for name, field in (("design.svg", "svg_sha256"), ("content.json", "content_sha256")):
                data = (src / name).read_bytes()
                if digest(data) != record[field]:
                    raise ValueError("Artifact hash mismatch: " + request["request_id"])
                (dest / name).write_bytes(data)
        elif record.get("provider_status") == "success":
            try:
                value = unwrap_json_fence(raw)
                svg = validate_output(value)
                (dest / "design.svg").write_text(svg, encoding="utf-8")
                write_json(dest / "content.json", {k: value[k] for k in ("caption", "alt_text", "source_notes")})
                record.update({"artifact_valid": True, "primary_error": record.get("error"),
                               "normalization": "removed_one_complete_json_fence", "salvaged_for_visual_review": True,
                               "svg_sha256": digest(svg), "content_sha256": digest((dest / "content.json").read_bytes())})
                counts["salvaged_for_visual_review"] += 1
            except (ValueError, TypeError, ET.ParseError, UnicodeError) as error:
                record["salvage_error"] = str(error)
        write_json(dest / "record.json", record)
    write_json(out / "salvage-manifest.json", {"policy": "Exact single complete json fence only, applied to all original records; exploratory visual study, strict failures unchanged", "source_run": str(run.resolve()), "counts": counts})
    print(json.dumps(counts))


def blind(args):
    run, out = Path(args.run), Path(args.out)
    briefs = {x["id"]: x for x in json.loads((run / "briefs.json").read_text())}
    requests = list(map(json.loads, (run / "requests.jsonl").read_text().splitlines()))
    groups = {}
    for request in requests:
        groups.setdefault((request["brief_id"], request["model"], request["seed"]), []).append(request)
    for group, pair in groups.items():
        conditions = [request.get("condition") for request in pair]
        if len(pair) != 2 or set(conditions) != {"baseline", "candidate"}:
            raise ValueError(
                f"Invalid paired group {group!r}: expected exactly 2 requests, one baseline "
                f"and one candidate; got {len(pair)} requests with conditions {conditions!r}")
    out.mkdir(parents=True, exist_ok=False)
    rng = random.Random(args.shuffle_seed)
    items = list(groups.items())
    rng.shuffle(items)
    key, packet = {}, []
    for i, ((bid, model, seed), pair) in enumerate(items, 1):
        rng.shuffle(pair)
        pid = "pair-%03d" % i
        entry = {"pair_id": pid, "brief": briefs[bid], "outputs": []}
        for letter, request in zip("AB", pair):
            label = pid + "-" + letter
            key[label] = request
            src = run / "outputs" / request["request_id"]
            record = json.loads((src / "record.json").read_text()) if (src / "record.json").exists() else {}
            result = {"label": label, "artifact_valid": bool(record.get("artifact_valid")), "visual_review_required": True}
            for field in ("exploratory_salvage", "primary_strict_artifact_valid", "raw_contract_compliant", "normalization", "salvaged_for_visual_review"):
                if field in record:
                    result[field] = record[field]
            if result["artifact_valid"]:
                for name in ("design.svg", "content.json"):
                    data = (src / name).read_bytes()
                    expected = record["svg_sha256" if name == "design.svg" else "content_sha256"]
                    if digest(data) != expected:
                        raise ValueError("Artifact hash mismatch: " + label)
                    (out / (label + "-" + name)).write_bytes(data)
                result.update({"design": label + "-design.svg", "content": label + "-content.json"})
            else:
                result["failure"] = "No valid artifact; count as failure, not a tie or success"
            entry["outputs"].append(result)
        packet.append(entry)
    write_json(out / "review-packet.json", packet)
    # Keep identity mapping OUTSIDE the review folder.
    write_json(run / (out.name + "-private-key.json"), key)
    print(json.dumps({"pairs": len(packet), "packet": str(out), "quality_proven": False}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("prepare")
    p.add_argument("--baseline", required=True)
    p.add_argument("--candidate", required=True)
    p.add_argument("--models", nargs="+", required=True)
    p.add_argument("--seed", type=int, default=41)
    p.add_argument("--brief-count", type=int, default=2)
    p.add_argument("--briefs", default=str(ROOT / "evals/fixtures/briefs.json"))
    p.add_argument("--out", required=True)
    p.set_defaults(func=prepare)
    p = sub.add_parser("ingest")
    p.add_argument("--run", required=True)
    p.add_argument("--metadata", required=True)
    p.add_argument("--response", required=True)
    p.set_defaults(func=ingest)
    p = sub.add_parser("reprocess")
    p.add_argument("--run", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--note", required=True)
    p.set_defaults(func=reprocess)
    p = sub.add_parser("salvage")
    p.add_argument("--run", required=True)
    p.add_argument("--out", required=True)
    p.set_defaults(func=salvage)
    p = sub.add_parser("blind")
    p.add_argument("--run", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--shuffle-seed", type=int, default=712)
    p.set_defaults(func=blind)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
