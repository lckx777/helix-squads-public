---
task: correlateRootCause()
responsavel: Correlator
responsavel_type: Agente
atomic_layer: Molecule
elicit: false
Entrada:
- campo: logAnalysisReport
  tipo: file
  origen: log-analyzer (analyzeIncidentLogs())
  obrigatorio: true
- campo: monitoringMetrics
  tipo: object
  origen: Ferramentas de monitoramento (Datadog, Prometheus, Grafana)
  obrigatorio: false
- campo: dependencyMap
  tipo: file
  origen: Documentação de arquitetura ou discovery automática
  obrigatorio: false
Saida:
- campo: rootCauseReport
  tipo: file
  destino: root-cause-report.md, runbook-executor, postmortem-writer
  persistido: true
- campo: blastRadiusAssessment
  tipo: object
  destino: status-page-updater, postmortem-writer
  persistido: true
- campo: confidenceScore
  tipo: number
  destino: root-cause-report.md
  persistido: true
Checklist:
  pre-conditions:
  - '[ ] Relatório de análise de logs recebido'
  - '[ ] Acesso a métricas de monitoramento'
  - '[ ] Mapa de dependências disponível (ou construído)'
  post-conditions:
  - '[ ] Causa raiz identificada com evidências'
  - '[ ] Blast radius mapeado'
  - '[ ] Confidence score calculado'
  - '[ ] root-cause-report.md gerado'
  - '[ ] Remediação sugerida para @runbook-executor'
  acceptance-criteria:
  - blocker: true
    criteria: Causa raiz identificada com confidence score >= 50%
  - blocker: true
    criteria: Blast radius mapeado com serviços afetados listados
  - blocker: false
    criteria: Remediação sugerida vinculada a runbook existente
Performance:
  duration_expected: 10-30 minutos
  cost_estimated: ~0 (consulta a ferramentas existentes)
  cacheable: false
  parallelizable: false
Error Handling:
  strategy: escalate
  retry:
    max_attempts: 2
    delay: exponential(base=10s, max=60s)
  fallback: Se correlação inconclusiva, escalar para engenharia sênior com dados coletados
  notification: status-page-updater
Metadata:
  version: 1.0.0
  dependencies:
  - analyzeIncidentLogs()
  author: incident-response-squad
  created_at: '2026-02-24T00:00:00Z'
description: '```'
---

# Correlate Root Cause

## Flow

```
1. Receber relatório de análise de logs do @log-analyzer
2. Coletar métricas de monitoramento relevantes
3. Construir/atualizar grafo de dependências
4. Correlacionar anomalias de log com métricas
5. Identificar ponto de origem da cascata de falhas
6. Mapear blast radius (direto, first-order, second-order)
7. Calcular confidence score baseado em evidências
8. Propor causa raiz e remediação sugerida
9. Gerar root-cause-report.md
10. Enviar relatório para @runbook-executor
```

## Correlação Multi-Ferramenta

### Fontes de Sinal

| Categoria | Ferramentas | Sinais |
|---|---|---|
| Métricas | Datadog, Prometheus, CloudWatch | CPU, memória, latência, error rate |
| Traces | Jaeger, X-Ray, Datadog APM | Distributed traces, latência por serviço |
| Logs | ELK, Splunk, CloudWatch Logs | Erros, exceções, padrões |
| Alertas | PagerDuty, OpsGenie | Timeline de alertas |
| Infra | Kubernetes, AWS, GCP | Events, health checks |
