---
description: Oracle insight pipeline: scan codebase, predict patterns, validate findings, implement improvements
---

# oracle-insight-chain

Oracle insight pipeline: scan codebase, predict patterns, validate findings, implement improvements

## Execution

This command triggers the `oracle-insight-chain` chain. The canonical chain
definition lives at `chains/oracle-insight-chain.yaml` within this plugin.

See the YAML file for detailed step sequence. Execute each step by invoking the specified agent and task in order, passing outputs forward as inputs to subsequent steps.

## Arguments

$ARGUMENTS will be passed as the initial input to step 1.
