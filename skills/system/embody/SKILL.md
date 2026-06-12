---
name: embody
description: Runs Pahl-Beitz Phase 3 Embodiment Design, producing a System Architecture block diagram, Interface Control Document (ICD), spatial layout, preliminary BOM, DfX review (DfM/DfA/DfT/DfMaint), and power/thermal budget. Use after Phase 2 concept selection Gate is passed. Triggers on: "phase 3", "embodiment design", "system architecture", "ICD", "thiết kế hiện thân", "kiến trúc hệ thống", "giai đoạn 3".
---
Run Phase 3 Embodiment Design for a project following Pahl-Beitz systematic design.

Usage: /embody [project_name] OR provide details interactively.

1. If $ARGUMENTS provided, use as project name; otherwise ask:
   - What project? (project code or name)
   - Which concept variant was selected from Phase 2?

2. Read existing project artifacts:
   - `1_Projects/{{project}}/Status.md` — verify Phase 2 Gate PASSED
   - Phase 2 documents (winning concept, evaluation, morphological matrix)
   - Phase 1 documents (requirements list, function structure)
   - Any existing Phase 3 documents (avoid duplicates)

3. Phase 3 Embodiment Design produces these documents:

   **Doc: System Architecture v2.0**
   - Block diagram: all subsystems with interfaces
   - For each subsystem: function, key specs, selected working principle, spatial allocation
   - Subsystem categories (typical): Mechanical, Electronics, Software, Power, Thermal, HMI
   - Traceability: each subsystem block → requirements it fulfills

   **Doc: Interface Control Document (ICD)**
   - Every interface between subsystems documented:
     - Mechanical interfaces (mounting, alignment, tolerances)
     - Electrical interfaces (connectors, pinouts, voltage levels, protocols)
     - Software interfaces (APIs, data formats, timing)
     - Thermal interfaces (heat paths, cooling requirements)
   - Interface responsibility matrix: who owns each interface
   - Integration debt tracker: unresolved interface TBDs

   **Doc: Preliminary Layout**
   - Spatial arrangement of all subsystems
   - Envelope dimensions and mass budget
   - Assembly sequence (what goes in first/last)
   - Access for maintenance
   - Reference: Pahl-Beitz Chapter 7 (embodiment guidelines)

   **Doc: DfX Review**
   - DfM (Design for Manufacturing): part count, process selection, tolerances
   - DfA (Design for Assembly): assembly steps, tools required, skill level
   - DfT (Design for Test): test points, built-in test features
   - DfMaint (Design for Maintenance): MTBF, MTTR, replaceable modules
   - Local content analysis: Vietnam-sourceable vs import components

   **Doc: Preliminary BOM**
   - All components with: Part Name | Qty | Specification | Source (Local/Import) | Est. Unit Cost | Lead Time
   - Cost rollup vs target budget
   - Local content percentage
   - Long-lead items flagged
   - Critical single-source items flagged

   **Doc: Power Budget** (if applicable)
   - Every subsystem: operating power, standby power, peak power
   - Total system power vs supply capacity
   - Margin analysis (target: ≥20% margin)
   - Thermal dissipation estimate

   **Doc: Risk Update**
   - Update Phase 2 risk register with embodiment-specific risks
   - Add manufacturing risks, supply chain risks, integration risks
   - Physical prototype test plan (what to validate first)

4. For each document:
   - Draft and present to user (HITL checkpoint)
   - Wait for approval before proceeding
   - Save to `1_Projects/{{project}}/Phase3-Embodiment/{{NNN}}_{{DocName}}_v{{X}}.0.md`

5. After all documents, update Status.md. Suggest: Phase 3 Gate Review or physical prototype.

RULES:
- Phase 2 Gate MUST be passed — check Status.md
- Every requirement must trace to at least one subsystem
- Flag any subsystem with TRL < 6 — it needs a prototype test
- BOM must show local content % — this is a hard constraint for VN defense
- Power budget mandatory for any electronic system
- COD: Offload (AI drafts layout, CEO reviews and decides on trade-offs)
- Physical prototype plan is the MOST IMPORTANT output — dP/dt > 0 depends on it
- Number documents continuing from Phase 2 sequence
