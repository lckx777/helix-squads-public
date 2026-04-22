---
task: synthesizeContextReport()
responsavel: Lotus
responsavel_type: Agente
atomic_layer: Organism
Entrada:
- campo: sageFindings
  tipo: file
  origen: .nce/findings/sage.md (executeDeepResearch() output)
  obrigatorio: true
- campo: scoutFindings
  tipo: file
  origen: .nce/findings/scout.md (exploreSkillsEcosystem() output)
  obrigatorio: true
- campo: scholarFindings
  tipo: file
  origen: .nce/findings/scholar.md (collectAcademicSources() output)
  obrigatorio: true
- campo: reportTemplate
  tipo: file
  origen: templates/context-report-16section.template.md
  obrigatorio: true
- campo: quorumVerdict
  tipo: object
  origen: validateCoverageQuorum() — must have passed=true
  obrigatorio: true
Saida:
- campo: contextReport
  tipo: file
  destino: .nce/report.md (consumed by deliverEnrichmentReport())
  persistido: true
- campo: sourceMap
  tipo: object
  destino: contextReport frontmatter — claim→source traceability index
  persistido: true
Checklist:
  pre-conditions:
  - '[ ] quorumVerdict.passed is true'
  - '[ ] All 3 findings files have status=complete'
  - '[ ] context-report-16section.template.md is readable'
  - '[ ] synthesis-quality-gate.md checklist is loaded'
  post-conditions:
  - '[ ] .nce/report.md exists and is non-empty'
  - '[ ] All 16 sections present and non-empty'
  - '[ ] Every claim maps to at least one citation via sourceMap'
  - '[ ] Section 15 (Contested Findings) is populated when disagreements exist'
  - '[ ] Section 16 (Knowledge Gaps) is always populated'
  - '[ ] synthesis-quality-gate.md all items passed'
  acceptance-criteria:
  - blocker: true
    criteria: Zero sections are empty
  - blocker: true
    criteria: Zero claims without citations
  - blocker: true
    criteria: Synthesis quality gate passes
  - blocker: false
    criteria: No section exceeds 2000 words (readability target)
Template:
  path: templates/context-report-16section.template.md
  type: markdown
  version: 1.0.0
  variables:
  - topic
  - generated_at
  - coverage_stats
  - researchers
  schema: references/task-format.md
Performance:
  duration_expected: 3-6 minutes
  cost_estimated: ~15k tokens (reading 3 findings + composing 16 sections)
  cacheable: false
  parallelizable: false
  skippable_when: Never — this is the synthesis step
Error Handling:
  strategy: retry
  retry:
    max_attempts: 2
    delay: immediate (no backoff)
  fallback: Emit partial report with explicit gaps flagged in Section 16
  notification: nirva
description: '```'
---


## Pipeline Diagram

```
.nce/findings/sage.md    ┐                                  ┌─> contextReport ──> .nce/report.md
                         │                                  │
.nce/findings/scout.md   ├──[synthesizeContextReport()]─────┤
                         │                                  │
.nce/findings/scholar.md ┘                                  └─> sourceMap (claim→citation traceability)
                                         │
                                         ├──read──> templates/context-report-16section.template.md
                                         ├──apply──> synthesis-quality-gate.md checklist
                                         └──gate──> quorumVerdict.passed (pre-condition)
```

## Responsibility

Lotus's sole task. Reconciles 3 independent research perspectives into a single 16-section unified briefing. This is the integration step — no new research, only synthesis of what the 3 parallel researchers produced.

## The 16 Sections (Fixed Order)

| # | Section | Primary Source |
|---|---------|---------------|
| 1 | Executive Summary | all |
| 2 | Topic Definition | sage |
| 3 | Historical Context | sage + scholar |
| 4 | Core Architecture & Mechanics | sage |
| 5 | Theoretical Foundations | scholar |
| 6 | Best Practices | sage |
| 7 | Advanced Considerations | sage |
| 8 | Current State & Trends | sage + scholar |
| 9 | Ecosystem Map — Skills | scout |
| 10 | Ecosystem Map — Libraries | scout |
| 11 | Ecosystem Map — Curated Collections | scout |
| 12 | Recommended Tools Shortlist | scout |
| 13 | Academic References | scholar |
| 14 | Common Pitfalls & Anti-Patterns | sage |
| 15 | Contested Findings & Disagreements | all |
| 16 | Knowledge Gaps & Open Questions | all |

## Execution Steps

1. Validate pre-conditions (quorum passed, all findings complete)
2. Load template and quality gate checklist
3. Build internal source map: `claim → (researcher, citation)`
4. Compose each of 16 sections in order:
   - Pull from primary source(s)
   - Cross-reference secondary sources
   - Preserve citations verbatim
   - Surface disagreements in Section 15 (never silently resolve)
5. Populate Section 16 with explicit gaps:
   - Rounds Sage flagged as "thin"
   - Axes Scout marked "no findings"
   - Topics with only tier-4 preprint sources
   - User questions no researcher addressed
6. Run synthesis-quality-gate.md checklist
7. Write `.nce/report.md` with YAML frontmatter containing coverage stats and sources_cited counter

## Conflict Resolution Rules

| Conflict | Lead With | Cite |
|----------|-----------|------|
| Sage (blog) vs Scholar (peer-reviewed) | Scholar | Sage as practical counterpoint |
| Scout (lib claim) vs Sage (official docs) | Sage (primary source) | Scout with maintenance verdict |
| Scholar tier-1 vs tier-4 | Tier-1 | Tier-4 as "emerging signal" |
| Unresolvable | neither | Both, surfaced in Section 15 |
