Perform deep multi-framework analysis on any article, book chapter, podcast transcript, or intellectual content. Combines Systems Thinking (stock-flow, feedback loops, leverage points, archetypes, constraints) with Meta-Learning (Feynman clarification, chunking, mnemonics, rubrics, drills) AND First-Principles Debate with ARCHITECT expanded framework generation.

Triggers: "analyze this article", "deep analysis", "phan tich sau", "break down this content", "extract insights", "debate", "first principles", "expand framework", "ARCHITECT", or when user pastes substantial text requesting comprehensive analysis.

Usage: /analyze [content_or_file_path] OR paste content interactively.

---

## PROCESS: 5 PHASES

### PHASE 1: CONTENT INTAKE

1. If $ARGUMENTS is a file path, read the file.
   If $ARGUMENTS is text, use directly.
   If no arguments, ask user to paste or point to content.

2. Identify content type: article / book chapter / transcript / framework / technical paper / other

3. Determine analysis depth from user cues:
   - **FULL** (default): All 5 phases, all frameworks, 5000+ word output
   - **FOCUSED**: Phases 2-3 only (skip debate/ARCHITECT) — use if user says "quick analysis"
   - **DEBATE ONLY**: Phases 2 + 4 only — use if user says "debate this" or "first principles"

### PHASE 2: CONTENT EXTRACTION

Before applying frameworks, extract raw materials:

**2.1 Core Thesis**
- Author's single most important claim
- Problem being solved
- Paradigm shift proposed (if any)
- Stated vs. real goal

**2.2 System Variables**
- **Stocks** — What accumulates? (knowledge, debt, trust, capability, risk)
- **Flows** — What changes those stocks? (learning rates, decay rates, investment)
- **Delays** — Where are time lags between cause and effect?
- **Feedback dynamics** — What reinforces? What balances? What spirals?
- **Constraints** — What limits the system's throughput?

**2.3 Learning Content**
- Core concepts (chunk candidates — groups of 5-9 related ideas)
- Prerequisite chains (what must be understood before what)
- Common mistakes the author warns about
- Actionable principles vs. theoretical background

**2.4 What's Missing (feeds Phase 4)**
- What does the author assume but never state?
- What counter-arguments exist?
- What system archetypes are present but unnamed?
- What rate-of-change dynamics does the author treat as static?
- What dimensions does the author ignore entirely?

### PHASE 3: FRAMEWORK APPLICATION

#### 3A: Systems Thinking Analysis

**Stock-Flow Map:**
For each critical stock (target 4-7):
```
Stock: [Name]
Level: [High/Medium/Low] | Units: [specific] | Type: [Buffer/Constraint]

Inflows:
  1. [Name] — Rate: [Fast/Med/Slow] — Control: [what governs] — Delay: [duration]

Outflows:
  1. [Name] — Rate: [Fast/Med/Slow] — Control: [what governs] — Delay: [duration]

Pattern: [Growth/Depletion/Equilibrium/Oscillation]
```

**Feedback Loop Detection:**
Map causal links: `[A] +-> [B]` (same direction), `[A] --> [B]` (opposite direction)
Mark delays with `||`
Classify: R (Reinforcing) / B (Balancing)
For each loop: Name, Strength x Speed x State = Dominance
Target: 3-7 loops with dominance ranking table.

**System Archetype Detection:**
Match against: Shifting the Burden, Fixes That Fail, Escalation, Success to Successful, Eroding Goals, Tragedy of Commons, Limits to Growth, Growth and Underinvestment.
Provide: pattern, evidence, confidence, counter-strategy.

**Leverage Point Analysis (Meadows L1-L12):**
Scan for presence, prioritize high leverage:
- L1-L3 (Paradigm, Mindset, Goals) — always prioritize
- L4-L6 (Self-organization, Rules, Information) — high ROI
- L7-L9 (Loop gain, Loop strength, Delays) — structural
- L10-L12 (Physical structure, Buffers, Parameters) — last resort

For each (target 5-8):
```
L[X]: [Name] — Priority: [HIGH/MED/LOW]
Evidence: [Quote or observation]
Intervention: [Specific, actionable]
Expected Impact: [Cascade effects]
```

Design Phase 1-3 Intervention Cascade.

#### 3B: Meta-Learning Analysis

**Feynman Clarification:**
- 60-second explanation (no jargon)
- Everyday analogy (kitchen, sports, construction — visceral)
- 3 diagnostic questions at increasing depth

**Chunking Breakdown:**
- 4-8 learning chunks, each with 5-9 concepts
- Dependency hierarchy (optimal learning sequence, not presentation order)

**Mnemonic Creation:**
- 1-2 memorable acronyms for core framework
- Must be a meaningful word connected to the domain
- Include retrieval instructions

**Self-Assessment Rubric:**
```
| Dimension | 1 (Novice) | 3 (Competent) | 5 (Expert) |
```
- 6-10 dimensions, behavioral indicators, scoring bands

**Interleaving Schedule:**
- 4-16 week schedule mixing topics
- Morning/afternoon blocks, no consecutive same-topic blocks

**Targeted Drills:**
- 2-5 exercises, progressive difficulty (Week 1-2 / 3-4 / 5+)
- Each: purpose, duration, instructions, scoring

**Learning Journal Prompts:**
- 5-7 prompts tied to content's key dynamics
- At least one about feedback loops, one about meta-learning

#### 3C: Use Cases
4-6 audience-specific use cases with: situation, risk/opportunity, interventions, 90-day target.

### PHASE 4: FIRST-PRINCIPLES DEBATE + ARCHITECT FRAMEWORK

This phase is CORE, NOT optional. It elevates "comprehensive summary" to "original intellectual contribution."

#### 4A: First-Principles Debate (3-7 debate points)

For each major claim:

**Step 1: State Precisely** — strip rhetoric, what is actually asserted?

**Step 2: Decompose to Fundamentals** — what must be true for this claim to hold?
- Axiomatic (self-evident)
- Empirical (testable, currently supported)
- Conventional (widely believed, not proven from first principles)
- Speculative (projection without strong evidence)

**Step 3: Current vs. Fundamental Limitation Test**
```
CURRENT LIMITATION (will be overcome):
- Technology trajectory is clear
- Scaling/cost barriers that reduce over time
-> DON'T bet strategy on current limitations lasting

FUNDAMENTAL LIMITATION (physics-level):
- Requires what computation fundamentally cannot provide
- Violates information-theoretic limits
- Requires embodiment, consciousness, or skin-in-the-game
-> SAFE to build strategy on these lasting
```

**Step 4: Rate-of-Change Analysis**
- dH/dt (human capability change rate)
- dA/dt (agent/technology capability change rate)
- dR/dt (regulatory/institutional change rate)
- dM/dt (market/competitive change rate)
- Define survival/success condition in terms of these rates

**Step 5: Missing Dimensions Checklist**
```
[ ] Taste/Aesthetic Judgment
[ ] Skin in the Game
[ ] Compound Stack Effect
[ ] Trust Capital
[ ] Physical-World Interface
[ ] Organizational Power Dynamics
[ ] Information Asymmetry
[ ] Regulatory Dynamics
[ ] Co-Evolution
[ ] Second-Order Effects
[ ] Temporal Dynamics
[ ] Selection Bias
```

**Step 6: Generate Debate Points**
```
## Debate Point N: [Title]

**The claim:** [precise statement]

**First-principles counter-argument:**
[2-4 paragraphs with physics analogies, rate-of-change, or constraint theory]

**The corrected frame:**
[1-2 paragraphs — more accurate version]

**Systems Thinking integration:**
[Connection to stocks, flows, loops, or leverage points from Phase 3]
```

#### 4B: ARCHITECT Framework Generation

**Step 1: Irreducible Elements**
```
ORIGINAL MODEL: [author's items — typically 5-12 flat list]
FIRST-PRINCIPLES REDUCTION: [3-5 irreducible elements with hierarchy]
WHY REDUCTION MATTERS: [what the reduction reveals]
```

**Step 2: Layered Architecture**
```
+---------------------------------------------+
|     LAYER N: [Highest capability]           |
+---------------------------------------------+
|     LAYER N-1: [Supporting capability]      |
+---------------------------------------------+
|     LAYER 1: [Foundation]                   |
+---------------------------------------------+
         ^ Substrate: [META-CAPABILITY]

OUTPUT: [What the complete system produces]
```

**Step 3: Framework Mnemonic**
- Meaningful word, each letter = actionable principle
- Include retrieval instructions

**Step 4: Complete System Map**
Extended loop inventory (Phase 3 loops + debate-discovered loops):
```
| Loop | Name | Structure | Speed | Dominance | Status |
```

**Step 5: Extended Leverage Cascade**
- Phase 1 (Week 1-4): Quick Wins — L2 + L6
- Phase 2 (Week 5-12): Structural Lock-In — L5 + L7 + L8
- Phase 3 (Month 4-6): Systemic Transformation — L3 + L4 + L10

**Step 6: Extended Rubric**
```
| Dimension | 1 (Vulnerable) | 3 (Building) | 5 (Antifragile) |
```
Scoring bands: EXPOSED / TRANSITIONING / POSITIONED / ANTIFRAGILE

**Step 7: ARCHITECT Drills** (3-7, each linked to a loop or leverage point)

**Step 8: Extended Interleaving Schedule** (12-16 weeks)

**Step 9: Focus Session Design** (90-minute optimal block)

**Step 10: Learning Journal Template** (keyed to framework dimensions)

**Step 11: Distill Three Laws**
```
### Law 1: The [Name] Law
[One sentence + 2-3 sentences WHY this is a law]

### Law 2: The [Name] Law
### Law 3: The [Name] Law
```
Memorable, generative, irreducible. 80% of value from 3 principles.

### PHASE 5: SYNTHESIS AND OUTPUT

Generate the complete document following this structure:

```
# Multi-Framework Analysis: "[Content Title]"
## Systems Thinking + Meta-Learning + First-Principles Debate

**Source:** [details] | **Date:** [today] | **Frameworks:** [list]

---

## PART 1: CLARIFICATION
### 1.1 Core Thesis (Feynman)
### 1.2 Chunked Breakdown

## PART 2: SYSTEMS THINKING
### 2.1 Stock-Flow Map
### 2.2 Feedback Loops
### 2.3 System Archetypes
### 2.4 Leverage Points + Intervention Cascade

## PART 3: META-LEARNING
### 3.1 Learning Architecture
### 3.2 Diagnostic Questions
### 3.3 Mnemonic
### 3.4 Self-Assessment Rubric
### 3.5 Interleaving Schedule
### 3.6 Targeted Drills
### 3.7 Learning Journal

## PART 4: CONCEPT EVALUATION
### 4.1 Strengths
### 4.2 Weaknesses
### 4.3 Missing Dimensions

## PART 5: FIRST-PRINCIPLES DEBATE
### 5.1 Debate Points
### 5.2 Current vs. Fundamental Limitations
### 5.3 Rate-of-Change Analysis

## PART 6: ARCHITECT EXPANDED FRAMEWORK
### 6.1 First-Principles Reduction
### 6.2 Framework Mnemonic: [WORD]
### 6.3 Complete System Map
### 6.4 Extended Loop Inventory
### 6.5 Archetypes + Counter-Strategies
### 6.6 Leverage Cascade (3 phases)
### 6.7 Extended Rubric
### 6.8 ARCHITECT Drills
### 6.9 Interleaving Schedule (12-16 weeks)
### 6.10 Focus Session Design
### 6.11 Learning Journal Template

## PART 7: USE CASES
### 7.1 Audience Map
### 7.2 Implementation Roadmap

## PART 8: SYNTHESIS
### 8.1 Single Most Important Insight
### 8.2 System Archetype Warning
### 8.3 Counter-Intuitive Insights (3-5)
### 8.4 The Three Laws

## PART 9: PROGRESS TRACKING
### 9.1 Competency Grid
### 9.2 Weekly Review Questions
```

---

## QUALITY CHECKLIST (verify before finalizing)

**Systems Thinking:**
- [ ] >=4 stocks with full inflow/outflow/delay
- [ ] >=3 feedback loops classified R/B with dominance ranking
- [ ] >=1 archetype identified with evidence
- [ ] >=5 leverage points across multiple levels
- [ ] Phase 1-3 intervention cascade designed
- [ ] >=3 counter-intuitive insights

**Meta-Learning:**
- [ ] Feynman explanation genuinely simple
- [ ] Chunking follows dependency, not presentation order
- [ ] Mnemonic is memorable meaningful word
- [ ] Rubric has behavioral indicators
- [ ] Drills are specific and progressive

**First-Principles Debate:**
- [ ] >=3 debate points with formal structure
- [ ] Current vs. Fundamental distinction on >=2 claims
- [ ] Rate-of-change analysis with >=2 rates identified
- [ ] >=3 missing dimensions from checklist
- [ ] Each debate point integrates with systems thinking
- [ ] Corrected frame is genuinely more useful than original

**ARCHITECT Framework:**
- [ ] Irreducible reduction applied (collapses flat list to layers)
- [ ] Layered architecture diagram (ASCII)
- [ ] Meaningful mnemonic word
- [ ] Extended loop inventory includes debate-discovered loops
- [ ] Extended rubric covers all dimensions
- [ ] >=3 drills linked to loops/leverage points
- [ ] Three Laws are memorable, generative, non-redundant

**Output:**
- [ ] All 9 Parts present
- [ ] >=5000 words (full analysis requires depth)
- [ ] Tables for comparisons, ASCII for diagrams
- [ ] Synthesis adds NEW insight beyond individual frameworks

---

## EXECUTION RULES

1. The First-Principles Debate is NOT optional. Every content worth analyzing has debatable claims.
2. The ARCHITECT framework must ADD new value — if it just restates the original in different format, it has failed. Include >=2 dimensions the author ignores.
3. Three Laws are the crown jewel — pithy enough to remember, deep enough to generate the full framework.
4. Physics analogies are powerful (thermodynamics, mechanics, information theory, evolution).
5. Rate-of-change is the secret weapon — most authors describe snapshots, analyzing rates reveals hidden dynamics.
6. Save output as .md file to `3_Resources/Books & Articles/` or project folder as appropriate. Ask user for preferred location.
7. COD: Offload (AI generates analysis), but Galaxy note creation from insights is Core (CEO writes).
8. After analysis, suggest /signal to extract actionable signals for routing into projects/Galaxy.
9. Cross-reference previous analyses for recurring patterns (Shifting the Burden appears in ~85% of analyses).

---

## ARCHITECT HISTORY (meta-pattern tracking)

| Content | Original | Reduced | Mnemonic | Archetype | Key Law |
|---------|----------|---------|----------|-----------|---------|
| Naval — Wealth | 4 flat | 3 layers | SLAW-J | Shifting Burden | Compound: assets earn while you sleep |
| Profit First | GAAP | 2 behavioral | PLATES | Fixes That Fail | Small Plates: work with psychology |
| Self-Managing Co | 4 freedoms | Nested system | TRMP | Shifting Burden | Free Me First: free self before team |
| BASB/CODE | 4-step | 2 stocks + 1 goal | CODE | Shifting Burden | Project Primacy: knowledge without projects = hoarding |
| Mental Models | Collection | 3 functions | EPIC FIB-C | Success to Successful | Pointer Not Poster: models are compression |
| 5 AI Skills | 9 flat | 3 layers | OPERA | Shifting Burden | Rate Law: dH/dt > dA/dt |
| AI Skills Expanded | +debate | 3 + 7 missing | ARCHITECT | Shifting+CoEvol | Judgment Law: skin in game changes decisions |

**Meta-pattern:** First-principles reduction consistently collapses flat lists into 3+/-1 layered hierarchies. "Shifting the Burden" dominates (~85%). Three Laws center on: paradigm shift (L2), rate/compound dynamic, counter-intuitive structural insight.

When generating new ARCHITECT frameworks, update this table.
