---
task: enforceReuse()
responsavel: Cart Oracle
responsavel_type: Agente
atomic_layer: Molecule
workflow: cartographer-query
step: 2
Entrada:
- campo: proposed_artifact
  tipo: string
  obrigatorio: true
  validacao: Description of the artifact the caller wants to create
- campo: proposed_kind
  tipo: enum
  valores:
  - function
  - agent
  - task
  - workflow
  - hook
  - table
  - skill
  - mcp_server
  - package
  obrigatorio: true
- campo: caller_agent
  tipo: string
  obrigatorio: true
  validacao: ID of the agent requesting the check
Saida:
- campo: ids_verdict
  tipo: structured
  destino: response to caller (inline)
  obrigatorio: true
- campo: ids_log
  tipo: file
  destino: squads/cartographer/.run/ids-checks.ndjson
  obrigatorio: true
Checklist:
- '[ ] Graph snapshot age declared'
- '[ ] Exact name/signature match searched'
- '[ ] Keyword similarity search performed'
- '[ ] Similarity score computed for all near-matches'
- '[ ] Recommendation is REUSE, ADAPT, or CREATE (not free-form)'
- '[ ] REUSE: exact artifact path and usage example cited'
- '[ ] ADAPT: nearest artifact path + delta description cited'
- '[ ] CREATE: confirmed no match >= 0.75 similarity'
- '[ ] IDS check logged to ids-checks.ndjson'
description: '- **ID:** enforce-reuse'
---


# Task: Enforce Reuse (IDS Check Before Create)

## Metadata
- **ID:** enforce-reuse
- **Workflow:** cartographer-query
- **Step:** 2
- **Agent:** cart-oracle
- **Read-only:** true
- **Invoked by:** Any agent considering a CREATE operation

## Description
Enforces the IDS (Incremental Development Strategy) principle: REUSE > ADAPT > CREATE.
Called before any agent creates a new artifact. Returns a structured verdict with the
IDS recommendation and supporting evidence.

## Protocol

1. **Declare graph age** (mandatory header)
2. **Exact search**: Look for artifacts matching proposed name and kind
3. **Keyword/semantic search**: Scan descriptions, signatures, names for similarity
4. **Score all candidates**: Cosine similarity (or keyword overlap score pre-embedding)
5. **Classify and return verdict**:

### REUSE (similarity >= 0.95)
- Return exact artifact location, signature, and usage example
- Block CREATE recommendation

### ADAPT (similarity 0.75-0.94)
- Return nearest artifact with description of required delta
- Suggest: "Extend/configure this instead of creating new"

### CREATE (similarity < 0.75)
- Confirm no near-duplicate exists
- Provide: gap description (what's missing from existing catalog)
- GREEN LIGHT to create

## Response Format
```yaml
graph_snapshot: "2026-04-16T10:00:00Z"
graph_age: "0h 15m"
caller_agent: "aiox-dev"
proposed: "hook that validates gate state before tool execution"
proposed_kind: hook
verdict: ADAPT
confidence: 0.82
similar_artifacts:
  - id: "py:hook:gate-enforcement"
    kind: hook
    name: gate-enforcement.cjs
    file_path: ".claude/hooks/gate-enforcement.cjs"
    hook_event: PreToolUse
    similarity_score: 0.82
    reason: "Existing hook checks gate state pre-execution — may need extension rather than new hook"
recommendation: |
  Adapt gate-enforcement.cjs — add your specific gate condition as a new rule
  rather than creating a separate hook for the same lifecycle event.
  See: .claude/hooks/gate-enforcement.cjs
```

## Logging
Every IDS check is appended to `.run/ids-checks.ndjson`:
```json
{
  "timestamp": "2026-04-16T10:15:00Z",
  "caller_agent": "aiox-dev",
  "proposed": "...",
  "verdict": "ADAPT",
  "similarity_score": 0.82,
  "artifact_cited": "py:hook:gate-enforcement"
}
```
