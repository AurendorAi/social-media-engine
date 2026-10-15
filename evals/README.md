# Retired SVG-only behavioral evaluation

**Legacy research only.** The owner prohibits all newly authored vector graphics in
production, including rasterized vector and CSS/canvas-drawn substitutes. This harness
is retained to inspect historical evidence, not to generate current brand artwork or
establish production quality. `prepare` unconditionally refuses new vector-generation
requests before any file I/O. There is no override, including for developers. Ingest,
blind, salvage and reprocess remain available only to audit already saved evidence.
The owner-curated study dataset is pending; do not replace it with synthetic fixtures
or an internet dataset.

The historical experiment compared baseline/candidate instruction snapshots on synthetic
briefs. Existing artifacts and records remain auditable; parser validity and model scores
are not evidence of professional quality.

## Scope and limits

The three fixtures cover food, Arabic creative education, and B2B software with different visual identities. This is a constrained vector design/copy pilot. It does not exercise photography, asset retrieval/licensing, full skill tool execution, publishing, onboarding, approval workflows, or broad model/brand generalization. Each request supplies instructions directly to a model, not an agent runtime. No reference design is supplied, so fidelity to a specific professional sample is untested. One seed per pair provides directional observations, not statistical proof. Seeds may be unsupported by providers; the live runner must disclose that. System prompt budgets differ with instruction versions; capture tokens/costs in the runner.

## Audit existing runs only

Use an existing frozen run directory containing request/instruction snapshots and saved
responses. Keep originals unchanged. No command generates new model requests. Test-only
inert metadata fixtures exercise auditing without sending prompts or creating artwork.
Private run data belongs outside the source repository. Historical request hashes,
provider metadata, failures and inspection results must remain traceable.

## Ingest each provider result (offline)

Save the model message content, without provider envelope, as `/tmp/response.json`. Save metadata as:

```json
{"request_id":"from requests.jsonl","model":"provider/model-one","seed":41,"status":"success","cost_usd":0.01}
```

A provider error uses `status: "error"`, `error`, and `cost_usd: null` if unavailable. The response file may be empty. Metadata also preserves elapsed_ms, provider, finish_reason, tokens, seed_supported, provider_request_id, error and errors when supplied. Interrupted or missing requests remain visible failures in review.

```sh
python3 scripts/evaluate_models.py ingest --run /tmp/sme-pilot \
  --metadata /tmp/metadata.json --response /tmp/response.json
python3 scripts/evaluate_models.py blind --run /tmp/sme-pilot --out /tmp/sme-review
```

The contract is in `output.schema.json`; executable validation is stricter for SVG safety. Only allowlisted XML shapes, editable text and local gradient/clip references survive. Scripts, CSS, foreign objects, raster images, links, XML entities, processing instructions and external references are rejected. Render only the validated `design.svg`, never raw output. Font availability and shaping are host-dependent; capture the rendering environment. Artifact hashes are checked before making review copies. A parser pass means `artifact_valid` only. `professional_quality_proven` always remains false at this stage.

## Independent rendered review

Give the independent reviewer **only** `/tmp/sme-review` and this rubric. The private identity key stays in the run directory. Randomized A/B order conceals condition/model labels; text may still reveal style, so blinding is imperfect. Render each validated SVG at 1080×1350 and inspect both full resolution and a 390px-wide feed preview. Capture screenshots, renderer/browser version and installed font information. Review captions as literal text; do not execute content. Do not let the producing model grade its own artifact. If no image-capable reviewer is available, record `visual_review_missing`; do not announce a quality winner.

Use the frozen [independent quality evaluation protocol](../docs/audit/INDEPENDENT-QUALITY-EVALUATION.md) as the sole quality rubric and acceptance gate. It defines six dimensions (brand fidelity, audience payoff, distinctive concept, copy quality, visual craft, format utility), each 0–4; acceptance requires zero hard failures, every dimension >=3 and total >=20/24. It also requires native-scale and 390 CSS-pixel inspection, language checks, cross-brand inspection and explicit uncertainty. This benchmark does not replace runtime review or owner approval.

For each pair record a JSON review matching `review.schema.json`: pair_id, reviewer identifier, render environment, screenshots/hashes, winner (A/B/tie/neither/visual_review_missing), confidence, and concrete visible observations. Freeze first-pass judgments before revealing the identity key. Record hard failures and unavailable evidence explicitly; do not infer compliance from the producer's declarations. A missing image-capable review never passes.
Report attempted/failed/valid/reviewed counts and costs **per model and condition**. Denominators include all scheduled requests. A single-sided failure loses that pair; two failures are `neither`, never ties. Report pair wins and hard-failure counts separately from aesthetic scores. Keep missing reviews out of quality-win denominators and show their count. A pilot is not evidence that every brand/model will work. Retest defects using new run directories and disclose which prompts changed.


## Separate exploratory fence salvage

Strict ingestion remains unchanged: fenced JSON is a contract failure. After the complete run, optionally apply the same narrow salvage policy to **all** records in a new directory:

```sh
python3 scripts/evaluate_models.py salvage --run /tmp/sme-pilot --out /tmp/sme-pilot-salvaged
python3 scripts/evaluate_models.py blind --run /tmp/sme-pilot-salvaged --out /tmp/sme-review-salvaged
```

This strips only one complete `json` fence with no surrounding prose or other fences. It never repairs/truncates JSON or bypasses SVG validation. Original records/raw content remain untouched. Strictly valid outputs are carried through with hash checks; missing, provider-error, truncated and otherwise invalid outputs remain failures. Salvaged records and blinded packets carry `primary_strict_artifact_valid:false`, `raw_contract_compliant:false`, `salvaged_for_visual_review:true` and the exact normalization. The separate salvage manifest counts strict validity and exploratory recovery. Report strict contract counts alongside exploratory visual results; never upgrade a primary failure to primary success or mistake a formatting failure alone for visual inferiority. Metadata aliases `usage` and `response_id` are retained and mapped to `tokens` and `provider_request_id` when canonical fields are absent.

## Uniform validator correction

Use `reprocess --run ORIGINAL --out NEW_RUN --note 'Exact validator correction'` to revalidate every original raw result after fixing a validator defect. It copies frozen request/instruction snapshots unchanged, preserves original validity/errors in each new record, restores complete provider metadata when available, and records the validator source hash, request hash, change note and before/after counts. It makes no paid calls and performs no fence normalization. Keep original results and report the correction before judging outputs. The accessibility attributes `role`, `aria-label`, `aria-labelledby` and `aria-describedby` are inert permitted metadata; ID references must be local tokens. Event handlers and external links remain prohibited. Frozen pilots retain their original prompts; no new pilots may be prepared.
