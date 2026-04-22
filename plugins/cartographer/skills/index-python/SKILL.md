---
task: indexPython()
responsavel: Cart PY Digger
responsavel_type: Agente
atomic_layer: Molecule
workflow: cartographer-excavation
step: 2
Entrada:
- campo: glob_scope
  tipo: config
  obrigatorio: true
  validacao: .claude/hooks/**/*.py, scripts/**/*.py, mega-brain/**/*.py
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
- campo: py_artifacts
  tipo: file
  destino: squads/cartographer/.run/digger-output/py-artifacts.ndjson
  obrigatorio: true
- campo: updated_hashes
  tipo: file
  destino: squads/cartographer/.run/last-hashes.json
  obrigatorio: true
- campo: digger_run_meta
  tipo: file
  destino: squads/cartographer/.run/digger-runs/py-{run_id}.yaml
  obrigatorio: true
Checklist:
- '[ ] glob_scope defined and all target directories accessible'
- '[ ] Hook files identified and tagged kind: hook'
- '[ ] Each hook''s lifecycle_event extracted (PreToolUse/PostToolUse/etc)'
- '[ ] SKILL.md files found under .claude/skills/ and tagged kind: skill'
- '[ ] Skill keyword triggers extracted'
- '[ ] Output NDJSON schema valid per digger-base-contract.md'
- '[ ] last-hashes.json updated'
- '[ ] digger_run_meta written'
description: '- **ID:** index-python'
---


# Task: Index Python

## Metadata
- **ID:** index-python
- **Workflow:** cartographer-excavation
- **Step:** 2
- **Agent:** cart-py-digger
- **Parallel:** can run in parallel with index-typescript (no shared state)

## Description
Static excavation of all Python hooks, scripts, and mega-brain modules.
Special handling for hook lifecycle registrations and SKILL.md keyword triggers.
Follows same hash-gate + NDJSON contract as index-typescript (AgentDropout shared base).

## Pre-conditions
- `.claude/hooks/` directory accessible
- `scripts/` directory accessible
- `mega-brain/` directory accessible

## Inputs
- File glob: `.claude/hooks/**/*.py`, `scripts/**/*.py`, `mega-brain/**/*.py`
- Additional: `.claude/skills/**/*.md` (SKILL.md files)
- Hash registry: `squads/cartographer/.run/last-hashes.json`

## Execution Steps

1. Load `.run/last-hashes.json`
2. For each Python file matching glob:
   a. Hash-check (skip if unchanged in incremental mode)
   b. Parse AST — extract functions, classes, module-level definitions
   c. For files in `.claude/hooks/`:
      - Extract lifecycle_event from function names, decorators, or settings cross-reference
      - Extract timeout if declared
      - Set `kind: hook` in artifact record
   d. Emit standard NDJSON record with function signatures + import edges
3. For each SKILL.md under `.claude/skills/`:
   a. Extract frontmatter: name, Auto-Trigger, Keywords, Prioridade, Tools
   b. Emit `kind: skill` artifact record with keywords[] array
4. Flush NDJSON to `.run/digger-output/py-artifacts.ndjson`
5. Update hash registry and write run metadata

## Artifact Record Schema — Hook variant
```json
{
  "id": "py:hook:{filename}:{function}",
  "kind": "hook",
  "name": "post_batch_cascading",
  "file_path": ".claude/hooks/post_batch_cascading.py",
  "hook_event": "PostToolUse",
  "timeout": 30,
  "exit_codes": {"0": "success", "1": "warning", "2": "block"},
  "dependencies": [],
  "hash": "sha256:...",
  "digger": "cart-py-digger",
  "run_id": "py-20260416-001",
  "timestamp": "2026-04-16T00:00:00Z"
}
```

## Artifact Record Schema — Skill variant
```json
{
  "id": "py:skill:{skill_dir_name}",
  "kind": "skill",
  "name": "source-sync",
  "file_path": ".claude/skills/source-sync/SKILL.md",
  "keywords": ["source-sync", "sync", "download", "planilha"],
  "priority": "ALTA",
  "tools": ["Read", "Bash"],
  "hash": "sha256:...",
  "digger": "cart-py-digger",
  "run_id": "py-20260416-001"
}
```

## Gate
- NDJSON file exists and valid
- At minimum one `kind: hook` artifact emitted (hooks directory is non-empty)
- Run metadata written
