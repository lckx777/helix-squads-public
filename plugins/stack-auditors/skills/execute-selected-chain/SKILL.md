---
task: executeSelectedChain()
name: execute-selected-chain
description: Step s2_execute of stack-auditors-flow. Delegate execution to the chain
  chosen by route-to-chain. The chain owns its own micro_tasks sequence; this task
  only invokes and awaits.
responsavel: sa-council
responsavel_type: Agente
atomic_layer: Molecule
Entrada:
- nome: chain_selected
  tipo: enum
  obrigatorio: true
  descricao: single-audit-chain | council-parallel-chain | debate-chain (from route-to-chain)
- nome: mentor
  tipo: string
  obrigatorio: false
  descricao: Mentor ID for single-audit chains
- nome: mentors_selected
  tipo: array
  obrigatorio: false
  descricao: Mentor IDs for council/debate chains
- nome: target
  tipo: string
  obrigatorio: true
  descricao: Audit target (file path, decision, spec section)
- nome: story_ref
  tipo: string
  obrigatorio: false
  descricao: Story ID for traceability
Saida:
- nome: verdict
  tipo: enum
  obrigatorio: true
  descricao: approved | concerns | blocked | advisory (from the chain's chain_gate)
- nome: skill_evidence
  tipo: object
  obrigatorio: true
  descricao: Aggregated evidence — single skill output for single-audit, map for council,
    debate rounds for debate
- nome: per_mentor_verdicts
  tipo: object
  obrigatorio: false
  descricao: Map of mentor ID to verdict (council/debate only)
- nome: dissent
  tipo: array
  obrigatorio: false
  descricao: Concerns not resolved during synthesis (council/debate only)
- nome: chain_id
  tipo: string
  obrigatorio: true
  descricao: Chain that ran (for traceability)
Checklist:
- Chain selected matches one of the components.chains entries
- Chain micro_tasks ran in declared order without unexpected handoffs
- chain_gate condition evaluated and verdict produced
- Auto-handoff exceptions respected (mentor_verdict == blocked stops chain)
- Latency captured for journey log entry
---

# Task: execute-selected-chain

**Owner:** sa-council
**Workflow step:** stack-auditors-flow → s2_execute
**Complexity:** M
**Gate:** chain_gate of the selected chain

## Purpose

Pure delegation step — invoke the chain chosen by `route-to-chain` and propagate its output. The
chain encapsulates its own micro_tasks pipeline (route → skill → verdict → log) and produces a
verdict bundle. This task does NOT re-implement the audit logic; it only awaits the chain.

## Selection mapping

| chain_selected            | Chain file                                  | Owner micro_tasks |
|---------------------------|---------------------------------------------|-------------------|
| `single-audit-chain`      | `chains/single-audit-chain.yaml`            | mt001..mt004      |
| `council-parallel-chain`  | `chains/council-parallel-chain.yaml`        | mt001..mt004      |
| `debate-chain`            | `chains/debate-chain.yaml`                  | mt001..mt007      |

## Output contract

```yaml
verdict: approved | concerns | blocked | advisory
skill_evidence: { ... }
per_mentor_verdicts: { sa-x: {...}, sa-y: {...} }   # council/debate only
dissent: ["concern 1", "concern 2"]                  # council/debate only
chain_id: <id>
latency_ms: <int>
```

## Auto-handoff exceptions

The flow's `auto_handoff` block stops the chain when:
- `@devops *push` — never auto-activated
- `gate_fail` — escalates to operator
- `mentor_verdict == 'blocked'` — chain stops, no further mentors invoked

When stopped early, return `verdict: blocked` + `dissent: [stop_reason]`.

## Not for

- Routing decisions → handled by `route-to-chain` in `s1_route`
- Persisting verdicts → handled by `log-to-journey-log` in `s3_log`
