---
task: indexSql()
responsavel: Cart SQL Digger
responsavel_type: Agente
atomic_layer: Molecule
workflow: cartographer-excavation
step: 4
Entrada:
- campo: migrations_path
  tipo: directory
  obrigatorio: true
  validacao: supabase/migrations/
- campo: last_hashes
  tipo: file
  obrigatorio: false
  validacao: squads/cartographer/.run/last-hashes.json
- campo: run_mode
  tipo: enum
  valores:
  - incremental
  - full
  obrigatorio: true
Saida:
- campo: sql_artifacts
  tipo: file
  destino: squads/cartographer/.run/digger-output/sql-artifacts.ndjson
  obrigatorio: true
- campo: schema_snapshot
  tipo: file
  destino: squads/cartographer/.run/schema-snapshot.yaml
  obrigatorio: true
- campo: digger_run_meta
  tipo: file
  destino: squads/cartographer/.run/digger-runs/sql-{run_id}.yaml
  obrigatorio: true
Checklist:
- '[ ] Migrations parsed in chronological order (timestamp prefix)'
- '[ ] CREATE TABLE, ALTER TABLE, DROP TABLE deltas applied in sequence'
- '[ ] Final schema state reflects all migrations'
- '[ ] RLS policies extracted per table'
- '[ ] Tables without RLS flagged rls_enabled: false'
- '[ ] FK dependency edges recorded'
- '[ ] pgvector columns tagged kind: vector_index'
- '[ ] schema_snapshot written with table count and timestamp'
- '[ ] Output NDJSON valid per digger-base-contract.md'
description: '- **ID:** index-sql'
---


# Task: Index SQL

## Metadata
- **ID:** index-sql
- **Workflow:** cartographer-excavation
- **Step:** 4
- **Agent:** cart-sql-digger
- **Parallel:** can run in parallel with steps 1-3

## Description
Parses Supabase migration files in chronological order to compute the current schema state.
Special handling for RLS policies (security signal) and pgvector columns (vector search infra).

## Pre-conditions
- `supabase/migrations/` directory exists
- Migration files have timestamp prefix (standard Supabase format: `YYYYMMDDHHMMSS_description.sql`)

## Execution Steps

1. List all files in `supabase/migrations/` sorted by filename (chronological by timestamp prefix)
2. For each migration file in order:
   a. Hash-check (if incremental and hash unchanged AND all later migrations also unchanged: use cached state)
   b. Parse SQL statements:
      - `CREATE TABLE` → new table artifact
      - `ALTER TABLE` → modify existing table artifact (add/drop columns)
      - `DROP TABLE` → mark table artifact as dropped
      - `CREATE POLICY` → RLS policy artifact linked to table
      - `CREATE INDEX` → index artifact (detect gin/gist/ivfflat for pgvector)
      - `CREATE FUNCTION` → plpgsql function artifact
      - `ALTER TABLE ... ADD CONSTRAINT ... FOREIGN KEY` → FK edge
3. After all migrations: finalize table artifacts with current column state
4. Flag tables with zero RLS policies as `rls_enabled: false`
5. Emit all artifacts to NDJSON
6. Write schema snapshot (table count, column count, RLS coverage %)

## Table Artifact Record
```json
{
  "id": "sql:table:public.agents",
  "kind": "table",
  "name": "agents",
  "schema": "public",
  "columns": [
    {"name": "id", "type": "uuid", "nullable": false, "default": "gen_random_uuid()"},
    {"name": "name", "type": "text", "nullable": false},
    {"name": "embedding", "type": "vector(1536)", "nullable": true}
  ],
  "rls_enabled": true,
  "rls_policies": ["agents_select_own", "agents_insert_authenticated"],
  "indexes": ["agents_embedding_idx"],
  "created_in_migration": "20260101000000_init.sql",
  "hash": "sha256:...",
  "digger": "cart-sql-digger"
}
```

## Gate
- Schema snapshot written
- At least one table artifact emitted (non-empty DB)
- All tables have explicit `rls_enabled` boolean
