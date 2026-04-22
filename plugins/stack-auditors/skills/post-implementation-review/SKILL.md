---
task: postImplementationReview()
name: post-implementation-review
description: 'Post-QA review for high-stakes PRs before @devops push. Complements
  @qa: validates architecture/security/perf/UX rather than correctness.'
responsavel: sa-council
responsavel_type: Agente
atomic_layer: Organism
Entrada:
- nome: pr_number
  tipo: integer
  obrigatorio: false
  descricao: GitHub PR number (optional if running locally)
- nome: branch
  tipo: string
  obrigatorio: false
  descricao: Branch to review, default current
- nome: base_ref
  tipo: string
  obrigatorio: false
  descricao: Baseline ref, default main
- nome: high_stakes_criteria
  tipo: object
  obrigatorio: false
  descricao: Override for default high-stakes detection rules
Saida:
- nome: council_verdict
  tipo: enum
  obrigatorio: true
  descricao: approved | concerns | blocked
- nome: per_mentor_verdicts
  tipo: object
  obrigatorio: true
  descricao: Map of mentor ID to verdict + line refs + evidence
- nome: pr_comment_posted
  tipo: boolean
  obrigatorio: true
  descricao: Whether the review comment was posted via gh pr review
- nome: pr_label_applied
  tipo: enum
  obrigatorio: true
  descricao: sa-reviewed-approved | sa-reviewed-concerns | sa-reviewed-blocked
- nome: files_changed
  tipo: integer
  obrigatorio: true
  descricao: Count of files changed in PR
Checklist:
- PR diff analyzed and domains identified
- Mentors selected based on actual changes (not story plan)
- All mentors cited evidence
- PR not merged before review (won't review merged PRs)
- Hook .claude/hooks/sa-gate-enforcement.cjs blocks merge on blocked verdict
---

# Task: post-implementation-review

**Owner:** sa-council (orchestrator)
**Complexity:** M
**Gate:** evidence-required

## Purpose

Pós-QA review para PRs high-stakes antes de @devops push. Complementa @qa — não substitui. @qa valida correctness; mentores validam arquitetura/segurança/perf/UX.

## Entrada

- `pr_number` — GitHub PR number (optional if running locally)
- `branch` — branch to review (default: current)
- `base_ref` — baseline (default: `main`)
- `high_stakes_criteria` — (optional) override default criteria

## Default high-stakes criteria

PR é high-stakes se qualquer um:
- Toca paths security-critical (`packages/vps-api/auth/**`, etc.)
- >500 lines changed
- >5 files changed across >2 packages
- Has migrations (`packages/**/migrations/**`)
- Changes public API (exports alterados)
- Has `sa-review-required: true` in PR description

## Fluxo

1. **Diff analysis (sa-council)** — `git diff base_ref...HEAD` to identify files + domains touched
2. **Mentor selection** — same rules as pre-implementation-audit, but focused on ACTUAL changes (not story plan)
3. **Parallel review (council-audit-parallel subtask)**
4. **Review comment generation** — formatted as PR comment with:
   - Summary of verdicts
   - Per-mentor findings with line refs
   - Required changes (if `blocked` or `concerns`)
5. **Post to PR** — if `pr_number` given, post review comment via `gh pr review`
6. **Update PR status** — add label `sa-reviewed` (approved/concerns/blocked)

## Saída

```yaml
task: post-implementation-review
pr_ref: "#{pr_number}"
branch: "{branch}"
base_ref: "{base_ref}"
files_changed: int
loc_changed: int
mentors_selected: [...]
per_mentor_verdicts: {...}
council_verdict: approved | concerns | blocked
pr_comment_posted: bool
pr_label_applied: "sa-reviewed-approved" | "sa-reviewed-concerns" | "sa-reviewed-blocked"
latency_ms: int
```

## Gates

- **evidence-required:** all mentors cite evidence
- **pr-not-merged-yet:** won't review already-merged PRs

## Blocks

If verdict = `blocked`:
- Hook `.claude/hooks/sa-gate-enforcement.cjs` blocks `gh pr merge` until human override or concerns resolved
- PR label `sa-reviewed-blocked` added

## Complementary to @qa

| Domain | @qa (Quinn) | stack-auditors |
|--------|-------------|----------------|
| Acceptance criteria | ✓ | — |
| Unit tests | ✓ | — |
| No regressions | ✓ | — (tangential) |
| Code quality / patterns | ✓ | sa-beck validates TDD discipline |
| Security | basic | sa-schneier threat model |
| Performance | basic | sa-carmack perf evidence |
| Architecture | — | sa-newman + sa-musk |
| UX | — | sa-jobs + sa-norman |
