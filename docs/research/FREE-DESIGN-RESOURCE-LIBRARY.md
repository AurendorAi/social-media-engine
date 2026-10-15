# Free design resource library

Verified against primary source pages on **15 October 2026**. This is a directory of
23 production-resource sources, not a collected design dataset, a bundle of third-party
assets, or a claim that every item on every site is free. The user will provide the study
dataset. No substitute corpus is being acquired.

The plugin must **never create vector graphics**. Existing licensed or owner-supplied
vectors may be used as ingredients. Do not draw new SVGs, icons, illustrations or
procedural shapes, vectorize images, or hide newly drawn vector artwork behind a raster
export. Use real materials, raster generation/editing, typography and composition.
Canva, HyperFrames and other available tools are production options, not exceptions to
this rule. Tool availability and tool costs are separate from asset pricing.

## Choose a source for the actual visual job

| Need | Sources | Free scope and practical detail |
|---|---|---|
| Real photographic subjects and environments | [Pexels](https://www.pexels.com/license/), [Unsplash](https://unsplash.com/license) | Free licensed photos; exclude paid collections. Inspect the crop, resolution and depicted people/brands. Do not pass off stock as the client's actual product or premises. |
| Physical paper, fabric, stone and metal | [ambientCG](https://docs.ambientcg.com/license/), [Poly Haven](https://polyhaven.com/license), [cgbookcase](https://www.cgbookcase.com/textures), [3DTextures.me](https://3dtextures.me/about/) | CC0 materials. Select base-color maps or rendered imagery, not normal/roughness maps as artwork. 3DTextures has free 1K downloads; higher resolution/source/bulk options may cost. |
| Historic imagery, botanical subjects, art and cultural objects | [The Met Open Access](https://www.metmuseum.org/hubs/open-access), [Smithsonian Open Access](https://www.si.edu/OpenAccess), [rawpixel Public Domain](https://www.rawpixel.com/public-domain) | Only the explicitly Open Access/CC0 files. rawpixel derivatives and cutouts may use a different license even if their source is public domain. |
| Distinctive typography | [Google Fonts](https://fonts.google.com/), [Fontshare](https://www.fontshare.com/), [Collletttivo](https://www.collletttivo.it/) | Check the exact family and bundled license. Fontshare's adaptable-font entry is scoped to its OFL subset. Google Fonts includes Arabic families; test actual shaping and glyph coverage. |
| Coherent supporting icons | [Lucide](https://lucide.dev/license), [Phosphor](https://github.com/phosphor-icons/core), [Tabler](https://tabler.io/icons), [Iconoir](https://iconoir.com/) | Existing open-source icon families, with required license notices. Choose one family/weight. Icons do not automatically make a strong hero image. |
| Existing expressive illustrations or stylized objects | [Open Doodles](https://www.opendoodles.com/about), [Kenney](https://kenney.nl/assets) | CC0 published assets; select only when their visual language suits the brand. No new vector drawing or generic illustration as a default. Kenney's paid convenience bundles/tools are separate. |
| Existing repeating patterns | [Hero Patterns](https://heropatterns.com/) | Published SVG patterns under CC BY 4.0: credit Steve Schoger/Hero Patterns, link the license and indicate changes. |
| Broader discovery when a specialist source lacks the subject | [Openverse](https://openverse.org/), [Wikimedia Commons](https://commons.wikimedia.org/), [Iconify](https://icon-sets.iconify.design/), [SVG Repo](https://www.svgrepo.com/page/licensing/) | Mixed-license indexes. A search result is not clearance. Verify the exact original asset and select a free commercially adaptable option. |

For mixed media, start with a meaningful photographic or archival subject and a compatible
surface; don't assemble unrelated decorations. For editorial or luxury typography, compare
actual family specimens and language coverage before choosing. For tech layouts, prefer
client product captures and purposeful supporting icons over a generic technology symbol.
For tactile styles, inspect material scale at the final crop; obvious tiling undermines the
illusion. These are production starting points, not universal style recipes or quality claims.

## Search and acquire

The dashboard's **Find free design resources & fonts** section filters the source directory
by material, style or intent and shows free scope, source terms, credit requirements and
verification date. The equivalent CLI commands are:

```sh
python3 plugins/social-media-engine/scripts/sme.py resource-libraries --query paper
python3 plugins/social-media-engine/scripts/sme.py resource-libraries --kind font --query Arabic
python3 plugins/social-media-engine/scripts/sme.py resource-libraries --id googlefonts
```

These are **offline metadata filters**, not live web searches or asset downloads.
The runtime has four native search adapters: **Openverse, Commons, Iconify and the Met**.
The remaining sources use the host's browser/search tools and explicit file import; this
update does not implement 23 APIs. Poly Haven's separate API terms require visible credit
and a unique User-Agent; do not scrape its website as a substitute.

1. Read the brand, audience, message and existing approved materials. Define the subject,
   light, crop, palette, surface and output dimensions before searching.
2. Use a relevant source, inspect actual shortlisted assets and reject weak fits. Prefer
   free files with adequate resolution; a free low-resolution file is not automatically usable.
3. Inspect the exact license and access conditions. Record creator, asset URL, license URL,
   required notices, intended use and visual rationale with `resource-add` / `resource-review`.
4. Use `resource-fetch` for a supported direct public file, or `resource-import` for a file
   explicitly obtained through the source UI. Preserve provenance and credit. The runtime
   accepts PNG/JPEG/WebP, conservative static SVG and TTF/OTF/WOFF/WOFF2 within its size limits.
   Archives, PSD/EPS, 3D packages and video require suitable host tools; they are not native
   resource-import formats. Extract or convert only the chosen permitted ingredient.
5. Compose and inspect the actual export at native and phone size. Assess meaning, brand
   specificity, imagery, typography and detail, then revise. Technical checks and numerical
   scores cannot override owner rejection.

No bulk downloading, watermark removal or asset-pack redistribution. Licenses and access
can change: recheck when acquiring an item. A source listing does not mean its download
flow has been tested in every host; the catalogue records known access limitations.

## Sources deliberately excluded from the default directory

- **[Texturelabs](https://texturelabs.org/terms/):** its free commercial-artwork grant does
  not permit assisting AI image generation; templates/software bundling and bulk access
  also have restrictions. It is not a default AI-production source.
- **[unDraw](https://undraw.co/license):** its custom terms restrict integrations and AI/ML
  uses. Removed from the previous directory rather than treating free downloads as plugin
  integration permission.
- **[Transparent Textures](https://www.transparenttextures.com/):** an applicable license
  was not established from the inspected official page. Excluded pending verification.

## Evidence and limits

The machine-readable [catalogue](../../plugins/social-media-engine/assets/resource-libraries.json)
records 23 unique sources, supported material kinds, free scope, access notes, exact terms,
search methods, use cases, primary-source evidence and verification dates. It contains no
third-party asset files. It is intentionally small enough to inspect and maintain.

The earlier vector-only samples were rejected by the owner. Their “professionally usable”
labels are withdrawn, and the SVG-only benchmark is retired from normal use. This library
and policy correction improve the production workflow; new professional-quality output
has **not** been established by this change. Future quality evaluation must use the
[owner-supplied reference dataset](REFERENCE-DATASET-PLAN.md) and actual rendered results.
