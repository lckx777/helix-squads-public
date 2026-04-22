# Padrões de Codificação — Claude Code Mastery Squad

## Visão Geral

Este documento define os padrões obrigatórios para todos os artefatos produzidos pelo Claude Code Mastery Squad. O squad especializa-se em configuração, extensão e integração do Claude Code como plataforma de desenvolvimento assistido por IA.

---

## Tipos de Artefato e Formatos

| Tipo de Artefato | Formato | Extensão | Prefixo de ID |
|------------------|---------|----------|---------------|
| Agent definitions | Markdown (AIOS format) | `.md` | `ccm-` |
| Task definitions | Markdown (TASK-FORMAT-SPECIFICATION V1) | `.md` | kebab-case |
| Skills | Markdown | `.md` | kebab-case |
| Workflows | YAML | `.yaml` | kebab-case |
| Checklists | Markdown | `.md` | kebab-case |
| Templates (CLAUDE.md) | Markdown | `.md` | `claude-md-` |
| Data/Catalogs | YAML | `.yaml` | kebab-case |
| Scripts | JavaScript (Node.js) | `.js` | kebab-case |

---

## Convenções de Nomenclatura

### Identificadores

| Elemento | Convenção | Exemplo |
|----------|-----------|---------|
| Agent ID | `ccm-` + `kebab-case` | `ccm-chief`, `ccm-hooks-architect` |
| Agent filename | `kebab-case.md` | `hooks-architect.md`, `skill-craftsman.md` |
| Task identifier | `camelCase()` | `configureClaudeCode()`, `hookDesigner()` |
| Task filename | `kebab-case.md` | `hook-designer.md`, `mcp-workflow.md` |
| Workflow filename | `kebab-case.yaml` | `wf-project-setup.yaml` |
| Checklist filename | `kebab-case-checklist.md` | `integration-audit-checklist.md` |
| Template filename | `claude-md-{type}.md` | `claude-md-fullstack.md`, `claude-md-monorepo.md` |
| Data catalog filename | `kebab-case.yaml` | `hook-patterns.yaml`, `mcp-integration-catalog.yaml` |
| Script filename | `kebab-case.js` | `validate-setup.js` |
| Constantes (JS) | `UPPER_SNAKE_CASE` (inglês) | `const MAX_HOOK_DEPTH = 3` |
| Variáveis (JS) | `camelCase` (inglês) | `const hookConfig = {}` |

### Regra de Ouro

- **Código, variáveis, identificadores**: sempre em **inglês**
- **Conteúdo textual, descrições, mensagens**: sempre em **PT-BR** com acentuação correta

---

## Idioma e Codificação

| Aspecto | Padrão |
|---------|--------|
| Codificação de arquivos | **UTF-8** sem BOM |
| Idioma do conteúdo | **Português (PT-BR)** com acentuação obrigatória |
| Idioma de código/variáveis | **Inglês** |
| Comentários em código | **PT-BR** ou inglês (consistente por arquivo) |

---

## Formatação YAML

| Regra | Valor |
|-------|-------|
| Indentação | **2 espaços** (nunca tabs) |
| Comprimento máximo de linha | **120 caracteres** |
| Strings com caracteres especiais | Aspas duplas (`"`) |
| Strings multiline | Block scalar (`>` ou `\|`) |
| Comentários | `#` com espaço após o símbolo |

### Exemplo de Workflow

```yaml
# Workflow de configuração de projeto
name: wf-project-setup
description: >
  Configura Claude Code em novo projeto com hooks, rules,
  CLAUDE.md e permissões otimizadas.

steps:
  - name: audit
    agent: config-engineer
    task: audit-setup.md
  - name: configure
    agent: config-engineer
    task: configure-claude-code.md
  - name: validate
    agent: hooks-architect
    task: audit-integration.md
```

---

## Estrutura de Agentes CCM

Todo agente CCM **deve** conter as seguintes seções no YAML frontmatter:

```markdown
---
agent:
  name: "NomeDoAgente"
  id: "ccm-nome-do-agente"
  title: "Título Descritivo do Papel"
  icon: "🔧"
  whenToUse: "Quando usar este agente — contexto específico"

persona_profile:
  archetype: "Arquétipo"
  communication:
    tone: methodical | pragmatic | creative
    style: systematic | collaborative

persona:
  role: "Função no squad CCM"
  focus: "Domínio de especialização Claude Code"
  core_principles:
    - "Princípio 1"

dependencies:
  tasks:
    - "task-name.md"
---
```

---

## Estrutura de Tasks CCM

Toda task **deve** seguir o TASK-FORMAT-SPECIFICATION V1:

```markdown
---
id: task-name
name: "taskName()"
type: task
version: 1.0.0
inputs:
  - name: "inputName"
    description: "Descrição do input"
outputs:
  - name: "outputName"
    description: "Descrição do output"
---

# taskName() — Título da Task

## Pipeline

[Input] → [Análise] → [Execução] → [Validação] → [Output]

## Descrição
...
```

---

## Convenções Específicas do Domínio

### Hooks (`.claude/hooks/`)
- Hooks seguem formato `settings.json` com `matcher`, `hooks` array
- Hook scripts em bash ou Node.js, documentados no topo com propósito e gatilho
- Hooks de validação devem ter exit code não-zero para bloquear operação

### Rules (`.claude/rules/`)
- Rules com `paths:` frontmatter carregam apenas quando arquivos correspondentes são editados
- Uma rule por responsabilidade (não regras genéricas catch-all)
- Tamanho máximo recomendado: **150 linhas** por rule file

### Skills (`.claude/skills/`)
- Skills são documentos Markdown com instrução de comportamento
- Nome do trigger deve estar na primeira linha como comentário YAML
- Skills de agentes usam prefixo `{squad-short}:agents:{name}`

### CLAUDE.md Templates
- Templates em `templates/` são bases para projetos — adaptar, nunca copiar literalmente
- Cada template documenta seu `project-type` no frontmatter
- Seções obrigatórias: Estrutura do Projeto, Padrões de Código, Comandos Frequentes

---

## Regras Gerais

1. **Sem BOM** — Arquivos UTF-8 sem Byte Order Mark
2. **Linha final** — Todo arquivo deve terminar com uma linha em branco
3. **Sem trailing whitespace** — Espaços em branco no final de linhas são proibidos
4. **Headings** — Use `#` para headings em Markdown (nunca underline style)
5. **Separadores** — Use `---` para separar seções principais
6. **Links relativos** — Prefira links relativos dentro do squad
