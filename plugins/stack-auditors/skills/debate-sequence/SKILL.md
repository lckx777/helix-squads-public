---
task: debateSequence()
name: debate-sequence
description: Sequential debate between two mentors in productive tension. Used when
  the decision itself is philosophical and friction produces clarity that synthesis
  cannot.
responsavel: sa-council
responsavel_type: Agente
atomic_layer: Organism
Entrada:
- nome: target
  tipo: string
  obrigatorio: true
  descricao: Decision under debate
- nome: mentor_a
  tipo: string
  obrigatorio: true
  descricao: First mentor voice
- nome: mentor_b
  tipo: string
  obrigatorio: true
  descricao: Opposing mentor voice
- nome: rounds
  tipo: integer
  obrigatorio: false
  descricao: Number of debate rounds before synthesis, default 3
- nome: story_ref
  tipo: string
  obrigatorio: false
  descricao: Story ID for traceability
Saida:
- nome: tension
  tipo: string
  obrigatorio: true
  descricao: mentor_a vs mentor_b on <topic>
- nome: rounds
  tipo: array
  obrigatorio: true
  descricao: List of rounds with each mentor's position, evidence, and concessions
- nome: synthesis
  tipo: object
  obrigatorio: true
  descricao: agreement, core_tradeoff, situational_recommendation
- nome: decision_changed
  tipo: boolean
  obrigatorio: true
  descricao: Whether the debate altered the primary agent's direction
Checklist:
- Tension declared explicitly in setup
- Both mentors cite skill evidence in at least round 1
- Synthesis surfaces core tradeoff, never consensus-washes
- Situational recommendations emit (when X go A, when Y go B)
- Journey log entry includes decision_changed flag
---

# Task: debate-sequence

**Owner:** sa-council (orchestrator)
**Complexity:** L
**Gate:** evidence-required

## Purpose

Sequential debate between 2+ mentors in productive tension. Used when the DECISION itself is philosophical — tension between mentors produces clarity that parallel synthesis cannot.

Examples:
- **Monolith vs microservices** → sa-newman vs sa-musk (vertical integration)
- **Elegance vs efficiency** → sa-jobs vs sa-carmack
- **Test-first vs pragmatic** → sa-beck vs sa-carmack
- **Standardization vs autonomy** → sa-torvalds vs sa-newman

## Entrada

- `target` — decision under debate
- `mentor_a` — first voice
- `mentor_b` — opposing voice
- `rounds` — (default: 3) debate rounds before synthesis
- `story_ref` — story ID if applicable

## Fluxo

1. **Setup (sa-council)** — declare tension explicitly. Example: "sa-newman will argue for microservices decomposition. sa-musk will argue for vertical integration. Both cite evidence."
2. **Round 1 — mentor_a position** — opening argument + skill evidence
3. **Round 1 — mentor_b rebuttal** — counter + skill evidence
4. **Round 2 — mentor_a response** — acknowledge valid points + restate or refine position
5. **Round 2 — mentor_b response** — same
6. **(Optional) Round 3** — final positions, narrower than openers
7. **Synthesize (sa-council)** — NOT consensus-washing. Surface:
   - What both agree on (high confidence)
   - Core disagreement (trade-off)
   - Situational recommendation (which mentor wins under which conditions)

## Saída

```yaml
task: debate-sequence
tension: "mentor_a vs mentor_b on <topic>"
rounds:
  - round: 1
    mentor_a: {position: "...", evidence: {...}}
    mentor_b: {rebuttal: "...", evidence: {...}}
  - round: 2
    mentor_a: {refinement: "...", conceded: [...]}
    mentor_b: {refinement: "...", conceded: [...]}
synthesis:
  agreement: "what both converge on"
  core_tradeoff: "the real decision"
  situational_recommendation:
    - "If X → go with mentor_a's approach because..."
    - "If Y → go with mentor_b's approach because..."
decision_changed: true | false  # did debate alter the primary agent's direction?
latency_ms: int
```

## Gates

- **evidence-required:** both mentors must cite skill evidence in at least round 1
- **no-consensus-washing:** synthesis MUST surface the core tradeoff, not flatten it

## Not for

- Questions with clear right answer → single-mentor-audit
- When both mentors would agree → council-audit-parallel
