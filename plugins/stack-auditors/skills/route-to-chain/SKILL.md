---
task: routeToChain()
name: route-to-chain
description: Step s1_route of stack-auditors-flow. Inspect invocation context (mode,
  trigger, path, explicit_mentor, story complexity) and select exactly one chain (single-audit
  | council-parallel | debate).
responsavel: sa-council
responsavel_type: Agente
atomic_layer: Atom
Entrada:
- nome: input.mode
  tipo: enum
  obrigatorio: false
  descricao: 'Explicit mode override: single-audit | council-parallel | debate-sequence
    | pre-implementation-audit | post-implementation-review'
- nome: input.trigger
  tipo: enum
  obrigatorio: false
  descricao: 'Source of invocation: rule | hook | aiox_agent | post-pr | manual'
- nome: input.explicit_mentor
  tipo: string
  obrigatorio: false
  descricao: Mentor ID forced by caller (e.g., sa-carmack)
- nome: input.mentors_selected
  tipo: array
  obrigatorio: false
  descricao: Mentor IDs already chosen upstream by an activation rule
- nome: input.story_frontmatter
  tipo: object
  obrigatorio: false
  descricao: Story metadata block — used to detect complexity == XL | COMPLEX
- nome: input.pr
  tipo: object
  obrigatorio: false
  descricao: PR metadata block — used to detect high_stakes == true
Saida:
- nome: chain_selected
  tipo: enum
  obrigatorio: true
  descricao: single-audit-chain | council-parallel-chain | debate-chain
- nome: mentor
  tipo: string
  obrigatorio: false
  descricao: Mentor ID for single-audit selection
- nome: mentors_selected
  tipo: array
  obrigatorio: false
  descricao: Mentor IDs for council/debate selection
- nome: routing_reason
  tipo: string
  obrigatorio: true
  descricao: Which routing rule fired and why
Checklist:
- Routing rules evaluated in declared order (1 explicit mode, 2 pre-impl, 3 post-pr,
  4 explicit_mentor, 5 rule single, 6 rule multi, default)
- First matching rule wins; later rules ignored
- Selected chain exists in components.chains
- If single-audit, exactly 1 mentor resolved; if council/debate, ≥2 resolved
- routing_reason logged for journey log audit trail
---

# Task: route-to-chain

**Owner:** sa-council
**Workflow step:** stack-auditors-flow → s1_route
**Complexity:** S
**Gate:** routing must select exactly one chain

## Purpose

Resolve the invocation input into a chain selection. This is a pure routing decision — no audit
work happens here. The output is consumed by step `s2_execute` to delegate to the chosen chain.

## Routing rules (priority order)

1. `input.mode == 'single-audit'`     → `single-audit-chain`
2. `input.mode == 'council-parallel'` → `council-parallel-chain`
3. `input.mode == 'debate-sequence'`  → `debate-chain`
4. `input.story_frontmatter.complexity ∈ {XL, COMPLEX}` → `council-parallel-chain` + `task: pre-implementation-audit`
5. `input.trigger == 'post-pr' AND input.pr.high_stakes == true` → `council-parallel-chain` + `task: post-implementation-review`
6. `input.explicit_mentor != null` → `single-audit-chain` + `mentor: {input.explicit_mentor}`
7. `input.trigger == 'rule' AND input.mentors_selected.length == 1` → `single-audit-chain` + `mentor: {first}`
8. `input.trigger == 'rule' AND input.mentors_selected.length > 1`  → `council-parallel-chain` + `mentors: {input.mentors_selected}`
9. Default → `single-audit-chain` (sa-council picks mentor by semantic routing)

## Output contract

```yaml
chain_selected: single-audit-chain | council-parallel-chain | debate-chain
mentor: sa-{name}                # only for single-audit
mentors_selected: [sa-x, sa-y]   # only for council/debate
routing_reason: "rule_index + condition match"
```

## Not for

- Actually running audits → handled by chains in `s2_execute`
- Persisting verdicts → handled by `log-to-journey-log` in `s3_log`
