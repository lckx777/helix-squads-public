---
task: fullIncidentResponse()
responsavel: Correlator
responsavel_type: Agente
atomic_layer: Page
elicit: true
Entrada:
- campo: incidentAlert
  tipo: string
  origen: Usuário ou sistema de monitoramento (descrição do alerta)
  obrigatorio: true
- campo: severity
  tipo: string
  origen: Usuário ou triagem automática (SEV1, SEV2, SEV3, SEV4)
  obrigatorio: true
Saida:
- campo: incidentResponsePackage
  tipo: object
  destino: Usuário, stakeholders
  persistido: true
- campo: logAnalysisReport
  tipo: file
  destino: log-analysis-report.md
  persistido: true
- campo: rootCauseReport
  tipo: file
  destino: root-cause-report.md
  persistido: true
- campo: executionLog
  tipo: file
  destino: execution-log.md
  persistido: true
- campo: statusUpdate
  tipo: file
  destino: status-update.md
  persistido: true
- campo: postmortemDocument
  tipo: file
  destino: postmortem.md
  persistido: true
Checklist:
  pre-conditions:
  - '[ ] Alerta de incidente recebido'
  - '[ ] Severidade definida'
  - '[ ] Acesso a ferramentas de monitoramento e logs'
  - '[ ] Canal de comunicação para stakeholders disponível'
  post-conditions:
  - '[ ] Logs analisados — anomalias identificadas'
  - '[ ] Causa raiz identificada com confidence score'
  - '[ ] Runbook executado — remediação aplicada'
  - '[ ] Status page atualizado — stakeholders notificados'
  - '[ ] Post-mortem blameless gerado'
  - '[ ] Action items definidos com owners'
  acceptance-criteria:
  - blocker: true
    criteria: Causa raiz identificada com confidence score >= 50%
  - blocker: true
    criteria: Remediação executada e validada
  - blocker: true
    criteria: Stakeholders notificados dentro do SLA
  - blocker: true
    criteria: Post-mortem completo com action items
  - blocker: false
    criteria: Tempo total de resposta dentro do target para a severidade
Performance:
  duration_expected: 30-90 minutos
  cost_estimated: Variável conforme ações de remediação
  cacheable: false
  parallelizable: false
Error Handling:
  strategy: escalate
  retry:
    max_attempts: 2
    delay: exponential(base=10s, max=60s)
  fallback: Se qualquer fase falhar, comunicar status parcial e escalar para engenharia
    sênior
  notification: status-page-updater
Metadata:
  version: 1.0.0
  dependencies: []
  author: incident-response-squad
  created_at: '2026-02-24T00:00:00Z'
description: '```'
---

# Full Incident Response

## Pipeline

```
Fase 1: Análise de Logs  → @log-analyzer          → analyzeIncidentLogs()
Fase 2: Causa Raiz        → @root-cause-correlator → correlateRootCause()
Fase 3: Remediação         → @runbook-executor      → executeRunbook()
Fase 4: Comunicação        → @status-page-updater   → updateStatusPage()
Fase 5: Post-Mortem        → @postmortem-writer      → writePostMortem()
```

## Elicitation

### Fase 1 — Alerta
- "Qual o alerta ou descrição do incidente?"
- "Qual a severidade? (SEV1, SEV2, SEV3, SEV4)"
- "Quando o problema começou (ou foi detectado)?"
- "Quais serviços ou componentes são suspeitos?"

### Fase 2 — Contexto
- "Quais ferramentas de monitoramento estão disponíveis?"
- "Houve algum deploy ou mudança recente?"
- "Existe mapa de dependências dos serviços?"

### Fase 3 — Remediação
- "Confirma execução do runbook sugerido?"
- "Qual ambiente será afetado? (staging, production)"
- "Há restrições de janela de mudança?"

### Fase 5 — Post-Mortem
- "Quem deve ser owner dos action items?"
- "Qual o prazo para publicação do post-mortem?"
- "Há impacto financeiro a ser documentado?"

## Timeline Targets por Severidade

| Severidade | Detecção | Resposta | Comunicação | Resolução |
|---|---|---|---|---|
| SEV1 | < 5 min | < 15 min | < 5 min | < 1h |
| SEV2 | < 15 min | < 30 min | < 15 min | < 4h |
| SEV3 | < 30 min | < 1h | < 30 min | < 24h |
| SEV4 | < 4h | < 8h | < 4h | < 1 semana |
