"""Synthetic creative memory fixtures; never customer assets or quality assertions."""
import copy
from test_engine import RuntimeHarness, PROFILE
from engine import digest, Workspace


class CreativeMemoryTests(RuntimeHarness):
    def brief(self, key="direction-one", brand="northstar", samples=None):
        return {
            "id": key, "brand_hash": self.call("status", brand=brand)["profile"]["hash"],
            "audience_situation": "Busy home brewers adjusting one variable before work.",
            "brand_promise": "Specific, repeatable brewing guidance, without guaranteed outcomes.",
            "proof_points": ["Owner supplied demonstration photos; results not independently measured."],
            "voice_examples": {"good": [{"text": "Change one variable in your next brew.", "why": "One concrete action."}],
                               "avoid": [{"text": "Unlock perfect coffee forever.", "why": "Vague and unverified promise."}]},
            "visual_principles": ["Real equipment, warm paper and quiet composition."],
            "content_pillars": ["Practical brewing"], "anti_patterns": ["Generic neon technology cards"],
            "asset_strategy": "Use owned demonstration photos; request original resolution.",
            "success_criteria": ["A reader can repeat the demonstrated step."],
            "source_notes": ["Synthetic test profile; no production evidence."],
            "sample_asset_ids": samples or []}

    def propose(self, value=None, brand="northstar"):
        return self.call("creative-brief-save", "--actor", "Test Author", body=value or self.brief(brand=brand), brand=brand)

    def approve(self, record, brand="northstar", ok=True):
        return self.call("creative-brief-approve", "--id", record["id"], "--hash", record["hash"], "--actor", "Test Owner", brand=brand, ok=ok)

    def sample(self, brand="northstar"):
        path = self.workspace / "synthetic-output.svg"
        path.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20"><rect width="20" height="20" fill="red"/></svg>')
        return self.call("asset-import", "--file", path, "--role", "output", "--rights", "owned", "--note", "Synthetic fixture", "--actor", "Test Author", brand=brand)

    def test_onboarding_read_and_proposal_never_approves_profile(self):
        self.assertEqual(self.call("creative-brief")["state"], "MISSING")
        self.call("brand-update", "--actor", "Test Owner", body={"name": "Unfinished Fictional Brand"})
        record = self.propose()
        self.assertEqual(self.call("creative-brief")["state"], "PROPOSED")
        self.approve(record, ok=False)
        self.assertFalse(self.call("status")["profile"]["approved"])

    def test_legacy_hash_and_approved_content_survive_proposals(self):
        before = self.ready()
        base = {k: v for k, v in before.items() if k not in {"context_hash", "creative_memory"}}
        self.assertEqual(before["context_hash"], digest(base))
        item = self.approve_text()
        record = self.propose()
        after = self.call("context")
        self.assertEqual(before["context_hash"], after["context_hash"])
        self.assertNotIn("creative_brief", after)
        ws = Workspace(str(self.workspace))
        try:
            self.assertEqual(ws.current_item("northstar", item["id"])["status"], "APPROVED")
            ctx = ws.item_context("northstar", item)
            self.assertEqual(ctx["context_hash"], digest({k: v for k, v in ctx.items() if k not in {"context_hash", "creative_memory"}}))
        finally:
            ws.close()
        self.approve(record)
        snap = self.call("snapshot")
        self.assertEqual(snap["items"][0]["effective_status"], "STALE")
        self.assertEqual(snap["creative_memory"]["state"], "APPROVED")
        self.assertTrue(snap["creative_memory"]["gaps"])
        self.assertEqual(len(snap["creative_briefs"]), 1)
        self.call("item-approve", "--id", item["id"], "--hash", item["hash"], "--actor", "Test Owner", ok=False)

    def test_two_fictional_brands_have_distinct_active_memory(self):
        self.ready()
        other = copy.deepcopy(PROFILE)
        other.update(name="Kiteworks Studio", voice="Precise and restrained", visual_style="Monochrome drafting diagrams")
        self.ready("kiteworks", other)
        one = self.propose()
        second = self.brief(brand="kiteworks")
        second["voice_examples"]["good"][0]["text"] = "Inspect the joint before finishing."
        second["visual_principles"] = ["Monochrome construction diagrams with measured detail."]
        two = self.propose(second, "kiteworks")
        self.approve(one)
        self.approve(two, "kiteworks")
        a, b = self.call("context"), self.call("context", brand="kiteworks")
        self.assertNotEqual(a["creative_brief"]["brief"], b["creative_brief"]["brief"])
        self.assertNotIn("construction", str(a["creative_brief"]))
        self.assertEqual(len(self.call("creative-brief", brand="kiteworks")["history"]), 1)
        asset = self.sample()
        self.call("creative-brief-save", "--actor", "Test Author", body=self.brief("foreign-asset", "kiteworks", [asset["id"]]), brand="kiteworks", ok=False)

    def test_exact_hash_and_profile_staleness_rejected(self):
        self.ready()
        record = self.propose()
        self.call("creative-brief-approve", "--id", record["id"], "--hash", "wrong", "--actor", "Owner", ok=False)
        self.call("brand-update", "--actor", "Owner", body={"voice": "A new voice"})
        self.call("brand-approve", "--hash", self.call("status")["profile"]["hash"], "--actor", "Owner")
        self.approve(record, ok=False)
        self.assertNotIn("creative_brief", self.call("context"))

    def test_samples_integrity_and_no_stale_fallback(self):
        self.ready()
        asset = self.sample()
        record = self.propose(self.brief(samples=[asset["id"]]))
        self.approve(record)
        valid = self.call("context")
        self.assertEqual(valid["creative_memory"]["state"], "CALIBRATED")
        path = self.workspace / ".social-media-engine" / asset["path"]
        path.write_text("mutated bytes")
        stale = self.call("context")
        self.assertEqual(stale["creative_memory"]["state"], "STALE")
        self.assertNotIn("creative_brief", stale)
        self.assertNotEqual(valid["context_hash"], stale["context_hash"])
        self.approve(record, ok=False)
        self.assertEqual(self.call("snapshot")["creative_memory"]["state"], "STALE")

    def test_sample_mutation_before_approval_rejected(self):
        self.ready()
        asset = self.sample()
        record = self.propose(self.brief(samples=[asset["id"]]))
        (self.workspace / ".social-media-engine" / asset["path"]).unlink()
        self.approve(record, ok=False)
        self.assertIsNone(self.call("creative-brief")["active"])

    def test_rules_and_replacement_invalidate_context(self):
        self.ready()
        one = self.propose()
        self.approve(one)
        first = self.call("context")["context_hash"]
        two = self.propose(self.brief("second"))
        self.assertEqual(first, self.call("context")["context_hash"])
        self.approve(two)
        self.assertNotEqual(first, self.call("context")["context_hash"])
        self.approve(one, ok=False)
        self.call("feedback", body={"id": "shorter", "instruction": "Keep headlines short.", "category": "preference", "actor": "Owner"})
        self.assertEqual(self.call("creative-brief")["state"], "APPROVED")
        self.call("rule-approve", "--id", "shorter", "--actor", "Owner")
        self.assertEqual(self.call("creative-brief")["state"], "STALE")
        self.approve(two, ok=False)

    def test_bad_inputs_are_not_saved(self):
        self.ready()
        for mutate in [lambda v: v.update(source_notes=[]), lambda v: v.update(source_notes=[{"url": "untyped"}]),
                       lambda v: v.update(unrelated_secret="no"), lambda v: v.update(sample_asset_ids="not-array"),
                       lambda v: v.update(voice_examples={"good": [], "avoid": []}),
                       lambda v: v.update(source_notes=["sk-" + "a" * 30])]:
            value = self.brief()
            mutate(value)
            self.call("creative-brief-save", "--actor", "Author", body=value, ok=False)
        self.assertEqual(self.call("creative-brief")["history"], [])

    def test_record_and_sample_metadata_mutation_do_not_reuse_approval(self):
        self.ready()
        asset = self.sample()
        record = self.propose(self.brief(samples=[asset["id"]]))
        ws = Workspace(str(self.workspace))
        try:
            changed = ws.get("creative_brief", "northstar", record["id"])
            changed["brief"]["brand_promise"] = "Changed after review"
            ws.put("creative_brief", "northstar", record["id"], changed)
        finally:
            ws.close()
        self.approve(record, ok=False)
        new = self.propose(self.brief("new", samples=[asset["id"]]))
        self.approve(new)
        ws = Workspace(str(self.workspace))
        try:
            changed = ws.get("asset", "northstar", asset["id"])
            changed["rights"] = "unknown"
            ws.put("asset", "northstar", asset["id"], changed)
        finally:
            ws.close()
        self.assertEqual(self.call("creative-brief")["state"], "STALE")
