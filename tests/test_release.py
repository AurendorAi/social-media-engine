"""Validate native packaging, portability and the exact release ZIP."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/social-media-engine"


class ReleaseTests(unittest.TestCase):
    def test_extracted_plugin_runs_outside_repository_with_space_in_path(self):
        spec = importlib.util.spec_from_file_location("build_release", ROOT / "scripts/build_release.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        archive = module.build()
        with tempfile.TemporaryDirectory(prefix="install with spaces ") as folder:
            base = Path(folder)
            install = base / "plugin cache" / "social-media-engine"
            work = base / "private working folder"
            work.mkdir()
            with zipfile.ZipFile(archive) as bundle:
                bundle.extractall(install)
            env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
            env.pop("PYTHONPATH", None)
            for key in ("POSTIZ_API_KEY", "POSTIZ_API_URL", "SOCIAL_ENGINE_ALLOW_PUBLISH"):
                env.pop(key, None)
            before = {p.relative_to(install): hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in install.rglob("*") if p.is_file()}
            run = subprocess.run([sys.executable, str(install / "scripts/sme.py"), "--workspace", str(work),
                                  "--brand", "new-brand", "status"], capture_output=True, text=True,
                                 env=env, cwd=work, timeout=10)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads(run.stdout)["state"], "ONBOARDING_REQUIRED")
            self.assertTrue((work / ".social-media-engine/state.sqlite3").is_file())
            self.assertFalse((install / ".social-media-engine").exists())
            libraries = subprocess.run(
                [sys.executable, str(install / "scripts/sme.py"), "--workspace", str(work),
                 "--brand", "new-brand", "resource-libraries"], capture_output=True, text=True,
                env=env, cwd=work, timeout=10)
            self.assertEqual(libraries.returncode, 0, libraries.stderr)
            self.assertIn("openverse", libraries.stdout.lower())

            def cli(command, *args, body=None, brand="new-brand", success=True):
                argv = [sys.executable, str(install / "scripts/sme.py"), "--workspace", str(work),
                        "--brand", brand, command, *args]
                if body is not None:
                    payload = work / "authored input.json"
                    payload.write_text(json.dumps(body), encoding="utf-8")
                    argv += ["--file", str(payload)]
                result = subprocess.run(argv, capture_output=True, text=True, env=env, cwd=work, timeout=10)
                self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
                return json.loads(result.stdout or result.stderr)

            catalog = cli("style-catalog")
            self.assertEqual(len(catalog["styles"]), 27)
            self.assertEqual(cli("status")["style_discovery"]["state"], "NEEDS_SAMPLES")

            # Reuse public fixture data only; the child process imports exclusively
            # from its extracted install, never the repository's runtime modules.
            from test_engine import PROFILE
            self.assertEqual(cli("creative-brief")["state"], "MISSING")
            cli("brand-update", "--actor", "Test Owner", body=PROFILE)
            profile_hash = cli("status")["profile"]["hash"]
            cli("brand-approve", "--hash", profile_hash, "--actor", "Test Owner")
            brief = {
                "id": "portable-brief", "brand_hash": profile_hash,
                "audience_situation": "Home brewers comparing simple routines",
                "brand_promise": "Explain one practical brewing choice",
                "proof_points": ["Use owner-reviewed source notes"],
                "voice_examples": {
                    "good": [{"text": "Change one variable.", "why": "Concrete action"}],
                    "avoid": [{"text": "Perfect results guaranteed", "why": "Unsupported promise"}]},
                "visual_principles": ["One focal point"],
                "content_pillars": ["Practical technique"],
                "anti_patterns": ["Invented results"],
                "asset_strategy": "Use reviewed original assets",
                "success_criteria": ["Useful specific questions"],
                "source_notes": ["Fictional packaging fixture; no external claims"],
                "sample_asset_ids": []}
            proposed = cli("creative-brief-save", "--actor", "Test Author", body=brief)
            self.assertFalse(proposed["approved"])
            self.assertEqual(cli("creative-brief")["state"], "PROPOSED")
            cli("creative-brief-approve", "--id", proposed["id"], "--hash", "wrong-hash",
                "--actor", "Test Owner", success=False)
            cli("creative-brief-approve", "--id", proposed["id"], "--hash", proposed["hash"],
                "--actor", "Test Owner")
            memory = cli("creative-brief")
            self.assertEqual(memory["state"], "APPROVED")
            self.assertTrue(memory["gaps"], "A brief with no samples must not imply visual calibration")
            self.assertEqual(cli("creative-brief", brand="other-brand")["state"], "MISSING")
            after = {p.relative_to(install): hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in install.rglob("*") if p.is_file()}
            self.assertEqual(before, after, "Installed runtime must not write to its package cache")

    def test_builder_rejects_stale_or_wrong_marketplace_sources(self):
        spec = importlib.util.spec_from_file_location("build_release", ROOT / "scripts/build_release.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        version = json.loads((PLUGIN / "plugin.json").read_text())["version"]
        cases = [(".claude-plugin/marketplace.json", "version", "0.0.0"),
                 (".claude-plugin/marketplace.json", "source", "./wrong-plugin"),
                 (".agents/plugins/marketplace.json", "source", {"source": "local", "path": "./wrong-plugin"}),
                 (".agents/plugins/marketplace.json", "name", "wrong-plugin")]
        for relative, field, value in cases:
            with self.subTest(relative=relative, field=field), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                for name in (".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json"):
                    data = json.loads((ROOT / name).read_text())
                    if name == relative:
                        data["plugins"][0][field] = value
                    target = root / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(json.dumps(data))
                with patch.object(module, "ROOT", root), patch.object(module, "PLUGIN", root / "plugins/social-media-engine"):
                    with self.assertRaises(ValueError):
                        module.validate_marketplaces("social-media-engine", version)

    def test_native_manifests_and_marketplaces_agree(self):
        codex = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text())
        claude = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text())
        self.assertEqual(codex["name"], PLUGIN.name)
        self.assertEqual(claude["name"], PLUGIN.name)
        self.assertEqual(codex["version"], claude["version"])
        portable = json.loads((PLUGIN / "plugin.json").read_text())
        self.assertEqual(portable["version"], codex["version"])
        self.assertEqual(portable["name"], codex["name"])
        cm = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
        am = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
        self.assertEqual((ROOT / cm["plugins"][0]["source"]["path"]).resolve(), PLUGIN)
        self.assertEqual((ROOT / am["plugins"][0]["source"]).resolve(), PLUGIN)
        self.assertEqual(am["plugins"][0]["version"], codex["version"])
        self.assertEqual(cm["plugins"][0]["policy"]["installation"], "AVAILABLE")
        self.assertTrue((PLUGIN / codex["skills"]).is_dir())

    def test_skill_is_self_contained_and_links_resolve(self):
        for file in (PLUGIN / "skills").rglob("*.md"):
            source = file.read_text()
            self.assertNotIn("/Users/", source)
            self.assertNotIn("Content OS", source)
            for link in re.findall(r"\]\(([^)]+)\)", source):
                if "://" not in link and not link.startswith("#"):
                    target = (file.parent / link.split("#")[0]).resolve()
                    self.assertTrue(target.is_file(), (file, link))
                    self.assertIn(PLUGIN, target.parents)

    def test_build_is_small_deterministic_and_contains_no_private_data(self):
        spec = importlib.util.spec_from_file_location("build_release", ROOT / "scripts/build_release.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        first = module.build()
        first_hash = hashlib.sha256(first.read_bytes()).hexdigest()
        second = module.build()
        self.assertEqual(first_hash, hashlib.sha256(second.read_bytes()).hexdigest())
        self.assertLess(first.stat().st_size, 1_000_000)
        with zipfile.ZipFile(first) as archive:
            self.assertIsNone(archive.testzip())
            names = archive.namelist()
            self.assertIn("plugin.json", names)
            self.assertIn(".claude-plugin/plugin.json", names)
            self.assertIn(".codex-plugin/plugin.json", names)
            for name in names:
                self.assertFalse(name.startswith("/"))
                self.assertNotIn("..", Path(name).parts)
                self.assertFalse(any(part in name for part in [
                    ".data/", ".git/", "node_modules/", ".env", "__pycache__", "state.sqlite3"]))
