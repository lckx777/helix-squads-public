# Pre-Dispatch Readiness Checklist

> **Owner:** Nirva
> **When to run:** Before invoking `dispatchResearchTeam()` (workflow step 2)
> **Purpose:** Verify all preconditions for safe parallel fan-out

## Hard Gates (BLOCKER if any fail)

- [ ] `.nce/request.md` exists and is parseable
- [ ] `parsedRequest.topic` is non-empty and ≤ 200 characters
- [ ] `prerequisitesCheck.passed` from `parseEnrichmentRequest()` is `true`
- [ ] `.nce/lock` is held by current `run_id` (not stale from a previous crash)
- [ ] `.nce/findings/` directory exists and is writable
- [ ] Claude Code Agent Teams is available (parallel subagent dispatch)
- [ ] At least 1 of {EXA, native WebSearch} is available
- [ ] At least 1 of {WebFetch, native fetch} is available

## Soft Gates (WARNING — proceed but log)

- [ ] No prior abort report at `.nce/abort-report.md` (clean previous run)
- [ ] Disk has ≥ 50 MB free under workspace
- [ ] No active concurrent run from another shell (orphan lock check)

## Outcome

- **All hard gates pass** → return `ready=true` to `dispatchResearchTeam()`
- **Any hard gate fails** → return `ready=false` with failing gate name, abort dispatch
- **Soft gate fails** → log warning to `.nce/dispatch-log.jsonl`, continue
