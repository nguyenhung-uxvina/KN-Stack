---
name: btc-wire
description: "Block R7 of book-to-codebase: wire library infrastructure — setup.sh, CLAUDE.md, ARCHITECTURE.md, ICD stubs, hooks. Outputs library/setup.sh + support files."
---

# BTC-Wire — Block R7

> **Pipeline:** book-to-codebase Block R7
> **Purpose:** Generate all infrastructure files that turn a folder of SKILL.md files into a deployable skill library.
> **Standalone:** `/btc-wire <book_output_dir>`

## Prerequisites
- R3-Charter.md (placement, deployment_path, library_name)
- R4-Architecture.md (domain map, skill list)
- R6-Skill-Registry.md (all generated skills + paths)

## Steps

### 1. Generate `library/setup.sh`

Four modes (mirrors KN-Stack setup.sh pattern):

```bash
# Usage: bash setup.sh [--install <vault_path>] [--update <vault_path>] [--verify] [--unlink]

--install:  Create junctions from ~/.claude/commands/ → library/skills/**/<skill>/
            For Type C standalone: create junction from target vault's commands/ to skill dirs
--update:   Re-sync changed skill files; does NOT remove junctions
--verify:   Check all junctions resolve; report broken ones
--unlink:   Remove all junctions (restore from backup first)
```

Populate with actual skill paths from R6-Skill-Registry.md.

### 2. Generate `library/CLAUDE.md`

Developer guide — mirrors KN-Stack CLAUDE.md pattern:
- Library name, version, purpose
- Structure section (domains + skill count)
- Adding/editing skills instructions
- Deployment section (setup.sh commands)
- Git conventions (domain-prefixed branches + commits)
- Naming conventions (domain prefix, kebab-case)

### 3. Generate `library/ARCHITECTURE.md`

Domain map + DAG + placement rationale:
- Placement decision (from R3-Charter.md) with rationale
- Domain map: one section per domain, skill list, concept_kind distribution
- DAG: Mermaid diagram of dependency edges (from R4-Architecture.md)
- Integration with KN-Stack or Workshop X (for Type A/B/C)

### 4. Generate ICD Stubs (if applicable)

For skills with cross-library integration edges (Type A: integrates with existing HELIX/FORGE pipeline):
- Create `library/ICD/{{skill}}_to_{{kn-stack-skill}}_ICD.md`
- Stub format: interface name, data flow direction, contract (what gets passed, what gets returned)

### 5. Generate Hooks (if discipline_contract skills present)

For each `discipline_contract` skill with a defined cadence:
- Create stub hook entry in `library/hooks/`
- Hook format matches KN-Stack hook pattern (UserPromptSubmit, Stop, SessionStart)

### 6. CEO Presentation

```
═══ R7 COMPLETE: BTC-Wire ═══
Infrastructure generated:
  ✓ setup.sh ({{N}} skill junctions)
  ✓ CLAUDE.md
  ✓ ARCHITECTURE.md ({{N}} domains + DAG)
  {{✓ ICD stubs: {{N}} | (none — no cross-library edges)}}
  {{✓ Hook stubs: {{N}} | (none — no discipline_contract skills with cadence)}}

Deploy when ready:
  bash {{btc_output_dir}}/library/setup.sh --install <vault_path>

CEO:
(1) ✅ Approve → R8 (btc-validate)
(2) ✏️ Adjust setup.sh target path
(3) ⏸️ Pause
```

## Output
- `library/setup.sh`
- `library/CLAUDE.md`
- `library/ARCHITECTURE.md`
- `library/ICD/` (if applicable)
- `library/hooks/` (if applicable)
- `R7-Infrastructure-Bundle.md` (manifest of all files created)
