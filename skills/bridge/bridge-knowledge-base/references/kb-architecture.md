# KB Architecture — 3 Layers

## LAYER 1: STANDARDS AND METHODS
Changes slowly, formal documents.

Contents:
- Design methodology templates (Pahl-Beitz phases, HELIX protocols)
- Standards library (MIL-STD, TCVN, STANAG references)
- Product templates (requirements checklist, DfX rules)
- FORGE templates (SHIFT checklist, fallback template, cost model)

Location: 3_Resources/
Update: quarterly or when standards change

## LAYER 2: PRODUCT KNOWLEDGE
Changes per project, semi-formal.

Contents:
- Per-product: requirements, function structures, ICDs, test results
- Design decisions log (from design journals)
- Validation evidence
- Model library catalog

Location: 1_Projects/[product-name]/
Update: per-project, synced with HELIX phases

Expected artifacts per Pahl-Beitz phase:
- Phase 0: Project charter, stakeholder analysis
- Phase 1: Requirements list, function structure, competitive analysis, standards matrix
- Phase 2: Morphological matrix, weight estimate, stability check, concept description
- Phase 3: GA drawing, BOM, tolerance analysis, manufacturing plan
- Phase 4: Detail drawings, assembly instructions, test procedures

## LAYER 3: TACIT AND INSIGHTS
Changes continuously, captured from work.

Contents:
- Design review extracts (from bridge-signal-extract)
- Field feedback digests (structured from anecdotal)
- Cross-product lessons (from bridge-cross-learn)
- CEO decision rationale (from bridge-judgment)
- Galaxy permanent notes (atomic insights)

Location: 5_Galaxy/, 2_Areas/
Update: weekly, continuous capture

## Search Patterns

To search L1: Glob "3_Resources/**/*.md"
To search L2: Glob "1_Projects/[product]/**/*.md"
To search L3: Glob "5_Galaxy/*.md" + Grep in 2_Areas/
Cross-layer: Grep across all directories for keyword
