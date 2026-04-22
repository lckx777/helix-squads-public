# Stack Auditors — Source Tree

> AIOS source tree reference. Maps squad file layout + external integration points.

```
copywriting-ecosystem/
├── .claude/
│   ├── agents/
│   │   ├── sa-council.md           # Native loader (frontmatter + quick commands + link)
│   │   ├── sa-carmack.md
│   │   ├── sa-van-rossum.md
│   │   ├── sa-stonebraker.md
│   │   ├── sa-torvalds.md
│   │   ├── sa-jobs.md
│   │   ├── sa-musk.md
│   │   ├── sa-schneier.md
│   │   ├── sa-kim.md
│   │   ├── sa-beck.md
│   │   ├── sa-newman.md
│   │   └── sa-norman.md
│   │
│   ├── skills/                     # L1 fundamentation (executable code)
│   │   ├── sa-carmack-bench/
│   │   │   └── SKILL.md
│   │   ├── sa-van-rossum-lint/
│   │   │   └── SKILL.md
│   │   ├── sa-stonebraker-plan/
│   │   │   └── SKILL.md
│   │   ├── sa-torvalds-git/
│   │   │   └── SKILL.md
│   │   ├── sa-jobs-taste/
│   │   │   └── SKILL.md
│   │   ├── sa-musk-requirements/
│   │   │   └── SKILL.md
│   │   ├── sa-schneier-threat/
│   │   │   └── SKILL.md
│   │   ├── sa-kim-flow/
│   │   │   └── SKILL.md
│   │   ├── sa-beck-tdd/
│   │   │   └── SKILL.md
│   │   ├── sa-newman-services/
│   │   │   └── SKILL.md
│   │   └── sa-norman-affordance/
│   │       └── SKILL.md
│   │
│   ├── rules/
│   │   └── sa-activation.md        # Path-based auto-activation (70% of model)
│   │
│   ├── hooks/
│   │   └── sa-gate-enforcement.cjs # Catastrophic enforcement (30% of model)
│   │
│   └── stack-auditors/              # Observability layer
│       ├── README.md               # Observability guide + kill/expand criteria
│       └── journey-log/
│           ├── _schema.yaml        # Schema for log entries
│           └── {YYYY-MM-DD}.yaml   # Daily logs (runtime)
│
├── squads/stack-auditors/
│   ├── squad.yaml                  # AIOS 2.1.0 manifest
│   ├── README.md                   # Squad overview + architecture
│   ├── _TEMPLATE.md                # Canonical persona template (11 sections)
│   │
│   ├── agents/                     # Full persona bodies (10+ sections each)
│   │   ├── sa-council.md
│   │   ├── sa-carmack.md
│   │   ├── sa-van-rossum.md
│   │   ├── sa-stonebraker.md
│   │   ├── sa-torvalds.md
│   │   ├── sa-jobs.md
│   │   ├── sa-musk.md
│   │   ├── sa-schneier.md
│   │   ├── sa-kim.md
│   │   ├── sa-beck.md
│   │   ├── sa-newman.md
│   │   └── sa-norman.md
│   │
│   ├── tasks/
│   │   ├── single-mentor-audit.md
│   │   ├── council-audit-parallel.md
│   │   ├── debate-sequence.md
│   │   ├── pre-implementation-audit.md
│   │   ├── post-implementation-review.md
│   │   └── doctrine-extraction.md
│   │
│   ├── chains/
│   │   ├── single-audit-chain.yaml
│   │   ├── council-parallel-chain.yaml
│   │   └── debate-chain.yaml
│   │
│   ├── checklists/
│   │   └── veredict-quality-gate.md
│   │
│   ├── config/
│   │   ├── persona-catalog.md      # Single source for mentor relationships
│   │   ├── invocation-rules.md     # Rules engine
│   │   └── source-tree.md          # this file
│   │
│   └── workflows/
│       └── stack-auditors-flow.yaml
│
├── scripts/stack-auditors/
│   └── metrics.sh                  # decision_changed calculator
│
└── docs/
    ├── stories/
    │   └── chore-squad-stack-auditors-v1.story.md   # tracking story
    └── architecture/
        └── adr-stack-auditors-layer.md              # L4 layer ADR (planned)
```

---

## File ownership

| Path | Owner | Modifiable by |
|------|-------|--------------|
| `.claude/agents/sa-*.md` | @sm / @po | Create/edit via story |
| `squads/stack-auditors/agents/*.md` | @sm / @po | Create/edit via story |
| `.claude/skills/sa-*/SKILL.md` | @dev (with mentor guidance) | via story |
| `.claude/rules/sa-activation.md` | @architect | via story; path triggers tuned weekly |
| `.claude/hooks/sa-gate-enforcement.cjs` | @devops | via story; hook changes require @qa review |
| `.claude/stack-auditors/journey-log/*.yaml` | runtime (mentors write) | gitignored (runtime state) |
| `squads/stack-auditors/squad.yaml` | @sm / @po | via story |
| `squads/stack-auditors/config/*.md` | @po (persona-catalog) / @architect (others) | via story |
| `scripts/stack-auditors/metrics.sh` | @devops | via story |

---

## Gitignore rules

Add to `.gitignore`:

```
# stack-auditors runtime
.claude/stack-auditors/journey-log/*.yaml
!.claude/stack-auditors/journey-log/_schema.yaml
```

Journey log files are runtime state (generated by invocations) and should not be committed. Schema file IS committed.

---

## Dependencies between files

```
squads/stack-auditors/squad.yaml
  └── references
      ├── agents/*.md           (all 12)
      ├── tasks/*.md            (all 6)
      ├── chains/*.yaml         (all 3)
      ├── checklists/veredict-quality-gate.md
      ├── config/*.md           (all 3)
      └── workflows/stack-auditors-flow.yaml

.claude/agents/sa-*.md
  └── frontmatter references
      ├── .claude/skills/sa-*-*/SKILL.md  (via fundamentation_skill field)
      ├── squads/stack-auditors/agents/sa-*.md (full persona body)
      └── config/persona-catalog.md (relationships)

.claude/hooks/sa-gate-enforcement.cjs
  └── reads
      ├── .claude/stack-auditors/journey-log/*.yaml
      ├── docs/stories/*.story.md (frontmatter)
      └── git diff output

.claude/rules/sa-activation.md
  └── path triggers map to
      └── agents (via squad.yaml routing table)
```

---

## Integration with rest of codebase

Stack-auditors is ORTHOGONAL to AIOX layer. Touches these external paths:

- **Reads:** `docs/stories/*.story.md`, `packages/**`, `hub/**`, `mega-brain/**`, git history
- **Writes:** ONLY `.claude/stack-auditors/journey-log/`, `docs/architecture/adr-sa-*.md` (via doctrine-extraction)
- **Invokes:** AIOX agents unchanged (doesn't modify @dev, @qa, etc.)
- **Invoked by:** AIOX agents via `Agent(subagent_type='sa-*', ...)`

Zero modifications to existing AIOX agents or their tasks.
