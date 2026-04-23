Run Phase 4 Detail Design for a project following Pahl-Beitz systematic design.

Usage: /detail [project_name] OR provide details interactively.

1. If $ARGUMENTS provided, use as project name; otherwise ask:
   - What project? (project code or name)
   - Is Phase 3 Embodiment complete? (system architecture, BOM, ICD)

2. Read existing project artifacts:
   - `1_Projects/{{project}}/Status.md` -- verify Phase 3 done
   - Phase 3 documents (architecture, BOM, ICD, DfX)
   - Phase 1 requirements (for final verification matrix)

3. Phase 4 Detail Design produces these documents:

   **Doc: Final BOM v2.0** (refine from Phase 3 preliminary)
   - Complete part-level BOM with actual supplier quotes
   - Final cost rollup vs budget
   - Long-lead procurement list with order dates
   - Local content final percentage

   **Doc: Manufacturing Plan**
   - Process sequence for each custom part
   - Tooling and fixture requirements
   - Quality inspection points (in-process + final)
   - Estimated manufacturing time per unit

   **Doc: Assembly Instructions**
   - Step-by-step assembly sequence with diagrams
   - Tools and equipment list
   - Torque specs, adhesive cure times, alignment procedures
   - Skill level required per step

   **Doc: Test Procedures**
   - Unit-level test procedures (per subsystem)
   - Integration test procedures
   - System-level acceptance test
   - Reference: verification plan from /verify

   **Doc: Documentation Package**
   - Drawing list (or 3D model references)
   - Wiring diagrams / schematics
   - Software version and build instructions
   - User manual outline
   - Maintenance manual outline

4. For each document:
   - Draft and present (HITL checkpoint)
   - Wait for approval
   - Save to `1_Projects/{{project}}/Phase4-Detail/{{NNN}}_{{DocName}}_v1.0.md`

5. After all documents, update Status.md. Suggest: Phase 4 Gate Review or prototype build.

RULES:
- Phase 3 Gate MUST be passed before Phase 4
- BOM must have ACTUAL quotes, not estimates -- flag any remaining estimates
- Manufacturing plan must be feasible with Vietnamese workshop capabilities
- COD: Offload (AI drafts, CEO reviews and approves for production)
- This is the last design phase -- output must be BUILD-READY
