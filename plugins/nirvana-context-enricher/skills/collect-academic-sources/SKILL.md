---
task: collectAcademicSources()
responsavel: Scholar
responsavel_type: Agente
atomic_layer: Molecule
Entrada:
- campo: scholarBrief
  tipo: object
  origen: dispatchResearchTeam() scholar-brief payload
  obrigatorio: true
- campo: findingsTemplate
  tipo: file
  origen: templates/research-findings.template.md
  obrigatorio: true
Saida:
- campo: scholarFindings
  tipo: file
  destino: .nce/findings/scholar.md (consumed by synthesizeContextReport() via join
    barrier)
  persistido: true
- campo: coverageStats
  tipo: object
  destino: scholar.md YAML frontmatter — consumed by validateCoverageQuorum()
  persistido: true
Checklist:
  pre-conditions:
  - '[ ] scholarBrief contains non-empty topic'
  - '[ ] research-findings.template.md is readable'
  - '[ ] .nce/findings/ directory is writable'
  - '[ ] Web search capability is available (Google Scholar / arxiv accessible)'
  post-conditions:
  - '[ ] .nce/findings/scholar.md exists and is non-empty'
  - '[ ] File has YAML frontmatter with status, searches, extractions, papers_cited,
    tier_breakdown'
  - '[ ] Both phases present (Seminal References + Current Research)'
  - '[ ] Total searches ≥ 2'
  - '[ ] Total extractions ≥ 2'
  - '[ ] Papers cited ≥ 2, each with DOI or stable URL'
  - '[ ] Every paper has a tier tag (1-4)'
  acceptance-criteria:
  - blocker: true
    criteria: Zero tier-5 (predatory/unreviewed blog) sources admitted
  - blocker: true
    criteria: 'Coverage quorum met: ≥2 searches, ≥2 extractions, ≥2 papers cited'
  - blocker: false
    criteria: At least 1 tier-1 or tier-2 source
Tools:
- tool_name: WebSearch
  version: latest
  used_for: Academic database search (Google Scholar, arxiv, ACM/IEEE/Springer)
  shared_with:
  - executeDeepResearch()
  - exploreSkillsEcosystem()
  cost: free
  cacheable: true
- tool_name: WebFetch
  version: latest
  used_for: Fetching paper abstracts and metadata
  shared_with:
  - executeDeepResearch()
  - exploreSkillsEcosystem()
  cost: free
  cacheable: true
Performance:
  duration_expected: 2-4 minutes
  cost_estimated: ~3k tokens + 2-4 academic searches + 2-3 abstract fetches
  cacheable: true
  parallelizable: true
  skippable_when: Never — academic grounding is non-negotiable for NCE reports
Error Handling:
  strategy: fallback
  fallback: If no peer-reviewed (tier 1-2) work exists, fall back to tier 3 (arxiv
    cited by peer-reviewed). Flag tier explicitly.
  notification: nirva
description: '```'
---


## Pipeline Diagram

```
scholarBrief ──topic+scope──> [collectAcademicSources()] ──scholarFindings──> .nce/findings/scholar.md
                                       │                         │
                                       │ 2 phases:               │
                                       │  1. seminal works       │ (status=complete, papers≥2,
                                       │  2. current research    │  every citation has DOI/URL)
                                       │                         │
                                       │                         └──coverageStats──> [validateCoverageQuorum()]
                                       ▼
                          WebSearch (academic) + WebFetch
```

## Responsibility

Scholar's core task. Collects peer-reviewed papers and foundational academic references with strict tier enforcement. Guards the academic rigor of the final report.

## Execution Steps

1. **Phase 1 — Seminal Works**
   - Search for foundational papers on the topic
   - Identify 1-2 seminal references (most-cited, canonical)
   - Extract title, authors, venue, year, DOI, abstract excerpt
   - Assign tier per source hierarchy

2. **Phase 2 — Current Research**
   - Search for peer-reviewed work from the last 3-5 years
   - Identify 1-2 recent papers extending the foundations
   - Extract same metadata as Phase 1

3. **Contested Findings Check**
   - If the literature disagrees on a claim, capture both sides in a `contested:` block
   - Do NOT silently choose a winner — Lotus will surface the debate in the final report

4. **Quality Gate**
   - Reject any tier-5 source (predatory journal, unverifiable blog)
   - If fallback to tier 3 or 4, tag explicitly in findings

5. **Write findings**
   - YAML frontmatter with counters + tier_breakdown
   - Two section bodies (seminal + current)
   - Set `status: complete` if quorum met, else `status: failed`

## Source Hierarchy Enforcement

| Tier | Example | Admitted? |
|------|---------|-----------|
| 1 | Peer-reviewed journal (ACM/IEEE/Springer/Nature) | ✅ |
| 2 | Top-tier conference (SOSP, OSDI, ICML, NeurIPS, POPL, PLDI) | ✅ |
| 3 | Arxiv with peer-reviewed citations | ✅ (tag as "cited preprint") |
| 4 | Unreviewed arxiv preprint | ⚠️ (tag as "preprint only") |
| 5 | Predatory journal / blog repost | ❌ REJECT |
