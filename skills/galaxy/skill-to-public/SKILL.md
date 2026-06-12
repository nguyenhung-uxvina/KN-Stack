---
name: skill-to-public
description: "Convert any KN-Stack skill, Galaxy note, design journal, or book chapter into outbound media — blog post, X thread, LinkedIn post, and/or short-video script — with mandatory defense-context IP audit before publish. Naval outbound leverage: turn specific knowledge into compounding reputation/recruitment/customer-education asset. Flags: --source <path>, --blog, --x, --linkedin, --video, --all (default), --lang vi|en, --audience technical|strategic|both, --dry-run. Triggers on: 'skill to public', 'xuat ban skill', 'biến skill thành nội dung', 'media leverage', 'blog from skill', 'X thread from', 'LinkedIn post from', 'publish skill', 'workshop x content'."
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob", "Agent"]
---

# skill-to-public — Outbound Media Leverage (Naval Principle)

> **Role:** Convert internal specific-knowledge assets into externally-publishable formats
> **Why this exists:** KN-Stack has 160 skills, 160+ Galaxy notes, 20+ project decisions — gần như không ai biết. Naval: *"Code và media là leverage không cần xin phép."* Workshop X đang im lặng trên thị trường defense AI Việt Nam. Một post/tuần × 52 tuần = 52 touchpoints với customers/recruits/partners — compounding asset, không phải lao động lặp lại.
> **Architecture:** Single mega-skill, 4 output formats, mandatory IP audit gate, register-on-publish for compounding tracking.
> **Defense gate:** Workshop X làm defense — IP/sensitivity audit là CORE, không skip.

## Pipeline Architecture

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                       skill-to-public (5-step pipeline)                       │
│                                                                                │
│  Flags: --source <path>  --blog  --x  --linkedin  --video  --all (default)   │
│         --lang vi|en  --audience technical|strategic|both                    │
│         --dry-run  --concept <name>                                           │
│                                                                                │
│  ┌─────┐   ┌─────┐   ┌─────┐   ┌─────┐   ┌─────┐                              │
│  │ S1  │──▶│ S2  │──▶│ S3  │──▶│ S4  │──▶│ S5  │                              │
│  │SCAN │   │IP-  │   │POSI-│   │GEN- │   │PUB- │                              │
│  │+CLAS│   │AUDIT│   │TION │   │ERATE│   │LISH │                              │
│  │SIFY │   │CORE │   │     │   │∥4×  │   │+REG │                              │
│  └──┬──┘   └──┬──┘   └──┬──┘   └──┬──┘   └──┬──┘                              │
│     │         │CORE     │CORE     │CEO      │CORE                             │
│     ▼         ▼         ▼         ▼         ▼                                 │
│  [detect   [SAFE/    [hook +   [4 formats [register +                        │
│   source    REVIEW/   audience  parallel]  cross-link]                       │
│   type]     SENSITIVE] thesis]                                                │
└───────────────────────────────────────────────────────────────────────────────┘

Legend: CORE = CEO non-delegable | ∥ = parallel format generation

Output: D:/Workshop_X/3_Resources/Marketing/Published/<YYYYMMDD>-<slug>/
Registry: D:/Workshop_X/3_Resources/Marketing/_published_registry.md
```

## How to Use

### Default (all 4 formats, Vietnamese, both audiences)
```
/skill-to-public --source skills/forge/forge-shift
```

### Single format
```
/skill-to-public --source 5_Galaxy/Operational-Envelope-Law.md --x
```

### English, technical audience only
```
/skill-to-public --source skills/helix/helix-task-clarify --lang en --audience technical --blog
```

### Concept-based (auto-locate source)
```
/skill-to-public --concept "ACH stack" --all
```

### Dry-run (positioning + IP audit only, no content generation)
```
/skill-to-public --source skills/forge/forge-job-map --dry-run
```

## Workflow

### Step 1: Source Scan + Classification

```
SOURCE DETECTION — {{source_path}}
□ Path exists?
□ Type:
   - Skill SKILL.md → load skill description + body
   - Galaxy note → load atomic concept + wikilinks
   - Design Journal entry → load decision + rationale
   - Book chapter → load chapter content
   - Other markdown → treat as raw content
□ Size: {{N}} lines, {{M}} words
□ Wikilinks/cross-refs: {{N}}
□ Frontmatter tags: [list]
```

If `--concept` given:
- Search `5_Galaxy/`, `skills/`, `1_Projects/.../Design_Journal.md`
- Present top 3 matches → CEO selects ONE source

### Step 2: IP / Sensitivity Audit (CORE — Non-Delegable)

**MANDATORY gate before any content generation.** Workshop X makes defense products — leakage = irreversible.

```
IP AUDIT — {{source_path}}
Date: {{today}}

DETECTED MENTIONS:
| Category | Items Found | Risk |
|----------|-------------|------|
| Product names | BB-01, V-SMASH, MTB-20, TDR, ... | HIGH if context reveals capability |
| Customer/contract refs | Cục KH-CN, BQP, HĐ-XXX | HIGH — always SENSITIVE |
| Pricing / cost data | VND figures, margins | HIGH — never publish |
| Vendor relationships | supplier names + terms | MED — anonymize |
| Performance specs | accuracy, range, exact tolerances | HIGH for defense products |
| Methodology / framework | Pahl-Beitz, HELIX, ACH, IPARAG | SAFE — competitive differentiator |
| Generic engineering principles | first-principles, DfX, FMEA | SAFE — public domain |
| War stories without identifiers | "a customer once needed X" | SAFE if anonymized |

CLASSIFICATION:
□ SAFE — methodology, principles, general lessons, sanitized stories
□ REVIEW — borderline, CEO must redact specific identifiers
□ SENSITIVE — contains product capability/customer/spec — DO NOT PUBLISH

CEO VERDICT:
(1) ✅ SAFE — proceed to S3
(2) 🔧 REVIEW — list required redactions, regenerate audit
(3) ❌ SENSITIVE — abort, suggest alternative source

═══════════════════════════════════════════════════
```

**No content generated until SAFE verdict.** Audit output saved as `IP-audit.md`.

### Step 3: Positioning (CORE — CEO approves)

The ONE insight worth sharing. Naval principle: specific knowledge > generic content.

```
POSITIONING — {{slug}}
Date: {{today}}

HOOK (1 sentence — the surprising claim or counter-intuitive truth):
{{e.g., "Most product reviews check if drawings are correct. We check if the workshop master says 'gia cong duoc'."}}

THE ONE INSIGHT (1 paragraph — the load-bearing idea):
{{the principle, pattern, or lesson — the thing only someone with Workshop X's specific knowledge would say}}

AUDIENCE:
  Primary: [defense procurement / VN engineers / AI researchers / CEO peers]
  Secondary: [...]
  Resonance: why this audience cares NOW

WHY IT MATTERS (1 paragraph):
{{the consequence — what changes if reader internalizes this}}

ASYMMETRY (Naval check):
  □ Is this specific knowledge? (only Workshop X could write this)
  □ Is this leverageable? (compounds when published vs spoken)
  □ Is this honest? (no hype, no exaggeration, claim defendable in 2 years)

CEO:
(1) ✅ Approve positioning → generate formats
(2) 🔄 Revise hook / insight
(3) ⏸️ Defer — source doesn't have clear positioning
```

### Step 4: Generate Formats (parallel where multi-format requested)

Each format generator reads positioning + source, generates draft to `<run_dir>/<format>.md`.

#### Format A: Blog Post (~1500-2500 words)

```
STRUCTURE — Blog Post (Naval/Workshop X voice)
1. Hook paragraph (≤80 words) — the surprising claim
2. Tension setup (200-300 words) — why conventional approach fails
3. The principle (300-500 words) — the load-bearing insight
4. Concrete example (400-600 words) — one specific case, anonymized if needed
5. Implications (300-500 words) — what changes
6. Closing principle (≤100 words) — one-line takeaway

VOICE:
- Factual, precise, declarative
- No marketing language ("revolutionary", "best-in-class", "world-leading")
- No buzzwords without operational meaning
- Active voice, present tense for principles
- Vietnamese technical terms in English: queue, dispatcher, throughput
- Defense terminology in Vietnamese: gia cong duoc, do dung, bun nuoc
- 1 concrete number per main claim where possible

DO NOT:
- Claim MIL-STD compliance without verification
- Name customers or contracts
- Quote pricing or margins
- Reference competitor products by name
- Promise capabilities (only describe what was done)
```

Save: `<run_dir>/blog.md`. Frontmatter includes audience + word count + estimated read time.

#### Format B: X Thread (10-15 tweets, 280 chars each)

```
STRUCTURE — X Thread

Tweet 1 (HOOK): 1 line, declarative, counter-intuitive
  Examples:
  - "Most CEOs delegate the wrong thing first."
  - "We don't ship until the workshop master says 4 words."

Tweets 2-3 (TENSION): 2-3 lines each, the contradiction or pain
  - What everyone assumes
  - What actually happens

Tweets 4-10 (BODY): one idea per tweet, max 3 lines
  - Concrete sequence or principle
  - One number/specific per tweet where possible
  - Use line breaks for scannability

Tweet 11-12 (PAYOFF): the principle distilled
  - What this means for the reader
  - 1-2 line max

Tweet 13 (CTA): soft — what to read/follow next
  - Link to blog if --blog also generated
  - "Reply with X if Y"

CONSTRAINTS:
- Each tweet ≤280 chars (count exactly)
- Thread reads coherently even if reader stops at any tweet
- Vietnamese threads OK but English reaches wider engineering audience
- No emoji walls
- No "🧵👇" — let content invite reading
```

Save: `<run_dir>/x-thread.md`. Each tweet numbered, char count shown.

#### Format C: LinkedIn Post (~1200-1800 chars, ~250-350 words)

```
STRUCTURE — LinkedIn (story-led, professional)

Line 1 (HOOK): 1 short line — surprising or specific
Line 2 (BLANK)
Para 1 (CONTEXT): 2-3 lines — the situation
Line break
Para 2 (THE MOMENT): 2-4 lines — what happened or what we discovered
Line break
Para 3 (THE LESSON): 2-4 lines — the principle
Line break
Closing: 1 line — the takeaway
Hashtags (3-5 max): #defense #engineering #vietnam #productdev #ai-hardware

VOICE:
- Professional but personal
- "We" or "I" voice — not detached
- One specific story or example
- No corporate platitudes
- No humble brag

LENGTH: 1200-1800 chars including spaces. LinkedIn truncates ~3 lines without "...see more" — front-load the hook.
```

Save: `<run_dir>/linkedin.md`.

#### Format D: Short Video Script (60-90s vertical)

```
STRUCTURE — Short Video Script (Reels/TikTok/Shorts)

[0-3s] HOOK (must stop scroll):
  Visual: [face on camera / object close-up / scene]
  Voice: 1 sentence — surprising claim or pattern interrupt

[3-15s] CONTEXT:
  Visual: [b-roll suggestion]
  Voice: 2-3 sentences setting up the tension

[15-50s] BODY:
  Visual: [3-4 cuts suggested with timing]
  Voice: the insight, broken into 3-4 beats

[50-75s] PAYOFF:
  Visual: [callback to hook image or transformation]
  Voice: 1-2 sentences distilling the principle

[75-90s] CTA:
  Visual: [text overlay]
  Voice: "Theo dõi Workshop X" / "Follow for more on Vietnamese defense engineering"

NOTES:
- Total word count: 150-220 words (≈ 90 seconds at 150 wpm Vietnamese)
- Vertical 9:16 aspect ratio
- No music suggestions (audio leverage = creator's call)
- Captions mandatory (60% watch muted)
- Defense visual safety: no product close-ups without IP audit second-pass
```

Save: `<run_dir>/video-script.md`. Include shot list + timing markers.

### Step 5: Publish Register + Cross-Link (Compounding Asset)

After CEO approves drafts:

```
REGISTER ENTRY — append to 3_Resources/Marketing/_published_registry.md

| Date | Slug | Source | Formats | Audience | Language | IP class | Status |
|------|------|--------|---------|----------|----------|----------|--------|
| YYYY-MM-DD | <slug> | <source path> | blog,x,linkedin,video | both | vi | SAFE | DRAFT/PUBLISHED |

CROSS-LINK SUGGESTIONS:
Read prior 5 entries in registry → propose 1-3 cross-references:
  - "If reader liked this → also see <prior post slug>"
  - Add to blog post bottom: "Related Workshop X writing: [list]"
  
This compounds: each new piece increases discoverability of all prior pieces.
```

Output `_publish_state.md`:
```
---
slug: <slug>
source: <path>
positioning_hash: <hash>
ip_class: SAFE
formats_generated: [blog, x, linkedin, video]
ceo_approved: {format: [yes/no/revise]}
published_url: {format: [url or DRAFT]}
created: <today>
---
```

CEO marks each format published URL after actually posting (manual or via separate publishing skill).

## Voice & Style Rules (Workshop X — Naval-influenced)

**The brand:**
- Workshop X = serious engineering, no fluff, Vietnamese defense AI specialist
- Tone: factual, precise, confident-without-arrogance
- Asymmetry: most defense companies don't publish at all — moderate-volume + signal-rich beats marketing splash

**Always:**
- One specific number per main claim where possible
- One concrete example per principle
- Active voice, present tense for principles
- Vietnamese for VN audience, English for international engineering audience
- Credit where due — name methodologies (Pahl-Beitz, ICDM, TRIZ) properly

**Never:**
- "Revolutionary", "world-class", "best-in-class", "industry-leading"
- "Synergy", "leverage" (as verb), "ecosystem" (without specifics)
- Promises about future capability — only what we did
- Customer names, contract numbers, exact specs, pricing
- Competitor names (criticism), even implicit
- Claims of MIL-STD compliance without verification footnote
- Hype around AI — describe operational utility, not magic

## Data Bus — Run Folder Contract

`D:/Workshop_X/3_Resources/Marketing/Published/<YYYYMMDD>-<slug>/`:

| File | Written By | Content |
|------|-----------|---------|
| `source.md` | S1 | Snapshot of source content (immutable reference) |
| `IP-audit.md` | S2 | Classification + redaction notes + CEO verdict |
| `positioning.md` | S3 | Hook + insight + audience + Naval asymmetry check |
| `blog.md` | S4 | Blog draft (if requested) |
| `x-thread.md` | S4 | X thread (if requested) |
| `linkedin.md` | S4 | LinkedIn post (if requested) |
| `video-script.md` | S4 | Video script + shot list (if requested) |
| `_publish_state.md` | S5 | Status tracking per format |

Registry file: `D:/Workshop_X/3_Resources/Marketing/_published_registry.md` (append-only ledger).

## Integration

```
skill-to-public READS FROM:
  - skills/**/SKILL.md → any skill content
  - 5_Galaxy/*.md → atomic Galaxy notes
  - 1_Projects/**/Design_Journal.md → decision logs
  - 3_Resources/Books/**/Phase4-Chapters/*.md → book chapters from codebase-to-book
  - 3_Resources/Marketing/_published_registry.md → prior publications (cross-link)

skill-to-public WRITES TO:
  - 3_Resources/Marketing/Published/<run_dir>/ → all run artifacts
  - 3_Resources/Marketing/_published_registry.md → append-only entry

skill-to-public COMPLEMENTS:
  - codebase-to-book → P9 CEO insights can feed skill-to-public for high-value chapters
  - galaxy-note → fresh permanent notes are good source candidates
  - helix-design-journal → notable decisions are storytelling gold
  - forge-evolve → Workshop X identity narrative tracking

skill-to-public CAN FEED (CEO-triggered):
  - Future: skill-to-public-publish — actual posting via API (not built; manual for now)
  - Future: skill-to-public-translate — VI ↔ EN auto-translation
  - Future: skill-to-public-thread-of-threads — chain multiple posts into series

skill-to-public DOES NOT (intentional):
  - Auto-publish to platforms (CEO maintains the publish button)
  - Generate engagement metrics or growth projections
  - Substitute for actual editorial judgment
```

## Rules

- **⛔ IP AUDIT IS NON-NEGOTIABLE** — Step 2 must produce SAFE verdict before any content generation. SENSITIVE = abort.
- **Source must exist and be readable** — Step 1 fails-fast, no guessing source content.
- **CEO approves positioning before generation** — Step 3 is CORE. Cannot infer "what's worth saying" automatically.
- **Each format independently reviewable** — CEO can approve blog, revise X thread, scrap video — granular control.
- **Defense-context redaction is irreversible-published-problem** — when in doubt, redact. When still in doubt, abort.
- **Registry is append-only** — never edit prior entries; rolling history of brand voice + reach.
- **NO auto-publish** — this skill drafts, CEO publishes manually (or via separate skill). Anti-pattern: AI publishing under CEO's identity without per-post approval.
- **Cross-link suggestions read prior 5 entries** — compounding discoverability without overwhelming the reader.
- **Workshop X voice rules apply universally** — even if user says "make it more exciting", DO NOT add marketing fluff. Refuse with rule citation.
- **Vietnamese is default** — Workshop X is Vietnamese-based. `--lang en` is for international reach, not default.
- **Specific knowledge > generic content** — if positioning Step 3 reveals the source is too generic (= anyone could write this), suggest the CEO pick a more specific source instead.

## COD Classification

- Source scan + classification: Offload (O1)
- IP audit pre-flag: Offload (O2) — AI flags, **CEO classifies (CORE)**
- Positioning draft: Offload (O2) — AI proposes hook+insight, **CEO approves (CORE)**
- Format generation: Offload (O1) — mechanical from positioning + source
- Cross-link suggestions: Offload (O2)
- Registry update: Offload (O1)
- **IP SAFE/REVIEW/SENSITIVE verdict: Core (C)** — non-delegable, defense liability
- **Positioning approval: Core (C)** — brand voice + audience fit judgment
- **Per-format final approval: Core (C)** — accountability for published claims
- **Actual publishing: Core (C)** — outside this skill, CEO retains the button

## Why This Skill Compounds (Naval Lens)

```
1 post     = +1 customer touchpoint
1 post/wk × 52 wk = 52 touchpoints (linear)
52 posts × 5 cross-links each = 260 internal pathways (compound)
Cross-links → search → recurring readers → DM → customer/recruit (compound)
2 years of writing = ~100 posts × ~5 cross-links = 500 paths
```

Workshop X currently has ≈0 outbound media. The first 12 posts cost the most. After post 20, each new post benefits from the prior 19 via cross-links and accumulated brand voice. **This is the Naval asymmetry: writing scales while you sleep, conversations don't.**

The skill is permission-less leverage. Run it, audit it, publish what's SAFE, register what's published. Compound.
