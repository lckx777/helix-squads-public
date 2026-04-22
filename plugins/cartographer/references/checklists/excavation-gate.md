# Excavation Gate Checklist

**Gate:** excavation
**Enforcer:** cart-surveyor
**Pre-requisite:** none
**Required before:** build-graph

## Checklist

- [ ] All diggers that were scheduled for this run have completed (no hanging/failed runs)
- [ ] Each digger's NDJSON output file exists in `.run/digger-output/`
- [ ] NDJSON files are non-empty OR digger explicitly reported zero-artifact scope
- [ ] Each artifact record is valid JSON (no parse errors)
- [ ] All artifact IDs use correct prefix (`ts:`, `py:`, `yaml:`, `sql:`)
- [ ] No duplicate artifact IDs within a single digger's output
- [ ] `last-hashes.json` updated by all diggers that ran
- [ ] Run metadata YAML written by each digger that ran
- [ ] Language boundary not crossed (TS digger has no `.py` file paths, etc.)

## Scoring

| Check | Weight |
|-------|--------|
| All diggers completed | REQUIRED |
| NDJSON files exist and readable | REQUIRED |
| Zero JSON parse errors | REQUIRED |
| Correct ID prefixes | REQUIRED |
| last-hashes.json updated | MUST |
| Run metadata written | MUST |
| Language boundary respected | MUST |

**PASS:** All REQUIRED checks pass + >= 2 MUST checks
**FAIL:** Any REQUIRED check fails
