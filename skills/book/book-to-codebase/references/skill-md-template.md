# SKILL.md Templates — book-to-codebase R6

> Used by `/btc-scaffold` (Block R6). One template per `concept_kind`.
> R6 selects the matching template, fills fields from `R2-Extraction-Manifest.md` + `R4-Architecture.md` + `R5-Ambiguity-Ledger.md`.
> Fields in `{{double braces}}` are filled by R6. Fields marked `[auto]` are computed. Fields marked `[CEO]` are left blank until CEO Core review.

---

## Template 1 — `decision_rule`

```markdown
---
name: {{skill-name}}
description: "{{one-line: when to apply this decision rule, what it decides, and the key constraint. ~80 chars. No emojis.}}"
---

# {{Skill Display Name}}

> **Kind:** decision_rule
> **Source:** {{book title}}, Ch{{N}} — "{{chapter title}}"
> **Confidence:** {{high | medium | low}} ({{Apply This | prose-derived | R2.1 derivation}})

## Rule

**Trigger:** {{when to apply — condition or context}}
**Decision:** {{what to decide}}
**Default:** {{what to do if no other signal — from R5 defaults if null}}

## Rationale

{{why this rule exists — from book; 2-4 sentences. If not stated in book: "Not explicitly stated. Inferred from: {{evidence}}."}}

## Application

```
WHEN: {{trigger condition}}
  AND: {{secondary condition if any — or omit}}
THEN: {{action}}
UNLESS: {{exception — or omit if none}}
```

## Boundaries

- **In scope:** {{contexts where this rule applies}}
- **Out of scope:** {{contexts where this rule does NOT apply — if stated}}
- **Common misapplication:** {{anti_pattern_guard from same chapter — if any}}

## Integration

```
{{skill-name}} READS:
  - [context inputs required to apply the rule]

{{skill-name}} INFORMS:
  - [downstream skills or decisions that depend on this rule's output]
```
```

---

## Template 2 — `architectural_principle`

```markdown
---
name: {{skill-name}}
description: "{{one-line: the principle stated as an actionable imperative. ~80 chars.}}"
---

# {{Skill Display Name}}

> **Kind:** architectural_principle
> **Source:** {{book title}}, Ch{{N}} — "{{chapter title}}"
> **Confidence:** {{high | medium | low}}

## Principle

{{The principle in one crisp sentence — from Apply This or Q3 extraction.}}

## Evidence

{{How the author supports this principle: example, case study, argument. 3-6 sentences.}}

## Scope

- **Applies at:** {{system level | component level | process level | all levels}}
- **Applies when:** {{conditions under which this principle is operative}}
- **Supersedes:** {{principles or defaults this overrides — if stated}}

## How to Apply

1. {{Step 1}}
2. {{Step 2}}
3. {{Step 3}}
*(Add or remove steps to match extraction — use null if book does not specify sequence)*

## Violation Indicators

{{Symptoms that this principle is being violated — from Q4 anti-patterns in same chapter, or null.}}

## Integration

```
{{skill-name}} CALLED BY:
  - [pipeline or skill that invokes this principle as a check]

{{skill-name}} INFORMS:
  - [downstream skills or artifacts affected by this principle]
```
```

---

## Template 3 — `mechanism`

```markdown
---
name: {{skill-name}}
description: "{{one-line: what process this runs, what it consumes, what it produces. ~80 chars.}}"
---

# {{Skill Display Name}}

> **Kind:** mechanism
> **Source:** {{book title}}, Ch{{N}} — "{{chapter title}}"
> **Confidence:** {{high | medium | low}}

## What This Does

{{1-2 sentences describing the mechanism's purpose and effect.}}

## Inputs

{{inputs required — from Q2 / R2.1 derivation. If null after R5: "[unspecified — use judgment]"}}

## Steps

1. {{Step 1}}
2. {{Step 2}}
3. {{Step 3}}
*(null steps → "[not specified — infer from context]")*

## Outputs

{{outputs produced — from Q2 / R2.1. If null: "[unspecified — document your output]"}}

## Stopping Condition

{{when this mechanism terminates — from Q2 / R2.1. If null: "[not specified — stop when output is stable]"}}

## Notes

{{Any constraints, warnings, or caveats from the book. If none: omit this section.}}

## Integration

```
{{skill-name}} READS:
  - [upstream artifacts or context it consumes]

{{skill-name}} PRODUCES:
  - [what it hands off to downstream]

{{skill-name}} CALLED BY:
  - [orchestrator or pipeline that invokes this]
```
```

---

## Template 4 — `discipline_contract`

```markdown
---
name: {{skill-name}}
description: "{{one-line: the ongoing commitment, its cadence, and what breaks without it. ~80 chars.}}"
---

# {{Skill Display Name}}

> **Kind:** discipline_contract
> **Source:** {{book title}}, Ch{{N}} — "{{chapter title}}"
> **Confidence:** {{high | medium | low}}

## The Contract

{{The discipline stated as a non-negotiable commitment. 1-3 sentences.}}

## Cadence

- **Frequency:** {{daily | weekly | per-project | event-triggered | {{null → "[not specified]"}}}}
- **Duration:** {{how long each instance takes — if stated}}
- **Trigger:** {{what initiates each instance — if stated}}

## Required Inputs

{{what you need to perform this discipline — tools, data, time, attention}}

## Non-Compliance Consequence

{{what breaks or degrades if you skip this — from Q6 or Q4. If null: "[not explicitly stated]"}}

## Minimum Viable Version

{{The simplest form of this discipline that still provides value — if the author specifies a "lite" version. Otherwise: omit.}}

## Integration

```
{{skill-name}} SCHEDULED BY:
  - [hook, cron, or session trigger that invokes this]

{{skill-name}} FEEDS INTO:
  - [what benefits from this discipline being maintained]
```
```

---

## Template 5 — `compounding_loop`

```markdown
---
name: {{skill-name}}
description: "{{one-line: the loop's name, its reinforcing mechanism, and direction (virtuous/vicious). ~80 chars.}}"
---

# {{Skill Display Name}}

> **Kind:** compounding_loop
> **Source:** {{book title}}, Ch{{N}} — "{{chapter title}}"
> **Confidence:** {{high | medium | low}}

## The Loop

{{Name and 1-2 sentence description of the feedback cycle.}}

**Direction:** {{virtuous | vicious | context-dependent}}

## Mechanics

```
TRIGGER → [what starts it]
    ↓
REINFORCING MECHANISM → [what amplifies each cycle]
    ↓
COMPOUNDING EFFECT → [what grows or degrades over time]
    ↓
BREAK CONDITION → [what interrupts the loop — null if not stated]
```

## Activation

{{How to intentionally enter the virtuous version — from Apply This or Q5. If vicious: how to exit.}}

## Warning Signs

{{Early indicators that the loop has inverted (virtuous → vicious) — from Q4/Q8. If null: omit.}}

## Integration

```
{{skill-name}} ACTIVATED BY:
  - [action, skill, or habit that starts the loop]

{{skill-name}} AMPLIFIES:
  - [downstream capabilities that compound]
```
```

---

## Template 6 — `anti_pattern_guard`

```markdown
---
name: {{skill-name}}
description: "{{one-line: the trap name, its symptom, and the remedy. ~80 chars.}}"
---

# {{Skill Display Name}}

> **Kind:** anti_pattern_guard
> **Source:** {{book title}}, Ch{{N}} — "{{chapter title}}"
> **Confidence:** {{high | medium | low}}

## The Trap

{{Name and 1-2 sentence description of the anti-pattern.}}

## How to Recognize It

**Symptom:** {{observable signs — from Q4}}
**Trigger context:** {{conditions that make this trap likely}}

## Root Cause

{{Why this anti-pattern emerges — from Q4. If null: "[not explicitly stated]"}}

## Remedy

{{What to do instead — from Q4 or Apply This. If null: "[not specified — return to first principles]"}}

## Prevention

{{How to avoid falling into this trap in the first place — from Q4 or Q6. If null: omit.}}

## Integration

```
{{skill-name}} GUARDS:
  - [skill or pipeline step this protects against the trap]

{{skill-name}} TRIGGERED BY:
  - [review gate or checkpoint that should invoke this guard]
```
```

---

## R6 Scaffolding Rules

1. **Template selection:** Match the `concept_kind` tag from `R2-Extraction-Manifest.md` to one of the 6 templates.
2. **Null handling:** Never invent values. If a field is null after R5 defaults: use the `[unspecified — ...]` fallback text shown in each template.
3. **Name convention:** Follow domain prefix from `R4-Architecture.md`. Use kebab-case. No acronyms unless in glossary.
4. **Description field:** Must be ≤100 chars, actionable, no emojis. Test: would this appear in a skill list and be immediately understood?
5. **Integration section:** Populate only from `R4-Architecture.md` DAG. Do not invent connections.
6. **Source attribution:** Always fill `Source:` from the chapter attributed in `R2-Extraction-Manifest.md`.
7. **Confidence wave assignment:**
   - Wave 1: Apply This specs with all fields populated
   - Wave 2: Q1-Q6 prose-derived specs with all fields populated
   - Wave 3: R2.1 derivations with medium+ confidence
   - Wave 4: Gap-fills from R5 sane defaults (CEO reviews sample before batch approval)
