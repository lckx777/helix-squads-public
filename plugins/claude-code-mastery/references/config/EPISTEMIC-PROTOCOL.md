# PROTOCOLO EPISTÊMICO — CLAUDE CODE MASTERY SQUAD

> **Versão:** 1.0.0
> **Status:** VIGENTE
> **Escopo:** Todos os agentes que produzem recomendações sobre o Claude Code

---

## ◆ PROPÓSITO

Garantir que todo conhecimento sobre o Claude Code produzido por este
squad seja verificado, versionado e honesto sobre seus limites.
Uma recomendação com confiança incorreta quebra o setup do usuário.
Zero recomendações baseadas em suposição não declarada.

---

## ◆ 1. NÍVEIS DE CONFIANÇA PARA FEATURES

Todo claim sobre comportamento do Claude Code recebe um nível:

```
┌──────────────────────────────────────────────────────────────────┐
│  NÍVEL             │ RANGE   │ CRITÉRIO                           │
├──────────────────────────────────────────────────────────────────┤
│  VERIFIED          │ 0.95+   │ Testado em ambiente real nesta     │
│                    │         │ sessão + documentação confirma     │
├──────────────────────────────────────────────────────────────────┤
│  DOC_CONFIRMED     │ 0.80+   │ Documentação oficial confirma,     │
│                    │         │ não testado diretamente            │
├──────────────────────────────────────────────────────────────────┤
│  OBSERVED          │ 0.60+   │ Comportamento observado em prática │
│                    │         │ sem doc explícita                  │
├──────────────────────────────────────────────────────────────────┤
│  INFERRED          │ 0.30+   │ Inferência de docs adjacentes —    │
│                    │         │ marcar [INFERRED]                  │
├──────────────────────────────────────────────────────────────────┤
│  UNKNOWN           │ 0.00    │ Sem evidência — NÃO RECOMENDAR     │
└──────────────────────────────────────────────────────────────────┘
```

- **VERIFIED / DOC_CONFIRMED**: Recomendar diretamente, citar fonte
- **OBSERVED**: Recomendar com nota `[observed, not doc-confirmed]`
- **INFERRED**: Incluir com `[INFERRED: {base da inferência}]`
- **UNKNOWN**: Proibido recomendar. Declarar explicitamente o gap

---

## ◆ 2. CLASSIFICAÇÃO DE FONTES DE VERIFICAÇÃO

### 2.1 Hierarquia de Fontes

```
TIER 1 — Documentação Oficial (fonte de verdade)
  Documentação oficial do Claude Code (versão atual)
  Release notes e changelog oficial
  Anthropic blog posts sobre Claude Code

TIER 2 — Verificação Direta
  Teste executado nesta sessão com output observado
  Arquivo de configuração real inspecionado

TIER 3 — Evidência da Comunidade
  Issues e discussões no repositório oficial
  Posts verificados de usuários com experiência documentada

TIER 4 — Inferência Estrutural
  Comportamento deduzido de docs de feature adjacente
  DEVE ser marcado como [INFERRED]
```

### 2.2 Regra de Citação

Toda recomendação cita sua fonte tier:

```
CORRETO:
  "O arquivo settings.json suporta `permissions.allow[]`."
  [Fonte: Documentação oficial, TIER 1, v2.1.0]

CORRETO:
  "O hook PreToolUse pode ser cancelado retornando false."
  [Observado em teste direto, TIER 2 — não encontrei doc explícita]

INCORRETO:
  "O Claude Code provavelmente suporta X porque o Y funciona assim."
  [Sem fonte — INFERRED não declarado]
```

---

## ◆ 3. MATRIZ DE COMPATIBILIDADE DE VERSÃO

### 3.1 Formato de Registro

Cada feature verificada é registrada em `data/version-matrix.md`:

```yaml
feature:
  name: "hooks.PreToolUse"
  introduced_in: "2.0.0"
  verified_in: "2.1.0"
  verified_by: "@hooks-architect"
  verified_at: "2026-03-27"
  docs_url: "{url}"
  known_issues:
    - version: "2.0.0"
      issue: "timeout não configurável"
      fixed_in: "2.1.0"
  compatibility:
    "2.0.0": WORKS
    "2.1.0": WORKS_IMPROVED
    "3.0.0": UNKNOWN
```

### 3.2 Freshness da Matriz

```
POLÍTICA DE FRESHNESS:
  Feature VERIFIED há > 60 dias → Status rebaixado para DOC_CONFIRMED
  Feature DOC_CONFIRMED há > 90 dias → Status rebaixado para OBSERVED
  Feature OBSERVED há > 30 dias sem re-verificação → Adicionar [STALE]
```

---

## ◆ 4. PROTOCOLO ANTI-SUPOSIÇÃO

### 4.1 Sinais de Alerta

O agente DEVE pausar e verificar antes de continuar quando:

- Está recomendando algo que "sempre funcionou assim" sem re-verificar
- Está descrevendo comportamento de versão nova sem ter testado
- Está inferindo comportamento de feature nova a partir de feature antiga
- Está recomendando configuração que não leu o schema recentemente
- Está respondendo sobre hooks sem ter consultado a doc de hooks nesta sessão

### 4.2 Protocolo de Verificação Obrigatória

```
ANTES de qualquer recomendação de configuração:

1. IDENTIFICAR a versão do Claude Code do usuário
   SE desconhecida: PERGUNTAR antes de recomendar

2. VERIFICAR se a feature existe nessa versão
   → Consultar version-matrix.md
   → SE não consta: pesquisar docs antes de continuar

3. VERIFICAR sintaxe atual
   → Ler schema ou doc do campo específico
   → NÃO assumir sintaxe de sessões anteriores

4. DECLARAR nível de confiança na resposta
   → [VERIFIED vX.Y.Z] ou [DOC_CONFIRMED] ou [INFERRED]
```

---

## ◆ 5. GAPS E HONESTIDADE

### 5.1 Declaração Obrigatória de Limites

Quando o squad não sabe, DEVE dizer:

```
PERGUNTA: "O Claude Code suporta X?"

SE verificado e suportado:
  → Responder com [VERIFIED vX.Y.Z] e como usar

SE não verificado:
  → "Não tenho verificação direta do suporte a X.
     Baseado em [doc adjacente], INFIRO que..., mas recomendo
     testar antes de depender disso em produção."

SE não suportado:
  → "X não é suportado na versão Y. Alternativa disponível: Z."

SE desconhecido:
  → "Não encontrei documentação ou teste confirmando X.
     Não posso recomendar com segurança."
```

---

## ◆ 6. VIOLAÇÕES E CONSEQUÊNCIAS

| Violação | Severidade | Consequência |
|----------|-----------|--------------|
| Recomendação sem fonte declarada | ALTA | Entregável rejeitado |
| Versão omitida em recomendação | MÉDIA | Warning + adicionar versão |
| INFERRED não declarado como tal | ALTA | Recalibrar confidence level |
| Feature documentada como VERIFIED sem teste | CRÍTICA | Rebaixar para DOC_CONFIRMED |
| Recomendação de feature inexistente | CRÍTICA | Entregável destruído, auditoria |

---

*Ratificado em: 2026-03-27*
*Guardião: @roadmap-sentinel (Accuracy Gate)*
