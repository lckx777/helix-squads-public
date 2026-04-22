# Source Tree — Claude Code Mastery Squad

## Visão Geral

Mapa completo da estrutura do Claude Code Mastery Squad, incluindo propósito de cada componente e relações entre agentes, tasks e workflows.

---

## Estrutura Completa

```
squads/claude-code-mastery/
│
├── squad.yaml                            # Manifesto do squad
├── config.yaml                           # Configuração interna do squad
├── README.md                             # Documentação principal (PT-BR)
├── CHANGELOG.md                          # Histórico de mudanças
│
├── agents/                               # 8 agentes especializados
│   ├── claude-mastery-chief.md           # Orquestrador — roteia e coordena
│   ├── config-engineer.md                # Engenheiro de configuração Claude Code
│   ├── hooks-architect.md                # Arquiteto de hooks e automações
│   ├── mcp-integrator.md                 # Integrador de MCP servers
│   ├── project-integrator.md             # Integrador de projetos existentes
│   ├── roadmap-sentinel.md               # Vigilante do roadmap Claude Code
│   ├── skill-craftsman.md                # Criador de skills e agentes
│   └── swarm-orchestrator.md             # Orquestrador de swarms multi-agente
│
├── tasks/                                # 26 tasks executáveis
│   ├── audit-integration.md              # Auditoria de integrações ativas
│   ├── audit-settings.md                 # Auditoria de settings.json e permissões
│   ├── audit-setup.md                    # Auditoria completa de setup Claude Code
│   ├── brownfield-setup.md               # Configuração em projetos existentes
│   ├── ci-cd-setup.md                    # Setup de CI/CD com Claude Code
│   ├── claude-md-engineer.md             # Engenharia de CLAUDE.md customizado
│   ├── configure-claude-code.md          # Configuração inicial do Claude Code
│   ├── context-rot-audit.md              # Auditoria de degradação de contexto
│   ├── create-agent-definition.md        # Criação de agent definition file
│   ├── create-rules.md                   # Criação de rules contextuais
│   ├── create-team-topology.md           # Design de topologia de equipe multi-agente
│   ├── diagnose.md                       # Diagnóstico de problemas de configuração
│   ├── enterprise-config.md              # Configuração para ambientes enterprise
│   ├── hook-designer.md                  # Design e implementação de hooks
│   ├── integrate-project.md              # Integração de projeto externo
│   ├── mcp-integration-plan.md           # Planejamento de integrações MCP
│   ├── mcp-workflow.md                   # Workflow com ferramentas MCP
│   ├── multi-project-setup.md            # Setup para múltiplos projetos
│   ├── optimize-context.md               # Otimização de janela de contexto
│   ├── optimize-workflow.md              # Otimização de fluxo de trabalho
│   ├── parallel-decomposition.md         # Decomposição de tarefas paralelas
│   ├── permission-strategy.md            # Estratégia de permissões e deny rules
│   ├── sandbox-setup.md                  # Setup de ambiente sandbox
│   ├── setup-repository.md               # Configuração de repositório
│   ├── setup-wizard.md                   # Wizard interativo de configuração
│   └── worktree-strategy.md              # Estratégia de git worktrees
│
├── workflows/                            # 3 workflows orquestrados
│   ├── wf-audit-complete.yaml            # Auditoria completa (settings + integration + context)
│   ├── wf-knowledge-update.yaml          # Atualização de knowledge base do squad
│   └── wf-project-setup.yaml            # Setup completo de novo projeto
│
├── checklists/                           # 7 checklists de qualidade
│   ├── agent-team-readiness-checklist.md # Prontidão para operação multi-agente
│   ├── brownfield-readiness-checklist.md # Prontidão para integração brownfield
│   ├── change-checklist.md               # Pré-mudança de configuração
│   ├── context-rot-checklist.md          # Verificação de degradação de contexto
│   ├── integration-audit-checklist.md    # Auditoria de integrações MCP
│   ├── multi-agent-review-checklist.md   # Review de topologia multi-agente
│   └── pre-push-checklist.md             # Verificações pré-push
│
├── templates/                            # 7 templates CLAUDE.md por tipo de projeto
│   ├── claude-md-fullstack.md            # CLAUDE.md para projetos fullstack
│   ├── claude-md-library.md              # CLAUDE.md para bibliotecas
│   ├── claude-md-microservices.md        # CLAUDE.md para microserviços
│   ├── claude-md-mobile.md               # CLAUDE.md para apps mobile
│   └── claude-md-monorepo.md             # CLAUDE.md para monorepos
│   (+ 2 adicionais)
│
├── data/                                 # 5 catálogos e referências
│   ├── ci-cd-patterns.yaml               # Padrões de CI/CD reutilizáveis
│   ├── claude-code-quick-ref.yaml        # Referência rápida de features
│   ├── hook-patterns.yaml                # Catálogo de padrões de hooks
│   ├── mcp-integration-catalog.yaml      # Catálogo de MCPs disponíveis
│   └── project-type-signatures.yaml      # Assinaturas para detectar tipo de projeto
│
└── scripts/                              # 1 script utilitário
    └── validate-setup.js                 # Validação automatizada do setup
```

---

## Mapeamento Agente → Tasks

| Agente | Tasks Primárias |
|--------|----------------|
| `claude-mastery-chief` | `setup-wizard`, `diagnose`, `audit-setup` |
| `config-engineer` | `configure-claude-code`, `audit-settings`, `permission-strategy`, `enterprise-config`, `multi-project-setup` |
| `hooks-architect` | `hook-designer`, `audit-integration`, `create-rules` |
| `mcp-integrator` | `mcp-integration-plan`, `mcp-workflow` |
| `project-integrator` | `integrate-project`, `brownfield-setup`, `setup-repository`, `claude-md-engineer` |
| `roadmap-sentinel` | `context-rot-audit`, `optimize-context`, `optimize-workflow` |
| `skill-craftsman` | `create-agent-definition`, `create-team-topology`, `parallel-decomposition` |
| `swarm-orchestrator` | `worktree-strategy`, `sandbox-setup`, `ci-cd-setup` |

---

## Mapeamento Workflow → Tasks

| Workflow | Tasks Envolvidas |
|----------|-----------------|
| `wf-project-setup` | `audit-setup` → `configure-claude-code` → `hook-designer` → `audit-integration` |
| `wf-audit-complete` | `audit-settings` → `audit-integration` → `context-rot-audit` → `diagnose` |
| `wf-knowledge-update` | `optimize-context` → `optimize-workflow` → `audit-setup` |

---

## Relação entre Componentes

```
                ┌──────────────┐
                │  squad.yaml  │  ← Manifesto
                └──────┬───────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
 ┌──────▼──────┐ ┌─────▼─────┐ ┌────▼────────┐
 │   agents/   │ │  tasks/   │ │ workflows/  │
 │  (8 files)  │ │ (26 files)│ │  (3 files)  │
 └──────┬──────┘ └─────┬─────┘ └────┬────────┘
        │              │             │
        └──────────────┼─────────────┘
                       │
              ┌────────▼─────────┐
              │     config/      │  ← Padrões e convenções
              │  checklists/     │
              │  templates/      │
              │  data/           │
              └──────────────────┘
```

---

## Contagem de Artefatos

| Tipo | Quantidade |
|------|-----------|
| Agentes | 8 |
| Tasks | 26 |
| Workflows | 3 |
| Checklists | 7 |
| Templates | 7 |
| Data/Catálogos | 5 |
| Scripts | 1 |
| Configurações | 3 |
| **Total** | **60 arquivos** |
