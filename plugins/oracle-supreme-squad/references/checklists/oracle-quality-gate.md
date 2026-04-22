# Oracle Quality Gate

## Pre-Execution
- [ ] Input context is sufficient for analysis depth requested
- [ ] Previous knowledge graph state is loaded and verified
- [ ] LSP server is responsive (if code analysis required)

## Execution
- [ ] All findings cite file:line evidence
- [ ] Confidence levels assigned to each recommendation
- [ ] No hallucinated file paths or function names

## Post-Execution
- [ ] oracle-critic has reviewed and approved output
- [ ] Knowledge graph updated with new learnings (if applicable)
- [ ] Output matches the declared output contract schema
