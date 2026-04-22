---
task: exploreSkillsEcosystem()
responsavel: Scout
responsavel_type: Agente
atomic_layer: Organism
Entrada:
- campo: scoutBrief
  tipo: object
  origen: dispatchResearchTeam() scout-brief payload
  obrigatorio: true
- campo: findingsTemplate
  tipo: file
  origen: templates/research-findings.template.md
  obrigatorio: true
Saida:
- campo: scoutFindings
  tipo: file
  destino: .nce/findings/scout.md (consumed by synthesizeContextReport() via join
    barrier)
  persistido: true
- campo: coverageStats
  tipo: object
  destino: scout.md YAML frontmatter — consumed by validateCoverageQuorum()
  persistido: true
Checklist:
  pre-conditions:
  - '[ ] scoutBrief contains non-empty topic'
  - '[ ] research-findings.template.md is readable'
  - '[ ] .nce/findings/ directory is writable'
  - '[ ] Web search capability is available'
  post-conditions:
  - '[ ] .nce/findings/scout.md exists and is non-empty'
  - '[ ] File has YAML frontmatter with status, searches, extractions, tools_shortlisted'
  - '[ ] All 3 axis sections present (skills, libraries, awesome-lists)'
  - '[ ] Total searches ≥ 3'
  - '[ ] Total extractions ≥ 3'
  - '[ ] Tools shortlisted ≥ 5'
  - '[ ] Every GitHub library has maintenance verdict (🟢/🟡/🔴)'
  acceptance-criteria:
  - blocker: true
    criteria: All 3 axes explored (skills.sh, GitHub, awesome-lists)
  - blocker: true
    criteria: 'Coverage quorum met: ≥3 searches, ≥3 extractions'
  - blocker: false
    criteria: Shortlist covers multiple tiers (incumbents + challengers + specialists)
Tools:
- tool_name: WebSearch
  version: latest
  used_for: 3 ecosystem axis searches
  shared_with:
  - executeDeepResearch()
  - collectAcademicSources()
  cost: free
  cacheable: true
- tool_name: WebFetch
  version: latest
  used_for: skills.sh listings, GitHub READMEs, awesome-lists
  shared_with:
  - executeDeepResearch()
  - collectAcademicSources()
  cost: free
  cacheable: true
Performance:
  duration_expected: 3-5 minutes
  cost_estimated: ~5k tokens + 3-6 web searches + 3-5 extractions
  cacheable: true
  parallelizable: true
  skippable_when: Never — ecosystem map is the breadth axis
Error Handling:
  strategy: retry
  retry:
    max_attempts: 2
    delay: 'per-axis: broaden query and retry once'
  fallback: Mark missing axis as 'no findings' and continue; status=failed if total
    extractions < 3
  notification: nirva
description: '```'
---


## Pipeline Diagram

```
scoutBrief ──topic+scope──> [exploreSkillsEcosystem()] ──scoutFindings────> .nce/findings/scout.md
                                    │                         │
                                    │ 3 axes:                 │
                                    │  1. skills.sh           │ (status=complete, searches≥3,
                                    │  2. GitHub libs         │  extractions≥3, tools≥5)
                                    │  3. awesome-lists       │
                                    │                         └──coverageStats──> [validateCoverageQuorum()]
                                    ▼
                          WebSearch + WebFetch
```

## Responsibility

Scout's core task. Maps the ecosystem around the topic across 3 axes. This is the breadth axis of the 3-researcher fan-out, complementing Sage's depth.

## Execution Steps

Per axis (repeat 3 times):
1. Formulate axis-specific search queries
2. Execute ≥1 web search
3. Extract content from top result(s)
4. For GitHub libraries: assign maintenance verdict based on commit recency + open issue triage
5. Write axis section to findings

After all 3 axes:
6. Build consolidated shortlist covering incumbents + challengers + specialists
7. Write YAML frontmatter with counters
8. Set `status: complete` if coverage quorum met, else `status: failed`

## Maintenance Verdict Rules

| Signal | Verdict |
|--------|---------|
| Commits within 90d + active issue triage | 🟢 Active |
| Commits sparse (<12mo) + bug fixes only | 🟡 Maintenance mode |
| No commits >12mo + backlog growing | 🔴 Stagnant |
