# claude-code-mastery

> This plugin is part of the [Helix Squads Public Marketplace](https://github.com/lckx777/helix-squads-public).

## Quick install

```
claude plugin marketplace add lckx777/helix-squads-public
claude plugin install claude-code-mastery@helix-squads-public
```

---

# Claude Code Mastery Squad

> Full-spectrum expertise in Claude Code: hooks, skills, subagents, MCP, plugins, agent teams, customization, integration, and roadmap awareness.

**Version:** 1.0.0 | **Created:** 2026-03-01 | **Total:** 8 agents, 6,741 lines

## Squad Architecture

```
                        Orion (Orchestrator)
                     claude-mastery-chief [Tier 0]
                              |
            ┌─────────┬───────┴───────┬──────────┐
            |         |               |          |
    ┌───────┴──┐  ┌───┴────┐  ┌──────┴───┐  ┌───┴──────┐
    |  Latch   |  | Piper  |  |  Nexus   |  |  Sigil   |
    |  Hooks   |  |  MCP   |  |  Swarm   |  |  Config  |
    | Tier 1   |  | Tier 1 |  |  Tier 1  |  |  Tier 1  |
    └──────────┘  └────────┘  └──────────┘  └──────────┘
            |         |               |
    ┌───────┴──┐  ┌───┴────┐  ┌──────┴───┐
    |  Anvil   |  | Conduit|  |  Vigil   |
    |  Skills  |  | Project|  | Roadmap  |
    | Tier 2   |  | Tier 2 |  |  Tier 2  |
    └──────────┘  └────────┘  └──────────┘
```

## Agents

| Tier | Agent | Persona | Based On | Lines | Focus |
|------|-------|---------|----------|-------|-------|
| 0 | claude-mastery-chief | Orion | Original | 554 | Triage, routing, cross-cutting knowledge |
| 1 | hooks-architect | Latch | disler (IndyDevDan) | 1,013 | 17 hook events, automation, damage control |
| 1 | mcp-integrator | Piper | Peter Steinberger (@steipete) | 791 | MCP servers, tool discovery, context budget |
| 1 | swarm-orchestrator | Nexus | Kieran Klaassen + Reuven Cohen | 1,008 | Agent teams, subagents, parallel execution |
| 1 | config-engineer | Sigil | SuperClaude-Org | 663 | Settings, permissions, CLAUDE.md, sandbox |
| 2 | skill-craftsman | Anvil | BMAD-CODE-ORG | 1,046 | Skills, plugins, commands, context engineering |
| 2 | project-integrator | Conduit | Daniel Miessler (PAI) | 959 | Project integration, CI/CD, AIOX bridge |
| 2 | roadmap-sentinel | Vigil | Boris Cherny | 707 | Roadmap, changelog, feature adoption |

## Quick Start

### Activate the Orchestrator
```
@claude-code-mastery:claude-mastery-chief
```
Or use the AIOX activation:
```
/AIOX:agents:claude-mastery-chief
```

### Direct Specialist Access
```
/AIOX:agents:hooks-architect        # Hook automation
/AIOX:agents:mcp-integrator         # MCP servers
/AIOX:agents:swarm-orchestrator     # Multi-agent orchestration
/AIOX:agents:config-engineer        # Settings & permissions
/AIOX:agents:skill-craftsman        # Skills & plugins
/AIOX:agents:project-integrator     # Project integration
/AIOX:agents:roadmap-sentinel       # Updates & roadmap
```

## Feature Coverage

| Claude Code Feature | Specialist | Key Commands |
|-------------------|-----------|-------------|
| Hooks (17 events) | Latch | `*create-hook`, `*audit-hooks`, `*hook-patterns` |
| MCP Integration | Piper | `*add-server`, `*audit-mcp`, `*create-mcp-server` |
| Subagents & Teams | Nexus | `*create-agent`, `*create-team`, `*orchestrate` |
| Settings & Permissions | Sigil | `*configure`, `*permission-strategy`, `*sandbox-setup` |
| Skills & Plugins | Anvil | `*create-skill`, `*create-plugin`, `*context-strategy` |
| Project Integration | Conduit | `*integrate-project`, `*brownfield-setup`, `*ci-cd-setup` |
| Roadmap & Updates | Vigil | `*update-knowledge`, `*feature-radar`, `*migration-guide` |
| AIOX Bridge | Orion + Conduit | `*aiox-bridge`, `*aiox-guide` |

## Elite Minds Research Attribution

This squad was created through iterative research with devil's advocate validation (3 iterations). Each agent is based on real people/projects with documented frameworks:

| Mind | Contribution | Source |
|------|-------------|--------|
| **disler** (IndyDevDan) | Hooks Mastery framework, meta-agent patterns, damage control | [GitHub](https://github.com/disler/claude-code-hooks-mastery) |
| **Peter Steinberger** (@steipete) | claude-code-mcp, multi-instance workflow, CLI-first philosophy | [Blog](https://steipete.me/), [GitHub](https://github.com/steipete/claude-code-mcp) |
| **Kieran Klaassen** | TeammateTool discovery, swarm patterns documentation | [Gists](https://gist.github.com/kieranklaassen) |
| **Reuven Cohen** (ruvnet) | Ruflo orchestration platform, 54+ agents, WASM kernels | [GitHub](https://github.com/ruvnet/ruflo) |
| **SuperClaude-Org** | 9 cognitive personas, 5 behavioral modes, pure .md config | [GitHub](https://github.com/SuperClaude-Org/SuperClaude_Framework) |
| **BMAD-CODE-ORG** | BMAD Method, 21 agents, 50+ workflows, spec-driven development | [Docs](https://docs.bmad-method.org/) |
| **Daniel Miessler** | Personal AI Infrastructure (PAI), Unix philosophy for AI | [Blog](https://danielmiessler.com/), [GitHub](https://github.com/danielmiessler/Personal_AI_Infrastructure) |
| **Boris Cherny** | Claude Code creator, plan-first methodology, parallel instances | [Blog](https://boristane.com/), [Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/how-claude-code-is-built) |

## AIOX-Core Integration

This squad understands both Claude Code native capabilities AND the AIOX-core framework:

| AIOX Concept | Claude Code Equivalent | Bridge Agent |
|-------------|----------------------|-------------|
| Agents (@dev, @qa...) | Subagents (.claude/agents/) | Nexus |
| Tasks (framework development tasks) | Skills (.claude/skills/) | Anvil |
| Workflows | Multi-step sessions | Nexus + Orion |
| core-config.yaml | .claude/settings.json | Sigil |
| Python hooks (monitor/) | Native hooks (command/http/prompt/agent) | Latch |
| Quality gates | Hook-based validation | Latch + Sigil |
| Entity registry | Tool Search + MCP registry | Piper |

## Directory Structure

```
squads/claude-code-mastery/
├── config.yaml                    # Squad configuration and tier architecture
├── README.md                      # This file
├── agents/
│   ├── claude-mastery-chief.md    # Tier 0: Orchestrator (Orion)
│   ├── hooks-architect.md         # Tier 1: Hooks (Latch)
│   ├── mcp-integrator.md          # Tier 1: MCP (Piper)
│   ├── swarm-orchestrator.md      # Tier 1: Subagents/Teams (Nexus)
│   ├── config-engineer.md         # Tier 1: Settings/Config (Sigil)
│   ├── skill-craftsman.md         # Tier 2: Skills/Plugins (Anvil)
│   ├── project-integrator.md      # Tier 2: Integration (Conduit)
│   └── roadmap-sentinel.md        # Tier 2: Roadmap (Vigil)
├── tasks/                         # Squad-specific tasks
├── workflows/                     # Multi-phase workflows
├── templates/                     # Output templates
├── data/                          # Reference data
├── scripts/                       # Utility scripts
└── outputs/
    └── minds/                     # Mind DNA extractions
```

## Quality Metrics

| Metric | Value |
|--------|-------|
| Total agents | 8 |
| Total lines | 6,741 |
| Avg lines/agent | 843 |
| Tier 0 coverage | 1 orchestrator |
| Tier 1 coverage | 4 core specialists |
| Tier 2 coverage | 3 strategic specialists |
| Minds cloned | 8 (from 7 distinct sources) |
| Research iterations | 3 (with devil's advocate) |
| Naming collisions fixed | 2 (Piper, Sigil) |

---

*Claude Code Mastery Squad v1.0 — Created by Squad Architect*
*Philosophy: "Master the tool to master the craft."*
