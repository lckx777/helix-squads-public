---
task: buildGraph()
responsavel: Cart Keeper
responsavel_type: Agente
atomic_layer: Molecule
workflow: cartographer-excavation
step: 5
Entrada:
- campo: ts_artifacts
  tipo: file
  obrigatorio: false
  validacao: squads/cartographer/.run/digger-output/ts-artifacts.ndjson
- campo: py_artifacts
  tipo: file
  obrigatorio: false
  validacao: squads/cartographer/.run/digger-output/py-artifacts.ndjson
- campo: yaml_artifacts
  tipo: file
  obrigatorio: false
  validacao: squads/cartographer/.run/digger-output/yaml-artifacts.ndjson
- campo: sql_artifacts
  tipo: file
  obrigatorio: false
  validacao: squads/cartographer/.run/digger-output/sql-artifacts.ndjson
- campo: previous_snapshot
  tipo: file
  obrigatorio: false
  validacao: squads/cartographer/.run/graph-snapshot-*.yaml
Saida:
- campo: graph_snapshot
  tipo: file
  destino: squads/cartographer/.run/graph-snapshot-{timestamp}.yaml
  obrigatorio: true
- campo: drift_log
  tipo: file
  destino: squads/cartographer/.run/drift-log.ndjson
  obrigatorio: true
- campo: embedding_queue
  tipo: file
  destino: squads/cartographer/.run/embedding-queue.ndjson
  obrigatorio: true
- campo: graph_build_meta
  tipo: file
  destino: squads/cartographer/.run/graph-builds/build-{run_id}.yaml
  obrigatorio: true
Checklist:
- '[ ] All available digger NDJSON files validated against digger-base-contract.md
  schema'
- '[ ] Artifacts upserted (not replaced) — lineage preserved'
- '[ ] Dependency edges upserted'
- '[ ] Drift events computed and logged to drift-log.ndjson'
- '[ ] Orphaned edges detected and reported'
- '[ ] embedding-queue.ndjson written for pre-MCP embedding batch'
- '[ ] graph-snapshot-{timestamp}.yaml written'
- '[ ] Graph integrity gate passed: no orphaned edges, all squads have agents'
description: '- **ID:** build-graph'
---


# Task: Build Graph

## Metadata
- **ID:** build-graph
- **Workflow:** cartographer-excavation
- **Step:** 5
- **Agent:** cart-keeper
- **Parallel:** false (must run after all diggers)

## Description
Ingests all digger NDJSON outputs, upserts artifact nodes and dependency edges, detects drift,
generates semantic embeddings (or queues them), and enforces graph integrity constraints.

## Pre-conditions
- At least one digger NDJSON file present in `.run/digger-output/`
- Excavation gate PASSED for all diggers that ran

## Execution Steps (Pre-MCP Phase — file-based catalog)

1. **Validate inputs**: For each available NDJSON file, validate each record against artifact schema
2. **Load previous snapshot** (if exists): Build in-memory set of previous artifact IDs
3. **Upsert artifacts**:
   - For each artifact record: write to `.run/catalog/artifacts/{kind}/{id}.json`
   - If artifact existed: update `last_updated`, append `run_id` to `run_ids[]`
   - If artifact new: set `first_seen = now`, `run_ids = [current_run_id]`
4. **Upsert dependency edges**:
   - Write edges to `.run/catalog/edges/{from}->{to}.json`
5. **Drift detection**: Compare current artifact IDs vs previous snapshot:
   - ADDED: new IDs not in previous snapshot
   - REMOVED: IDs in previous snapshot not in current
   - MODIFIED: same ID, different content hash
   - Log each event to `drift-log.ndjson`
6. **Integrity checks**:
   - Orphaned edges (source or target not in current artifacts)
   - Squads without any cataloged agents
   - Warn on circular dependencies
7. **Embedding queue**: Write artifact text representations to `embedding-queue.ndjson`
   (Future: when Supabase MCP is available, generate embeddings inline)
8. **Write snapshot**: `graph-snapshot-{timestamp}.yaml` with totals and drift summary

## Pre-MCP Storage Strategy
Since `packages/cartographer-mcp/` does not exist yet, the graph is stored as files:
```
squads/cartographer/.run/catalog/
├── artifacts/
│   ├── function/{id}.json
│   ├── agent/{id}.json
│   ├── task/{id}.json
│   ├── squad/{id}.json
│   ├── hook/{id}.json
│   ├── skill/{id}.json
│   └── table/{id}.json
├── edges/
│   └── {from}-{to}-{edge_type}.json
└── index.json  ← artifact count summary
```

## Graph Integrity Gate
PASSED when:
- Zero orphaned edges
- Every squad in yaml-artifacts has >= 1 cataloged agent
- drift-log.ndjson written (even if empty)
- embedding-queue.ndjson written

FAILED when:
- Orphaned edges exist (log all, block)
- Schema validation errors in input NDJSON
