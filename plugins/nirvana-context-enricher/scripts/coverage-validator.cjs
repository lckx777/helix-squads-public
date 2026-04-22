#!/usr/bin/env node
'use strict';

/*
 * coverage-validator.cjs
 *
 * Chain gate helper for validateCoverageQuorum() (chain micro-task 4).
 * Parses YAML frontmatter from .nce/findings/{sage,scout,scholar}.md,
 * computes per-researcher and aggregate metrics, and renders pass/fail verdict.
 *
 * Exit codes:
 *   0  -> quorum passed
 *   1  -> quorum failed (one or more gates not met)
 *   2  -> parse / IO error
 *
 * Usage:
 *   node scripts/coverage-validator.cjs [findings_dir]
 *
 * Default findings_dir: .nce/findings
 *
 * Outputs:
 *   stdout -> JSON verdict object (one line)
 *   stderr -> human-readable progress / errors
 *
 * No external dependencies. Node.js stdlib only.
 */

const fs = require('fs');
const path = require('path');

const MIN_SAGE_SEARCHES = 6;
const MIN_SAGE_EXTRACTIONS = 6;
const MIN_SCOUT_SEARCHES = 3;
const MIN_SCOUT_EXTRACTIONS = 3;
const MIN_SCOUT_TOOLS = 5;
const MIN_SCHOLAR_SEARCHES = 2;
const MIN_SCHOLAR_PAPERS = 2;
const MIN_TOTAL_SEARCHES = 24;
const MIN_TOTAL_EXTRACTIONS = 11;

const RESEARCHERS = ['sage', 'scout', 'scholar'];

function parseFrontmatter(filePath) {
  let content;
  try {
    content = fs.readFileSync(filePath, 'utf8');
  } catch (error) {
    throw new Error(`IO failure reading ${filePath}: ${error.message}`);
  }

  const match = content.match(/^---\s*\n([\s\S]*?)\n---\s*\n/);
  if (!match) {
    throw new Error(`Missing or malformed YAML frontmatter in ${filePath}`);
  }

  const block = match[1];
  const fields = {};

  for (const rawLine of block.split('\n')) {
    const line = rawLine.trim();
    if (!line || line.startsWith('#')) continue;
    const sep = line.indexOf(':');
    if (sep === -1) continue;
    const key = line.slice(0, sep).trim();
    const valueRaw = line.slice(sep + 1).trim();
    if (!valueRaw) continue;

    const numeric = Number(valueRaw);
    if (!Number.isNaN(numeric) && /^-?\d+(\.\d+)?$/.test(valueRaw)) {
      fields[key] = numeric;
    } else {
      fields[key] = valueRaw.replace(/^['"]|['"]$/g, '');
    }
  }

  return fields;
}

function evaluateGates(findings) {
  const gates = [];
  const sage = findings.sage || {};
  const scout = findings.scout || {};
  const scholar = findings.scholar || {};

  gates.push({
    id: 'sage.status',
    passed: sage.status === 'complete',
    actual: sage.status,
    expected: 'complete',
  });
  gates.push({
    id: 'scout.status',
    passed: scout.status === 'complete',
    actual: scout.status,
    expected: 'complete',
  });
  gates.push({
    id: 'scholar.status',
    passed: scholar.status === 'complete',
    actual: scholar.status,
    expected: 'complete',
  });

  gates.push({
    id: 'sage.searches',
    passed: (sage.searches || 0) >= MIN_SAGE_SEARCHES,
    actual: sage.searches || 0,
    min: MIN_SAGE_SEARCHES,
  });
  gates.push({
    id: 'sage.extractions',
    passed: (sage.extractions || 0) >= MIN_SAGE_EXTRACTIONS,
    actual: sage.extractions || 0,
    min: MIN_SAGE_EXTRACTIONS,
  });
  gates.push({
    id: 'scout.searches',
    passed: (scout.searches || 0) >= MIN_SCOUT_SEARCHES,
    actual: scout.searches || 0,
    min: MIN_SCOUT_SEARCHES,
  });
  gates.push({
    id: 'scout.extractions',
    passed: (scout.extractions || 0) >= MIN_SCOUT_EXTRACTIONS,
    actual: scout.extractions || 0,
    min: MIN_SCOUT_EXTRACTIONS,
  });
  gates.push({
    id: 'scout.tools_shortlisted',
    passed: (scout.tools_shortlisted || 0) >= MIN_SCOUT_TOOLS,
    actual: scout.tools_shortlisted || 0,
    min: MIN_SCOUT_TOOLS,
  });
  gates.push({
    id: 'scholar.searches',
    passed: (scholar.searches || 0) >= MIN_SCHOLAR_SEARCHES,
    actual: scholar.searches || 0,
    min: MIN_SCHOLAR_SEARCHES,
  });
  gates.push({
    id: 'scholar.papers_cited',
    passed: (scholar.papers_cited || 0) >= MIN_SCHOLAR_PAPERS,
    actual: scholar.papers_cited || 0,
    min: MIN_SCHOLAR_PAPERS,
  });

  const totalSearches = (sage.searches || 0) + (scout.searches || 0) + (scholar.searches || 0);
  const totalExtractions =
    (sage.extractions || 0) + (scout.extractions || 0) + (scholar.extractions || 0);

  gates.push({
    id: 'aggregate.total_searches',
    passed: totalSearches >= MIN_TOTAL_SEARCHES,
    actual: totalSearches,
    min: MIN_TOTAL_SEARCHES,
  });
  gates.push({
    id: 'aggregate.total_extractions',
    passed: totalExtractions >= MIN_TOTAL_EXTRACTIONS,
    actual: totalExtractions,
    min: MIN_TOTAL_EXTRACTIONS,
  });

  return gates;
}

function determineRetryInstructions(gates) {
  const failingResearchers = new Set();
  for (const gate of gates) {
    if (gate.passed) continue;
    if (gate.id.startsWith('sage.')) failingResearchers.add('sage');
    else if (gate.id.startsWith('scout.')) failingResearchers.add('scout');
    else if (gate.id.startsWith('scholar.')) failingResearchers.add('scholar');
  }
  return Array.from(failingResearchers);
}

function main() {
  const findingsDir = process.argv[2] || '.nce/findings';

  const findings = {};
  for (const researcher of RESEARCHERS) {
    const filePath = path.join(findingsDir, `${researcher}.md`);
    try {
      findings[researcher] = parseFrontmatter(filePath);
    } catch (error) {
      process.stderr.write(`[coverage-validator] ${error.message}\n`);
      process.exit(2);
    }
  }

  const gates = evaluateGates(findings);
  const allPassed = gates.every((g) => g.passed);
  const retryInstructions = allPassed ? [] : determineRetryInstructions(gates);

  const verdict = {
    passed: allPassed,
    timestamp: new Date().toISOString(),
    findings_dir: findingsDir,
    gates,
    retry_instructions: retryInstructions,
  };

  process.stdout.write(JSON.stringify(verdict) + '\n');

  if (!allPassed) {
    const failed = gates.filter((g) => !g.passed).map((g) => g.id).join(', ');
    process.stderr.write(`[coverage-validator] FAILED gates: ${failed}\n`);
    process.exit(1);
  }

  process.stderr.write('[coverage-validator] all gates passed\n');
  process.exit(0);
}

main();
