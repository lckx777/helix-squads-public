# Source Tree — Nirvana Context Enricher

Expected directory structure for the squad. Maintained by Workflow Creator (scaffolding) and validated by Phase 6 Validator.

## Top-Level Structure

```
squads/nirvana-context-enricher/
├── squad.yaml                          # Manifest (single source of truth for components)
├── README.md                           # Primary documentation
├── README.{en,es,zh,hi,ar}.md          # Multilingual (generated Phase 7)
├── analysis.md                         # Phase 1 artifact — domain analysis (read-only reference)
├── component-registry.md               # Phase 1 artifact — canonical names (read-only)
├── IDEATION.md                         # Phase 2 artifact — composition rationale
│
├── agents/                             # 5 agent persona definitions
│   ├── nirva.md                        # Flow_Master — orchestrator
│   ├── sage.md                         # Builder — deep research
│   ├── scout.md                        # Builder — ecosystem explorer
│   ├── scholar.md                      # Guardian — academic research
│   └── lotus.md                        # Balancer — synthesizer
│
├── tasks/                              # 9 task definitions (Entrada/Saida contracts)
│   ├── parse-enrichment-request.md
│   ├── dispatch-research-team.md
│   ├── execute-deep-research.md
│   ├── explore-skills-ecosystem.md
│   ├── collect-academic-sources.md
│   ├── validate-coverage-quorum.md
│   ├── synthesize-context-report.md
│   ├── deliver-enrichment-report.md
│   └── cleanup-research-team.md
│
├── workflows/                          # High-level pipeline (MACRO steps)
│   └── context-enrichment-pipeline.yaml
│
├── chains/                             # Micro-task decomposition (Constitution Art. VII)
│   └── context-enrichment.yaml         # Decomposes workflow step 3 (parallel research)
│
├── checklists/                         # Gate validation checklists
│   ├── pre-dispatch-readiness.md       # Consumed by nirva before step 2
│   └── synthesis-quality-gate.md       # Consumed by lotus after step 5
│
├── templates/                          # Reusable content schemas
│   ├── research-findings.template.md   # Schema for sage/scout/scholar findings files
│   └── context-report-16section.template.md  # Schema for lotus final report
│
├── scripts/                            # Utility scripts (CommonJS .cjs)
│   └── coverage-validator.cjs          # Chain gate helper for validateCoverageQuorum()
│
├── config/                             # Squad-level configuration
│   ├── coding-standards.md             # Style + naming + error handling rules
│   ├── tech-stack.md                   # Runtime, tooling, state storage
│   └── source-tree.md                  # [THIS FILE] expected directory layout
│
└── references/                         # Optional reference material (empty by default)
```

## Runtime Directories (Created at Execution Time)

NCE creates these directories at runtime — **NOT** part of the squad scaffold, never committed to git. Documented here so the validator does not flag them as missing.

```
.nce/                                   # Runtime state (per-project root)
├── lock                                # Concurrency guard (present during active run)
├── request.md                          # Parsed request (created by parseEnrichmentRequest)
├── findings/
│   ├── sage.md
│   ├── scout.md
│   └── scholar.md
├── report.md                           # Lotus synthesis output
├── dispatch-log.jsonl
├── quorum-log.jsonl
├── chain-log.jsonl
├── history.jsonl                       # Append-only run history
└── archive/
    └── {ISO-8601-timestamp}/           # Per-run archives
        ├── findings/
        ├── request.md
        └── report.md

.claude/context-enrichment/             # User-facing deliverables
└── {topic-slug}.md                     # One per completed run
```

## File Ownership Matrix

| Owner | Artifact |
|-------|----------|
| Analyzer (Phase 1) | `analysis.md`, `component-registry.md` |
| Agent Creator (Phase 2) | `agents/*.md`, `IDEATION.md` |
| Task Creator (Phase 3) | `tasks/*.md` |
| Workflow Creator (Phase 4) | `workflows/*.yaml`, `chains/*.yaml`, `squad.yaml`, `config/*.md`, `README.md` |
| Optimizer (Phase 5) | Refines `config/*`, `README.md`, optionally `squad.yaml` |
| Validator (Phase 6) | Read-only — validates all of the above against AIOS schema |
| README Creator (Phase 7) | `README.{en,es,zh,hi,ar}.md` (multilingual) |
| Publisher (Phase 8) | Deploys to `.claude/` + optional marketplace push |

## Invariants

| Invariant | Rule |
|-----------|------|
| Every file in `agents/` is listed in `squad.yaml > components.agents` | Validator enforces |
| Every file in `tasks/` is listed in `squad.yaml > components.tasks` | Validator enforces |
| Every task's `responsavel` maps to an agent in `agents/` | Validator enforces |
| `chains/` file exists when a workflow step has `chain:` field | Chain enforcement (Art. VII) |
| Filenames are kebab-case + `.md` (agents/tasks) or `.yaml` (workflows/chains) | Validator enforces |
| `squad.yaml > description` is inline string (not multi-line) | Validator enforces (parser quirk) |

## Expansion Paths (Future)

If NCE grows beyond its current scope, these additions fit the layout without restructuring:

- `agents/` → add `hawk.md` (adversarial critic for section 15) — would become a 6th agent
- `chains/` → add `synthesis-chain.yaml` if Lotus's 16-section synthesis ever needs decomposition
- `tasks/` → split `executeDeepResearch()` into 6 round-specific tasks if per-round caching becomes useful
- `templates/` → add per-domain templates (`context-report-ai-ml.template.md`, `context-report-distributed-systems.template.md`)
