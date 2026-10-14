# Architecture

## Package boundaries
- Repository marketplace files select `plugins/social-media-engine`.
- Native Codex and Claude manifests wrap the same portable skill.
- The skill routes onboarding, strategy, creative production, review, publishing and learning.
- Python CLI and SQLite provide state, validation and durable audit records.
- A loopback dashboard uses the same runtime functions, not a separate mock API.
- Postiz is an opt-in adapter. The host supplies the model and optional creative connectors.

## State and trust
Every operation selects an existing absolute workspace and explicit brand identifier.
The private state directory contains SQLite, imported hash-addressed assets and exports.
Records are keyed by kind, brand and ID; transactions serialize mutations.
A workspace is a trusted owner's boundary, not a shared SaaS tenant boundary.

The approved brand hash covers questionnaire answers and reference/identity assets.
Item context adds currently applicable approved rules. Output assets and sourced design materials do not alter brand
identity. Selected material bytes, licence evidence and usage records bind only the
items that reference them. An item hash includes its exact variants, revision, context and imported media.
Review records bind that hash. New revisions cannot inherit old owner approval.

Prepared dispatches bind owner-reviewed content, actual account IDs, provider identity,
operation and UTC time. SENDING is persisted before remote writes. Partial/ambiguous
acknowledgments are retained for investigation, not automatically retried.
The adapter distinguishes provider acceptance from publication evidence.

## Deliberate runtime boundaries
The runtime does not contain an LLM service, media-generation provider, social OAuth
broker, production metrics scraper, or universal inbox. Those use actual authorized
host tools/provider exports. Unavailable capabilities must remain explicitly unavailable.
Natural-language creative rules require meaningful review; optional caption constraints
are deterministically enforced in the runtime.

The dashboard is local/single-owner. Public hosting needs a separately designed security
and operations layer. No local UI label is evidence of a remote integration.

## Local migration archive
During productization, the copied internal application was moved to the ignored
`.data/legacy-reference/` under the plugin repository. It remains recoverable locally
and is excluded from the public package. The original reference application was not
modified. The public rewrite does not erase prior Git history; a clean downloadable
plugin artifact is distinct from rewriting the repository's historical commits.

## Resource sourcing

`resources.py` normalizes four public search APIs and stores candidates per brand.
Search is explicit and transmits only minimal query words. Host browsing supports other
libraries. A licence/style review is an authored record; acquisition never infers it.
`resource_http.py` validates public HTTPS, pins the connection to validated DNS addresses,
checks redirects and limits reads. Downloaded bytes are sniffed; active/complex SVGs,
HTML and archives are refused. Manual imports pass through the same format checks.

The material asset includes immutable provenance. Production items declare material_ids
and exact usage. Required attribution is enforced in all variant captions. Brand context
excludes materials so an unrelated download does not invalidate approvals. Final media,
material provenance and credits travel in handoffs, without raw source redistribution.
