---
task: createAgents()
responsavel: AgentCreator
responsavel_type: Agente
atomic_layer: Organism
Entrada:
- nome: analysisMd
  tipo: file
  descricao: analyzeRequirements() task output
  obrigatorio: true
- nome: componentRegistryMd
  tipo: file
  descricao: analyzeRequirements() task output
  obrigatorio: true
- nome: agentTemplateMd
  tipo: file
  descricao: templates/agent.template.md
  obrigatorio: true
- nome: agentFormatMd
  tipo: file
  descricao: references/agent-format.md
  obrigatorio: true
Saida:
- nome: agentFiles
  tipo: array<file>
  descricao: optimizeSquad() task + createTasks() task
  obrigatorio: true
- nome: ideationMd
  tipo: file
  descricao: optimizeSquad() task
  obrigatorio: true
Checklist:
  pre-conditions:
  - '[ ] analysis.md existe e contém seções obrigatórias'
  - '[ ] component-registry.md existe com nomes canônicos definidos'
  - '[ ] Template de agente disponível em templates/agent.template.md'
  - '[ ] Referência de formato disponível em references/agent-format.md'
  post-conditions:
  - '[ ] Pelo menos 1 agente criado no diretório agents/'
  - '[ ] Cada agente tem todos os campos required: agent.name, agent.id, agent.title,
    agent.icon, agent.whenToUse'
  - '[ ] Cada agente tem persona_profile com archetype e communication.tone'
  - '[ ] Cada agente tem greeting_levels (minimal, named, archetypal)'
  - '[ ] IDEATION.md gerado com raciocínio de design'
  - '[ ] IDs de agentes usam kebab-case e correspondem ao component-registry.md'
Performance:
  duration_expected: 3-8 minutos
  cost_estimated: ~5000 tokens (Opus)
  cacheable: false
  parallelizable: false
  skippable_when: Nunca — agentes são prerequisito para tasks e workflows
Error Handling:
  strategy: retry
  retry:
    max_attempts: 2
    delay: 5s
  fallback: Gerar agentes com configuração mínima e marcar para revisão
  notification: orchestrator
Metadata:
  story: Como pipeline, preciso gerar definições de agentes AIOS a partir da análise
    de requisitos
  version: 1.0.0
  dependencies:
  - analyzeRequirements()
  author: Squad Creator
  created_at: '2026-02-22T00:00:00Z'
  updated_at: '2026-02-22T00:00:00Z'
description: '```'
---

# createAgents()

## Pipeline Diagram

```
┌──────────────┐  ┌────────────────────┐  ┌───────────────┐  ┌───────────────┐
│ analysis.md  │  │ component-registry │  │ agent.template│  │ agent-format  │
│              │  │ .md                │  │ .md           │  │ .md           │
└──────┬───────┘  └────────┬───────────┘  └───────┬───────┘  └───────┬───────┘
       │                   │                      │                  │
       └───────────┬───────┘                      └────────┬─────────┘
                   │                                       │
                   ▼                                       ▼
          ┌─────────────────┐                    ┌──────────────────┐
          │  AgentCreator    │◀───────────────────│  Template +      │
          │  (squad-agent-   │                    │  Format Specs    │
          │   creator)       │                    └──────────────────┘
          └────────┬─────────┘
                   │
          ┌────────┴─────────────────┐
          │                          │
          ▼                          ▼
   ┌─────────────┐          ┌──────────────┐
   │ agents/     │          │ IDEATION.md  │
   │ *.md        │          │              │
   └─────────────┘          └──────────────┘
```

## Descrição

A task `createAgents()` é a **segunda fase** do pipeline. Transforma a análise de requisitos e o component registry em definições concretas de agentes AIOS.

### Responsabilidades

1. **Leitura do Registry** — Consumir os nomes canônicos do `component-registry.md` como fonte autoritativa de IDs e nomes.

2. **Geração de Agentes** — Para cada role identificado na análise, gerar um arquivo `.md` no formato AIOS com:
   - Bloco YAML frontmatter com `agent`, `persona_profile`, `persona`, `commands`, `dependencies`
   - `persona_profile.archetype` selecionado entre Builder, Guardian, Balancer, Flow_Master
   - `communication.tone` e `greeting_levels` com 3 níveis (minimal, named, archetypal)
   - `persona.core_principles` e `responsibility_boundaries`
   - `commands` com visibilidade e descrição

3. **IDEATION.md** — Documento de raciocínio que explica:
   - Por que cada agente foi criado (justificativa por capacidade)
   - Alternativas consideradas e descartadas
   - Mapeamento agente → capacidades do registry
   - Notas sobre potenciais redundâncias (para o Optimizer)

4. **Consistência** — Garantir que todos os `agent.id` correspondem exatamente ao `component-registry.md`.

### Arquétipos de Agente

| Archetype | Quando Usar |
|-----------|-------------|
| **Builder** | Agentes que criam artefatos (código, docs, configs) |
| **Guardian** | Agentes que validam, revisam ou protegem qualidade |
| **Balancer** | Agentes que otimizam, priorizam ou fazem trade-offs |
| **Flow_Master** | Agentes que orquestram, coordenam ou gerenciam fluxo |

### Regras de Geração

- Cada agente recebe exatamente 1 archetype
- `agent.id` é kebab-case e único no squad
- `agent.name` é PascalCase e legível
- `commands` usam prefixo `*` e kebab-case
- Agentes que cobrem capacidades similares devem ser consolidados (sinalizar para Optimizer)
