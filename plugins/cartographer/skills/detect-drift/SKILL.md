---
task: detectDrift()
responsavel: Cart Keeper
responsavel_type: Agente
atomic_layer: Molecule
workflow: cartographer-maintenance
step: 1
Entrada:
- campo: current_snapshot
  tipo: file
  obrigatorio: true
  validacao: squads/cartographer/.run/graph-snapshot-{timestamp}.yaml
- campo: previous_snapshot
  tipo: file
  obrigatorio: true
  validacao: squads/cartographer/.run/graph-snapshot-{prev_timestamp}.yaml
Saida:
- campo: drift_report
  tipo: file
  destino: squads/cartographer/.run/drift-reports/drift-{timestamp}.yaml
  obrigatorio: true
- campo: drift_log
  tipo: file
  destino: squads/cartographer/.run/drift-log.ndjson
  obrigatorio: true
Checklist:
- '[ ] Both snapshots loaded successfully'
- '[ ] ADDED artifacts identified (in current, not in previous)'
- '[ ] REMOVED artifacts identified (in previous, not in current)'
- '[ ] MODIFIED artifacts identified (same ID, different hash)'
- '[ ] RENAMED artifacts identified (path changed, content hash same)'
- '[ ] Drift events appended to drift-log.ndjson'
- '[ ] Drift report written with summary statistics'
description: '- **ID:** detect-drift'
---


# Task: Detect Drift

## Metadata
- **ID:** detect-drift
- **Agent:** cart-keeper
- **When:** After every graph build, or on explicit `*cart-drift` command

## Description
Compares two graph snapshots to identify what changed between excavation runs.
Drift detection is mandatory — every build generates a drift report, even if empty.

## Drift Event Types
- **ADDED**: New artifact in current, not in previous
- **REMOVED**: Artifact in previous, not in current (potential breaking change)
- **MODIFIED**: Same artifact ID, different content hash (signature or implementation changed)
- **RENAMED**: Content hash unchanged, but file_path changed (refactor)

## Security Signals
- `rls_enabled: false` tables that were previously `rls_enabled: true` → SECURITY_REGRESSION drift event
- Hooks removed that were in PreToolUse lifecycle → ENFORCEMENT_DEGRADED drift event
