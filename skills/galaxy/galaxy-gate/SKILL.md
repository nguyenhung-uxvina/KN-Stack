---
name: galaxy-gate
description: "Galaxy note creation gatekeeper for the IPARAG Zettelkasten vault. Runs a 3-question quality test (product impact / strategic decision / trap warning) before any new permanent note enters 5_Galaxy/. Use before creating any Galaxy note to enforce atomic, high-value knowledge. Triggers on: \"galaxy gate\", \"create galaxy note\", \"new permanent note\", \"tao galaxy note\", \"kiem tra truoc khi tao note\", \"permanent note check\", \"kiểm tra note\", \"tạo ghi chú vĩnh viễn\"."
---

Galaxy note creation gatekeeper. Run BEFORE creating any new permanent note in `5_Galaxy/`.

Ensures the proposed note passes the 3-question quality test, is atomic, and has proper links.

Usage: /galaxy-gate [concept description]
If no argument, ask the user to describe the proposed note concept.

---

## Process

### Step 1: Parse input

Extract the proposed note concept from $ARGUMENTS. If empty, ask:
"Describe the concept you want to create a Galaxy note for."

### Step 2: 3-question quality test

Evaluate the proposed concept against each question. Provide a specific answer or mark N/A:

**(a) Does this change how you design a specific product?**
→ If yes, name the product and how. If no → ❌ N/A

**(b) Does this change a strategic decision?**
→ If yes, name the decision. If no → ❌ N/A

**(c) Does this warn about a specific trap?**
→ If yes, name the trap and consequence. If no → ❌ N/A

**Gate:** ≥ 1 answer must be non-null. If all three are N/A → NO-GO.

### Step 3: Atomicity check

- Can the concept be expressed in < 300 words of core content?
- Does it contain exactly ONE concept? If multiple → suggest splitting into separate notes.

### Step 4: Link suggestion (ranked)

Scan `5_Galaxy/` filenames and read frontmatter tags. Suggest links using this priority:

1. **Hub notes** (if thematically related):
   - `Phán đoán không thể uỷ thác cho AI` (judgment core)
   - `Physical-World Interface — Kiểm Chứng Bằng Thực Tế` (validation)
   - `Shifting the Burden Archetype` (systems thinking)
   - `Nguyên Tắc Atomic Note` (KM foundation)

2. **Same-cluster notes** — identify which cluster (A-I per CLAUDE.md) the concept belongs to, then suggest notes from that cluster

3. **Cross-cluster notes** — suggest ≥ 1 note from a different cluster that shares tags or themes

### Step 5: Output verdict

```
## Galaxy Gate — [Concept Name]

### Quality Test
(a) Changes design: [answer or ❌ N/A]
(b) Changes strategy: [answer or ❌ N/A]
(c) Warns about trap: [answer or ❌ N/A]

### Verdict: [✅ GO / ❌ NO-GO]
```

**If ✅ GO**, also output:
```
### Preparation
- Cluster: [letter] — [cluster name]
- Hub note: [[hub note name]]
- Suggested links: [[Note 1]] (reason), [[Note 2]] (reason)
- Suggested tags: #type/permanent-note, #[galaxy-tag from: acq, sys, pahl, defense, product, ceo, meta, three-laws, warning]
- Suggested filename: [Vietnamese descriptive name with dấu].md
```

**If ❌ NO-GO**, output:
```
### Why Not Yet
- Reason: [why it doesn't pass the gate]
- Suggestion: [how to distill further, or where to put it instead (Inbox? Resources?)]
```
