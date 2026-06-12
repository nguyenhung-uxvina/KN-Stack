# INTAKE Protocol — Smart Router Logic

Used by `mentor-board` when CEO calls `/mentor-board "<problem>"` (no mode flag).

## Clarifying Questions (Step I2)

Present this prompt to CEO. Minimum required: questions 1, 3, 6.

```
Câu hỏi làm rõ vấn đề (CEO trả lời, AI sẽ route mentor + mode):

1. **Underlying decision** [REQUIRED]
   Bề mặt vấn đề là "<as stated>". Quyết định THẬT SỰ bên dưới là gì?
   (Thường: problem stated = symptom; real decision = below)

2. **Deadline / urgency** [optional]
   Quyết định khi nào? Deadline cứng có không?
   Options: immediate (today) / this week / this quarter / strategic long-term

3. **Options đang cân nhắc** [REQUIRED]
   CEO đã có options A/B/C concrete chưa?
   - Có ≥2 options → DECIDE mode candidate
   - Chưa có options → PANEL hoặc DEBATE
   - 1 hướng duy nhất → CONSULT để stress-test

4. **Sacred constraints** [optional, but valuable]
   Điều gì PHẢI giữ không thay đổi?
   - Defense IP (không leak)
   - MIL-STD compliance
   - Customer commitments đang ship
   - Team capacity (CEO + 3 expert)
   - Cash runway / cost cap
   - Vietnam regulatory

5. **Worst outcome** [optional, surfaces hidden priority]
   CEO sợ điều gì NHẤT xảy ra?
   (Reveals true priority — often differs from stated optimization target)

6. **Domain hint** [REQUIRED for routing]
   Vấn đề thuộc domain nào?
   - capital (allocation, funding, valuation)
   - scaling (production, team, market)
   - manufacturing (process, vertical integration)
   - ai-strategy (compute, model, chips)
   - people (hiring, culture, team building)
   - founder-wisdom (judgment, mental models, life decisions)
   - other: [specify]

[CEO answers — at minimum: 1, 3, 6]
```

## Mentor Proposal Logic (Step I3)

Read `D:/Workshop_X/3_Resources/Mentor-Board/_registry.md` for available mentors + reliability stats.

Match domain hint → mentor specialty (from each `<leader>/profile.md`):

| Domain | ★★★ Strong fit | ★★ Moderate | ★ Weak / not-recommended |
|---|---|---|---|
| capital | Munger, Marks, Dalio | Buffett (if added), Naval | Musk, Huang, Grove |
| scaling | Musk, Huang, Grove | Bezos (if added) | Munger, Marks |
| manufacturing | Musk, Grove | Toyota Way (if added) | Marks, Naval |
| ai-strategy | Huang, Musk, Naval | Hassabis (if added) | Munger, Marks |
| people | Grove, Dalio, Munger | Hsieh (if added) | Marks, Huang |
| founder-wisdom | Naval, Grove, Munger | Thiel (if added) | Marks (specific to investing) |
| other | All evaluated | — | — |

**Reliability weighting:** if mentor has reliability_log data for the domain, weight ★ rating:
- ≥70% reliability → ★★★ (or maintain rating)
- 40-69% → keep at ★★
- <40% with N≥5 → downgrade to ★ with note "low past accuracy in this class"

**Missing from board:** if CEO's problem maps to a domain where no current mentor is ★★★, suggest ADD:

```
MISSING FROM BOARD (would be ★★★):
- <Suggested Leader X> — <why ideal>
  Primary works: <list 2-3 T1 sources>
  Estimated setup: ~2h via /mentor-board --add <slug>
  → Recommend ADD before this consult? Or proceed with current subset?
```

## Mode Proposal Logic (Step I4)

Decision tree:

```
IF answers[options_state] == "CEO đã có A/B/C concrete":
  → DECIDE mode (need options scoring)

ELIF answers[domain] is ambiguous OR spans 2+ domains:
  IF expected_tension (multiple frameworks likely disagree):
    → DEBATE mode (3-round argument surfaces assumptions)
  ELSE:
    → PANEL mode (broad exploration)

ELIF answers[options_state] == "1 hướng duy nhất, muốn stress-test":
  → CONSULT mode (1 mentor) — pick strongest contrarian to default
     (e.g., if CEO leans optimistic → propose Munger to counter)

ELIF answers[domain] is single + clear:
  IF problem complexity == low + 1 framework sufficient:
    → CONSULT mode (1 mentor)
  ELSE:
    → PANEL mode (multiple perspectives)

DEFAULT:
  → PANEL with relevant preset
```

## Mode Heuristics — Tension Detection

When choosing between DEBATE vs PANEL:

**Pick DEBATE if any of these signals:**
- Problem involves capital + scaling (Marks risk-aware vs Musk growth-aggressive)
- Problem involves manufacturing + finance (Grove process vs Marks capital efficiency)
- Problem involves AI strategy + safety/ethics (multiple frameworks compete)
- CEO explicitly says "tôi không chắc" / "mâu thuẫn" / "tranh cãi"
- Past consults show mentors disagreed on similar class

**Pick PANEL if:**
- Brainstorming / exploration
- CEO wants diversity of views without forcing convergence
- Mentors mostly aligned on this domain
- Time-constrained (PANEL faster than DEBATE)

## Output of INTAKE — `intake_context` Frontmatter

Save CEO answers + AI proposals to consult file frontmatter:

```yaml
---
consult_id: <YYYYMMDD-HHMM-slug>
mode: <CONSULT|PANEL|DEBATE|DECIDE>
mentors: [<list>]
problem: "<original problem statement>"
intake_context:
  underlying_decision: "<from Q1>"
  urgency: "<from Q2 or 'unspecified'>"
  options_state: "<from Q3>"
  sacred_constraints: [<from Q4>]
  worst_outcome: "<from Q5 or unspecified>"
  domain: "<from Q6>"
ceo_adjustments: [<any I5 modifications>]
---
```

This frontmatter:
- Provides D-Diagnose context to mentors during consultation
- Enables `--retro` to reference original framing
- Feeds SUGGEST mode pattern analysis
