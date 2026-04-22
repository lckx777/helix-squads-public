---
task: validateCoverageQuorum()
responsavel: Nirva
responsavel_type: Agente
atomic_layer: Analysis
Entrada:
- campo: sageFindings
  tipo: file
  origen: .nce/findings/sage.md (executeDeepResearch() output)
  obrigatorio: true
- campo: scoutFindings
  tipo: file
  origen: .nce/findings/scout.md (exploreSkillsEcosystem() output)
  obrigatorio: true
- campo: scholarFindings
  tipo: file
  origen: .nce/findings/scholar.md (collectAcademicSources() output)
  obrigatorio: true
Saida:
- campo: quorumVerdict
  tipo: object
  destino: Nirva controller — gates handoff to synthesizeContextReport()
  persistido: false
- campo: retryInstructions
  tipo: object
  destino: Nirva controller — populated only when quorum fails; identifies failing
    researcher(s)
  persistido: false
- campo: quorumLog
  tipo: file
  destino: .nce/quorum-log.jsonl
  persistido: true
Checklist:
  pre-conditions:
  - '[ ] All 3 findings files exist on disk'
  - '[ ] Each findings file has parseable YAML frontmatter'
  - '[ ] Each findings file has status field (complete | in_progress | failed)'
  post-conditions:
  - '[ ] quorumVerdict.passed is a boolean (never null)'
  - '[ ] quorumLog appended with current run metrics'
  - '[ ] If failed, retryInstructions names the failing researcher(s) and reason'
  acceptance-criteria:
  - blocker: true
    criteria: Decision is deterministic — same inputs always yield same verdict
  - blocker: true
    criteria: Never passes quorum if any researcher has status=failed
  - blocker: false
    criteria: Verdict rendered in < 1 second
Scripts:
- script_path: scripts/coverage-validator.cjs
  description: Parses findings frontmatter, computes aggregate metrics, renders verdict
  language: javascript
  version: 1.0.0
Performance:
  duration_expected: <1 second
  cost_estimated: negligible (pure file parsing + arithmetic)
  cacheable: false
  parallelizable: false
  skippable_when: Never — this IS the join barrier
description: '```'
---


## Pipeline Diagram

```
.nce/findings/sage.md    ┐
                         │
.nce/findings/scout.md   ├──[validateCoverageQuorum()]──┬─quorumVerdict.passed=true──> [synthesizeContextReport()]
                         │                              │
.nce/findings/scholar.md ┘                              ├─quorumVerdict.passed=false──> [dispatchResearchTeam() retry]
                                                        │
                                                        └─quorumLog──> .nce/quorum-log.jsonl
```

## Responsibility

The join barrier of the pipeline. Parses the 3 findings files, computes aggregate coverage metrics, and renders a pass/fail verdict. Nirva uses this verdict to decide: proceed to Lotus or retry failing researchers.

## Quorum Formula

A quorum passes if and only if ALL of the following are true:

```
sage.status == "complete"
scout.status == "complete"
scholar.status == "complete"

sage.searches >= 6
scout.searches >= 3
scholar.searches >= 2

total_searches = sage.searches + scout.searches + scholar.searches
total_searches >= 24                  # NOTE: encourages over-delivery beyond minimums

total_extractions = sage.extractions + scout.extractions + scholar.extractions
total_extractions >= 11
```

Any violation → `quorumVerdict.passed = false`, with `retryInstructions` naming the failing researcher.

## Execution Steps

1. Read YAML frontmatter from each findings file
2. Validate all 3 have `status: complete`
3. Compute per-researcher minimums
4. Compute aggregate minimums (≥24 searches, ≥11 extractions)
5. Render verdict object
6. If failed, determine which researcher(s) need re-dispatch
7. Append entry to `.nce/quorum-log.jsonl`
8. Return verdict to Nirva controller

## Retry Logic (handled by Nirva, informed by retryInstructions)

- Identify failing researcher(s) from retryInstructions
- Re-dispatch each with directive "increase coverage — previous run fell short"
- Max 1 retry per researcher
- If retry also fails → abort pipeline with diagnostic, Lotus is NEVER invoked
