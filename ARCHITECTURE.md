# Arquitetura Squads — Source of Truth & Distribuição

**Status:** v1.0.0 (2026-04-22) · Ativo
**Owner:** lucapimenta (@lckx777)
**Última revisão:** 2026-04-22

Este documento é a **fonte canônica** da arquitetura de distribuição dos
squads do ecossistema Helix. Qualquer dúvida sobre onde um squad vive, como
editá-lo, como instalá-lo num projeto novo — começa aqui.

---

## TL;DR

```
┌─────────────────────────────────────────────────────────────────┐
│                        Source of Truth                          │
│                                                                 │
│  ~/.claude/skills/squads/squads/  (git repo)                    │
│  remote: lckx777/helix-squads-sot  (privado)                    │
│                                                                 │
│  18 squads canônicos (16 ativos + 1 placeholder + _example)     │
└─────────────────────┬──────────────────────┬────────────────────┘
                      │                      │
          auto-sync   │                      │   consumo direto
          (post-commit hook)                 │   (symlink)
                      │                      │
                      ▼                      ▼
        ┌─────────────────────────┐    ┌──────────────────────┐
        │ Marketplaces            │    │ Projetos consumidores│
        │                         │    │                      │
        │ helix-squads-public     │    │ copywriting-ecosystem│
        │   (8 plugins, público)  │    │ HelixOS              │
        │                         │    │ ads-dashboard        │
        │ helix-squads-private    │    │                      │
        │   (9 plugins, privado)  │    │ (todos via symlink)  │
        └─────────────────────────┘    └──────────────────────┘
                 │                                │
                 │                                │
        ┌────────┴──────────────┐       ┌────────┴────────────┐
        │ Install em qq lugar:  │       │ Edição local:       │
        │ claude plugin         │       │ cd squads/          │
        │   marketplace add     │       │ vim squad.yaml      │
        │   lckx777/helix-...   │       │ (symlink → SoT)     │
        └───────────────────────┘       └─────────────────────┘
```

---

## Os 3 repos GitHub

| Repo | Visibilidade | Conteúdo | Tamanho |
|------|--------------|----------|---------|
| [`lckx777/helix-squads-sot`](https://github.com/lckx777/helix-squads-sot) | Privado | Canonical SoT (18 squads + conversor + hooks) | 51M |
| [`lckx777/helix-squads-public`](https://github.com/lckx777/helix-squads-public) | Público | 8 plugins Claude Code — infra/meta (zero-config) | 6.2M |
| [`lckx777/helix-squads-private`](https://github.com/lckx777/helix-squads-private) | Privado | 9 plugins Claude Code — IP-proprietary | 22M |

**Repos arquivados:**
- [`lckx777/helix-squads`](https://github.com/lckx777/helix-squads) — formato legacy pi-squad-loader. ARCHIVED 2026-04-22.

---

## Os 18 squads

### Públicos (8) — infra/tooling (repo `helix-squads-public`)

Instalação zero-config:
```bash
claude plugin marketplace add lckx777/helix-squads-public
claude plugin install <nome>@helix-squads-public
```

| Squad | Propósito | Agents | Skills |
|-------|-----------|-------:|-------:|
| `cartographer` | Arqueologia de ecossistema (REUSE > ADAPT > CREATE) | 7 | 9 |
| `claude-code-mastery` | Expertise Claude Code (hooks, skills, MCP, plugins) | 8 | 26 |
| `incident-response-squad` | DevOps/SRE — logs, RCA, runbooks, post-mortems | 5 | 6 |
| `nirvana-context-enricher` | Enrichment paralelo para briefings arquiteturais | 5 | 9 |
| `nirvana-squad-creator` | Gera squads AIOS a partir de linguagem natural | 9 | 10 |
| `oracle-supreme-squad` | Extração do DNA do Claude Code | 5 | 1 |
| `stack-auditors` | Council de mentores históricos (Carmack, Jobs, Beck, etc.) | 12 | 9 |
| `synthetic-intelligence-factory` | Meta-system pra manufaturar inteligências sintéticas | 6 | 4 |

### Privados (9) — IP proprietário (repo `helix-squads-private`)

Instalação via bootstrap (requer `gh auth`):
```bash
curl -fsSL https://raw.githubusercontent.com/lckx777/helix-squads-private/main/install.sh | bash
claude plugin install <nome>@helix-squads-private
```

| Squad | Propósito | Version |
|-------|-----------|---------|
| `aios-forge-squad` | Desenvolvimento, otimização e evolução do próprio AIOS | 1.0.2 |
| `brandcraft-nirvana` | Harness-engineered branding (extract assets, tokens) | 4.0.0 |
| `content-radar` | Spy de ads + triple-source research (Apify+Brave+Exa) | 2.4.0 |
| `copy-chief` | Direct Response copy squad (HELIX briefing, DRE-First) | 3.0.0 |
| `fabrica-de-genios` | Pipeline industrial de mind-clones de IA | 1.0.0 |
| `fabrica-de-genios-source` | Constitution + protocols da fábrica de gênios | 1.0.0 |
| `helix-truth-engine` | HelixOS judgment layer — 11-agent reasoning mesh | 0.3.4 |
| `instagram-intelligence-nirvana` | Instagram intelligence NIRVANA v5.4 | 5.4.0 |
| `roteiro-factory` | MAAP weekly guide production | 4.0.0 |

### Placeholder (1) — não publicado

- `aiox-dev-squad` — virtual marker; agentes reais vivem em `framework/development` do AIOX core.

### Template (1) — base para squads novos

- `_example` — copiar daqui quando criar um squad novo.

---

## Consumidores (projetos)

Todos consomem via symlink:

| Projeto | Path | Uso |
|---------|------|-----|
| `copywriting-ecosystem` | `squads/` → SoT | Produção de copy DR + ofertas |
| `HelixOS` | `squads/` → SoT | Workbench/agent-OS — research e planejamento |
| `ads-dashboard` | `squads/` → SoT | Dashboard de ads (Next.js) |

**Futuro projeto novo:** apenas rode `claude plugin marketplace add lckx777/helix-squads-public` e os 8 públicos ficam disponíveis imediatamente. Para os privados, rode o install.sh.

---

## Contratos de edição

### Como editar um squad

```bash
# 1. Edit em qualquer consumer (symlink) OU direto no SoT
cd ~/HelixOS/squads/copy-chief     # symlink
# ou
cd ~/.claude/skills/squads/squads/copy-chief    # direto

vim squad.yaml                      # mesma coisa — vai pro SoT

# 2. Commit no SoT (único lugar git)
cd ~/.claude/skills/squads/squads
git add copy-chief/
git commit -m "feat: update copy-chief"
# Post-commit hook AUTOMATICAMENTE:
#   - detecta copy-chief mudou
#   - re-converte pra plugin
#   - commita + pusha no marketplace privado
#   - (30s depois: lckx777/helix-squads-private tem v3.0.1)

# 3. Push do SoT pra remote (opcional, recomendado)
git push origin main
```

### Como adicionar um squad novo

```bash
# 1. Scaffold
cd ~/.claude/skills/squads/squads
cp -r _example meu-squad-novo
# Edit squad.yaml + agents/ + tasks/ + etc.

# 2. Decidir público ou privado
# Editar arrays PUBLIC_SQUADS ou PRIVATE_SQUADS em:
#   ~/.claude/skills/squads/squads/.git/hooks/post-commit

# 3. Commitar — hook publica automaticamente
git add meu-squad-novo
git commit -m "feat: new squad meu-squad-novo"
git push
```

### Como desabilitar sync automático (emergência)

```bash
# Opção 1 — commit sem sync
cd ~/.claude/skills/squads/squads
git -c hooks.post-commit-sync=false commit -am "emergency"

# Opção 2 — disable total
chmod -x .git/hooks/post-commit
# (reabilite depois: chmod +x .git/hooks/post-commit)
```

---

## Regras de sanidade

1. **Nunca edite em um marketplace diretamente** — plugins são gerados a partir do SoT. Edit no marketplace será sobrescrito no próximo sync.
2. **Nunca crie `squads/` físico num projeto** — use symlink pro SoT OU instale via marketplace. Cópia física = drift inevitável.
3. **`.backup/`, `.bak`, `.pre-*`, `.venv/`, `node_modules/` são gitignored no SoT** — não commite por acidente.
4. **Sempre git push** no SoT pra persistir. Local-only = risco de perda se o WSL for wipado.
5. **`aiox-dev-squad` é placeholder intencional** — não tentar "completar".

---

## Hooks git instalados no SoT

| Hook | O que faz |
|------|-----------|
| `pre-commit` | Valida YAML dos squad.yaml tocados + bloqueia `.bak` staged |
| `post-commit` | Detecta squad modificado → re-converte plugin → commit+push marketplace |

Código em `~/.claude/skills/squads/squads/.git/hooks/`.

---

## Histórico

- **2026-04-22** v1.0.0 release
  - SoT git-ificado + remote `lckx777/helix-squads-sot`
  - Public marketplace v1.0.0 (8 plugins)
  - Private marketplace v1.0.0 (9 plugins)
  - 3 projetos migrados pra consumir via symlink (copywriting-ecosystem, HelixOS, ads-dashboard)
  - Legacy `lckx777/helix-squads` (pi-squad-loader format) arquivado
  - Hooks pre-commit + post-commit instalados

---

## Suporte

Problemas ou dúvidas: abrir issue em `lckx777/helix-squads-sot`.

Para a arquitetura pública, ver `README.md` de cada repo:
- [SoT README](https://github.com/lckx777/helix-squads-sot/blob/main/README.md)
- [Público README](https://github.com/lckx777/helix-squads-public/blob/main/README.md)
- [Privado README](https://github.com/lckx777/helix-squads-private/blob/main/README.md)
