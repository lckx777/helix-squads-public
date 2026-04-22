---
task: indexYaml()
responsavel: Cart YAML Digger
responsavel_type: Agente
atomic_layer: Molecule
workflow: cartographer-excavation
step: 3
Entrada:
- campo: glob_scope
  tipo: config
  obrigatorio: true
  validacao: squads/**/squad.yaml, squads/**/agents/*.md, .claude/agents/*.md, squads/**/chains/*.yaml,
    .mcp.json
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
- campo: yaml_artifacts
  tipo: file
  destino: squads/cartographer/.run/digger-output/yaml-artifacts.ndjson
  obrigatorio: true
- campo: updated_hashes
  tipo: file
  destino: squads/cartographer/.run/last-hashes.json
  obrigatorio: true
- campo: digger_run_meta
  tipo: file
  destino: squads/cartographer/.run/digger-runs/yaml-{run_id}.yaml
  obrigatorio: true
Checklist:
- '[ ] All squad.yaml files found and parsed'
- '[ ] All .claude/agents/*.md frontmatter extracted'
- '[ ] All squads/**/agents/*.md YAML blocks extracted'
- '[ ] All chains/*.yaml step-to-agent edges recorded'
- '[ ] .mcp.json parsed — MCP server names only (no env var values)'
- '[ ] Cross-squad dependency edges recorded'
- '[ ] Output NDJSON valid per digger-base-contract.md'
- '[ ] last-hashes.json updated'
description: '- **ID:** index-yaml'
---


# Task: Index YAML

## Metadata
- **ID:** index-yaml
- **Workflow:** cartographer-excavation
- **Step:** 3
- **Agent:** cart-yaml-digger
- **Parallel:** can run in parallel with steps 1+2

## Description
Excavates all YAML configuration and Markdown agent manifests, mapping the complete topology
of squads, agents, workflows, chains, and MCP registrations.

## Execution Steps

1. Hash-check all target files
2. **squad.yaml files** (`squads/**/squad.yaml`):
   - Extract: name, version, orchestrator, tiers (opus/sonnet agent lists), sub_squads, routing table, gates, cross_squad_dependencies
   - Emit: `kind: squad` artifact + squad-to-squad dependency edges
3. **Agent definition files** (`.claude/agents/*.md`, `squads/**/agents/*.md`):
   - Extract frontmatter: name, description, model, tools
   - From YAML body block: agent.id, agent.title, tier, commands, dependencies
   - Emit: `kind: agent` artifact
4. **Task definition files** (`squads/**/tasks/*.md`):
   - Extract frontmatter: task name, responsavel, workflow, step, Entrada, Saida fields
   - Emit: `kind: task` artifact with input/output contracts
5. **Chain files** (`squads/**/chains/*.yaml`):
   - Extract: chain name, steps (agent_id, task_id, condition, auto_handoff)
   - Emit: `kind: chain` artifact + step-to-agent edges
6. **MCP registration** (`.mcp.json`, `.claude/settings.json`, `.claude/settings.local.json`):
   - Extract: server names, command, args pattern (no env values)
   - Emit: `kind: mcp_server` artifact
7. Flush to `.run/digger-output/yaml-artifacts.ndjson`

## Squad Artifact Record
```json
{
  "id": "yaml:squad:copy-chief",
  "kind": "squad",
  "name": "copy-chief",
  "version": "2.0.0",
  "orchestrator": "helix",
  "agents": ["atlas", "echo", "scout", "hawk", "sentinel"],
  "cross_squad_deps": ["content-radar"],
  "routing": {"research": ["vox"], "vsl": ["echo"]},
  "file_path": "squads/copy-chief/squad.yaml",
  "hash": "sha256:...",
  "digger": "cart-yaml-digger"
}
```

## Gate
- All squad.yaml files in squads/ directory have been parsed
- At least one `kind: agent` record per squad found
- No env var values present in MCP records
