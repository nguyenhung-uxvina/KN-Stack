# NLM Mechanics & CREATE-Mode Reference

> Folded in from the former `skill-from-research` skill (merged into `research-to-skill`).
> Use this when you need the concrete NLM CLI commands, the CREATE-mode skill
> architecture, the no-NLM Quick Upgrade path, or the Galaxy→Skill bridge.
> The main pipeline, CEO gates, first-principles adaptation, and surgical-edit
> discipline live in `../SKILL.md`.

## Step 1 (CREATE): Skill Scope Definition (CEO — Core)

```markdown
## Skill Scope Definition
1. **Tên skill:** [name] — slug for folder name
2. **Mục đích:** [1-2 câu mô tả skill làm gì]
3. **Target user:** [CEO / engineer / researcher]
4. **Trigger keywords:** [từ khóa nào kích hoạt skill]
5. **Domain:** [engineering / defense / business / KM / other]
6. **Existing knowledge:** [notebook NLM liên quan? Galaxy notes?]
7. **Output mong muốn:** [skill tạo ra deliverable gì?]
8. **Freedom level:** [HIGH creative / MED follow pattern / LOW strict procedure]
```

## NLM CLI Commands (knowledge base)

```bash
# Use existing notebook
nlm alias list

# Create new notebook + alias
nlm notebook create "Skill Research: <skill-name>"
nlm alias set skill-<name> <uuid>

# Deep Research (auto-find sources)
nlm research start skill-<name> "<topic: concepts, best practices, failure modes>"
nlm research status skill-<name>
nlm research import skill-<name>

# Add curated sources (CEO selects — Core)
nlm source add skill-<name> --url "<url>"
nlm source add skill-<name> --text "<vault content>" --title "<note title>"
```

**Key insight:** include Galaxy permanent notes as sources — distilled, CEO-validated knowledge that should ground the skill.

### 6-Question extraction (NLM query form)
```bash
nlm notebook query skill-<name> "3-5 core principles an expert in <domain> must follow? Rules + rationale."   # Q1 KNOW
nlm notebook query skill-<name> "Step-by-step procedure for <task>? Decision points + branching."             # Q2 EXECUTE
nlm notebook query skill-<name> "Top 5 failure modes / mistakes for <task>? Detect + prevent each."           # Q3 AVOID
nlm notebook query skill-<name> "Decision rules / criteria for the right approach? IF-THEN-ELSE."             # Q4 WHEN
nlm notebook query skill-<name> "What makes output good vs bad? Specific quality criteria + examples."        # Q5 JUDGE
nlm notebook query skill-<name> "Edge cases / exceptions? When to modify the standard procedure?"             # Q6 EDGE
```

## CREATE-Mode Skill Architecture (map knowledge → SKILL.md)

```
YAML Frontmatter:  name ← Step 1 ; description ← Step 1 triggers
When to Use ← Step 1 (triggers + contexts)
Workflow Steps ← Q2 (procedures)
Decision Points ← Q4 (IF-THEN)
Quality Criteria ← Q5
Gotchas/Warnings ← Q3 (failure modes) + Q6 (edge cases)
Core Principles ← Q1 (embedded as rules, not explanations)
References ← NLM notebook alias for follow-up queries
COD Classification ← which steps Core vs Offload
```

Architecture rules: **< 500 lines** (else split into references/); imperative style ("Do X"); include only what Claude doesn't know (domain rules, not general knowledge); decision rules as code-like IF-THEN; link the NLM notebook for runtime queries.

## Validation (CREATE)

```
6a. 3 test prompts: happy path / edge case / out-of-scope (should NOT trigger)
6b. Ground-truth: nlm notebook query <same question> → compare skill output vs NLM
    (aligned? missed domain knowledge? hallucinated beyond sources?)
6c. Optional eval JSON in _meta/evals/<skill-name>.json:
```
```json
{ "skill": "<name>", "created": "YYYY-MM-DD",
  "tests": [ { "prompt": "<test>",
    "assertions": [ {"type":"contains","value":"<term>"},
                    {"type":"not_contains","value":"<term>"} ] } ] }
```

## Quick Upgrade (no NLM — small fixes)

```
1. CEO feedback: "skill X should also handle Y"
2. Read current SKILL.md
3. Surgical Edit to add Y
4. No NLM — CEO judgment is the source
5. Log in _meta/learnings.md
```
Quick = 1 new rule/gotcha, trigger update, minor procedure. Full = new domain knowledge, multiple gaps, standards change, structural rework.

## Upgrade Triggers

| Trigger | Detection | Action |
|---------|-----------|--------|
| CEO says "skill X thiếu Y" | Direct feedback | UPGRADE with CEO feedback as extraction prompt |
| New research found sources | During /research | UPGRADE → add sources + extract delta |
| Standards updated | Periodic check | UPGRADE → update standards table |
| Skill used 5+ times, recurring gap | Usage pattern | UPGRADE → fill gap |
| New Galaxy note in domain | Galaxy growth | UPGRADE → embed note as rule |
| Project post-mortem | Post-project | UPGRADE → add learned procedure |

## Galaxy → Skill Bridge

Galaxy permanent notes = distilled CEO judgment → can become skill rules:
```
Galaxy: "Recoil Fidelity Threshold — 70% Lực Đủ Cho Training Transfer"
→ Rule: "When evaluating recoil simulation, 70% force fidelity is the minimum for
   positive training transfer. Below 70% → may create negative transfer."
```
Scan Galaxy for domain-relevant notes → extract as rules → embed in SKILL.md.

## Integration Points

- Feeds from: `/research --deep`, `/nlm`, Galaxy
- Feeds into: `~/.claude/commands/` (deployed skills), `_meta/evals/`
- Companion to: `skill-creator` (Anthropic meta-skill — SKILL.md syntax)
- Position: after research, before deployment
