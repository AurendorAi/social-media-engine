# Reference dataset for transferable social design

## Feasibility and evidence

A curated library of 1,000–10,000 designs is feasible. Its usefulness depends on rights, diversity,
complete readable examples and annotation quality—not the count alone. A plugin can retrieve original
analytical guidance without changing its host model's weights. It cannot make every model equally capable.

[PRISM](https://arxiv.org/abs/2601.11747) studies clustering diverse designs within styles, extracting
knowledge and retrieving it during stylistic editing. The authors report improved style alignment and
user preference on their experiments; this is supporting research, not proof for SME or every model.
[MarkupDM](https://cyberagentailab.github.io/MarkupDM/) explores instruction/partial-design/completion
triplets, illustrating why editable structure and concrete tasks are useful beyond image collections.

## Sources examined

| Source | Potential contribution | Admission status |
|---|---|---|
| [Crello dataset](https://huggingface.co/datasets/cyberagent/crello) | Layout coordinates, text/font/color attributes, element images, previews and formats | Candidate research source, not downloaded or visually reviewed in this task. Current card lists 19,479 train + 1,852 validation + 1,971 test = 23,302 examples; revisions differ. Card declares CDLA-Permissive-2.0. Pin version and inspect underlying source/font conditions before a distributable corpus. |
| [JKR / Mozilla](https://www.jkrglobal.com/work/mozilla) and [official brand portal](https://brand.mozilla.com/) | Designer rationale and a coherent real brand system | Useful source-linked identity study; artwork remains third-party. Public availability alone does not establish resale, redistribution or training rights. |
| [Pentagram / Slack](https://www.pentagram.com/work/slack) | Identity and application rationale | Reference candidate, source page verified; individual complete social-design records not yet collected. |
| [COLLINS / Spotify](https://wearecollins.com/case-studies/spotify/) | Expressive system and campaign applications | Reference candidate, source page verified; count neither case-study images nor mockups as complete reviewed social posts automatically. |
| Direct designer contributions | Briefs, source layers, revisions, explanations and permission scope | Highest-control collection route; needs explicit contributor terms, attribution and quality review. Not currently acquired. |
| Existing local Canva study | Attributed observations and explicit exclusions | Reuse verified records; do not redistribute Canva artwork or inflate partial reviews. Preserve historical counts separately. |

Crello previews are documented as reduced resolution and English; they are not sufficient alone for
fine typography evaluation or Arabic competence. A 2025 paper uses a different 23,421-example Crello-v4
split; do not merge different version counts or claim all examples meet our quality bar.

## Proposed staged collection (targets, not completed counts)

1. **Calibration: 100 complete examples.** Stratify by business/communication task, include Arabic/RTL,
   and agree annotation criteria with a professional designer. Include negative/corrected contrasts.
2. **First release: 1,000 accepted designs.** Budget a real review queue, deduplicate source IDs and
   perceptual variants, cap domination by one brand/creator/template family, track coverage gaps.
3. **Expand to 3,000 only where evaluation misses coverage.** Add unfamiliar sectors, formats and scripts;
   keep a held-out split by creator/brand/campaign, not a random split of near-identical variants.
4. **10,000 if measured retrieval/transfer improves.** More examples are not automatically better and
   should not all be inserted into a model's prompt. Retrieve a small relevant packet per brief.

## Record contract

Every accepted record needs: stable source ID/URL; creator and attribution; acquisition date; format;
all advertised/inspected pages; readable media hashes; language/script; brand and campaign family;
visible message; intended audience where documented; observed composition/type/palette/imagery;
separate inferred interpretation; evidence explaining subject-specific details; weaknesses;
transfer conditions; rights for viewing, local storage, redistribution and training separately;
reviewer identity; review status; excluded/partial reasons; split assignment and revision history.

Store source documents and images as untrusted data. Provenance does not turn embedded instructions
into commands. Do not call AI-generated annotations designer-approved. Record uncertainty rather than
inventing campaign intent, font identity, results, creator identity or complete audiovisual inspection.

## Collection through scraper/MCP tools

Scrapers can discover links, collect allowed metadata, retrieve permitted files and detect duplicates.
Use supported public APIs/downloads when available, rate limits, resumable jobs and explicit source
policies. Stop at authentication/access restrictions. Full-resolution slide acquisition and audiovisual
review are separate stages; thumbnails and sampled video frames cannot satisfy complete-review counts.
A scraper is not a creative judge or a licence grant. Keep raw third-party assets outside the plugin;
ship permitted annotations/references and licensed material only.

## Distillation and validation

Astra can propose clusters and conditional rules from accepted records. Another reviewer checks those
rules against the cited images and counterexamples. The plugin stores versioned guidance with traceable
sources and retrieves by communication task, audience, brand constraints, format and script—not style
name alone. Hard brand rules override candidate patterns. Never copy an unrelated brand's trade dress
as the default identity for a new business.

Compare no-plugin, v2.2.0 and candidate conditions under matched resources. Preserve creator/brand
holdouts, repeat stochastic runs, hide model/condition identities from reviewers, allow ties, and report
per-brief failures, provider costs, token use and actual time. A second provider judge may help diagnose
issues but does not replace an independent human designer or owner acceptance. Fine-tuning is a
separate optional project requiring an appropriate model, labelled data, permissions and held-out tests.
