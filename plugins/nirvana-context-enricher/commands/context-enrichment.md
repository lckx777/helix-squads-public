---
description: Decomposes the parallel research step into 4 micro-tasks — 3 parallel researcher dispatches and a barrier validator — with explicit handoffs and gate checks per Constitution Art. VII
---

# context-enrichment

Decomposes the parallel research step into 4 micro-tasks — 3 parallel researcher dispatches and a barrier validator — with explicit handoffs and gate checks per Constitution Art. VII

## Execution

This command triggers the `context-enrichment` chain. The canonical chain
definition lives at `chains/context-enrichment.yaml` within this plugin.

See the YAML file for detailed step sequence. Execute each step by invoking the specified agent and task in order, passing outputs forward as inputs to subsequent steps.

## Arguments

$ARGUMENTS will be passed as the initial input to step 1.
