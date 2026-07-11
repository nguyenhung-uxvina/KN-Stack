# seed-sources — topic notebook `std` (MIL-STD / TCVN / STANAG)

> Status: CEO-APPROVED 2026-07-11; rows 1-5 BUILT into notebook `514c700e-4449-47b4-b770-ad2d2dc3166a`.
> TCVN/STANAG/ISO (rows 6-9) DEFERRED — CEO to supply. Refresh via `/topic-notebook --refresh std`.
> ⚠ Ingest caveat: everyspec URLs captured LANDING-PAGE metadata (version/status/FSC) only, not the
> standard body. Notebook is valid for revision/status lookup + fail-safe reference; clause-level
> content (test method numbers, tolerances) needs the actual PDFs ingested as files — REFRESH follow-up.
> Tier scheme: S = standard/primary · A = authority/OEM · B = professional · C = community.

| # | Source | Tier | URL / access | Note |
|---|--------|------|--------------|------|
| 1 | MIL-STD-810H Environmental Engineering | S | http://everyspec.com/MIL-STD/MIL-STD-0800-0899/MIL-STD-810H_55998/ | Temp/humidity/vibration/salt-fog — P1 CAT 13 |
| 2 | MIL-STD-461G EMI/EMC | S | http://everyspec.com/MIL-STD/MIL-STD-0300-0499/MIL-STD-461G_53571/ | P1 CAT 6 |
| 3 | MIL-STD-882E System Safety | S | http://everyspec.com/MIL-STD/MIL-STD-0800-0899/MIL-STD-882E_41682/ | P1 CAT 7 |
| 4 | MIL-STD-1472H Human Engineering | S | http://everyspec.com/MIL-STD/MIL-STD-1400-1499/MIL-STD-1472H_57041/ | Ergonomics/conscript operators |
| 5 | ASSIST Quick Search (index page) | A | https://quicksearch.dla.mil/qsSearch.aspx | Authoritative status/revision lookup for any MIL-STD |
| 6 | ISO 128 (technical drawing general principles) — summary source | A | CEO to supply licensed copy or authoritative summary | P4 drawing |
| 7 | ISO 2768 general tolerances — summary source | A | CEO to supply licensed copy or authoritative summary | P4 drawing |
| 8 | TCVN <CEO to supply — never fabricated> | S | CEO to supply | Vietnamese national defense standards |
| 9 | STANAG <CEO to select applicable, e.g. 4370 environmental> | S | CEO to supply (NSO public or licensed) | NATO interop where relevant |

Open questions for CEO: which TCVN set applies across products; licensed ISO copies available?
