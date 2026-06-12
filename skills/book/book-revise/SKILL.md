---
name: book-revise
description: "Block P6 của codebase-to-book pipeline — apply P5 review feedback trong một pass duy nhất. Structural changes (split/merge chapters, fix cross-refs), deduplication (concept canonical home), content cuts (enumeration → patterns), content additions (examples, diagrams), consistency (Apply This standardization, phrase dedup, glossary enforcement). Sinh Phase6-Revised/Ch*_v2.md. Can run standalone. Triggers on: 'book revise', 'apply feedback', 'revise chapters', 'fix review issues', 'P6 book'."
---

# Block P6: Revision — Single-Pass Feedback Application

> **Pipeline:** codebase-to-book → Block P6
> **Input:** `Phase5-Review.md` + `Phase4-Chapters/Ch*_Draft.md`
> **Output:** `Phase6-Revised/Ch<NN>_<slug>_v2.md`
> **Reference:** `../codebase-to-book/references/book-voice-and-style.md`

## Operational Envelope

| DO (within envelope) | DON'T (outside envelope) |
|---|---|
| Apply P5 feedback in ONE pass (no iterative loops) | Re-review and flag new issues (= P5's job, done) |
| Split/merge chapters per P5 structural recommendations | Add entirely new chapters not in outline (= back to P3) |
| Deduplicate concepts — each has canonical home | Remove content CEO approved in P2 thesis |
| Cut bloated sections, compress enumeration into tables | Cut verbatim source code (= P7 audit's specific job) |
| Add missing content flagged by P5 (examples, diagrams) | Inflate word count — cutting is more common than adding |
| Enforce glossary + Apply This format rotation | Change voice or thesis — locked |

**Multi-Agent Mode:** NO — sequential chapter-by-chapter revision (coordination across chapters needs single agent state).
**CEO Checkpoint:** After all revisions — CEO spot-checks before P7.

## Standalone Usage
```
/book-revise <codebase-slug>
```

## Input Requirements

- `_pipeline_state.md` Block Ledger — must show P5 complete + CEO scope decision
- `Phase5-Review.md` — consolidated feedback + P6 scope (CRITICAL/MAJOR/MINOR subset)
- `Phase4-Chapters/Ch*_Draft.md` × N — originals
- `Phase2-Positioning.md` — glossary + thesis (consistency reference)
- `Phase3-Outline.md` — chapter spec (verify structural changes don't violate outline)

## Workflow

### Step P6.1: Load Review + Scope

Read `Phase5-Review.md`. Read CEO scope decision từ Block Ledger:
- "Fix all CRITICAL + MAJOR" → process issues with severity in [CRITICAL, MAJOR]
- "Fix CRITICAL only" → process only CRITICAL
- "Fix all" → process everything

Build issue list grouped by chapter.

### Step P6.2: Categorize Changes

Partition issues into 4 categories for systematic application:

#### Category A: Structural Changes
- Split chapter X into chapters Xa + Xb
- Merge chapter Y into chapter Z
- Reorder chapters (update backward/forward refs)
- Add missing section within chapter
- Remove duplicate section

#### Category B: Content Cuts
- Remove enumeration that doesn't teach
- Compress reference material into tables
- Trim bloated paragraphs
- Cut redundant examples

#### Category C: Content Additions
- Add missing transitions
- Add worked examples where gaps flagged
- Add diagrams at P5-identified locations
- Add missing Apply This patterns

#### Category D: Consistency Fixes
- Standardize Apply This format per rotation
- Replace synonyms with glossary terms
- Remove repeated rhetorical phrases across chapters
- Fix cross-references (Ch N mentions Ch M — verify M still exists post-structural changes)

### Step P6.3: Apply in Order

**Order matters.** Apply bottom-up:

1. **Category A (Structural)** first — split/merge affects chapter count, so downstream refs need update
2. **Category B (Cuts)** next — smaller surface for remaining operations
3. **Category C (Additions)** next — fill gaps identified
4. **Category D (Consistency)** last — polish over stable structure

#### Category A Application

```python
# Pseudocode — structural changes
for issue in structural_issues:
    if issue.type == "split":
        split_chapter(issue.chapter, issue.proposed_Xa, issue.proposed_Xb)
        # Update chapter numbering for downstream chapters
        renumber_chapters(from_index=issue.chapter + 1, shift=+1)
        update_cross_refs(renumbered=True)
    elif issue.type == "merge":
        merge_chapters(issue.source, issue.target)
        renumber_chapters(from_index=issue.source, shift=-1)
    elif issue.type == "add_section":
        insert_section(chapter=issue.chapter, position=issue.after, content=issue.new_content)
    elif issue.type == "remove_section":
        delete_section(chapter=issue.chapter, section=issue.section)
```

#### Category B Application

```python
# Pseudocode — content cuts
for issue in cut_issues:
    content = read_chapter(issue.chapter)
    match issue.type:
        case "enumeration":
            content = compress_enumeration(content, location=issue.location)
        case "bloated_section":
            content = trim_section(content, issue.section, target_reduction="20-30%")
        case "long_code_block":
            content = trim_code_block(content, issue.block_id, max_lines=15)
        case "redundant_example":
            content = remove_example(content, issue.example_id)
    write_chapter(issue.chapter, content)
```

#### Category C Application

```python
# Pseudocode — content additions
for issue in add_issues:
    content = read_chapter(issue.chapter)
    match issue.type:
        case "missing_transition":
            content = insert_paragraph(content, between=(issue.sec_a, issue.sec_b), text=issue.draft)
        case "missing_example":
            content = add_example(content, issue.location, issue.draft)
        case "missing_diagram":
            # Draft Mermaid diagram per P5 spec
            diagram = render_mermaid(issue.diagram_spec)
            content = insert_diagram(content, issue.location, diagram)
        case "missing_apply_pattern":
            content = add_apply_pattern(content, issue.pattern_spec)
    write_chapter(issue.chapter, content)
```

#### Category D Application

```python
# Pseudocode — consistency fixes
# Apply to all chapters at once
for chapter_file in glob(f"{output_dir}/Phase6-Revised/*.md"):
    content = read(chapter_file)
    
    # Enforce glossary terms
    content = replace_synonyms_with_glossary(content, glossary)
    
    # Standardize Apply This format per rotation
    content = apply_rotation_format(content, rotation_map[chapter_num])
    
    # Remove repeated rhetorical phrases
    content = dedupe_across_book(content, phrase_frequency_threshold=3)
    
    # Verify cross-refs point to existing chapters
    content = verify_cross_refs(content, current_chapter_count)
    
    write(chapter_file, content)
```

### Step P6.4: Cross-Reference Audit

After all changes, re-scan every chapter:

```
CROSS-REFERENCE AUDIT — Post-Revision

Chapter count before: {{N_before}}
Chapter count after: {{N_after}}
Renumbering operations: {{count}}

Forward references checked: {{count}}
  ✅ Valid: {{count}}
  ❌ Broken (point to deleted chapter): {{count}} → FIX

Backward references checked: {{count}}
  ✅ Valid: {{count}}
  ❌ Broken (point to wrong chapter post-renumber): {{count}} → FIX

Glossary compliance:
  Term "<X>" used consistently: {{yes|drift in Ch {{list}}}}
```

### Step P6.5: Quality Metrics

Track what changed:

```markdown
## P6 Revision Metrics

| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| Chapter count | {{N}} | {{M}} | {{+/-}} |
| Total lines | {{X}} | {{Y}} | {{-Z}} ({{pct}}%) |
| Mermaid diagrams | {{A}} | {{B}} | {{+C}} |
| Pseudocode blocks | {{P}} | {{Q}} | {{+/-R}} |
| Apply This patterns | {{M×5}} | {{M'×5}} | {{delta}} |

Issues resolved:
  🔴 CRITICAL: {{N}} / {{N}} (100%)
  🟠 MAJOR: {{M}} / {{M_total}} ({{pct}}%)
  🟡 MINOR: {{K}} / {{K_total}} ({{pct}}%)

Issues NOT resolved (deferred):
  - <issue 1>: <reason deferred>
  - <issue 2>: <reason deferred>
```

### Step P6.6: Update Pipeline State + Ledger

```markdown
### P6 — Revision (<date>)
**Key findings:**
- {{N_before}} → {{N_after}} chapters ({{delta}} via split/merge)
- Lines: {{before}} → {{after}} ({{pct}} reduction — typical 20-40%)
- Diagrams added: {{N}}
- All CRITICAL + MAJOR issues resolved (CEO scope)

**Decisions for downstream:**
- P7 audit can proceed — structure stable
- Chapter count final: {{N_after}}
- Any remaining MINOR issues: [list if not resolved]

**Open questions:** [if any]

**CEO checkpoint result:** [pending]
```

## Output

Save to `{{output_dir}}/Phase6-Revised/`:
- `Ch<NN>_<slug>_v2.md` × N_after (new chapter count after structural changes)

Update: `{{output_dir}}/_pipeline_state.md`.

## CEO Checkpoint

```
═══ BLOCK P6 REVISION COMPLETE ═══
Structural changes: {{N_splits}} splits, {{N_merges}} merges
Chapter count: {{before}} → {{after}}
Total lines: {{before}} → {{after}} ({{pct}} reduction)

Issues resolved:
  🔴 CRITICAL: {{N}}/{{N}} (must be 100%)
  🟠 MAJOR: {{M}}/{{M_total}}
  🟡 MINOR: {{K}}/{{K_total}}

Diagrams added: {{N}}
Cross-refs verified: ✅

Deliverables:
  - {{output_dir}}/Phase6-Revised/ ({{N_after}} files)

CEO:
(1) ✅ Approve → tiếp tục Block P7 (Audit)
(2) 🔄 Re-revise Ch <N> với concerns: [specify]
(3) 🔄 Additional pass for MINOR issues: [approve/deny]
(4) ⏸️ Dừng — CEO cần spot-check revised chapters
═══════════════════════════════════════════════════
```

## COD Classification

- Issue categorization: Offload (O2)
- Structural changes (split/merge): Offload (O2) — with care
- Content cuts: Offload (O2)
- Content additions (draft): Offload (O2)
- Diagram drafting: Offload (O2)
- Cross-ref audit: Offload (O2)
- **Scope decision override**: Core (C) — CEO can extend scope mid-revision

## Rules

- **Single pass — no iterative loops** — apply all feedback, move on to P7. If revisions create new issues, P7 audit and subsequent runs catch them.
- **Order matters: A → B → C → D** — structural first, consistency last
- **Don't add unreviewed content** — if CEO didn't approve a thesis shift, don't introduce it via addition
- **Cross-ref audit mandatory** — structural changes break refs. Must fix before P7.
- **Glossary enforcement** — every chapter uses glossary terms. Synonyms replaced.
- **Apply This rotation enforced** — if chapter was Variant A, keep A (don't drift to B during addition)
- **If > 50% lines changed** — chapter was too broken, flag for re-write (back to P4 for that chapter only)
- **Preserve voice** — P4 subagents each had slight voice; P6 normalizes but doesn't rewrite entirely
- **Document deferred issues** — not every MINOR must be fixed. Record why deferred in Ledger.
