import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'plugins/social-media-engine/scripts/design_patterns.py'
spec = importlib.util.spec_from_file_location('design_patterns', SCRIPT)
patterns = importlib.util.module_from_spec(spec)
spec.loader.exec_module(patterns)


class DesignPatternsTests(unittest.TestCase):
    def test_compact_retrieval_preserves_evidence_boundary(self):
        result = patterns.retrieve(intent='compare', format='carousel')
        self.assertEqual([p['id'] for p in result['patterns']], ['comparable-pair'])
        self.assertIn('not an empirical', result['evidence_status'])
        self.assertEqual(len(result['sources']), 3)
        self.assertIn('not a suitability score', result['retrieval']['method'])

    def test_intersection_does_not_silently_broaden(self):
        result = patterns.retrieve(intent='compare', format='story')
        self.assertEqual(result['patterns'], [])
        self.assertEqual(result['retrieval']['count'], 0)
        with self.assertRaises(ValueError):
            patterns.retrieve(intent='comapre')
        with self.assertRaises(ValueError):
            patterns.retrieve(pattern_id='missing')

    def test_cli_is_portable_outside_workspace(self):
        result = subprocess.run([sys.executable, str(SCRIPT), '--id', 'artifact-with-context'],
                                cwd=SCRIPT.parent.parent, capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(result.stdout)['patterns'][0]['id'], 'artifact-with-context')
        bad = subprocess.run([sys.executable, str(SCRIPT), '--format', 'reel'],
                             capture_output=True, text=True)
        self.assertEqual(bad.returncode, 2)
        self.assertIn('Unknown format', bad.stderr)

    def test_guidance_records_are_actionable_and_originally_attributed(self):
        result = patterns.retrieve()
        ids = [p['id'] for p in result['patterns']]
        self.assertEqual(len(ids), len(set(ids)))
        for p in result['patterns']:
            with self.subTest(pattern=p['id']):
                for field in ('use_when', 'avoid_when', 'weak', 'better', 'check'):
                    self.assertTrue(p[field].strip())
                self.assertNotEqual(p['weak'], p['better'])
                self.assertGreaterEqual(len(p['composition']), 2)
                self.assertGreaterEqual(len(p['adapt']), 2)
                self.assertEqual(p['provenance'], 'original-synthesis')


if __name__ == '__main__':
    unittest.main()
