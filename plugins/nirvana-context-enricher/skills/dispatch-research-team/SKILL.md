---
task: dispatchResearchTeam()
responsavel: Nirva
responsavel_type: Agente
atomic_layer: Molecule
Entrada:
- campo: parsedRequest
  tipo: file
  origen: .nce/request.md (output of parseEnrichmentRequest())
  obrigatorio: true
- campo: prerequisitesCheck
  tipo: object
  origen: parseEnrichmentRequest() output — must have passed=true
  obrigatorio: true
Saida:
- campo: sageHandle
  tipo: object
  destino: parallel subagent handle for Sage — consumed by validateCoverageQuorum()
    join barrier
  persistido: false
- campo: scoutHandle
  tipo: object
  destino: parallel subagent handle for Scout — consumed by validateCoverageQuorum()
    join barrier
  persistido: false
- campo: scholarHandle
  tipo: object
  destino: parallel subagent handle for Scholar — consumed by validateCoverageQuorum()
    join barrier
  persistido: false
- campo: dispatchLog
  tipo: file
  destino: .nce/dispatch-log.jsonl
  persistido: true
Checklist:
  pre-conditions:
  - '[ ] parseEnrichmentRequest() completed with prerequisitesCheck.passed=true'
  - '[ ] .nce/request.md exists and is parseable'
  - '[ ] .nce/findings/ directory exists (create if missing)'
  - '[ ] Claude Code supports 3 parallel subagents (Agent Teams)'
  post-conditions:
  - '[ ] 3 subagent handles returned (sage, scout, scholar) — all non-null'
  - '[ ] Each dispatched agent received its scoped brief'
  - '[ ] .nce/dispatch-log.jsonl has entries for all 3 dispatches'
  acceptance-criteria:
  - blocker: true
    criteria: All 3 researchers dispatched in parallel (not sequentially)
  - blocker: true
    criteria: No shared state between dispatched briefs
  - blocker: false
    criteria: Dispatch latency < 2 seconds
Performance:
  duration_expected: <2 seconds for dispatch; researchers run in parallel afterward
  cost_estimated: ~500 tokens per brief × 3 briefs
  cacheable: false
  parallelizable: true
  skippable_when: Never — fan-out is the entire point of the pipeline
Error Handling:
  strategy: retry
  retry:
    max_attempts: 2
    delay: linear(30s)
  fallback: Abort with diagnostic — Agent Teams feature may be unavailable
  notification: user
description: '```'
---


## Pipeline Diagram

```
.nce/request.md ──parsedRequest──> [dispatchResearchTeam()] ──sageHandle────> [executeDeepResearch()]
                                            │
                                            ├──scoutHandle───> [exploreSkillsEcosystem()]
                                            │
                                            └──scholarHandle──> [collectAcademicSources()]
                                            │
                                            └──dispatchLog───> .nce/dispatch-log.jsonl
```

## Responsibility

Fan-out step of the pipeline. Nirva takes the parsed request and dispatches 3 researchers in true parallel, each receiving a scoped brief tailored to its axis (foundational / ecosystem / academic). The handles returned are consumed later by `validateCoverageQuorum()` as the join barrier.

## Execution Steps

1. Read `.nce/request.md`
2. Derive 3 scoped briefs (one per researcher) — each brief includes topic, scope hints, target findings path, and minimum coverage requirements
3. Dispatch Sage subagent with sage-brief → store sageHandle
4. Dispatch Scout subagent with scout-brief → store scoutHandle
5. Dispatch Scholar subagent with scholar-brief → store scholarHandle
6. Append 3 dispatch entries to `.nce/dispatch-log.jsonl`
7. Return 3 handles to Nirva's controller (does NOT wait for completion)

## Anti-Pattern Prevention

The three dispatches MUST happen in parallel. Sequentializing them (waiting for sage to finish before dispatching scout) defeats the entire purpose of the NCE pipeline and multiplies total runtime by ~3x.
