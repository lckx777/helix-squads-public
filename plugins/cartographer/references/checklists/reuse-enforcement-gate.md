# Reuse Enforcement Gate Checklist

**Gate:** reuse-enforcement
**Enforcer:** cart-oracle
**Pre-requisite:** graph-integrity PASSED
**Required before:** IDS enforcement goes live

## Checklist

- [ ] `query-log.ndjson` initialized (oracle ready to log queries)
- [ ] `ids-checks.ndjson` initialized
- [ ] At least one IDS check test run produces a structured verdict (not error)
- [ ] REUSE threshold (0.95) and ADAPT threshold (0.75) correctly applied
- [ ] Staleness warning triggers correctly for graphs > 24h old
- [ ] cart-oracle correctly declines to answer business strategy questions (redirect to oracle-supreme-squad)
- [ ] Oracle does NOT write to artifact catalog (read-only enforcement)

## Scoring

**PASS:** All checks pass
**FAIL:** Oracle writes to catalog OR IDS thresholds misconfigured
