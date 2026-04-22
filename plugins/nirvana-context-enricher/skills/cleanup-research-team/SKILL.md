---
task: cleanupResearchTeam()
responsavel: Nirva
responsavel_type: Agente
atomic_layer: Atom
Entrada:
- campo: pipelineState
  tipo: object
  origen: Nirva controller — run_id, start_time, outcome (success|failed|aborted)
  obrigatorio: true
- campo: deliveredPath
  tipo: string
  origen: deliverEnrichmentReport() output (null on failure/abort)
  obrigatorio: false
Saida:
- campo: cleanupLog
  tipo: file
  destino: .nce/history.jsonl (append-only pipeline history)
  persistido: true
- campo: archiveDir
  tipo: string
  destino: .nce/archive/{timestamp}/ (relocated findings for audit trail)
  persistido: true
Checklist:
  pre-conditions:
  - '[ ] pipelineState.run_id is present'
  - '[ ] pipelineState.outcome is one of {success, failed, aborted}'
  - '[ ] .nce/ directory exists'
  post-conditions:
  - '[ ] .nce/lock removed'
  - '[ ] .nce/findings/ relocated to .nce/archive/{timestamp}/'
  - '[ ] .nce/history.jsonl appended with final entry'
  - '[ ] All subagent handles released (no lingering processes)'
  acceptance-criteria:
  - blocker: true
    criteria: Cleanup runs on every pipeline outcome (success AND failure AND abort)
  - blocker: true
    criteria: .nce/lock is always removed
  - blocker: false
    criteria: Archive uses ISO-8601 timestamp directory name
Performance:
  duration_expected: <1 second
  cost_estimated: negligible (file operations only)
  cacheable: false
  parallelizable: false
  skippable_when: Never — lifecycle close is a contract, even on failure
Error Handling:
  strategy: fallback
  fallback: If archive move fails, log warning and proceed with lock removal — lock
    removal is the critical invariant
  notification: nirva
description: '```'
---


## Pipeline Diagram

```
pipelineState ──run_id+outcome──> [cleanupResearchTeam()] ──cleanupLog──> .nce/history.jsonl
                                          │                      │
deliveredPath ──path or null──>           │                      └──archiveDir──> .nce/archive/{timestamp}/
                                          │
                                          └──remove──> .nce/lock
                                          └──release──> subagent handles
```

## Responsibility

Final lifecycle hook. Always runs — regardless of pipeline success, failure, or abort. Its job is to release resources, archive artifacts for audit, and record the run outcome.

## Execution Steps

1. Remove `.nce/lock` — this is the critical invariant (permits the next run)
2. Generate timestamp directory: `.nce/archive/{ISO-8601}/`
3. Move `.nce/findings/` → `.nce/archive/{timestamp}/findings/`
4. Move `.nce/request.md` → `.nce/archive/{timestamp}/request.md`
5. Move `.nce/dispatch-log.jsonl` → `.nce/archive/{timestamp}/dispatch-log.jsonl`
6. Move `.nce/quorum-log.jsonl` → `.nce/archive/{timestamp}/quorum-log.jsonl`
7. Move `.nce/report.md` → `.nce/archive/{timestamp}/report.md` (if exists)
8. Append single JSON line to `.nce/history.jsonl`:
   ```json
   {"run_id": "...", "topic": "...", "outcome": "success|failed|aborted",
    "started_at": "...", "completed_at": "...", "duration_seconds": N,
    "coverage": {"sage": N, "scout": N, "scholar": N, "extractions": N},
    "delivered_path": "... or null", "archive": ".nce/archive/{timestamp}/"}
   ```
9. Release any lingering subagent handles
10. Return control — pipeline is officially closed

## Critical Invariants

| Invariant | Why it matters |
|-----------|---------------|
| `.nce/lock` is ALWAYS removed | Otherwise next run is permanently blocked |
| `.nce/history.jsonl` is append-only | Never truncate — audit trail |
| Archive directory timestamp is ISO-8601 | Sortability for historical queries |
| Runs even on abort | Abandoned locks would be a liveness bug |
