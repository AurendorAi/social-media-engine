import argparse
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("evaluate_models", ROOT / "scripts/evaluate_models.py")
evalmod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evalmod)
SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1350"><rect width="1080" height="1350" fill="#fff"/><text x="50" y="90">Hello</text></svg>'


class EvaluationTests(unittest.TestCase):
    def test_editable_svg_accepts_arabic_and_local_gradient(self):
        svg = SVG.replace('<rect', '<defs><linearGradient id="tone"><stop offset="0" stop-color="#fff"/></linearGradient></defs><rect').replace('fill="#fff"', 'fill="url(#tone)"').replace('Hello', 'نبتة')
        self.assertIn('نبتة', evalmod.validate_svg(svg))

    def test_active_external_and_disguised_svg_rejected(self):
        attacks = ['<script>alert(1)</script>', '<foreignObject/>', '<image href="https://bad.test/x"/>', '<style>text{fill:red}</style>', '<use href="#x"/>', '<g xmlns="urn:evil"/>']
        for attack in attacks:
            with self.subTest(attack=attack), self.assertRaises(ValueError):
                evalmod.validate_svg(SVG.replace('</svg>', attack + '</svg>'))
        for attribute in ['onclick="alert(1)"', 'style="fill:red"', 'fill="url(https://bad.test)"']:
            with self.subTest(attribute=attribute), self.assertRaises(ValueError):
                evalmod.validate_svg(SVG.replace('<text ', '<text ' + attribute + ' '))
        with self.assertRaises(ValueError):
            evalmod.validate_svg('<!DOCTYPE svg [<!ENTITY x "boom">]>' + SVG)

    def test_rejects_noneditable_or_wrong_canvas(self):
        with self.assertRaises(ValueError):
            evalmod.validate_svg(SVG.replace('Hello', ''))
        with self.assertRaises(ValueError):
            evalmod.validate_svg(SVG.replace('1080 1350', '800 800'))

    def test_accessibility_attributes_are_inert_and_local(self):
        valid = SVG.replace('<svg ', '<svg role="img" aria-label="نبتة ورشة" aria-labelledby="title" aria-describedby="description" ')
        self.assertIn('role="img"', evalmod.validate_svg(valid))
        for attribute in ['role="javascript:alert(1)"', 'aria-labelledby="https://bad.test/x"', 'aria-describedby="#external"', 'onclick="bad()"', 'href="https://bad.test/x"']:
            with self.subTest(attribute=attribute), self.assertRaises(ValueError):
                evalmod.validate_svg(SVG.replace('<svg ', '<svg ' + attribute + ' '))

    def test_root_dimensions_normalized_or_rejected(self):
        self.assertIn('width="1080"', evalmod.validate_svg(SVG))
        with self.assertRaises(ValueError):
            evalmod.validate_svg(SVG.replace('<svg ', '<svg width="100" '))

    def test_production_slice_includes_patterns_excludes_runtime(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            base = root / 'skills/social-media-engine'
            for relative in evalmod.SELECTED:
                target = base / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text('pattern fixture' if relative.endswith('.json') else 'creative guidance')
            (base / 'references/runtime.md').write_text('FORBIDDEN RUNTIME FIXTURE')
            system, manifest = evalmod.instruction_bundle(root)
            self.assertIn('pattern fixture', system)
            self.assertNotIn('FORBIDDEN RUNTIME FIXTURE', system)
            self.assertTrue(system.startswith(evalmod.PREAMBLE))
            self.assertIn('assets/design-patterns.json', [x['path'] for x in manifest])
            self.assertTrue(all(len(x['sha256']) == 64 for x in manifest))

    def test_paired_prompts_failures_hashes_and_blind_mapping(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            baseline, candidate = base / 'baseline.md', base / 'candidate.md'
            baseline.write_text('Baseline guidance')
            candidate.write_text('Candidate guidance')
            run, review = base / 'run', base / 'review'
            evalmod.prepare(argparse.Namespace(out=str(run), briefs=str(ROOT / 'evals/fixtures/briefs.json'), brief_count=3, models=['model/a'], seed=41, baseline=str(baseline), candidate=str(candidate)))
            requests = list(map(json.loads, (run / 'requests.jsonl').read_text().splitlines()))
            self.assertEqual(len(requests), 6)
            for first, second in zip(requests[:3], requests[3:]):
                self.assertEqual(first['prompt_sha256'], second['prompt_sha256'])
                self.assertNotEqual(first['instruction_sha256'], second['instruction_sha256'])
            response, meta = base / 'response.json', base / 'meta.json'
            response.write_text(json.dumps({'caption': 'Useful caption', 'alt_text': 'Description', 'source_notes': [], 'design': {'format': 'svg', 'width': 1080, 'height': 1350, 'svg': SVG}}))
            first = requests[0]
            meta.write_text(json.dumps({'request_id': first['request_id'], 'model': first['model'], 'seed': 41, 'cost_usd': .01, 'status': 'success', 'elapsed_ms': 123, 'provider': 'fixture-provider', 'finish_reason': 'stop', 'tokens': {'total': 100}, 'seed_supported': False}))
            evalmod.ingest(argparse.Namespace(run=str(run), metadata=str(meta), response=str(response)))
            record = json.loads((run / 'outputs' / first['request_id'] / 'record.json').read_text())
            self.assertEqual(record['elapsed_ms'], 123)
            self.assertEqual(record['tokens'], {'total': 100})
            self.assertFalse(record['seed_supported'])
            self.assertTrue(record['artifact_valid'])
            self.assertFalse(record['professional_quality_proven'])
            evalmod.blind(argparse.Namespace(run=str(run), out=str(review), shuffle_seed=9))
            packet = json.loads((review / 'review-packet.json').read_text())
            self.assertEqual(sum(x['artifact_valid'] for p in packet for x in p['outputs']), 1)
            self.assertNotIn('model/a', (review / 'review-packet.json').read_text())
            self.assertFalse((review / 'private-key.json').exists())
            self.assertTrue((run / 'review-private-key.json').exists())
            (run / 'outputs' / first['request_id'] / 'design.svg').write_text(SVG + 'tampered')
            with self.assertRaises(ValueError):
                evalmod.blind(argparse.Namespace(run=str(run), out=str(base / 'review2'), shuffle_seed=9))

    def test_prepare_rejects_duplicate_ids_before_creating_output(self):
        for duplicate in ('models', 'briefs'):
            with self.subTest(duplicate=duplicate), tempfile.TemporaryDirectory() as folder:
                base = Path(folder)
                briefs = base / 'briefs.json'
                briefs.write_text(json.dumps([{'id': 'one'}, {'id': 'one' if duplicate == 'briefs' else 'two'}]))
                out = base / 'run'
                args = argparse.Namespace(out=str(out), briefs=str(briefs), brief_count=2,
                                          models=['model/a', 'model/a'] if duplicate == 'models' else ['model/a'],
                                          seed=41, baseline='unused', candidate='unused')
                with self.assertRaisesRegex(ValueError, 'Duplicate .* IDs'):
                    evalmod.prepare(args)
                self.assertFalse(out.exists())

    def test_blind_rejects_malformed_pairs_before_creating_output(self):
        cases = [('baseline',), ('baseline', 'candidate', 'candidate'),
                 ('baseline', 'baseline'), ('candidate', 'candidate'),
                 ('baseline', 'unknown')]
        for conditions in cases:
            with self.subTest(conditions=conditions), tempfile.TemporaryDirectory() as folder:
                base = Path(folder)
                run, out = base / 'run', base / 'review'
                run.mkdir()
                (run / 'briefs.json').write_text(json.dumps([{'id': 'one'}, {'id': 'two'}]))
                # A valid group first ensures validation covers all groups before any writes.
                requests = [{'request_id': f'valid-{condition}', 'brief_id': 'one',
                             'model': 'model/a', 'seed': 41, 'condition': condition}
                            for condition in ('baseline', 'candidate')]
                requests += [{'request_id': f'invalid-{i}', 'brief_id': 'two',
                              'model': 'model/a', 'seed': 41, 'condition': condition}
                             for i, condition in enumerate(conditions)]
                (run / 'requests.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in requests))
                with self.assertRaisesRegex(ValueError, 'expected exactly 2 requests, one baseline and one candidate'):
                    evalmod.blind(argparse.Namespace(run=str(run), out=str(out), shuffle_seed=9))
                self.assertFalse(out.exists())
                self.assertFalse((run / 'review-private-key.json').exists())

    def test_exact_fence_salvage_preserves_strict_failure_and_raw(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            instruction = base / 'instruction.md'
            instruction.write_text('Fixture')
            run, out = base / 'run', base / 'salvaged'
            evalmod.prepare(argparse.Namespace(out=str(run), briefs=str(ROOT / 'evals/fixtures/briefs.json'), brief_count=1, models=['model/a'], seed=41, baseline=str(instruction), candidate=str(instruction)))
            requests = list(map(json.loads, (run / 'requests.jsonl').read_text().splitlines()))
            value = {'caption': 'Useful', 'alt_text': 'Description', 'source_notes': [], 'design': {'format': 'svg', 'width': 1080, 'height': 1350, 'svg': SVG}}
            raw = ('```json\n' + json.dumps(value) + '\n```').encode()
            response, meta = base / 'raw.txt', base / 'meta.json'
            response.write_bytes(raw)
            for request in requests:
                meta.write_text(json.dumps({'request_id': request['request_id'], 'model': 'model/a', 'seed': 41, 'status': 'success', 'cost_usd': .01, 'usage': {'total_tokens': 50}, 'response_id': 'provider-fixture'}))
                evalmod.ingest(argparse.Namespace(run=str(run), metadata=str(meta), response=str(response)))
            originals = {r['request_id']: (run / 'outputs' / r['request_id'] / 'record.json').read_bytes() for r in requests}
            reprocessed = base / 'reprocessed'
            evalmod.reprocess(argparse.Namespace(run=str(run), out=str(reprocessed), note='Test uniform revalidation'))
            self.assertEqual((run / 'requests.jsonl').read_bytes(), (reprocessed / 'requests.jsonl').read_bytes())
            report = json.loads((reprocessed / 'reprocess-manifest.json').read_text())
            self.assertEqual(report['counts']['reprocessed_valid'], 0)
            evalmod.salvage(argparse.Namespace(run=str(run), out=str(out)))
            for request in requests:
                rid = request['request_id']
                self.assertEqual(originals[rid], (run / 'outputs' / rid / 'record.json').read_bytes())
                record = json.loads((out / 'outputs' / rid / 'record.json').read_text())
                self.assertTrue(record['artifact_valid'])
                self.assertFalse(record['primary_strict_artifact_valid'])
                self.assertFalse(record['raw_contract_compliant'])
                self.assertEqual(record['normalization'], 'removed_one_complete_json_fence')
                self.assertEqual(record['tokens'], {'total_tokens': 50})
                self.assertEqual(record['provider_request_id'], 'provider-fixture')
                self.assertEqual(raw, (out / 'outputs' / rid / 'raw-response.txt').read_bytes())
            evalmod.blind(argparse.Namespace(run=str(out), out=str(base / 'review'), shuffle_seed=9))
            packet = json.loads((base / 'review/review-packet.json').read_text())
            self.assertTrue(all(x['salvaged_for_visual_review'] for x in packet[0]['outputs']))

    def test_fence_salvage_rejects_prose_truncation_and_multiple_blocks(self):
        for raw in [b'Here it is\n```json\n{}\n```', b'```json\n{\n```', b'```json\n{}', b'```json\n{}\n```\n```json\n{}\n```', b'{}', b'```\n{}\n```']:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                evalmod.unwrap_json_fence(raw)

    def test_invalid_output_is_not_success(self):
        with self.assertRaises(ValueError):
            evalmod.validate_output({'caption': 'a', 'alt_text': 'b', 'source_notes': [], 'design': {'format': 'svg', 'width': 1080, 'height': 1350, 'svg': SVG.replace('<text ', '<text onclick="bad" ')}})


if __name__ == '__main__':
    unittest.main()
