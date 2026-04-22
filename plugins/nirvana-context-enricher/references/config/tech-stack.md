# Tech Stack — Nirvana Context Enricher

Technologies the NCE squad depends on or interacts with. Only items that exist in the host project (`copywriting-ecosystem` / Synkra AIOX v4.0) and are actually used by agents or tasks are listed.

## Runtime Foundations

| Component | Version | Role |
|-----------|---------|------|
| Node.js | ≥ 18 | Runtime for chain validator scripts (`scripts/coverage-validator.cjs`) |
| npm | ≥ 9 | Package manager (matches root `engines` requirement) |
| Synkra AIOX Core | ≥ 2.1.0 | Agent Teams support, squad loader, workflow executor |
| Claude Code | 2.x | Host CLI with parallel subagent dispatch (Agent Teams) |

## Research Tooling (Consumed by Agents)

Agents consume native Claude Code tools and, when available, MCP-backed augmentations. No MCP is required — researchers degrade gracefully to native tools.

| Tool | Used By | Purpose |
|------|---------|---------|
| WebSearch (native) | sage, scout, scholar | Round/axis/phase search queries |
| WebFetch (native) | sage, scout, scholar | Content extraction from primary sources |
| Read / Glob / Grep (native) | all agents | Workspace file operations |
| Write / Edit (native) | all agents | Findings and report file production |

## Optional MCP Augmentation

The squad operates without any MCP, but these MCPs (if installed via `@devops`) enrich specific axes:

| MCP | Enriches | Fallback |
|-----|----------|----------|
| EXA (via docker-gateway) | sage foundational search quality | Native WebSearch |
| Context7 (via docker-gateway) | scout library documentation depth | Native WebFetch |
| Apify (via docker-gateway) | scout GitHub trending scrapers | Native WebSearch of GitHub |

@devops manages all MCP lifecycle per `.claude/rules/mcp-usage.md`. Agents are consumers, never administrators.

## Storage & State

| Location | Purpose |
|----------|---------|
| `.nce/request.md` | Parsed request (Nirva) |
| `.nce/findings/{sage,scout,scholar}.md` | Parallel researcher findings |
| `.nce/report.md` | Lotus synthesis output |
| `.nce/dispatch-log.jsonl` | Dispatch audit trail |
| `.nce/quorum-log.jsonl` | Quorum gate decisions |
| `.nce/chain-log.jsonl` | Chain micro-task execution log |
| `.nce/history.jsonl` | Pipeline run history (append-only) |
| `.nce/archive/{timestamp}/` | Archived findings per run |
| `.nce/lock` | Concurrency guard |
| `.claude/context-enrichment/{slug}.md` | User-facing final report |

All state is filesystem-based — no external DB. Aligns with CLI-First Constitution principle (Art. I).

## Intentionally Not Used

| Technology | Why Not |
|-----------|---------|
| Database (Supabase, Postgres) | All state is append-only filesystem; no relational needs |
| HTTP server | Squad is CLI-only — no runtime daemon |
| External queues (Redis, etc.) | Join barrier is file-presence-based, no queue needed |
| ORMs | No DB |
| Frontend frameworks | Observability only — never controls or dispatches (Constitution Art. I) |

## Format Standards

| Format | Usage |
|--------|-------|
| Markdown | Agents, tasks, findings, reports, config |
| YAML | squad.yaml, workflow, chain, frontmatter |
| JSONL | Append-only logs (dispatch, quorum, chain, history) |

## Dependency Policy

- **Zero new external npm dependencies** at squad install time (`squad.yaml > dependencies.node` is empty)
- Scripts use only Node.js stdlib (`fs`, `path`, `process`, optionally `js-yaml` if already in host project — it is, at `^4.1.1` in root)
- No transitive squad dependencies (`squads: []`) — NCE is standalone
