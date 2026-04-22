# Stack Auditors — Invocation Rules

> Executable rules engine for when to invoke which mentor. Complements `.claude/rules/sa-activation.md` (path-based rules) with semantic rules.

## Rules of Engagement

### RULE 1 — Evidence-first, opinion-never

**Every** mentor invocation MUST invoke the mentor's fundamentation skill BEFORE producing a verdict. Verdict text MUST cite evidence from skill output.

Violation → verdict rejected by `veredict-quality-gate` checklist → chain aborts.

### RULE 2 — Path takes precedence over opinion

If `.claude/rules/sa-activation.md` matches a path, the corresponding mentor is invoked regardless of AIOX agent's opinion about need. Primary agent may bypass with explicit `sa-skip: true` + justification.

### RULE 3 — Single mentor > council when possible

Council (parallel) is expensive (N latency + synthesis time). Prefer single-mentor-audit when:
- Domain is unambiguous
- Question is specific
- No architectural dimension

Promote to council ONLY when >1 domain is clearly affected.

### RULE 4 — Debate over synthesis for philosophical tensions

If the question has productive-tension dimension (see `persona-catalog.md` debate candidates table), USE `debate-sequence` instead of `council-audit-parallel`. Synthesis-washing kills the information; debate preserves it.

### RULE 5 — Pre-impl audit for COMPLEX stories ONLY

Don't invoke `pre-implementation-audit` for SIMPLE/STANDARD stories. Complexity is determined by:
- Story frontmatter `complexity: XL | COMPLEX`
- OR >16 story points
- OR explicit `sa-review-required: true`

Over-invocation = theater risk.

### RULE 6 — Post-impl review for high-stakes PRs ONLY

Triggers (any):
- PR touches `packages/vps-api/auth/**` OR other security-critical paths
- PR >500 LOC changed
- PR changes public API
- PR contains migrations
- PR description has `sa-review-required: true`

Not every PR needs mentor review. Default = skip.

### RULE 7 — Defer-to respected

If sa-jobs defers to sa-schneier (per catalog), and both have opinions, sa-schneier wins. sa-council synthesis must reflect this.

### RULE 8 — Challenges surface, don't block

If sa-carmack challenges sa-musk's position (per catalog), the challenge is recorded but doesn't veto. Only `blocked` verdicts veto.

### RULE 9 — Journey log is non-negotiable

Every invocation → journey log entry. Including bypasses. Including synthesis. Without journey log, observability fails, `decision_changed` can't be computed, kill/expand criterion doesn't work.

### RULE 10 — Kill criterion respected

If any mentor's `decision_changed` rate is <5% for 30 consecutive days:
1. Flag in weekly review
2. After 2 weeks of flagging, deactivate that specific mentor (not whole squad)
3. Mentor's native loader stays (for historical audits) but rule triggers removed

If squad-wide `decision_changed` rate <10% for 30 days:
- Remove squad entirely (Alan's BS3 criterion)
- Archive artifacts
- Document lessons learned in ADR

---

## Priority Matrix (when multiple rules apply)

```
Priority 1 (highest): RULE 1 (evidence-first)
Priority 2:           RULE 2 (path precedence)
Priority 3:           RULE 7 (defer-to)
Priority 4:           RULE 4 (debate for tension)
Priority 5:           RULE 5/6 (selective invocation)
Priority 6:           RULE 3 (single over council)
```

---

## Examples

### Example 1 — Clear domain
**Input:** "Audit the new Python script in mega-brain/tools/extractor.py"
**Routing:** RULE 3 (single mentor), RULE 2 (path → sa-van-rossum)
**Chain:** single-audit-chain
**Mentor:** sa-van-rossum
**Skill:** sa-van-rossum-lint

### Example 2 — Security-sensitive
**Input:** "Review the auth middleware refactor"
**Routing:** RULE 2 (path `packages/vps-api/auth/**` → sa-schneier), RULE 7 (sa-jobs would defer anyway)
**Chain:** single-audit-chain
**Mentor:** sa-schneier
**Skill:** sa-schneier-threat

### Example 3 — Architectural decision
**Input:** "Should we decompose the monolith queue-worker into 3 services?"
**Routing:** RULE 4 (philosophical tension → debate)
**Chain:** debate-chain
**Mentors:** sa-newman (pro-decomposition) vs sa-musk (vertical integration)
**Outcome:** synthesis with situational recommendation

### Example 4 — UI change
**Input:** "New component hub/src/lib/components/DecisionPicker.svelte"
**Routing:** RULE 2 (path → sa-jobs + sa-norman both)
**Chain:** council-parallel-chain (2 mentors)
**Mentors:** sa-jobs + sa-norman

### Example 5 — Trivial change
**Input:** "Fix typo in docs/README.md"
**Routing:** skip — trivial, no mentor invoked
**Action:** none. Not worth overhead.

### Example 6 — Repeat audit (bypass)
**Input:** "Review same auth middleware I reviewed 2 days ago"
**Routing:** check journey log; if sa-schneier verdict found <7 days, reuse
**Action:** no new invocation, cite prior verdict

---

## References

- Path rules: `.claude/rules/sa-activation.md`
- Catalog: `./persona-catalog.md`
- Checklist enforcement: `../checklists/veredict-quality-gate.md`
- Observability: `.claude/stack-auditors/README.md`
