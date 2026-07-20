# Distribution Kit — Top-3 Projects (2026-07)

**Status: DRAFT for owner review. Nothing in this file has been published anywhere.**

Scope: cc-autopilot (77), openbid-intel (76), kimi-adapter (71). All three score just below the "excellent" line; the only missing signal is community traction (stars). Distribution is the one lever left.

Rules of engagement:
- One shot per project per platform. If a post flops, do **not** repost it.
- Space posts for the same project 2–3 days apart; stagger the three projects so nothing looks like a spam wave.
- Post in English (international platforms).
- Disclose authorship plainly ("I built this"). No astroturfing, no vote-begging.

---

## 1. Project selling points (distilled from the READMEs)

### cc-autopilot (AgentCron)
- Cron + watchdog for unattended AI coding agents (Codex, Gemini CLI, any custom command).
- Detects the failure mode raw schedulers can't see: **exit-0-but-empty "silent failures"**, plus hung process trees and Windows Task Scheduler PATH/encoding traps.
- Zero runtime dependencies, Python 3.9+, Windows-first but cross-platform, local-only, structured logs, `status --json` for monitoring integration, optional failure webhooks.
- Verified demo output and a 30-test dependency-free suite are in the README — lead with that credibility.

### kimi-adapter
- Local proxy that lets the Claude Code VS Code extension run on a **Kimi** backend.
- Solves a concrete, reproducible pain: Claude Code sends attachments as Anthropic-native `document` blocks, which Kimi's Anthropic-compatible gateway rejects with `API Error: 400`. The adapter transparently rewrites `document` → `text` blocks.
- API key never touches the adapter (headers pass through untouched); optional PDF text extraction; buffered retry against truncated streams; single-file script, pip package, or Docker.

### openbid-intel
- Local-first tender/bid intelligence: normalizes messy procurement exports (CSV/JSON/JSONL, EN+CN field aliases), deduplicates, ranks against an editable industry profile, and produces a digest + self-contained HTML dashboard.
- **Explainable scoring**: every 0–100 score itemizes each positive/negative/zero contribution (business line, buyer, stage, budget, recency, deadline) and reconciles exactly to the total.
- Nine built-in industry packs, local overlays for private rules, SQLite storage, zero runtime dependencies, deterministic `--as-of` for reproducible runs, live demo on GitHub Pages (synthetic data only).

---

## 2. Show HN drafts

### 2.1 cc-autopilot

**Title (73 chars):**
```
Show HN: AgentCron – cron + watchdog for unattended AI coding agents
```

**First comment:**

> Hi HN, I built AgentCron because I kept getting burned by the same class of failure: I'd schedule an AI coding agent (Codex / Gemini CLI) to do a nightly review, and a raw scheduler would happily report success while the agent had actually produced nothing.
>
> Unattended agent jobs fail differently from normal scripts:
> - the CLI exits 0 but returns an empty or four-character response;
> - a tool call hangs and leaks child processes;
> - Windows Task Scheduler runs with a different PATH/encoding than your terminal;
> - nobody notices until the output is needed.
>
> AgentCron is the small reliability layer between the scheduler and the agent. It flags exit-0-but-empty runs as `silent-fail` (configurable `min_output_chars`), enforces timeouts with process-tree cleanup, does bounded retries, keeps structured logs per run, and gives you one `agentcron status` view (with `--json` and a non-zero exit code so unhealthy jobs break your existing monitoring). Optional webhooks notify on failure — metadata only by default, never the prompt or agent output unless you opt in.
>
> Design constraints I stuck to: zero runtime dependencies (stdlib only), Python 3.9+, Windows-first (schtasks) but works with cron on Linux/macOS, and fully local — no hosted control plane. The README's demo transcript and test suite output are captured from real runs, not mockups.
>
> Repo: https://github.com/shkyyy18/cc-autopilot
>
> Happy to answer questions, and genuinely curious how others babysit scheduled agent jobs today.

### 2.2 kimi-adapter

**Title (66 chars):**
```
Show HN: Run Claude Code on a Kimi backend, with attachments
```

**First comment:**

> I wanted to use the Claude Code VS Code extension with Kimi's Anthropic-compatible endpoint. Chat worked, but every time I attached a code or text file the request died with `API Error: 400 Invalid request`. The reason: Claude Code sends attachments as Anthropic-native `document` content blocks, and Kimi's gateway doesn't accept that block type.
>
> Kimi Adapter is a tiny local proxy that sits between the extension and `api.kimi.com`. It forwards everything as-is except one transformation: `document` blocks are rewritten into `text` blocks Kimi can handle (optionally extracting PDF text if you install `pypdf`). Point `ANTHROPIC_BASE_URL` at `http://127.0.0.1:18231` and attachments just work.
>
> Properties I cared about:
> - **Key never touches the adapter** — auth headers pass through unread and unlogged.
> - **Buffered retry** — the single-file version reads the full upstream response and validates stream integrity before replying; a mid-stream disconnect retries up to 3 times instead of handing the client a truncated JSON (`Unterminated string`).
> - **Zero/optional deps** — one Python file, or `pip install -e .`, or Docker; a VS Code task auto-starts/stops it with the editor.
>
> Known limits: text attachments and PDF only (no image blocks), and obviously requests fail while the adapter isn't running.
>
> Repo: https://github.com/shkyyy18/kimi-adapter

---

## 3. Reddit drafts

### 3.1 cc-autopilot → r/ChatGPTCoding (primary), r/selfhosted (secondary)

- **r/ChatGPTCoding**: audience actively runs Codex-style agents and complains about unattended-job reliability; the silent-failure angle is a direct hit.
- **r/selfhosted**: the tool is local-only, zero-dep, and slots into existing schedulers/monitoring — matches the sub's ethos. Post here only if the first post got a civil reception; wait the full 2–3 days.

**Title:** `I kept scheduling AI coding agents overnight and they "succeeded" while doing nothing — so I built a watchdog`

**Body:**

> Raw schedulers (cron, Windows Task Scheduler) can tell you a process started. They can't tell you whether your AI agent did any useful work. My scheduled Codex/Gemini jobs kept failing in a specific way: exit code 0, output of four characters, nobody notified.
>
> AgentCron is a small Python layer between your scheduler and the agent:
> - flags exit-0-but-empty runs as `silent-fail` (configurable minimum output length)
> - timeouts with process-tree cleanup, bounded retries
> - per-run structured logs, one `status` view, `--json` output with non-zero exit for unhealthy jobs
> - optional failure webhooks (metadata only unless you opt in)
> - zero runtime dependencies, stdlib only, local-only
>
> Install: `pip install "git+https://github.com/shkyyy18/cc-autopilot.git"` then `agentcron init`.
>
> Repo: https://github.com/shkyyy18/cc-autopilot — README has real captured demo output and the test suite. Feedback welcome, especially from people running scheduled agent jobs on Windows.

### 3.2 kimi-adapter → r/ClaudeAI (primary), r/LocalLLaMA (secondary)

- **r/ClaudeAI**: the exact user base (Claude Code extension users) and a known recurring question — "can I run Claude Code on a non-Anthropic backend". Cite the concrete 400-error fix, not a generic pitch.
- **r/LocalLLaMA**: audience cares about alternative backends and local proxies; frame it as "transparent adapter pattern" rather than a Claude post. Skip if r/ClaudeAI reception was hostile.

**Title:** `Claude Code + Kimi backend: attachments kept failing with 400 errors, so I wrote a local adapter that fixes them`

**Body:**

> If you point the Claude Code VS Code extension at Kimi's Anthropic-compatible endpoint, chat works but any code/text attachment dies with `API Error: 400 Invalid request`. Cause: the extension sends attachments as Anthropic `document` content blocks, which Kimi's gateway doesn't support.
>
> Kimi Adapter is a local proxy (127.0.0.1:18231) that passes everything through untouched except rewriting `document` → `text` blocks. Your API key passes through in the headers — the adapter never reads or stores it.
>
> - Optional PDF text extraction (`pip install -e ".[pdf]"`)
> - Buffered retry so a dropped upstream stream doesn't surface as truncated JSON
> - Single-file script, pip package, or Docker; VS Code task starts/stops it automatically
>
> Repo: https://github.com/shkyyy18/kimi-adapter — includes a runnable before/after conversion demo. Limitations: text/PDF attachments only, no image blocks.

### 3.3 openbid-intel → r/procurement (primary), r/selfhosted (secondary)

- **r/procurement**: domain audience that actually feels the pain (fragmented portals, noisy keyword alerts). Keep the tone practitioner-to-practitioner and lead with the explainable scoring + "bring your own CSV export" story; do NOT oversell it as a bidding platform — the README's own disclaimer is a selling point here.
- **r/selfhosted**: local-first, SQLite, zero-dep, offline HTML dashboard — clean fit. Wait 2–3 days after the r/procurement post.

**Title:** `Open-source, local-first tender triage: rank bid opportunities against your own profile, with explainable scores`

**Body:**

> Public procurement data is scattered across portals, spreadsheets, and email alerts, and keyword alerts are noisy. I built OpenBid Intel to triage it locally:
>
> - Import CSV/JSON/JSONL exports (common English and Chinese column names recognized, custom mappings supported)
> - Dedup + rank against an editable industry profile — nine built-in packs (IT, medical, construction, energy, education, logistics, ...)
> - Every score is explainable: itemized contributions (business line, buyer, stage, budget, recency, deadline) that sum exactly to the 0–100 result, plus recommended next actions
> - One self-contained HTML dashboard generated from the local SQLite DB — search, filters, works offline, no server
> - Local-first: nothing leaves your machine unless you explicitly send a digest; zero runtime dependencies
>
> It's a triage tool, not a bidding database — deadlines and qualifications still get verified on the official notice page. Live demo (synthetic data): https://shkyyy18.github.io/openbid-intel/
>
> Repo: https://github.com/shkyyy18/openbid-intel

---

## 4. Awesome-list submission plan (all targets verified to exist via `gh api`, 2026-07-20)

| Target list | Verified status | Fit | Submission method |
|---|---|---|---|
| `hesreallyhim/awesome-claude-code` | exists, 50k★, pushed 2026-07-20, not archived | kimi-adapter | **Issue form only — PRs not accepted.** Must be submitted through the web UI "recommend-resource" template (explicitly not possible via `gh` CLI). One-line description, no emoji, no sales pitch. |
| `awesome-selfhosted/awesome-selfhosted` | exists, 306k★, pushed 2026-07-19, not archived | openbid-intel | PR against `README.md`, entry format below. |
| `e2b-dev/awesome-ai-agents` | exists, 28k★, pushed 2026-07-09, not archived | cc-autopilot | PR; the list uses `### Name` + Category/Description/Links sections (not single-line entries). |
| ~~`punkpeye/awesome-mcp-servers`~~ | exists and active, but **rejected**: kimi-adapter is a proxy, not an MCP server | — | do not submit |
| ~~`makegov/awesome-procurement-data`~~ | exists (78★) but **inactive since 2023-11** | — | do not submit |

### 4.1 kimi-adapter → hesreallyhim/awesome-claude-code (issue form, not a PR)

Fill the "Recommend a resource" issue form at:
`https://github.com/hesreallyhim/awesome-claude-code/issues/new?template=recommend-resource.yml`

Suggested one-line description (their style rules: description not pitch, one line, no emoji):

> Local proxy that lets the Claude Code VS Code extension run on a Kimi backend by rewriting Anthropic `document` attachment blocks into text blocks, with buffered retry and pass-through auth.

Note in the kit: recommendations are best-effort with no review guarantee; this is one bullet, fire once, move on.

### 4.2 openbid-intel → awesome-selfhosted/awesome-selfhosted (PR)

Entry line (matches the list's format — name, one-line description, source link, license, language). Suggested section: **Miscellaneous** (verify against current section list when opening the PR; "Money, Budgeting & Management" is the fallback):

```markdown
- [OpenBid Intel](https://github.com/shkyyy18/openbid-intel) - Local-first tender/bid intelligence toolkit that normalizes procurement exports, ranks opportunities against editable industry profiles with explainable scores, and generates a self-contained HTML dashboard. ([Demo](https://shkyyy18.github.io/openbid-intel/), [Source Code](https://github.com/shkyyy18/openbid-intel)) `MIT` `Python`
```

**PR title:** `Add OpenBid Intel to Miscellaneous`

**PR body:**

> Adds [OpenBid Intel](https://github.com/shkyyy18/openbid-intel), a local-first, zero-dependency Python toolkit for triaging public tender notices: imports CSV/JSON/JSONL exports, deduplicates, ranks against editable industry profiles with fully explainable 0-100 scores, and generates an offline, self-contained HTML dashboard from a local SQLite database.
>
> - [x] Entry is in alphabetical order within its section
> - [x] Description is one line, ends with a period, and follows the list format
> - [x] License and language tags match the repo (`MIT`, `Python`)
> - [x] Software is actively maintained and self-hostable (no hosted service required; CLI + local dashboard only)
> - [x] I have read the contributing guidelines

### 4.3 cc-autopilot → e2b-dev/awesome-ai-agents (PR)

Entry block (matches that list's `### Name` + Category/Description/Links structure):

```markdown
### [AgentCron](https://github.com/shkyyy18/cc-autopilot)

### Category
Agent tooling / scheduling

### Description
Cron + watchdog for unattended AI coding agents. Runs Codex, Gemini CLI, or any command on schedule; detects exit-0-but-empty silent failures, enforces timeouts with process-tree cleanup, retries safely, and exposes one health view with JSON output. Zero runtime dependencies, local-only, Windows-first and cross-platform.

### Links
- [GitHub](https://github.com/shkyyy18/cc-autopilot)
```

**PR title:** `Add AgentCron — cron + watchdog for unattended AI coding agents`

**PR body:**

> AgentCron sits between a scheduler (cron / Windows Task Scheduler) and an AI coding agent (Codex, Gemini CLI, or any command) and catches the failures schedulers can't see: exit-0-but-empty responses, hung process trees, and environment drift. Stdlib-only Python 3.9+, local-only, structured logs and JSON health output. MIT licensed, actively maintained.

---

## 5. Posting cadence (suggested, starting 2026-07-21)

Intervals: 2–3 days between platforms for the same project; the three projects are interleaved so no two posts land on the same day. One bullet per project — if a post fails, it is not reposted.

| Date (±1d) | Action |
|---|---|
| Tue 2026-07-21 | Show HN: cc-autopilot |
| Thu 2026-07-23 | Show HN: kimi-adapter |
| Sat 2026-07-25 | Reddit r/procurement: openbid-intel |
| Mon 2026-07-27 | Reddit r/ChatGPTCoding: cc-autopilot |
| Wed 2026-07-29 | Reddit r/ClaudeAI: kimi-adapter |
| Fri 2026-07-31 | awesome-claude-code issue-form recommendation (kimi-adapter) |
| Sun 2026-08-02 | Reddit r/selfhosted: openbid-intel |
| Tue 2026-08-04 | awesome-selfhosted PR (openbid-intel) |
| Thu 2026-08-06 | e2b-dev/awesome-ai-agents PR (cc-autopilot) |
| Sat 2026-08-08 | Optional, only if r/ChatGPTCoding went well: r/selfhosted for cc-autopilot |

Execution notes:
- HN: post the link, then add the first comment immediately; stay around to reply for the first few hours.
- Reddit: check each subreddit's self-promotion rules the day of posting; some require flair or limit link posts.
- Awesome lists: these are slow-burn (maintainer review latency is days to weeks) — that's fine, they're the durable channel.
