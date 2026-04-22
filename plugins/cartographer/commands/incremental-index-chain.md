---
description: Hash-gated incremental excavation — only re-parses changed files, then updates graph
---

# incremental-index-chain

Hash-gated incremental excavation — only re-parses changed files, then updates graph

## Execution

This command triggers the `incremental-index-chain` chain. The canonical chain
definition lives at `chains/incremental-index-chain.yaml` within this plugin.

Follow these steps in order:

1. **detect-changes** — agent: `cart-surveyor`
2. **index-ts** — agent: `cart-ts-digger` — task: `index-typescript`
3. **index-py** — agent: `cart-py-digger` — task: `index-python`
4. **index-yaml** — agent: `cart-yaml-digger` — task: `index-yaml`
5. **index-sql** — agent: `cart-sql-digger` — task: `index-sql`
6. **build-graph** — agent: `cart-keeper` — task: `build-graph`

## Arguments

$ARGUMENTS will be passed as the initial input to step 1.
