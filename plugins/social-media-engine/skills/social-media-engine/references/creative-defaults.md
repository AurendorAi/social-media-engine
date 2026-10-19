# Creative direction is the default

Apply this to ordinary requests to create content, including requests that say only
“make a post.” The user supplies the goal and brand context; they do not need to ask
for creativity, professional design, better ideas or another attempt before you use
this process. It applies to approved production and authorized exploratory proposals;
it does not change onboarding, rights, service permissions or publishing approval.

## Develop the idea before the layout

For a new campaign or standalone concept, develop a few genuinely different directions
(usually three) in compact working notes. Do this within the existing brief; do not ask
the user to invent the creative idea or approve every internal option. These are idea
notes, not three paid renders. For each, write:

- The particular audience moment, desire or tension and the useful or emotional payoff.
- An actual headline in the requested language and a concrete scene, demonstration or
  narrative. Describe what the viewer sees, not just a style name or “premium visual.”
- What the image communicates and what the words add; why their combination is stronger
  than either alone. Identify the brand-specific fact or character that makes it fit.
- The necessary materials, known evidence, production feasibility and main weakness.

Compare by relevance, clarity, meaningful surprise, brand fit and feasible execution.
Reject unsupported promises and arbitrary spectacle. Select a direction and record the
reason plus why the strongest alternative was weaker. Do not invent numerical scores or
audience-performance predictions. Different colors or fonts on the same idea are not
different directions. Choose an honest, direct treatment when it serves the audience
better than a metaphor; novelty is not a requirement for a factual announcement.

For an approved recurring series, adapt its established direction to the new substance.
For a typo, crop, translation or other narrow revision, repair the requested part and
preserve the approved idea. Do not restart concept development or force extra options.
Respect a user's explicit budget, scope and direct instructions.

## Make the visual carry meaning

Name the visual mechanism in one sentence: what relationship, change, detail, contrast
or feeling will the audience actually perceive? An adjective such as “bold” is not a
mechanism. Give the central subject enough scale to do that job. Secondary materials
must contribute to the story, evidence, atmosphere or reading order; remove them when
they merely fill space. Negative space is intentional room for attention, not a defect
that needs decorative circles, random textures or more text.

Choose and inspect materials using [resource sourcing](resource-sourcing.md). Use the
owner's actual products and evidence where fidelity matters. Licensed photography,
archive imagery, textures, existing graphics and permitted raster generation/editing
can work together; no fixed sourcing/generation ratio is required. A generation prompt
should specify the subject's action or relationship, material qualities, lighting,
viewpoint and room needed for copy. “Make it professional” is not art direction.
Inspect the resulting image before finalizing text placement. Generative metaphors are
expressive imagery, never proof of a real product, location, feature or result.

The [no-new-vector boundary](../SKILL.md#production-boundary-no-newly-created-vector-graphics)
applies throughout. Never fall back to code-drawn objects when a source or image tool is
missing. Follow [image acquisition](image-acquisition.md): source suitable licensed
media, use connected design services or available image APIs, or produce quality-checked
raster/3D renders. State a limitation only after checking feasible available routes.
Prefer separately typeset, editable text where it improves accuracy and control. Proof
the actual script and export; generated lettering is not assumed correct.

## Compose the words and image together

Use the [composition contract](design-patterns.md#make-a-small-composition-contract)
with actual copy and materials. The headline can complete a visual thought, reframe a
familiar subject or state a useful contrast. It need not describe everything visible.
The supporting line resolves ambiguity; the caption adds substance or context instead
of repeating the poster. A CTA follows the audience's payoff and need not dominate it.
Use the brand's language and register, not a literal translation of a clever English line.

Set a deliberate reading order, subject scale, crop, type roles and quiet space. Fit
the composition to the asset's real geometry and the viewing ratio. Preserve required
logistics and accessibility. A large headline cannot compensate for unreadable details.
For a carousel or video, give each step a new contribution and a payoff; a striking
cover followed by filler is an unfinished concept.

## Transfer principles, not the demonstration designs

The owner positively received the creativity of a six-design local Arabic demonstration.
That is preference evidence for this workflow, not proof of universal quality, model
training, a completed reference dataset or measured marketing performance. Its private
artwork, brands, fonts and production assets are not included in the plugin. The following
are abstracted working examples, to be adapted or rejected against the selected brief:

| Principle | What makes it meaningful | When to avoid it |
| --- | --- | --- |
| Turn an intangible benefit into a tangible relationship | A constructed scene can make an invitation to imagine or explore visible, while a short headline completes the thought. Material detail gives the scene a believable world. | When the benefit requires literal evidence or the scene could be mistaken for the real product. Do not give every brand a miniature world. |
| Show a sensory effect through light, surface or trace | A restrained scene can suggest presence without unsupported claims; light and material become the subject, not decorative filters. | When essential product identity disappears, required information becomes illegible, or mood implies a specific unverified property. |
| Make friction and release visible | A material changing from tangled to ordered can express a defined recurring-work problem. The caption explains the real scope and remaining human judgment. | When a real mechanism must be demonstrated, or the metaphor promises capabilities or measured savings without evidence. |
| Let the viewpoint embody the message | An immersive photograph and copy placed around its movement can let the viewer experience the proposed pace or attitude. | When stock imagery would imply a real destination, inventory or available experience that has not been verified. |
| Make one practical decision easy | A truthful photograph plus precise typographic contrast can isolate the one variable the audience should change and what stays constant. | When the factual guidance is unsupported, more variables matter, or an evocative campaign is being forced into an instruction card. |
| Show the act, not a generic symbol | A close view of real hands, tools or material can communicate participation and texture; event facts stay clearly separate. | When rights, consent, craft claims or event facts are unknown. Do not replace the real process with a decorative imitation. |

These are examples of image/copy reasoning, not six templates or sector-to-style rules.
Retain a brand's approved visual language. Across unrelated brands or a large batch,
compare contact sheets for accidental reuse of the same scaffold, imagery, headline
rhythm and CTA. Within a deliberate series, preserve useful anchors and vary the part
that conveys new information. Do not create complexity solely to look different.

## Judge the result, not the plan

Use the [producer revision loop](producer-revision-loop.md) on the actual native and
phone-sized exports. In addition to technical checks, record visible answers:

- What catches attention, and does it lead to this post's particular payoff?
- Does the central image carry the intended meaning, or could any stock image replace it?
- Do the headline and visual work together, and does the caption add something useful?
- Which material, crop, typographic choice or detail makes this feel deliberate? Which
  detail is arbitrary or competes with the subject?
- Does the work still fit this brand with the logo hidden? Are the important details
  readable without zooming? Is the actual carousel/video rewarding beyond its opening?

A technically valid export with an interchangeable concept is a substantive-revision
case. Fix the concept, evidence or image/copy relationship; a new palette is not a repair.
A simple factual post can pass because of precision and relevance, without spectacle.
Use the existing bounded repair loop, then independent review and owner feedback. Do not
lower the bar silently when a model or tool struggles, or self-certify unseen pixels.

Save concise decision notes in the selected workspace, linked from the composition
contract. For normal item records, the existing free-form `creative` object can retain
`concept_options`, `selection_reason`, `visual_mechanism` and actual `qa` observations,
alongside the existing production/source/export fields. These are working notes, not new
runtime-required fields, approval states or automated quality checks. Preserve required
`material_uses` records when resources are used. Onboarding previews stay proposals;
do not bypass readiness to save them as approved production items.
