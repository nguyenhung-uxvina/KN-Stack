# helix-p3-form (khối BF) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Thêm khối P3 bắt buộc `helix-p3-form` (BF, giữa B0 và BA). Khối đi từ từng chức năng → phương án hình thể bằng C&C² + hướng dẫn chưng cất từ ba sách → đối chiếu giải pháp hiện có (dự án/web/sáng chế) → chấm D-lọc + W×HOQ → CEO chọn → bàn giao BA.

**Architecture:** Đợt 1 dựng bộ tham chiếu (6 tệp trong `skills/helix/helix-p3-form/references/`), mọi dòng có con trỏ sách được máy kiểm (`p3_form_ref_check.py`). Đợt 2 dựng SKILL.md của BF, cổng máy cho đầu ra BF (`p3_form_lint.py`), sửa orchestrator P3 và 3 khối liên quan, eval static, rồi chạy thử trên VN-TGT-F `--variant TGT-10`.

**Tech Stack:** Markdown SKILL (Claude Code skills), Python 3 stdlib + pytest, eval runner `evals/run-eval.sh` (static mode).

**Spec:** `docs/superpowers/specs/2026-10-27-helix-p3-form-design.md`

## Global Constraints

- Nhánh `feature/helix-p3-form`, worktree `D:/KN-Stack-wt-p3form` tách từ `origin/feature/evals-static-mode`. Không mang thay đổi chưa commit của `D:/KN-Stack`.
- Commit: `[HELIX] <mô tả>`, kết bằng `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- KHÔNG sửa `VERSION`, `CHANGELOG.md`, `scripts/_codify_ledger.md`. Changelog đặt trong mô tả PR dưới `## CHANGELOG`.
- Sách (ngoài repo, chỉ đọc):
  - TKHT = `D:/Workshop_X/3_Resources/Books/thiet-ke-hien-than/book.md` (tiêu đề `# Chương NN[a-z]`, mục `## NN.x`)
  - TKKTHT = `D:/Workshop_X/3_Resources/Books/thiet-ke-ky-thuat-he-thong/Phase6-Revised-Tap1/Ch*_v2.md` (mỗi tệp một chương, `# Chương NN`, mục `### x.y`); TKKTHT2 = `.../Phase6-Revised-Tap2/Ch*_v2.md`
  - KL9 = `D:/Workshop_X/3_Resources/Books/pahl-beitz-konstruktionslehre/book.md` (`# Chương NN`, mục theo số Kap. gốc `## 13.6`)
- Ký hiệu trích nguồn duy nhất: `[TKHT Ch05b §05b.4]`, `[TKKTHT Ch16 §3.1]`, `[TKKTHT2 Ch13]`, `[KL9 Ch08 §13.6]`; dòng ngoài sách ghi `[ngoài sách]`.
- Trích nguyên văn ≤ 1 câu, trong `“…”` hoặc `«…»`. Diễn ý cho phần còn lại.
- Nhãn tri thức đúng ba chữ: `tri thức` / `phỏng đoán` / `giả định`.
- Python chạy `python -X utf8`; grep tiếng Việt `LC_ALL=C.UTF-8`; đọc tệp `utf-8-sig`, chuẩn hoá NFC.
- Mỗi tệp tham chiếu ≤ ~1.500 dòng.
- Không dữ liệu mật, không giá nhà cung cấp.
- Báo cáo của tác tử con không phải bằng chứng — mỗi task kết thúc bằng lệnh kiểm máy + đọc hiện vật.

## Review Focus

1. Chương có hậu tố chữ (`Ch05b`, `Ch13b`, `Ch02a`) và trích TKKTHT2 — người dùng cần trích đúng vẫn qua; được ghim ở Task 1 `test_letter_suffix_chapter` và `test_tap2_citation`.
2. Trích nguyên văn có `…` ở giữa — mỗi đoạn hai bên `…` phải được kiểm riêng, không bị coi là một chuỗi liền (lớp lỗi «đầu thật đuôi bịa» đã gặp); Task 1 `test_ellipsis_quote_tail_fabricated`.
3. Tệp đầu ra viết bằng NFD hoặc có BOM — không được báo lỗi giả; Task 1 `test_nfd_and_bom_input`, Task 7 `test_lint_nfd_bom`.
4. Bảng chấm có W trọng số trống: hợp lệ CHỈ KHI có `🔴`; ô `?` không lý do là lỗi; Task 7 `test_empty_weight_requires_red_flag`, `test_question_cell_requires_reason`.
5. Nguồn giải pháp hiện có dạng số sáng chế có dấu phẩy/khoảng trắng (`US 9,097,498 B2`, `CN116753779A`) hoặc đường dẫn tệp dự án — phải nhận là nguồn hợp lệ; Task 7 `test_benchmark_source_forms`.

---

## ĐỢT 1 — Bộ tham chiếu

### Task 0: Worktree, nhánh, commit spec + plan

**Files:**
- Create (copy): `docs/superpowers/specs/2026-10-27-helix-p3-form-design.md`, `docs/superpowers/plans/2026-10-27-helix-p3-form.md` (copy từ `D:/KN-Stack` — hai tệp này chưa tracked ở đó)

- [ ] **Step 1:** `git -C D:/KN-Stack fetch origin && git -C D:/KN-Stack worktree add D:/KN-Stack-wt-p3form -b feature/helix-p3-form origin/feature/evals-static-mode`
- [ ] **Step 2:** Copy hai tệp spec/plan vào worktree cùng đường dẫn; xoá bản untracked ở `D:/KN-Stack` sau khi copy xong (để không có hai bản lệch nhau).
- [ ] **Step 3:** Kiểm `ls D:/KN-Stack-wt-p3form/skills/helix/helix-cc2/references/` có `hypothesis-sheet.md` (worktree đúng gốc). Commit `[HELIX] Spec + plan helix-p3-form (khối BF)`.

### Task 1: `p3_form_ref_check.py` — kiểm con trỏ sách trong references

**Files:**
- Create: `scripts/p3_form_ref_check.py`
- Test: `scripts/test_p3_form_ref_check.py`
- Fixtures: `evals/fixtures/p3_form/books/{tkht.md,tkktht/Ch16_x_v2.md,tkktht2/Ch13_y_v2.md,kl9.md}`, `evals/fixtures/p3_form/refs/*.md`

**Interfaces:**
- Consumes: mẫu `scripts/cc2_ref_check.py` (load_book theo tiêu đề chương, `norm()` NFC + gộp khoảng trắng, giữ dấu).
- Produces:
  - CLI `python -X utf8 scripts/p3_form_ref_check.py <thư-mục-references> [--sample 0.1 --seed N --out <tệp>]`; exit 0 sạch, 1 có finding, 2 lỗi đọc, 3 thiếu sách.
  - Env ghi đè đường dẫn sách: `P3F_BOOK_TKHT`, `P3F_BOOK_TKKTHT`, `P3F_BOOK_TKKTHT2`, `P3F_BOOK_KL9` (TKKTHT/TKKTHT2 là thư mục, nối `Ch*_v2.md` theo tên).
  - `load_book(path) -> dict[chapter_id, {'text': str, 'sections': set[str]}]`
  - `check_file(path, books) -> list[Finding]`, `Finding = namedtuple('Finding','file line code msg')`
  - Mã lỗi: `CHAPTER_NOT_FOUND`, `SECTION_NOT_FOUND`, `QUOTE_NOT_FOUND`, `UNCITED_ROW` (dòng bảng dữ liệu không có trích nào và không có `[ngoài sách]`), `NO_CITATION` (< 5 trích/tệp).
  - `--sample`: chọn ngẫu nhiên tỉ lệ dòng có trích, ghi ra `<tệp>` mỗi dòng kèm văn bản mục sách được trỏ (≤ 400 từ) để người kiểm đọc đối chiếu.

- [ ] **Step 1: Viết test thất bại** — trong `test_p3_form_ref_check.py`:
  - `test_valid_citations_pass`: ref có `[TKHT Ch05 §05.4]`, `[TKKTHT Ch16 §3.1]`, `[KL9 Ch08 §13.6]` khớp fixture → `findings == []`.
  - `test_chapter_not_found`: `[TKHT Ch99]` → một finding `CHAPTER_NOT_FOUND`.
  - `test_section_not_found`: `[TKKTHT Ch16 §9.9]` → `SECTION_NOT_FOUND`.
  - `test_letter_suffix_chapter`: `[TKHT Ch05b §05b.4]` với fixture có `# Chương 05b` và `## 05b.4` → sạch; `[TKHT Ch05 §05b.4]` → `SECTION_NOT_FOUND`.
  - `test_tap2_citation`: `[TKKTHT2 Ch13]` khớp fixture tap2 → sạch.
  - `test_quote_found_and_not_found`: `“…8+ từ có trong chương…”` sạch; đổi 1 từ → `QUOTE_NOT_FOUND`; cả `«»` cũng được kiểm.
  - `test_ellipsis_quote_tail_fabricated`: `“<đầu có thật> … <đuôi bịa>”` → `QUOTE_NOT_FOUND` (mỗi đoạn ≥ 4 từ quanh `…` kiểm riêng).
  - `test_uncited_row`: dòng bảng dữ liệu không trích, không `[ngoài sách]` → `UNCITED_ROW`; dòng tiêu đề và `|---|` không bị bắt.
  - `test_nfd_and_bom_input`: ref lưu NFD + BOM, nội dung hợp lệ → sạch.
  - `test_missing_book_exit3`: env trỏ tệp không có → exit 3.
- [ ] **Step 2:** `python -X utf8 -m pytest scripts/test_p3_form_ref_check.py -v` → FAIL (module chưa có).
- [ ] **Step 3:** Viết `scripts/p3_form_ref_check.py` theo Interfaces. Regex trích: `\[(TKHT|TKKTHT2|TKKTHT|KL9)\s+Ch(\d{2}[a-z]?)(?:\s*§\s*([0-9]{1,2}[a-z]?(?:\.[0-9]+[a-z]?)+))?\]`. Mục khớp khi chương có dòng tiêu đề `^#{2,4}\s+<token>(?=[\s—–:.-]|$)`. Trích ≥ 8 từ mới kiểm (đoạn quanh `…`: ≥ 4 từ).
- [ ] **Step 4:** Chạy lại test → PASS. Chạy thật trên `skills/helix/helix-cc2/references/` với sách thật chỉ để khói (định dạng trích khác → mong đợi 0 trích nhận diện, exit 1 `NO_CITATION`; ghi kết quả vào commit message).
- [ ] **Step 5: Đột biến:** xoá lần lượt từng dòng `regex`/điều kiện mà mỗi assert dựa vào, xác nhận test tương ứng đỏ; khôi phục. Commit `[HELIX] p3_form_ref_check: kiểm con trỏ ba sách cho references BF`.

### Task 2: `references/tkht-rules.md` — chưng cất *Thiết kế hiện thân*

**Files:** Create `skills/helix/helix-p3-form/references/tkht-rules.md`

**Interfaces:**
- Produces: các mục `## <Nhóm>` (Ch01–Ch03b phương pháp; Ch04–Ch16 kho quy tắc; Ch17–Ch20 vòng đời). Mỗi quy tắc một dòng bảng 7 cột cố định:
  `| Quy tắc | Điều kiện đúng | Câu hỏi kiểm hình thể | Tham số khoá | Con số / khoảng | Kiểu hỏng khi vi phạm | Nguồn |`
  Mã quy tắc ở cột 1 dạng `TKHT-R<nn>` (dùng cho Task 5 và BF).
- Ghi riêng mục `## C&C² 7 bước dựng mô hình` (Ch02a) và `## Ca TG-2` (Ch20) dạng danh sách đánh số, mỗi bước có trích nguồn.

- [ ] **Step 1:** Chia việc theo chương cho tác tử con (mỗi tác tử 3–4 chương, đọc `Phase6-Revised/` hoặc chương tương ứng trong `book.md`), mỗi tác tử trả về các dòng bảng đúng 7 cột. Brief chỉ trỏ tới khuôn cột này, không nhắc lại thuật ngữ (bài học fan-out).
- [ ] **Step 2:** Gộp, đánh số `TKHT-R01…`, khử trùng lặp (giữ một nhà chính, dòng còn lại trỏ mã).
- [ ] **Step 3:** `python -X utf8 scripts/p3_form_ref_check.py skills/helix/helix-p3-form/references` → 0 finding cho tệp này. Cột «Con số / khoảng» để `—` khi sách không cho số (không bịa).
- [ ] **Step 4:** `--sample 0.1 --seed 1 --out <scratchpad>/sample_tkht.md`; người kiểm (không phải tác tử viết) đọc từng dòng mẫu đối chiếu văn bản sách; sửa mọi dòng lệch; ghi tỉ lệ lệch vào commit message.
- [ ] **Step 5:** `wc -l` ≤ ~1.500. Commit `[HELIX] BF references: tkht-rules (TKHT Ch01–Ch20)`.

### Task 3: `references/tkktht-guidelines.md` — chưng cất *Thiết kế kỹ thuật hệ thống* (P&B)

**Files:** Create `skills/helix/helix-p3-form/references/tkktht-guidelines.md`

**Interfaces:**
- Produces (các mục bắt buộc, theo đúng tên):
  - `## 15 bước hiện thân và 3 cổng` (Tập 1 Ch13) — danh sách đánh số, đánh dấu 3 bước là CỔNG.
  - `## Checklist 14 mục` — bảng `| # | Mục | Câu hỏi ví dụ | Nguồn |`, đủ 14 dòng đánh số 1–14 đúng thứ tự Figure 7.3, kèm ba luật dùng checklist. Task 7 lint dùng đúng tên 14 mục này.
  - `## Quy tắc và nguyên lý` — bảng 7 cột như Task 2, mã `PB-R<nn>`, phủ Tập 1 Ch14–Ch22.
  - `## Bảng tra mối ghép (§8.1.5)` — Ch23, bảng `| Mục đích dùng | Loại mối ghép (lớp vật lý) | Điều kiện | Nguồn |`.
  - `## Cơ điện tử, dãy cỡ, mô-đun` — Ch24–Ch26, bảng 7 cột, mã `PB-M<nn>`.
  - `## Đánh giá ở pha hiện thân` — Ch22 §7.6 (cùng mức cụ thể hoá; ≥1 tiêu chí mỗi mục checklist) — Task 5 `scoring.md` trỏ vào đây.
  - Chỗ Tập 2 phân tích sâu hơn: thêm dòng trỏ `[TKKTHT2 ChNN]`.

- [ ] **Step 1–5:** như Task 2 (tác tử con theo chương; ref_check 0 finding; mẫu 10% `--seed 2`; ≤ ~1.500 dòng). Thêm kiểm: `grep -c "^| *[0-9]\{1,2\} *|" ` trong mục Checklist = 14. Commit `[HELIX] BF references: tkktht-guidelines (P&B Ch13–Ch26 + checklist 14 mục)`.

### Task 4: `references/kl9-gestaltung.md` — chưng cất *Konstruktionslehre* 9

**Files:** Create `skills/helix/helix-p3-form/references/kl9-gestaltung.md`

**Interfaces:**
- Produces: mục `## Quá trình và mô hình hiện thân (Kap. 13.1–13.5)`, `## Phân tích và tổng hợp (Kap. 13.6–13.8)`, `## Thiết kế công nghiệp (16.9)`, `## Sản xuất bồi đắp (16.13)`, `## Chi phí · sinh thái · tiêu chuẩn · sở hữu công nghiệp` (KL9 Ch13–Ch16), `## Phát triển sản phẩm ảo` (Ch17). Quy tắc dạng bảng 7 cột mã `KL-R<nn>`. Mỗi mục mở bằng 1–3 câu «Khác/mới so với TKKTHT:» có trích nguồn.

- [ ] **Step 1–5:** như Task 2 (`--seed 3`). Commit `[HELIX] BF references: kl9-gestaltung (KL9 Kap.13, 16.9, 16.13, 21–25)`.

### Task 5: `function-index.md`, `scoring.md`, `benchmark-search.md`

**Files:** Create `skills/helix/helix-p3-form/references/{function-index.md,scoring.md,benchmark-search.md}`; Modify `skills/helix/helix-cc2/references/embodiment-rules.md` (thêm 1 dòng đầu tệp trỏ sang `helix-p3-form:references:function-index`).

**Interfaces:**
- `function-index.md`: bảng `| Loại chức năng | Quy tắc áp dụng (mã) | Mục catalog | Câu hỏi mở đầu |` cho ít nhất 10 loại: nhận/tiêu tán va đập; truyền lực; định vị/dẫn hướng; nối ghép; bịt kín; giữ nổi/ổn định; bảo vệ cảm biến; dẫn điện/tín hiệu; tản nhiệt; thao tác người. Mọi mã trỏ tới phải tồn tại trong Task 2–4 (kiểm bằng grep, Step 2).
- `scoring.md`: thang 0–4 (VDI 2225) với mô tả từng mức; ánh xạ yêu cầu → DP qua cột nguồn `HOQ-DPx`; luật W không DP: giữ, `🔴`, trọng số trống (spec §13 Q7); luật `D/W tạm` (Q6); ô `?(<lý do>)`; độ nhạy ±20% trọng số và `?`→0/4; định dạng bảng đúng như Task 7 lint (dán nguyên khuôn bảng).
- `benchmark-search.md`: 3 tầng (dự án → Exa web → sáng chế qua Exa, ưu tiên ≤ 5 năm, đọc hình vẽ); truy vấn theo CHỨC NĂNG; ≤ 8 giải pháp/chức năng; khuôn hồ sơ một giải pháp đúng định dạng Task 7 (`Nguồn:`, `Truy cập:`, `Nhãn:`, `Chuỗi C&C²:`); cờ FTO chuyển `ip-*` / QP-02-06, không phán định.

- [ ] **Step 1:** Viết ba tệp.
- [ ] **Step 2:** Kiểm mã: mọi `TKHT-R|PB-R|PB-M|KL-R<nn>` trong `function-index.md` có trong tệp nguồn (`grep -o` + so tập hợp, lệnh một dòng; 0 mã treo).
- [ ] **Step 3:** `p3_form_ref_check.py` trên cả thư mục → exit 0.
- [ ] **Step 4:** Commit `[HELIX] BF references: function-index, scoring, benchmark-search`.

### Task 6: ⛔ Cổng CEO cuối Đợt 1

- [ ] **Step 1:** Gộp ba tệp mẫu (Task 2–4) thành `<scratchpad>/BF_ref_sample_review.md` (dòng + văn bản sách + phán quyết người kiểm).
- [ ] **Step 2:** Trình CEO: số dòng mỗi tệp, tỉ lệ lệch ở mẫu, 5 dòng `function-index` cho «nhận va chạm đầu đạn» và «giữ nổi thẳng đứng». CEO đọc mẫu, duyệt hoặc trả sửa. **Không sang Đợt 2 khi chưa duyệt.**

---

## ĐỢT 2 — Khối BF

### Task 7: `p3_form_lint.py` — cổng máy cho đầu ra BF

**Files:**
- Create: `scripts/p3_form_lint.py`, `scripts/test_p3_form_lint.py`
- Fixtures: `evals/fixtures/p3_form/out_good/` (bộ 4 tệp hợp lệ), các biến thể hỏng sinh trong test.

**Interfaces:**
- CLI: `python -X utf8 scripts/p3_form_lint.py <thư-mục-đầu-ra> --prefix <PREFIX> [--quick]`; exit 0/1/2.
- `lint_dir(path, prefix, quick=False) -> list[Finding]` (cùng `Finding` như Task 1).
- Định dạng được kiểm (SKILL.md Task 8 dán nguyên các khuôn này):
  - `<P>BF_Form_Variants.md`: `## F-<id> — <tên>`; phương án `### PA-<F-id>-<n> — <tên>`; trong mỗi phương án các dòng `Nguồn quy tắc:` (≥1 trích dạng Global Constraints), `Tham số khoá:` (không rỗng), `Nhãn:` (một trong ba nhãn). ≥3 PA/F (≥2 khi `--quick`). Mã: `TOO_FEW_VARIANTS`, `VARIANT_NO_RULE`, `VARIANT_NO_PARAM`, `BAD_LABEL`.
  - `<P>BF_Benchmark.md`: `### HC-<F-id>-<n> — <tên>`; `Nguồn:` khớp URL `https?://`, hoặc số công bố `\b(US|EP|CN|WO|JP|KR|DE)\s?[\d,\s]{5,}\s?[A-Z]\d?\b`, hoặc đường dẫn có `/` hay `\`; `Truy cập:` `YYYY-MM-DD`; `Nhãn:`; `Chuỗi C&C²:` không rỗng. ≤ 8 HC/F. Mã: `BENCH_NO_SOURCE`, `BENCH_NO_DATE`, `BENCH_NO_CHAIN`, `TOO_MANY_BENCH`, `BAD_LABEL`.
  - `<P>BF_Scoring.md`: mục `## Checklist 14 mục` — bảng đủ 14 dòng số 1–14, mỗi dòng có tiêu chí hoặc `Bỏ — lý do: <…>` (`CHECKLIST_INCOMPLETE`, `CHECKLIST_SKIP_NO_REASON`). Mục `## Bảng chấm` — bảng `| Req-ID | D/W | DP | Trọng số | <ứng viên…> | Ghi chú |`; dòng D: ô ∈ {`Đạt`,`Loại`,`?(…)`}; dòng W: ô ∈ {`0`–`4`,`?(…)`}; `Trọng số` số hoặc trống kèm `🔴` trong dòng (`EMPTY_WEIGHT_NO_FLAG`, `BAD_CELL`, `QUESTION_NO_REASON`). Có mục `## Độ nhạy` (`NO_SENSITIVITY`). Cột ứng viên phải gồm mọi `PA-*` và `HC-*` của F tương ứng (`CANDIDATE_MISSING`). Dòng `D/W` mang chữ `tạm` hợp lệ.
  - `<P>BF_Form_Selection.md`: mỗi `## F-<id>` có `Chọn: PA-…` (hoặc `HC-…`), `Khoảng tham số:` và `Kế hoạch thử:` không rỗng. Mã `NO_SELECTION`, `NO_TEST_PLAN`, `NO_PARAM_RANGE`.
  - Thiếu tệp: `MISSING_FILE`.

- [ ] **Step 1: Test thất bại:** `test_good_fixture_clean`; một test cho mỗi mã lỗi trên (đột biến fixture tốt bằng thay chuỗi trong `tmp_path`); `test_quick_allows_two_variants`; `test_empty_weight_requires_red_flag`; `test_question_cell_requires_reason`; `test_benchmark_source_forms` (`US 9,097,498 B2`, `CN116753779A`, `https://…`, `RE/ArtixGear/x.md` → hợp lệ; `báo chí` → `BENCH_NO_SOURCE`); `test_provisional_dw_ok`; `test_lint_nfd_bom`.
- [ ] **Step 2:** `python -X utf8 -m pytest scripts/test_p3_form_lint.py -v` → FAIL.
- [ ] **Step 3:** Viết `scripts/p3_form_lint.py`.
- [ ] **Step 4:** Test → PASS. Đột biến theo chính regex của từng assert (xoá điều kiện → test đỏ → khôi phục).
- [ ] **Step 5:** Commit `[HELIX] p3_form_lint: cổng máy cho đầu ra khối BF`.

### Task 8: `skills/helix/helix-p3-form/SKILL.md` + eval static

**Files:**
- Create: `skills/helix/helix-p3-form/SKILL.md`, `evals/helix-p3-form.json`

**Interfaces:**
- Consumes: references Task 2–5; khuôn tệp Task 7; `helix-cc2:references:{cc2-core,view-ops,synthesis-moves,hypothesis-sheet,param-bridge}`.
- Produces: skill `helix-p3-form`, ID BF; cờ `<project> [--variant <V>] [--function <F-id>] [--quick]`; tiền tố/thư mục theo luật VARIANT_SHORT của P3 (`<PROJECT>_<V0>_`; thư mục `Phase3-Embodiment/<V>/`). Với `VN-TGT-F --variant TGT-10` → `VN_TGT_F_TGT10_`, thư mục `Phase3-Embodiment/TGT-10/`.
- Nội dung SKILL (theo spec §5–§8, §11b, §13): frontmatter `name: helix-p3-form`, description có «Triggers on: …» EN+VI; bảng đầu vào + glob linh hoạt (chấp nhận tệp không tiền tố như `BE_Concept_Selection.md`, `Requirements_Draft`); F1…F7 với hai cổng CEO; D/W tạm (Q6); `🔴` W không DP (Q7); P2 cấp hệ → suy nguyên lý, nhãn *phỏng đoán*; nhập `CC2_Handoff` nếu có, sinh nếu chưa (định dạng C6); khuôn 4 tệp đầu ra dán nguyên từ Task 7; bước cuối bắt buộc `python -X utf8 D:/KN-Stack/scripts/p3_form_lint.py <dir> --prefix <P>` phải exit 0 trước Cổng 2; Analyst Trap: mỗi phương án chọn phải có kế hoạch thử; COD (F1/F7 Core, F2–F6 Offload); chỉ nạp mục reference cần qua `function-index.md`.

- [ ] **Step 1: Eval thất bại** — `evals/helix-p3-form.json` (`mode: "static"`, `include_references: true`), assertions `required: true`, ít nhất: `BF-POSITION` (`B0.*BF.*BA`), `BF-GATES` (2 cổng CEO), `BF-3VAR` (`≥ ?3 phương án`), `BF-3TIER` (`dự án.*web.*sáng chế`), `BF-READ-FIG` (`hình vẽ`), `BF-DFILTER` (`\bD\b.*lọc`), `BF-HOQ` (`HOQ`), `BF-REDFLAG` (`🔴`), `BF-PROVISIONAL` (`D/W tạm`), `BF-CHECKLIST14` (`14 mục`), `BF-LINT` (`p3_form_lint\.py`), `BF-TESTPLAN` (`Kế hoạch thử`), `BF-LABELS` (`tri thức.*phỏng đoán.*giả định`), `BF-BOOKS` (`TKHT.*TKKTHT.*KL9`). Chạy `bash evals/run-eval.sh helix-p3-form` → FAIL (skill chưa có).
- [ ] **Step 2:** Viết SKILL.md.
- [ ] **Step 3:** `bash evals/run-eval.sh helix-p3-form` → mọi required PASS. Đột biến: xoá câu khớp từng regex → assert đỏ → khôi phục.
- [ ] **Step 4:** Commit `[HELIX] helix-p3-form: khối BF chức năng → hình thể`.

### Task 9: Nối BF vào P3 + tài liệu

**Files:**
- Modify: `skills/helix/helix-embody-realize/SKILL.md` (sơ đồ §Pipeline Architecture, bảng Sub-Skills, `_pipeline_state` Block Progress thêm dòng `| BF | helix-p3-form | PENDING | - | - | - |` sau B0, Data Bus thêm 5 tệp BF + đổi dòng `CC2_Handoff` thành «BF hoặc /helix-cc2», cờ `--skip-form "<lý do>"` ghi Adjustments Log, `--quick` = BF quick, `--from/--only BF`, Integration)
- Modify: `skills/helix/helix-p3-preflight/SKILL.md` (xuất mục «Yêu cầu quyết định hiện thân» dạng bảng `| Req-ID | Chức năng (F-id) | Lý do |` cho BF đọc)
- Modify: `skills/helix/helix-p3-layout/SKILL.md` (đọc `BF_Form_Selection.md` = nguồn khoảng tham số; đổi khoảng → quay lại BF; giữ nguyên mục CC2_Handoff cũ)
- Modify: `skills/helix/helix-p3-compile/SKILL.md` (kiểm layout ↔ hình thể chọn; in lý do `--skip-form`; còn `D/W tạm` → không khuyến nghị qua Gate 3)
- Modify: `evals/helix-embody-realize.json` (thêm assert `P3-BF` regex `helix-p3-form`)
- Modify: `docs/HELIX_Architecture.md`, `CLAUDE.md` (dòng `helix/` thêm «P3 có khối BF helix-p3-form: chức năng→hình thể C&C² + 3 sách + đối chiếu giải pháp hiện có»; số đếm helix +1), `docs/SYSTEM_OVERVIEW.md` nếu liệt kê khối P3

- [ ] **Step 1:** Thêm assert `P3-BF` vào `evals/helix-embody-realize.json`; chạy `bash evals/run-eval.sh helix-embody-realize` → FAIL đúng assert đó.
- [ ] **Step 2:** Sửa các tệp trên.
- [ ] **Step 3:** `bash evals/run-eval.sh helix-embody-realize` → PASS toàn bộ (không assert cũ nào đỏ). `bash setup.sh --status` trong worktree đếm thêm 1 skill helix.
- [ ] **Step 4:** `python -X utf8 -m pytest scripts/test_p3_form_ref_check.py scripts/test_p3_form_lint.py scripts/test_cc2_skill_consistency.py -v` → PASS.
- [ ] **Step 5:** Commit `[HELIX] Nối khối BF vào P3 (embody-realize, preflight, layout, compile) + docs`.

### Task 10: Chạy thử nghiệm thu — VN-TGT-F `--variant TGT-10`

Ghi vào vault `D:/Workshop_X/1_Projects/VN-TGT-F/Phase3-Embodiment/TGT-10/` (ngoài repo). Skill chưa deploy qua junction (nằm trên worktree) → chạy bằng cách đọc trực tiếp `D:/KN-Stack-wt-p3form/skills/helix/helix-p3-form/SKILL.md`, lint gọi từ worktree.

- [ ] **Step 1:** Kiểm thư mục `Phase3-Embodiment/TGT-10/` chưa có tệp trùng tên (đọc trước khi ghi). Chạy B0 rồi BF đến Cổng 1: trình danh sách chức năng + D/W tạm. **CEO quyết (Core).**
- [ ] **Step 2:** Chạy F2–F6; `python -X utf8 D:/KN-Stack-wt-p3form/scripts/p3_form_lint.py <dir> --prefix VN_TGT_F_TGT10_` → exit 0. Tự mở 3 nguồn web/sáng chế ngẫu nhiên trong `BF_Benchmark.md` để xác nhận tồn tại và đúng nội dung (báo cáo tác tử không phải bằng chứng).
- [ ] **Step 3:** Cổng 2: CEO chọn hình thể (ghi bằng TÊN phương án). Kiểm câu nghiệm thu spec §12: CEO quyết được «nhận va chạm đầu đạn» và «giữ nổi thẳng đứng» không cần hỏi lại. Ghi kết quả + chỗ hụt vào `<scratchpad>/BF_pilot_findings.md`; sửa SKILL/references nếu có, commit `[HELIX] helix-p3-form: vá sau chạy thử TGT-10`.

### Task 11: PR

- [ ] **Step 1:** `python -X utf8 -m pytest scripts/test_p3_form_ref_check.py scripts/test_p3_form_lint.py -v` và `bash evals/run-eval.sh helix-p3-form && bash evals/run-eval.sh helix-embody-realize` → PASS (theo quy tắc «ALWAYS run tests before PR»).
- [ ] **Step 2:** `git push -u origin feature/helix-p3-form`; `gh pr create --base feature/evals-static-mode` với mô tả có `## CHANGELOG` (khối BF, 6 references, 2 script, sửa 4 khối P3, eval) và kết `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
- [ ] **Step 3:** Ghi memory dự án (trạng thái PR, đường dẫn worktree, bài học chạy thử).
