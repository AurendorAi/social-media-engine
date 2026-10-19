# Professional plugin implementation study

Date: 2026-10-14. Baseline: Social Media Engine 2.2.0, commit 0c3f76d.

## Method and limits

Inspected eight primary GitHub repositories, their public metadata, selected source implementations,
fixtures, evaluation instructions and recent issue reports. Retrieved 30 source files at pinned
Git tree revisions; inspected relevant sections rather than claiming complete repository audits.
`plugin-source-snapshot.json` records exact source URLs, revisions and retrieval-time adoption counts.
The sample includes skills, plugin bundles and MCP services: these solve different problems and are
not interchangeable products. No third-party code was executed or copied into the plugin.

This is a purposive comparison, not a statistically representative ranking of all plugins.
Stars/forks measure attention and participation, not satisfaction, retention, output quality or
causal improvement. Repository claims about users or quality are not independently verified.
Open issue totals include pull requests and are not defect rates. Closed issues can be redirected,
not resolved: Playwright MCP directs reports to the main Playwright repository.

## Findings from actual implementation

| Project | Snapshot stars | Inspected implementation | Useful lesson for SME |
|---|---:|---|---|
| [Anthropic Skills](https://github.com/anthropics/skills) | 181,107 | `frontend-design/SKILL.md`, `skill-creator/SKILL.md`, comparator agent and evaluator script | Subject-specific design decisions; compare old/new outputs; separate generation and blind assessment; record cost/variance, not just prompt compliance. |
| [Superpowers](https://github.com/obra/superpowers) | 299,066 | writing/subagent skills, testing guide, host manifest, Haiku-specific test | Composable workflows and platform adapters; runtime tests differ from real agent behavior tests; bounded loops must survive long sessions. |
| [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills) | 32,411 | React entrypoint, individual async rule and test extraction script | Atomic advice with rationale and contrasting examples is easier to apply and evaluate than a large list of adjectives. |
| [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 135,780 | skill, search and design-system scripts, reasoning table, relevance thresholds | Local searchable structured knowledge; persist an explicit project design system; confirm retrieval fit; handle empty results honestly. |
| [Playwright MCP](https://github.com/microsoft/playwright-mcp) | 38,140 | README, capabilities tests, fixtures and package | Real tools extend capability; test exposed tool contracts and optional capabilities. CLI can be more context-efficient for coding hosts; MCP serves other interaction patterns. |
| [Context7](https://github.com/upstash/context7) | 63,041 | README, server entrypoint and host manifest tests | Retrieve narrow current context through a common interface; test each host's installation/auth schema. Its server repository does not include the private crawling/parsing backend. |
| [Trail of Bits Skills](https://github.com/trailofbits/skills) | 7,535 | context-building skill and scenario/fixture/grader | Outcome-specific fixtures and explicit failure criteria; distinguish task scope from general capability; repeated runs can expose instability. |
| [K-Dense Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 49,139 | scientific-visualization skill and CI workflow | Domain-specific instructions, reproducible executable helpers, dependency declarations, actual export inspection and dated-source boundaries. |

### How useful instructions are written

1. A precise trigger makes discovery cheap; a short entrypoint routes to relevant references.
2. Instructions identify the user's outcome and concrete invariants, not just a prestigious role.
3. Conditional examples connect a decision to a reason and show when the advice would be wrong.
4. Structured data stores reusable facts/patterns; executable tools handle repeatable transformations.
5. The host's available tools, paths and dependencies are checked, not presumed.
6. Failure behavior is explicit: missing evidence, unsupported capabilities and exhausted iterations
   remain visible. A passing score is not fabricated to finish the workflow.
7. Evaluation measures generated artifacts as well as tool/runtime correctness.

There is no shared magic prompt, universal backend or evidence here that these plugins equalize
all models. Some are largely instructions; others rely on maintained services or substantial code.
The instruction length itself is not evidence of quality.

### What user reports actually establish

Positive examples: [Superpowers #641](https://github.com/obra/superpowers/issues/641) describes usefulness
while requesting another host; [UI UX Pro Max #56](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/issues/56)
reports a favorable Codex experience; [#163](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/issues/163)
praises demos and requests their sources. These are self-selected anecdotes, not satisfaction rates.

Counterexamples inform implementation: [Superpowers #2481](https://github.com/obra/superpowers/issues/2481)
reports a loop limit lost after context compaction; [#2509](https://github.com/obra/superpowers/issues/2509)
reports instruction priority conflicts; [UI UX Pro Max #530](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/issues/530)
reports a host-specific script path breaking other installation modes; [Trail of Bits #376](https://github.com/trailofbits/skills/issues/376)
reports portability issues. These are user reports, not defects independently reproduced in this study.

## Difference from Social Media Engine 2.2.0

| Area | Existing strength | Remaining gap / change direction |
|---|---|---|
| Packaging | Codex/Claude manifests, portable Python stdlib CLI, deterministic ZIP | Native installation must still be tested in each actual host. A model API call is not an installed-host test. |
| Brand state | Onboarding, approved identity, scoped memory, brand separation | Structured context alone does not guarantee the host uses it creatively. Evaluate unfamiliar brands. |
| Production | Asset sourcing, provenance and production references | Creation remains host-dependent. Add concrete conditional composition patterns and inspect resulting pixels. |
| Review | Hash-bound independent roles, owner approval and stale-state guards | Existing numerical review thresholds are judgments, not calibrated proof. Add blind outcome comparisons. |
| Research | Attributed limited Canva observations; no claim of model training | Not a complete reference corpus. Do not rename generated guidance as reviewed professional examples. |
| Tests | Runtime, browser, provider and release regressions | Missing paired multi-model creative outputs, independent visual comparisons and held-out brand transfer. |

## Implemented experiment boundary

New design-pattern guidance is original synthesis, not a licensed artwork collection or trained model.
The experimental benchmark requests model-authored vector posts and captions with the same synthetic
brief, output contract and tool constraints in baseline/candidate conditions. It snapshots the instruction
packets and records errors, hashes, provider/model IDs, cost and latency. An anonymized review packet
allows a distinct reviewer to judge actual renders without seeing condition/model labels.

This is a constrained composition/copy pilot. It does not exercise a full agent tool loop, reference
retrieval behavior, photographic art direction, complete carousels, video, real account integration or
native Codex/Claude installation. Results must not be advertised as proof of universal professional
quality. Subsequent full-host studies need the same real assets, approved profiles and capabilities,
repeated runs, unseen brands, and independent human designer review.

## Iteration and release decision

Freeze the baseline and rubric; make a candidate; run identical paired briefs; inspect actual exports;
record defects against hashes; repair supported problems; repeat affected checks; run the full runtime
suite and release build. Preserve rejected results. Stop a local iteration after a bounded number of
rounds and report the unresolved blocker, rather than endlessly optimizing to one judge or silently
changing the acceptance criteria. User approval remains separate from benchmark acceptance.

See `REFERENCE-DATASET-PLAN.md`, `../audit/INDEPENDENT-QUALITY-EVALUATION.md` and the evaluation
runner documentation for scope and evidence. No satisfaction leaderboard or universal-quality claim
is supported by this study.
