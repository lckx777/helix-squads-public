---
description: Sequential debate between 2 mentors in productive tension. Council frames tension, mentors debate N rounds, council synthesizes without flattening.
---

# debate-chain

Sequential debate between 2 mentors in productive tension. Council frames tension, mentors debate N rounds, council synthesizes without flattening.

## Execution

This command triggers the `debate-chain` chain. The canonical chain
definition lives at `chains/debate-chain.yaml` within this plugin.

See the YAML file for detailed step sequence. Execute each step by invoking the specified agent and task in order, passing outputs forward as inputs to subsequent steps.

## Arguments

$ARGUMENTS will be passed as the initial input to step 1.
