Initialize a new project with the Workshop X / Pahl-Beitz folder structure and Phase 0 artifacts.

Usage: /init [project_code] OR provide details interactively.

1. If $ARGUMENTS provided, use as project code; otherwise ask:
   - Project code (e.g., VN-XXX-XXX or BB-XX)?
   - Project name (human-readable)?
   - Tier: 1 (Prototype) / 2 (Product Dev) / 3 (Strategic)?
   - One-sentence description?
   - Target customer segment?
   - Estimated cost target (if known)?
   - Known deadline (if any)?

2. Create folder structure under `1_Projects/{{project_code}}/`:
   ```
   {{project_code}}/
   ├── Phase1-Task/
   ├── Phase2-Concept/
   ├── Phase3-Embodiment/
   ├── Phase4-Detail/
   ├── References/
   ├── VnV/
   ├── _Project_Brief.md
   └── Status.md
   ```

3. Generate `_Project_Brief.md` with frontmatter:
   ```yaml
   ---
   created: {{today}}
   updated: {{today}}
   type: project
   status: active
   tags: [#type/project, #status/active]
   tier: {{tier}}
   ---
   ```
   Content sections:
   - Project Identity (code, name, tier, description)
   - Customer & Market (segment, job-to-be-done, existing solutions)
   - Scope (primary function, top 3 targets, cost target)
   - Constraints (hard constraints, standards, local content)
   - Success Criteria (done definition, kill condition)
   - Timeline (deadline, key milestones)

4. Generate `Status.md` with:
   - Tier designation
   - Current Phase: Phase 0 (initialized)
   - Pahl-Beitz progress checklist (Phase 0-4, all unchecked)
   - Physical Validation section (dP/dt: 0, next milestone: TBD)
   - Blocking Constraints section (empty)
   - Deadline
   - For Tier 1: physical gate deadline (must be ≤30 days)
   - For Tier 2: note that physical gate needed before Phase 3 exit

5. Present created files to user for review.

RULES:
- ALWAYS ask before creating — never auto-create without confirmation
- Tier 1 projects MUST have a physical gate defined within 30 days
- Tier 2 projects follow full Pahl-Beitz (Phase 0-4)
- Tier 3 projects need clear "done" criteria — reject if vague
- Project code format: VN-XXX-XXX or BB-XX (defense product codes)
- Vietnamese for description fields if user prefers, English for code
- COD: This is Offload (AI creates structure, CEO provides content)
- After init, suggest next step: /gate0 (if Phase 0 artifacts exist) or /odi (if market analysis needed)
