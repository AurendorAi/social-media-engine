# Social Media Engine

**Everything social media, in one plugin.**

Ask your agent: **"Use Social Media Engine to set up my brand."**

Bring guidelines, a few references, or no visual identity at all. The first run asks a
few relevant questions, can save 2–4 visual directions for you to compare, and asks you
to approve the brand brief before generating content. Later runs resume that brand's
workspace. Use a separate brand identifier for each brand.

## Creative direction is included
An ordinary content request activates concept development, meaningful imagery, writing
designed with the visual, and review of real native and phone-sized exports. You do not
need an extra “be creative” prompt. The [shared workflow](skills/social-media-engine/references/creative-defaults.md)
adapts to each brand and preserves approved directions for narrow revisions. It uses
your host's actual tools; it does not guarantee equal results from every model.

## Requirements
- Codex or Claude with local skill execution and access to your chosen working folder.
- Python 3.10 or newer; `python3` on macOS/Linux, `python` on Windows.
- An IANA time-zone database. If missing on your machine, install Python's `tzdata`.
- Creative tools are optional, but actual image/video production requires an available
  renderer or generation tool. The plugin does not include model credits.

## What is included
Brand memory, scoped feedback, monthly plans, platform/language variants, asset records,
revision-bound reviews, owner approval, a loopback review dashboard, manual export,
an optional Postiz publishing adapter, and evidence-backed analytics records.

The agent performs creative work using your host's model and available tools.
The runtime stores and checks the workflow. It does not generate media by itself.
Remote accounts, real publishing, analytics permissions, and inbox access require your
own authorized providers. No provider or platform is silently connected.

## Production materials and boundaries
Never create new vector artwork, SVG illustrations, icons, procedural drawings or
vectorizations, including code-drawn artwork later rasterized. Existing licensed or
owner-supplied vectors are allowed ingredients. Use real sourced materials, raster image
generation/editing, typography and composition with available tools.

The searchable Design library directory contains 23 sources for free photography,
textures, patterns, fonts, archival imagery and existing graphics. Each entry records
free scope, terms and access limitations; mixed-license indexes require individual
asset verification. Four native search adapters are included; other sources use the
host's browser and explicit import. No third-party asset files are bundled.

Study references will come from the owner-provided dataset, not a substitute internet
dataset. Owner rejection overrides internal quality scores.

## Creative workflow
Research the audience's actual situation, develop an argument and useful payoff, then
choose a composition that demonstrates it. Discover available design/motion tools and
prove a small sample before scaling. Use owner feedback to revise actual exports and
save approved preferences for the next run. No fixed palette, font, dialect or industry
is imposed on your brand.

## Dashboard
Today shows your next useful action. Review posts shows one piece at a time with slide
navigation, platform captions and written change requests. Publishing contains exports
and delivery records. Results contains observed metrics. Find brand setup, plans and
saved feedback under More tools. Interface labels are English; content retains its language.

Ask: "Open my Social Media Engine review dashboard."
The agent runs `scripts/sme.py --workspace /absolute/working/folder --brand my-brand dashboard`
using Python. Keep that process running. Open the printed URL on the same machine.
Treat its token-bearing URL as private. This is a single-owner local dashboard, not a
publicly deployable multi-user web app.

## Safety and ownership
All data is local under `.social-media-engine/` in the working folder. Keep this folder
out of public repositories. Back up the whole folder while the dashboard is stopped.
Provider calls send selected assets/captions to that provider only after explicit consent.
Do not put credentials in brand answers. Use environment variables outside chat.

A passed review is not a guarantee of quality or platform acceptance. Inspect actual
outputs and approve them. Published content cannot be recalled by deleting local files.
See the bundled skill references for complete workflow and command contracts.

Built by [Aurendor](https://www.instagram.com/aurendor/).
MIT licensed. Support: [mohammedj@aurendor.io](mailto:mohammedj@aurendor.io).

## Design library (2.1)

Search public libraries for real imagery, icons, textures and patterns. The assistant
can also browse specialist libraries and import explicitly selected files. Source
inspection, licence evidence, style rationale and item-level material tracking are part
of production. Open **More tools → Design library** to search and review saved materials.
See [resource sourcing](skills/social-media-engine/references/resource-sourcing.md) and
[CLI contracts](skills/social-media-engine/references/runtime.md).

## Creative memory (2.2)

Ask: “Study my existing content and audience. Propose a distinct creative brief and
show me three actual samples before scaling.” Review the proposed direction with your
assistant. Approved briefs and sample references persist separately for each brand;
profile, feedback and sample changes can require a fresh review. Today and Brand & assets
show the current status. New proposals never replace approved direction automatically.

Read the [brand-quality workflow](skills/social-media-engine/references/brand-quality.md)
and [original research findings](skills/social-media-engine/references/research-findings.md).
The research is a partial study, not completed style quotas or model training. This plugin
ships original guidance, not Canva artwork or the author's private brand identity.

Other capable assistants can read `skills/social-media-engine/SKILL.md` and run the bundled
Python runtime. Preserve the package folder structure; native plugin support is host-specific.
