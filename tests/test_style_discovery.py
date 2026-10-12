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
