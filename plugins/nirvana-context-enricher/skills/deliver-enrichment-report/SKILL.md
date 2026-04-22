---
task: deliverEnrichmentReport()
responsavel: Nirva
responsavel_type: Agente
atomic_layer: Molecule
Entrada:
- campo: contextReport
  tipo: file
  origen: .nce/report.md (synthesizeContextReport() output)
  obrigatorio: true
- campo: parsedRequest
  tipo: file
  origen: .nce/request.md (parseEnrichmentRequest() output)
  obrigatorio: true
Saida:
- campo: deliveredPath
  tipo: string
  destino: user (displayed in final message)
  persistido: false
- campo: finalReport
  tipo: file
  destino: .claude/context-enrichment/{slugified-topic}.md (user-facing artifact)
  persistido: true
- campo: executiveSummary
  tipo: string
  destino: user (displayed in final message, extracted from Section 1 of report)
  persistido: false
Checklist:
  pre-conditions:
  - '[ ] .nce/report.md exists and is non-empty'
  - '[ ] synthesis-quality-gate.md passed for this report'
  - '[ ] .claude/context-enrichment/ directory exists and is writable'
  - '[ ] Topic slug can be generated (no conflicting filename)'
  post-conditions:
  - '[ ] .claude/context-enrichment/{slug}.md exists'
  - '[ ] File has YAML frontmatter with topic, generated_at, coverage_stats, researchers'
  - '[ ] Executive summary ≤ 3 sentences'
  - '[ ] deliveredPath is absolute and points to a readable file'
  acceptance-criteria:
  - blocker: true
    criteria: Final file exists at the declared path
  - blocker: true
    criteria: Frontmatter is parseable YAML
  - blocker: false
    criteria: Filename slug is URL-safe
Performance:
  duration_expected: <2 seconds
  cost_estimated: ~500 tokens (summary extraction + frontmatter build)
  cacheable: false
  parallelizable: false
  skippable_when: Never — delivery is the user-facing result
Error Handling:
  strategy: retry
  retry:
    max_attempts: 2
    delay: immediate
  fallback: If target path is unwritable, fall back to .nce/report-delivered.md and
    surface path to user
  notification: user
description: '```'
---


## Pipeline Diagram

```
.nce/report.md ──────> [deliverEnrichmentReport()] ──finalReport────> .claude/context-enrichment/{slug}.md
                                │                          │
.nce/request.md ──topic slug──> │                          ├──executiveSummary──> user message
                                │                          │
                                │                          └──deliveredPath─────> user message
```

## Responsibility

Delivers the final synthesized report to the user-facing location. Nirva adds metadata frontmatter, extracts a 3-sentence executive summary from Section 1, and returns the path.

## Execution Steps

1. Read `.nce/report.md`
2. Read `.nce/request.md` to extract original topic and scope
3. Slugify topic (kebab-case, URL-safe, strip stopwords)
4. Check for filename collision in `.claude/context-enrichment/`
   - If collision: append `-{ISO-date}` suffix
5. Build YAML frontmatter:
   ```yaml
   ---
   topic: "<original topic>"
   scope: "<original scope or null>"
   generated_at: <ISO-8601>
   coverage_stats:
     sage_searches: <int>
     scout_searches: <int>
     scholar_searches: <int>
     total_extractions: <int>
   researchers: [sage, scout, scholar]
   synthesizer: lotus
   orchestrator: nirva
   ---
   ```
6. Prepend frontmatter + write to `.claude/context-enrichment/{slug}.md`
7. Extract first 3 sentences of Section 1 as executive summary
8. Return `deliveredPath` and `executiveSummary` to Nirva controller
9. Nirva displays both to the user

## Slugification Rules

| Input | Slug |
|-------|------|
| "Vector Databases" | `vector-databases` |
| "Event Sourcing + CQRS" | `event-sourcing-cqrs` |
| "What is CRDT?" | `crdt` (stopwords removed) |
| Slug conflict exists | `vector-databases-2026-04-13` |
