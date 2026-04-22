# Helix Squads — Public Marketplace

Infrastructure and meta-tooling squads distributed as Claude Code plugins.
Zero configuration: install and go.

## Install

```
claude plugin marketplace add lckx777/helix-squads-public
claude plugin install <plugin-name>@helix-squads-public
```

After install, list available plugins:

```
claude plugin marketplace update helix-squads-public
claude plugin list
```

## Plugins

| Plugin | Purpose | Version |
|--------|---------|---------|
| `cartographer` | Ecosystem archaeology — REUSE > ADAPT > CREATE | 1.0.0 |
| `claude-code-mastery` | Claude Code full-spectrum expertise (hooks, skills, MCP, plugins) | 1.0.0 |
| `incident-response-squad` | DevOps/SRE incident response — logs, RCA, runbooks, post-mortems | 1.0.0 |
| `nirvana-context-enricher` | Parallel multi-agent context enrichment for architectural briefings | 1.0.0 |
| `nirvana-squad-creator` | Generate AIOS squads from natural language (9-phase pipeline) | 1.0.0 |
| `oracle-supreme-squad` | Extract DNA of Claude Code — transcendent meta-analysis squad | 4.0.0 |
| `stack-auditors` | Celebrity-engineer mentor council for L4 evidence-based audits | 1.0.0 |
| `synthetic-intelligence-factory` | Meta-system to manufacture synthetic intelligences from any domain | 1.2.0 |

## How plugins work

Each plugin namespaces its skills: `/plugin-name:skill-name`. Agents keep their
original names but are scoped per-plugin. See the Claude Code plugin docs:
<https://code.claude.com/docs/en/plugins>.

Typical invocations after install:

```
# Skills (model-invoked via natural language in a session)
"Use the stack-auditors council to audit my architecture decision"
"Run cartographer to detect drift in my repository"

# Slash commands
/stack-auditors:single-audit-chain
/cartographer:detect-drift
```

## Source of truth

Plugins here are generated from the maintainer's SoT at
`~/.claude/skills/squads/squads/<name>/` via
`scripts/convert-squad-to-plugin.py`. See `AGENTS.md` for the maintenance
flow.

## Statistics

- **8 plugins**
- **57 agents**
- **74 skills**
- **8 slash commands**
- **3.2 MB** total install size
- **End-to-end validated** — each plugin installs and loads correctly in
  Claude Code 2.1.117+.

## Validation

This marketplace passes:

- `python3 scripts/validate-plugins.py` (custom schema checks)
- `claude plugin validate .` (official CLI validator)
- End-to-end install test via `claude plugin install <name>@helix-squads-public`

## License

MIT. See `LICENSE`.
