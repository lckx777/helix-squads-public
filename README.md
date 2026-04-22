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
claude plugin marketplace info helix-squads-public
```

## Plugins

This marketplace hosts the following squads (status column shows which are
already migrated from the source-of-truth at `~/.claude/skills/squads/squads/`):

| Plugin | Purpose | Agents | Status |
|--------|---------|-------:|--------|
| `stack-auditors` | Celebrity-engineer mentor council for L4 audit | 12 | ✅ v1.0.0 |
| `cartographer` | Ecosystem archaeology — IDS (REUSE > ADAPT > CREATE) | 7 | 🚧 planned |
| `claude-code-mastery` | Claude Code full-spectrum expertise (hooks, skills, MCP) | 8 | 🚧 planned |
| `incident-response-squad` | DevOps/SRE incident response | 5 | 🚧 planned |
| `synthetic-intelligence-factory` | Meta-system for synthetic expertise extraction | 6 | 🚧 planned |
| `nirvana-squad-creator` | Squad generator from natural language | 9 | 🚧 planned |
| `nirvana-context-enricher` | Parallel multi-agent context enrichment | 5 | 🚧 planned |
| `oracle-supreme-squad` | Claude Code DNA extraction | 5 | 🚧 planned |

## How it works

Each plugin is a self-contained directory under `plugins/` with its own
`.claude-plugin/plugin.json` manifest, agents, skills, commands, and workflows.

The `marketplace.json` at the repo root lists all available plugins with
their metadata and `source: "./plugins/<name>"` relative paths.

When Claude Code installs a plugin, it copies that directory to a local cache
and namespaces the skills (e.g., `/stack-auditors:audit` instead of `/audit`)
to prevent conflicts.

## Source of Truth

The canonical squads live at `~/.claude/skills/squads/squads/` on the
maintainer's machine. This marketplace is generated from there via
`scripts/sync-from-sot.sh` and validated by CI before release.

## Companion marketplace

See [`helix-squads-private`](https://github.com/lckx777/helix-squads-private)
for proprietary squads (copy-chief, brandcraft-nirvana, content-radar, etc.).
That marketplace requires authentication; this one is zero-config.

## License

MIT — see LICENSE.
