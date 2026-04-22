---
name: memory-consolidate
persona_profile:
  archetype: Specialist
  communication:
    tone: technical
    style: formal
greeting_levels:
  brief: Agent ready.
  standard: Agent ready to help.
  detailed: Agent ready with full context.
task: memoryConsolidate()
responsavel: OracleCritic
responsavel_type: Agente
Entrada:
- campo: input
  tipo: string
  obrigatorio: true
  validacao: upstream artifact or user input
Saida:
- campo: output
  tipo: file
  obrigatorio: true
  destino: .run/{task}-output.yaml
Checklist:
- '[ ] Task completed'
atomic_layer: Molecule
description: Consolida aprendizados no grafo de conhecimento hierárquico do Oracle.
---

# memoryConsolidate() - Consolidate Learning

Consolida aprendizados no grafo de conhecimento hierárquico do Oracle.

**Inspired by:** Claude Code QueryEngine + memdir (512K lines DNA)

## Process

1. **Extract** - Parse transcript, identify patterns
2. **Analyze** - Calculate confidence scores  
3. **Enrich** - Generate embeddings (384d)
4. **Persist** - Update knowledge-graph.json
5. **Optimize** - Generate cost suggestions

---

**Oracle Memory** - Infinite retention 🧠✨

## Input
- `?` (string)
- `?` (object)
- `?` (array)
- `?` (object)

## Output
- `?` (object)
- `?` (object)
- `?` (number)
- `?` (array)

## Acceptance Criteria
- session_transcript file exists
- .oracle-state/ directory exists
- knowledge-graph.json updated
- At least 1 new node added
