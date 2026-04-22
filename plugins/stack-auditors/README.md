# stack-auditors

> This plugin is part of the [Helix Squads Public Marketplace](https://github.com/lckx777/helix-squads-public).

## Quick install

```
claude plugin marketplace add lckx777/helix-squads-public
claude plugin install stack-auditors@helix-squads-public
```

---

# Stack Auditors Squad

> L4 mentor council — celebrity engineers audit high-stakes decisions with evidence-based verdicts.

## What this is

A squad of 12 agents (11 mentors + 1 orchestrator) based on historical computing figures who serve as **L4 auditors** over the AIOX execution layer. They do not implement — they give verdicts grounded in evidence produced by dedicated fundamentation skills.

## Agents

| Agent | Persona | Domain | Fundamentation Skill |
|-------|---------|--------|---------------------|
| `sa-council` | The Council | Routing + synthesis | — (orchestrator) |
| `sa-carmack` | John Carmack | Real-time / performance | `sa-carmack-bench` |
| `sa-van-rossum` | Guido van Rossum | Pythonic idiomatic | `sa-van-rossum-lint` |
| `sa-stonebraker` | Michael Stonebraker | Database architecture | `sa-stonebraker-plan` |
| `sa-torvalds` | Linus Torvalds | Systems / kernel | `sa-torvalds-git` |
| `sa-jobs` | Steve Jobs | Product vision / taste | `sa-jobs-taste` |
| `sa-musk` | Elon Musk | First-principles method | `sa-musk-requirements` |
| `sa-schneier` | Bruce Schneier | Security / threat model | `sa-schneier-threat` |
| `sa-kim` | Gene Kim | DevOps / flow | `sa-kim-flow` |
| `sa-beck` | Kent Beck | TDD / XP | `sa-beck-tdd` |
| `sa-newman` | Sam Newman | Microservices | `sa-newman-services` |
| `sa-norman` | Don Norman | Cognitive UX | `sa-norman-affordance` |

## Architecture — layer respect

```
L4 (WHY + EVIDENCE)   → stack-auditors mentors          [opus, thinking]
L3 (WHAT)             → @architect / @pm                 [existing AIOX]
L2 (HOW)              → @dev / @qa                       [existing AIOX]
L1 (DO)               → Skills sa-* (fundamentation)     [executable code]
```

**Mentors do NOT substitute AIOX agents.** They complement as L4 verdict layer.

## Invocation

### Direct
```
Agent(subagent_type="sa-carmack", prompt="audit hot path in packages/worker-queue/processor.ts")
```

### Via council (recommended)
```
Agent(subagent_type="sa-council", prompt="pre-impl audit story X")
```
The council routes to relevant mentor(s).

### Via commands
```
*audit {target}
*veredict {question}
*doctrine {topic}
*challenge {aiox_agent} {decision}
```

## Auto-activation

- **70% rules** (`.claude/rules/sa-activation.md`): path-triggered advisory
- **30% hooks** (`.claude/hooks/sa-gate-enforcement.cjs`): catastrophic enforcement (git commit + @devops push)

When you touch `packages/vps-api/auth/**`, the rule injects a suggestion to invoke sa-schneier. When you try to push a PR tagged `sa-gate-required: true` without council verdict, the hook blocks.

## Observability

Every mentor invocation is logged in `.claude/stack-auditors/journey-log/{date}.yaml` with schema:

```yaml
invocation:
  id: string
  timestamp: ISO8601
  mentor: sa-{name}
  trigger: rule | hook | explicit
  context_path: string
  skill_invoked: string | null
  verdict: approved | concerns | blocked
  evidence_cited: boolean
  decision_changed: boolean   # ← métrica vital
  latency_ms: integer
  story_ref: string | null
```

### Kill / Expand criteria

| Metric | Threshold | Action |
|--------|-----------|--------|
| `decision_changed` < 10% in 30d | Squad is theater | **MATA** — remove squad |
| `decision_changed` >= 30% in 30d | Squad is adding value | **EXPAND** — scale to v0.2 |
| `decision_changed` between 10-29% | Calibrate | Review rules/mentors |

Run `scripts/stack-auditors/metrics.sh` to compute weekly.

## Workflow patterns

| Pattern | Mode | When to use |
|---------|------|-------------|
| Single-mentor audit | `single-audit` | Pergunta focada num domínio |
| Council parallel | `council-parallel` | Decisão ambígua, múltiplas lentes |
| Debate sequence | `debate-sequence` | Tensão produtiva (Jobs vs Musk, etc.) |
| Pre-implementation audit | `pre-implementation-audit` | Story COMPLEX (>16 points) |
| Post-implementation review | `post-implementation-review` | PR high-stakes antes de @devops push |

## Structure

```
squads/stack-auditors/
├── squad.yaml                  # AIOS 2.1.0 manifest
├── README.md                   # this file
├── _TEMPLATE.md                # canonical template (11 sections)
├── agents/                     # 12 persona bodies
├── tasks/                      # 6 tasks
├── chains/                     # 3 chains YAML
├── checklists/                 # 1 quality gate
├── config/                     # persona-catalog, invocation-rules, source-tree
└── workflows/                  # 1 workflow YAML

.claude/
├── agents/sa-*.md              # 12 native loaders
├── skills/sa-*/                # 11 fundamentation skills
├── rules/sa-activation.md      # auto-activation rule
├── hooks/sa-gate-enforcement.cjs  # catastrophic enforcement
└── stack-auditors/
    ├── README.md               # observability guide
    └── journey-log/            # daily YAML logs
```

## References

- **Persona format:** Hybrid Jobs+Musk (see `_TEMPLATE.md`)
- **AIOS manifest schema:** Based on `squads/cartographer/squad.yaml`
- **Story tracking:** `docs/stories/chore-squad-stack-auditors-v1.story.md`
- **ADR (planned):** `docs/architecture/adr-stack-auditors-layer.md`
- **Alan's consultation** (in-session): validated architecture decisions — layer discipline, skills over agents, 70/30 activation split, day-0 observability

## Status

v1.0 — Under construction. See story file for progress.
# test sync 1776871092
