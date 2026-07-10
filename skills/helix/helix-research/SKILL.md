---
name: helix-research
description: "HELIX research dispatcher — single entry point for deep research on hard problems across P0-P4. Routes a standardized Research Brief through 3 tiers: T1 LOOKUP (topic-notebook/mentor NLM query, free), T2 SPRINT (/research v4.1 multi-channel with source tiers), T3 DEEP (NLM native Deep Research or deep-research fan-out). AI proposes tier, CEO approves per COD; risk_if_wrong=HIGH forces tier S/A sources; mandatory NOT-FOUND fail-safe (no silent model-memory answers). Triggers on: 'helix research', 'research brief', 'nghiên cứu sâu', 'tra cứu chuẩn', 'nghiên cứu vấn đề khó', 'prior art search', 'knowledge gap research', 'tìm tài liệu kỹ thuật', 'state of the art'."
---

# Helix Research — 3-Tier Research Dispatcher

> Harness class: `guide` (routing) + `sensor-inferential` (responses are cited evidence, propose-only).
> Every HELIX block that needs external knowledge sends a Research Brief here — no block picks its own executor.

## Operational Envelope

| CAN | CANNOT |
|-----|--------|
| Route briefs to T1/T2/T3 and run T1 immediately | Launch T2/T3 without CEO confirmation |
| Compile cited Research Responses | Answer HIGH-risk questions without S/A-tier sources |
| Propose escalation when a tier comes back empty | Fill gaps from model memory silently |
| Write Response files next to `_pipeline_state.md` | Modify pipeline state beyond its ledger line |

## Research Brief (input)

    brief_id: RB-<project>-<seq>          # e.g. RB-VNTGTF-003
    question: <specific research question>
    type: standards | prior-art | working-principle | state-of-the-art | knowledge-gap | market
    phase: P0 | P1 | P2 | P3 | P4
    source_block: <skill that generated it, e.g. helix-p2-firmup>
    risk_if_wrong: LOW | MEDIUM | HIGH    # HIGH => answer must rest on tier S/A sources
    known_sources: [<topic-notebook aliases, from project charter pinned notebooks>]
    deadline: <optional>

Ad-hoc use: `/helix-research "<question>"` — the skill drafts the brief, CEO confirms fields.

## Router

| Tier | Executor | When | COD |
|------|----------|------|-----|
| **T1 LOOKUP** | `/topic-notebook --query <alias>` or mentor NLM `notebook_query` | Lookup question; a registered notebook plausibly covers it (`known_sources` or type→alias map below) | Offload — run immediately, report back |
| **T2 SPRINT** | `/research "<question>"` (v4.1: multi-channel discovery, S/A/B/C tiers, NLM ingest) | New sources needed with tier control; standards/prior-art not covered by a notebook | Offload — **CEO confirms before launch** |
| **T3 DEEP** | `nlm` Mode 8 (NLM Deep Research native, background, token-free) OR `deep-research` plugin (fan-out + adversarial verify, faster, token-heavy) | Open/multi-faceted question, unclear sources; type = knowledge-gap or state-of-the-art | **CEO confirms + picks engine** |

Type→alias defaults for T1: `standards`→`std` (when built; until then T2), methodology→`vdi-2221`/`vdi-2206`, harness→`harness`, plus any charter-pinned alias.

**Routing rules:**
1. Always propose a tier + 1-line rationale. T1 runs immediately; T2/T3 wait for CEO.
2. `risk_if_wrong: HIGH` → final answer must cite tier S/A sources. T1 acceptable only if the notebook's sources are S/A; otherwise escalate to T2.
3. T1 returns NOT FOUND (fully or partially) → auto-propose T2 escalation. NEVER quietly substitute model memory.
4. Judgment questions (trade-off debates, RED subfunctions, doctrine) → route to `/mentor-board` CONSULT/PANEL instead of search. Retrieval ≠ judgment.
5. Patent/prior-art briefs at T2: include Espacenet + Google Patents in the search scope; standards briefs: include ASSIST Quick Search (quicksearch.dla.mil) for MIL-STD status.
6. Two consecutive T3 failures on the same brief → STOP, flag to CEO (roadmap trigger for internal deep-research harness — see HARNESS_STANDARD roadmap).

## Research Response (output)

File: `Research_Response_<brief_id>.md` in the project working folder (next to `_pipeline_state.md`; ad-hoc → current directory).

    # Research Response — <brief_id>
    Question: … · Tier used: T1/T2/T3 · Date: …

    ## Answer
    <each claim followed by [source — tier S/A/B/C]>

    ## NOT FOUND
    <parts of the question the sources did not answer — mandatory section, "—" only if truly complete>

    ## Confidence
    HIGH / MEDIUM / LOW + overall source-tier mix

    ## Next steps (propose-only)
    <escalate tier? add sources to a topic notebook? consult a mentor council?>

Ledger: the calling block appends ONE line to `_pipeline_state.md` Block Ledger:
`Research: <brief_id> → <tier> → <verdict 1-line> (see Research_Response_<brief_id>.md)`.

## COD
- Brief drafting, T1 execution, response compilation: **Offload**
- T2/T3 launch approval, engine choice, accepting a LOW-confidence answer for a HIGH-risk brief: **Core (CEO)**
- Re-running identical briefs: Default (skip — reuse the existing Response)

## Integration
- Called by Research Hooks in: helix-p1-preflight, helix-p1-requirements, helix-p2-frame, helix-p2-firmup, helix-p2-risk (ICDM), helix-domain-debate (escalation)
- Orchestrators list charter-pinned notebooks at Step 1.5 (context enrichment)
- Executors: /topic-notebook, /research, /nlm, /mentor-board, deep-research plugin

## Rules
1. NO block-order changes, no new pipeline blocks — this is a service skill, ONE BLOCK PER TURN untouched.
2. Every Response has a NOT FOUND section. Empty answers are reported, not padded.
3. Citations are per-claim, not per-document.
4. HIGH-risk + no S/A source = no answer; escalate or return NOT FOUND.
