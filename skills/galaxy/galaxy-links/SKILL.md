Batch scan and per-note link suggestions for IPARAG Galaxy permanent notes. Automates the THỊNH "Ích" (Connect) step — finds missing wikilinks between existing Galaxy notes using cluster-guided reasoning.

Usage: /galaxy-links [mode] where mode = scan | suggest "<note-title>"

---

## MODE 1: SCAN — Batch analysis of entire Galaxy

If $ARGUMENTS = "scan" or no arguments:

### Step 1: Load Galaxy inventory

Read `~/.claude/commands/galaxy-note/references/galaxy-state.md` for:
- Full note list with cluster assignments
- Hub notes and their link counts
- Cluster summary table
- Growth gaps

### Step 2: Read all Galaxy notes

Read ALL files in `5_Galaxy/` (use parallel reads for speed).

For each note, extract:
- **Title** (from H1 heading)
- **Core concept** (first 3 sentences of "Ý Tưởng Cốt Lõi" section)
- **Existing wikilinks** (from `links:` frontmatter field + all `[[...]]` in body)
- **Tags** (from frontmatter)
- **Cluster** (from galaxy-state.md mapping)

### Step 3: Build concept graph

Construct a mental model of the link network:
- Nodes = all Galaxy notes
- Edges = existing wikilinks (directional — A links to B ≠ B links to A)
- Note which notes are below minimum (< 2 links)
- Note which notes lack cross-cluster links

### Step 4: Cluster-guided similarity analysis

For each note, reason about which other notes should link to it but don't.

**Priority order for candidate matching:**
1. Same-cluster notes (most likely to share concepts)
2. Hub notes (high-connectivity — always consider)
3. Adjacent-cluster notes (clusters sharing themes, e.g., G↔H physical/technical)
4. Cross-cluster notes (highest compound value if connection is real)

**Link criteria — propose a link when:**
- Shared concept or domain (both discuss the same engineering principle)
- Complementary insight (one explains "why", the other "how")
- Warning↔trap pair (one note warns about a failure mode, another shows the mechanism)
- Same domain, different angle (e.g., two notes on HDPE from structural vs thermal perspective)
- Analogy across domains (e.g., KM principle maps to engineering design principle)

**Skip:** Pairs already linked. Pairs where the connection is too generic ("both are about design").

**Confidence scoring:**

| Level | Meaning | When to assign |
|-------|---------|----------------|
| ★★★ | Obvious | Shared concept, same domain, clear causal/logical relationship |
| ★★ | Plausible | Related theme, complementary angle — needs CEO judgment |
| ★ | Serendipity | Cross-domain analogy, novel stretch — may spark unexpected insight |

### Step 5: Generate output

```markdown
## Galaxy Link Scan — {{today}}

### Network Stats
- Notes: {{N}} | Total links: {{count all edges}} | Avg density: {{avg links/note}}
- Below minimum (< 2 links): {{list note titles}}
- Notes with 0 cross-cluster links: {{list}}
- Cross-cluster links: {{count}} / {{total}} ({{%}})

### Missing Links (high confidence)
| Note A | Note B | Reason | Confidence |
|--------|--------|--------|------------|
| [[X]] | [[Y]] | {{specific reason}} | ★★★ |
| ... | ... | ... | ... |

### Missing Links (medium confidence — CEO review)
| Note A | Note B | Reason | Confidence |
|--------|--------|--------|------------|
| ... | ... | ... | ★★ |

### Missing Links (serendipity)
| Note A | Note B | Reason | Confidence |
|--------|--------|--------|------------|
| ... | ... | ... | ★ |

### Orphan Risk
Notes with ≤ 1 cross-cluster link (isolated within their cluster):
- {{note title}} (cluster {{X}}, links: {{list}})

### Cluster Bridge Gaps
| Cluster Pair | Current Bridges | Gap | Suggested Bridge |
|-------------|----------------|-----|-----------------|
| {{X}}↔{{Y}} | {{N}} | {{missing}} | [[A]] ↔ [[B]] |

CEO: Chọn links nào để thêm? (Core — chất lượng link là judgment)
```

### Step 6: Apply CEO selections

After CEO selects which links to add:

**For each approved link A↔B:**

1. **Update Note A:**
   - Add `[[Note B]]` to `links:` frontmatter field (if not already present)
   - Add entry in "Liên Kết" section:
     ```
     - [[Note B]] — {{annotation from Reason column, Vietnamese with dấu}}
     ```
   - If note has no "Liên Kết" section, append one

2. **Update Note B** (bidirectional):
   - Add `[[Note A]]` to `links:` frontmatter field
   - Add entry in "Liên Kết" section:
     ```
     - [[Note A]] — {{annotation, reverse perspective}}
     ```

3. After all updates, report:
   ```
   ✓ {{N}} links added ({{N}} notes updated)
   New avg density: {{updated avg}}
   ```

---

## MODE 2: SUGGEST — Per-note link suggestions

If $ARGUMENTS starts with "suggest":

Parse the note title from arguments. Match against Galaxy note filenames (fuzzy — match by title substring).

### Step 1: Read target note

Read the target note from `5_Galaxy/`. Extract: title, core concept, all existing links, cluster, tags.

### Step 2: Load candidates

Read `~/.claude/commands/galaxy-note/references/galaxy-state.md` for full inventory.

Select ~10 candidate notes to read:
- All notes in same cluster (most likely connections)
- Hub notes from adjacent clusters
- Notes the target already links to (read to understand context, then find what's missing)

Read the selected candidate notes.

### Step 3: Generate suggestions

```markdown
## Link Suggestions for: [[{{note title}}]]

Cluster: {{X}} | Current links: {{N}} ({{list existing}})

### Suggested New Links
1. **[[Note A]]** (cluster {{Y}}) — {{reason}} (★★★)
2. **[[Note B]]** (cluster {{Z}}) — {{reason}} (★★★)
3. **[[Note C]]** (cluster {{W}}) — {{reason, cross-cluster}} (★★)
4. **[[Note D]]** (cluster {{V}}) — {{reason, serendipity}} (★)

CEO: Thêm links nào? (Core)
```

### Step 4: Apply CEO selections

Same bidirectional update logic as scan mode Step 6.

---

## RULES

- **NEVER auto-add links** — always propose, CEO decides (Core per COD)
- **Bidirectional** — every approved link updates BOTH notes
- **Vietnamese with dấu** — all annotations in Vietnamese with proper diacritical marks
- **Flat structure** — never create subdirectories in Galaxy
- `scan` reads all Galaxy files — token-heavy, use monthly or quarterly
- `suggest` reads ~10 files — lightweight, good for weekly THỊNH "Ích" drill
- **Scaling ceiling:** Current ~66 notes is comfortable. If Galaxy exceeds ~100 notes, switch to cluster-sampled scan (hub notes + random sample per cluster) instead of full read.
- Update both `links:` frontmatter AND body "Liên Kết" section
- Respect existing link annotations — don't overwrite, only append
- COD: Scan/analysis = **O** (Offload), Link approval = **C** (Core)
- Link to Galaxy: [[Forced Link Rule]], [[Retrieval Lớn Hơn Storage]], [[Nguyên Tắc Atomic Note]], [[Activation Threshold]]
