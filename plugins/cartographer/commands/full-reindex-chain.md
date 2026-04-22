---
description: Full monorepo excavation across all languages — runs weekly or on demand after major changes
---

# full-reindex-chain

Full monorepo excavation across all languages — runs weekly or on demand after major changes

## Execution

This command triggers the `full-reindex-chain` chain. The canonical chain
definition lives at `chains/full-reindex-chain.yaml` within this plugin.

Follow these steps in order:

1. **reindex-announce** — agent: `cart-surveyor`
2. **index-ts-full** — agent: `cart-ts-digger` — task: `index-typescript`
3. **index-py-full** — agent: `cart-py-digger` — task: `index-python`
4. **index-yaml-full** — agent: `cart-yaml-digger` — task: `index-yaml`
5. **index-sql-full** — agent: `cart-sql-digger` — task: `index-sql`
6. **build-full-graph** — agent: `cart-keeper` — task: `build-graph`
7. **generate-health-report** — agent: `cart-oracle` — task: `generate-report`

## Arguments

$ARGUMENTS will be passed as the initial input to step 1.
