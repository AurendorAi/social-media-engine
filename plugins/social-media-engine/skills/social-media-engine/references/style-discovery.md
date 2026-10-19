# Find a visual direction, without requiring a brand folder

## Three starting points

**Existing identity:** read the selected guidelines and actual logo/font files. Extract
constraints with their source. Ask what is flexible. Improve execution inside those
constraints; do not turn a content request into a rebrand. Confirm gaps only.

**Partial identity or references:** preserve known assets and ask what the owner likes
about each example. Separate typography, hierarchy, imagery, color, density, texture,
and motion. A reference is evidence of a preference, not permission to copy a brand's
marks, layout, photography or protected artwork. Save `reference_notes` and provenance.
Conflicting references need a clear choice about which qualities matter.

**Starting fresh:** no folder or reference is required. Ask these in small groups, in the
owner's language, using their business context rather than a design questionnaire dump:

1. Who should feel this is for them, what do you sell, and what should they do next?
2. What three qualities should people feel? Offer useful contrasts in ordinary words:
   calm/energetic, precise/expressive, accessible/exclusive. Ask what would feel wrong.
3. Any colors, images or brands you like or dislike? References are optional. Explain
   what appeals to you if you have them; don't ask the person to know typography terms.
4. Do you have a usable logo or product photos? If not, offer an explicitly temporary
   typeset name and a feasible imagery approach. Don't invent customer/product images.
5. Which languages, channels and production budget/capacity do we need to support?

Reuse answers already supplied. Save partial answers with `brand-update`, including
`identity_status` (`existing`, `partial`, `new`), `design_personality`, and `reference_notes`
when known. Do not invent missing answers or require optional fields to be completed.

## First content request: ten actual style samples

Before creating a brand's first content batch, check `status.style_discovery`, `snapshot`,
selected style and approved creative memory. Existing identity does not by itself tell
us which social composition the owner prefers. Unless an owner-selected direction or
established approved content already supplies it, create **at least 10 actual post
samples in 10 distinct styles chosen from the 27**. Default to 10; an explicit request
for more may use up to all 27. A request for five posts still starts with this style
comparison, then the five requested posts follow the owner's choice. The owner may
explicitly supply a direction or narrow/skip the exploration; record that instruction.
Do not infer a waiver from a request for a full batch or private drafts.

1. Run `style-catalog` (or read `assets/style-catalog.json` from the plugin root).
   These are the 27 requested priorities, not the eight composition patterns and not a
   list of proven best-performing designs. Assess all 27 against the actual use case:
   audience and desired action, subject, identity constraints, language/script, channel,
   available meaningful imagery, budget and ability to sustain future production.
   Choose the best-fitting 10 with useful visual variety; do not always use the first
   ten, select by industry stereotypes, or treat a model score as evidence of quality.
   Save a short selection basis and a fit rationale/tradeoff for each selected style.
2. Preserve existing logos, colors, type and exclusions unless a change was explicitly
   requested. Adapt styles within those constraints; style exploration is not an
   unsolicited rebrand. For a new identity, propose real usable fonts/palettes.
3. Use one representative idea, truthful core message, language and target ratio across
   the ten samples so the owner compares style. Adapt wording/structure as needed to
   express the idea, with the same factual claim. Each option needs a visibly different
   treatment of hierarchy, imagery, texture, density or composition; ten recolors of
   one template do not qualify. Do not substitute ten prompts, swatches or moodboards.
4. Discover capabilities and follow [image acquisition](image-acquisition.md). No native
   image generator is required. Source, license and inspect suitable imagery, use an
   available connected design service, or produce high-quality permitted raster assets.
   Render each completed sample at the requested size and inspect original/mobile
   pixels. A style that cannot be executed well should be replaced by another suitable
   catalogue style. Do not count placeholders or failed renders toward ten.
5. Keep the previews in the selected brand's private workspace, labeled exploratory.
   Import each finished sample as `role=output` with truthful rights. Save a
   `style-propose` board with `mode: "first-content"`, `use_case`, `selection_basis`,
   current `brand_hash` and 10–27 options using catalogue IDs and `sample_asset_ids`.
   See [runtime](runtime.md) for the complete contract. The runtime binds actual sample
   bytes, rejects duplicates and never generates the images itself.
6. Present **all ten actual images**, clearly labeled by style, in the dashboard or a
   gallery/contact sheet with full-size access. Explain each fit/tradeoff briefly. Ask
   which style to follow (or which qualities to combine) and wait for the owner's
   answer before the requested production batch. This is a concrete choice after the
   samples are complete, not a permission request before doing the work. Do not select
   your own favorite on the owner's behalf. If no viewing surface works, deliver actual
   image files; do not ask the owner to choose unseen styles.

If fewer than ten viable styles can be completed because capabilities, rights or the
budget genuinely block them, keep the actual finished previews and explain the exact
remaining gap. Offer a concrete sourcing/tool alternative or owner-agreed narrower
scope. Do not claim the first-content comparison is complete or silently skip it.

Only the owner's choice permits `style-select`. It updates visual fields, preserves
business/audience context and invalidates brand approval; it never approves posts or
publishing. Show the resulting brand brief for the normal exact-hash approval. A stale
board cannot overwrite changed identity. For a requested hybrid, render the combined
sample and obtain the owner's choice of that concrete revision; the existing 2–4 option
`directions` mode remains available for focused refinements. Do not falsely label a
hybrid as an unchanged catalogue sample.

## Continue with the chosen direction

Read `context.selected_style` and inspect its bound sample on later runs, alongside the
current profile and approved creative brief/rules. Use the chosen treatment consistently,
while varying composition to serve each post's meaning. Do not repeat the ten-style
exploration for an unchanged selected brand or unrelated narrow revision. Retain earlier
boards as history. A new exploration is appropriate when the owner requests a change,
the use case substantially changes, or current samples conflict with revised identity.

For subsequent calibration within the selected style, use 1–3 representative finished
pieces where helpful. Include sequence/motion samples only when that format is planned.
Apply feedback to real exports and save approved reusable preferences. An explicit full
private batch can proceed once the style is chosen, without an extra sample-only pause.

Legacy 2–4 direction boards and established approved content stay valid on upgrade; do
not force existing customers to restart. `EXISTING_CONTENT` is a cue to inspect owner
approval/history, not evidence that every saved draft was approved. Use [brand quality](brand-quality.md)
for brand checks and [research findings](research-findings.md) for the limited historical
evidence. The catalogue is not the pending owner-provided study dataset, and style names
never guarantee quality.
