# book-to-learn — Design Spec

- **Ngày:** 2026-09-17
- **Trạng thái:** chờ CEO duyệt bản viết
- **Nhánh:** `feature/book-to-learn` (worktree `D:\KN-Stack-btl`)
- **Kế thừa:** `book-to-skill`, `notebook-to-book` / `book-notebook`, `/research`, `learn-teach`, bộ skill DMIR (`/cld`, `/archetype`, `/sdmodel`, `/constraint`, `/leverage`, `/reflect`, `/paradigm`), `galaxy-gate`
- **Tiền lệ làm tay:** `2_Areas/CEO-Self/Learning-Architecture/PRACTICE_PahlBeitz_Mastery_2026-03-21.md`, `2_Areas/CEO-Self/AI-Fluency-Ledger/`
- **Tham chiếu DMIR:** 3 tài liệu CEO cung cấp 2026-09-17 (Unified Framework × ODI × P&B; Deep Research; Playbook v1.0) + `Learning-Architecture/DMIR_Skill_Architecture_v2.md`

## 1. Mục đích và tiêu chí xong

Giúp CEO **đọc hiểu → thực hành → ứng dụng** một cuốn sách vào Workshop X trong **một chu kỳ ~30 ngày**.

**Một chu kỳ chỉ được coi là xong khi:** có ≥1 thí nghiệm ứng dụng vào một vấn đề thật của Workshop X, được CEO duyệt, chạy thật, đo được kết quả, và đóng vòng DMIR-R (AAR + quyết định giữ / chỉnh / bỏ). Chu kỳ không có thí nghiệm vẫn đóng được, nhưng ghi `applied:false` vào sổ meta — **không bao giờ ghi là "xong"**.

Quyết định thiết kế (CEO chốt 2026-09-17):

| Câu hỏi | Quyết định |
|---|---|
| Đích | Ứng dụng đo được |
| Nhịp | ~30 ngày mỗi cuốn |
| Mở rộng | Cả 4 hướng: phản biện & bằng chứng; chuyển bối cảnh VN; bản mới & tác phẩm sau; nối tri thức sẵn có |
| Meta-learning | Cả 3 tầng: hiểu cách CEO học; chuyển giao giữa các sách; pipeline tự cải tiến |
| NotebookLM | Toàn văn, mỗi chương một nguồn |
| Kiến trúc | **A — orchestrator mỏng**, gọi lại skill có sẵn, chỉ viết mới phần còn thiếu |
| Vị trí chu kỳ | `1_Projects/LEARN-<slug>/` |

## 2. DMIR dùng trong skill

**Định nghĩa dùng:** Diagnose–Model–Intervene–Reflect, là **tầng meta** chứ không phải framework thứ tư (theo `DMIR_Skill_Architecture_v2.md`):

- **D — Systems Thinking:** ranh giới hệ, archetype, mô hình tư duy ngầm.
- **M — System Dynamics:** stock / flow / độ trễ / vòng lặp; lượng hoá biến.
- **I — Theory of Constraints:** điểm nghẽn, 5 bước tập trung; chọn can thiệp theo mức đòn bẩy Meadows L12→L1.
- **R — Meta-learning:** AAR, học vòng kép, deutero-learning; leo dần thang đòn bẩy qua các chu kỳ.

**Quy tắc áp dụng:**
- **Chu kỳ 30 ngày dùng DMIR bản nhẹ** (chính tài liệu cảnh báo khi nào không nên dùng bản đầy đủ). M = 1 CLD + 3 biến hiện tại→mục tiêu. `/sdmodel` chỉ chạy khi CEO yêu cầu.
- **Chỉ lấy cấu trúc, câu hỏi, template từ tài liệu tham chiếu.** Không trích như sự thật các con số chưa có nguồn kiểm (ví dụ "70% change initiatives fail", "15x faster", "ROI 10–50x", các case có ghi "giả lập").
- **Biến thể tên:** `1_Projects/BB-01_LOMAH/References/dmir1…4` dùng Diagnose–Measure–Improve–Review. Skill ghi rõ đây là biến thể khác. Hợp nhất hay không là việc CEO quyết riêng.

**Meta-learning đo theo 3 trục:**
- Mức thành thạo Dreyfus 1–5 (Novice → Expert).
- Mức đòn bẩy đã chạm tới L12→L1.
- Mức siêu nhận thức Perkins: tacit / aware / strategic / reflective.

## 3. Các pha

| Pha | Ngày | Việc | Gọi | COD | Cổng |
|---|---|---|---|---|---|
| **L0 Mission** | 0 | Đọc `Status.md` dự án đích. CEO ghi **vấn đề/quyết định thật** + **3 dự đoán** về sách + tiêu chí thành công + **tự chấm mức Dreyfus ban đầu** (chấm lại ở L7). DMIR-R bước lập kế hoạch siêu nhận thức. | khuôn MISSION | C | **Chặn cứng** nếu thiếu vấn đề thật |
| **L1 Trích** | 1–2 | Skill tri thức (DEPTH=study); gán mỗi framework một mức đòn bẩy → `Leverage_Map.md` | `book-to-skill` | O | script |
| **L2 NLM** | 2 | Notebook `btl-<slug>-goc`: toàn văn, mỗi chương một nguồn | logic `book-notebook` | O | script |
| **L3 Mở rộng** | 3–6 | 4 hướng → notebook `btl-<slug>-mo-rong` → `Claims.md` (SUPPORTED / CONTESTED / CẦN-CHUYỂN-VN) | `/research` | O | **C** duyệt danh sách nguồn trước khi nạp |
| **L4 Học** | 3–10 | Workspace `learn/` chỉ cho framework ứng viên áp dụng; nhịp micro-DMIR hằng tuần; ôn giãn cách hết chu kỳ | `learn-teach` | O+C | không chặn |
| **L5 Thiết kế** | 8–12 | **D:** `/archetype` + `/cld`. **M:** 3 biến. **I:** `/constraint` + `/leverage`. → `Experiment_Card.md` với dự đoán ghi trước. D+M tối đa 2 phiên. | DMIR skills | O soạn, C chọn | **C** duyệt thẻ; thiếu thì L6/L7 bị khoá |
| **L6 Chạy** | 12–28 | Chạy thật; `Run_Log.md`; kiểm tra 10/25: "điểm nghẽn còn đó không?" | — | C | trễ hạn → cảnh báo `Status.md` |
| **L7 Retro** | 28–30 | AAR 4 câu; vòng kép (L3 mục tiêu, L2 mô hình tư duy); nối sổ meta; ứng viên Galaxy; đề xuất sửa skill; gợi ý sách kế tiếp | `/reflect`, `/paradigm`, `galaxy-gate` | O soạn, C quyết | **C** giữ / chỉnh / bỏ |

**Thứ tự:**
- L0 → L1 → L2 chạy liền.
- L3 (máy, nền) song song L4 (phiên CEO).
- L5 cần `Claims.md`. Nếu `--quick` thì mọi framework bị gắn nhãn CHƯA KIỂM.

## 4. Lệnh

```
/book-to-learn <file|thư mục> [--slug X] [--notebook <id>] [--target <dự án>]
               [--from Ln] [--only Ln] [--resume] [--quick]
```
- `--quick`: bỏ L3. **Không bỏ được L0 / L5 / L7.**
- `--only L5 --target <dự án>`: dùng lại một cuốn đã học.
- `--resume`: đọc `_pipeline_state.md`.

## 5. Dữ liệu

**Mã skill (KN-Stack):**
```
skills/book/book-to-learn/SKILL.md
skills/book/book-to-learn/references/dmir-unified.md      cô đọng 3 tài liệu DMIR + nguồn + cảnh báo
skills/book/book-to-learn/references/phase-contracts.md   in/out/skill gọi/điều kiện cổng mỗi pha
skills/book/book-to-learn/references/templates/           mission, claims, experiment-card, aar, cycles-row
scripts/btl_gate_check.py
scripts/test_btl_gate_check.py   (+ evals/fixtures/btl/)
evals/book-to-learn.json         (mode: static)
```

**Tri thức bền về sách (Data Bus của notebook-to-book):**
```
3_Resources/Books/<slug>/_source/        chương tách để upload
3_Resources/Books/<slug>/Leverage_Map.md
3_Resources/Books/<slug>/Claims.md
~/.claude/skills/<slug>/                 skill tri thức
```

**Chu kỳ học (dự án PARA; xong thì chuyển 4_Archives):**
```
1_Projects/LEARN-<slug>/_Project_Brief.md   = MISSION
1_Projects/LEARN-<slug>/Status.md
1_Projects/LEARN-<slug>/_pipeline_state.md  pha, dấu cổng, id 2 notebook
1_Projects/LEARN-<slug>/learn/              workspace learn-teach
1_Projects/LEARN-<slug>/Experiment_Card.md
1_Projects/LEARN-<slug>/Run_Log.md
1_Projects/LEARN-<slug>/AAR.md
```
Dự án đích chỉ nhận **một dòng liên kết** tới thẻ thí nghiệm, sau khi CEO đồng ý.

**Sổ meta xuyên sách:**
```
2_Areas/CEO-Self/Learning-Meta/cycles.jsonl    1 dòng/cuốn
2_Areas/CEO-Self/Learning-Meta/calibration.md
2_Areas/CEO-Self/Learning-Meta/transfer-map.md
2_Areas/CEO-Self/Learning-Meta/skill-backlog.md
```

Schema một dòng `cycles.jsonl`:
```json
{"slug":"profit-first","opened":"YYYY-MM-DD","closed":"YYYY-MM-DD","target":"VN-TGT-F",
 "dreyfus_before":2,"dreyfus_after":3,"leverage_reached":"L5","perkins":"strategic",
 "applied":true,"decision":"keep|adapt|drop","prediction_hits":1,"prediction_total":3,
 "failure_points":["..."],"next_book_hint":"..."}
```

## 6. Cơ chế chống thủng

### 6.1 `btl_gate_check.py <LEARN-dir> <phase>`

Exit ≠ 0 thì không được đánh dấu pha xong. Exit 0 thì script ghi dấu thời gian vào `_pipeline_state.md`.

| Pha | Kiểm |
|---|---|
| L0 | ô `van_de_that` khác rỗng; đúng 3 dự đoán; ô `dreyfus_truoc` ∈ 1–5; nếu có `--target` thì thư mục dự án đích tồn tại, nếu không thì ô `noi_ap_dung` khác rỗng (ví dụ: cả Workshop X); quyết định ghi bằng chữ (cấm dòng chỉ gồm nhãn `(A)`/`(B)`) |
| L1 | skill có `SKILL.md` và ≥1 tệp `chapters/`; **không có `\$[0-9]` trong SKILL.md**; mọi framework trong `Leverage_Map.md` có mức `L1`–`L12` |
| L2 | JSON `nlm source list -j`: số nguồn sẵn sàng = số tệp `_source/`; mỗi nguồn có độ dài nội dung (lấy qua `nlm source content -j`) ≥ 50% số ký tự của tệp chương tương ứng (status=2 vẫn có thể là trang chặn bot) |
| L3 | mỗi dòng `Claims.md` có nhãn hợp lệ và nguồn kèm vị trí; không có "✅" trần |
| L5 | đủ ô: giả thuyết, chỉ số, baseline **là số**, ngưỡng, người chịu trách nhiệm, ngày kết thúc ≤ bắt đầu + 16, dự đoán, `don_vi_framework` = `don_vi_thi_nghiem`, mức tin cậy dữ liệu, dấu duyệt CEO |
| L7 | AAR có đủ 4 câu; quyết định ∈ {keep, adapt, drop}; đã nối dòng `cycles.jsonl` hợp lệ theo schema; L5 chưa duyệt thì bắt buộc `applied:false` |

### 6.2 NotebookLM
- Cấm `chat_configure(goal=custom)`.
- Mỗi truy vấn một conversation mới; loại câu trả lời có `sources_used = 0`.
- Số liệu NLM trả về phải grep lại trong `_source/` với `LC_ALL=C.UTF-8`, thử nhiều cách viết. Tự kiểm lại mình trước khi kết luận NLM sai.
- 2 lỗi nhanh liên tiếp (4–6 giây) → dừng, nghi hết hạn mức.
- Không tin kết quả in ra của `nlm source add`.

### 6.3 Bản quyền và rò rỉ
- Notebook `btl-*` không bao giờ share public; `_source/` chỉ trong vault.
- Không chép nguyên văn dài; trích ngắn có số trang.
- Chương bị loại khỏi NLM: không ghi lý do loại vào manifest hay truy vấn.

### 6.4 Bẫy phân tích và bịa
- L5 D+M tối đa 2 phiên.
- Số liệu sách giữ bối cảnh gốc; dùng ở VN phải có dòng CẦN-CHUYỂN-VN.
- Ứng viên Galaxy phải qua `galaxy-gate` và đối chiếu `5_Galaxy` trước; AI không tự tạo ghi chú.
- Sửa ở tệp nguồn (Brief, Claims), không vá vào tệp dựng ra.

## 7. Kiểm thử
- **pytest `test_btl_gate_check.py`:** mỗi pha 1 bộ đạt + các bộ trượt: L0 thiếu vấn đề / 2 dự đoán; L1 còn `$0`; L2 lệch số nguồn / nguồn rỗng; L3 "✅" trần; L5 baseline chữ / quá 16 ngày / lệch đơn vị / thiếu duyệt; L7 thiếu quyết định / `applied:true` khi L5 chưa duyệt. L2 dùng JSON giả.
- **Eval static `book-to-learn.json`:** SKILL.md có 3 cổng C, lệnh gọi script, cấm persona, cấm share public, tên các skill DMIR, định nghĩa DMIR. Kiểm eval bằng đột biến: xoá câu theo đúng regex của assertion → eval phải trượt.
- `bash setup.sh --verify`.

## 8. Triển khai
- Worktree `D:\KN-Stack-btl`, nhánh `feature/book-to-learn` tách từ `origin/feature/evals-static-mode`.
- Commit `[BOOK] …`. Không sửa `VERSION` / `CHANGELOG.md` / số skill trong `CLAUDE.md`; changelog để trong PR mục `## CHANGELOG`.
- Chạy test trước khi mở PR.
- **Dogfood:** `/book-to-learn <Profit First pdf> --slug profit-first --target VN-TGT-F`. L1 dùng lại skill `~/.claude/skills/profit-first` qua cổng kiểm; L5 là quyết định thật của CEO. Ứng viên: định giá pilot, hoặc 4 tài khoản Profit First cho cả Workshop X. Pipeline coi là chạy được khi qua L0–L5 bằng script, và ngày 30 có dòng `cycles.jsonl` với `applied:true`.

## 9. Ngoài phạm vi
Học nhiều sách song song; audio / EPUB; persona tác giả; tự tạo ghi chú Galaxy. Chỉ mở lại nếu `skill-backlog.md` cho thấy cần.
