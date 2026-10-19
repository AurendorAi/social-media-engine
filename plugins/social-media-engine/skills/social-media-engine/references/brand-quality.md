# Carry the rigor, rebuild the identity

Use this when starting a campaign, transferring the workflow to a new brand, or repairing
work described as generic. It supplements—not replaces—the independent review, owner
approval and asset-rights gates in [review](review.md) and [resource sourcing](resource-sourcing.md).
A complete brief and successful renderer cannot guarantee creative quality.

## Establish a real baseline

Read the selected owner's guidelines, actual account, recent approved work and feedback.
When accessible, inspect at least three representative actual examples: record their
source, date, format, visible qualities and what the owner values or dislikes. Open the
actual post/sequence when possible; a profile grid alone does not establish caption,
full carousel, motion, results or intent. Inspect all pages of a reference you describe
as fully reviewed. For video, watch the full audiovisual work.

If examples are inaccessible or the brand is new, record that limitation and use supplied
materials or explicitly provisional original directions. Do not invent a baseline or
block an authorized exploratory proposal because optional references are missing.
Distinguish current identity from a proposed improvement. The owner's constraints win
over this guide, research preferences and sector conventions. Do not default to any
house palette, font, nationality, vocabulary, content ratio or design style by sector.

## Save a brand-specific creative brief before production

Read [runtime](runtime.md), then use `creative-brief-save --file FILE --actor ACTOR`,
`creative-brief-approve --id ID --hash HASH --actor ACTOR`, and `creative-brief` with the
usual selected workspace and brand arguments. The owner approves the exact current
hash; saving is not approval. Keep the record in the selected brand workspace.

The JSON contract is `id`, `brand_hash`, `audience_situation`, `brand_promise`,
`proof_points` (strings), `voice_examples` (`good` and `avoid`, each with `text` and `why`),
`visual_principles`, `content_pillars`, `anti_patterns`, `asset_strategy`,
`success_criteria`, `source_notes`, and optional `sample_asset_ids`. List fields contain
strings except the structured voice examples and asset IDs. Record source qualifiers
and unresolved evidence in `source_notes`; put the intended payoff in `brand_promise`,
its support/mechanism in `proof_points`, and reviewable expectations in `success_criteria`.
Do not invent evidence to satisfy a field.

The record binds the brand profile, rules and immutable reference/output sample assets.
States are MISSING, PROPOSED, APPROVED, CALIBRATED and STALE. CALIBRATED requires explicit
approval with nonempty verified samples; it is not an automatic quality certification.
The runtime does not impose a new production lockout for a missing brief; only a current
approved brief joins resolved context. Never bypass the existing brand, review or
publishing gates. A stale record needs rereading and current approval before it can be
used as approved guidance.

The brief's substance should cover:

- **Audience situation:** a real task, desire, occasion, question or tension; familiarity
  and context; evidence or an explicit hypothesis. A demographic label alone is weak.
- **Purpose and payoff:** what this item lets someone understand, feel, compare, enjoy,
  choose or do. A sensory reveal or a good joke can be the payoff; not every brand needs
  an educational business explainer.
- **Evidence and limits:** sources, authorized materials, verified claims, unresolved
  facts and forbidden inferences. Distinguish observation, owner statement, inference
  and clearly fictional demonstration. Identify changing facts to recheck.
- **Mechanism:** why the central point follows. For a product, this may be a visible
  detail or a useful comparison; for an event, the actual experience and logistics;
  for instruction, the step that changes the result. Mood alone need not explain a
  process, but must still be truthful and relevant.
- **Voice in practice:** a few original sample lines suited to this audience and language,
  plus lines to avoid and the reason. Dialect tokens or adjectives such as “premium”
  do not establish voice. Keep technical clarity, natural rhythm and appropriate humor.
- **Visual meaning:** the actual image, artifact, material or interaction that carries
  the idea; what it shows, what it cannot prove, crop/scale requirements and rights.
  Avoid unrelated decorative objects, invented dashboards and false product imagery.
- **Identity and range:** owner constraints, allowed flexibility, relevant reference
  qualities, one coherent direction and planned variation across formats. State why
  the composition serves this message, not merely which style label it resembles.
- **Production and validation:** available tools/materials, real deliverables, source
  limitations, sample plan, reviewers, owner feedback and unresolved dependencies.

Approval of a creative brief is not approval of media, a post, an asset license or a
publishing action. Show a concrete brief before requesting its approval. Read it again
when continuing work; do not reconstruct it from a previous chat's vague memory.

## Calibrate with actual work

For first content without a selected style, complete the **ten-style comparison** in
[style discovery](style-discovery.md) before the owner chooses. Within an already chosen
style, default to **1–3 finished representative samples**, including a sequence or motion only
when planned. Present actual media and complete captions; collect specific feedback on
idea, payoff, voice, imagery, hierarchy and brand recognition. Revise the affected sample
and compare actual exports. Save owner-approved preferences with their scope.

After the style choice, the user may explicitly request a full proposal/batch instead
of another sample-first cycle. A full-batch request alone does not waive initial discovery.
Honor that scope: use one coherent proposed direction, deliver the authorized batch as
unapproved drafts, state the uncalibrated assumptions, and gather feedback afterward.
Do not create a new approval pause merely because the default suggests a small sample.
Existing brand/content approval requirements still apply to production records and
publishing; a private exploratory proposal is not an approved campaign.

## Prevent the five-brand pilot failure mode

The pilot exposed two transferable problems: reusing a small photo plus headline plus
identical header/footer across unrelated identities, and repeating “send a message” as
the substance of nearly every item. Changing color and type did not repair the first;
changing the wording of the same CTA did not repair the second.

Run a **logo-swap test**: hide the name and ask whether the concept, visual evidence,
voice and composition still identify the selected brand or its particular offer. A
shared layout is appropriate inside a deliberate series, but a universal scaffold that
survives every brand swap needs reconsideration. Compare contact sheets across brands
when producing several together; each should have its own visual logic. Contrast
subject scale, composition, materials and information rhythm—not just palette.

Audit the audience's takeaway before the CTA. A preference poll, product detail,
behind-the-scenes reveal, occasion, story, comparison and practical ordering guide can
all have different jobs. A message request is suitable when the audience needs tailored
help or ordering detail; it must not replace an actual idea. Do not impose a fixed mix
or ban a repeated action when the owner's campaign genuinely needs it.

## Fictional method examples, not customer claims

These are original scenario ideas, not ready captions, documented results or style rules.
Use them only after checking the selected brand's real offer and permissions.

| Fictional context | Evidence or material to obtain | Useful payoff and possible action |
|---|---|---|
| Neighborhood bakery, family gathering | Actual portion photographs and confirmed serving guidance | Compare sharing sizes; choose a suitable format. A sensory close-up can simply invite anticipation. |
| Independent apparel maker | Same real garment shown standing, seated and at a detail scale | Understand silhouette or a verified construction detail; save a look or ask one specific fit question. |
| Plant shop | Customer-permitted room photo and species-specific verified guidance | Identify what information is needed before choosing; no generic care prescription or invented stock. |
| Community concert | Authorized rehearsal excerpt and verified access information | Feel the performance character, then find date, place and accessibility details. No lecture required. |
| Ceramic studio | Real glaze tests photographed under consistent conditions | See why two pieces vary; appreciate the making process without unsupported “handmade” claims. |
| Consumer travel service | Current route facts and genuine destination material | Compare two feasible days by pace or interests; no invented availability or guaranteed experience. |
| Business software team | Consented real task recording or labeled synthetic demonstration | See where a handoff changes the result and what still requires a person; try a defined check. |

## Reject, reread or repair

**Return to the brief and evidence** when the central claim lacks support, the promised
payoff never arrives, the image contradicts the text, an unverified offer appears,
owner constraints are displaced, or unrelated brands share the same interchangeable
concept. Reject the current version rather than polishing a false premise.

**Reread source material and feedback** when revising a disputed fact, using a reference
in a new context, changing audience/language/format, inheriting an old campaign, or
continuing after context loss. Verify source access and freshness; previous inspection
is not permission to claim unseen details. A newly changed brief/context requires the
runtime's current validation and approval checks.

**Repair execution** when the idea works but crops, scale, contrast, rhythm, language or
layout fail. A generic diagnosis must identify the cause and a concrete repair. Do not
respond only with synonyms, different colors or another layer of decoration.

## Audit the delivered format

- **Single image:** one coherent takeaway; real subject at useful scale; truthful text;
  legible required details at phone size; no faux controls implying interaction.
- **Carousel:** inspect every slide in order and alone. Each contributes to the promise;
  evidence and payoff are present; continuity does not mean duplicated layouts; final
  action follows the story. Count pages and alternatives honestly.
- **Story:** inspect safe areas and quick reading, the intended interaction and its actual
  implementation. A drawn poll is a static prompt unless a real platform control is added.
- **Video/reel:** full playback with sound, timing, captions, opening promise and eventual
  payoff; evidence-bearing shots remain readable. Still frames are not completed video.
- **Caption/text:** works with the actual media and can stand on its own where needed;
  no unsupported extension of the visual claim; natural register and real destination.
- **Every format:** confirm rights and source provenance, original composition, script
  shaping/RTL where applicable, dimensions and export integrity. Review at native and
  mobile scales. Independent reviewers must inspect the current asset/content hashes.

Record failures, repairs, real feedback and limits. Quality is an accountable review
process with evidence; it is not guaranteed by a style name, rubric score or plugin.
