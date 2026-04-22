---
task: analyzeIncidentLogs()
responsavel: LogAnalyzer
responsavel_type: Agente
atomic_layer: Organism
elicit: false
Entrada:
- campo: incidentAlert
  tipo: string
  origen: Usuário ou fullIncidentResponse() — descrição do alerta
  obrigatorio: true
- campo: timeWindow
  tipo: string
  origen: 'Usuário ou pipeline (ex: 30m, 1h, 6h)'
  obrigatorio: true
- campo: logSources
  tipo: array
  origen: Usuário ou pipeline (cloudwatch, elk, splunk, datadog)
  obrigatorio: false
Saida:
- campo: logAnalysisReport
  tipo: file
  destino: log-analysis-report.md, root-cause-correlator
  persistido: true
- campo: anomalyList
  tipo: array
  destino: root-cause-correlator, postmortem-writer
  persistido: true
Checklist:
  pre-conditions:
  - '[ ] Alerta de incidente recebido com descrição'
  - '[ ] Janela de tempo definida'
  - '[ ] Fontes de log acessíveis'
  post-conditions:
  - '[ ] Logs agregados de todas as fontes'
  - '[ ] Anomalias identificadas e priorizadas'
  - '[ ] Timeline de eventos de log construída'
  - '[ ] log-analysis-report.md gerado'
  acceptance-criteria:
  - blocker: true
    criteria: Ao menos uma fonte de log analisada com dados relevantes
  - blocker: true
    criteria: Anomalias identificadas com timestamps e fonte
  - blocker: false
    criteria: Correlação entre múltiplas fontes de log
Performance:
  duration_expected: 5-15 minutos
  cost_estimated: ~0 (consulta a ferramentas existentes)
  cacheable: false
  parallelizable: true
Error Handling:
  strategy: retry
  retry:
    max_attempts: 3
    delay: exponential(base=5s, max=30s)
  fallback: Se fonte de log indisponível, usar fontes alternativas disponíveis
  notification: root-cause-correlator
Metadata:
  version: 1.0.0
  dependencies: []
  author: incident-response-squad
  created_at: '2026-02-24T00:00:00Z'
description: '```'
---

# Analyze Incident Logs

## Flow

```
1. Receber alerta e definir janela de tempo
2. Identificar fontes de log relevantes
3. Agregar logs de cada fonte na janela de tempo
4. Normalizar timestamps entre fontes (UTC)
5. Identificar baseline de operação normal
6. Detectar anomalias (error spikes, padrões incomuns)
7. Extrair stack traces e mensagens de erro relevantes
8. Priorizar anomalias por severidade e relevância
9. Gerar log-analysis-report.md
10. Enviar relatório para @root-cause-correlator
```

## Elicitation

- "Qual o alerta ou descrição do incidente?"
- "Há quanto tempo o problema começou? (janela de tempo)"
- "Quais fontes de log devem ser consultadas? (CloudWatch, ELK, Splunk, Datadog)"
- "Há algum serviço ou componente específico suspeito?"
