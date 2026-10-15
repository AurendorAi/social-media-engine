# Multi-model design pilot — 2026-10-14

> **Owner correction — 2026-10-15:** The owner rejected the displayed designs as
> unacceptable. Earlier agent descriptions of them as “professionally usable” are
> withdrawn as quality claims. Numerical scores remain historical observations, not
> evidence of acceptance. The SVG-only experiment is retired; new vector creation is
> prohibited. Future evaluation must be calibrated against the owner-provided references.

## What this experiment tests

This is a small, paid OpenRouter experiment using three fictional briefs and a
production-only slice of the baseline and candidate plugin instructions. Models return
one 1080 × 1350 SVG post, caption, alt text and source notes. The briefs cover a quiet
coffee brand, a software handoff checklist, and an Arabic creative-workshop poster.

This does **not** test an installed Codex/Claude agent, onboarding, runtime approval,
tool use, external asset sourcing, photo production, carousels, video or real audiences.
The test constrains all models to the same safe SVG vocabulary and one local Chromium
and system-font environment. No actual customer data or credentials are in the fixtures.

Three Astra agents handled implementation, harness/testing and independent assessment.
The evaluator is a separate agent, not an independent human designer. Its fixed rubric
requires six scores of at least 3/4, a total of at least 20/24, and zero hard failures.
It examines full-size and 390-pixel phone renders, captions and the original brief.
See [the frozen protocol and observations](../audit/INDEPENDENT-QUALITY-EVALUATION.md).

## Round 1: matched baseline versus candidate

18 attempts = 3 models × 3 briefs × 2 conditions; one attempt per cell. Instruction
packets, selected source hashes and request hashes were frozen before generation.
Each matched pair used the same brief, output contract and production-only preamble.
The candidate packet was longer; this comparison does not hold token count constant.

| Model | Requests | Actual provider cost, USD | Mean request latency, seconds |
|---|---:|---:|---:|
| OpenAI `gpt-5.4-mini` | 6 | 0.07627365 | 9.91 |
| Anthropic `claude-sonnet-4.6` | 6 | 0.55563000 | 64.07 |
| Google `gemini-3.1-flash-lite-preview` | 6 | 0.02307015 | 5.56 |
| Total | 18 | 0.65497380 | — |

Nine outputs initially passed strict ingestion. The harness had incorrectly rejected
inert SVG accessibility attributes; uniform reprocessing of all responses raised strict
success to 11/18. The original records remain intact. Removing one exact surrounding
JSON fence recovered three more outputs for visual inspection. Those remain raw-format
failures, producing 14 renderable pieces and four unavailable artifacts overall.

Three missing Anthropic outputs exhausted the 6,000-token completion limit in reasoning;
one Google output used an unsupported SVG attribute. These are delivery/configuration
failures, not evidence about unseen artwork. Seed 41 was sent only where supported;
Anthropic did not support it. Repeated-run stability was not measured.

**Zero of the 18 attempts passed the frozen professional acceptance gate.** All 14
available pieces were reviewed at both sizes with their full copy. Severe Arabic
clipping, hidden supporting text, tiny required details, ambiguous subject illustration,
unsupported claims and invented website addresses prevented acceptance. All nine pairs
received “neither” as the acceptance winner; this does not imply equal aesthetic scores.

| Model / condition | Attempted | Strict after uniform validator fix | Rendered and reviewed, including fence recovery | Accepted | Actual cost, USD |
|---|---:|---:|---:|---:|---:|
| OpenAI / baseline | 3 | 3 | 3 | 0 | 0.03621420 |
| OpenAI / candidate | 3 | 3 | 3 | 0 | 0.04005945 |
| Anthropic / baseline | 3 | 0 | 1 | 0 | 0.27929100 |
| Anthropic / candidate | 3 | 0 | 2 | 0 | 0.27633900 |
| Google / baseline | 3 | 2 | 2 | 0 | 0.01025655 |
| Google / candidate | 3 | 3 | 3 | 0 | 0.01281360 |

The results do not establish a first-pass quality gain from the candidate. More guidance
alone was insufficient, including when baseline instructions already warned against
generic design, unsupported claims and uninspected exports.

## Round 2: provider configuration diagnostic

Six Anthropic calls used the same three paired briefs with reasoning disabled and a
3,500-token completion limit. Actual cost: **USD 0.46560000**. Four provider responses
completed and two truncated; none passed the strict output contract. Two complete
responses became renderable through exact-fence recovery, while two others contained
unsupported SVG attributes. These diagnostic renders have not received the frozen
independent creative assessment and are not counted as professional passes.

Disabling reasoning removed reasoning-token exhaustion in this configuration, but did
not ensure complete, schema-compatible artwork. This is a configuration diagnostic,
not a causal plugin improvement comparison.

## Round 3: six targeted repairs

Six candidate-only attempts received the earlier artifact when available and specific
observed repair feedback. The candidate added Arabic logical-anchor guidance, actual
phone-scale inspection, text/decoration collision checks, recognizable subject drawing
and tighter factual boundaries. The output prompt also disclosed the exact SVG
allowlist. Anthropic reasoning remained disabled; completion allowance was 5,000 tokens.

All six provider responses completed. Five passed strict ingestion; one required exact
JSON-fence recovery. All six were rendered at native and phone sizes. Actual cost:
**USD 0.22663630**. Independent assessment found **0/6 accepted**: repeated clipping,
occlusion and tiny text remained; a newly drawn coffee cone was physically reversed.

This round is assisted targeted repair, **not a new blinded baseline/candidate trial**.
Instruction changes, feedback, prior artifacts and configuration changes are bundled;
their separate causal effects cannot be identified. Contact-address fact locking was
added after this round's prompt freeze and therefore was not tested by these calls.

## Round 4: second targeted repair

Three cases were selected to cover all three sectors and one case per provider: Anthropic
coffee, Google software, OpenAI Arabic workshop. The other failed cases were not retried.
Models received the prior artifact, concrete observed defects and the latest guidance,
including rebuilding broken text regions instead of nudging decoration. Actual cost:
**USD 0.13766900**. All three responses completed; two were strict-valid and one needed
exact-fence recovery. All three were independently inspected at both sizes.

Arabic clipping and the reversed coffee cone were repaired. Remaining weaknesses included
coffee text crossing an internal card border and generic software composition. None
cleared the unchanged aggregate acceptance gate. These repairs establish specific resolved
defects, not a successful general-purpose quality release or a new paired comparison.

## Separate Astra agent-with-tools diagnostic

A GPT Astra producer used the candidate guidance and the same three fictional briefs,
but could actually render, inspect images and measure text bounds. It saw prior failure
feedback; this was a nonblind assisted diagnostic with different capabilities and is not
a causal comparison against the API-only runs. It used original editable vectors, no
external assets or paid generation API, and preserved its first exports and repair log.

The producer viewed native and phone renders and repaired the Arabic font choice.
All 34 measured text regions fit their allocated areas. The separate evaluator then
opened all six final PNGs and read all content. It found no hard failures: correct complete
Arabic, readable essential details, recognizable subjects and no invented claims/URLs.
Fieldnote and Nabta scored 3 on every dimension (18/24); Orbitdesk scored 17/24 because
its concept remained a generic checklist. Two pieces therefore met the rubric's
“professionally usable with minor refinements” anchor on every dimension, while **0/3
met its stricter >=20/24 aggregate acceptance threshold**. Do not collapse that distinction.

A further art-direction pass rebuilt all three concepts and preserved the first diagnostic.
The producer inspected all six new native/phone PNGs and checked 38 text regions. The
independent evaluator inspected all six final PNGs, full copy and hashes again:

| Fictional brand | Final score /24 | Hard failures | Every dimension >=3 | Frozen >=20 gate |
|---|---:|---:|---|---|
| Fieldnote Coffee | 18 | 0 | Yes | Not met |
| Nabta creative workshop | 18 | 0 | Yes | Not met |
| Orbitdesk software | 19 | 0 | Yes | Not met |

The coffee composition now illustrates a controlled grind comparison with shared
constants; pottery imagery has coherent handmade character; the software post uses an
explicitly fictional decision/owner/file handoff example instead of a generic checklist.
The evaluator judged all three professionally usable with minor refinements, without
awarding unsupported excellence scores. No final item met the stricter aggregate gate.
An uncertain Jev payoff-rating check was resolved by the evaluator's own stated judgment,
as the decision policy permits. Neither self-review nor a score was entered as runtime
approval, and there was no real owner or human-designer acceptance.

## Costs and evidence

The four API rounds made 33 provider calls with known actual generation charges
totalling **USD 1.48487910**. Pricing preflights are estimates, not charges. No automatic
retries were made after unknown billing; no unknown-billing event occurred. Small Jev
decision-check charges are recorded separately in the research/evaluator evidence.
Astra desktop-agent usage is separate and is not represented as free inference or
included in this API dollar figure.
The seven recorded Jev checks total USD 0.00063714; together with generation, known
OpenRouter charges for this investigation total USD 1.48551624.

Raw requests, provider responses, usage, errors, frozen instructions, normalized copies,
anonymous review packets, PNG hashes and private condition mappings are retained locally
under the ignored `.data/model-evaluations/2026-10-14/` evidence archive. Generated
fixtures and provider exports are not part of the distributable plugin or committed
source. The harness is offline and never loads API credentials or makes paid calls.

## What can be concluded

The plugin now has a concrete way to specify composition, retrieve eight original
conditional patterns, inspect an export, repair observed defects and preserve failure
evidence. The experiment demonstrates why technical validation and creative acceptance
must be separate. It does not demonstrate identical quality across models, universal
professional output, or success in the full installed production workflow.

Before promoting this as a proven quality release, run repeated full-host trials with
matched tools and actual approved brand assets, unseen brand/creator holdouts and human
designer review. Preserve the failed first-pass results and evaluate complete final
artifacts; do not replace these results with the best selected examples.

## Technical verification and distribution status

The final source passes **97 offline unit tests** (47.814 seconds in the recorded run),
`git diff --check`, and the deterministic release builder. The package contains 35 files,
122,121 bytes, SHA-256
`0fed3912aed8f68fda93b83de3a97e8177d14ab7e1f72a2be47fc420fcbac6ff`.
Skill-format validation also passed. No live posts were published.

This is a development candidate. Manifest versions remain 2.2.0; the locally rebuilt
archive is not the already-published 2.2.0 release and must not replace its release asset.
No new public release/tag or native-host installation success is claimed. The research,
code changes, failed trials and usable final examples are reviewable; universal quality
and the stricter creative acceptance target remain unproven.
