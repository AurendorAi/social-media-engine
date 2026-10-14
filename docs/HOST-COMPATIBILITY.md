# Host compatibility and installation

Verified 14 October 2026. This is a local skill plus a Python runtime, not a bundled
model, media generator, or hosted service. Host installation and runtime execution are
separate checks. The release ZIP keeps `plugin.json`, `.codex-plugin/`,
`.claude-plugin/`, `skills/`, `scripts/`, and `assets/` at its root.

## Codex

From a terminal with plugin-capable Codex installed:

```sh
codex plugin marketplace add AurendorAi/social-media-engine
codex plugin add social-media-engine@social-media-engine
```

For a local checkout, replace the first command's repository argument with its absolute
root path. Then use the same plugin selector. The repository root supplies the marketplace;
`plugins/social-media-engine` supplies the plugin. They are different directories.

Local CLI verification used `codex-cli 0.162.0-alpha.17.2`: `plugin --help`,
`plugin add --help`, and `plugin marketplace add --help` confirm both commands and the
selector syntax. These checks do not install anything into the reviewer's account.
Older installations may expose different commands; check their help or use the host's
plugin interface. Workspace policy and account availability can restrict installation.

OpenAI documents repo marketplaces at `.agents/plugins/marketplace.json`, portable root
manifests, and the `.codex-plugin/plugin.json` compatibility layout. GitHub distribution
is not submission to the public Plugins Directory. This repository ships both manifest
layouts and the local skills directory. See [OpenAI packaging documentation](https://developers.openai.com/plugins/build/plugins).

## Claude Code

Run these **shell** commands:

```sh
claude plugin marketplace add AurendorAi/social-media-engine
claude plugin install social-media-engine@social-media-engine
```

Or, inside an interactive Claude Code session:

```text
/plugin marketplace add AurendorAi/social-media-engine
/plugin install social-media-engine@social-media-engine
```

The interactive command may open plugin details and ask for scope. Follow the installation
summary for reload requirements. Invoke `/social-media-engine:social-media-engine`.
The shell installation route also works before a non-interactive session; `/plugin` is not
a non-interactive prompt command. See [Claude installation documentation](https://code.claude.com/docs/en/plugins/install).

For an unpacked ZIP or development checkout:

```sh
claude plugin validate /absolute/path/to/social-media-engine
claude --plugin-dir /absolute/path/to/social-media-engine
```

Use the plugin directory, not the repository marketplace root. Native validation passed
with Claude Code 2.1.206 for both this plugin and its repository marketplace. Validation
checks metadata, not model behavior or rendering quality. Current docs also describe ZIP
loading with `--plugin-dir`; the unpacked-directory route is the conservative example
here because that installed CLI version's ZIP loading was not exercised. See
[Claude plugin creation and local loading](https://code.claude.com/docs/en/plugins/create).

## Cowork and other hosts

Cowork's available plugin import/customization flow depends on the account. This audit
has not run a Cowork installation. Use its supported marketplace or plugin-ZIP import,
then verify local Python execution and workspace access before promising runtime support.
A cloud/chat surface is not assumed to share local desktop plugins or files.

Other agents can use the runtime if they can read the full installed skill and its
references, execute Python 3.10+, and write a user-selected workspace. Preserve the full
package: copying only `SKILL.md` breaks its relative script and reference paths. Root
`plugin.json` supplies portable metadata; automatic discovery, slash commands and plugin
installation remain host-specific and are not certified for untested products.

A manual runtime smoke check, from an unrelated directory:

```sh
python3 /absolute/path/to/plugin/scripts/sme.py --workspace /absolute/path/to/private-work --brand example status
```

Expect JSON with `ONBOARDING_REQUIRED` for a new brand. State belongs under the working
folder's `.social-media-engine/`, never inside the installed plugin. Paths with spaces
must be quoted. Windows can use `python`; Python needs IANA timezone data (`tzdata` may
be needed on Windows). The runtime's Python standard-library implementation is portable;
this audit's local execution does not establish a Windows or Linux test result.

## Capabilities to verify in every host

| Capability | Required support / honest fallback |
| --- | --- |
| Brand records and CLI | Python 3.10+, filesystem access, writable private workspace |
| Strategy, copy, critique | Host model; no bundled model or provider key |
| Verified research | Actual web/browser tools and inspected sources; record unavailable research honestly |
| Images, video, editable design | Discover available generation/rendering tools; instructions alone are not finished media |
| Visual review | Image/video inspection; never claim pixel review from source code alone |
| Local studio | Long-running local process and a browser that can reach its loopback port; otherwise inspect/export files |
| Public resource search | Network access to selected libraries when explicitly invoked; installation performs no resource search |
| Publishing / account data | Optional provider credentials, supported account capabilities, and existing approval/send gates |

No host compatibility workaround may bypass owner approval, asset validation, brand
isolation, or ambiguous-send protection.

## Release verification

`tests/test_release.py` extracts the exact ZIP into a temporary path outside the repository,
runs from a separate working folder with no inherited `PYTHONPATH`, checks local resource
catalog access, and verifies package files remain unchanged. Build checks cover matching
plugin identities/versions and marketplace sources. The installed CLI smoke also reads
empty creative memory, saves a proposal after brand approval, rejects a wrong approval
hash, approves the exact brief, retains the missing-samples calibration warning, and
checks a second brand cannot see that memory. These are packaging/runtime tests,
not an end-to-end host conversation or evidence of campaign performance.

Before releasing, run the full test suite and builder specified in `AGENTS.md`. For a host
acceptance check, install in an isolated test profile, invoke the skill, confirm the first
status is onboarding-required, and verify a new brand cannot export/publish approved
content without its required approvals. Do not connect real publishing accounts for a
packaging smoke test.
