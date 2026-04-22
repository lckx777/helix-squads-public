# Coding Standards — incident-response-squad

## Linguagem
- YAML para configurações de runbooks, alertas e workflows
- Markdown para post-mortems, relatórios e documentação
- JSON para dados estruturados (anomalias, métricas, action items)
- Bash/Python para scripts de automação e runbooks
- PromQL/LogQL para queries de monitoramento

## Convenções de Nomes
- Variáveis e funções: camelCase (`incidentAlert`, `analyzeIncidentLogs`)
- Constantes: UPPER_SNAKE_CASE (`MAX_RETRY_ATTEMPTS`, `DEFAULT_TIME_WINDOW`)
- Arquivos: kebab-case (`analyze-incident-logs.md`, `root-cause-report.md`)
- IDs de incidente: `INC-YYYY-NNNN` (`INC-2026-0142`)
- Runbooks: snake_case (`rollback_deploy`, `restart_service`)

## Timestamps
- SEMPRE usar UTC para todos os timestamps
- Formato: ISO 8601 (`2026-02-24T14:30:00Z`)
- Incluir timezone quando reportar para stakeholders
- Normalizar timestamps entre fontes diferentes (clock skew)

## Segurança
- NUNCA incluir credenciais em logs ou relatórios
- Mascarar dados sensíveis (PII, tokens, API keys) em outputs
- Usar variáveis de ambiente para credenciais de ferramentas
- Validar permissões antes de executar runbooks
- Logs de auditoria para todas as ações de remediação

## Post-Mortems
- SEMPRE blameless — focar em sistemas, não em indivíduos
- JSON/Markdown em UTF-8
- Action items com owner, prioridade e prazo
- Timeline com timestamps precisos em UTC
- Publicar em até 48 horas após resolução

## Runbooks
- Cada passo deve ter validação de pré e pós-condição
- Incluir plano de rollback para cada ação
- Logar cada ação com timestamp
- Máximo 2 tentativas antes de escalar
- Documentar dependências e permissões necessárias

## Testes
- Testar runbooks em staging antes de produção
- Simular incidentes periodicamente (game days)
- Validar alertas e thresholds regularmente
- Testar comunicação de status page
