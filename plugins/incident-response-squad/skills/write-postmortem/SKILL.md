---
task: writePostMortem()
responsavel: PostMortem
responsavel_type: Agente
atomic_layer: Organism
elicit: false
Entrada:
- campo: logAnalysisReport
  tipo: file
  origen: log-analyzer (analyzeIncidentLogs())
  obrigatorio: true
- campo: rootCauseReport
  tipo: file
  origen: root-cause-correlator (correlateRootCause())
  obrigatorio: true
- campo: executionLog
  tipo: file
  origen: runbook-executor (executeRunbook())
  obrigatorio: false
- campo: statusUpdates
  tipo: file
  origen: status-page-updater (updateStatusPage())
  obrigatorio: false
- campo: timelineEvents
  tipo: array
  origen: Todos os agentes — eventos com timestamps
  obrigatorio: true
Saida:
- campo: postmortemDocument
  tipo: file
  destino: postmortem.md
  persistido: true
- campo: actionItems
  tipo: array
  destino: postmortem.md, tracking system
  persistido: true
Checklist:
  pre-conditions:
  - '[ ] Incidente resolvido (status: resolved)'
  - '[ ] Todos os artefatos do incidente coletados'
  - '[ ] Timeline de eventos disponível'
  post-conditions:
  - '[ ] postmortem.md gerado com todas as seções obrigatórias'
  - '[ ] Timeline completa e precisa'
  - '[ ] Action items definidos com owners e prazos'
  - '[ ] Linguagem blameless verificada'
  - '[ ] Lições aprendidas documentadas'
  acceptance-criteria:
  - blocker: true
    criteria: Post-mortem contém todas as seções obrigatórias
  - blocker: true
    criteria: Action items têm owner, prioridade e prazo definidos
  - blocker: true
    criteria: Linguagem é blameless — foco em sistemas, não indivíduos
  - blocker: false
    criteria: Impacto quantificado (usuários afetados, duração, custo)
Performance:
  duration_expected: 15-45 minutos
  cost_estimated: ~0
  cacheable: false
  parallelizable: false
Error Handling:
  strategy: retry
  retry:
    max_attempts: 2
    delay: fixed(30s)
  fallback: Gerar post-mortem parcial com dados disponíveis e marcar seções incompletas
  notification: root-cause-correlator
Metadata:
  version: 1.0.0
  dependencies:
  - analyzeIncidentLogs()
  - correlateRootCause()
  - executeRunbook()
  - updateStatusPage()
  author: incident-response-squad
  created_at: '2026-02-24T00:00:00Z'
description: '```'
---

# Write Post-Mortem

## Flow

```
1. Coletar todos os artefatos do incidente
2. Construir timeline completa (alerta → detecção → resposta → resolução)
3. Escrever resumo executivo do incidente
4. Documentar causa raiz em linguagem blameless
5. Listar fatores contribuintes (sistêmicos)
6. Quantificar impacto (técnico, negócio, usuário)
7. Documentar resposta (o que funcionou, o que não funcionou)
8. Definir action items com prioridade, owner e prazo
9. Extrair lições aprendidas
10. Gerar postmortem.md final
```

## Estrutura do Post-Mortem

```markdown
# Post-Mortem: [Título do Incidente]

## Resumo
- Data: YYYY-MM-DD
- Duração: X horas Y minutos
- Severidade: SEVN
- Impacto: [resumo]

## Timeline
| Hora | Evento |
|------|--------|
| HH:MM | ... |

## Causa Raiz
[Análise técnica blameless]

## Fatores Contribuintes
- [Fator 1]
- [Fator 2]

## Impacto
- Usuários afetados: N
- Duração total: X
- Perda estimada: $Y

## O que funcionou bem
- [Item 1]

## O que pode melhorar
- [Item 1]

## Action Items
| Item | Owner | Prioridade | Prazo |
|------|-------|-----------|-------|
| ... | ... | P1/P2/P3 | YYYY-MM-DD |

## Lições Aprendidas
- [Lição 1]
```
