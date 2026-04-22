---
task: parseEnrichmentRequest()
responsavel: Nirva
responsavel_type: Agente
atomic_layer: Atom
Entrada:
- campo: topic
  tipo: string
  origen: user prompt via *enrich-context command
  obrigatorio: true
- campo: scope
  tipo: string
  origen: user prompt (optional scope hints)
  obrigatorio: false
- campo: runtimeCapabilities
  tipo: object
  origen: .aiox/runtime-capabilities.json
  obrigatorio: true
Saida:
- campo: parsedRequest
  tipo: file
  destino: .nce/request.md (consumed by dispatchResearchTeam())
  persistido: true
- campo: prerequisitesCheck
  tipo: object
  destino: dispatchResearchTeam() gate condition
  persistido: false
Checklist:
  pre-conditions:
  - '[ ] topic is non-empty and ≤ 200 characters'
  - '[ ] Claude Code Agent Teams support is available (parallel subagents possible)'
  - '[ ] .claude/context-enrichment/ directory exists or can be created'
  - '[ ] No existing .nce/lock file (no concurrent run)'
  post-conditions:
  - '[ ] .nce/request.md written with parsed topic, scope, and metadata'
  - '[ ] prerequisitesCheck.passed is true'
  - '[ ] .nce/lock acquired with current run ID'
  acceptance-criteria:
  - blocker: true
    criteria: Topic is well-formed and prerequisites are met
  - blocker: false
    criteria: Scope hints (if provided) are syntactically valid
Performance:
  duration_expected: <5 seconds
  cost_estimated: ~200 tokens
  cacheable: false
  parallelizable: false
  skippable_when: Never — gate for the entire pipeline
Error Handling:
  strategy: abort
  fallback: Surface actionable error to user (e.g., 'Agent Teams not available')
  notification: user
description: '```'
---


## Pipeline Diagram

```
[user prompt] ──topic+scope──> [parseEnrichmentRequest()] ──parsedRequest──> .nce/request.md
                                         │
                                         ├──prerequisitesCheck──> [dispatchResearchTeam()]
                                         │
                                         └──.nce/lock acquired
```

## Responsibility

First step of the NCE pipeline. Nirva parses the user's request, validates prerequisites (Agent Teams available, no concurrent run, target directory accessible), and writes a canonical `request.md` artifact for downstream consumers. This task is the gate — if it fails, no dispatch occurs.

## Execution Steps

1. Read topic and optional scope from command arguments
2. Validate topic length and non-empty
3. Check `.aiox/runtime-capabilities.json` for Agent Teams support
4. Check for `.nce/lock` — abort if present (concurrent run)
5. Create `.claude/context-enrichment/` if missing
6. Write `.nce/request.md` with parsed fields + metadata (run_id, timestamp)
7. Acquire `.nce/lock` with current run_id
8. Return `prerequisitesCheck.passed = true` to Nirva's controller
