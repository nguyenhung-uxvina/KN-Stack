# Fable-GPT — Design Spec

> Skill: `skills/ops/fable-gpt/SKILL.md` · gọi bằng `/fable-gpt <nhiệm vụ> [flags]`
> Ngày: 2026-07-17 · CEO đã duyệt kiến trúc (2 phần) trong session brainstorm.
> Kiến trúc: **Phương án A — single-file thin orchestrator** (không sub-block, không vendor script).

## 1. Mục đích

Đóng gói quy trình "Claude điều khiển — Codex thực hiện" thành một lệnh duy nhất:
Claude (Fable 5) giữ phán đoán (phân loại, review plan, verify kết quả); Codex (GPT-5.6)
giữ thực thi qua sub-agent `codex:codex-rescue` của plugin OpenAI chính thức.
Mọi dispatch Codex đi qua Agent tool (`subagent_type: "codex:codex-rescue"`) với
`--model`/`--effort` tường minh — KHÔNG gọi codex-companion trực tiếp, KHÔNG vendor
đường dẫn plugin (gãy khi plugin update version).

Nguồn phương pháp: bài phân tầng GPT-5.6 CEO cung cấp 2026-07-17
(Sol medium DeepSWE 61/$1.86 · Sol xhigh 71/$4.70 · Terra/Luna thực thi thuần)
+ memory `codex-orchestrator-workflow`. Cả 3 model + effort xhigh ĐÃ verify khả dụng
trên tài khoản ChatGPT của CEO (smoke-test 2026-07-17).

## 2. Bước 0 — Security Gate + Classify (Claude inline, không tốn Codex)

**Security Gate (chạy TRƯỚC classify, không có ngoại lệ):**
Codex = cloud OpenAI. Theo rule "No classified data in prompts" (CLAUDE.md global)
và pattern gate MẬT của `leo-assist`/`wx-krpano`:
- Nhiệm vụ chạm nội dung MẬT/HẠN-CHẾ (geometry sản phẩm quốc phòng, thông số vũ khí,
  dữ liệu khách BQP, supplier pricing) → **DỪNG, không dispatch Codex.**
- Đề xuất 2 lối ra: (a) abstract hóa — đổi tên/số liệu thành generic rồi chạy tiếp,
  (b) CEO tự làm local không qua Codex.
- Task code thuần KN-Stack / generic / open-source → PASS, đi tiếp.

**Classify — chọn đường đi.** 3 tiêu chí:
1. Phạm vi đã rõ chưa? (file/hàm cụ thể vs mô tả mơ hồ)
2. Số file dự kiến chạm (≤2 vs nhiều)
3. Rủi ro kiến trúc (đổi interface/schema/cross-domain?)

| Kết quả | Đường | Điều kiện |
|---|---|---|
| Task nhỏ, rõ, ≤2 file, không đụng kiến trúc | **FAST PATH** | mặc định cho ~80% việc |
| Task lớn / mơ hồ / đa file / kiến trúc | **FULL CYCLE** | classifier tự chọn |

Flags override: `--fast` ép fast path · `--full` ép full cycle. Classifier phải nêu
1 câu lý do phân loại trong output (traceability).

## 3. FAST PATH

```
/fable-gpt "task" → [Security Gate] → dispatch codex:codex-rescue
    --model gpt-5.6-sol   (effort mặc định medium — KHÔNG set --effort)
    prompt = task đã được Claude viết lại cụ thể (phạm vi, file, tiêu chí done)
→ nhảy thẳng đến Bước Verify (mục 4, bước 5)
```

## 4. FULL CYCLE — 5 bước

| # | Bước | Ai | Model/effort | Sản phẩm |
|---|---|---|---|---|
| 1 | **Plan** | Codex read-only | `gpt-5.6-sol` + `--effort xhigh` | Kế hoạch: các bước, file chạm, edge cases, tiêu chí done |
| 2 | **Review** | Claude inline | Fable 5 | Soi lỗ hổng, thách thức giả định, đối chiếu repo THẬT (đọc file, không tin plan mù); sửa/bổ sung plan |
| 3 | **CEO Gate** | CEO | — | Trình plan đã-review, chờ duyệt. `--auto` bỏ gate |
| 4 | **Execute** | Codex write | `gpt-5.6-terra` (default) | Thi công theo plan đã khóa; task giao từng phần cụ thể |
| 5 | **Verify** | Claude inline | Fable 5 | Đọc diff + chạy test/eval liên quan |

Chi tiết từng bước:
- **Plan (1):** dispatch read-only (yêu cầu rõ "planning only, do not edit files").
  Prompt chứa: nhiệm vụ, ngữ cảnh repo Claude đã nắm, yêu cầu output có cấu trúc
  (steps / files / edge cases / done criteria).
- **Review (2):** Claude PHẢI đọc các file plan nhắc đến trước khi duyệt. Nếu plan
  sai hướng nặng → trả Codex 1 lần kèm phản biện (`--resume` giữ thread); vẫn lệch
  → Claude tự viết plan (Fable), ghi rõ nguồn plan trong báo cáo.
- **CEO Gate (3):** mặc định DỪNG — trình bản plan cuối + điểm tôi đã sửa. `--auto`
  chạy thẳng (CEO chấp nhận rủi ro cho task đó).
- **Execute (4):** executor mặc định `gpt-5.6-terra`; flag `--executor luna|sol`
  để đổi. Prompt = plan đã khóa, nguyên văn + ranh giới phạm vi ("only touch files
  listed in plan").
- **Verify (5):**
  - Đọc TOÀN BỘ diff. Diff chạm file ngoài phạm vi plan → cờ đỏ, không chấp nhận im lặng.
  - Chạy test/eval liên quan (repo có gì chạy nấy: run-eval.sh, pytest, smoke).
  - FAIL → viết fix-hints cụ thể → dispatch lại qua `--resume` (giữ thread Codex).
    **Tối đa 2 vòng.** Sau 2 vòng vẫn FAIL → DỪNG, báo CEO: root-cause, diff hiện
    trạng, đề xuất (tự sửa tay / đổi hướng).
  - PASS → báo cáo hoàn thành: tóm tắt diff, kết quả test, số vòng đã dùng.

## 5. State & Resume

File `_fablegpt_state.md` tại repo đích (không phải scratchpad — session sau phải thấy):

```markdown
task: <nhiệm vụ gốc>
route: fast | full
plan: <plan đã duyệt hoặc "n/a">
step: classify | plan | review | ceo-gate | execute | verify | done
fix_rounds: 0-2
codex_thread: open | closed
flags: <flags gốc>
```

- `/fable-gpt --resume` → đọc state, nối lại đúng bước; dispatch tiếp dùng `--resume`
  của codex:rescue để giữ thread.
- Hoàn thành (báo cáo xong) → XÓA state file.
- State file là artifact tạm: skill KHÔNG BAO GIỜ commit nó; nếu repo đích có
  `.gitignore` thì kiểm tra `_fablegpt_state.md` đã được ignore chưa, chưa có thì
  nhắc CEO (không tự sửa .gitignore của repo đích).

## 6. Error handling

| Tình huống | Hành xử |
|---|---|
| Codex CLI chết / timeout | Báo ngay + gợi ý `/codex:status`, `/codex:setup`; KHÔNG retry mù |
| Verify FAIL 2 vòng | Dừng + báo cáo chẩn đoán (mục 4.5) |
| Plan sai hướng nặng | Trả Codex 1 lần → vẫn lệch → Claude tự viết plan |
| Diff ngoài phạm vi | Cờ đỏ trong Verify, liệt kê file lạ, chờ CEO |
| Security Gate chặn | Dừng + 2 lối ra (abstract / local) |

## 7. Frontmatter & Triggers

```yaml
name: fable-gpt
description: >-
  Fable-GPT orchestrator — Claude (Fable 5) điều khiển, Codex (GPT-5.6) thực hiện.
  Adaptive routing: task nhỏ → Sol medium fast path; task lớn → full cycle
  Plan(Sol xhigh) → Review(Fable) → CEO Gate → Execute(Terra) → Verify(Fable,
  tối đa 2 vòng fix). Security Gate MẬT trước mọi dispatch. Flags: --fast, --full,
  --auto, --executor <terra|luna|sol>, --resume. Triggers on: 'fable-gpt',
  'fable gpt', 'giao codex', 'delegate to codex', 'codex thực hiện',
  'chu trình plan review execute', 'giao việc cho gpt', 'codex execute this'.
```

## 8. Eval & Deployment

- **Eval:** `evals/fable-gpt.json`, `mode: "static"` (orchestrator không thể sinh
  full deliverable một shot). Checks audit SKILL.md có đủ: security gate MẬT,
  classifier 3 tiêu chí + lý do, model map đúng 3 tầng (sol-medium / sol-xhigh /
  terra), CEO gate mặc định + `--auto`, verify loop tối đa 2 vòng, state file
  + `--resume`, quy tắc diff-ngoài-phạm-vi, error handling Codex-chết.
- **Deployment:** junction sẵn có (skills/ → ~/.claude/commands/). Bump `VERSION`
  + `CHANGELOG.md` entry — thời điểm bump chờ CEO chốt (đang có VERSION bump khác
  pending).
- **Đếm skill:** 257 → 258 (verify bằng `bash setup.sh --status` trước khi cite).

## 9. Ngoài phạm vi (YAGNI — chốt trong brainstorm)

- KHÔNG parallel subagents (Mẹo 3 bài gốc) — thêm sau nếu cần.
- KHÔNG tự động /checkpoint sau 4 chu kỳ (Mẹo 4) — thói quen vận hành, không thuộc skill.
- KHÔNG cost tracking trong skill.
- KHÔNG sub-block skills, KHÔNG wrapper script.
