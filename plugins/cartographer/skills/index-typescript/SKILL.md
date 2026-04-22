---
task: indexTypescript()
responsavel: Cart TS Digger
responsavel_type: Agente
atomic_layer: Molecule
workflow: cartographer-excavation
step: 1
Entrada:
- campo: glob_scope
  tipo: config
  obrigatorio: true
  validacao: packages/**/*.ts, packages/**/*.tsx, hub/**/*.ts, hub/**/*.svelte
- campo: last_hashes
  tipo: file
  obrigatorio: false
  validacao: squads/cartographer/.run/last-hashes.json
- campo: run_mode
  tipo: enum
  valores:
  - incremental
  - full
  obrigatorio: true
Saida:
- campo: ts_artifacts
  tipo: file
  destino: squads/cartographer/.run/digger-output/ts-artifacts.ndjson
  obrigatorio: true
- campo: updated_hashes
  tipo: file
  destino: squads/cartographer/.run/last-hashes.json
  obrigatorio: true
- campo: digger_run_meta
  tipo: file
  destino: squads/cartographer/.run/digger-runs/ts-{run_id}.yaml
  obrigatorio: true
Checklist:
- '[ ] glob_scope defined and all target directories accessible'
- '[ ] last-hashes.json loaded (or created fresh for first run)'
- '[ ] Each .ts/.tsx file hash-checked before parsing'
- '[ ] All exported symbols extracted (functions, classes, types, interfaces, constants,
  enums)'
- '[ ] Cross-package import edges recorded'
- '[ ] Output NDJSON schema valid per digger-base-contract.md'
- '[ ] last-hashes.json updated with new hashes'
- '[ ] digger_run_meta written with: run_id, files_parsed, files_skipped, artifacts_emitted,
  timestamp'
description: '- **ID:** index-typescript'
---


# Task: Index TypeScript

## Metadata
- **ID:** index-typescript
- **Workflow:** cartographer-excavation
- **Step:** 1
- **Agent:** cart-ts-digger
- **Parallel:** false (sequential per package)

## Description
Static excavation of all TypeScript packages in the monorepo. Extracts exported symbols and
inter-package dependency edges. Produces structured NDJSON for cart-keeper graph build.

## Shared Base Pattern (AgentDropout — TS/PY share this contract)
Both ts-digger and py-digger follow the same Entrada/Saída/hash-gate contract.
The difference is language boundary and parser tooling only. See `config/digger-base-contract.md`.

## Pre-conditions
- Target directories exist and are readable
- `squads/cartographer/.run/digger-output/` directory exists
- `squads/cartographer/.run/` directory exists

## Inputs
- File glob: `packages/**/*.ts`, `packages/**/*.tsx`, `hub/**/*.ts`, `hub/**/*.svelte`
- Hash registry: `squads/cartographer/.run/last-hashes.json`
- Run mode: `incremental` (hash-gated) or `full` (all files)

## Execution Steps

1. Load `.run/last-hashes.json` (empty object `{}` if first run)
2. For each file matching glob:
   a. Compute SHA256 of file contents
   b. If mode=incremental AND hash unchanged: skip (log as skipped)
   c. Parse file — extract exported symbols:
      - Functions: name, signature (parameters + return type), exported_from (package)
      - Classes: name, methods[], properties[], extends[], implements[]
      - Types/Interfaces: name, shape (simplified), exported_from
      - Constants/Enums: name, type, exported_from
   d. Record cross-package imports: `import { X } from '@/packagename'` → dependency edge
   e. Emit NDJSON record (see schema in `config/digger-base-contract.md`)
   f. Update hash registry entry
3. Flush NDJSON to `.run/digger-output/ts-artifacts.ndjson`
4. Write updated `.run/last-hashes.json`
5. Write run metadata to `.run/digger-runs/ts-{run_id}.yaml`

## Artifact Record Schema (key fields)
```json
{
  "id": "ts:{package}:{name}",
  "kind": "function|class|type|interface|constant|enum",
  "name": "functionName",
  "file_path": "packages/pipeline-engine/src/dag.ts",
  "package": "pipeline-engine",
  "line_start": 42,
  "line_end": 67,
  "signature": "(config: DagConfig) => Promise<DagResult>",
  "exported": true,
  "dependencies": [{"from": "pipeline-engine", "symbol": "PipelineState", "to": "context-registry"}],
  "hash": "sha256:...",
  "digger": "cart-ts-digger",
  "run_id": "ts-20260416-001",
  "timestamp": "2026-04-16T00:00:00Z"
}
```

## Outputs
- `squads/cartographer/.run/digger-output/ts-artifacts.ndjson` — one artifact per line
- `squads/cartographer/.run/last-hashes.json` — updated hash registry
- `squads/cartographer/.run/digger-runs/ts-{run_id}.yaml` — run metadata

## Gate
- NDJSON file exists and is valid (each line parseable as JSON)
- Run metadata written with files_parsed count
- Hash registry updated
