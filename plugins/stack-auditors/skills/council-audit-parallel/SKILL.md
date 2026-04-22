---
task: councilAuditParallel()
name: council-audit-parallel
description: Parallel invocation of N mentors for ambiguous decisions requiring multiple
  lenses. Council synthesizes divergent verdicts into unified recommendation.
responsavel: sa-council
responsavel_type: Agente
atomic_layer: Molecule
Entrada:
- nome: target
  tipo: string
  obrigatorio: true
  descricao: Decision, spec, or artifact under audit
- nome: mentors
  tipo: array
  obrigatorio: false
  descricao: List of mentor IDs to invoke; if omitted sa-council selects by domain
- nome: minimum_mentors
  tipo: integer
  obrigatorio: false
  descricao: Minimum mentor count, default 3
- nome: story_ref
  tipo: string
  obrigatorio: false
  descricao: Story ID for traceability
Saida:
- nome: council_verdict
  tipo: enum
  obrigatorio: true
  descricao: approved | concerns | blocked (any veto = block)
- nome: per_mentor_verdicts
  tipo: object
  obrigatorio: true
  descricao: Map of mentor ID to verdict + evidence + summary
- nome: council_summary
  tipo: string
  obrigatorio: true
  descricao: Synthesis text preserving dissent
- nome: dissent
  tipo: array
  obrigatorio: true
  descricao: Concerns not resolved during synthesis
Checklist:
- At least 3 mentors selected covering distinct perspectives
- All N mentors spawned in parallel via Agent() in single message
- Each mentor invoked its fundamentation skill
- Council synthesis preserves dissent rather than averaging
- N+1 journey log entries written (N mentors + 1 council)
---

# Task: council-audit-parallel

**Owner:** sa-council (orchestrator)
**Complexity:** M
**Gate:** evidence-required

## Purpose

Parallel invocation of N mentors for ambiguous decisions requiring multiple lenses. Council synthesizes divergent verdicts into unified recommendation.

## Entrada

- `target` — decision, spec, or artifact under audit
- `mentors` — (optional) list of mentor IDs. If omitted, sa-council selects based on domain signals
- `minimum_mentors` — (default: 3)
- `story_ref` — story ID if applicable

## Fluxo

1. **Select mentors (sa-council)** — at least 3, covering distinct perspectives (e.g., perf + security + UX; OR architecture + product + db)
2. **Spawn in parallel** — N `Agent(subagent_type="sa-{mentor}", prompt=...)` calls in single message
3. **Each mentor:** invoke own skill → produce evidence → deliver verdict
4. **Synthesize (sa-council)** — unified verdict structure:
   - If all `approved` → council verdict = `approved`
   - If any `blocked` → council verdict = `blocked` (any veto = block)
   - If mixed `approved/concerns` → council verdict = `concerns` + list concerns
5. **Log** — N+1 entries (N mentor invocations + 1 council synthesis)

## Saída

```yaml
task: council-audit-parallel
mentors_invoked: [sa-x, sa-y, sa-z]
per_mentor_verdicts:
  sa-x: {verdict: approved, evidence: {...}, summary: "..."}
  sa-y: {verdict: concerns, evidence: {...}, summary: "..."}
  sa-z: {verdict: approved, evidence: {...}, summary: "..."}
council_verdict: approved | concerns | blocked
council_summary: "synthesis text"
dissent: [list of concerns not resolved]
latency_ms: int  # max of parallel + council synthesis
```

## Gates

- **evidence-required:** each mentor must have `evidence_cited: true`
- **minimum-mentors:** ≥3 unless explicitly overridden

## Not for

- Simple single-domain question → use `single-mentor-audit` (faster, cheaper)
- Intentional tension exploration → use `debate-sequence`
