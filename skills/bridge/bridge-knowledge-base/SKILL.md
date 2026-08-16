---
name: bridge-knowledge-base
description: Organizational knowledge management system for Workshop X. This skill should be used when the user wants to search, capture, index, or serve knowledge across products and projects. Covers 3 layers (Standards, Product Knowledge, Tacit Insights) and integrates with FORGE and HELIX frameworks. Triggers on keywords like KB, knowledge base, document, find information, tri thuc.
---

# Bridge Knowledge Base — Workshop X Organizational Knowledge System

Manage the 3-layer knowledge architecture for Workshop X. Foundation skill — all other BRIDGE skills depend on this.

## When to Use

- User asks to find information across projects or products
- User wants to capture knowledge, lessons learned, or design decisions
- User needs context from similar past projects before starting new work
- During HELIX phases: inject relevant KB context
- Gap detection: identify products with missing documentation

## Knowledge Architecture

Read `references/kb-architecture.md` for the full 3-layer structure.

### Quick Reference

| Layer | Content | Update Frequency | Location |
|-------|---------|-----------------|----------|
| L1: Standards | Design methodology, MIL-STD, templates | Quarterly | 3_Resources/ |
| L1b: TRIZ Patterns | Proven TRIZ principles applied across WX products | Per-project (after Phase 2) | 2_Areas/HELIX/TRIZ-Applied-Patterns.md |
| L2: Product | Requirements, function structures, ICDs, test results | Per-project | 1_Projects/ |
| L3: Tacit | Design review extracts, field feedback, CEO decisions | Weekly | 5_Galaxy/, 2_Areas/ |

### L1b: TRIZ Applied Patterns (Cross-Product Reuse)

When a TRIZ principle is successfully applied to a product (validated in Phase 2+ or dry run), capture it as a reusable pattern:

```
TRIZ APPLIED PATTERNS — Workshop X

| Pattern ID | TRIZ # | Principle | Product Applied | Phase | Result (I-Level) | Reuse Candidates |
|-----------|--------|-----------|----------------|-------|-----------------|-----------------|
| TP-001 | #28 | Mechanics substitution | VN-12.7MM-SIM | P2 | L2 (pneumatic vs electric) | BB-01, VN-USV |
| TP-002 | #1 | Segmentation | VN-12.7MM-SIM | P2 | L3 (Two-Channel) | Any multi-domain |
| TP-003 | #7 | Nesting | VN-XUONG-UUV | P2 | L3 (cable drum inside UUV) | Containerized systems |
| TP-004 | #10 | Preliminary action | VN-12.7MM-SIM | P2 | L2 (data-first before ACH) | All ACH products |
| TP-005 | #8 | Anti-weight | VN-AST-MSL-001 | P2 | L2 (foam-filled HDPE) | Marine products |
| TP-006 | #33 | Homogeneity | VN-AST-MSL-001 | P2 | L2 (all-HDPE construction) | Marine products |
```

**When to query L1b:** At the START of `/helix-concept-generate` (Step 0), before morphological matrix. Ask: "Which TRIZ patterns have been proven at WX for this product domain?"

**When to update L1b:** After every Phase 2 completion or TRIZ dry run. Extract patterns from `TRIZ_Validation_Dry_Run_*.md` or concept evaluation docs.

**Impact:** New engineer starting Phase 2 gets a Level 2 floor immediately by applying proven patterns — no re-discovery needed.

## Workflow

### SEARCH Mode (most common)

1. Parse user query to identify: product, topic, knowledge layer
2. Search vault using Glob and Grep across relevant directories
3. Return structured results with source, confidence level, and related items
4. Flag if query hits a KB gap (no results for expected topic)

### CAPTURE Mode

1. Identify knowledge type: standard (L1), product artifact (L2), or insight (L3)
2. Route to correct location:
   - L1: `3_Resources/` with proper template
   - L2: `1_Projects/[product]/` with phase-appropriate naming
   - L3: `5_Galaxy/` (use galaxy-note skill) or `2_Areas/` dashboard
3. Add metadata: date, source, confidence level, cross-references
4. Update relevant indexes

### GAP DETECTION Mode

1. Scan each active project for expected L2 artifacts per Pahl-Beitz phase
2. Compare against checklist: requirements list, function structure, ICD, weight estimate, stability check, etc.
3. Report gaps with severity:
   - RED: Missing artifact blocking current phase gate
   - YELLOW: Missing artifact needed within 30 days
   - GREEN: Optional or future-phase artifact
4. Present gap report to CEO for prioritization

### CONTEXT INJECTION Mode

When user starts a HELIX task (clarify, concept, embody, detail):
1. Identify the product and phase
2. Search KB for: similar products, prior solutions, known constraints, field feedback
3. Present as "KB Context Brief" before the user begins work
4. Include: relevant Galaxy notes, prior design decisions, supplier constraints

## Integration Points

### Feeds Into (BRIDGE provides)
- FORGE: forge-scout reads KB for ACH opportunities
- FORGE: forge-cost reads KB for historical cost data
- HELIX: helix-task-clarify reads KB for similar requirements
- HELIX: helix-concept-generate reads KB for prior solutions

### Receives From (BRIDGE receives)
- FORGE: validation results, library entries
- HELIX: design journals, sync summaries, quality gate results
- BRIDGE: signal-extract outputs, cross-learn sessions

> 💡 Cần bản xuất bản (PNG/PDF cho báo cáo/trình duyệt)? Gợi ý: `/wx-diagram <type> Knowledge Base` — KHÔNG tự chạy, chỉ gợi ý.

## Metrics

| Metric | Current | Target 6M |
|--------|---------|-----------|
| KB Coverage (products with L2 docs) | ~20% | 70% |
| KB Currency (updated within 3 months) | Unknown | 80% |
| KB Utilization (queries/week) | 0 | 10+ |

## COD Classification

- SEARCH: Offload (O1) — AI searches, presents results
- CAPTURE routing: Offload (O2) — AI routes, human validates
- GAP DETECTION: Offload (O1) — AI scans, CEO prioritizes
- CONTEXT INJECTION: Offload (O1) — AI provides, human uses judgment
- Knowledge VALIDATION: Core (C) — human confirms accuracy
