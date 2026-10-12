# Version 2 acceptance scenarios

The portable workflow generalizes editorial and production methods. It does not copy a
private company's creative library or guarantee the same output from every host/model.

| Scenario | Expected behavior |
| --- | --- |
| Established architecture studio with supplied guidelines | Read selected files; extract existing palette/fonts/logo rules; ask only for gaps; preserve identity |
| New ceramics maker with no folder | Ask audience, offer, personality, dislikes, channels; propose 2–4 directions; compare real samples when tools permit |
| Tutor with conflicting visual references | Explain the qualities in each reference; resolve the conflict; save the selected traits without copying artwork |
| Arabic and English brand | Ask language variety; use actual script-supporting fonts; inspect shaped text in final pixels; adapt captions rather than translate literally |
| Change “the whole batch feels generic” | Diagnose idea, evidence, visual mechanism and rhythm; rebuild the weak argument before reskinning |
| Revise one cover | Keep this feedback item-scoped unless the owner wants a broader rule |
| New chat, same brand | Read status/context, selected identity, rules and assets; don't repeat completed onboarding |
| Tool unavailable | Explain exact limitation and a feasible production path; don't call a brief a finished asset |
| Existing v1 workspace | Open without migration; preserve records; new discovery fields remain optional |

Technical tests use fictional data and synthetic review fixtures, not owner approval.
Host-specific installation, real creative quality and live provider behavior need separate
acceptance in the intended environment. No real publishing is part of automated tests.

Packaging references checked for this upgrade:
- [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins)
- [Claude plugin manifest reference](https://code.claude.com/docs/en/plugins-reference)
- [Claude marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)

## Validation completed for this candidate

- 57 standard-library runtime/API/release tests passed on the local Python environment.
- Chromium browser exercise passed with a fictional brand: saved onboarding and style
  selection, brand approval, actual image and video previews, ordered slide navigation,
  platform captions, incomplete-review blocking, mobile overflow, feedback and filters.
- Claude plugin and marketplace validators passed.
- Portable root manifest passed the published Agent Plugins 1.0.0 JSON schema.
- Skill frontmatter/reference validation and extracted ZIP portability tests passed.
- The deterministic ZIP contains 23 files and no brand workspace or external dependencies.

This candidate has not been installed and creatively benchmarked in both end-user hosts,
and no live social account was connected. The interface is English; brand/content language
and direction are preserved. Real-brand creative calibration remains essential.
