# Resource sourcing and art direction

Use only existing sourced or owner-supplied vectors under their licenses; never create
new vector artwork or vectorize a raster. The [production boundary](../SKILL.md#production-boundary-no-newly-created-vector-graphics)
also prohibits rasterized model-authored vector or code-drawn substitutes.

Use this workflow before creating visual content. When native generation is missing or
a source fails, follow [image acquisition](image-acquisition.md) to select another
available source/service/rendering route without weakening quality or rights checks. Real photography, vectors, textures,
patterns and typography are production ingredients, alongside original composition and
AI tools. Default to source-first materials with zero asset acquisition cost: reuse approved
owner assets, then inspect suitable free licensed resources. “Free assets” does not mean
free tools, subscriptions or model calls; discover costs and follow existing authorization.
Do not force flat illustration or an icon as the hero when photography, texture, type or
another permitted medium better serves the actual brand and message. Do not default to generating an entire flattened post. Do not add materials
just to meet a quota: a strong typographic composition may need none.

## Start from the post, not a stock-image keyword
Read the approved brand context, item brief and available local materials in `snapshot`.
Write a short sourcing brief in `creative.sourcing`: visual purpose, material kinds,
palette, lighting, surface/era, subject, crop/negative space, output size, language,
exclusions and planned combination. Note when no external material would help.

For example, a calm coffee tutorial might need a close crop of real brewing equipment
and fine warm paper grain. A technology comparison might need an authorized product capture or a typographic
comparison; existing licensed icons can help only when they add meaning. Neither needs
generic decorative confetti or newly drawn vector objects.

Translate the brief into focused searches, including material, composition and physical
qualities: "warm uncoated paper fine grain", "pour over coffee hands overhead negative
space", "botanical engraving single branch". Search alternatives when the first results
are weak. Search only minimal, non-confidential terms; do not transmit the whole brand
profile, unpublished campaign or private reference images to a public search service.

## Find and inspect
1. Reuse this brand's acquired library if the rights and intended use still fit.
2. Filter the local source catalogue with `resource-libraries --query 'paper'`,
   `resource-libraries --kind font --query Arabic`, or inspect one stable source with
   `resource-libraries --id googlefonts`. These commands filter bundled source metadata
   only: no web search, live asset inventory or licence clearance occurs. Combine `--kind`
   and `--query` to narrow sources; then open the source and inspect actual assets.
   Built-in `resource-search` has only four native adapters: Openverse, Wikimedia Commons,
   Iconify and the Met. All other catalogue sources require browsing/manual sourcing.
   Search saves candidates, not cleared production assets. `kind` records intent;
   image APIs do not reliably classify style.
3. Use the host's web/image search or browser for specialist libraries and other public
   sources. Search within a useful library, or use a focused `site:` query. Visit the
   original asset page, not only a search thumbnail. Discover available host tools;
   if browsing is unavailable, use built-in search and explain missing capabilities.
4. Compare a small shortlist against the brief. Actually inspect images/previews. Check
   resolution at the planned crop, visual weight, negative space, lighting, authenticity,
   distracting details, text baked into images, cultural fit and language requirements.
   For icons, keep stroke, optical size and family consistent. For textures, check
   scale and repetition. Fonts need script coverage, shaping and licence checks.
5. Record the chosen candidate with `resource-add` when found outside built-in search.
   Reject a poor fit instead of inventing a fit score. Keep a concise rationale and
   discarded alternatives in the item's sourcing notes. A library result is not an
   owner-approved brand reference or permission to copy another designer's layout.

Do not scrape behind authentication, defeat anti-bot controls, remove watermarks or
purchase assets without authorization. Paid libraries and owner subscriptions can be
used through authorized host connections/browser sessions; record the purchase/licence
reference privately and use `resource-import` for the explicitly downloaded file.
Do not put signed download links, credentials or account-specific tokens in source records.

## Check source rights before production download
Read the exact source page and applicable licence. Search-index metadata is a lead.
Record the author, source, licence name/link, actual evidence and intended use. Check
commercial use, adaptations, required attribution, share-alike/notice obligations,
restrictions on logos/templates/redistribution, and recognizable people, property or
brands where relevant. Resolve uncertainty or choose another source. Do not infer
clearance from "free", a public URL, a stock site's general reputation or missing labels.

Use `resource-review` only after that inspection. Its booleans record your judgment;
the runtime cannot legally certify it. The default acquisition path accepts only reviewed
materials permitted for commercial adaptation. Restricted examples can remain candidates
or brand references; do not use them as production ingredients. Record a complete credit
in `attribution` (title/author, source, licence link, notices as needed). For assets without
required credit, record an honest source credit anyway. Record special obligations in
`evidence`; meet them in the actual output and handoff, or choose a simpler licence.

`resource-fetch` downloads a direct public HTTPS file. It rejects private-network
addresses, credential-bearing URLs, HTML, archives, active SVG and unsupported formats.
Current limits: 20 MB per material, 2 MB for static SVG. Supported: PNG/JPEG/WebP,
conservative static SVG, TTF/OTF/WOFF/WOFF2. Some legitimate complex SVGs need a trusted
static export; do not disable the checks. For libraries serving archives, extract only
needed files using trusted host tools, never execute scripts, then `resource-import`.
Other formats (e.g. PSD, EPS, full 3D bundles) require host conversion into supported
materials; do not claim the bundled runtime can edit or render them.

If a source times out, rate-limits or changes its API, show the actual failure, use a
browser/manual import or another source. Do not retry in a loop or quietly generate a
replacement while claiming it was sourced. Source inspection and download are distinct:
inspect actual downloaded bytes again before composition.

## Compose, then review the result
Use the selected materials as editable layers in the host's available design tools.
Crop for meaning, control contrast and color, unify line weights, place type deliberately,
and use textures at a scale/opacity that supports reading. Preserve a clear focal point.
Keep product accuracy and brand identity intact. Use raster AI generation/editing for a missing original element
or a justified edit when appropriate, with permission for external asset transmission.
Never call downloading ingredients a finished design.

Import actual finished media as `role=output`. Add the source assets to `material_ids`
and one `creative.material_uses` entry per material with purpose, edits and credit placement.
The runtime binds selected material bytes and provenance to content approval. Merely
adding an unused material does not invalidate the brand or other posts.

For this release, required attribution must appear verbatim in **every variant caption**
of an item using the material. Ensure the credit includes necessary modification notices;
`material_uses.edits` also records the exact transformation. If caption limits or brand
rules conflict, choose a different material or separate the variants into separate items.
Do not treat a CREDITS file as a replacement for public attribution.

Inspect actual final pixels at original and mobile sizes; watch full videos. Judge the
composition, visual coherence, readable type, crop and substance, not the number of
sources used. Export adds material provenance and CREDITS.md without redistributing
raw source files. Required notices beyond the credit must be supplied by the host.
