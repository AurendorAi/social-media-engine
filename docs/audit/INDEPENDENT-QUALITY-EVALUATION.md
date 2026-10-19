# Independent agent quality evaluation

> **Owner correction — 2026-10-15:** The owner rejected the displayed designs as
> unacceptable. Earlier agent descriptions of them as “professionally usable” are
> withdrawn as quality claims. Numerical scores remain historical observations, not
> evidence of acceptance. The SVG-only experiment is retired; new vector creation is
> prohibited. Future evaluation must be calibrated against the owner-provided references.

Local evidence is durably archived under the ignored
`.data/model-evaluations/2026-10-14/` directory. Historical `/tmp/<name>/...` references
below map to `<archive>/<name>/...`; original evidence bytes and hashes are preserved.
The archive includes a browsable `index.html` and a SHA-256 inventory. These local
artifacts are not redistributed with the plugin source or release package.

## Pre-registered protocol — 2026-10-14

This protocol was recorded before the evaluator received or inspected candidate rendered
outputs. The evaluator is a separate agent, not an independent human designer. Model and
condition mappings must remain hidden until first-pass judgments are recorded. Brand
briefs, authorized facts, requested formats, constraints, and source/rights manifests
must remain visible because judging without them would reward unsupported invention.

The starting v2.2.0 skill already instructs agents to inspect actual pixels, avoid generic
brand swapping, preserve Arabic shaping, verify claims, and deliver complete exports.
Its unit/browser suites verify runtime behavior with fictional technical fixtures. They
do not establish that a host following those instructions produces professional work.
No schema, build, release, or browser pass is counted as creative quality evidence.

### Required evaluation packet

Each anonymized packet must contain the complete brief, authorized facts and constraints,
ordered final exports, full platform/language-specific captions, alt text, editable
sources or an explicit justified limitation, source/rights record, and asset hashes.
Exclude model names, condition labels, previous scores, creator self-evaluations, and
unnecessary private customer information. Identify unavailable evidence explicitly.

Inspect every exported image/slide at native scale and at a representative phone display
width (390 CSS pixels, without zoom); inspect a cross-brand contact sheet separately.
For motion, complete audiovisual playback is mandatory. A still does not establish
motion quality. Check page ordering, crop, safe areas, brand marks and required details.
For Arabic, examine joining, bidi, punctuation, numerals, glyph coverage and line breaks
in the actual render as well as natural register in the caption. Do not claim native
language expertise or human review. Record uncertainty instead of assuming correctness.

### Hard failures

Any one blocks acceptance of the affected deliverable; an average cannot conceal it:

- Missing requested final asset, caption, language variant, or required handoff component.
- Unsupported material claim, fabricated evidence/provenance, invented availability or
  performance, or imagery that misrepresents the offered product/service.
- Violation of an explicit brand constraint, incorrect logo/product proportions, or
  contamination from another brand's identity or private context.
- Unreadable required text at phone size; clipping, missing glyphs, broken Arabic joining
  or bidi that compromises meaning; unsafe placement of essential information.
- Corrupt export, wrong required dimensions/order, or storyboard substituted for video.
- Unaccounted-for rights/source status for third-party material; false clearance claims.

Missing visual evidence is NOT TESTED, never a pass. Uncertain language/provenance blocks
an unqualified acceptance claim until resolved, even if no defect has been proved.

### Scoring anchors and thresholds

Each dimension is scored 0–4 using concrete observations tied to the brief:
0 = unusable/absent; 1 = substantial failure; 2 = material repair needed;
3 = professionally usable with only minor refinements; 4 = unusually strong execution
with specific evidence of excellence. Aesthetic preference alone does not earn a 4.

| Dimension | Evidence required for 3 or better |
| --- | --- |
| Brand fidelity | Respects explicit identity, offer, audience, voice and examples; recognizable through substantive choices beyond name/color. |
| Audience payoff | A clear, useful or emotionally appropriate takeaway arrives before the CTA; it is supported by the actual content. |
| Distinctive concept | Message and visual mechanism are specific to the brief; cross-brand swapping exposes a meaningful mismatch. Shared series structure is acceptable when intentional. |
| Copy quality | Clear, natural, precise language; platform-appropriate structure; no filler, forced dialect, repetitive CTA-only substance or unsupported extensions of the visual. |
| Visual craft | Deliberate hierarchy, readable typography, coherent spacing/crops/materials, meaningful subject scale and controlled detail at native and phone size. |
| Format utility | The complete requested format works: each slide advances its sequence, caption supports the media, and handoff/alt text/order/dimensions are usable. |

Accept an individual deliverable only with zero hard failures, all six dimensions >=3,
and total >=20/24. Accept a packet only when every required deliverable passes. This benchmark rubric does
not replace or lower the runtime’s separate 145/160 role-review threshold or owner and
publishing gates; no benchmark result is entered as a production approval. Report
per-brand results and worst-case defects; do not report only a mean. Compare conditions
on matched briefs and distinguish first-pass quality from repaired final quality.

A candidate improvement requires more than a better numerical average: show concrete
resolved defects or better brief-relative outcomes, without new hard failures. If both
conditions pass, report preference and its basis separately from acceptance. A small
fictional benchmark does not establish performance on all brands, hosts or models.

### Revision and evidence discipline

Freeze first-pass observations and scores before unblinding. Record asset path/hash,
viewed scale, exact visible defect, severity, and targeted repair. Re-evaluate changed
exports and any dependent captions after revision. Preserve first-pass results; never
replace them with final scores. Limit iteration to focused defects and report remaining
shortcomings honestly. Owner approval and real human reception remain separate gates.

Jev checked the nonsecret protocol for adequacy before output review: `usable`, confidence
0.96 (probability 0.98), elapsed 727.83 ms, actual cost USD 0.000027678; conservative
preflight USD 0.005376000. Payload and response are local evaluator artifacts under
`/tmp/sme-plugin-evaluator/`. This is a protocol check, not a visual judgment or quality
certification. Jev sees only observed nonsecret evidence for subsequent bounded decisions.

## Output evaluation status

First-round blinded review completed as recorded below. Cross-host installation and
live publishing are outside this creative review.

## Separate candidate implementation inspection

Inspected `design_patterns.py`, `design-patterns.md`, `producer-revision-loop.md`,
`design-patterns.json`, and the corresponding SKILL.md diff before output review.
This inspection was separate from, and provides no score for, creative output quality.

The helper uses Python standard-library modules, resolves its bundled data from
`__file__`, and neither reads a brand workspace nor makes network calls. Direct checks
confirmed eight entries, exact-filter intersection, an empty valid combination,
rejection of unknown filters, and the documented installed relative path. The guidance
labels patterns original hypotheses and retains identity, evidence, rights and existing
approval boundaries. Producer inspection explicitly cannot satisfy independent review.

The main unresolved question is effectiveness: the baseline already contains strong
quality instructions, and additional guidance could add reading load without changing
outcomes. Only actual matched outputs can establish improvement in this pilot. This
inspection did not verify all upstream source claims, full release packaging, installation
in either end-user host, or live provider behavior; those require their own evidence.


## Blinded first-pass output findings — 2026-10-14

Packet: `/tmp/sme-review-final-v1/review-packet.json`. Exact per-asset observations,
repairs, scores, inspected PNG paths and SHA-256 hashes are in
`/tmp/sme-review-final-v1/independent-review.json`. Model/condition mapping was not read.
All 14 available native PNGs and all 14 corresponding 390-pixel phone PNGs were actually
opened with the image viewer. All 14 complete captions, alt texts and source notes were
read against the supplied fictional briefs. Four attempts supplied no valid artifact.
No unseen asset was credited with a pass. Cross-brand comparison used the individual
phone views; a separate combined contact sheet was not supplied or inspected.

**Zero of 18 attempts met the frozen acceptance threshold.** All nine pairs therefore
receive `neither` as the acceptance winner. This does not mean every pair is aesthetically
equal; it means neither delivered an acceptable complete piece under the fixed gate.
Three rendered outputs required removal of one exact JSON fence and remain strict-format
failures; their visible quality was still evaluated. Strict API-format success is reported
separately by the harness and must not be conflated with these visual/copy judgments.

Scores below follow brand / payoff / concept / copy / craft / format, each out of four.
They are anchored agent judgments, not measured audience responses.

| Anonymous output | Six scores | Total /24 | Concrete finding |
| --- | --- | --- | --- |
| pair-001-A | 0 / 0 / 0 / 0 / 0 / 0 | 0 | No valid requested final artifact delivered. |
| pair-001-B | 2 / 3 / 2 / 2 / 2 / 3 | 14 | Readable cream/green serif teaching post; required brewing facts and save action present |
| pair-002-A | 3 / 3 / 2 / 2 / 3 / 3 | 16 | Caption promises checklist will ensure nothing gets lost; evidence supports only three checklist actions. |
| pair-002-B | 3 / 3 / 2 / 2 / 3 / 3 | 16 | Caption calls context loss the most common friction point without supplied comparative evidence. |
| pair-003-A | 1 / 1 / 1 / 2 / 0 / 0 | 5 | Nearly all Arabic headline, date/time, tools and booking text extends beyond right canvas edge. |
| pair-003-B | 2 / 3 / 2 / 3 / 2 / 2 | 14 | Required day/time is cream on yellow with poor contrast, compromising phone reading. |
| pair-004-A | 2 / 2 / 3 / 2 / 1 / 1 | 11 | Core comparison details and required save CTA too small at phone size; CTA final word loses contrast beyond pill. |
| pair-004-B | 0 / 0 / 0 / 0 / 0 / 0 | 0 | No valid requested final artifact delivered. |
| pair-005-A | 3 / 3 / 2 / 3 / 1 / 1 | 13 | Second card support text is obscured by icon; save CTA is extremely small at phone size. |
| pair-005-B | 3 / 3 / 2 / 3 / 2 / 2 | 15 | Three step headlines and save action readable; supporting text spills beyond card right edges (all three cards, third nearly reaches canvas edge) |
| pair-006-A | 3 / 3 / 2 / 3 / 2 / 3 | 16 | Warm serif hierarchy and concise caption fit brand; all required facts and save action present |
| pair-006-B | 2 / 3 / 2 / 3 / 2 / 3 | 15 | Main steps and caption are clear and truthful |
| pair-007-A | 1 / 1 / 2 / 2 / 0 / 0 | 6 | Arabic heading, subline and required time are clipped beyond right edge; booking text overruns pill. |
| pair-007-B | 1 / 1 / 2 / 3 / 0 / 0 | 7 | Arabic heading and required time/tools are clipped beyond right edge; Latin DM reads MD in bidi setting. |
| pair-008-A | 2 / 3 / 2 / 2 / 1 / 1 | 11 | Artwork invents orbitdesk.io destination. |
| pair-008-B | 2 / 3 / 2 / 1 / 2 / 2 | 12 | Caption invents Thirty seconds versus a week of catch-up productivity comparison. |
| pair-009-A | 0 / 0 / 0 / 0 / 0 / 0 | 0 | No valid requested final artifact delivered. |
| pair-009-B | 0 / 0 / 0 / 0 / 0 / 0 | 0 | No valid requested final artifact delivered. |


The strongest recurring defects are execution and honesty, not palette choice. Three
Arabic posters place most required text beyond the right canvas edge; one also reverses
Latin DM to MD. The fourth Arabic poster keeps complete text but makes the required time
cream on yellow. Visible joining alone does not establish usable Arabic composition.
English pieces include text hidden by icons, text spilling from cards, tiny phone-scale
CTAs/support, and coffee illustrations that do not clearly depict the specified dripper.

Several captions/artworks go beyond the supplied facts: “most common” friction,
“ensure nothing gets lost,” “Zero lost context,” “Every time,” and “Thirty seconds” versus
“a week of catch-up.” Both pair-008 artworks invent a website destination. Some source
notes and alt texts claim clear/validated layouts despite the visible defects. Those
claims must be checked against the final actual export, not copied from the intention.

The briefs produce visibly different broad families (cream coffee editorials, dark
software checklists, Arabic cultural posters); there is no basis to allege an identical
single scaffold across all three. Within those families, however, common stacked-text
layouts and decorative shapes rarely develop a distinctive, information-bearing concept.
No numeric score substitutes for the specific repair notes in the evidence file.

Jev classified acceptance from the evaluator's nonsecret textual observations and scores:
reject for all 14 rendered pieces, confidence 0.98–1.00, elapsed 784.412 ms, actual cost
USD 0.000216594 (preflight USD 0.005376000). It did not inspect pixels and is not a second
visual reviewer. Its certainty reflects the supplied evidence/threshold, not a statistical
probability that all audiences would reject the work.

This is a small first-pass single-image SVG pilot in one Chromium/system-font environment.
It skips actual onboarding/runtime execution and does not test carousels, motion, full
installed workflows, real owners or live publishing. It establishes concrete failures in
these outputs, not general superiority/inferiority of any model or condition. Preserve
these first-pass findings if repairs are made; evaluate new hashes separately.


## Six targeted repairs — separate candidate-only exercise

Reviewed `/tmp/sme-review-v3-repairs/review-packet.json` without reading private mappings.
This is NOT a new paired A/B or held-out benchmark. All six native PNGs and six 390-pixel
phone PNGs were opened; complete captions, alt text and source notes were checked against
the same briefs. Per-asset hashes and evidence are in that folder’s
`independent-review.json`. Frozen thresholds are unchanged: **0/6 accepted**.

| Repair | Six scores | /24 | Resolved | Remaining/new defect |
| --- | --- | --- | --- | --- |
| repair-001 | 2 / 2 / 3 / 2 / 1 / 1 | 11 | CTA now fits its background. | Comparison labels remain roughly 7–8px at phone scale; next-brew card locks all variables while saying adjust next variable. New dripper cone points upward like a roof, not an open funnel. Source note says labels increased to 21px but inspected original comparison had 22px; declaration is not evidence of improvement. |
| repair-002 | 2 / 3 / 1 / 2 / 2 / 2 | 12 | Gross right-canvas clipping corrected; workshop and time now visible and joined. | Card text starts at x near outer right edge instead of padded inner margin; rightmost letters of time/tools/booking collide with edge. Circle, triangle and arch lack clay-vessel specificity. Formal/colloquial caption mixture remains. Source claim all information legible is overstated. |
| repair-003 | 3 / 3 / 2 / 3 / 1 / 1 | 13 | Icons shifted right and first arrow less tangled. | Second line ends under icon despite alt/source saying separate column and no coverage. Cards narrowed, support not reflowed. Phone support/CTA still tiny; decorative icon function is unclear. Caption remains accurate. |
| repair-004 | 3 / 3 / 2 / 2 / 3 / 3 | 16 | Readable support and clear three-step order; no clipping; unsupported most-common claim removed. | Still a generic numbered list with no particular handoff mechanism; stiff Identify singular accountability language. Caption still says ensure transitions remain clear and actionable despite note saying all effectiveness claims removed. Overall usable technical layout, below distinct-concept/copy threshold. |
| repair-005 | 1 / 1 / 1 / 3 / 0 / 0 | 6 | Centered booking remains visible; caption avoids previous slash constructions. | Huge decorative vase monopolizes upper two-thirds; necessary information is clipped. direction rtl with text-anchor end at right edge repeats known faulty placement. Brand name centered but event name absent in full. JSON fence normalization remains strict-format failure. |
| repair-006 | 1 / 1 / 2 / 3 / 0 / 0 | 7 | Latin DM now reads DM rather than MD. | Core RTL anchor error unresolved; some white lettering is off dark card onto near-white canvas. Full caption accurate, but alt text falsely says clear readable hierarchy and safe margins. |

The repairs show real but partial progress: wider CTA, one corrected RTL placement,
readable checklist support, and corrected DM direction. They also show why declarations
are not QA: the icon still covers text after notes say it does not, two Arabic exports
retain catastrophic clipping, and a rebuilt dripper points upward like a roof. The clean
checklist remains below the concept/copy bar, rather than failing merely on cosmetics.

Feedback was sent while reviewing so any further authorized pass can target visible
causes: reflow/remove icons, use measured padded text regions, simplify comparisons,
correct object geometry, and remove assurance claims. Preserve first-pass and repair
results separately. Do not count repeated exposure as fresh generalization evidence.

Jev applied the gate to the nonsecret observation record: reject all six, confidence 1.0,
elapsed 722.418 ms, actual cost USD 0.000087402 (preflight USD 0.005376000). It saw text
observations and anchored scores, not pixels, and does not add independent visual proof.


## Second selected repair pass — separate candidate-only exercise

All three native and phone PNGs (six views) and full caption/alt/source content in
`/tmp/sme-review-v4-repairs/` were inspected, without private mapping access. Exact hashes
and observations are in its `independent-review.json`. This selected repair set is not a
fresh paired comparison; other failures were not retried. **0/3 accepted**, unchanged gate.
No new hard failure was identified in this set; below-threshold craft/concept/copy still
prevent acceptance. One exact JSON-fence recovery remains a separate strict-format failure.

| Output | Six scores | /24 | Visible improvement | Remaining issue |
| --- | --- | --- | --- | --- |
| second-repair-001 | 3 / 3 / 3 / 3 / 2 / 2 | 16 | Dripper cone now wide at top and narrows down toward cup. Core table and CTA type enlarged; contradictory adjust-next-variable instruction removed. | Right-card taste instruction crosses bottom border and crowding remains; low-contrast small headers and same labels weaken comparison. This-brew/next-brew still less direct than change/hold/taste. Caption hear what dial is telling you is strained metaphor. No new material false claim. |
| second-repair-002 | 2 / 3 / 2 / 2 / 2 / 3 | 14 | All three steps and save CTA readable; icon occlusion and overflow absent. | Three disconnected white modules plus left dashed line merely restate steps; there is no particular example or visible transfer of context. No headline or brand name on artwork; vast empty gaps. Caption retains bureaucratic singular accountability/source of truth wording. |
| second-repair-003 | 3 / 3 / 2 / 3 / 2 / 3 | 16 | All Arabic headline, time, tools and booking lines fit; joining/order visibly coherent; high contrast; no DM reversal. Caption truthful and concise. | Abstract floating rings/crescents resemble disassembled eyes/objects rather than convincing pottery; no strong specific workshop concept. Small peripheral copy and decorative low-contrast circles add little. Alt text contains unexplained English editable inside Arabic and overstates artistic specificity. |

Arabic placement is now complete and readable; coffee geometry and text scale improved.
The coffee right-card note crosses its border, software reduces to three generic boxes
without a title, and the Arabic illustration remains visually incoherent as pottery.
These are narrower defects than catastrophic clipping, but repairing blockers alone
does not automatically establish the fixed professional-quality threshold.

Jev text-only gate check: reject all three, confidence 1.0, elapsed 700.620 ms, actual
cost USD 0.000048636 (preflight USD 0.005376000). It did not inspect the pixels.


## Tool-assisted production diagnostic — separate, nonblind

A separate Astra production agent created three vector outputs and used actual render
inspection. This evaluator independently opened all three final native and three phone
PNGs, read complete captions/alt/source notes, and verified PNG hashes against the packet
at `/tmp/sme-astra-agent-diagnostic/`. Producer inspection was not counted as independent
acceptance. Results are in that folder’s `independent-review.json`.

This exercise is nonblind: producer identity and prior failure patterns are known. It is
not a cross-model comparison, paired test, or causal estimate of the upgrade’s effect.
The frozen bar remains unchanged: **0/3 reach 20/24, but two now meet every individual
professional-usability anchor. No hard failures were observed in these three.** Rejection
at the aggregate threshold must not be paraphrased as “all outputs are unusable.”

| Output | Six scores | /24 | Evidence | Remaining limitation |
| --- | --- | --- | --- | --- |
| fieldnote | 3 / 3 / 3 / 3 / 3 / 3 | 18 | All essential text reads at phone scale; recognizable small dripper over mug; restrained serif/sans and supplied palette. CHANGE grind is visually separated from KEEP THE SAME dose/water, then taste/compare instruction and save action. Caption concise and truthful; alt text matches; no invented claims or external assets. | Professionally usable at each dimension anchor. Composition is clear and competent, with limited tactile character or unusually distinctive craft to justify exceptional (4) scores. No material defect identified. |
| nabta | 3 / 3 / 3 / 3 / 3 / 3 | 18 | Complete Arabic headline, audience, tools, time and booking readable native/phone with visibly joined coherent glyphs/order. Tahoma looks clear and modern. Original bowl/vase silhouettes are recognizable and playful, identity correct. Caption natural and factual; no added location/price/availability. | Professionally usable at each dimension anchor. Simple outlined vessels and conventional stacked announcement have no unusually strong conceptual/craft feature to justify 4. Minor bowl/vase stylistic mismatch (outlined bowl versus solid vase) is optional refinement, not blocker. Native human Arabic proof remains separate. |
| orbitdesk | 3 / 3 / 2 / 3 / 3 / 3 | 17 | Clear headline, brand mark, readable numbered flow and brief-specific plain-language questions. All facts and save CTA present, no overclaims. Icons/boxes no longer obstruct support; useful hierarchy survives phone. Caption precise and complete. | Concept remains conventional three-step list with arrows; questions paraphrase instructions rather than reveal a particular handoff artifact/mechanism. This is the sole below-3 dimension; execution and copy otherwise professionally usable. |

Fieldnote and Nabta are competent usable examples at the rubric’s 3/4 anchors. They do
not show the unusually strong execution needed to justify enough 4s for the pre-registered
20/24 threshold. Orbitdesk is readable and truthful but its conventional list/arrow
concept remains a 2. Do not manufacture hard failures or inflate scores to force a pass.
Optional refinement notes are not equivalent to required blocker repairs.

These outputs support a narrow practical finding: actual rendering and inspection can
produce substantially more usable examples than the observed broken drafts. They do not
isolate whether the improvement came from model, tools, extra time, instructions, feedback
or familiarity with these briefs. No claim of universal professional quality follows.

Jev selected `usable_but_below_gate` for reporting the textual evidence, confidence 1.0,
elapsed 711.582 ms, actual cost USD 0.000046074 (preflight USD 0.005376000). As throughout,
Jev did not inspect images and was not an additional independent visual reviewer.


## Final focused art-direction revision — nonblind, feedback-assisted

Independently opened all six final native/phone PNGs and read all captions, alt text and
source notes in `/tmp/sme-astra-agent-diagnostic-v2/`; verified PNG hashes against its
packet. Evidence is in that folder’s `independent-review.json`. Earlier packets/reports
remain unchanged. The fixed bar was not relaxed. **Scores: Fieldnote 18/24, Nabta 18/24,
Orbitdesk 19/24; 0/3 reach 20, all three meet every professional-usability dimension.**
No concrete hard defect was observed; no further production is requested by this review.

| Output | Six scores | Outcome evidence |
| --- | --- | --- |
| Fieldnote | 3 / 3 / 3 / 3 / 3 / 3 | A controlled comparison is now visible: different symbolic grind sizes, shared dose/water band, taste question and save CTA. This is more message-specific than a text checklist, with complete readable type and an accurate caption. The familiar comparison structure is competent rather than unusually exceptional; coarse score remains 18. |
| Nabta | 3 / 3 / 3 / 3 / 3 / 3 | Natural first-encounter invitation, cohesive handmade bowl and curved logistics panel improve character. Complete readable Arabic time/tools/booking and truthful caption remain. The illustration is usable and specific, while still a conventional one-object announcement; score 18. |
| Orbitdesk | 3 / 4 / 3 / 3 / 3 / 3 | Concrete decision, owner and file example makes the desired handoff immediately actionable. Fictional status is explicit on artwork and caption; Mina and the filename are appropriate illustrative content, not fabricated customer evidence or live destinations. The familiar note motif remains a 3 concept/craft; payoff earns 4, total 19. |

No unsupported claim is created merely by adding an explicitly fictional instructional
example. The check is whether the example is clearly labeled, consistent with the brief,
and does not pretend to be a real product, customer, result or functioning link. These
examples satisfy that boundary. Coffee dots are symbolic, not a grind specification or
a claim that coarser is better. The pottery drawing promises no particular workshop result.

Jev considered all 18 dimension ratings from nonsecret observed evidence, not pixels.
It selected 3 for 17 dimensions; Orbitdesk payoff 4 was uncertain (confidence 0.36,
P(4)=0.52/P(3)=0.48). The evaluator therefore made that call independently: 4, because the
populated example teaches exactly what context to leave while preserving explicit fiction.
Other Jev confidence values were 0.55–1.0. Elapsed 966.318 ms; actual cost USD 0.000176442;
preflight USD 0.005376000. This remains one agent’s visual judgment, not human certification.

The endpoint is useful work below a deliberately high aggregate threshold, not a forced
pass and not a claim that all drafts are unusable. Repeated feedback, actual tools, host,
model and production time are confounded; this exercise cannot attribute improvement
causally to the plugin upgrade or establish generalization to unseen brands.
