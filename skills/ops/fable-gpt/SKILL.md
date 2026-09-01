---
name: fable-gpt
description: "Fable-GPT orchestrator — Claude (Fable 5) điều khiển, Codex (GPT-5.6) thực hiện. Adaptive routing: task nhỏ/rõ → FAST PATH gpt-5.6-sol medium; task lớn/mơ hồ/kiến trúc → FULL CYCLE Plan(sol xhigh, read-only) → Review(Fable đọc repo thật) → CEO Gate → Execute(gpt-5.6-terra) → Verify(Fable, tối đa 2 vòng fix qua --resume). Security Gate MẬT chạy trước mọi dispatch. Flags: --fast, --full, --auto, --executor <terra|luna|sol>, --resume. Triggers on: 'fable-gpt', 'fable gpt', 'giao codex', 'delegate to codex', 'codex thực hiện', 'chu trình plan review execute', 'giao việc cho gpt', 'codex execute this', 'điều phối codex'."
---

# fable-gpt — Claude điều khiển · Codex thực hiện

> **Role:** thin commander. Claude (Fable 5) giữ phán đoán — phân loại, review plan,
> verify kết quả. Codex (GPT-5.6) giữ thực thi. Mọi dispatch đi qua Agent tool
> `subagent_type: "codex:codex-rescue"` (plugin OpenAI chính thức) — KHÔNG gọi
> codex-companion trực tiếp, KHÔNG vendor đường dẫn plugin (gãy khi plugin update).
> **Nguyên tắc bất di bất dịch:** không bao giờ chấp nhận kết quả Codex mà chưa tự verify.

## Model tiers (đã verify khả dụng 2026-07-17)

| Tầng | Model + effort | Vai trò |
|---|---|---|
| Xe hàng ngày | `gpt-5.6-sol` (effort mặc định medium — KHÔNG set `--effort`) | FAST PATH, ~80% việc |
| Lý luận nặng | `gpt-5.6-sol` + `--effort xhigh` | bước Plan của FULL CYCLE |
| Thực thi thuần | `gpt-5.6-terra` (mặc định) / `gpt-5.6-luna` | bước Execute |
| Phán đoán | Fable 5 (Claude, inline — không dispatch) | Classify, Review, Verify |

## Usage

```
/fable-gpt <nhiệm vụ>                       # adaptive routing
/fable-gpt <nhiệm vụ> --fast                # ép FAST PATH
/fable-gpt <nhiệm vụ> --full                # ép FULL CYCLE
/fable-gpt <nhiệm vụ> --full --auto         # full cycle, bỏ CEO Gate
/fable-gpt <nhiệm vụ> --executor luna       # đổi executor (terra|luna|sol)
/fable-gpt --resume                         # nối lại từ _fablegpt_state.md
```

## Step 0 — Security Gate (chạy TRƯỚC mọi dispatch, không ngoại lệ)

Codex = cloud OpenAI. Theo rule "No classified data in prompts" + pattern gate MẬT
của leo-assist/wx-krpano:

- Nhiệm vụ chạm nội dung MẬT/HẠN-CHẾ (geometry sản phẩm quốc phòng, thông số vũ khí,
  dữ liệu khách BQP, supplier pricing) → **DỪNG, không dispatch Codex.** Trình CEO
  2 lối ra: (a) abstract hóa — đổi tên/số liệu thành generic rồi chạy tiếp;
  (b) CEO tự làm local, không qua Codex.
- Task code thuần KN-Stack / generic / open-source → PASS.
- Gate áp cho **MỌI payload dispatch** (task text, ngữ cảnh repo, plan, fix-hints) VÀ **repo đích** — Codex CLI đọc repo trực tiếp, nên repo chứa nội dung MẬT thì DỪNG bất kể task text nghe generic.

## Step 0.5 — Classify (Claude inline, không tốn Codex)

Đánh giá theo **3 tiêu chí**: (1) phạm vi rõ chưa — file/hàm cụ thể vs mô tả mơ hồ;
(2) số file dự kiến chạm — ≤2 vs nhiều; (3) rủi ro kiến trúc — đổi interface/schema/
cross-domain. PHẢI nêu 1 câu lý do phân loại trong output (traceability).

| Kết quả | Đường đi |
|---|---|
| Nhỏ + rõ + ≤2 file + không kiến trúc | **FAST PATH** |
| Lớn / mơ hồ / đa file / kiến trúc | **FULL CYCLE** |

Override: `--fast` / `--full` thắng classifier.

## FAST PATH

1. Claude viết lại nhiệm vụ thành prompt cụ thể: phạm vi, file, tiêu chí done.
2. Dispatch Agent tool `subagent_type: "codex:codex-rescue"`, prompt bắt đầu bằng
   `--model gpt-5.6-sol` (KHÔNG set `--effort` — giữ medium mặc định) + task text.
3. Nhảy thẳng đến **Verify** (bước 5 của FULL CYCLE, cùng quy tắc 2 vòng).

Lưu ý: `--executor` chỉ áp cho bước Execute của FULL CYCLE — FAST PATH luôn dùng `gpt-5.6-sol` (flag bị bỏ qua).

Prompt giao Codex (mọi đường) chỉ yêu cầu EDIT — **KHÔNG yêu cầu executor tự chạy test/eval của repo** (env Codex ≠ git-bash, dễ kẹt hàng chục phút); mọi validation thuộc bước Verify của Claude.

## FULL CYCLE — 5 bước

| # | Bước | Ai | Model/effort |
|---|---|---|---|
| 1 | Plan | Codex read-only | `gpt-5.6-sol` + `--effort xhigh` |
| 2 | Review | Claude inline (Fable 5) | — |
| 3 | CEO Gate | CEO | — |
| 4 | Execute | Codex write | `gpt-5.6-terra` mặc định |
| 5 | Verify | Claude inline (Fable 5) | — |

### 1. Plan — sol xhigh, read-only
Dispatch `codex:codex-rescue` với prompt: `--model gpt-5.6-sol --effort xhigh` +
"PLANNING ONLY — do not edit any files, read-only analysis" + nhiệm vụ + ngữ cảnh
repo Claude đã nắm + yêu cầu output cấu trúc: steps / files chạm / edge cases /
done criteria.

### 2. Review — Fable đọc repo thật
Claude PHẢI đọc các file mà plan nhắc đến trước khi duyệt — không tin plan mù.
Soi: lỗ hổng, giả định sai, edge case thiếu, phạm vi phình. Sửa/bổ sung plan.
Plan sai hướng NẶNG → trả Codex đúng 1 lần kèm phản biện (dispatch `--resume` giữ
thread); vẫn lệch → Claude tự viết plan (Fable), ghi rõ nguồn plan trong báo cáo.

### 3. CEO Gate — mặc định DỪNG
Trình plan đã-review + các điểm Claude đã sửa. Chờ CEO duyệt rồi mới Execute.
`--auto` bỏ gate — chạy thẳng (CEO chấp nhận rủi ro cho task đó).

### 4. Execute — terra mặc định
Dispatch `codex:codex-rescue` với prompt: `--model gpt-5.6-terra` (hoặc model theo
`--executor luna|sol`) + plan đã khóa NGUYÊN VĂN + ranh giới cứng: "only touch
files listed in the plan". Task giao từng phần cụ thể, không giao cả cụm mơ hồ.
Không yêu cầu Codex tự chạy test/eval repo — validation thuộc bước 5.

### 5. Verify — Fable, tối đa 2 vòng
- Đọc TOÀN BỘ diff (`git diff` / `git status`).
- Diff chạm file **ngoài phạm vi** plan đã duyệt → **cờ đỏ**: liệt kê file lạ,
  không chấp nhận im lặng, chờ CEO.
- Chạy test/eval liên quan — repo có gì chạy nấy (run-eval.sh, pytest, smoke).
- FAIL → viết fix-hints cụ thể → dispatch lại qua `--resume` (giữ thread Codex).
  **TỐI ĐA 2 vòng fix.** Sau 2 vòng vẫn FAIL → DỪNG, báo CEO: root-cause, diff
  hiện trạng, đề xuất (tự sửa tay / đổi hướng).
- PASS → báo cáo: tóm tắt diff, kết quả test, số vòng đã dùng, đường đã đi
  (fast/full + lý do phân loại).

## State & Resume

File `_fablegpt_state.md` tại thư mục gốc repo đích (KHÔNG phải scratchpad):

```markdown
task: <nhiệm vụ gốc>
route: fast | full
plan: <plan đã duyệt hoặc "n/a">
step: classify | plan | review | ceo-gate | execute | verify | done
fix_rounds: 0-2
codex_thread: open | closed
flags: <flags gốc>
```

- `/fable-gpt --resume` → đọc state, nối đúng bước; dispatch tiếp dùng `--resume`
  của codex:rescue để giữ thread.
- Xong việc (báo cáo hoàn thành) → XÓA state file.
- State file là artifact tạm — skill **KHÔNG BAO GIỜ commit** nó. Repo đích có
  `.gitignore` → kiểm tra `_fablegpt_state.md` đã ignore chưa, chưa có thì nhắc
  CEO (không tự sửa .gitignore của repo đích).

## Error handling

| Tình huống | Hành xử |
|---|---|
| Codex CLI chết / timeout | Báo ngay + gợi ý `/codex:status`, `/codex:setup`; **KHÔNG retry mù** |
| Verify FAIL 2 vòng | Dừng + báo cáo root-cause, diff, đề xuất |
| Plan sai hướng nặng | Trả Codex 1 lần → vẫn lệch → Claude tự viết plan |
| Diff ngoài phạm vi | Cờ đỏ trong Verify, liệt kê file lạ, chờ CEO |
| Security Gate chặn | Dừng + 2 lối ra (abstract / local) |
| `--resume` mà `_fablegpt_state.md` thiếu/hỏng | Báo CEO, đề nghị chạy lại từ đầu — **KHÔNG đoán bước** |

## Ngoài phạm vi (YAGNI)

Không parallel subagents · không tự động /checkpoint theo chu kỳ · không cost
tracking · không sub-block skills · không wrapper script.
