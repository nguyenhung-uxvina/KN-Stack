---
name: helix-design-journal
description: Continuous design decision capture for Workshop X engineering sessions. This skill should be used when the user asks for "design journal", "nhật ký thiết kế", "log decision", "end of session", "journal entry", or when wrapping up a design session. Lowest urgency but highest compound value — decisions not recorded are decisions lost.
---

# Helix Design Journal — Session Decision Capture

Capture every design session's decisions, rationale, and rejected alternatives. The compound value of this journal grows exponentially — after 50 entries, pattern recognition becomes possible. After 200, institutional knowledge emerges.

## When to Use

- End of any design session (daily/per-session)
- After a significant design decision is made mid-session
- When user says "log this decision" or "record that we decided..."
- Weekly summary generation for helix-sync-protocol prep
- Monthly pattern analysis across projects

## Workflow

### Step 1: Gather Session Context

AI reads current project state:
1. `1_Projects/{{project}}/Status.md` — current phase, recent changes
2. Active ICD entries from helix-integration-debt (if interfaces discussed)
3. Current session conversation history — extract decisions made
4. Previous journal entries for this project (last 3) — continuity check

### Step 2: Generate Pre-Filled Entry

AI drafts the journal entry from session context. Human reviews and corrects.

```
============================================
   DESIGN JOURNAL — Entry #{{NNN}}
============================================

Date:       {{YYYY-MM-DD}}
Project:    {{project name}}
Phase:      {{current phase}}
Domain:     {{Mechanical / Electrical / AI / System}}
Duration:   {{estimated session time}}
Session ID: DJ-{{project-code}}-{{NNN}}

--- Decisions Made (B2 Governance pattern) ---
| # | Decision | Rationale | Alternatives Rejected | Confidence | Accountable Role | Escalation If Wrong |
|---|----------|-----------|----------------------|------------|-----------------|-------------------|
| 1 | | | | HIGH/MED/LOW | CEO / Domain Lead | |
| 2 | | | | | | |

--- Interface Impacts ---
| Decision # | ICD Affected | Change Required | Status |
|------------|-------------|-----------------|--------|
| 1 | IF-001-03 | Update mounting spec | Pending |

--- Integration Debt Changes ---
| Action | Debt-ID | Description |
|--------|---------|-------------|
| ADDED | D-005 | New thermal constraint from motor selection |
| RESOLVED | D-002 | Cable connector spec agreed |

--- Blocked Items ---
| Item | Blocked By | Needed From | Deadline |
|------|-----------|-------------|----------|
| Motor bracket design | Motor datasheet | Supplier | 2026-03-20 |

--- CEO Notes ---
(Human fills: strategic context, gut feelings, concerns not captured above)


--- AI-Assisted Work Summary ---
| Task | COD | Tool/Skill Used | Output |
|------|-----|----------------|--------|
| BOM weight calculation | O1 | Spreadsheet | 12.3 kg total |
| Concept sketch feedback | O2 | forge-shift | CONDITIONAL GO |

--- AI Output Failures (from Pattern Library Anti-Patterns) ---
| # | AI Output | Failure Type | Why Rejected | Pattern | Fix Applied |
|---|-----------|-------------|-------------|---------|-------------|
| 1 | [what AI generated] | AP-1/2/3/4/5 | [CEO reason] | [which anti-pattern] | [how corrected] |

Failure Types (Pattern Library Phần 5):
  AP-1: "Handle it" — AI given task without context → output missed key constraint
  AP-2: Ambiguous delegation — HW debug/architecture delegated → AI gave generic answer
  AP-3: VN military context — AI hallucinated TCVN/doctrine details
  AP-4: Skipped review — AI output used without check → error found later
  AP-5: Decision avoidance — AI asked to choose → CEO should have decided

Note: Log failures WITHOUT blame. Purpose is COMPOUND LEARNING:
  after 20+ failure entries → patterns emerge → delegation templates improve

============================================
```

### Step 3: Auto-Link to ICD

When journal entry mentions interface changes:
1. Cross-reference with helix-integration-debt registry
2. Flag any ICD entries that need updating
3. Generate change request if interface spec modified

### Step 4: Store Entry

Save to: `1_Projects/{{project}}/Phase{{N}}-{{name}}/journal/DJ-{{project-code}}-{{NNN}}.md`

If journal directory doesn't exist, create it.

### Step 5: Weekly Summary (Auto-Generated)

Every sync prep, AI aggregates journal entries into: key decisions with impact, integration debt delta (added/resolved/net), open blocked items, and time allocation by domain (Mech/Elec/AI/System).

### Step 6: Monthly Pattern Analysis

After 10+ entries per project, AI identifies patterns: decision category distribution (e.g., "70% of Phase 3 decisions involve thermal trade-offs"), recurring blockers with avg resolution time, domain generating most integration debt, and confidence level trends. Feed pattern insights to Galaxy as permanent note candidates.

## Integration

```
helix-design-journal READS FROM:
  - 1_Projects/*/Status.md → project context
  - helix-integration-debt → current ICD status for cross-reference
  - Session conversation → decisions made (AI extracts)
  - Previous journal entries → continuity and numbering

helix-design-journal WRITES TO:
  - helix-sync-protocol → weekly summary for sync prep
  - helix-integration-debt → ICD change flags from decisions
  - bridge-knowledge-base → Layer 3 tacit knowledge capture
  - 5_Galaxy/ → pattern insights as permanent note candidates
  - 1_Projects/*/Phase*/journal/ → journal entry files
```

## Rules

- Journal entries are APPEND-ONLY — never edit past entries, only add corrections as new entries
- "Alternatives Rejected" column is MANDATORY — rationale without rejected options is incomplete
- AI pre-fills but human MUST review — do not auto-save without confirmation
- Minimum 1 entry per design session — even "no decisions made, continued analysis" is valid
- Confidence level must be honest: LOW = "gut feeling", MED = "some evidence", HIGH = "data-backed"
- CEO Notes section is human-only — AI leaves blank for human input
- Weekly summaries auto-generated but CEO reviews before sync
- Reference: [[Retrieval Lớn Hơn Storage — Links Là Kiến Trúc Thật]] — journal value is in retrieval, not storage

## COD Classification

- Pre-filled template generation: Offload (O1) — AI reads context, formats
- ICD auto-linking: Offload (O1) — pattern matching against registry
- Weekly summary generation: Offload (O1) — AI aggregates entries
- Monthly pattern analysis: Offload (O2) — AI identifies trends, CEO validates
- Decision recording with rationale: **Core (C)** — human captures actual decisions
- "Alternatives Rejected" documentation: **Core (C)** — human recalls what was considered
- CEO Notes: **Core (C)** — non-delegable strategic context
- Galaxy note extraction from patterns: **Core (C)** — human judges what's permanent
