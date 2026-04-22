---
task: executeDeepResearch()
responsavel: Sage
responsavel_type: Agente
atomic_layer: Organism
Entrada:
- campo: sageBrief
  tipo: object
  origen: dispatchResearchTeam() sage-brief payload
  obrigatorio: true
- campo: findingsTemplate
  tipo: file
  origen: templates/research-findings.template.md
  obrigatorio: true
Saida:
- campo: sageFindings
  tipo: file
  destino: .nce/findings/sage.md (consumed by synthesizeContextReport() via join barrier)
  persistido: true
- campo: coverageStats
  tipo: object
  destino: sage.md YAML frontmatter — consumed by validateCoverageQuorum()
  persistido: true
Checklist:
  pre-conditions:
  - '[ ] sageBrief contains non-empty topic'
  - '[ ] research-findings.template.md is readable'
  - '[ ] .nce/findings/ directory is writable'
  - '[ ] Web search capability is available'
  post-conditions:
  - '[ ] .nce/findings/sage.md exists and is non-empty'
  - '[ ] File has YAML frontmatter with status, searches, extractions, primary_sources'
  - '[ ] All 6 round sections are present'
  - '[ ] Total searches ≥ 6'
  - '[ ] Total content extractions ≥ 6'
  - '[ ] Primary sources ≥ 3'
  - '[ ] Zero rounds are empty'
  acceptance-criteria:
  - blocker: true
    criteria: All 6 rounds executed (fundamentals, architecture, practices, advanced,
      current, pitfalls)
  - blocker: true
    criteria: 'Coverage quorum met: ≥6 searches, ≥6 extractions'
  - blocker: false
    criteria: Primary source ratio ≥ 50%
Tools:
- tool_name: WebSearch
  version: latest
  used_for: 6 rounds of topic investigation
  shared_with:
  - exploreSkillsEcosystem()
  - collectAcademicSources()
  cost: free
  cacheable: true
- tool_name: WebFetch
  version: latest
  used_for: Content extraction from primary sources
  shared_with:
  - exploreSkillsEcosystem()
  - collectAcademicSources()
  cost: free
  cacheable: true
Performance:
  duration_expected: 5-10 minutes
  cost_estimated: ~8k tokens + 6-12 web searches + 6-10 extractions
  cacheable: true
  parallelizable: true
  skippable_when: Never — deep research is the foundational capability
Error Handling:
  strategy: retry
  retry:
    max_attempts: 2
    delay: 'per-round: reformulate query and retry up to 2x'
  fallback: Mark round as 'thin' and continue; set status=failed if total extractions
    < 6
  notification: nirva
description: '```'
---


## Pipeline Diagram

```
sageBrief ──topic+scope──> [executeDeepResearch()] ──────sageFindings─────> .nce/findings/sage.md
                                   │                          │
                                   │ 6 rounds:                │
                                   │  1. fundamentals         │ (status=complete, searches≥6,
                                   │  2. architecture         │  extractions≥6)
                                   │  3. practices            │
                                   │  4. advanced             └──coverageStats──> [validateCoverageQuorum()]
                                   │  5. current
                                   │  6. pitfalls
                                   ▼
                          WebSearch + WebFetch
```

## Responsibility

Sage's core task. Executes the full 6-round foundational investigation and writes findings to `.nce/findings/sage.md`. This is the deep axis of the 3-researcher fan-out.

## Execution Steps

Per round (repeat 6 times):
1. Formulate search queries for the round's goal
2. Execute ≥1 web search
3. Evaluate results; pick primary source(s)
4. Extract content via WebFetch
5. Write round section to findings with: summary, bullets, extracted passages, citations
6. Update running counters (searches, extractions, primary_sources)

After all 6 rounds:
7. Write YAML frontmatter to top of `.nce/findings/sage.md`
8. Set `status: complete` if coverage quorum met, else `status: failed`
9. Return control to Nirva
