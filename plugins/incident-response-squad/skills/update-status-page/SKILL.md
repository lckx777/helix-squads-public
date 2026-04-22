---
task: updateStatusPage()
responsavel: StatusUpdater
responsavel_type: Agente
atomic_layer: Organism
elicit: false
Entrada:
- campo: incidentDetails
  tipo: object
  origen: Pipeline de incidente (alerta, descrição, serviços afetados)
  obrigatorio: true
- campo: remediationStatus
  tipo: string
  origen: runbook-executor (executeRunbook())
  obrigatorio: false
- campo: severityLevel
  tipo: string
  origen: Triagem inicial ou @root-cause-correlator
  obrigatorio: true
Saida:
- campo: statusUpdate
  tipo: file
  destino: status-update.md, postmortem-writer
  persistido: true
- campo: notificationLog
  tipo: object
  destino: postmortem-writer
  persistido: true
Checklist:
  pre-conditions:
  - '[ ] Detalhes do incidente recebidos'
  - '[ ] Severidade definida'
  - '[ ] Acesso ao status page configurado'
  post-conditions:
  - '[ ] Status page atualizado'
  - '[ ] Stakeholders notificados conforme matriz de severidade'
  - '[ ] status-update.md gerado com histórico'
  - '[ ] SLA de tempo de resposta atendido'
  acceptance-criteria:
  - blocker: true
    criteria: Status page atualizado dentro do SLA de resposta
  - blocker: true
    criteria: Stakeholders corretos notificados para o nível de severidade
  - blocker: false
    criteria: Linguagem empática e profissional na comunicação
Performance:
  duration_expected: 2-5 minutos por atualização
  cost_estimated: ~0
  cacheable: false
  parallelizable: true
Error Handling:
  strategy: retry
  retry:
    max_attempts: 3
    delay: exponential(base=2s, max=15s)
  fallback: Se status page indisponível, notificar via Slack/email diretamente
  notification: root-cause-correlator
Metadata:
  version: 1.0.0
  dependencies:
  - executeRunbook()
  author: incident-response-squad
  created_at: '2026-02-24T00:00:00Z'
description: '```'
---

# Update Status Page

## Flow

```
1. Receber detalhes do incidente e severidade
2. Selecionar template de comunicação apropriado
3. Compor mensagem de status (investigating/identified/monitoring/resolved)
4. Publicar atualização no status page externo
5. Publicar atualização no canal interno (#incidents)
6. Notificar stakeholders conforme matriz de severidade
7. Logar notificação no notification-log.json
8. Agendar próxima atualização conforme frequência da severidade
9. Atualizar status-update.md com histórico
```

## Status Transitions

```
investigating → identified → monitoring → resolved
     ↓              ↓
  escalated     partial_fix → monitoring → resolved
```

## Elicitation

- "Qual o nível de severidade? (SEV1, SEV2, SEV3, SEV4)"
- "Qual o impacto atual nos usuários?"
- "Já foi identificada a causa raiz?"
- "Qual o status atual da remediação?"
