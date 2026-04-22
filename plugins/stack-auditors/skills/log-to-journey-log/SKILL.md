---
task: logToJourneyLog()
name: log-to-journey-log
description: Step s3_log of stack-auditors-flow. Persist the chain's verdict + evidence
  to the journey log per _schema.yaml. Enforces the evidence-required gate via checklists/veredict-quality-gate.md.
responsavel: sa-council
responsavel_type: Agente
atomic_layer: Atom
Entrada:
- nome: chain_id
  tipo: string
  obrigatorio: true
  descricao: Chain that produced the verdict
- nome: verdict
  tipo: enum
  obrigatorio: true
  descricao: approved | concerns | blocked | advisory
- nome: skill_evidence
  tipo: object
  obrigatorio: true
  descricao: Evidence YAML from mentor's fundamentation skill (or aggregated for council)
- nome: per_mentor_verdicts
  tipo: object
  obrigatorio: false
  descricao: Map of mentor ID to verdict (council/debate only)
- nome: dissent
  tipo: array
  obrigatorio: false
  descricao: Unresolved concerns (council/debate only)
- nome: story_ref
  tipo: string
  obrigatorio: false
  descricao: Story ID for traceability
- nome: context_path
  tipo: string
  obrigatorio: false
  descricao: File path under audit if no story_ref
- nome: latency_ms
  tipo: integer
  obrigatorio: true
  descricao: End-to-end chain duration
Saida:
- nome: journey_log_path
  tipo: string
  obrigatorio: true
  descricao: .claude/stack-auditors/journey-log/{YYYY-MM-DD}.yaml — file appended
- nome: entry_id
  tipo: string
  obrigatorio: true
  descricao: Generated entry ID for cross-reference (single or N+1 IDs for council)
- nome: gate_passed
  tipo: boolean
  obrigatorio: true
  descricao: veredict-quality-gate.md MUST items all PASS
- nome: gate_failures
  tipo: array
  obrigatorio: false
  descricao: List of failed MUST items (M1..M6) if gate_passed=false
Checklist:
- Journey log file resolved under .claude/stack-auditors/journey-log/{YYYY-MM-DD}.yaml
- Schema _schema.yaml respected (all required fields populated)
- veredict-quality-gate.md MUST items M1-M6 evaluated; M1 (evidence cited) and M5
  (context ref) hard-blocking
- Council/debate produces N+1 entries with cross-references
- 'Bypass entries (sa-skip: true) require bypass_justification'
- On gate FAIL, journey log NOT written; mentor prompted to revise verdict
---

# Task: log-to-journey-log

**Owner:** sa-council
**Workflow step:** stack-auditors-flow → s3_log
**Complexity:** S
**Gate:** evidence-required (checklists/veredict-quality-gate.md)

## Purpose

Persist the chain's output to the journey log so observability metrics (decision_changed, gate
pass rate, kill_criterion) can be computed. This is the ONLY step that enforces the
`evidence-required` gate — the chain itself produces verdicts; this task validates them before
they hit permanent storage.

## Storage contract

- File: `.claude/stack-auditors/journey-log/{YYYY-MM-DD}.yaml`
- Schema: `.claude/stack-auditors/journey-log/_schema.yaml`
- Mode: append-only (preserves history)

## Gate enforcement (veredict-quality-gate.md)

The checklist runs before write. MUST items (blocking):

- **M1** Evidence cited (concrete data point in verdict text)
- **M2** Verdict ∈ {approved, concerns, blocked, advisory}
- **M3** Summary ≤500 chars
- **M4** Traceable to skill output (skill field referenced)
- **M5** story_ref or context_path populated
- **M6** No contradiction with skill_evidence verdict_hint

If any MUST fails:
- Journey log NOT written
- `gate_passed: false` returned with `gate_failures: [Mx, My]`
- Mentor prompted to revise verdict citing the specific failure

## Council / Debate entries

For council-parallel-chain and debate-chain, write N+1 entries (one per mentor + one synthesis)
with cross-references:

```yaml
- id: jl-2026-04-19-001
  chain: council-parallel-chain
  mentor: sa-carmack
  verdict: approved
  skill_evidence: {...}
  references_synthesis: jl-2026-04-19-005

- id: jl-2026-04-19-005
  chain: council-parallel-chain
  mentor: sa-council
  verdict: concerns
  references_mentor_entries: [jl-2026-04-19-001, jl-2026-04-19-002, jl-2026-04-19-003]
```

## Bypass protocol

When a chain is bypassed (e.g., `sa-skip: true` on commit), still write a journey entry:

```yaml
- id: jl-2026-04-19-099
  chain: bypassed
  bypass: true
  bypass_justification: "explicit operator override — story xx, comment yy"
```

Bypass entries are exempt from M1-M4 but MUST have `bypass_justification`.

## Not for

- Routing decisions → handled by `route-to-chain` in `s1_route`
- Running audits → handled by `execute-selected-chain` in `s2_execute`
