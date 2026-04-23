---
name: skill-from-research
description: Build or UPGRADE Claude Skills from deep research using NotebookLM as knowledge engine. Two modes - CREATE (new skill) and UPGRADE (enhance existing skill with new research). Pipeline - NLM Deep Research → Knowledge Extraction → SKILL.md Generation/Merge → Eval. Triggers on "tạo skill từ research", "build skill from research", "nâng cấp skill", "upgrade skill", "skill from NLM", "deep research to skill", "xây dựng kỹ năng chuyên sâu", "cải tiến skill", "add knowledge to skill", "bổ sung kiến thức cho skill".
---

# Skill From Research — NLM Deep Research → Claude Skill Pipeline

Build NEW or UPGRADE EXISTING Claude Skills from curated research. NLM provides the grounded domain knowledge (free Gemini tokens), Claude structures it into an executable SKILL.md.

## When to Use

- **CREATE mode:** CEO wants a new skill backed by deep domain research
- **UPGRADE mode:** Existing skill needs domain knowledge upgrade from new sources
- New product/domain requires specialized AI assistant capability
- After `/research --deep` produces insights that should become reusable
- Skill performance gap identified (missing domain knowledge, wrong procedures)

## Mode Detection

```
IF user says "tạo", "create", "build", "xây dựng" → CREATE mode
IF user says "nâng cấp", "upgrade", "cải tiến", "bổ sung", "update" → UPGRADE mode
IF user provides existing skill name → UPGRADE mode
IF ambiguous → ask CEO: "Tạo skill mới hay nâng cấp skill hiện có?"
```

## Pipeline Flow

### CREATE Mode (new skill)
```
[1] DEFINE SKILL SCOPE
    What should this skill do? Who uses it? When does it trigger?
     ↓
[2] NLM KNOWLEDGE BASE
    Create/select notebook → add authoritative sources → Deep Research
     ↓
[3] KNOWLEDGE EXTRACTION
    Query NLM for: principles, procedures, failure modes, decision rules
     ↓
[4] SKILL ARCHITECTURE
    Map extracted knowledge → SKILL.md structure (metadata + instructions)
     ↓
[5] SKILL GENERATION
    Write SKILL.md with embedded domain knowledge from NLM
     ↓
[6] VALIDATION
    Test with sample prompts → compare output vs NLM ground truth
     ↓
[7] DEPLOY + ITERATE
    Install skill → use in real sessions → refine from feedback
```

## Step 1: Define Skill Scope (CEO — Core)

Ask CEO:

```markdown
## Skill Scope Definition
1. **Tên skill:** [name] — slug for folder name
2. **Mục đích:** [1-2 câu mô tả skill làm gì]
3. **Target user:** [ai dùng skill này? CEO / engineer / researcher]
4. **Trigger keywords:** [từ khóa nào kích hoạt skill]
5. **Domain:** [engineering / defense / business / KM / other]
6. **Existing knowledge:** [có notebook NLM nào liên quan? có Galaxy notes?]
7. **Output mong muốn:** [skill tạo ra deliverable gì?]
8. **Freedom level:** [HIGH — creative / MED — follow pattern / LOW — strict procedure]
```

## Step 2: NLM Knowledge Base

### 2a. Source Collection

```bash
# Option A: Use existing notebook
nlm alias list  # check if relevant notebook exists

# Option B: Create new notebook + add sources
nlm notebook create "Skill Research: <skill-name>"
nlm alias set skill-<name> <uuid>

# Option C: Use NLM Deep Research (auto-find sources)
nlm research start skill-<name> "<topic: key concepts, best practices, failure modes>"
nlm research status skill-<name>
nlm research import skill-<name>
```

### 2b. CEO Source Curation

Present discovered sources → CEO selects which to keep (Core decision).
Add CEO-selected sources:

```bash
# Authority sources (standards, OEM docs, textbooks)
nlm source add skill-<name> --url "<url>"

# Existing vault content (Galaxy notes, project docs)
nlm source add skill-<name> --text "<vault content>" --title "<note title>"
```

**Key insight:** Include Galaxy permanent notes as sources — they contain distilled, CEO-validated knowledge that should ground the skill.

## Step 3: Knowledge Extraction (6-Question Framework)

Run structured NLM queries to extract skill-building knowledge:

```bash
# Q1: Core principles (what must the skill KNOW?)
nlm notebook query skill-<name> "What are the 3-5 core principles that an expert in <domain> must follow? List as rules with rationale."

# Q2: Procedures (what steps must the skill EXECUTE?)
nlm notebook query skill-<name> "What is the step-by-step procedure for <task>? Include decision points and branching logic."

# Q3: Failure modes (what must the skill AVOID?)
nlm notebook query skill-<name> "What are the top 5 failure modes or common mistakes when doing <task>? How to detect and prevent each?"

# Q4: Decision rules (when to do WHAT?)
nlm notebook query skill-<name> "What decision rules or criteria determine the right approach? Format as IF-THEN-ELSE."

# Q5: Quality criteria (how to judge OUTPUT?)
nlm notebook query skill-<name> "What makes the output good vs bad? List specific quality criteria with examples."

# Q6: Edge cases (what breaks the rules?)
nlm notebook query skill-<name> "What edge cases or exceptions exist? When should the standard procedure be modified?"
```

Save all 6 answers — these become the skill's domain knowledge.

## Step 4: Skill Architecture

Map extracted knowledge to SKILL.md structure:

```
YAML Frontmatter:
  - name ← from Step 1
  - description ← from Step 1 (trigger keywords)

Content Sections:
  - When to Use ← from Step 1 (triggers + contexts)
  - Workflow Steps ← from Q2 (procedures)
  - Decision Points ← from Q4 (IF-THEN rules)
  - Quality Criteria ← from Q5 (output validation)
  - Gotchas/Warnings ← from Q3 (failure modes) + Q6 (edge cases)
  - Core Principles ← from Q1 (embedded as rules, not explanations)
  - References ← NLM notebook alias for follow-up queries
  - COD Classification ← which steps Core vs Offload
```

### Architecture Rules:
- **< 500 lines** — if longer, split into SKILL.md + references/
- **Imperative style** — "Do X" not "You should consider doing X"
- **Only include what Claude doesn't know** — domain-specific rules, NOT general knowledge
- **Embed decision rules as code-like IF-THEN** — not prose
- **Link to NLM notebook** — skill can query NLM for deeper context at runtime

## Step 5: Skill Generation

Write SKILL.md using extracted knowledge. Structure:

```markdown
---
name: <skill-name>
description: <trigger description from Step 1>
---

# <Skill Name> — <1-line purpose>

<1-2 sentence summary of what this skill does>

## When to Use
<triggers and contexts from Step 1>

## Workflow
### Step 1: <step name>
<procedure from Q2, with decision points from Q4>

### Step 2: <step name>
...

## Quality Criteria
<from Q5 — checklist for output validation>

## Gotchas
<from Q3 + Q6 — numbered failure modes with prevention>

## NLM Reference
- Notebook: `<alias>` — query for deeper domain context
- Key sources: <list top 3-5 authority sources in notebook>

## COD Classification
| Task | COD | Notes |
|------|-----|-------|
| <task> | C/O/D | <why> |
```

## Step 6: Validation

### 6a. Sample Prompt Test

Create 3 test prompts that would trigger the skill:

```
Test 1 (happy path): "<typical use case prompt>"
Test 2 (edge case): "<unusual but valid request>"
Test 3 (out of scope): "<should NOT trigger skill>"
```

### 6b. Ground Truth Comparison

For Test 1-2, compare skill output against NLM query:

```bash
# Get NLM ground truth
nlm notebook query skill-<name> "<same question as test prompt>"

# Compare:
# - Does skill output align with NLM ground truth?
# - Did skill miss important domain knowledge?
# - Did skill hallucinate beyond source material?
```

### 6c. Binary Eval (optional — for critical skills)

Create eval JSON in `_meta/evals/<skill-name>.json`:

```json
{
  "skill": "<skill-name>",
  "created": "YYYY-MM-DD",
  "tests": [
    {
      "prompt": "<test prompt>",
      "assertions": [
        {"type": "contains", "value": "<must-have term>"},
        {"type": "not_contains", "value": "<must-not-have term>"}
      ]
    }
  ]
}
```

## Step 7: Deploy + Iterate

1. Save SKILL.md to `~/.claude/commands/<skill-name>/SKILL.md`
2. Test in live session
3. First 3 uses → collect feedback → refine
4. After 5+ successful uses → skill is production-grade

## UPGRADE Mode Pipeline (enhance existing skill)

### U1: Identify Skill & Gap

```
1. Read current SKILL.md: ~/.claude/commands/<skill-name>/SKILL.md
2. Identify gaps:
   - What domain knowledge is missing?
   - What procedures are incomplete?
   - What failure modes aren't covered?
   - What new sources/standards have emerged?
   - CEO feedback from real usage: what went wrong?
3. Present gap analysis to CEO for confirmation
```

### U2: Research Gap

```
Option A — Add sources to EXISTING NLM notebook (if skill has one):
  nlm source add <existing-notebook> --url "<new source>"

Option B — Create supplementary notebook:
  nlm notebook create "Upgrade: <skill-name>"

Option C — Run /research on gap topic:
  /research <gap topic> --notebook <existing-notebook>
```

### U3: Targeted Extraction (only gap questions)

Don't re-run all 6 questions. Only extract for the GAP:

```bash
# IF missing procedures:
nlm notebook query <notebook> "What specific procedures for <gap topic>
are NOT covered in [paste current skill workflow summary]?"

# IF missing failure modes:
nlm notebook query <notebook> "What failure modes for <gap topic>
should be added? Only list ones NOT already in: [paste current gotchas]"

# IF outdated standards:
nlm notebook query <notebook> "What has changed in <domain> standards
since [skill creation date]? List only updates that affect procedures."

# IF CEO feedback (most valuable):
# Use CEO's real-world usage feedback as the extraction prompt:
nlm notebook query <notebook> "In practice, [CEO feedback problem] occurred.
What does the literature say about preventing this? What procedure was missing?"
```

### U4: Merge Delta Into Existing Skill

```
1. Read current SKILL.md
2. Identify EXACT insertion points for new knowledge:
   - New workflow steps → insert at correct position
   - New failure modes → append to Gotchas table
   - New decision rules → add to Decision Points
   - Updated standards → update Standards table
   - New trigger keywords → update description in frontmatter
3. Use Edit tool (NOT Write) — preserve existing content, only add delta
4. Add changelog comment at bottom:
   <!-- Upgraded YYYY-MM-DD: added [what] from [NLM notebook] -->
```

**CRITICAL: UPGRADE = surgical Edit, not full rewrite.** Preserve what works. Only add what's missing.

### U5: Validate Upgrade

```
1. Re-run existing test prompts → should still pass (no regression)
2. Create 1 new test prompt targeting the gap that was filled
3. Compare new test output vs NLM ground truth
4. IF regression detected → revert Edit, investigate
```

### U6: Log Upgrade

Append to `_meta/learnings.md`:
```
[DATE] Skill upgrade <skill-name>: added [what] from [NLM notebook/sources].
Gap: [what was missing]. Trigger: [CEO feedback / new research / standards update].
```

## Upgrade Triggers (when to run UPGRADE mode)

| Trigger | Detection | Action |
|---------|-----------|--------|
| CEO says "skill X thiếu Y" | Direct feedback | UPGRADE with CEO feedback as extraction prompt |
| New research found relevant sources | During /research | UPGRADE → add sources + extract delta |
| Standards updated | Periodic check | UPGRADE → update standards table |
| Skill used 5+ times with consistent gap | Usage pattern | UPGRADE → fill recurring gap |
| New Galaxy note relevant to skill domain | Galaxy growth | UPGRADE → embed Galaxy note as rule |
| Project post-mortem reveals missing procedure | Post-project | UPGRADE → add learned procedure |

## Quick Upgrade (no NLM — for small fixes)

For minor upgrades that don't need NLM research:

```
1. CEO provides feedback: "skill X should also handle Y"
2. Read current SKILL.md
3. Edit to add Y (surgical insertion)
4. No NLM needed — CEO judgment is the source
5. Log in _meta/learnings.md
```

Use Quick Upgrade when: 1 new rule, 1 new gotcha, trigger keyword update, minor procedure addition.
Use Full Upgrade when: new domain knowledge, multiple gaps, standards change, structural rework.

## Advanced: Galaxy → Skill Bridge

Galaxy permanent notes = distilled CEO judgment. They can become skill rules:

```
Galaxy Note: "Recoil Fidelity Threshold — 70% Lực Đủ Cho Training Transfer"
→ Skill Rule: "When evaluating recoil simulation, 70% force fidelity is the minimum
   for positive training transfer. Below 70% → training may create negative transfer."
```

Scan Galaxy for notes relevant to skill domain → extract as rules → embed in SKILL.md.

## Integration Points

- Feeds from: `/research --deep` (discovery), `/nlm` (knowledge base), Galaxy (distilled insights)
- Feeds into: `~/.claude/commands/` (deployed skills), `_meta/evals/` (validation)
- Companion to: `skill-creator:skill-creator` (Anthropic's meta-skill — handles SKILL.md syntax)
- Pipeline position: After research, before deployment

## COD Classification

| Task | COD | Notes |
|------|-----|-------|
| Define skill scope | **Core** | CEO judgment — what to build |
| NLM source curation | **Core** | CEO selects authority sources |
| Knowledge extraction (Q1-Q6) | Offload | NLM queries (free Gemini) |
| Skill architecture | Offload | Claude structures |
| SKILL.md generation | Offload | Claude writes |
| Validation prompts | **Core** | CEO defines test cases |
| Ground truth comparison | Offload | Claude compares |
| Deploy decision | **Core** | CEO approves |

## Rules

- **NLM is the source of truth** — skill knowledge must trace back to NLM sources
- **Galaxy notes override generic knowledge** — if Galaxy says X, skill follows X
- **< 500 lines** — split into SKILL.md + references/ if longer
- **Test before deploy** — minimum 3 test prompts
- **Document NLM notebook** — every skill references its source notebook for refresh
- **CEO approves** — skill scope, source selection, and deploy are Core decisions
