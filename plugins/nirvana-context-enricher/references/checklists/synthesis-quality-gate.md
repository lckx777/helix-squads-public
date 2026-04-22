# Synthesis Quality Gate

> **Owner:** Lotus
> **When to run:** After `synthesizeContextReport()` writes `.nce/report.md`, before handoff to Nirva
> **Purpose:** Self-review of the 16-section report before delivery

## Section Completeness (BLOCKER — all must pass)

- [ ] Section 1 (Executive Summary) is non-empty AND ≤ 500 words
- [ ] Section 2 (Topic Definition) is non-empty
- [ ] Section 3 (Historical Context) is non-empty
- [ ] Section 4 (Core Architecture & Mechanics) is non-empty
- [ ] Section 5 (Theoretical Foundations) is non-empty
- [ ] Section 6 (Best Practices) is non-empty
- [ ] Section 7 (Advanced Considerations) is non-empty
- [ ] Section 8 (Current State & Trends) is non-empty
- [ ] Section 9 (Ecosystem Map — Skills) is non-empty
- [ ] Section 10 (Ecosystem Map — Libraries) is non-empty
- [ ] Section 11 (Ecosystem Map — Curated Collections) is non-empty
- [ ] Section 12 (Recommended Tools Shortlist) is non-empty AND ≥ 3 tools
- [ ] Section 13 (Academic References) is non-empty AND ≥ 2 papers with citations
- [ ] Section 14 (Common Pitfalls & Anti-Patterns) is non-empty
- [ ] Section 15 (Contested Findings) is present (may be "none surfaced" if applicable)
- [ ] Section 16 (Knowledge Gaps & Open Questions) is non-empty

## Traceability (BLOCKER)

- [ ] Every Section 9-12 tool entry traces to scout findings
- [ ] Every Section 13 paper traces to scholar findings with DOI / stable URL
- [ ] Every Section 14 anti-pattern traces to sage round 6
- [ ] Section 15 disagreements cite both sides with sources
- [ ] Source map header lists `sources_cited` count > 0

## Conflict Resolution Discipline (BLOCKER)

- [ ] No silent winner-picking — disagreements appear in Section 15, not buried
- [ ] No claim appears in body without a citation (zero unattributed claims)
- [ ] Tier-4 (preprint-only) sources are tagged explicitly

## Frontmatter (BLOCKER)

- [ ] YAML frontmatter present and parseable
- [ ] `synthesizer: lotus`
- [ ] `topic` matches `.nce/request.md`
- [ ] `sections: 16`
- [ ] `coverage` block has all 4 numeric fields
- [ ] `generated_at` is ISO-8601

## Soft Quality (WARNING — log but proceed)

- [ ] No section exceeds 2000 words (readability target)
- [ ] At least 1 tier-1 or tier-2 academic source in Section 13
- [ ] At least 1 🟢 Active library in Section 10
- [ ] Section 16 lists ≥ 1 open question (rarely zero gaps in genuine research)

## Outcome

- **All blockers pass** → return `quality=passed`, hand off to Nirva
- **Any blocker fails** → retry composition once with explicit gap directive; if retry also fails, emit partial report with flagged gaps in Section 16 and surface error to user
