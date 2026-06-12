# Domain Mapping Heuristics — book-to-codebase R3/R4

> Used by `/btc-charter` (R3) for HELIX-FORGE placement decision (A/B/C/D)
> and `/btc-architect` (R4) for domain taxonomy construction.

---

## Part 1 — HELIX-FORGE Placement Decision (R3)

### Classification Rules

**Type A — Forward Pipeline Enhancement**
Criteria (ALL must hold):
- [ ] The book encodes ≤3 cohesive skills that slot into an existing HELIX or FORGE pipeline phase
- [ ] The skills extend an existing pipeline step (not create a new domain)
- [ ] No new domain prefix needed — existing `helix-p{N}-*` or `forge-*` naming fits
- [ ] Deploy path: `d:\KN-Stack\skills\helix\` or `skills\forge\`

Example triggers: "book teaches a better way to write P2 requirements" → Type A (helix-p2-* additions)

---

**Type B — Domain-Specific (new named prefix)**
Criteria (ALL must hold):
- [ ] The book encodes 4-15 skills in a cohesive domain not in current KN-Stack taxonomy
- [ ] A single domain prefix adequately covers all skills (e.g., `acoustic-*`, `logistics-*`)
- [ ] The domain is standalone — not cross-portfolio compound learning
- [ ] Deploy path: `d:\KN-Stack\skills\{{new_domain}}\`

Example triggers: "underwater acoustics textbook" → Type B (`acoustic-*` domain, 6-10 skills)

---

**Type C — Compound Tool (cross-domain peer library)**
Criteria (ANY applies):
- [ ] The book encodes compound learning across 2+ existing KN-Stack domains (HELIX + FORGE, or FORGE + Galaxy, etc.)
- [ ] The book's process model maps to multiple pipeline phases across different domains
- [ ] A single domain prefix would misrepresent the skill set
- [ ] OR: the skill count is large enough (>15 skills) that a standalone repo with its own setup.sh makes more sense than merging into KN-Stack

Type C deployment:
- Standalone repo with own `setup.sh` and `CLAUDE.md`
- Junctions to `~/.claude/commands/` via own `setup.sh`
- Reference in KN-Stack `ARCHITECTURE.md` as peer library

Taxonomy preference for Type C: **Anchor-Based (γ)**
- Encodes the HELIX-FORGE verdict in the taxonomy itself
- Surfaces station/gate distinction hidden in bare source slugs

Example: gstack skill library → Type C (station+gate pipeline pattern = HELIX, compound cluster = FORGE peer)

---

**Type D — Galaxy Note Only**
Criteria (ANY applies):
- [ ] The book encodes abstract concepts not operational enough for a skill (no trigger/action structure)
- [ ] The book is deeply domain-specific to a single product (not transferable to Workshop X broadly)
- [ ] All extracted specs have `concept_kind = architectural_principle` at a meta level
- [ ] OR: Apply This count < 3 AND prose-derived specs < 5

Type D handling:
- No SKILL.md files generated
- R9 surfaces 3-7 Galaxy permanent note candidates from the concepts
- Route to `/galaxy-note` for manual creation

---

### Decision Flowchart (R3 walkthrough)

```
START: Extraction Manifest summary (Apply This count, concept_kind distribution, chapter count)

1. Apply This count ≥ 5?
   NO → Type D (insufficient operational density)
   YES → continue

2. All specs fit in 1-2 existing pipeline phases?
   YES → Type A
   NO → continue

3. All specs fit in 1 new domain prefix?
   YES → Type B
   NO → continue

4. Specs span 2+ existing KN-Stack domains OR compound learning?
   YES → Type C
   NO → re-examine with CEO; likely edge B/C case

PRESENT TO CEO: recommended type + rationale + alternative.
CEO makes final call.
```

---

## Part 2 — Domain Taxonomy Construction (R4)

### Taxonomy Styles

Three taxonomy styles. R4 recommends one based on book structure; CEO approves.

**Style α — Flat (concept-driven)**
```
skills/
  decision-rule-A/
  decision-rule-B/
  mechanism-C/
  discipline-D/
```
- Best when: book has no explicit process structure; concepts are peers
- Risk: no natural ordering; DAG must be constructed manually
- Use when: Type B, ≤8 skills

**Style β — Phase-Prefixed (pipeline-driven)**
```
skills/
  p1-[concept]/
  p2-[concept]/
  p3-[concept]/
```
- Best when: book has explicit phases or stages (Chapter 1 = phase 1, etc.)
- Risk: phase numbers become meaningless if book reorganized
- Use when: Type A or Type B with clear chapter-to-phase mapping

**Style γ — Anchor-Based (structure-preserving)**
```
skills/
  [anchor-name]/
    [station-skill]/
    [gate-skill]/
  [second-anchor]/
    ...
```
- Best when: book has anchor concepts that organize everything else
- Encodes HELIX-FORGE verdict (station = HELIX execute, gate = FORGE review)
- Best for Type C compound libraries
- Recommended when `--from-pipeline` (book structure already validated)

---

### Domain Naming Rules

1. **Derive from book vocabulary** — use the book's own terminology, not KN-Stack terms
2. **Kebab-case** — all lowercase, hyphens, no underscores
3. **No acronyms** — unless in book's glossary
4. **Domain name = the skill's broadest natural grouping** — not the chapter title
5. **Max 8 domains** — if more than 8, merge related ones; surface as footnote for CEO
6. **Domain names must survive the library** — don't use names that will be confusing 2 years from now

---

### DAG Construction Rules

The skill DAG in `R4-Architecture.md` defines dependency direction for validation (R8 V3).

**Edge types:**
- `→ depends_on` — skill B requires output of skill A
- `→ informs` — skill A provides context to skill B (non-blocking)
- `→ guards` — anti_pattern_guard C protects a step in skill A

**DAG construction heuristics:**
1. Start from `mechanism` skills — they have explicit inputs/outputs; draw edges from their inputs/outputs
2. `decision_rule` skills are typically leaves or mid-nodes (they take context, produce decisions)
3. `discipline_contract` skills are typically scheduled (no DAG edges, just cadence)
4. `compounding_loop` skills sit at the end of a sequence (they amplify upstream effects)
5. `anti_pattern_guard` skills are parallel guards — they don't block the main path
6. Cyclic dependencies = a `compounding_loop` — OK if intentional; flag for CEO if unexpected

**DAG validation in R8 V3:**
- No unresolved `depends_on` edges (skill references another skill not in the library)
- No unexpected cycles outside declared `compounding_loop` skills
- All `guards` edges point to an existing skill in the library

---

## Part 3 — R5.5 KN-Stack Overlap Scan (--deep-scaffold)

### Delta Categories

When `--deep-scaffold` is active, R5.5 scans existing KN-Stack skills (`d:\KN-Stack\skills\**\SKILL.md`) against the proposed skill list from R4.

```
Category A — Direct overlap: skill already exists in KN-Stack with same concept
  Action: do not create; R6 generates a "reference wrapper" pointing to existing skill

Category B — Partial overlap: similar concept, different domain or context
  Action: create new skill; note in SKILL.md Integration section that KN-Stack skill also covers related ground

Category C — No overlap: new concept not in KN-Stack
  Action: create skill normally (Wave 1-3 confidence)

Category D — Book gap: KN-Stack has skills in this area that the book did NOT cover
  Action: surface in R9 DMIR Reflect section as "forward pipeline feedback — consider covering in next book edition"
```

### Scan Method

```
For each proposed skill S in R4-Architecture.md:
  1. Extract concept keywords from S's name + description
  2. Grep d:\KN-Stack\skills\**\SKILL.md for those keywords (case-insensitive)
  3. Read top 3 matches; compare concept_kind + scope
  4. Classify as A/B/C

For Cat D (inverse):
  5. List all KN-Stack skills in domains touched by R4 taxonomy
  6. Check each against R2-Extraction-Manifest.md
  7. Skills with no Apply This coverage AND no prose spec = Cat D
```

Output: `R5.5-Delta-Report.md`
```
## Delta Report — {{slug}} vs KN-Stack

### Category A — Overlap (skip)
| Proposed Skill | Existing KN-Stack Skill | Note |

### Category B — Partial (create with note)
| Proposed Skill | Related KN-Stack Skill | Difference |

### Category C — New (create)
| Proposed Skill | Domain | concept_kind |

### Category D — Book Gaps (feedback)
| KN-Stack Skill | Domain | Signal for next book |

Summary: {{A_count}} skip / {{B_count}} with note / {{C_count}} new / {{D_count}} gaps
```
