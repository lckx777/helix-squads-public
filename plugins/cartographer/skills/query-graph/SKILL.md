---
task: queryGraph()
responsavel: Cart Oracle
responsavel_type: Agente
atomic_layer: Molecule
workflow: cartographer-query
step: 1
Entrada:
- campo: query
  tipo: string
  obrigatorio: true
  validacao: Non-empty artifact query string
- campo: query_type
  tipo: enum
  valores:
  - find_artifact
  - trace_dependencies
  - list_by_kind
  - detect_conflicts
  - ecosystem_report
  obrigatorio: true
- campo: artifact_kind
  tipo: enum
  valores:
  - function
  - agent
  - task
  - squad
  - hook
  - skill
  - table
  - workflow
  - chain
  - mcp_server
  - any
  obrigatorio: false
- campo: depth_limit
  tipo: integer
  obrigatorio: false
  validacao: 1-10, default 5
Saida:
- campo: query_result
  tipo: structured
  destino: response to caller (inline)
  obrigatorio: true
- campo: query_log
  tipo: file
  destino: squads/cartographer/.run/query-log.ndjson
  obrigatorio: true
Checklist:
- '[ ] Graph snapshot age declared in response header'
- '[ ] Exact match search performed first'
- '[ ] Semantic/keyword search performed if exact match fails'
- '[ ] Results include artifact_path, kind, package/squad, similarity_score'
- '[ ] query logged to query-log.ndjson'
- '[ ] Response is structured (not free-form prose)'
description: '- **ID:** query-graph'
---


# Task: Query Graph

## Metadata
- **ID:** query-graph
- **Workflow:** cartographer-query
- **Step:** 1
- **Agent:** cart-oracle
- **Elicit:** false
- **Read-only:** true

## Description
Answers artifact existence queries against the Cartographer catalog. Returns structured results
with artifact paths, similarity scores, and IDS recommendations.

## Pre-conditions
- `squads/cartographer/.run/catalog/` exists with at least one artifact
- `squads/cartographer/.run/graph-snapshot-*.yaml` exists for staleness check

## Query Types and Execution

### `find_artifact`
1. Exact name match in `.run/catalog/artifacts/{kind}/{id}.json` files
2. If no exact match: keyword search across name and description fields
3. Return: `{exact_matches: [], keyword_matches: [], graph_age: "Xh Ym"}`

### `trace_dependencies`
1. Load artifact by ID from catalog
2. Traverse dependency edges up to `depth_limit` hops
3. Distinguish: direct (depth=1) vs transitive (depth>1)
4. Flag circular paths
5. Return: `{artifact: {...}, direct_deps: [], transitive_deps: [], circular: []}`

### `list_by_kind`
1. List all artifacts of requested kind from `.run/catalog/artifacts/{kind}/`
2. Return: sorted list with name, file_path, package

### `detect_conflicts`
1. Search for artifacts with similar names across different packages
2. Flag: same function name exported from 2+ packages
3. Return: `{conflicts: [{name, locations: [...]}, ...]}`

### `ecosystem_report`
1. Load `.run/graph-snapshot-*.yaml` (most recent)
2. Load `.run/drift-log.ndjson` (recent events)
3. Return: health report with artifact counts by kind, drift summary, coverage metrics

## Response Format
```yaml
graph_snapshot: "2026-04-16T10:00:00Z"
graph_age: "2h 15m"
staleness_warning: false  # true if > 24h
query_type: find_artifact
query: "function that validates gate state"
exact_matches: []
keyword_matches:
  - id: "ts:workflow-gate-engine:canProceed"
    kind: function
    name: canProceed
    file_path: "packages/workflow-gate-engine/src/gate.ts"
    package: workflow-gate-engine
    signature: "(workflow: string, step: number) => Promise<boolean>"
    similarity_score: 0.89
ids_recommendation: REUSE
ids_recommendation_reason: "High confidence match — canProceed already implements gate validation"
```
