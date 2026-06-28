# Notebook Index — mentor-naval-architect-council

| Facet | Notebook ID | NLM URL | Sources | Scope | Last refresh | Primary? |
|-------|------------|---------|:-------:|-------|:------------:|:--------:|
| primary | 41390b69-f462-47a5-806a-41126df09a0d | https://notebooklm.google.com/notebook/41390b69-f462-47a5-806a-41126df09a0d | 42 | Taylor/PNA/Gertler classics + Tupper/Molland/MIT-OCW + shallow-water/shear-current; (prior untracked expansion) mooring/anchoring + ABS/ISO scantlings + DNV ts301 + floating-offshore-wind; (+11 Exa 2026-06-14) floating pontoon/ribbon bridge hydrodynamics, multi-hull/demihull interference, shallow-water squat | 2026-06-14 | ✓ |

**Split trigger:** >45 sources → ⚠ APPROACHING (42/45). Plan now THREE facets, not two: `taylor-hydrodynamics` (resistance/propulsion/shallow-water/squat/multihull) + `lewis-stability-structures` (stability, strength, seakeeping, scantlings) + `vsn1500-floating-bridge` (pontoon/ribbon bridge hydrodynamics, pontoon-pontoon interaction, mooring, wave-current).
**Current: single facet** — all queries use primary notebook.

## Added 2026-06-14 via Exa Channel 0 (11)

### Floating pontoon / ribbon bridge hydrodynamics (VSN-1500 IS a floating pontoon bridge)
- ERDC — Improved Ribbon Bridge (IRB) structural-response validation (MLC 96, anchorage in moving water) `1aa3402b`
- Dynamic responses of a ribbon floating bridge under moving loads (small draught; wave+current+moving load) `bb8f46ca` *(text — SD blocked)*
- SINTEF — wave-current interaction on a fjord-crossing floating pontoon bridge `4a615182`
- SINTEF Ocean — extensive hydro-elastic floating-bridge tests (pontoon-pontoon interaction, wave trapping, KC drag) `195931bc` *(text — SD blocked)*

### Multi-hull / demihull interference (multi-pontoon "phà" wave interference)
- Strathprints — demihull interference + shallow-water effects, catamaran (OpenFOAM 2025) `721639af`
- Experimental interference, high-speed catamarans (Delft 372; up to 30% penalty, Fr-dependent) `090dd65d` *(text — SD blocked)*
- MDPI JMSE 2025 — catamaran hull arrangement / demihull spacing (BS/LPP 0.2 → +14%) `529d342e`

### Shallow-water resistance / squat (refines existing single shallow-water source)
- Resistance of an inland vessel in shallow & confined water (Schijf critical speed, ITTC form factor) `8aef9075`
- Elsherbiny — experimental squat, New Suez Canal (KCS; Fnh<0.4 threshold) `bdd1e84e`
- MDPI JMSE 2025 — draft-control / sinkage model, ship passing a lock (Yangtze inland) `29434aaf`
- MDPI JMSE — KCS resistance vs water depth, model/full-scale (Raven correction) `1ef80bde`

> ⚠ Hygiene 2026-06-14: live notebook had drifted from registry (18→32). Deleted 1 junk Cloudflare stub ("Just a moment...", `39e21f68`). Deduped 3 ScienceDirect URL stubs that auto-landed alongside their richer text versions. **Untracked extras now recorded** (added in a prior un-logged expansion, kept — on-topic for VSN-1500 floating/moored structure): mooring/anchoring DLC review `29facd7a`, catenary anchor-leg mooring `b63f9b72`, ABS scantlings `8f84732c`, ISO 12215-3 `54d99365` / 12215-5 `31590a5d`, hull-block construction `ef5a1070`, ship construction `77ba0eb6`, NREL floating-wind `800b2441`, WFO floating-wind blog `fe5aaa60`, ABS steel-vessels U90 `ce71f7f8`, ScienceDirect mooring-design topic `a2386251`, DNV ts301 hull rules `cde29fe6`. ⚠ STILL SUSPECT: generic **"Publications"** (`2ffb9e8e`) — left in place per CEO (delete-junk-stub-only); verify at next refresh. Final: 42 sources.
