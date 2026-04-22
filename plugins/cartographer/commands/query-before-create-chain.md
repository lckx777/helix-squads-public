---
description: IDS enforcement chain — query oracle before any CREATE operation
---

# query-before-create-chain

IDS enforcement chain — query oracle before any CREATE operation

## Execution

This command triggers the `query-before-create-chain` chain. The canonical chain
definition lives at `chains/query-before-create-chain.yaml` within this plugin.

Follow these steps in order:

1. **ids-check** — agent: `cart-oracle` — task: `enforce-reuse`

## Arguments

$ARGUMENTS will be passed as the initial input to step 1.
