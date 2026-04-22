# Graph Integrity Gate Checklist

**Gate:** graph-integrity
**Enforcer:** cart-keeper
**Pre-requisite:** excavation PASSED
**Required before:** oracle can serve queries

## Checklist

- [ ] Zero orphaned dependency edges (source or target artifact must exist in catalog)
- [ ] Every squad in yaml-artifacts has at least 1 cataloged agent artifact
- [ ] `drift-log.ndjson` written (may be empty for first run, must exist)
- [ ] `graph-snapshot-{timestamp}.yaml` written with valid artifact counts
- [ ] `embedding-queue.ndjson` written (pre-MCP: all artifacts queued for embedding)
- [ ] No duplicate artifact IDs across digger outputs (cross-digger ID collision check)
- [ ] Circular hard-dependencies flagged in snapshot (not blocking, but must be declared)
- [ ] Catalog index (`catalog/index.json`) reflects current artifact counts

## Security Checks (WARN — not blocking)

- [ ] Tables without RLS listed in snapshot security section
- [ ] PreToolUse hooks cataloged (enforcement coverage declared)
- [ ] No hooks removed vs previous run without drift event logged

## Scoring

| Check | Severity |
|-------|----------|
| Zero orphaned edges | REQUIRED |
| All squads have agents | REQUIRED |
| drift-log.ndjson written | REQUIRED |
| graph-snapshot written | REQUIRED |
| embedding-queue written | MUST |
| No cross-digger ID collisions | REQUIRED |

**PASS:** All REQUIRED checks pass + MUST checks pass
**FAIL:** Any REQUIRED check fails
