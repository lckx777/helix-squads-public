# cartographer

> This plugin is part of the [Helix Squads Public Marketplace](https://github.com/lckx777/helix-squads-public).

## Quick install

```
claude plugin marketplace add lckx777/helix-squads-public
claude plugin install cartographer@helix-squads-public
```

---

# Cartographer Squad — Sistema Nervoso do Ecossistema

> **Versão:** 1.0.0 — Artifacts only (Implementation pending — see @sm stories)
> **Squad prefix:** `cart`
> **Slash commands:** `*cart-reindex`, `*cart-find`, `*cart-check`, `*cart-status`, `*cart-report`
> **Origem:** Blueprint arquitetural de Alan Nicolas (consultado via `/ask alan-nicolas`)

---

## O Que Faz

O Cartographer é o sistema nervoso do monorepo. Ele escava, cataloga e mapeia continuamente
todos os artefatos do ecossistema — funções TypeScript, agentes, workflows, hooks, schemas SQL,
MCPs — e expõe esse conhecimento via CLI e MCP para que qualquer outro agente possa **consultar
antes de agir**.

**Princípio central: IDS — REUSE > ADAPT > CREATE.**

Sem o Cartographer, cada agente age no escuro: não sabe o que já existe, recria o que já foi
criado, e o ecossistema vira um labirinto com 100+ componentes sem mapa.

---

## Composição da Squad (7 Agentes)

| Agente | Papel | Modelo | Escopo |
|--------|-------|--------|--------|
| `@cart-surveyor` | Orquestrador / PM | opus | Coordena escavações, resolve conflitos, enforça IDS |
| `@cart-ts-digger` | Escavador TypeScript | sonnet | `packages/**/*.ts`, `hub/**/*.ts` |
| `@cart-py-digger` | Escavador Python | sonnet | `.claude/hooks/**`, `scripts/**`, `mega-brain/**/*.py` |
| `@cart-yaml-digger` | Escavador Config | sonnet | `squads/**/squad.yaml`, agentes, chains, `.mcp.json` |
| `@cart-sql-digger` | Escavador SQL | sonnet | `supabase/migrations/**` |
| `@cart-keeper` | Curador do Grafo | opus | Único escritor do catálogo — upsert, drift, embeddings |
| `@cart-oracle` | Camada de Query | opus | Read-only — responde perguntas, enforça IDS, gera relatórios |

### Resultado AgentDropout (Phase 5)

**TS-Digger + PY-Digger:** Mantidos como agentes separados (limites de linguagem absolutos),
mas compartilham o `config/digger-base-contract.md` como abstração base. Mesmo contrato de
NDJSON, mesma lógica de hash-gate, parser diferente. Sem fusão — fusão criaria ambiguidade de
escopo.

**Oracle vs oracle-supreme-squad:** Disambiguado explicitamente na definição do agente.
`cart-oracle` responde sobre artefatos de código. `oracle-supreme-squad` responde sobre
estratégia de negócio. Perguntas erradas são redirecionadas.

---

## Fluxo de Funcionamento

```
MONOREPO (100+ components)
         │
         ▼ (escavação)
┌─────────────────────────────────────────────┐
│  cart-ts-digger    → .run/ts-artifacts.ndjson  │
│  cart-py-digger    → .run/py-artifacts.ndjson  │  (paralelo)
│  cart-yaml-digger  → .run/yaml-artifacts.ndjson│
│  cart-sql-digger   → .run/sql-artifacts.ndjson │
└─────────────────────────────────────────────┘
         │ (gate: excavation PASSED)
         ▼
┌─────────────────────────────────────────────┐
│  cart-keeper                                   │
│  → upsert nodes + edges no catálogo            │
│  → detecta drift vs run anterior              │
│  → gera embedding-queue (pre-MCP)             │
│  → escreve graph-snapshot-{timestamp}.yaml    │
└─────────────────────────────────────────────┘
         │ (gate: graph-integrity PASSED)
         ▼
┌─────────────────────────────────────────────┐
│  cart-oracle (read-only)                       │
│  → *cart-find "função que valida gate state"  │
│  → *cart-check "novo hook PreToolUse"         │  → REUSE | ADAPT | CREATE
│  → *cart-trace pipeline-engine:canProceed     │
│  → *cart-report --format md                   │
└─────────────────────────────────────────────┘
```

---

## Comandos

| Comando | Quando Usar |
|---------|-------------|
| `*cart-reindex --full` | Escavação completa semanal ou pós-mudança grande |
| `*cart-reindex --incremental` | Pós-commit, atualiza só arquivos alterados |
| `*cart-find <query>` | "Já existe isso no ecossistema?" |
| `*cart-check <desc> --type <kind>` | IDS check antes de criar algo novo |
| `*cart-trace <artifact_id>` | Mapa completo de dependências de um artefato |
| `*cart-status` | Estado atual do grafo (frescor, contagens) |
| `*cart-report` | Relatório de saúde do ecossistema |
| `*cart-drift` | O que mudou desde o último run |

---

## Enforcement IDS (REUSE > ADAPT > CREATE)

O Oracle retorna sempre uma de 3 respostas:

| Veredicto | Condição | Ação Recomendada |
|-----------|----------|-----------------|
| **REUSE** | Similaridade >= 0.95 | Use o artefato existente — path e exemplo de uso citados |
| **ADAPT** | Similaridade 0.75-0.94 | Estenda/configure o artefato mais próximo — delta descrito |
| **CREATE** | Similaridade < 0.75 | Gap confirmado — pode criar, gap descrito |

Override (quando CREATE com similaridade >= 0.75):
- cart-surveyor loga em `.run/ids-overrides.yaml`
- Campos obrigatórios: `caller_agent`, `proposed`, `similarity_score`, `override_rationale`

---

## Artefatos Produzidos

```
squads/cartographer/
├── squad.yaml                    ← Definição completa da squad
├── agents/                       ← 7 definições de agentes (squad-side)
│   ├── cart-surveyor.md
│   ├── cart-ts-digger.md
│   ├── cart-py-digger.md
│   ├── cart-yaml-digger.md
│   ├── cart-sql-digger.md
│   ├── cart-keeper.md
│   └── cart-oracle.md
├── tasks/                        ← 9 contratos de tasks
│   ├── index-typescript.md
│   ├── index-python.md
│   ├── index-yaml.md
│   ├── index-sql.md
│   ├── build-graph.md
│   ├── query-graph.md
│   ├── enforce-reuse.md
│   ├── detect-drift.md
│   └── generate-report.md
├── chains/                       ← 3 chains (Art. VII compliant)
│   ├── incremental-index-chain.yaml
│   ├── full-reindex-chain.yaml
│   └── query-before-create-chain.yaml
├── checklists/
│   ├── excavation-gate.md
│   ├── graph-integrity-gate.md
│   └── reuse-enforcement-gate.md
└── config/
    └── digger-base-contract.md

.claude/agents/                   ← 7 native agent files (invocáveis)
├── cartographer-surveyor.md
├── cartographer-ts-digger.md
├── cartographer-py-digger.md
├── cartographer-yaml-digger.md
├── cartographer-sql-digger.md
├── cartographer-keeper.md
└── cartographer-oracle.md
```

**Runtime (gitignored — gerado durante operação):**
```
squads/cartographer/.run/
├── digger-output/          ← NDJSON dos escavadores
├── catalog/                ← Catálogo de artefatos (pre-MCP: arquivos JSON)
├── last-hashes.json        ← Hash registry para incremental
├── drift-log.ndjson        ← Histórico de drifts
├── ids-checks.ndjson       ← Histórico de checks IDS
├── query-log.ndjson        ← Log de queries ao oracle
├── embedding-queue.ndjson  ← Fila de embeddings (pre-MCP)
├── ids-overrides.yaml      ← CREATEs com override de IDS
└── graph-snapshot-*.yaml   ← Snapshots pós-build
```

---

## O Que Não Está Implementado (Roadmap)

Esta entrega contém os **artefatos de definição da squad** (agents, tasks, chains, README).
A implementação concreta requer as seguintes histórias para `@sm`:

### Histórias @sm

| ID | Título | Prioridade | Dependências |
|----|--------|------------|--------------|
| SM-CART-01 | Criar estrutura `.run/` e lógica de hash-gate base | P1 | nenhuma |
| SM-CART-02 | Implementar cart-ts-digger: parser TS AST via Glob+Grep | P1 | SM-CART-01 |
| SM-CART-03 | Implementar cart-py-digger: parser Python AST + hook extraction | P1 | SM-CART-01 |
| SM-CART-04 | Implementar cart-yaml-digger: squad.yaml + frontmatter parser | P1 | SM-CART-01 |
| SM-CART-05 | Implementar cart-sql-digger: migration parser com order awareness | P2 | SM-CART-01 |
| SM-CART-06 | Implementar cart-keeper: file-based catalog (pre-MCP) | P1 | SM-CART-02..05 |
| SM-CART-07 | Implementar cart-oracle: query layer sobre file-based catalog | P1 | SM-CART-06 |
| SM-CART-08 | Schema Supabase para cartographer (tabelas artifacts, edges, runs) | P2 | SM-CART-06 |
| SM-CART-09 | Criar `packages/cartographer-mcp/` com 5 tools MCP | P2 | SM-CART-07, SM-CART-08 |
| SM-CART-10 | Hook PreToolUse de IDS enforcement (WARN → BLOCK) | P2 | SM-CART-07 |
| SM-CART-11 | Migrar cart-keeper de file-based para Supabase pgvector | P3 | SM-CART-08, SM-CART-09 |
| SM-CART-12 | Integração de embeddings (Supabase + Voyage AI) | P3 | SM-CART-11 |

**Prioridade imediata (P1):** SM-CART-01 → SM-CART-07 (MVP: file-based catalog funcional)
**Segunda onda (P2):** SM-CART-08 → SM-CART-10 (Supabase + MCP + hook enforcement)
**Terceira onda (P3):** SM-CART-11 → SM-CART-12 (embeddings semânticos)

---

## Decisões de Design (Alan's Blueprint)

### Armazenamento: Supabase pgvector
**Decisão:** Backend em Supabase com coluna `vector` para busca semântica.
**Tradeoff:** Dependência de Supabase (já em uso no ecossistema). Alternativa seria SQLite local.
**Mitigação:** Fase P1 usa file-based catalog (arquivos JSON) — funcional sem Supabase.

### Escavação Estática (não execução)
**Decisão:** Todos os diggers fazem análise estática — nenhum executa código.
**Razão:** Segurança (hooks podem ter efeitos colaterais), reprodutibilidade, velocidade.
**Tradeoff:** Tipos dinâmicos (decoradores Python, conditional exports TS) marcados como `dynamic: true`.

### Hash-Gate Incremental
**Decisão:** SHA256 por arquivo, skip se hash inalterado.
**Razão:** Monorepo grande — escavação completa seria cara para rodar em PostToolUse.
**Tradeoff:** Se o arquivo não mudou mas sua dependência mudou, o incremental não re-avalia o impacto.
**Mitigação:** Full reindex semanal reconstrói o grafo completo.

### Write Exclusivity (cart-keeper como único escritor)
**Decisão:** Apenas cart-keeper escreve no catálogo de artefatos.
**Razão:** Evita race conditions e garante que integridade do grafo é validada antes de cada write.

### Oracle Distinto do oracle-supreme-squad
**Decisão:** cart-oracle é query layer sobre artefatos de código — não responde sobre estratégia.
**Razão:** Evitar scope creep e confusão de responsabilidades.

---

## Agent Authority

Esta squad **NÃO interfere** com as autoridades de outros agentes:

- `@devops` continua sendo o ÚNICO autorizado para `git push` e `gh pr create`
- `@po` valida stories antes de qualquer implementação das histórias @sm
- `cart-oracle` é read-only — nunca modifica código-fonte
- Escavadores são read-only — nunca modificam arquivos do monorepo

---

---

# English Summary

## What It Does

Cartographer is the ecosystem nervous system. It continuously excavates, catalogs, and maps
all monorepo artifacts (TS functions, agents, workflows, hooks, SQL schemas, MCPs) and exposes
this knowledge via CLI+MCP so any agent can **query before acting**.

**Core principle: IDS — REUSE > ADAPT > CREATE.**

## Squad Composition

7 agents: 1 orchestrator (Surveyor), 4 language diggers (TS/Python/YAML/SQL), 1 graph curator
(Keeper), 1 query oracle (Oracle). Models: opus for Surveyor/Keeper/Oracle, sonnet for diggers.

## Current Status

**Phase 1 complete:** All squad artifacts generated (agents, tasks, chains, checklists, README).

**Pending implementation** (requires @sm stories SM-CART-01 through SM-CART-12):
- File-based catalog runtime (P1, no Supabase dependency)
- Supabase pgvector schema + MCP package (P2)
- Semantic embeddings via Voyage AI (P3)

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| Static analysis only (never execute) | Safety + reproducibility |
| Hash-gated incremental index | Cost efficiency on large monorepo |
| File-based catalog pre-MCP | MVP without Supabase dependency |
| cart-keeper as sole writer | Graph integrity enforcement |
| cart-oracle distinct from oracle-supreme-squad | Scope clarity |
