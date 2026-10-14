"""Explicit, brand-scoped creative proposals. No generation or implicit approvals."""
from datetime import datetime, timezone
from engine import EngineError, digest, identifier, instant, now, require, string_list, text

TEXT_FIELDS = {"audience_situation", "brand_promise", "asset_strategy"}
LIST_FIELDS = {"proof_points", "visual_principles", "content_pillars", "anti_patterns", "success_criteria", "source_notes"}
FIELDS = TEXT_FIELDS | LIST_FIELDS | {"voice_examples"}


def rules_hash(ws, brand):
    rules = [r for r in ws.list("rule", brand) if r.get("approved") and not r.get("retired")
             and (not r.get("expires_at") or instant(r["expires_at"]) > datetime.now(timezone.utc))]
    return digest(sorted(rules, key=lambda r: r["id"]))


def clean(value):
    require(isinstance(value, dict), "Creative brief must be an object.")
    require(not set(value) - (FIELDS | {"id", "brand_hash", "sample_asset_ids"}), "Unknown creative brief fields.")
    require(FIELDS <= set(value), "Complete all creative brief fields, including source_notes and voice_examples.")
    result = {k: text(value[k], k, 6000) for k in TEXT_FIELDS}
    for field in LIST_FIELDS:
        result[field] = string_list(value[field], field, True)
        require(len(result[field]) <= 40, f"{field} must contain at most 40 entries.")
    examples = value["voice_examples"]
    require(isinstance(examples, dict) and set(examples) == {"good", "avoid"}, "voice_examples needs good and avoid arrays.")
    result["voice_examples"] = {}
    for category in ("good", "avoid"):
        rows = examples[category]
        require(isinstance(rows, list) and 1 <= len(rows) <= 20, "Provide 1-20 examples per voice category.")
        result["voice_examples"][category] = []
        for row in rows:
            require(isinstance(row, dict) and set(row) == {"text", "why"}, "Each voice example needs only text and why.")
            result["voice_examples"][category].append({k: text(row[k], k, 4000) for k in ("text", "why")})
    ids = value.get("sample_asset_ids", [])
    require(isinstance(ids, list) and len(ids) <= 20, "sample_asset_ids must be an array of at most 20 asset IDs.")
    ids = [identifier(key) for key in ids]
    require(len(ids) == len(set(ids)), "Sample asset IDs must be unique.")
    return result, ids


def samples(ws, brand, ids):
    result = []
    for key in ids:
        try:
            asset, _ = ws.asset_bytes(brand, key)
        except OSError as exc:
            raise EngineError("Creative sample is unavailable; restore it or propose a new brief.") from exc
        require(asset["role"] in {"reference", "output"}, "Creative samples must be actual reference or output assets for this brand.")
        result.append({"id": key, "sha256": asset["sha256"], "record_hash": digest(asset)})
    return result


def stale_gaps(ws, brand, record):
    gaps = []
    content = {k: v for k, v in record.items() if k not in {"hash", "approved", "approved_by", "approved_at"}}
    if digest(content) != record["hash"]:
        gaps.append("Creative brief content no longer matches its reviewed hash.")
    profile = ws.get("brand", brand, "profile", optional=True)
    if not profile or not profile.get("approved") or profile["hash"] != record["brand_hash"]:
        gaps.append("Brand profile changed or is not approved; review a new creative brief against the current profile.")
    if rules_hash(ws, brand) != record["rules_hash"]:
        gaps.append("Approved rules changed or expired; review a new creative brief.")
    try:
        if samples(ws, brand, record["sample_asset_ids"]) != record["sample_assets"]:
            gaps.append("Creative sample records changed; import and review new samples.")
    except EngineError as exc:
        gaps.append(str(exc))
    return gaps


def save(ws, brand, value, actor):
    brief, ids = clean(value)
    key, actor = identifier(value.get("id")), text(actor, "actor", 200)
    def apply():
        profile = ws.get("brand", brand, "profile")
        require(value.get("brand_hash") == profile["hash"], "Creative brief must bind the current brand hash from status.profile.hash.")
        require(not ws.get("creative_brief", brand, key, optional=True), "Use a new creative brief ID to preserve history.")
        record = {"id": key, "brand": brand, "brand_hash": profile["hash"], "rules_hash": rules_hash(ws, brand),
                  "brief": brief, "sample_asset_ids": ids, "sample_assets": samples(ws, brand, ids),
                  "created": now(), "actor": actor}
        record["hash"] = digest(record)
        record["approved"] = False
        ws.put("creative_brief", brand, key, record)
        ws.audit(brand, "creative_brief.proposed", key, {"hash": record["hash"], "actor": actor})
        return record
    return ws.transaction(apply)


def approve(ws, brand, key, expected_hash, actor):
    actor = text(actor, "approval owner", 200)
    def apply():
        record = ws.get("creative_brief", brand, key)
        require(record["hash"] == expected_hash, "Creative brief changed; approve its exact reviewed hash.")
        gaps = stale_gaps(ws, brand, record)
        require(not gaps, "Creative brief is stale: " + " ".join(gaps))
        active = ws.get("creative_memory", brand, "active", optional=True)
        if record.get("approved"):
            require(active and active["id"] == key, "This brief was superseded; propose a new revision instead of reactivating history.")
            return record
        record.update(approved=True, approved_by=actor, approved_at=now())
        ws.put("creative_brief", brand, key, record)
        ws.put("creative_memory", brand, "active", {"id": key, "hash": record["hash"]})
        ws.audit(brand, "creative_brief.approved", key, {"hash": expected_hash, "actor": actor})
        return record
    return ws.transaction(apply)


def read(ws, brand):
    identifier(brand)
    history = ws.list("creative_brief", brand)
    pointer = ws.get("creative_memory", brand, "active", optional=True)
    result = {"brand": brand, "state": "PROPOSED" if history else "MISSING", "active": None,
              "active_id": pointer["id"] if pointer else None, "gaps": [], "history": history}
    if not pointer:
        result["gaps"] = ["No owner-approved creative brief. Use brand research and propose a distinct direction; no forced re-onboarding."]
        return result
    record = ws.get("creative_brief", brand, pointer["id"])
    gaps = stale_gaps(ws, brand, record)
    if not record.get("approved") or record["hash"] != pointer["hash"]:
        gaps.append("Creative approval no longer matches the selected brief.")
    if gaps:
        result.update(state="STALE", gaps=gaps)
    else:
        result.update(state="CALIBRATED" if record["sample_asset_ids"] else "APPROVED", active=record)
        if not record["sample_asset_ids"]:
            result["gaps"] = ["Brief approved without actual reference/output samples; visual calibration remains unvalidated."]
    return result


def context_fields(ws, brand):
    memory = read(ws, brand)
    fields = {}
    if memory["active"]:
        active = memory["active"]
        fields["creative_brief"] = {k: active[k] for k in ("id", "hash", "brief", "sample_assets")}
    elif memory["active_id"]:
        # Never revert to the pre-brief legacy hash after an approval becomes stale.
        pointer = ws.get("creative_memory", brand, "active")
        fields["creative_brief_state"] = {"id": pointer["id"], "hash": pointer["hash"], "state": "STALE"}
    readiness = {k: memory[k] for k in ("state", "active_id", "gaps")}
    return fields, readiness
