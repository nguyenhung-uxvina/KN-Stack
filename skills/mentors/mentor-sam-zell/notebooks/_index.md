# mentor-sam-zell — Notebooks Index

Facet registry for NLM notebooks. Single facet (26 sources < 45 split threshold).

---

## Facets

| Facet | Slug | NLM URL | NLM ID | Sources | Scope | Primary? | Last refresh |
|-------|------|---------|--------|:-------:|-------|:--------:|:------------:|
| Full Doctrine | primary | https://notebooklm.google.com/notebook/d2cb143a-57b0-4d31-b9f9-ef4643d2fe11 | d2cb143a-57b0-4d31-b9f9-ef4643d2fe11 | 26 | Distressed investing, supply/demand, REIT architecture, capital cycles, emerging markets, leadership, team/culture | ✓ | 2026-05-13 |

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
