# PROTOCOLO CIRCUIT BREAKER — CLAUDE CODE MASTERY SQUAD

> **Versão:** 1.0.0
> **Status:** VIGENTE
> **Escopo:** Hooks, MCPs, skills e configurações em execução

---

## ◆ PROPÓSITO

Prevenir loops de hook, timeouts de MCP, erros de carregamento de skill
e falhas de validação de configuração de propagarem para o ambiente
real do usuário. O Circuit Breaker isola falhas antes que causem dano.

---

## ◆ 1. TIPOS DE CIRCUIT BREAKER

### 1.1 Hook Execution Breaker

Previne hooks com falha recorrente de travar o fluxo de trabalho.

```
┌──────────────────────────────────────────────────────┐
│  HOOK EXECUTION CIRCUIT BREAKER                      │
│                                                      │
│  max_consecutive_failures: 3                         │
│  timeout_per_execution: 30s                          │
│                                                      │
│  FALHA 1: Log de erro, hook executado novamente      │
│  FALHA 2: Log de erro com contexto expandido         │
│  FALHA 3: Hook marcado como DEGRADED                 │
│                                                      │
│  SE 3 falhas consecutivas:                           │
│    → Hook DESABILITADO temporariamente               │
│    → Workflow continua sem o hook                    │
│    → @hooks-architect notificado                     │
│    → Usuário notificado com mensagem clara           │
│                                                      │
│  REABILITAÇÃO:                                       │
│    → Após diagnóstico e correção pelo usuário        │
│    → Nunca reabilitar automaticamente                │
└──────────────────────────────────────────────────────┘
```

### 1.2 MCP Connection Breaker

Gerencia instabilidade de conexão com servidores MCP.

```
┌──────────────────────────────────────────────────────┐
│  MCP CONNECTION CIRCUIT BREAKER                      │
│                                                      │
│  max_connection_failures: 3                          │
│  timeout_per_call: 30s                               │
│  cooldown_period: 300s (5 min)                       │
│                                                      │
│  ESTADOS:                                            │
│                                                      │
│  CLOSED (conectado)                                  │
│    → Calls fluem normalmente                         │
│    → Timeout > 30s = falha                           │
│    → failures >= 3 → OPEN                            │
│                                                      │
│  OPEN (desconectado)                                 │
│    → Calls bloqueadas para este MCP                  │
│    → Fallback para documentação local se disponível  │
│    → Health check a cada 60s                         │
│    → Após 5min cooldown → HALF_OPEN                  │
│                                                      │
│  HALF_OPEN (testando)                                │
│    → 1 call de teste permitida                       │
│    → Se sucesso → CLOSED                             │
│    → Se falha → OPEN (cooldown duplicado)            │
└──────────────────────────────────────────────────────┘
```

### 1.3 Skill Loading Breaker

Previne erros de carregamento de skill de bloquear sessão.

```
┌──────────────────────────────────────────────────────┐
│  SKILL LOADING CIRCUIT BREAKER                       │
│                                                      │
│  max_load_retries: 2                                 │
│  trigger: skill file not found | parse error         │
│                                                      │
│  RETRY 1: Tentar path alternativo (local vs global)  │
│  RETRY 2: Tentar versão anterior se disponível       │
│                                                      │
│  SE após 2 retries skill não carrega:                │
│    → Marcar skill como UNAVAILABLE                   │
│    → Continuar sessão sem a skill                    │
│    → Reportar ao usuário qual skill falhou           │
│    → NÃO bloquear outras skills                      │
└──────────────────────────────────────────────────────┘
```

### 1.4 Config Validation Breaker

Protege o settings.json do usuário contra validação em loop.

```
┌──────────────────────────────────────────────────────┐
│  CONFIG VALIDATION CIRCUIT BREAKER                   │
│                                                      │
│  max_validation_retries: 2                           │
│  trigger: JSON schema error | field conflict         │
│                                                      │
│  RETRY 1: Validar com schema relaxado                │
│  RETRY 2: Isolar campo problemático                  │
│                                                      │
│  SE após 2 retries config inválida:                  │
│    → NÃO aplicar a configuração                      │
│    → Preservar backup do settings.json               │
│    → Reportar campo específico que causou erro       │
│    → Aguardar correção manual                        │
└──────────────────────────────────────────────────────┘
```

---

## ◆ 2. DIAGRAMA DE ESTADOS (MCP)

```
              ┌────────────────────┐
              │                    │
      ┌──────▶│      CLOSED        │◀──────────────┐
      │       │   (conectado)      │               │
      │       └────────┬───────────┘               │
      │                │                           │
      │       failures >= 3                 test ok
      │                │                           │
      │                ▼                           │
      │       ┌────────────────────┐               │
      │       │                    │               │
      │       │       OPEN         │               │
      │       │  (desconectado)    │               │
      │       └────────┬───────────┘               │
      │                │                           │
      │         cooldown expira                    │
      │                │                           │
      │                ▼                           │
      │       ┌────────────────────┐               │
      │       │                    │               │
      └───────│    HALF_OPEN       │───────────────┘
   test fail  │   (testando)       │
              └────────────────────┘
```

---

## ◆ 3. LIMITES POR OPERAÇÃO

| Operação | Max Falhas/Retries | Timeout | Ação ao Atingir |
|----------|-------------------|---------|-----------------|
| Hook PreToolUse | 3 falhas consec. | 30s | Desabilitar hook, continuar |
| Hook PostToolUse | 3 falhas consec. | 30s | Desabilitar hook, continuar |
| MCP connection | 3 falhas | 30s/call | Circuit OPEN, fallback local |
| Skill loading | 2 retries | 10s | Marcar UNAVAILABLE |
| Config validation | 2 retries | 15s | Não aplicar, preservar backup |
| Schema parse | 1 tentativa | 5s | Rejeitar imediatamente com erro |

---

## ◆ 4. LOGGING DE CIRCUIT BREAKER

```yaml
circuit_breaker_event:
  id: "CB-{timestamp}-{random}"
  type: "hook | mcp | skill | config"
  trigger: "max_failures_exceeded | timeout | parse_error"
  context:
    squad: "claude-code-mastery"
    agent: "@hooks-architect"
    component: "{nome do hook/mcp/skill}"
    version: "vX.Y.Z"
  attempts: 3
  last_error: "{mensagem de erro}"
  resolution: "disabled | unavailable | fallback_local"
  timestamp: "2026-03-27T00:00:00Z"
  user_notified: true
  settings_backup_preserved: true
```

---

## ◆ 5. RECUPERAÇÃO

### 5.1 Após Hook Execution Breaker

```
1. Hook permanece DEGRADED até correção explícita
2. @hooks-architect documenta causa raiz
3. Usuário recebe:
   - Qual hook falhou
   - Qual erro ocorreu (mensagem legível)
   - Como diagnosticar (passo a passo)
   - Como reabilitar após corrigir
4. Hook só é reabilitado manualmente pelo usuário
```

### 5.2 Após MCP Connection Breaker

```
1. Estado OPEN: calls bloqueadas para o MCP específico
2. Outros MCPs NÃO são afetados
3. Fallback: documentação local se disponível
4. Health checks automáticos a cada 60s
5. Ao entrar HALF_OPEN: 1 call de teste (não-crítica)
6. Se teste passa: flush calls pendentes em ordem
7. Se teste falha: cooldown dobra (máx 30min)
```

### 5.3 Após Config Validation Breaker

```
1. Backup de settings.json preservado em ~/.claude/settings.json.bak
2. Configuração problemática isolada e reportada ao usuário
3. NÃO fazer alterações parciais no settings.json
4. Entregável inclui:
   - Campo exato que causou erro
   - Valor atual vs valor esperado
   - JSON corrigido para aplicação manual
```

---

## ◆ 6. MÉTRICAS DE SAÚDE

```yaml
health_metrics:
  circuit_breaker_activations:
    last_24h: 0
    last_7d: 0
    total: 0

  by_type:
    hook_execution: 0
    mcp_connection: 0
    skill_loading: 0
    config_validation: 0

  hooks_currently_degraded: []
  mcps_currently_open: []
  skills_currently_unavailable: []

  current_state:
    hooks_pipeline: CLOSED
    mcp_connections: CLOSED
    skill_loader: CLOSED
    config_validator: CLOSED
```

---

*Ratificado em: 2026-03-27*
*Guardiões: @hooks-architect (Hooks) + @mcp-integrator (MCP) + @roadmap-sentinel (Config)*
