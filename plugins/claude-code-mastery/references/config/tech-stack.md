# Tech Stack — Claude Code Mastery Squad

## Visão Geral

Este documento descreve a stack tecnológica do Claude Code Mastery Squad, especializado em configurar, estender e integrar o Claude Code como plataforma de desenvolvimento assistido por IA.

---

## Runtime e Ambiente

| Componente | Versão/Requisito | Notas |
|------------|------------------|-------|
| **Node.js** | 18+ | Runtime para scripts de validação e automação |
| **Claude Code CLI** | Latest | Plataforma central — atualizar sempre |
| **AIOX Core** | >= 2.1.0 | Framework base do ecossistema |
| **npm** | 9+ | Gerenciador de pacotes |
| **Git** | 2.30+ | Controle de versão |

---

## Claude Code — Funcionalidades Utilizadas

O CCM domina e configura cada feature nativa do Claude Code:

| Feature | Uso no Squad | Agente Responsável |
|---------|--------------|--------------------|
| **Custom Agents** | 8 agentes especializados via `.claude/agents/` | `claude-mastery-chief` |
| **Skills** | Criação e validação de skills em `.claude/skills/` | `skill-craftsman` |
| **Teams** | Topologias multi-agente paralelas | `swarm-orchestrator` |
| **Hooks** | Pre/post-tool, pre/post-turn hooks | `hooks-architect` |
| **Rules** | `.claude/rules/` com frontmatter `paths:` | `config-engineer` |
| **Memory** | `MEMORY.md` por agente para persistência cross-session | `config-engineer` |
| **MCP Servers** | Integração e gestão de servidores MCP | `mcp-integrator` |
| **CLAUDE.md** | Templates para fullstack, monorepo, mobile, etc. | `project-integrator` |
| **Permissions** | `settings.json` allow/deny rules | `config-engineer` |
| **Worktrees** | Estratégias para repos multi-worktree | `swarm-orchestrator` |

---

## Formatos e Especificações

| Especificação | Versão | Aplicação |
|---------------|--------|-----------|
| **AGENT-PERSONALIZATION-STANDARD** | V1 | Definição de todos os agentes |
| **TASK-FORMAT-SPECIFICATION** | V1 | Definição de todas as tasks |
| **AIOX Constitution** | Current | Gates de qualidade obrigatórios |

---

## MCP Servers

### Servidores Utilizados pelo CCM

| Servidor | Propósito | Tipo de Acesso |
|----------|-----------|----------------|
| **context7** | Documentação de bibliotecas em tempo real (Claude Code docs, Node.js, etc.) | Deferred (Tool Search) |
| **playwright** | Testes de browser, validação de UI gerada | Direto (global) |

### Padrão de Uso

```yaml
# context7 — documentação de libraries
mcp__context7__resolve-library-id("claude-code")
mcp__context7__query-docs(topic: "hooks configuration")

# playwright — validação de interfaces
mcp__playwright__browser_navigate(url: "http://localhost:3000")
mcp__playwright__browser_snapshot()
```

---

## Quality Gates — Constituição AIOX

Todo artefato CCM deve passar pelos 6 artigos constitucionais:

| Artigo | Nome | Aplicação no CCM |
|--------|------|-----------------|
| **I** | CLI First | Toda configuração funciona 100% via CLI antes de qualquer UI |
| **II** | Agent Authority | CCM chief orquestra; especialistas têm autoridade exclusiva em seu domínio |
| **III** | Story-Driven | Mudanças de configuração partem de stories documentadas |
| **IV** | No Invention | Configurações rastreadas a requisitos ou padrões oficiais Claude Code |
| **V** | Quality First | Checklists obrigatórios: `change-checklist.md`, `pre-push-checklist.md` |
| **VI** | Absolute Imports | Paths absolutos em CLAUDE.md e configurações de projeto |

---

## Integração com CI/CD

| Template | Propósito |
|----------|-----------|
| `github-actions-claude-ci.yml` | Pipeline CI com validação Claude Code |
| `github-actions-claude-review.yml` | Review automático via Claude em PRs |

---

## Compatibilidade

| Plataforma | Suporte | Notas |
|------------|---------|-------|
| macOS | Completo | Ambiente primário |
| Linux | Completo | CI/CD e VPS |
| Windows (WSL2) | Completo | Via WSL2 |
| Windows (nativo) | Parcial | Hooks bash requerem adaptação |
