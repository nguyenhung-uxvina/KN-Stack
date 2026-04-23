---
name: galaxy-note
description: Guided creation of IPARAG Galaxy permanent notes. This skill should be used when the user wants to create a new Zettelkasten permanent note in 5_Galaxy/, extract atomic concepts from articles/projects/transcripts, or when running the THINH H (Hoa) step. Ensures atomic concept, proper wikilinks (at least 2), cluster assignment, and frontmatter. Always proposes draft for CEO approval before creating file.
---

# Galaxy Note Creator

Create atomic permanent notes for the IPARAG Galaxy (5_Galaxy/) following Zettelkasten principles.

## When to Use

- User says "create Galaxy note", "permanent note", "extract insight"
- During THINH practice (H step: Hoa/Atomize)
- After reading articles, completing project milestones, or processing transcripts
- When user has a raw concept that needs formalization

## Workflow

### 1. Identify Source Type

Determine where the insight comes from:
- **Project experience** - insight emerged from design work (e.g., VN-XUONG-UUV gate review)
- **Article/book** - extracted atomic concept from reading material
- **Voice transcript** - processed from Tana/StenoAI capture
- **Direct insight** - user states concept directly

### 2. Extract Atomic Concept

Each Galaxy note = exactly 1 concept. To verify atomicity:
- State the concept in 1-3 sentences
- If the statement contains "and" connecting two independent ideas, split into 2 notes
- The concept must answer at least 1 of these questions:
  1. Does this change how I design products?
  2. Does this change strategic decisions?
  3. Does this warn against a specific trap?

If none apply, the concept is not Galaxy-worthy. Route to Resources or discard.

### 3. Determine Cluster and Links

Read `references/galaxy-state.md` to check current Galaxy notes and clusters.

Assign the note to one of 8 clusters:

| Cluster | Topic | Hub Note |
|---------|-------|----------|
| A | KM Fundamentals | Nguyen Tac Atomic Note |
| B | Network Effects | Activation Threshold |
| C | Judgment & Agency | Phan doan khong the uy thac cho AI |
| D | AI Failure Modes | AI Dependency Spiral (R3) |
| E | Systems Archetypes | Shifting the Burden |
| F | Knowledge Lifecycle | Vault = Graveyard |
| G | Pahl-Beitz Technical | PZT vs MEMS |
| H | Physical Design | Foam-Filled HDPE |

Requirements:
- Link to hub note of assigned cluster
- Add at least 1 cross-cluster link (different cluster)
- Minimum 2 total wikilinks, target 3+

### 4. Draft the Note

Use this exact structure:

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: permanent-note
tags: [#type/permanent-note, <galaxy-tags>]
links: [[Note 1]], [[Note 2]], [[Note 3]]
---

# <Title> (Vietnamese with diacritics)

## Y Tuong Cot Loi
1-3 sentences. The core concept in the user's own voice.

## Giai Thich Chi Tiet
Expand with examples, diagrams, evidence. Reference the source experience.

## Tai Sao Dieu Nay Quan Trong?
Personal relevance to Workshop X, current projects, or CEO decision-making.

## Lien Ket
- [[Note 1]] - annotation explaining why linked
- [[Note 2]] - annotation explaining why linked
- [[Note 3]] - cross-cluster annotation

## Nguon Goc
Citation + date encountered. For project insights: project name + phase + date.
```

Galaxy tags (pick relevant): `#acq` (ACH), `#sys` (systems), `#pahl` (Pahl-Beitz), `#defense` (VN defense), `#product` (technical), `#ceo` (leadership), `#meta` (learning), `#three-laws` (distilled laws), `#warning` (traps)

### 5. Present Draft for Approval

NEVER auto-create the file. Always present the draft to the CEO with:

1. Proposed filename (Vietnamese with diacritics, pattern: `Concept Name - Vietnamese Subtitle`)
2. Full note content
3. Cluster assignment rationale
4. Wikilinks with justification
5. Ask: "Create this note?" or "Edit before creating?"

### 6. Create File

After CEO approval:
- Write file to `5_Galaxy/<filename>.md`
- File structure is FLAT (no subdirectories in Galaxy)
- Update Galaxy count in CLAUDE.md if needed
- Update GALAXY-ROADMAP.md count if it exists

## Quality Gates

Before presenting draft, verify:

| Check | Requirement |
|-------|-------------|
| Atomic | Exactly 1 concept per note |
| Links | >= 2 wikilinks, at least 1 cross-cluster |
| Voice | Written in CEO's voice, not copy-paste from source |
| Galaxy-worthy | Answers >= 1 of the 3 qualifying questions |
| Vietnamese | Title and content use proper diacritical marks |
| Flat | No subdirectory - file goes directly in 5_Galaxy/ |
| Tags | Uses Galaxy tag system (#acq, #sys, #pahl, etc.) |

## COD Classification

This skill is **Offload (O2)** - AI drafts, human reviews and approves.
The judgment of whether a concept is Galaxy-worthy remains **Core (C)**.
