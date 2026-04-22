---
task: preImplementationAudit()
name: pre-implementation-audit
description: Pre-implementation block for COMPLEX or XL stories. Forces architecture/security/perf
  lens before code is written.
responsavel: sa-council
responsavel_type: Agente
atomic_layer: Organism
Entrada:
- nome: story_path
  tipo: string
  obrigatorio: true
  descricao: Path to story file (e.g., docs/stories/x.story.md)
- nome: force_mentors
  tipo: array
  obrigatorio: false
  descricao: Specific mentor IDs required regardless of domain routing
Saida:
- nome: council_verdict
  tipo: enum
  obrigatorio: true
  descricao: approved | concerns | blocked
- nome: blocks_implementation
  tipo: boolean
  obrigatorio: true
  descricao: Whether the story may transition to Ready
- nome: per_mentor_verdicts
  tipo: object
  obrigatorio: true
  descricao: Map of mentor ID to verdict + evidence
- nome: required_changes_before_unblock
  tipo: array
  obrigatorio: true
  descricao: Specific changes story must address to unblock
- nome: frontmatter_patch
  tipo: object
  obrigatorio: true
  descricao: Story frontmatter updates (sa-preimpl-verdict, sa-preimpl-date)
Checklist:
- Story frontmatter parsed and domains identified
- Mentor selection covers all touched domains
- Each mentor cited evidence
- Veto rule enforced (any blocked = story cannot enter Ready)
- Story frontmatter patched with sa-preimpl-verdict + sa-preimpl-date
- Journey log entries written
---

# Task: pre-implementation-audit

**Owner:** sa-council (orchestrator)
**Complexity:** L
**Gate:** evidence-required

## Purpose

Bloqueio pre-impl para stories COMPLEX (>16 points OR complexity=XL). Invoked BEFORE @dev starts implementation. Forces architecture/security/perf lens BEFORE code is written.

## Entrada

- `story_path` — path to story file (e.g., `docs/stories/chore-m0-secrets-purge.story.md`)
- `force_mentors` — (optional) specific mentors required regardless of domain routing

## Fluxo

1. **Story analysis (sa-council)** — parse story frontmatter + AC to identify domains touched
2. **Mentor selection** — for each domain, add corresponding mentor:
   - DB → sa-stonebraker
   - Security → sa-schneier
   - Perf → sa-carmack
   - Python → sa-van-rossum
   - Architecture → sa-newman + sa-musk
   - UI → sa-jobs + sa-norman
   - Testing → sa-beck
   - DevOps → sa-kim
3. **Parallel audit (council-audit-parallel subtask)** — invoke all selected mentors
4. **Gate enforcement** — if any mentor `blocked`, story cannot enter Ready status. Return to @pm/@po with specific concerns.
5. **Council synthesis** — write pre-impl verdict to story frontmatter + journey log.
6. **Update story frontmatter** — add `sa-preimpl-verdict: approved | concerns | blocked`

## Saída

```yaml
task: pre-implementation-audit
story_ref: "{story_id}"
mentors_selected: [sa-x, sa-y, ...]
per_mentor_verdicts: {...}
council_verdict: approved | concerns | blocked
blocks_implementation: true | false
required_changes_before_unblock: [...]
frontmatter_patch:
  sa-preimpl-verdict: "{verdict}"
  sa-preimpl-date: "ISO8601"
latency_ms: int
```

## Gates

- **evidence-required:** all mentors cite evidence
- **council-blocks-on-veto:** any mentor `blocked` → implementation cannot start

## Integration with AIOX

Triggered by:
- `.claude/rules/sa-activation.md` when story complexity XL or COMPLEX
- Explicit invocation from @po before validate-story-draft GO

Blocks:
- @dev starting implementation until verdict is `approved` or story updated to address concerns
