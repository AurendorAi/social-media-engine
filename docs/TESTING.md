# Testing

All test writes stay in ignored `.data/` and `dist/` inside this repository.
Tests clear provider environment variables and use local fake HTTP services.
Never add real brand accounts, API keys, or owner approval to test fixtures.

## Standard-library suite
```sh
python3 -m unittest discover -s tests -v
python3 scripts/build_release.py
```

Coverage includes resumable first-run onboarding, separate brands, current context,
scoped deterministic caption constraints, immutable revisions, reference/media integrity,
required independent review roles, stale approvals, owner change requests, real export
bytes, timezone-aware plans, evidence-labelled metric records, dashboard authorization,
origin/host protection, provider-account binding, partial/ambiguous writes, no blind
retries, reconciliation, native manifests, portable ZIP layout and deterministic builds.

The automated reviews and metrics in unit tests are explicitly synthetic fixtures.
They must never be copied into a real brand workspace as genuine approval or evidence.

## Browser and actual-media exercise
Optional developer dependencies: Node.js, Playwright, Chromium/Chrome, and ffmpeg.
Install these in your development environment, not as required plugin runtime dependencies.

```sh
npm install --no-save --package-lock=false playwright
npx playwright install chromium
node tests/dashboard.e2e.mjs
```

The script uses Playwright Chromium. Set `BROWSER_CHANNEL=chrome` to use an installed
Google Chrome instead.
Set `PLAYWRIGHT_MODULE` to an existing Playwright module path if using a bundled runtime.
Set `PYTHON` or `FFMPEG` if their executable names differ.

The exercise opens the real dashboard, saves questionnaire progress via the UI,
selects a saved style direction, approves the fictional brand, renders five original PNGs and a six-second MP4,
creates four content drafts (carousel, image, video, Arabic image), checks order and
desktop/mobile previews, platform caption selection, missing-review approval blocking,
empty filter results, plays the entire video, and saves rated owner-test feedback.
It also checks unauthorized and cross-origin requests. The video is intentionally silent.
Output files, screenshots and RESULT.json remain under `.data/browser-TIMESTAMP/`.

These are technical fictional-brand samples, not quality-certified content or a
side-by-side benchmark against an existing production campaign.

## Host and live-account acceptance
The following checks require your own supported host/account and are NOT replaced by
the local suite:

1. Install the release ZIP/marketplace in your Codex or Claude account and invoke it.
2. Confirm that actual agent behavior starts with the questionnaire and resumes memory.
3. Connect dedicated test social accounts through the provider's OAuth UI.
4. Confirm available formats/settings and safe draft/schedule behavior.
5. Verify remote post IDs, actual published status, cancellation and provider-specific errors.
6. Import real analytics with definitions and permission-specific engagement data.
7. Have a genuine owner evaluate brand accuracy, writing, imagery, language and motion.

Never use a real production brand's credentials to make these checks implicitly.
A passing unit/browser suite does not guarantee host availability, third-party uptime,
social-platform approval, subjective creative quality, or absence of every defect.

## Resource sourcing coverage

Offline tests cover all four adapters, review-before-download, local import, separate
brands, preserved brand approval, material byte/provenance integrity, required caption
credit and export records. Downloader tests cover private/mixed DNS, unsafe URL forms,
redirect rejection, size/incomplete responses and active SVG. Browser tests exercise the
real SVG material preview and search form with a mocked provider response. No CI request
requires a third-party account or internet library to be available.

For a live smoke check, explicitly search a public library in a fictional local workspace,
inspect the original source/licence and actual image, acquire a chosen material, and
verify its byte hash and source record. Keep downloaded third-party assets under ignored
`.data/`; never add them to the plugin or use synthetic review evidence for them.

## Creative outcome experiments

Use the opt-in [paired evaluation harness](../evals/README.md) for synthetic production-only
API experiments. It is separate from the offline unit suite and does not call providers itself.
Exact snapshots, raw responses, failures, normalized exploratory artifacts and independent
rendered review must remain auditable. External calls need their own explicit scope, current
pricing check and bounded budget. Do not use real account credentials or customer assets in CI.
A live model API test is not proof that the native Codex or Claude plugin installation works.
