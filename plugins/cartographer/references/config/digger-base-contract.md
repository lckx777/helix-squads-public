# Digger Base Contract

> AgentDropout Result: ts-digger and py-digger share this base contract.
> All 4 diggers follow the same NDJSON output schema and hash-gate protocol.
> Language boundary and parser tooling differ — the artifact schema is identical.

## Artifact Record Schema (NDJSON — one JSON object per line)

```typescript
interface ArtifactRecord {
  // Identity
  id: string;          // Format: "{digger_prefix}:{package_or_module}:{name}"
                       // Examples: "ts:pipeline-engine:canProceed", "py:hook:gate-enforcement", "yaml:squad:copy-chief"
  kind: ArtifactKind;  // See enum below
  name: string;        // Human-readable name

  // Location
  file_path: string;   // Relative to monorepo root
  package?: string;    // npm package name (TS artifacts)
  module?: string;     // Python module path (PY artifacts)
  schema?: string;     // DB schema name (SQL artifacts — default: "public")
  squad?: string;      // Squad name (YAML artifacts)
  line_start?: number;
  line_end?: number;

  // Content
  signature?: string;  // Simplified type signature or schema shape
  description?: string; // Extracted from JSDoc, docstring, or YAML description field
  exported?: boolean;  // TS: is this exported? Default true for catalog entries.
  dynamic?: boolean;   // PY: defined at runtime (decorator magic etc)

  // Kind-specific fields
  hook_event?: string;       // PY hooks: "PreToolUse"|"PostToolUse"|"SessionStart"|"Stop"|"UserPromptSubmit"
  timeout?: number;          // PY hooks: timeout in seconds
  exit_codes?: object;       // PY hooks: {0: "success", 1: "warning", 2: "block"}
  keywords?: string[];       // SKILL artifacts: auto-trigger keywords
  priority?: string;         // SKILL artifacts: "ALTA"|"MEDIA"|"BAIXA"
  tools?: string[];          // Agent/SKILL artifacts: allowed tools list
  model?: string;            // Agent artifacts: claude model name
  rls_enabled?: boolean;     // SQL table artifacts
  rls_policies?: string[];   // SQL table artifacts: policy names
  orchestrator?: string;     // Squad artifacts: orchestrator agent name
  tiers?: object;            // Squad artifacts: {opus: [...], sonnet: [...]}

  // Dependencies
  dependencies: DependencyEdge[];

  // Excavation metadata
  hash: string;        // SHA256 of file content — "sha256:{hex}"
  digger: string;      // "cart-ts-digger"|"cart-py-digger"|"cart-yaml-digger"|"cart-sql-digger"
  run_id: string;      // Format: "{lang}-{YYYYMMDD}-{NNN}"
  timestamp: string;   // ISO 8601
}

type ArtifactKind =
  // TypeScript
  | "function" | "class" | "type" | "interface" | "constant" | "enum"
  // Python
  | "py_function" | "py_class" | "hook" | "skill"
  // YAML/Config
  | "agent" | "squad" | "task" | "workflow" | "chain" | "rule" | "mcp_server"
  // SQL
  | "table" | "rls_policy" | "index" | "vector_index" | "trigger" | "sql_function" | "migration";

interface DependencyEdge {
  from: string;   // artifact ID or package name
  symbol?: string; // specific symbol being imported (if applicable)
  to: string;     // artifact ID or package name
  type: "import" | "extends" | "implements" | "foreign_key" | "calls" | "external_call" | "squad_dep";
}
```

## Hash-Gate Protocol (ALL diggers)

```
1. Load last-hashes.json: { "path/to/file.ts": "sha256:abc..." }
2. For each file in scope:
   a. Compute SHA256(file_content)
   b. If hash == last-hashes[file_path] AND mode == "incremental": SKIP
   c. Else: PARSE and update hash
3. After all files: write updated last-hashes.json
```

## NDJSON Output Rules

- One JSON record per line (no pretty-print)
- UTF-8 encoding
- File truncated and rewritten each run (not appended — avoids stale records)
- Empty file is valid (zero artifacts in scope)

## Digger Prefix Map

| Digger | ID Prefix | Output File |
|--------|-----------|-------------|
| cart-ts-digger | `ts:` | `.run/digger-output/ts-artifacts.ndjson` |
| cart-py-digger | `py:` | `.run/digger-output/py-artifacts.ndjson` |
| cart-yaml-digger | `yaml:` | `.run/digger-output/yaml-artifacts.ndjson` |
| cart-sql-digger | `sql:` | `.run/digger-output/sql-artifacts.ndjson` |
