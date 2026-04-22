---
task: generateReport()
responsavel: Cart Oracle
responsavel_type: Agente
atomic_layer: Molecule
workflow: cartographer-query
step: 3
Entrada:
- campo: report_type
  tipo: enum
  valores:
  - health
  - drift-summary
  - ids-audit
  - full
  obrigatorio: true
- campo: output_format
  tipo: enum
  valores:
  - md
  - yaml
  - json
  obrigatorio: false
  default: md
Saida:
- campo: report
  tipo: file
  destino: squads/cartographer/.run/reports/report-{type}-{timestamp}.{format}
  obrigatorio: true
Checklist:
- '[ ] Graph snapshot age declared'
- '[ ] Artifact counts by kind included'
- '[ ] IDS check history summarized (total checks, REUSE/ADAPT/CREATE breakdown)'
- '[ ] Drift summary included (events since last full reindex)'
- '[ ] Coverage metrics: squads indexed, packages indexed, hooks cataloged'
description: '- Total artifacts by kind (function, agent, task, squad, hook, skill,
  table)'
---


# Task: Generate Report

## Report Types

### health
- Total artifacts by kind (function, agent, task, squad, hook, skill, table)
- Squads indexed: N/M
- Packages with TS artifacts: N
- Hooks by lifecycle event: {PreToolUse: N, PostToolUse: N}
- RLS coverage: N tables, M without RLS
- Graph snapshot age

### drift-summary
- Last N drift events grouped by type (ADDED/REMOVED/MODIFIED/RENAMED)
- Security regression signals highlighted
- Enforcement degradation alerts

### ids-audit
- Total IDS checks since last reindex
- Breakdown: REUSE N, ADAPT N, CREATE N
- Top 5 most-consulted artifacts (REUSE candidates)
- CREATE decisions that might have been avoided (high similarity CREATEs)

### full
- All of the above combined
