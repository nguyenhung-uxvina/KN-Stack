# Chapter Template

> Reference mẫu cho P4 (`book-write`) khi viết từng chương. Mỗi chương được viết bởi 1 Task subagent, đầu ra là 1 file `Ch<NN>_<slug>_Draft.md`.

## Structure (4 sections bắt buộc)

```markdown
# Chapter <NN>: <Title>

<Opening: 2-3 paragraphs — problem, why, connection, promise>

## <Body section 1 — the core concept>

<prose + diagram(s) + pseudocode block(s)>

## <Body section 2>

...

> **Deep Dive: <topic>**
> <optional inline callout — leaders can skip>

## <Body section N>

## Apply This

### 1. <Pattern 1>
...

### 5. <Pattern 5>
```

## Section 1: Opening (2-3 paragraphs)

Cấu trúc:

**Paragraph 1 — Problem:**
> What problem does this layer/subsystem solve? Why does it exist?
> What would break without it?

**Paragraph 2 — Connection:**
> Explicit backward reference to previous chapter.
> Bridge giữa "cái đã biết" (Ch N-1) và "cái sắp học" (Ch N).

**Paragraph 3 — Promise:**
> What will the reader understand by end of this chapter?
> 2-3 concrete outcomes, không mơ hồ.

### Example opening (chapter về dispatcher)

> The system has a queue of events waiting to be processed. But a queue by itself is inert — something must pull events out, decide what to do with them, and coordinate with the rest of the system. That's the dispatcher's job. Without it, events accumulate forever and nothing happens.
>
> Chapter 4 built the queue and the producer side. This chapter follows an event from the moment the dispatcher picks it up to the moment its side effects land in downstream systems.
>
> By the end, you'll understand how the dispatcher stays single-threaded without blocking the whole system, why it hands off work instead of executing it, and the specific trade-off that makes retries safe even when handlers are not idempotent.

## Section 2: Body

### Build logic
Mỗi section của body giải quyết MỘT vấn đề con trong chapter. Order theo narrative flow, không alphabetical.

Sau mỗi concept:
1. **Prose** — giải thích narrative (WHY + HOW at high level)
2. **Diagram** — nếu có kiến trúc, data flow, state machine
3. **Pseudocode** — nếu cần show pattern cụ thể (3-5 blocks/chapter max)
4. **Table** — nếu là reference material (config options, field listings)

### Cấu trúc mỗi body section

```markdown
## <Descriptive Header — no "Introduction to X">

<1-2 paragraph prose — establishes the idea>

```mermaid
<diagram>
```

<1 paragraph — what the diagram shows and why>

```python
# Pseudocode — illustrates <pattern name>
<5-15 lines>
```

<1 paragraph — why this pattern matters, trade-offs, variations>
```

## Section 3: Deep Dive (optional, 0-2 per chapter)

**Purpose:** Implementation detail cho engineers đọc sâu. Leaders có thể skip mà không mất narrative.

Format:

```markdown
> **Deep Dive: <specific topic>**
>
> <2-4 paragraphs + maybe 1 pseudocode block>
> <The "how does this actually work at the byte level" content>
> <Must be self-contained — readable without prior section context>
```

### Khi nào dùng Deep Dive:
- Algorithm specifics (how timeout is calculated, why 2^n jitter)
- Data layout details (byte order, packing, alignment)
- Edge case handling (what if Redis disconnects mid-transaction)
- Performance micro-optimization (why this allocation pattern matters at 100k rps)

### Khi KHÔNG dùng Deep Dive:
- Concept quan trọng cho narrative (đưa vào body)
- "Interesting but tangential" (cắt luôn, không thêm vào)
- Fix cho edge case không ai gặp (cắt)

## Section 4: Apply This (mandatory, exactly 5 patterns)

**Cấu trúc mỗi pattern:**

1. **Name** — 2-4 từ, catchy nhưng không marketing-y
2. **Problem it solves** — 1 câu, cụ thể
3. **How to adapt** — 1-2 câu, actionable nhưng generic đủ để transfer
4. **Pitfall** — 1 câu, specific failure mode

### Example Apply This

```markdown
## Apply This

### 1. Single-Writer Queue
**Problem it solves:** Multiple producers writing to the same queue lead to interleaving and lost updates under load.
**How to adapt:** Promote one thread (or process) to be the sole writer. All other producers send messages through a channel; the writer drains the channel and commits.
**Pitfall:** The channel becomes a secondary queue — size it with the same care as the primary, or you just moved the bottleneck.

### 2. Dispatcher as Router, Not Worker
**Problem it solves:** Dispatchers that do work themselves block on slow handlers and stall the whole system.
**How to adapt:** The dispatcher's only responsibility is to hand off events to handlers. Use thread pools, actor mailboxes, or goroutines for execution.
**Pitfall:** You still need backpressure — a router with no bound on its handoff queue just moves the crash from CPU to memory.

### 3. Retry on Claim, Not on Completion
**Problem it solves:** Handlers that crash mid-work leave events in an ambiguous state.
**How to adapt:** Mark an event "claimed" when picked up, only "completed" when the handler finishes cleanly. A visibility timeout re-claims unfinished events after N seconds.
**Pitfall:** Non-idempotent handlers will double-execute under retry. Either make handlers idempotent or track claim_id to deduplicate.

### 4. ...

### 5. ...
```

### Varying format giữa các chapter

Để Apply This không monotonous, **vary format** qua chapters:

**Variant A — Inline header** (chapter về foundations):
```markdown
### 1. <Name> — <1-line summary>
<prose paragraph combining all 3 dimensions>
```

**Variant B — Bold keywords** (chapter về patterns):
```markdown
### 1. <Name>
**Problem:** ...
**Apply:** ...
**Trap:** ...
```

**Variant C — Quote style** (chapter về rationale):
```markdown
### 1. <Name>
> <Problem in 1 sentence>

<Adaptation paragraph>

**Watch for:** <pitfall>
```

Target: 3 variants rotate qua 18 chapters. Mỗi chapter chọn 1 variant, ghi chú vào Phase3-Outline.md.

## Diagram Placement

**Quy tắc 2-4 diagrams/chapter:**
- 1 architectural overview (mandatory) — thường đầu chapter sau opening
- 1 data flow HOẶC state machine (tùy concept)
- 0-1 sequence diagram cho interaction
- 0-1 decision tree / timeline cho advanced detail

Xem `diagram-types.md` cho pattern cụ thể.

## Citations (nếu có `--deep`)

Nếu chapter được viết với `/research --deep` feed vào, thêm section cuối:

```markdown
## Sources

- [NLM Notebook: <topic>](https://notebooklm.google.com/notebook/<id>) — Tier S sources, consulted <date>
- [Cited paper 1] — <1-line what it contributed>
- [Cited paper 2] — ...
```

## Filename convention

`Ch<NN>_<slug>_Draft.md` (2-digit number, kebab-case slug)

Examples:
- `Ch01_runtime-startup_Draft.md`
- `Ch07_core-execution-loop_Draft.md`
- `Ch14_multi-agent-coordination_Draft.md`

P6 (revise) đổi thành `Ch<NN>_<slug>_v2.md`.

## Quality checklist (P4 subagent verify trước khi submit)

- [ ] Opening có 2-3 paragraphs + backward reference?
- [ ] Body có 3-5 sections, mỗi section có prose + (diagram or code or table)?
- [ ] 2-4 Mermaid diagrams total?
- [ ] 3-5 pseudocode blocks, mỗi 5-15 dòng, có "// Pseudocode" label?
- [ ] Không có verbatim source code?
- [ ] Apply This có exactly 5 patterns?
- [ ] Chapter length 300-800 lines?
- [ ] Không có filler sentence?
- [ ] Technical terms consistent với Phase2-Positioning.md glossary?
