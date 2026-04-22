---
researcher: <sage | scout | scholar>
topic: "<topic string>"
status: <complete | in_progress | failed>
searches: <integer>
extractions: <integer>
primary_sources: <integer>          # sage only — papers/RFCs/official docs
tools_shortlisted: <integer>        # scout only
papers_cited: <integer>             # scholar only
tier_breakdown:                     # scholar only
  tier_1: <integer>
  tier_2: <integer>
  tier_3: <integer>
  tier_4: <integer>
generated_at: <ISO-8601>
---

# Findings — <Researcher> on "<Topic>"

> **Note:** Section count and titles depend on researcher type:
> - **sage** → 6 sections (one per round): Foundations, Architecture & Mechanics, Best Practices, Advanced Considerations, Current State & Trends, Pitfalls & Anti-Patterns
> - **scout** → 3 sections (one per axis): Skills Marketplace, GitHub Libraries, Awesome-Lists & Curated Collections
> - **scholar** → 2 sections (one per phase): Seminal References, Current Research

## <Section Title>

### Summary

<3-5 sentence overview of what this section covers>

### Key Findings

- <Bullet 1>
- <Bullet 2>
- <Bullet 3>

### Extracted Passages

#### From <Source Name>

> <Verbatim quoted passage>

**Source:** <URL or DOI>
**Tier (scholar only):** <1 | 2 | 3 | 4>
**Maintenance verdict (scout only):** <🟢 Active | 🟡 Maintenance | 🔴 Stagnant>

### Citations

1. <Source 1 — title, author/maintainer, URL/DOI, accessed date>
2. <Source 2 — ...>

---

## Contested Findings (scholar only — optional block)

```yaml
contested:
  - claim: "<claim text>"
    side_a:
      position: "<position A>"
      citation: "<source A>"
    side_b:
      position: "<position B>"
      citation: "<source B>"
    note: "<context for the disagreement>"
```

---

## Coverage Self-Check

- Total searches in this run: <int>
- Total extractions in this run: <int>
- Status: <complete | failed>
- Failure reason (if failed): <text>
