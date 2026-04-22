# Coding Standards — Nirvana Context Enricher

Adapted to the NCE domain (parallel research + synthesis). These standards apply to squad-level scripts, chain validators, and any utility code under `scripts/`.

## Runtime & Language

- **Node.js ≥ 18**, **npm ≥ 9** (matches root `package.json` engines)
- **ES2022 syntax** with **CommonJS modules** (`require` / `module.exports`) — aligns with host project conventions
- Zero external dependencies unless explicitly approved — prefer Node.js stdlib

## Formatting

| Rule | Value |
|------|-------|
| Indentation | 2 spaces |
| Quotes | Single quotes for strings |
| Semicolons | Required |
| Line endings | LF |
| Trailing whitespace | Forbidden |
| Max line length | 100 characters (soft limit) |

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Files | kebab-case | `coverage-validator.cjs` |
| Variables / functions | camelCase | `parseFindingsHeader` |
| Constants | SCREAMING_SNAKE_CASE | `MIN_TOTAL_SEARCHES` |
| Classes (if any) | PascalCase | `QuorumEvaluator` |
| Chain identifiers | kebab-case | `context-enrichment` |
| Workflow names | snake_case | `context_enrichment_pipeline` |
| Agent IDs | kebab-case | `nirva`, `sage`, `scout`, `scholar`, `lotus` |
| Task identifiers | camelCase() | `validateCoverageQuorum()` |

## File Structure

- Chain validators: `.cjs` extension, single entry point, `main()` function
- Exit codes: `0` for pass, `1` for gate failure, `2` for parse/IO error
- Read from `.nce/findings/` via `fs.readFileSync`
- Write to `.nce/*.jsonl` via `fs.appendFileSync` (append-only)

## Error Handling

Wrap all IO and parsing in `try/catch` with descriptive errors:

```javascript
try {
  const content = fs.readFileSync(findingsPath, 'utf8');
  return parseFrontmatter(content);
} catch (error) {
  const message = `Failed to parse findings file at ${findingsPath}: ${error.message}`;
  process.stderr.write(message + '\n');
  process.exit(2);
}
```

## Logging

- All structured logs go to `.nce/*.jsonl` (JSON Lines format — one JSON object per line)
- Human-readable progress goes to stderr, never stdout (stdout is reserved for exit-condition metadata)
- Every log entry MUST include: `run_id`, `timestamp_iso`, `event`, domain-specific fields

## Agent Prompts (Persona Files)

- Markdown files with top YAML block + content sections (AIOS Agent Personalization Standard V1)
- Greeting levels MUST start with the agent's icon emoji
- Responsibility boundaries are explicit — every agent declares what it handles AND what it delegates
- Persona tone aligned with archetype:
  - `Flow_Master` → `pragmatic`
  - `Builder` → `pragmatic` or `analytical`
  - `Guardian` → `analytical`
  - `Balancer` → `collaborative`

## YAML Rules

- `description` fields MUST be inline strings (`description: "..."`) — NEVER use multi-line (`|` or `>`) blocks. The AIOS parser does not handle multi-line here
- YAML keys in snake_case for workflow/chain fields; kebab-case for IDs
- Quote all booleans declared as `yes/no` context (always use `true`/`false`)

## Commit Hygiene (when squad-level changes ship)

- Scope: `feat(nce): ...`, `fix(nce): ...`, `docs(nce): ...`
- Reference issue/story in body when available
- @devops owns all git push and PR creation per Constitution Art. II

## Test Philosophy

- Unit tests for `scripts/coverage-validator.cjs` are mandatory before the squad is considered GA
- Tests live under `tests/nirvana-context-enricher/` (project-level convention)
- No mocks for filesystem operations on findings — use real fixture files under `tests/nirvana-context-enricher/fixtures/`
