# Checklist: Veredict Quality Gate

> Pre-commit gate for every stack-auditors verdict. Prevents theater — ensures each verdict is evidence-based, specific, and actionable.

**Invoked by:** sa-council after every chain completion, before journey log write.
**Enforcer:** sa-council
**Blocks:** journey log write if any MUST item fails

---

## MUST (blocking — verdict rejected if any fails)

- [ ] **M1 — Evidence cited:** Verdict text contains at least one concrete data point from `skill_evidence`. Pattern: "{number} {unit}" OR "{file}:{line}" OR "{metric}: {value}". Generic praise/concerns without numbers = FAIL.

- [ ] **M2 — Verdict is one of {approved, concerns, blocked, advisory}:** No invented verdict labels. No "probably ok" / "tentatively" — must pick a category.

- [ ] **M3 — Summary ≤500 chars:** Terse, scannable. Long prose belongs in journey log `verdict_text` field, not summary.

- [ ] **M4 — Traceable to skill output:** If `skill_invoked` is not null, `verdict_summary` must reference at least one field from skill output schema. Example: "per skill `sa-carmack-bench`, regression_pct 3.2%".

- [ ] **M5 — Story/context reference:** Either `story_ref` or `context_path` populated. Anonymous verdicts rejected.

- [ ] **M6 — No contradiction with skill_evidence:** If skill output has `verdict_hint: blocked`, mentor verdict cannot be `approved` without justification in verdict_summary.

## SHOULD (warnings — logged but not blocking)

- [ ] **S1 — Decision_changed field populated:** Mentor should record whether verdict altered primary agent's direction. Unfilled = warn; blank rate >30% = squad health issue.

- [ ] **S2 — Mentor cites other mentors (where relevant):** For cross-domain verdicts, mentor should acknowledge sister-mentor perspective. Example: sa-carmack reviewing perf should note sa-stonebraker if DB involved.

- [ ] **S3 — Actionable recommendations:** Verdict should end with 1-2 concrete actions (refactor X, add index Y, rotate key Z). Pure diagnostic verdicts (no action) = warn.

- [ ] **S4 — Reasonable latency:** `latency_ms < 10000` (10s). Slow verdicts indicate skill issues or context overload.

## Logged-only (informational)

- **L1 — Council-only:** sa-council verdicts (orchestrator) don't require skill_evidence — exempt from M4.
- **L2 — Bypass records:** bypass entries (sa-skip: true) exempt from M1-M4 but must have `bypass_justification`.

---

## Enforcement

This checklist runs as part of the `single-audit-chain` mt004 (`log_journey`) and `council-parallel-chain` mt004. If any MUST fails, chain returns error and journey log is NOT written.

Mentor is prompted to revise verdict citing the specific failure.

## Rationale

From Alan consultation 2026-04-18:
> "Todo mentor sem evidência é alucinação empacotada em autoridade. Carmack sem benchmark real é LinkedIn influencer. [F004 — Evidência vale mais que promessa]."

This gate operationalizes that principle — prevents the squad from devolving into opinion-as-authority over time.
