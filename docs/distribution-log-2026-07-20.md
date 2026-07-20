# Distribution Log — Awesome-List Submissions (2026-07-20)

Executed on behalf of shkyyy18 (fully authorized, automated run). Source material: `docs/distribution-kit-2026-07.md`. Each target list's contributing rules were read before acting; unqualified channels were not forced.

## Results summary

| Project | Target list | Action | Result |
|---|---|---|---|
| cc-autopilot | e2b-dev/awesome-ai-agents → **redirected** to e2b-dev/awesome-ai-sdks | PR opened | https://github.com/e2b-dev/awesome-ai-sdks/pull/289 |
| openbid-intel | awesome-selfhosted/awesome-selfhosted | **Skipped — not eligible** | reasons below |
| kimi-adapter | hesreallyhim/awesome-claude-code | **Skipped — submissions temporarily locked** | reasons below |

---

## 1. cc-autopilot → e2b-dev/awesome-ai-sdks — PR opened ✅

- **Scope check:** `e2b-dev/awesome-ai-agents` README states: *"For adding AI agents'-related SDKs, frameworks and tools, please visit Awesome SDKs for AI Agents. This list is only for AI assistants and agents."* AgentCron (cc-autopilot) is a cron + watchdog **tool for** AI coding agents, not an agent itself — out of scope for awesome-ai-agents. The same org's sibling list `e2b-dev/awesome-ai-sdks` (renamed from `awesome-sdks-for-ai-agents`; old URL redirects) explicitly covers "SDKs, frameworks, libraries, and tools for creating, **monitoring**, debugging and deploying autonomous AI agents" and accepts PRs ("Do it via pull request"). Submitted there instead of forcing a bad-fit PR.
- **Action:** forked to `shkyyy18/awesome-ai-sdks`, branch `add-agentcron`, added an alphabetical entry (between AgentOps and Chidori) in the list's `## [Name](url)` + tagline + `<details>` format, committed via Git Data/Contents API.
- **PR:** https://github.com/e2b-dev/awesome-ai-sdks/pull/289 — "Add AgentCron — cron + watchdog for unattended AI coding agents"
- **Status:** open, awaiting maintainer review (review latency on this list is historically days to weeks).

## 2. openbid-intel → awesome-selfhosted — skipped ❌ (not eligible)

Read `awesome-selfhosted/awesome-selfhosted-data/CONTRIBUTING.md` (the main repo's PR template redirects all submissions there). Two hard blockers:

1. **Scope mismatch:** the list is for self-hosted *network services and web applications*. OpenBid Intel is a local CLI toolkit that generates a static, self-contained HTML dashboard — there is no server component to self-host. The "What does not qualify" section excludes desktop/mobile/command-line applications in this category of submission.
2. **Age rule:** the PR template requires *"Any software project you are adding was first released more than 4 months ago."* `shkyyy18/openbid-intel` was created 2026-07-12 (8 days old at submission time).

Submitting anyway would violate the list's stated rules and waste maintainer time. Revisit no earlier than ~2026-11 (4-month mark), and only if the project grows a genuinely self-hostable service component; otherwise this list is simply the wrong venue. (The kit's suggested "Miscellaneous" section does not override the CLI/age disqualifiers.)

## 3. kimi-adapter → hesreallyhim/awesome-claude-code — skipped ⏸️ (submissions locked)

- **Channel verified:** recommendation goes through a **GitHub issue form** (`.github/ISSUE_TEMPLATE/recommend-resource.yml`), not an external web form — so it is an acceptable channel per the "no manual web forms" rule. An automated workflow (`validate-new-issue.yml`) validates issue bodies parsed as `### Field` sections; the labels `resource-submission` / `validation-pending` exist.
- **Prepared submission** (form-equivalent body, category `Providers, Runtime & Integration Infrastructure`, description per the kit draft, link/author fields, all three checklist items) was validated against the repo's own parser rules (`resources/parse_issue_form.py`: required fields, https:// links, 10–500 char description, exact category name from `config.yaml`) before attempting submission. No duplicate found in open/closed issues or `THE_RESOURCES_TABLE_NEW.csv`.
- **Blocked:** `gh issue create` was rejected with *"Interactions on this repository have been restricted to collaborators only."* The maintainer's own pinned issue #2310 *"Let it bake for a minute"* (2026-07-19) indicates submissions are temporarily paused. This is a repository-level lock, not a CLI limitation.
- **Next step:** retry the prepared issue in a few days (e.g. after 2026-07-24) once the interaction restriction lifts. The prepared body is archived here verbatim:

```markdown
Title: [Resource]: Kimi Adapter
Labels: resource-submission, validation-pending

### Display Name

Kimi Adapter

### Category

Providers, Runtime & Integration Infrastructure

### Link

https://github.com/shkyyy18/kimi-adapter

### Author Name

shkyyy18

### Author Link

https://github.com/shkyyy18

### Description

Local proxy that lets the Claude Code VS Code extension run on a Kimi backend by rewriting Anthropic `document` attachment blocks into text blocks, with buffered retry and pass-through auth.

### Checklist

- [X] I checked that this resource isn't already on the list
- [X] All links are working and publicly accessible
- [X] This resource is specific to Claude Code
```

---

## Notes

- One submission per project per venue; nothing was posted twice.
- No manual web-form channels were used (per standing rule).
- The kit's 2026-07-31/08-04/08-06 cadence dates for awesome lists were overridden by the "run now" instruction for this batch; HN/Reddit cadence in the kit is unchanged and untouched.
