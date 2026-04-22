---
task: doctrineExtraction()
name: doctrine-extraction
description: Extract reusable doctrine from a specific audit outcome. Output is an
  ADR future agents consult before re-running the same audit.
responsavel: sa-council
responsavel_type: Agente
atomic_layer: Molecule
Entrada:
- nome: mentor
  tipo: string
  obrigatorio: true
  descricao: Mentor ID extracting the doctrine
- nome: topic
  tipo: string
  obrigatorio: true
  descricao: Subject of the doctrine (e.g., queue-processor perf budget)
- nome: source_audit
  tipo: string
  obrigatorio: true
  descricao: journey_log entry ID that motivated the doctrine
Saida:
- nome: adr_path
  tipo: string
  obrigatorio: true
  descricao: Path to the written ADR (docs/architecture/adr-sa-{mentor}-{slug}.md)
- nome: abstract_principle
  tipo: string
  obrigatorio: true
  descricao: One-sentence abstract principle extracted from the audit
- nome: rule_update_proposed
  tipo: boolean
  obrigatorio: true
  descricao: Whether a new sa-activation.md path trigger is proposed
- nome: source_audit_id
  tipo: string
  obrigatorio: true
  descricao: Traceability anchor to the source journey log entry
Checklist:
- Source audit reviewed (journey log + skill evidence)
- Principle abstracted from specific case (rule, not anecdote)
- ADR written in standard format (Status/Context/Decision/Consequences/Enforcement/References)
- ADR saved to docs/architecture/adr-sa-{mentor}-{slug}.md
- Existing ADRs grepped to avoid duplication
- 'Journey log entry written with trigger: doctrine-extraction'
---

# Task: doctrine-extraction

**Owner:** Single mentor
**Complexity:** M
**Gate:** evidence-required

## Purpose

Extract reusable doctrine/principle/pattern from a specific audit outcome. Output is an ADR
(Architecture Decision Record) that future agents consult before re-running the same audit.

Usage: when a mentor's verdict establishes a pattern the team should follow forever.

## Entrada

- `mentor` — which mentor extracts the doctrine
- `topic` — subject of the doctrine (e.g., "queue-processor perf budget", "jwt secret storage policy")
- `source_audit` — journey_log entry ID that motivated the doctrine (for traceability)

## Fluxo

1. **Review source audit (mentor)** — read journey log entry + skill evidence
2. **Abstract principle** — extract the rule from the specific case:
   - Bad: "packages/queue-processor.ts:42 is slow" (specific)
   - Good: "Hot path functions MUST have benchmark regression test blocking merge" (abstract)
3. **Write ADR** — mentor drafts in format:
   ```markdown
   # ADR-sa-{mentor}-{topic-slug}: {title}
   **Status:** Accepted
   **Date:** YYYY-MM-DD
   **Mentor:** sa-{name}
   **Source audit:** journey_log entry ID
   ## Context
   ## Decision
   ## Consequences
   ## Enforcement
   ## References
   ```
4. **Save** — `docs/architecture/adr-sa-{mentor}-{slug}.md`
5. **Update rule** — if ADR implies new `.claude/rules/sa-activation.md` path trigger, propose update
6. **Log** — journey log entry with `trigger: doctrine-extraction`

## Saída

```yaml
task: doctrine-extraction
mentor: sa-{name}
topic: "{topic}"
source_audit_id: "{journey-log-id}"
adr_path: "docs/architecture/adr-sa-{mentor}-{slug}.md"
rule_update_proposed: bool
abstract_principle: "{one-sentence principle}"
latency_ms: int
```

## Gates

- **evidence-required:** principle must trace to source audit evidence
- **no-duplication:** mentor must grep `docs/architecture/` for similar ADR before writing new

## Ownership

This is the MOST high-leverage task. One doctrine extracted = hundreds of future audits avoided
(because pattern is now codified as rule/hook/ADR).

Review frequency: weekly. sa-council should nominate top 3 audits from past 7 days for doctrine extraction.
