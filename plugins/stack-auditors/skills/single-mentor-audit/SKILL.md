---
task: singleMentorAudit()
name: single-mentor-audit
description: Single-focus audit from one mentor. Fastest path when the question domain
  is unambiguous.
responsavel: sa-council
responsavel_type: Agente
atomic_layer: Atom
Entrada:
- nome: target
  tipo: string
  obrigatorio: true
  descricao: File path, decision description, or spec section under audit
- nome: mentor
  tipo: string
  obrigatorio: false
  descricao: Specific mentor ID to invoke; if omitted sa-council routes by domain
- nome: context
  tipo: string
  obrigatorio: false
  descricao: Additional context or story reference
Saida:
- nome: verdict
  tipo: enum
  obrigatorio: true
  descricao: approved | concerns | blocked
- nome: skill_evidence
  tipo: object
  obrigatorio: true
  descricao: Structured YAML evidence from the mentor's fundamentation skill
- nome: verdict_summary
  tipo: string
  obrigatorio: true
  descricao: 1-2 sentence summary of the verdict
- nome: latency_ms
  tipo: integer
  obrigatorio: true
  descricao: End-to-end audit duration in milliseconds
Checklist:
- Target mentor selected via routing rules or explicit parameter
- Fundamentation skill invoked (unless mentor is sa-council)
- Evidence cited inline in verdict
- Journey log entry appended at .claude/stack-auditors/journey-log/{date}.yaml
---

# Task: single-mentor-audit

**Owner:** sa-council (routes) → target mentor (executes)
**Complexity:** S
**Gate:** evidence-required

## Purpose

Single-focus audit from one mentor. Fastest path when the question domain is unambiguous.

## Entrada

- `target` — file path, decision description, or spec section
- `mentor` — (optional) specific mentor to invoke; if omitted, sa-council routes
- `context` — (optional) additional context / story reference

## Fluxo

1. **Route (sa-council)** — determine target mentor based on:
   - Explicit `mentor` parameter, OR
   - Path matching via `.claude/rules/sa-activation.md`, OR
   - Semantic routing (keyword extraction from question)
2. **Fundamentation (target mentor)** — invoke `fundamentation_skill` (if defined) to produce structured evidence YAML
3. **Verdict (target mentor)** — cite evidence + deliver verdict (`approved | concerns | blocked`)
4. **Log (sa-council)** — append entry to `.claude/stack-auditors/journey-log/{date}.yaml`

## Saída

```yaml
task: single-mentor-audit
mentor: sa-{name}
skill_invoked: sa-*-*
skill_evidence: {...}
verdict: approved | concerns | blocked
verdict_summary: "1-2 sentences"
evidence_cited: true | false
latency_ms: int
```

## Gates

- **evidence-required:** `skill_evidence` non-null (unless mentor is sa-council with no skill) AND `evidence_cited: true`. If fails → verdict marked `advisory` and flagged for review.

## Not for

- Ambiguous questions requiring multiple lenses → use `council-audit-parallel`
- Tensions that need debate → use `debate-sequence`
- Blocking commit or PR → use `pre-implementation-audit` or `post-implementation-review`
