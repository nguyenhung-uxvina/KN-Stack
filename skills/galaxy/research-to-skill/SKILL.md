---
name: research-to-skill
description: End-to-end pipeline from deep research to skill upgrade/creation. Orchestrates /research --deep → NLM extraction → /first-principles adaptation → surgical Edit → validate. Use when CEO says "research and upgrade skill", "nâng cấp skill từ research", "build skill from topic", "research to skill", "tạo skill từ nghiên cứu", or wants to systematically enhance a Claude skill with grounded domain knowledge.
---

# Research-to-Skill — Full Pipeline Super-Skill

End-to-end: deep research → NLM knowledge base → first-principles adaptation → skill upgrade/create → validate. One command, 5 steps, CEO checkpoints at each gate.

## When to Use

- CEO identifies methodology gap: "skill X thiếu Y" + needs research to fill it
- New domain knowledge discovered that should become reusable skill capability
- After reading paper/article: "tích hợp methodology này vào HELIX/FORGE/BRIDGE"
- Standards updated: need to refresh skill with new procedures
- Cross-product lesson should become permanent skill knowledge

## Mode Detection

```
IF user specifies existing skill name → UPGRADE mode
IF user says "tạo mới", "create", "new skill" → CREATE mode
IF ambiguous → ask: "Nâng cấp skill hiện có hay tạo skill mới?"
```

## Arguments

```
/research-to-skill UPGRADE <skill-name> with <topic>
/research-to-skill CREATE <new-skill-name> from <topic>

Examples:
  /research-to-skill UPGRADE helix-concept-generate with ICDM methodology
  /research-to-skill CREATE helm-welding-inspection from NDT aluminum 5083
  /research-to-skill UPGRADE forge-shift with latest ACH research 2025
```

---

## Pipeline (5 Steps — Sequential, CEO Gates)

### Step 1: Deep Research — Source Discovery + Curation

**Invoke:** `/research --deep <topic>`

**Process:**
1. Multi-channel search (Web + YouTube + Authority + Patents)
2. Tier classify (S/A/B/C)
3. Present source table to CEO

**CEO GATE 1:** "Chọn sources nào để analyze?"
- CEO selects sources → proceed
- CEO says "thêm search" → refine queries → re-present

**Output:** NLM notebook created with curated sources + research report saved.

**Time:** ~45-60 min

---

### Step 1.5: CEO Review NLM Notebook (Core — BLOCKING)

**Purpose:** Một số sources bị paywall, restricted access, hoặc ingest fail. CEO tự kiểm tra NLM notebook và bổ sung nguồn trước khi extraction.

**Process:**

1. **AI báo cáo ingest status:**
   ```
   NLM NOTEBOOK REVIEW — {{notebook_alias}}

   INGESTED: {{N}}/{{M}} sources
   FAILED:
   | # | Source | Tier | Failure Reason |
   |---|--------|------|---------------|
   | X | {{title}} | S/A | paywall / restricted / format error |

   CRITICAL GAPS (if Tier S/A sources failed):
   - {{source}}: thiếu {{specific knowledge}}
   - Impact nếu không bổ sung: extraction sẽ thiếu {{what}}

   ⏸️ CEO: Mở notebooklm.google.com → review notebook {{alias}}
         Tự thêm sources nếu cần → xác nhận khi đủ.
   ```

2. **CEO tự review + bổ sung:**
   - Mở NotebookLM trực tiếp (notebooklm.google.com)
   - Kiểm tra source list → nguồn nào thiếu?
   - Tự upload PDF/URL (bypass paywall bằng tài khoản cá nhân, thư viện, mua paper)
   - Đánh giá: notebook đủ cover topic cần extract?

3. **CEO xác nhận (1 trong 3):**
   - **"ĐỦ — proceed"** → AI tiếp tục Step 2
   - **"ĐÃ THÊM — proceed"** → AI re-check source list rồi tiếp tục Step 2
   - **"THIẾU — tìm thêm"** → quay lại Step 1 mở rộng search

**COD:** Gate = **Core** (CEO). AI báo gaps, KHÔNG tự quyết đủ hay thiếu.
**Time:** 5-30 phút

---

### Step 2: NLM Deep Extraction — Domain Knowledge Mining

**Process:**

For UPGRADE mode — targeted gap extraction:
```
1. Read current SKILL.md completely
2. Identify specific gaps (missing steps, tools, procedures)
3. Present gap analysis to CEO for confirmation

CEO GATE 2a: "Gaps đúng chưa? Thiếu gì nữa?"

4. Query NLM with gap-specific questions:
   "I need EXACT procedures for [N] tools to add to an existing
   [framework] skill. For each tool provide:
   (a) input required
   (b) exact procedure steps
   (c) output format/table
   (d) decision thresholds
   (e) integration with existing workflow"

5. Save raw extraction output
```

For CREATE mode — full 6-question framework:
```
Q1: Core 3-5 principles (what must skill KNOW?)
Q2: Step-by-step procedures (what must skill EXECUTE?)
Q3: Top 5 failure modes (what must skill AVOID?)
Q4: Decision rules (IF-THEN-ELSE)
Q5: Quality criteria (how to judge output?)
Q6: Edge cases (what breaks the rules?)
```

**Output:** Raw extracted procedures + citations from NLM.

**Time:** ~30 min

---

### Step 2.5: First-Principles Adaptation — Academic → WX Executable

**Purpose:** Bridge gap giữa "academic procedure" (NLM output) và "WX-executable tool." NLM gives WHAT, first-principles reveals WHY it works and WHEN it fails in WX context.

**Process per extracted tool:**

```
STRIP:
  → Tool dựa trên assumptions nào?
  → PROVEN (physics/math) vs CONVENTION (large team, Western industry)?

INVERT:
  → Trong WX context (CEO + 2 experts, defense VN, budget limited):
    - Assumptions nào SAI?
    - Tool nào vẫn hoạt động?
    - Tool nào cần modify?

REBUILD:
  → Giữ PROVEN principles
  → Bỏ/thay CONVENTION elements
  → Thêm WX-specific: scoring scales, thresholds, VN defense context
  → Output: ADAPTED procedure
```

**6 Adaptation Patterns:**

| Pattern | From → To | When |
|---------|----------|------|
| Vague scale → Quantified | "excellent/poor" → Score 1-16 | Scale undefined in source |
| Missing checklist → WX questions | "checklist" → 13 specific questions | Source says "checklist" without items |
| Conceptual → Scoring table | "gap principle" → 3×5 matrix | Source describes concept, no numbers |
| No formula → Linear scoring | "CSR functions" → 0-10 vs targets | Source has no math |
| Team-based → CEO + 2 experts | "PDT consensus 20 people" → CEO + CK + AI/Edge | Org structure mismatch |
| Generic → Defense VN | Standard robustness → +blast, +tropical, +ACH | Domain mismatch |

**CEO GATE 2.5:** "Adapted scales/thresholds có thực tế không?"
- CEO validates scoring makes sense for WX projects
- CEO may adjust thresholds based on experience

**Skip condition:** Tool already specific + context matches WX → skip straight to Step 3.

**Output:** Adapted tool procedures ready for insertion.

**Time:** ~20-30 min

---

### Step 3: Surgical Skill Edit — Insert Delta

**CRITICAL RULE: Edit, NEVER Write. Preserve existing content.**

**Process:**

For UPGRADE mode:
```
1. Read current SKILL.md one more time (verify no changes since Step 2)
2. For each adapted tool from Step 2.5:
   a. Identify EXACT insertion point (between which existing steps)
   b. Write new step content with:
      - Step number (e.g., 3.5a, 5.6, 9)
      - Purpose statement
      - Input/output
      - Procedure table
      - Scoring scales + thresholds
      - CEO gate (if decision needed)
      - COD classification
      - Source citation + NLM notebook reference
      - Skip condition
   c. Execute Edit tool — surgical insertion
3. Update MANDATORY Output Sections (if skill has this section)
4. Update Integration section (reads-from/writes-to)
5. Update Gotchas (if new failure modes discovered)
```

For CREATE mode:
```
1. Write full SKILL.md with all extracted + adapted knowledge
2. Structure: frontmatter → When to Use → Workflow → Quality Criteria →
   Gotchas → NLM Reference → COD Classification → Rules
3. Deploy to ~/.claude/commands/<skill-name>/SKILL.md
```

**Insertion naming convention:**
- Between Step 3 and 4 → Step 3.5
- Multiple inserts → Step 3.5a, 3.5b
- New final step → Step N+1
- New gate criterion → A(N+1) in Auto-Check

**Output:** Updated SKILL.md with new tools integrated.

**Time:** ~30 min

---

### Step 4: Validate + Log

**4a. Regression Check:**
```
- Read updated SKILL.md
- Verify: existing steps untouched (no accidental deletion)
- Verify: new steps reference correct inputs/outputs
- Verify: step numbering consistent
- Verify: MANDATORY Output Sections updated
```

**4b. Count Verification:**
```
Before: [N] steps, [M] output sections
After:  [N+X] steps, [M+Y] output sections
Added:  [list of new steps/tools]
```

**4c. Log to _meta/learnings.md:**
```
[YYYY-MM-DD] Skill upgrade <skill>: added [tools] from [NLM notebook].
Gap: [what was missing]. Trigger: [research/CEO feedback].
Pipeline: /research-to-skill UPGRADE.
```

**4d. Update Research Report:**
Append to `3_Resources/Deep-Content-Analyzer-Outputs/RESEARCH_<topic>_<date>.md`:
```
## Skill Integration (Step 7 addendum)
- Skill upgraded: <skill-name>
- Tools added: [list]
- Steps: [list with numbers]
- ICDM/methodology integration score: X/Y
```

**CEO GATE 4:** "Review final skill. Chấp nhận?"
- CEO approves → done
- CEO requests changes → iterate Step 3

**Time:** ~15-20 min

---

## Summary Output (end of pipeline)

```markdown
## /research-to-skill Complete

### Research
- Topic: {{topic}}
- Sources: {{N}} found, {{M}} selected, {{K}} ingested to NLM
- NLM notebook: {{alias}}
- Report: {{path to research file}}

### Extraction + Adaptation
- Tools extracted: {{N}}
- Tools adapted (first-principles): {{N}}
- Adaptation patterns used: {{list}}

### Skill Update
- Mode: UPGRADE / CREATE
- Skill: {{skill-name}}
- Steps added: {{list with numbers}}
- Output sections added: {{list}}
- Integration score: {{X/Y}} (if methodology-based)

### Validation
- Regression: PASS / FAIL
- New steps count: +{{N}}
- Logged: _meta/learnings.md ✓
```

---

## NLM Reference

- Pipeline concept: `2_Areas/CEO-Self/Pipeline-Reference/Research-to-Skill-Upgrade-Pipeline.md`
- Proven case: NLM notebook `icdm` (11 sources) → helix-concept-generate + helix-quality-gate (8/8 ICDM tools)

## Reject Conditions

```
REJECT IF:
  □ No clear topic or methodology to research
  □ Skill to upgrade doesn't exist (for UPGRADE mode)
  □ NLM auth fails after 2 retries → fallback to Quick Upgrade (no NLM)
  □ CEO declines all sources at Gate 1 → refine topic
```

## COD Classification

| Task | COD | Notes |
|------|-----|-------|
| Source discovery (Step 1) | Offload | Multi-channel search |
| Source selection (Gate 1) | **Core** | CEO judgment |
| NLM notebook review (Step 1.5) | **Core** | CEO reviews + adds sources |
| NLM extraction (Step 2) | Offload | Free Gemini tokens |
| Gap confirmation (Gate 2a) | **Core** | CEO validates gaps |
| First-principles STRIP+INVERT (Step 2.5) | Offload | AI analyzes |
| Adaptation REBUILD (Gate 2.5) | **Core** | CEO validates scales/thresholds |
| Surgical Edit (Step 3) | Offload | AI edits |
| Final review (Gate 4) | **Core** | CEO approves |
| Logging (Step 4) | Offload | Mechanical |

## Rules

- **NEVER rewrite existing SKILL.md** — always surgical Edit for UPGRADE mode
- **ALWAYS run first-principles adaptation** — raw academic copy = unusable for WX
- **CEO gates are NON-SKIPPABLE** — 4 checkpoints, each requires explicit CEO approval
- **Log EVERY upgrade** — future sessions need to know what changed
- **NLM is primary analysis engine** — free Gemini tokens, save Claude for editing
- **Adaptation patterns are reusable** — document new patterns when discovered
