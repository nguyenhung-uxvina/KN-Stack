# mentor-sam-zell — Notebooks Index

Facet registry for NLM notebooks. Single facet (24 sources < 45 split threshold).

---

## Facets

| Facet | Slug | NLM URL | NLM ID | Sources | Scope | Primary? | Last refresh |
|-------|------|---------|--------|:-------:|-------|:--------:|:------------:|
| Full Doctrine | primary | https://notebooklm.google.com/notebook/d2cb143a-57b0-4d31-b9f9-ef4643d2fe11 | d2cb143a-57b0-4d31-b9f9-ef4643d2fe11 | 24 | Distressed investing, supply/demand, REIT architecture, capital cycles, emerging markets, leadership, team/culture | ✓ | 2026-05-13 (count reconciled 2026-06-14, 2× purge 2026-06-14) |

## Cross-Facet Query (default)

Single-facet mentor. All queries hit the primary notebook.
`--facet primary` targets this facet explicitly (same as default).
`--facet auto` resolves to primary.

## ADD Pipeline Record

| Step | Date | Action |
|------|------|--------|
| A1 | 2026-05-13 | Slug `sam-zell` confirmed — no duplicate in registry |
| A2 | 2026-05-13 | Source discovery: 43 found, 27 selected for ingestion |
| A3 | 2026-05-13 | CEO approved all 27 sources |
| A3.5 | 2026-05-13 | 27 sources < 45 threshold — single facet, no split |
| A4 | 2026-05-13 | Notebook created, 26 sources ingested (1 CBRE page blocked, 1 CBRE PDF blocked, GlobeSt/Britannica/Bisnow failed) |
| Reconcile | 2026-06-14 | Live notebook_get confirmed 27 sources — count corrected 26→27 in registry |
| Purge | 2026-06-14 | Deleted 2 Cloudflare CBRE blocks — count 27→25; bare "Wide Moat Research" (7ad98e0e) kept but flagged |
| Purge 2 | 2026-06-14 | "Wide Moat Research" (7ad98e0e) inspected → 404 "page doesn't exist" → deleted. Count 25→24, clean |
| A4 persona | 2026-05-13 | `chat_configure` persona set — strict purity, VN adaptation frame mandatory |
| A5 | 2026-05-13 | 8-query foundational extraction complete (Q1-Q8 all parallel) |
| A6 | pending | Studio artifacts (briefing doc, audio, quiz, flashcards) — not yet created |
| A7 | 2026-05-13 | Skill files generated: SKILL.md, persona.md, seed-sources.md, _index.md |
| A8 | 2026-05-13 | Junction deployed via setup.sh --install |
| A9 | 2026-05-13 | Registry updated — mentor_count: 2→3, sam-zell row added |
| A10 | 2026-05-13 | profile.md + reliability_log.md initialized |

## Studio Artifacts (A6 — pending)

Run these to complete A6:
- `studio_create(notebook_id="d2cb143a-57b0-4d31-b9f9-ef4643d2fe11", artifact_type="briefing_doc")`
- `studio_create(notebook_id="d2cb143a-57b0-4d31-b9f9-ef4643d2fe11", artifact_type="audio")`
- `studio_create(notebook_id="d2cb143a-57b0-4d31-b9f9-ef4643d2fe11", artifact_type="quiz")`
- `studio_create(notebook_id="d2cb143a-57b0-4d31-b9f9-ef4643d2fe11", artifact_type="flashcards")`

## Reconciled 2026-06-14 (registry-drift audit)

count corrected 26→27 to match live notebook (notebook_get confirmed source_count=27).

Sources present in live notebook NOT previously registered in seed-sources.md:

| NLM Source ID | Title | Notes |
|---------------|-------|-------|
| a48c95e5-287d-4706-b895-b22a6ae2729a | Just a moment... | Likely second CBRE page; Cloudflare block page ingested |
| 29b65b02-c19e-4ff1-9940-fbb8d28c3184 | Sam Zell — Emerging Market Playbook, Global Real Estate Doctrine, and Supply/Demand Analysis Framework | Not in original seed-sources registry; appears to be a synthesized/curated document |

Note: The original ADD pipeline log stated "26 sources ingested" but live notebook shows 27. One additional source was present or added post-ingestion. No NLM source changes made — registry only.

## Junk purge 2026-06-14

Purged 2 Cloudflare "Just a moment…" CBRE blocks from NLM (count 27→25): source IDs not separately recorded at purge time — both were Cloudflare gate pages blocking CBRE domain content.

Kept-but-flagged for manual review:
- `7ad98e0e` — bare title "Wide Moat Research": ambiguous — may be a real Wide Moat Research report or a generic landing/paywall page. Manual NLM inspection required to determine if it should be kept or deleted.
