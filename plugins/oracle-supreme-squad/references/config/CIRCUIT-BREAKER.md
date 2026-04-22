# Oracle Supreme Squad Circuit Breaker

## Triggers
- oracle-critic rejects same output 3x → HALT, escalate for human review
- LSP server unavailable → DEGRADE to grep-based analysis with WARNING
- Knowledge graph inconsistency detected → FREEZE writes, audit required

## Recovery
- On rejection loop: change analysis strategy, broaden context
- On LSP failure: restart language server, fallback to text search
- On graph inconsistency: rollback to last verified checkpoint
