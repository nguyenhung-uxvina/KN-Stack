---
name: first-principles
description: Apply first principles thinking to any problem, design decision, or business challenge. 5-step stack strips assumptions layer by layer until bedrock truth remains, then rebuilds from fundamentals. Triggers on "first principles", "nguyên lý đầu tiên", "strip assumptions", "bóc giả định", "why do we do it this way", "tại sao làm như vậy", "rebuild from scratch", "xây lại từ đầu", "challenge assumption", "Musk test".
---

# First Principles — Bóc Giả Định, Xây Lại Từ Gốc

5-bước phân tích First Principles cho bất kỳ vấn đề nào. Mỗi bước bóc 1 lớp giả định cho đến khi chạm bedrock truth, rồi xây lại từ fundamentals.

## When to Use

- Bế tắc trong thiết kế — "tại sao mình phải làm theo cách này?"
- Đánh giá concept mới — lọc convention ra khỏi physics
- Phân tích đối thủ — tại sao họ làm vậy? Có phải vì đúng hay vì thói quen?
- Trước Pahl-Beitz Phase 2 (Conceptual Design) — đảm bảo không bị Solution Bias
- Business strategy — tìm cơ hội disruption trong defense market

## Workflow (5 Steps — chạy tuần tự)

### Step 1: STRIP — Bóc Giả Định

```
Prompt: "Break [topic/problem] down using first principles.
Identify every assumption people commonly make about this.
Then strip each assumption away and ask:
What is fundamentally, provably true here?
Rebuild from only what remains."
```

**Output:** Danh sách gồm:
- Assumptions (giả định đang được chấp nhận)
- Bedrock truths (sự thật không thể tranh cãi — physics, math, logic)
- Gap: điều mọi người *nghĩ* là đúng nhưng thực ra chỉ là convention

**WX Engineering rule:** Bedrock = physics + material properties + user needs. Convention = "industry always does it this way."

### Step 2: SIMPLIFY — Đơn Giản Hóa (Feynman Test)

```
Prompt: "Explain the same concept as if I'm a 12-year-old.
No jargon. No assumed knowledge.
If you can't explain it simply, there's still hidden complexity.
Keep going until it's genuinely simple."
```

**Output:** 1-3 câu mô tả bản chất vấn đề.

**Test:** Nếu không explain được trong 3 câu → chưa hiểu đủ sâu → quay lại Step 1.

**Ví dụ WX:**
- LOMAH phức tạp: "Sensor → amplifier → digital → miss/hit decision"
- First principles: "Viên đạn chạm tấm thép tạo rung. Rung = hit. Không rung = miss. Hết."

### Step 3: QUESTION — 5 Giả Định Nền Tảng

```
Prompt: "What are the 5 core assumptions this field/approach makes
that beginners just accept as true?
Which ones are actually proven?
Which are just convention?"
```

**Output:** Bảng:

| # | Assumption | Status | Evidence |
|---|-----------|--------|----------|
| 1 | ... | PROVEN / CONVENTION / UNKNOWN | ... |
| 2 | ... | ... | ... |

**WX Decision rule:**
- PROVEN → giữ nguyên, thiết kế theo
- CONVENTION → thử thách, tìm alternative
- UNKNOWN → research trước khi quyết định (dùng `/research`)

### Step 4: INVERT — Đảo Ngược Giả Định

```
Prompt: "If the 3 most important assumptions turned out to be wrong,
what happens? What breaks? What still works?
What would the solution look like WITHOUT these assumptions?"
```

**Output:**
- Consequences: cái gì vỡ nếu assumption sai?
- Survivors: cái gì vẫn đứng vững?
- New paths: hướng đi mới nếu bỏ assumption

**WX link:** Đây chính là cơ chế tìm ACH opportunities. "Giả sử hardware chính xác KHÔNG cần thiết → AI có thể compensate không?" = ACH thesis.

### Step 5: REBUILD — Xây Lại Từ Zero (Musk Test)

```
Prompt: "Starting from zero — no existing industry, no convention —
using only the fundamental truths from Step 1,
what would you build?
What would look completely different from today?"
```

**Output:** Concept design không bị ràng buộc bởi convention.

**WX Engineering rule:** Gap giữa "cách hiện tại" và "cách xây từ zero" = chính là cơ hội thiết kế. Gap càng lớn → opportunity càng lớn.

**Sau Step 5:** Route output vào Pahl-Beitz pipeline:
- IF concept mới khả thi → `/helix-concept-generate` (morphological matrix)
- IF business opportunity → `/forge-pre-study` (GO/PARK/KILL)
- IF insight atomic → `/galaxy-gate` (Galaxy note candidate)

## Application Templates

### Template A: Engineering Design Problem

```
Topic: [mô tả vấn đề thiết kế]
Context: [project nào, phase nào, constraint gì]

→ Run Step 1-5
→ Compare Step 5 output vs current design approach
→ IF different → challenge current approach with evidence
→ IF same → current approach is well-founded, proceed
```

### Template B: Business/Market Problem

```
Topic: [vấn đề kinh doanh]
Context: [product nào, customer nào, market nào]

→ Run Step 1-5
→ Step 5 output = potential disruption hypothesis
→ Route to /forge-pre-study if viable
```

### Template C: Learning New Domain

```
Topic: [lĩnh vực mới cần học]
Context: [tại sao cần học, áp dụng vào đâu]

→ Run Step 1-3 BEFORE studying
→ Study with Step 3 assumptions as guide
→ After studying → run Step 4-5 to test understanding
→ Route insights to Galaxy
```

## Integration Points

- Feeds into: `/paradigm` (deeper paradigm challenge nếu Step 4 phát hiện flawed assumption)
- Feeds into: `/helix-concept-generate` (Step 5 output → concept candidates)
- Feeds into: `/forge-pre-study` (Step 5 business output → opportunity screening)
- Feeds into: `/galaxy-gate` (bedrock truths → Galaxy permanent notes)
- Feeds into: `/constraint` (Step 1 bedrock truths → binding constraint identification)
- Related Galaxy: [[Phán đoán không thể uỷ thác cho AI]], [[Solution-Determining Subfunction]]

## Gotchas

1. **First principles ≠ ignoring expertise.** Stripping assumptions means testing them, not discarding proven engineering. IF Step 1 confirms assumption is PROVEN → respect it.
2. **Convention có lý do.** Nhiều convention tồn tại vì history of failures. Trước khi bỏ convention → hỏi "convention này tồn tại vì ai đã chết/mất tiền?"
3. **Step 5 là thought experiment, không phải action plan.** Rebuild from zero hiếm khi khả thi 100%. Giá trị nằm ở *gap analysis* giữa zero-build và current approach.
4. **Solo CEO trap:** First principles thinking tiêu tốn judgment. Dùng cho quyết định quan trọng (design concept, market entry), KHÔNG dùng cho routine tasks.

## COD Classification

| Task | COD | Notes |
|------|-----|-------|
| Step 1 (Strip) | Offload | AI breaks down, CEO validates |
| Step 2 (Simplify) | Offload | AI explains, CEO tests understanding |
| Step 3 (Question) | **Core** | CEO judges PROVEN vs CONVENTION |
| Step 4 (Invert) | Offload | AI explores consequences |
| Step 5 (Rebuild) | **Core** | CEO judges feasibility of new approach |
| Route output | **Core** | CEO decides next action |
