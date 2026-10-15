# Professional creative production

## Direction before rendering
Choose composition from the post's argument. For an established brand, reuse its approved
visual vocabulary while varying imagery, hierarchy, storytelling and rhythm. For new or
uncertain identity, use [style discovery](style-discovery.md) before production. Don't
force four concepts or a new direction for a simple revision.

Use [production toolkit](production-toolkit.md) to select available methods and prove a
representative render before scaling. A review that says "generic" needs a diagnosis:
weak argument, irrelevant imagery, repeated composition, buried mechanism, unnatural
voice or interchangeable pacing. Fix that cause; swapping a surface treatment is not a
substantive revision.

Use supplied brand typography, palette, logo rules, photography, and reference material.
Do not redistribute or assume licences for a font. Inspect font coverage for every
required script. For Arabic, verify shaping, bidi order, punctuation, numerals, joining,
and actual line breaks. For Japanese, verify glyph coverage and appropriate line breaks.
Never substitute missing brand assets without explaining and getting agreement.

Before execution, use [conditional composition guidance](design-patterns.md) to make a
compact plan from this audience, message and available material. Its original weak/better
contrasts diagnose specific failures; they are not style assignments or tested recipes.

## Execution
Discover native tools and connectors in the current host. Possible backends include
image generation/editing, Canva, video generation, HTML/SVG rendering, or Remotion.
Use their applicable instructions. These are optional capabilities, not bundled services.
Do not claim to have called a backend that is unavailable.

Produce actual files with editable sources where feasible. Preserve original logo and
product proportions. Don't invent text in a generated image and assume it is correct;
typeset or proof it. Use current destination specs and safe zones. Plan a carousel as
a sequence: promise, development, examples/proof, useful payoff, appropriate CTA.
Each slide should work at phone size without cramming.

For video: write a timed script and storyboard, design shots and transitions that serve
the idea, use licensed audio, render the actual file, inspect duration/dimensions and
decode, watch the ENTIRE video with sound, and inspect caption timing/safe zones.
Do not call a storyboard or still preview a completed video.

## Recognizable subjects and readable small views

Inspect the full exported composition at its intended on-screen phone width, without
zooming in to rescue labels. Check every comparison label, condition, logistics line and
CTA through its final word. A large source canvas does not make tiny text readable.
If a card or text block overflows, first remove or relocate obscuring icons/decoration,
then shorten nonessential copy or reflow/split the content. Do not solve crowding by
shrinking required text until only the headline remains usable. After each edit, check
adjacent elements and the complete export again; bounds can pass while text is occluded.
If the same text region fails again, rebuild that region: allocate a clean text area,
remove overlapping ornament, reflow the actual copy, then render and measure anew.
Repeatedly nudging an icon does not resolve an invalid layout. Where measurement tools
exist, require text bounds to fit both the canvas safe area AND the intended card,
label, pill or other text container, accounting for its padding and coordinate transforms.
Record unavailable measurement honestly; do not claim a bounds check from source values.

Check the subject against an authorized reference, including its identifying silhouette
and functional details. For example, a generic cone or stacked circles labeled “dripper”
does not necessarily depict a recognizable coffee dripper. Draw its actual relevant
structure, use a suitable authorized photograph, or present an explicitly abstract
illustration without claiming it demonstrates the real object. A label cannot repair a
misleading depiction. Stylization is allowed; verify that it preserves what this message
needs viewers to recognize rather than requiring photorealism for every brand. Check
orientation and functional geometry, not only silhouette: a vessel must read as having
a plausible opening, body and base; a pouring/filtering object must have a coherent
flow direction. Compare these parts with the actual reference before labeling the image.
If the geometry is uncertain, obtain a reference or use an honest alternative.

## SVG Arabic placement: direction and anchor together

In horizontal SVG text, `text-anchor` is relative to the text direction. With
`direction="rtl"`, `start` anchors the right side of the text chunk at `x`; `end`
anchors its left side. Thus `direction="rtl" text-anchor="end" x="1008"` can push
Arabic text off the right edge of a 1080-wide canvas. Use `start` for a right-edge
anchor; for a centered line, use `middle` at the intended center. This follows
[SVG text alignment](https://www.w3.org/TR/SVG2/text.html#TextAnchorProperty).

Minimal placement example, with an illustrative 72-unit inset (not a platform safe-zone
specification). Replace the demonstration font with the approved, loaded Arabic font:

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1350"
     viewBox="0 0 1080 1350">
  <rect width="1080" height="1350" fill="white"/>
  <text x="1008" y="180" direction="rtl" text-anchor="start"
        font-family="sans-serif" font-size="56" fill="black"
        lang="ar">ورشة فخار</text>
  <text x="540" y="280" direction="rtl" text-anchor="middle"
        font-family="sans-serif" font-size="40" fill="black"
        lang="ar">تجربة تبدأ من الطين</text>
</svg>
```

This demonstrates anchor placement, not automatic fitting or a recommended brand style.
Set explicit `x` on each separately positioned line or `tspan`, preserve normal Unicode
Arabic character order, and let a capable renderer perform shaping and bidi layout.
Do not reverse characters or use bidi override to repair alignment. Check mixed Latin,
numerals and punctuation in the actual sentence; handle runs deliberately when needed.

Before measuring, wait for fonts to load and verify the actual rendered font covers the
required script; a declared family or successful font request does not prove glyph
coverage. Generic `sans-serif` here is only a demonstration fallback. If the approved
font lacks Arabic, request an approved compatible alternative rather than silently
changing identity. If the export renderer cannot shape Arabic, use a capable available
renderer or report the capability block; do not treat disconnected letters as finished.

When available, harvest every text element's rendered bounds and compare them with its
intended safe region. For SVG, `getBBox()` uses local coordinates: transform its corners
to canvas coordinates before comparing transformed elements. In a browser,
`getBoundingClientRect()` values must be compared in the same viewport coordinates as
the SVG and safe region. Check both left/right and top/bottom overflow after fonts load,
including each multiline chunk. Repair wrapping, scale or placement, then re-export.
Bounding boxes do not prove correct shaping, readability or absence of clipping/masking.
Inspect the actual export at native and phone sizes, including all glyphs and diacritics.
If bidi placement fails again, simplify the affected line before adding more positioning
rules: use normal logical-order text in one plain SVG `text` element, `direction="rtl"`,
`text-anchor="middle"`, and `x` at the center of its allocated region. Remove inherited
transforms and per-character offsets from that trial; isolate mixed-script runs if needed.
This is a diagnostic fallback, not proof of correctness or a universal layout preference.
Render it with the actual font and inspect the whole line and measured bounds; preserve
brand constraints when integrating a verified repair. If even the simplified render fails,
use a capable available text renderer or report the block rather than certifying it.
Do not copy this SVG anchor recipe into HTML/CSS blindly: use that layout system's
`dir`, alignment and bidi rules and inspect its actual result.

## Handoff
Import finished files with role `output` and accurate rights. Keep reference images out
of deliverables. Save editable sources alongside the user's working files; link them in
the creative brief. Every published image needs useful alt text; a carousel needs ordered
alt text for every slide. Keep language variants separate when the artwork changes.

View actual exports at original and mobile sizes before sending to a critic. Fix
obvious overflow, poor contrast, missing glyphs, awkward crops, incorrect logos, weak
hierarchy, unnatural pacing, and export artifacts. A source-code review is not visual QA.
If tools cannot render or display outputs, report what is blocked and offer a supported
alternative rather than returning mock assets as finished work.

Before rendering, follow [resource sourcing](resource-sourcing.md) to find, inspect and
compose suitable real materials. Keep the brief, actual sourced ingredients, editable
composition and final rendered files distinct. Use AI where it helps the concept.

## Apply the same rigor to each brand

Follow [brand quality](brand-quality.md): establish the real baseline, save the selected
brand's creative brief, and connect audience situation, evidence, mechanism, payoff,
voice and meaningful materials. Transfer the method, never another brand's identity.
Check cross-brand layout repetition and repetitive CTA-only ideas before scaling.
Use [research findings](research-findings.md) as conditional observations, not templates
or sector-to-style assignments. Owner constraints and actual feedback take precedence.

Use the [producer revision loop](producer-revision-loop.md) for concrete inspect/repair
steps and stopping conditions before independent review.
