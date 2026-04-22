# nirvana-context-enricher

> This plugin is part of the [Helix Squads Public Marketplace](https://github.com/lckx777/helix-squads-public).

## Quick install

```
claude plugin marketplace add lckx777/helix-squads-public
claude plugin install nirvana-context-enricher@helix-squads-public
```

---

# Nirvana Context Enricher

[English](README.en.md) • [中文](README.zh.md) • [हिन्दी](README.hi.md) • [Español](README.es.md) • [العربية](README.ar.md)

> Enriquecimento de contexto multi-agente em paralelo — pesquisa profunda, ecossistema de skills e literatura acadêmica sintetizados em briefings arquiteturais de 16 seções.

A NCE existe para resolver um problema concreto: pesquisas técnicas sequenciais produzem cobertura rasa e gastam tempo. A solução é decompor qualquer tópico em três eixos ortogonais — fundacional, ecossistêmico e acadêmico — e despachar pesquisadores especializados em paralelo, garantindo cobertura mínima de 24 buscas e 11 extrações antes que um sintetizador unifique tudo num briefing único.

O resultado é um relatório de 16 seções salvo em `.claude/context-enrichment/{topic}.md`, pronto para guiar decisões arquiteturais antes de qualquer implementação. Tempo típico de execução: 7 a 15 minutos.

**Versão:** 1.0.0 • **Licença:** MIT • **AIOS:** ≥ 2.1.0 • **Slash Prefix:** `/nce`

---

## Instalação

```bash
# A partir da raiz do projeto AIOX
aiox squads enable nirvana-context-enricher
```

Pré-requisitos:

| Requisito | Notas |
|-----------|-------|
| Claude Code com Agent Teams | Necessário para dispatch paralelo de subagentes |
| Synkra AIOS Core ≥ 2.1.0 | Loader de squad e executor de workflows |
| Conectividade de rede | Web search e content extraction |
| `.claude/context-enrichment/` writable | Criado automaticamente se ausente |

MCPs (EXA, Context7, Apify) são **opcionais** — pesquisadores fazem fallback para WebSearch/WebFetch nativos.

---

## O que Faz

A NCE entrega uma capability principal: transformar um tópico técnico em um relatório arquitetural denso, com rastreabilidade total das fontes. Cinco capabilities atômicas compõem essa entrega:

1. **Orquestração paralela com lifecycle completo** — parsing de request, dispatch, barreira de quórum, entrega e cleanup
2. **Pesquisa fundacional profunda** — 6 rounds (fundamentos → arquitetura → práticas → avançado → estado atual → pitfalls)
3. **Mapeamento de ecossistema** — skills.sh, GitHub trending, awesome-lists com veredicto de manutenção
4. **Coleta acadêmica com hierarquia de tiers** — peer-reviewed, arxiv, refusing tier-5 (predatory)
5. **Síntese unificada** — 16 seções fixas, conflitos preservados (não escondidos), gaps explícitos

---

## Pipeline

| Fase | Agente | Papel | Modelo |
|------|--------|-------|--------|
| 1 | nirva | Parse request + acquire lock | sonnet |
| 2 | nirva | Dispatch parallel team | sonnet |
| 3a | sage | 6-round deep research (paralelo) | opus |
| 3b | scout | 3-axis ecosystem map (paralelo) | sonnet |
| 3c | scholar | Academic sources com tiers (paralelo) | sonnet |
| 4 | nirva | Validate coverage quorum (join barrier) | sonnet |
| 5 | lotus | Synthesize 16-section report | opus |
| 6 | nirva | Deliver report ao usuário | sonnet |
| 7 | nirva | Cleanup team (sempre executa) | sonnet |

---

## Agentes

| Agente | Título | Archetype | Descrição |
|--------|--------|-----------|-----------|
| 🎯 nirva | Context Enrichment Orchestrator | Flow_Master | Conduz o pipeline — parsing, dispatch paralelo, quórum, entrega e cleanup |
| 📜 sage | Deep Research Specialist | Builder | Constrói corpus fundacional via 6 rounds exaustivos com primary sources |
| 🧭 scout | Skills & Ecosystem Explorer | Builder | Mapeia ecossistema com veredicto de manutenção (🟢/🟡/🔴) |
| 🎓 scholar | Academic Research Analyst | Guardian | Guarda rigor acadêmico — rejeita tier-5, surfaces disagreements |
| 🪷 lotus | Knowledge Synthesizer | Balancer | Reconcilia 3 perspectivas em relatório unificado de 16 seções |

---

## Tasks

| Task | Responsável | Atomic Layer | Descrição |
|------|-------------|-------------|-----------|
| `parseEnrichmentRequest()` | Nirva | Atom | Parse topic + valida pré-requisitos |
| `dispatchResearchTeam()` | Nirva | Molecule | Fan-out de 3 researchers em paralelo |
| `executeDeepResearch()` | Sage | Organism | 6 rounds fundacionais |
| `exploreSkillsEcosystem()` | Scout | Organism | 3 eixos de mapeamento ecossistêmico |
| `collectAcademicSources()` | Scholar | Molecule | 2 fases com hierarquia de tiers |
| `validateCoverageQuorum()` | Nirva | Analysis | Join barrier (≥24 searches, ≥11 extractions) |
| `synthesizeContextReport()` | Lotus | Organism | 16-section unified report |
| `deliverEnrichmentReport()` | Nirva | Molecule | Save + executive summary ao usuário |
| `cleanupResearchTeam()` | Nirva | Atom | Lifecycle close (sempre executa) |

---

## Workflows

| Workflow | Pattern | Agentes | Descrição |
|----------|---------|---------|-----------|
| `context_enrichment_pipeline` | fan_out_with_join_barrier | nirva, sage, scout, scholar, lotus | Pipeline completo de enrichment paralelo |

Chain associada (Constitution Art. VII):

| Chain | Parent Step | Micro-tasks |
|-------|-------------|-------------|
| `context-enrichment` | step 3 (parallel research) | 4 (run-sage, run-scout, run-scholar, enforce-quorum-barrier) |

### Coverage Quorum

Lotus **não** roda até que todas as condições sejam satisfeitas:

| Métrica | Mínimo |
|---------|--------|
| sage: status | `complete` |
| sage: searches / extractions | ≥ 6 / ≥ 6 |
| scout: status | `complete` |
| scout: searches / extractions / tools | ≥ 3 / ≥ 3 / ≥ 5 |
| scholar: status | `complete` |
| scholar: searches / papers cited | ≥ 2 / ≥ 2 |
| **Total searches** | **≥ 24** |
| **Total extractions** | **≥ 11** |

Falha do quórum → Nirva re-dispatcha researcher(s) falhantes uma vez; se falhar de novo, aborta com diagnóstico em `.nce/abort-report.md`.

---

## Configuração

- `config/coding-standards.md` — Convenções de código (ES2022, CommonJS, kebab-case)
- `config/tech-stack.md` — Runtime, ferramentas, storage
- `config/source-tree.md` — Estrutura esperada de diretórios

---

## Uso

### Comandos Disponíveis

| Comando | Owner | Descrição |
|---------|-------|-----------|
| `*enrich-context` | nirva | Roda o pipeline completo num tópico |
| `*dispatch-team` | nirva | Fan-out de researchers (passo manual) |
| `*validate-quorum` | nirva | Enforce join barrier |
| `*deliver-report` | nirva | Salva e entrega o relatório final |
| `*cleanup-team` | nirva | Libera recursos do lifecycle |
| `*execute-deep-research` | sage | Roda os 6 rounds em um tópico |
| `*explore-skills-ecosystem` | scout | Mapeia 3 eixos ecossistêmicos |
| `*collect-academic-sources` | scholar | Coleta papers tier 1-4 |
| `*synthesize-context-report` | lotus | Merge dos 3 findings em 16 seções |

### Exemplos

```bash
# Enrichment full pipeline
/nce:agents:nirva
*enrich-context --topic="vector databases" --scope="production-ready"

# Pesquisa profunda isolada (sem o squad completo)
/nce:agents:sage
*execute-deep-research --topic="CRDTs" --scope="convergence proofs"
```

---

## Autor

Generated by Nirvana Squad Creator (linhagem: [gutomec/nirvana-context-enricher](https://squads.sh/pt/gutomec/nirvana-context-enricher/nirvana-context-enricher))

## Licença

MIT
