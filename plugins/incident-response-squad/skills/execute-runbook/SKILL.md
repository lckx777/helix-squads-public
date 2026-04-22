---
task: executeRunbook()
responsavel: RunbookExec
responsavel_type: Agente
atomic_layer: Molecule
elicit: false
Entrada:
- campo: rootCauseReport
  tipo: file
  origen: root-cause-correlator (correlateRootCause())
  obrigatorio: true
- campo: runbookLibrary
  tipo: file
  origen: Biblioteca de runbooks do squad
  obrigatorio: false
- campo: environmentContext
  tipo: object
  origen: Configuração do ambiente (staging, production, região)
  obrigatorio: true
Saida:
- campo: executionLog
  tipo: file
  destino: execution-log.md, postmortem-writer
  persistido: true
- campo: remediationStatus
  tipo: string
  destino: status-page-updater, postmortem-writer
  persistido: true
Checklist:
  pre-conditions:
  - '[ ] Root cause report recebido com remediação sugerida'
  - '[ ] Runbook identificado e validado para o incidente'
  - '[ ] Pré-condições do runbook verificadas'
  - '[ ] Plano de rollback preparado'
  post-conditions:
  - '[ ] Runbook executado com sucesso'
  - '[ ] Métricas mostram melhoria ou resolução'
  - '[ ] execution-log.md gerado com todas as ações'
  - '[ ] Status de remediação comunicado'
  acceptance-criteria:
  - blocker: true
    criteria: Runbook executado com todos os passos logados
  - blocker: true
    criteria: Status de remediação definido (resolved, partially_resolved, failed)
  - blocker: false
    criteria: Métricas de saúde confirmam melhoria
Performance:
  duration_expected: 5-30 minutos
  cost_estimated: Variável conforme ação (scaling pode ter custo de infra)
  cacheable: false
  parallelizable: false
Error Handling:
  strategy: retry
  retry:
    max_attempts: 2
    delay: exponential(base=10s, max=60s)
  fallback: Se remediação falhar após 2 tentativas, escalar para engenharia e abrir
    circuit breaker
  notification: root-cause-correlator, status-page-updater
Metadata:
  version: 1.0.0
  dependencies:
  - correlateRootCause()
  author: incident-response-squad
  created_at: '2026-02-24T00:00:00Z'
description: '```'
---

# Execute Runbook

## Flow

```
1. Receber root cause report com remediação sugerida
2. Selecionar runbook apropriado da biblioteca
3. Validar pré-condições (permissões, acesso, estado do sistema)
4. Preparar plano de rollback
5. Executar passos do runbook sequencialmente
6. Validar pós-condição de cada passo
7. Monitorar métricas após execução
8. Se falhar, executar rollback e tentar alternativa
9. Registrar todas as ações no execution-log.md
10. Comunicar status para @status-page-updater
```

## Runbooks Disponíveis

| Runbook | Categoria | Tempo | Risco |
|---|---|---|---|
| `rollback_deploy` | Deploy | 5-15 min | Médio |
| `canary_rollback` | Deploy | 2-5 min | Baixo |
| `feature_flag_disable` | Deploy | 1-2 min | Baixo |
| `horizontal_scale_up` | Scaling | 5-10 min | Baixo |
| `restart_service` | Infra | 2-5 min | Médio |
| `restart_pod` | Infra | 1-3 min | Baixo |
| `failover_db` | Infra | 5-15 min | Alto |
| `clear_cache` | Infra | 1-2 min | Baixo |
| `dns_failover` | Network | 5-10 min | Alto |
| `circuit_breaker_open` | Network | 1 min | Médio |
