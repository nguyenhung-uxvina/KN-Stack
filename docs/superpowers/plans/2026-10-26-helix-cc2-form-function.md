# helix-cc2 — Bộ skill phân tích ⇄ tổng hợp chức năng–hình thể · Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Dựng `helix-cc2` (orchestrator, 4 chế độ) + 7 khối skill. Bộ skill đi từ chức năng có thông số → ≥3 chuỗi C&C² → hình thể → bảng tham số → phiếu giả thuyết 9 mục + kế hoạch thử → bàn giao P3, cộng thêm chiều phân tích độc lập.

**Architecture:** Skill markdown theo khuôn pipeline HELIX (orchestrator + khối chạy riêng được, data bus qua tệp). Có một nhà chính tài liệu dùng chung ở `skills/helix/helix-cc2/references/`, nạp bằng tên skill. Có hai script Python làm **cơ chế chặn**: lint phiếu/bảng, và kiểm nguồn trích của references so với sách. Kèm test pytest nhất quán và eval static.

**Tech Stack:** Markdown SKILL.md · Python 3 stdlib + pytest · bash `setup.sh` / `evals/run-eval.sh`.

**Spec:** `docs/superpowers/specs/2026-10-26-helix-cc2-form-function-design.md`. Đọc §2–§9. §8–§9 thắng các chỗ khác.

## Global Constraints

- Nhánh `feature/helix-cc2-form-function`, worktree `D:\KN-Stack-wt-cc2`, tách từ `feature/evals-static-mode`. Không làm trên cây chính (cây chính bẩn, có việc dở của người khác).
- Commit `[HELIX] …`, kết bằng `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. **Không** sửa `VERSION`, `CHANGELOG.md`, `scripts/_codify_ledger.md`.
- Mỗi SKILL.md mở bằng frontmatter `name:` (= tên thư mục) + `description:` có `Triggers on:` tiếng Anh + tiếng Việt.
- Không có đường dẫn `../` giữa các skill. Tài liệu dùng chung gọi bằng `helix-cc2:references:<tên>`, kèm đường dẫn tuyệt đối dự phòng `~/.claude/commands/helix-cc2/references/<tên>.md`.
- Nguồn tri thức: CC = `D:\Workshop_X\3_Resources\Books\cc2-gia-thuyet-ket-cau\book.md`, TK = `D:\Workshop_X\3_Resources\Books\thiet-ke-hien-than\book.md`. Cách trích: `(CC Ch04 §04.3)` / `(TK Ch06)`. Trích nguyên văn đặt trong «…».
- **Cấm** đọc hay đưa cho tác tử con bất kỳ tệp nào dưới `D:\Workshop_X\1_Projects\`. Ví dụ trong skill dùng cơ cấu công khai. Ví dụ quang→điện chỉ ở mức nguyên lý (rào sáng xuyên / phản xạ / bóng đổ lên mảng), không có số.
- Tiếng Việt cho nội dung skill, tiếng Anh cho mã và tên hàm. Đơn vị mét hệ.
- Grep tiếng Việt: luôn `LC_ALL=C.UTF-8`. Python: mở tệp `encoding='utf-8'`.

## Review Focus

1. Phiếu viết bằng dấu gạch khác (`-`, `–`, `—`) hay thụt lề khác khuôn ⇒ lint phải vẫn nhận ra phiếu, không im lặng bỏ qua. Test: `test_lint_nhan_phieu_voi_gach_khac`.
2. Tệp không có phiếu nào ⇒ lint phải **báo lỗi**, không trả ĐẠT. Kiểu cổng câm này đã gặp với fidelity_audit. Test: `test_lint_tep_rong_la_loi`.
3. Ngày ký dự đoán bằng ngày thử, hoặc thiếu ngày thử ⇒ phải chặn (luật: ký **trước**). Test: `test_lint_du_doan_cung_ngay_thu`.
4. Trích «…» trong references bị sửa một chữ so với sách ⇒ kiểm nguồn phải bắt. Dùng đối chứng âm: một câu bịa đuôi phải FAIL (bài học «đuôi bịa»). Test: `test_trich_duoi_bia_bi_bat`.
5. Máy không có thư mục sách (CI, máy khác) ⇒ test kiểm nguồn phải `skip` có lý do, không FAIL, không PASS giả. Test: `test_khong_co_sach_thi_skip`.

---

### Task 1: Worktree + commit spec/plan

**Files:** spec + plan này (copy vào worktree).

- [ ] **Step 1:** `git worktree add D:/KN-Stack-wt-cc2 -b feature/helix-cc2-form-function feature/evals-static-mode`
- [ ] **Step 2:** Copy `docs/superpowers/specs/2026-10-26-helix-cc2-form-function-design.md` và tệp plan này từ cây chính sang worktree, cùng đường dẫn. Kiểm: `git -C D:/KN-Stack-wt-cc2 status --short` chỉ thấy 2 tệp đó.
- [ ] **Step 3:** Commit `[HELIX] helix-cc2: spec + plan`. Xong thì **xoá** 2 bản chưa track ở cây chính (bản gốc đã vào nhánh).

---

### Task 2: `cc2_sheet_lint.py` — lint phiếu giả thuyết và bảng tham số

**Files:**
- Create: `scripts/cc2_sheet_lint.py`
- Test: `scripts/test_cc2_sheet_lint.py`

**Interfaces — Produces:**
- `parse_sheets(text: str) -> list[dict]`. Mỗi dict: `{'id': 'GT-001', 'items': {1: str, …, 9: str}, 'line': int}`. Phiếu bắt đầu ở dòng khớp `^PHIẾU GIẢ THUYẾT\s*[—–-]\s*(GT-\d{3})`. Mục là dòng `^\s*([1-9])\s+(.+)` cho tới phiếu kế tiếp hoặc fence ``` đóng.
- `lint_sheets(text: str, today: str | None = None) -> list[Finding]` với `Finding = namedtuple('Finding', 'sheet line code msg')`.
- `lint_param_table(text: str) -> list[Finding]`. Đọc mọi bảng markdown có cột tiêu đề `Nhãn` và `Nguồn số`.
- CLI: `python scripts/cc2_sheet_lint.py <tệp.md> --kind hypo|params`. In mỗi finding một dòng `GT-001:L12 CODE msg`. Exit 0 khi sạch, 1 khi có finding, 2 khi lỗi đọc tệp.
- Mã lỗi (cố định, các task sau trích):
  `NO_SHEETS` · `MISSING_ITEM` (mục 1–9 thiếu/trống; riêng mục 6 được để `{{điền SAU}}`) · `EFFECT_IN_IF` (mục 2 chứa từ tác dụng) · `IF_MULTI_VAR` (mục 2 có >1 dấu `=`) · `NO_BECAUSE` (mục 4 trống/placeholder) · `PRED_UNSIGNED` (mục 7 thiếu `người ký <tên>` hoặc `ngày YYYY-MM-DD`) · `PRED_NOT_BEFORE_TEST` (ngày mục 7 ≥ `ngày thử: YYYY-MM-DD` ở mục 5, hoặc mục 5 thiếu ngày thử) · `LABEL_MISSING` (bảng: ô `Nhãn` không thuộc {tri thức, phỏng đoán, giả định}) · `SOURCE_MISSING` (ô `Nguồn số` không bắt đầu bằng `đo được` / `suy ra (từ` / `chưa biết`) · `KNOWLEDGE_NO_EVIDENCE` (Nhãn = tri thức mà `Nguồn số` = `chưa biết`).
- Hằng `EFFECT_WORDS = ('ma sát', 'mòn', 'mài mòn', 'tín hiệu', 'nhiễu', 'độ bền', 'rò', 'lỏng', 'friction', 'wear')`, so khớp không phân biệt hoa thường. Đây là danh sách khởi đầu theo CC:2818, người xây được thêm.

- [ ] **Step 1: Viết test hỏng.** Fixture `PHIEU_TOT`: một phiếu GT-001 đủ 9 mục, mục 2 `NẾU: chiều rộng khe w = 3 mm | Đối chứng: w = 6 mm`, mục 5 có `ngày thử: 2026-11-10`, mục 7 `người ký CEO — ngày 2026-11-01`. Các test:
  - `test_phieu_tot_sach`: `lint_sheets(PHIEU_TOT) == []`
  - `test_lint_tep_rong_la_loi`: `[f.code for f in lint_sheets("# không có gì")] == ['NO_SHEETS']`
  - `test_thieu_muc_4`: bỏ dòng `4 …` ⇒ có `MISSING_ITEM`
  - `test_tac_dung_o_neu`: mục 2 `NẾU: ma sát giảm` ⇒ có `EFFECT_IN_IF`
  - `test_hai_bien`: mục 2 `NẾU: w = 3 mm, d = 20 mm` ⇒ có `IF_MULTI_VAR`
  - `test_lint_du_doan_cung_ngay_thu`: ngày mục 7 = `2026-11-10` ⇒ có `PRED_NOT_BEFORE_TEST`; bỏ `ngày thử` khỏi mục 5 ⇒ cũng có
  - `test_du_doan_khong_ky`: mục 7 không có `người ký` ⇒ có `PRED_UNSIGNED`
  - `test_lint_nhan_phieu_voi_gach_khac`: tiêu đề dùng `-` và `–`, mục thụt 2 dấu cách ⇒ `parse_sheets` trả 1 phiếu đủ 9 mục
  - `test_bang_thieu_nhan`: bảng `| Tham số | Nhãn | Nguồn số |` có một dòng Nhãn trống ⇒ `LABEL_MISSING`
  - `test_tri_thuc_chua_biet`: Nhãn `tri thức`, Nguồn `chưa biết` ⇒ `KNOWLEDGE_NO_EVIDENCE`
  - `test_cli_exit_code`: chạy subprocess trên tệp tạm sạch ⇒ exit 0; tệp rỗng ⇒ exit 1
- [ ] **Step 2:** `python -m pytest scripts/test_cc2_sheet_lint.py -v` ⇒ FAIL (`ModuleNotFoundError`).
- [ ] **Step 3:** Cài `scripts/cc2_sheet_lint.py` theo Interfaces. Chỉ dùng stdlib (`re`, `argparse`, `datetime`, `collections`).
- [ ] **Step 4:** Chạy lại test ⇒ PASS hết.
- [ ] **Step 5:** Commit `[HELIX] cc2_sheet_lint: chan phieu gia thuyet va bang tham so thieu nhan`.

---

### Task 3: References dùng chung + `cc2_ref_check.py` kiểm nguồn

**Files:**
- Create: `skills/helix/helix-cc2/references/{cc2-core,view-ops,synthesis-moves,embodiment-rules,param-bridge,hypothesis-sheet,multidomain}.md`
- Create: `scripts/cc2_ref_check.py`
- Test: `scripts/test_cc2_ref_check.py`

**Interfaces — Produces:**
- `check_refs(ref_dir: str, books: dict[str, str]) -> list[Finding]`. `books = {'CC': path, 'TK': path}`. `Finding(file, line, code, msg)`. Mã: `CHAPTER_NOT_FOUND` (trích `(CC Ch04 …)` mà book.md không có tiêu đề chương 04) · `QUOTE_NOT_FOUND` (đoạn «…» ≥ 8 từ không có nguyên văn trong sách nguồn mà dòng đó trích; so sau khi chuẩn hoá khoảng trắng + NFC, **giữ dấu**) · `NO_CITATION` (tệp reference có < 5 trích nguồn).
- CLI: `python scripts/cc2_ref_check.py skills/helix/helix-cc2/references`. Đường dẫn sách lấy từ env `CC2_BOOK_CC` / `CC2_BOOK_TK`, mặc định là hai đường dẫn trong Global Constraints. Exit 0/1, exit 3 = thiếu sách (in rõ «không có sách — không kiểm được», **không** in ĐẠT).
- Nội dung bắt buộc của từng tệp (các task sau và eval dựa vào đúng các tiêu đề này):
  - `cc2-core.md`: `## Từ vựng` (WFP, LSS, Connector, mặt biên, trạng thái logic) · `## Bảy bước dựng mô hình` · `## Giới hạn dùng và bằng chứng` (có câu: bằng chứng hiệu quả C&C² yếu, đọc như kỷ luật tư duy chứ không như phương pháp đã chứng minh) · `## Phạm vi cứng` (chức năng quyết định giải pháp + ≤3 chức năng tới hạn; ba ô sàng `dựng C&C²` / `chỉ bảng tham số` / `không áp dụng`) · `## Hai loại nhãn` (tri thức/phỏng đoán/giả định; đo được/suy ra (từ …)/chưa biết).
  - `view-ops.md`: mỗi phép một mục `### zoom-in` · `### zoom-out` · `### shift` · `### state` · `### view` · `### observe`. Mỗi mục có ba dòng `Khi nào:` (câu hỏi kích hoạt), `Làm gì với mô hình:`, `Dấu hiệu dùng sai:`. Thêm `## Rào cản quan sát` là bảng rào cản (quá nhanh, quá chậm, bị che, quá nhỏ/quá lớn, sai góc nhìn, ngoài biên) → phép/phương tiện phá.
  - `synthesis-moves.md`: các nước đi thêm/bớt/tách/gộp WFP, đổi LSS, dời Connector, đổi trạng thái, đổi miền. Mỗi nước đi có ví dụ cơ cấu công khai.
  - `embodiment-rules.md`: bảng `| Quy tắc | Câu hỏi kiểm hình thể | Tham số bị khoá | Nguồn |`, ≥1 dòng cho mỗi chương TK Ch04–Ch16.
  - `param-bridge.md`: WSPO/WSPA, tham số vs tác dụng, độ nhạy, dải đã kiểm. Có khuôn bảng C3 với đúng các cột `| Phần tử | Tham số hình thể | Thông số chức năng | Chiều ảnh hưởng | Ước lượng | Khoảng chọn | Nhãn | Nguồn số |`.
  - `hypothesis-sheet.md`: khuôn phiếu 9 mục **đúng định dạng `parse_sheets` của Task 2** (tiêu đề `PHIẾU GIẢ THUYẾT — GT-{{nnn}}`, mục 5 có `ngày thử:`, mục 7 có `người ký … — ngày …`). Kèm điều kiện hợp lệ, khuôn kế hoạch thử trên bàn thử (đại lượng mục tiêu, đối chứng, đổi một biến, dải, người đọc kết quả ≠ người lập), định tuyến độ tin × tầm ảnh hưởng. Có một **phiếu mẫu đã điền** (cơ cấu công khai) trong fence ```text.
  - `multidomain.md`: chỗ C&C² còn dùng được cho quang/điện/phần mềm, chỗ phải dừng, câu khuôn `C&C²: không áp dụng, vì …`.

- [ ] **Step 1: Viết test hỏng** cho `cc2_ref_check.py`, dùng sách giả trong `tmp_path`: `book.md` có `## Chương 04 …` và câu «Shift dời trọng tâm từ WFP1 sang WFP2 theo câu hỏi».
  - `test_trich_dung_qua`: ref có `«Shift dời trọng tâm từ WFP1 sang WFP2 theo câu hỏi» (CC Ch04)` ⇒ không finding
  - `test_trich_duoi_bia_bi_bat`: cùng câu nhưng đuôi đổi thành `… sang WFP2 theo mọi trường hợp` ⇒ `QUOTE_NOT_FOUND`
  - `test_chuong_khong_co`: `(CC Ch99)` ⇒ `CHAPTER_NOT_FOUND`
  - `test_it_trich`: tệp chỉ 2 trích ⇒ `NO_CITATION`
  - `test_khong_co_sach_thi_skip`: CLI với env trỏ đường dẫn không tồn tại ⇒ exit 3, stdout không chứa `ĐẠT`
  - `test_refs_that` (`pytest.mark.skipif` khi không có sách thật): `check_refs` trên `skills/helix/helix-cc2/references` với sách thật ⇒ `[]`
  - `test_phieu_mau_qua_lint`: lấy fence ```text trong `hypothesis-sheet.md`, chạy `lint_sheets` (Task 2) ⇒ `[]`. Bài kiểm đi hai chiều: khuôn trong reference và parser phải khớp nhau.
- [ ] **Step 2:** Chạy ⇒ FAIL.
- [ ] **Step 3:** Cài `cc2_ref_check.py`. Chuẩn hoá khoảng trắng + NFC, **không** bỏ dấu (`quote_locate.py` từng xoá chữ có dấu).
- [ ] **Step 4: Rút 7 references từ sách.** Đọc đúng chương thật trong CC/TK: CC Ch02, Ch04, Ch05, Ch06, Ch08–Ch11, Ch13–Ch15; TK Ch04–Ch16. Viết lại bằng lời mình. Mỗi quy tắc một trích nguồn. Nếu giao tác tử con đọc chương: chỉ đưa đường dẫn sách + danh sách tiêu đề bắt buộc ở trên, **không** đưa gì từ `1_Projects`.
- [ ] **Step 5:** `python -m pytest scripts/test_cc2_ref_check.py -v` ⇒ PASS, gồm cả `test_refs_that` trên máy này. Thêm: `python scripts/cc2_ref_check.py skills/helix/helix-cc2/references` ⇒ exit 0. Báo cáo của tác tử không tính, phải là output của lệnh này.
- [ ] **Step 6:** Commit `[HELIX] helix-cc2: references rut tu CC/TK + cong kiem nguon`.

---

### Task 4: Orchestrator `helix-cc2` + test nhất quán

**Files:**
- Create: `skills/helix/helix-cc2/SKILL.md`
- Test: `scripts/test_cc2_skill_consistency.py`

**Interfaces — Produces (các khối sau phải khớp):**
- Chế độ: `--project <đường dẫn dự án>`, `--function "<câu>"`, `--improve <hình thể> "<chức năng mới>"`, `--analyze <hình thể>`. Cờ phụ: `--out <thư mục>`, `--from <khối>`, `--only <khối>`, `--op <phép> <đích>`.
- `--op` nhận đúng 6 phép: `zoom-in`, `zoom-out`, `shift`, `state`, `view`, `observe`. Đích theo cú pháp `<chuỗi>[:<phần tử>[→<phần tử>]]`, ví dụ `B:WFP2`, `B:WFP1→WFP2`. Mỗi phép tạo phiên bản chuỗi mới `B.1`, `B.2`… và một dòng trong mục `## Nhật ký phép biến đổi` của `_pipeline_state.md`.
- Bảng **Data Bus** (mục `## Data Bus`), mỗi dòng `| Tệp | Ghi bởi | Đọc bởi |`. Tên tệp cố định: `{{prefix}}CC2_C0_Frame.md` (C0), `{{prefix}}CC2_C1_Chains.md` (C1), `{{prefix}}CC2_C2_Forms.md` (C2), `{{prefix}}CC2_C3_Params.md` (C3), `{{prefix}}CC2_C4_Hypotheses.md` + `{{prefix}}CC2_C4_Test_Plan.md` (C4), `{{prefix}}CC2_CA_Analysis.md` (CA), `{{prefix}}CC2_C6_Crosscheck.md` + `{{prefix}}CC2_Handoff.md` (C6), `_pipeline_state.md` (orchestrator).
- Nơi ghi theo spec §8 R4: `--out`, nếu không có thì `Phase3-Embodiment/CC2/` (trong dự án), nếu không thì `./_cc2/<slug>/`. `{{prefix}}` = tiền tố dự án/biến thể hoặc `<slug>_`.
- Luồng bốn chế độ đúng spec §5 + §8 R4. Có ba cổng CEO: duyệt danh sách sàng C0 (chế độ dự án) · chọn chuỗi sau C1 · ký dự đoán sau C4.
- Phải có: câu cảnh báo bằng chứng yếu ở đầu phiên (trỏ `cc2-core.md` §Giới hạn dùng) · bảng COD (dựng nháp = Offload; chọn chuỗi, ký dự đoán, duyệt bàn giao = Core) · mục `READS FROM` / `WRITES TO` · luật cấm đọc `1_Projects` có IP để lấy ví dụ.

- [ ] **Step 1: Viết test hỏng** `test_cc2_skill_consistency.py`:
  - `test_frontmatter`: với mọi `skills/helix/helix-cc2*/SKILL.md`: `name:` = tên thư mục; `description:` chứa `Triggers on:` và ít nhất một ký tự tiếng Việt có dấu
  - `test_du_bon_che_do`: SKILL.md của orchestrator chứa đủ 4 cờ chế độ
  - `test_op_khop_view_ops`: tập phép trong mục `--op` của orchestrator == tập tiêu đề `### …` trong `view-ops.md` == {zoom-in, zoom-out, shift, state, view, observe}
  - `test_data_bus_khop_khoi`: mỗi tệp trong Data Bus xuất hiện trong SKILL.md của khối ghi nó. Task 4 chỉ kiểm phía orchestrator; vòng kiểm khối được thêm ở Task 5–7, đánh dấu `xfail(strict=True)` cho tới khi khối tồn tại
  - `test_khong_duong_dan_cheo`: không SKILL.md/references nào chứa `../`
  - `test_khong_tro_1_projects`: không tệp nào trong `skills/helix/helix-cc2*` chứa `1_Projects/` ngoài luật cấm
- [ ] **Step 2:** Chạy ⇒ FAIL.
- [ ] **Step 3:** Viết `skills/helix/helix-cc2/SKILL.md` theo Interfaces. Khuôn tham khảo là `skills/helix/helix-embody-realize/SKILL.md` (Parse Arguments → Input Validation → Pipeline State → chạy từng khối một → Completion), nhưng gọn hơn.
- [ ] **Step 4:** Chạy ⇒ PASS (các xfail vẫn xfail).
- [ ] **Step 5:** Commit `[HELIX] helix-cc2: orchestrator 4 che do + phep bien doi giua phien`.

---

### Task 5: Khối C0 `helix-cc2-frame` + C1 `helix-cc2-chain`

**Files:** Create `skills/helix/helix-cc2-frame/SKILL.md`, `skills/helix/helix-cc2-chain/SKILL.md`. Modify `scripts/test_cc2_skill_consistency.py` (bỏ xfail cho C0/C1, thêm test dưới đây).

**Interfaces — Consumes:** tên tệp Data Bus (Task 4), `cc2-core.md`, `synthesis-moves.md`, `view-ops.md`, `multidomain.md` (Task 3).
**Produces:**
- `CC2_C0_Frame.md` có các mục: `## Chức năng` · `## Thông số chức năng` (bảng có cột `Nhãn`, `Nguồn số`, đúng luật lint Task 2) · `## Connector biên` · `## Nguyên lý` (`đã nêu: …` hoặc `chưa nêu` + `miền ứng viên`) · `## Sàng chức năng con` (chỉ chế độ dự án: bảng ba ô, mỗi dòng một lý do) · `## Hình thể hiện có` (chỉ `--improve`: trỏ `CC2_CA_Analysis.md`).
- C0 đọc ở chế độ dự án: `Function_Structure.md`, `Requirements_List_v*.md`; nếu có thì thêm `Concept_Selection.md`, `Morphological_Matrix.md` (glob như `helix-embody-realize` Step 1.5a).
- `CC2_C1_Chains.md`: ≥3 chuỗi đặt tên `A`, `B`, `C`…. Mỗi chuỗi có: sơ đồ Mermaid `flowchart LR` WFP/LSS/Connector · bảng phần tử · trạng thái logic · mặt biên · dòng `Vì sao chuỗi này hợp thông số C0:` có nhãn. Khi nguyên lý `chưa nêu`: ≥2 miền vật lý khác nhau. Khi có P2: chuỗi lệch P2 ghi `lệch P2 — CEO quyết`. `--improve`: có một chuỗi `sửa tối thiểu`. Cuối tệp có khối `## Phép nên làm tiếp` (1–3 dòng `phép · đích · câu hỏi kích hoạt`).
- C1 ghi rõ: đề xuất đa miền là nguồn ý, không phải quyết định concept; không dựng ma trận hình thái, không chấm DSO/VDI 2225.

- [ ] **Step 1: Test hỏng:** `test_c0_c1_tieu_de` (SKILL.md của C0 nêu đủ 6 mục tiêu đề trên; C1 nêu `≥3`, `≥2 miền`, `lệch P2`, `sửa tối thiểu`, `## Phép nên làm tiếp`, `Mermaid`); `test_c1_khong_lan_p2` (C1 chứa `không dựng ma trận hình thái`).
- [ ] **Step 2:** Chạy ⇒ FAIL.
- [ ] **Step 3:** Viết 2 SKILL.md. Mỗi khối có mục `## Chạy riêng` (cờ, đầu vào tối thiểu) và một ví dụ ngắn quang→điện ở mức nguyên lý: ba chuỗi rào sáng xuyên / phản xạ ngược / bóng đổ lên mảng thu, **không có số**.
- [ ] **Step 4:** Chạy ⇒ PASS.
- [ ] **Step 5:** Commit `[HELIX] helix-cc2: khoi C0 frame + C1 chain`.

---

### Task 6: Khối C2 `helix-cc2-form` + C3 `helix-cc2-param`

**Files:** Create `skills/helix/helix-cc2-form/SKILL.md`, `skills/helix/helix-cc2-param/SKILL.md`. Modify test nhất quán.

**Interfaces — Consumes:** `CC2_C1_Chains.md` (chuỗi CEO đã chọn, ghi trong `_pipeline_state.md`), `embodiment-rules.md`, `param-bridge.md`, `cc2_sheet_lint.py --kind params`.
**Produces:**
- `CC2_C2_Forms.md`: mỗi chuỗi đã chọn có 2–3 phương án `A-1`, `A-2`…. Mỗi phương án có: mô tả hình học bằng lời + phác Mermaid/ASCII · bảng `| Quy tắc TK | Câu hỏi kiểm | Kết quả | Nhãn |` lấy từ `embodiment-rules.md` · khối `## Phép nên làm tiếp`.
- `CC2_C3_Params.md`: một bảng C3 mỗi phương án, **đúng cột** của `param-bridge.md`. Đánh dấu ≤3 tham số `NHẠY` mỗi phương án. Ước lượng giải tích ghi `suy ra (từ <công thức/nguồn>)`.
- C3 kết thúc bằng lệnh bắt buộc `python scripts/cc2_sheet_lint.py <CC2_C3_Params.md> --kind params`. Exit ≠ 0 ⇒ không sang C4. Trong skill viết rõ: «báo cáo "đã kiểm" không thay output của lệnh».

- [ ] **Step 1: Test hỏng:** `test_c3_cot_khop_param_bridge` (tiêu đề cột trong ví dụ bảng của C3 SKILL.md == khuôn trong `param-bridge.md`); `test_c3_goi_lint` (C3 chứa `cc2_sheet_lint.py` và `--kind params`); `test_c2_tro_embodiment_rules`.
- [ ] **Step 2:** Chạy ⇒ FAIL.
- [ ] **Step 3:** Viết 2 SKILL.md.
- [ ] **Step 4:** Chạy ⇒ PASS.
- [ ] **Step 5:** Commit `[HELIX] helix-cc2: khoi C2 form + C3 param`.

---

### Task 7: Khối C4 `helix-cc2-hypo` + CA `helix-cc2-analyze`

**Files:** Create `skills/helix/helix-cc2-hypo/SKILL.md`, `skills/helix/helix-cc2-analyze/SKILL.md`. Modify test nhất quán.

**Interfaces — Consumes:** `CC2_C3_Params.md` (tham số `NHẠY`), `hypothesis-sheet.md`, `view-ops.md`, `cc2-core.md`, `multidomain.md`.
**Produces:**
- `CC2_C4_Hypotheses.md`: mỗi tham số `NHẠY` một phiếu theo khuôn `hypothesis-sheet.md`, kèm dòng `Phép thử nhỏ nhất để bác bỏ:`. Mục 7 để `người ký {{…}} — ngày {{…}}` cho CEO điền. Lint chạy **sau** khi CEO ký (cổng 3 của orchestrator).
- `CC2_C4_Test_Plan.md`: một hàng thử cho mỗi phiếu, xếp theo định tuyến độ tin × tầm ảnh hưởng.
- C4 kết bằng `python scripts/cc2_sheet_lint.py <CC2_C4_Hypotheses.md> --kind hypo`, exit 0 mới qua.
- CA nhận: bản vẽ / `cad_extract.json` (từ `helix-cad-ingest`) / ảnh / mô tả. Ghi `CC2_CA_Analysis.md` gồm: mô hình C&C² một trang (≤ 2 chức năng con chính + ≤ 3 tới hạn) · bảng `Vì sao hình học này` có nhãn · rào cản quan sát gặp phải + phép phá đề xuất · `## Phép nên làm tiếp` · giả thuyết nháp (khuôn 9 mục, có thể chuyển C4).
- CA phải chạy được **không cần** RE: không Purpose Gate, không ACCESS LEVEL. Có một câu: khi đích là sản phẩm của bên khác thì dùng `/reverse-engineering`.
- CA có chế độ `--crosscheck` cho C6: chỉ được đọc C0 + C2/C3 của phương án, **không** đọc C1 (người đọc ≠ người lập).

- [ ] **Step 1: Test hỏng:** `test_c4_goi_lint_hypo`; `test_c4_phep_thu_bac_bo` (chứa `Phép thử nhỏ nhất để bác bỏ`); `test_ca_khong_purpose_gate` (CA không chứa `ACCESS LEVEL` ngoài câu trỏ RE); `test_ca_crosscheck_khong_doc_c1` (mục `--crosscheck` liệt kê đầu vào không có `CC2_C1_Chains`).
- [ ] **Step 2:** Chạy ⇒ FAIL.
- [ ] **Step 3:** Viết 2 SKILL.md. Ví dụ CA dùng một cơ cấu công khai (ví dụ kẹp lò xo, mối vít), không dùng sản phẩm Xưởng.
- [ ] **Step 4:** Chạy ⇒ PASS.
- [ ] **Step 5:** Commit `[HELIX] helix-cc2: khoi C4 hypo + chieu phan tich CA doc lap`.

---

### Task 8: Khối C6 `helix-cc2-handoff` + sửa phía P3

**Files:**
- Create: `skills/helix/helix-cc2-handoff/SKILL.md`
- Modify: `skills/helix/helix-embody-realize/SKILL.md` (Step 1.5a RECOMMENDED INPUTS; mục `READS FROM` quanh dòng 439)
- Modify: `skills/helix/helix-p3-layout/SKILL.md` (thêm một mục ngắn)
- Modify: `scripts/test_cc2_skill_consistency.py` (bỏ hết xfail)

**Interfaces — Consumes:** mọi tệp C0–C4 + CA `--crosscheck`.
**Produces:**
- `CC2_C6_Crosscheck.md`: danh sách lệch. Mỗi chỗ lệch → phiếu mới (GT-nnn) hoặc dòng sửa C2. Đầu tệp ghi rõ `Mức đối chiếu: mô tả (chưa có hình học)`.
- `{{prefix}}CC2_Handoff.md`, **chỉ** khi có thư mục dự án, ghi vào `Phase3-Embodiment/` (hoặc thư mục biến thể). Các mục: `## Chuỗi đã chọn theo chức năng con` · `## Tham số hình thể và khoảng chọn` · `## Tham số nhạy` · `## Phiếu giả thuyết đang mở` · `## Kế hoạch thử` · `## Chỗ C&C² không áp dụng` · `## Vòng lặp P3` (khi BA/`helix-cad-bridge` có `cad_extract.json` ⇒ chạy `/helix-cc2 --analyze <cad_extract.json>` để đối chiếu mức hình học). Chế độ dự án gộp mọi chức năng con vào một tệp.
- Ngoài dự án: dừng ở Crosscheck + Test_Plan, in câu «không sinh bàn giao P3 vì không có thư mục dự án».
- Sửa `helix-embody-realize`: thêm `□ {{prefix}}CC2_Handoff.md → chuỗi C&C², khoảng tham số, phiếu mở (from /helix-cc2)` vào RECOMMENDED INPUTS, và `- helix-cc2 → CC2_Handoff (khoảng tham số, phiếu giả thuyết mở)` vào `READS FROM`.
- Sửa `helix-p3-layout`: mục `## Khi có CC2_Handoff.md`. Layout lấy khoảng tham số từ đó; muốn đổi khoảng thì phải mở hoặc sửa phiếu giả thuyết tương ứng, không tự chọn lại. Khi có hình học thì chạy vòng lặp P3.

- [ ] **Step 1: Test hỏng:** `test_handoff_hai_phia` (`CC2_Handoff` có trong C6, trong `helix-embody-realize` ở **cả** Step 1.5a lẫn `READS FROM`, và trong `helix-p3-layout`); `test_handoff_vong_lap_p3`; `test_handoff_chi_khi_co_du_an`; bỏ mọi `xfail` ⇒ `test_data_bus_khop_khoi` phải PASS thật.
- [ ] **Step 2:** Chạy ⇒ FAIL.
- [ ] **Step 3:** Viết C6, sửa 2 tệp P3. Chỉ thêm dòng, không viết lại đoạn có sẵn.
- [ ] **Step 4:** `python -m pytest scripts/test_cc2_skill_consistency.py scripts/test_cc2_sheet_lint.py scripts/test_cc2_ref_check.py -v` ⇒ PASS, không còn xfail.
- [ ] **Step 5:** Commit `[HELIX] helix-cc2: khoi C6 ban giao + hop dong hai phia voi P3`.

---

### Task 9: Eval + kiểm đột biến

**Files:** Create `evals/helix-cc2.json`, `evals/helix-cc2-analyze.json`.

- [ ] **Step 1:** `evals/helix-cc2.json`: `mode: "static"`, `include_references: true`. Assertion `required: true` (regex khớp tiêu đề/từ khoá có thật trong Task 3–8): `CC2-MODES` (4 cờ) · `CC2-CHAINS3` (`≥ ?3 chuỗi`) · `CC2-LABELS` (`tri thức.*phỏng đoán.*giả định`) · `CC2-SHEET9` (`PHIẾU GIẢ THUYẾT`) · `CC2-FALSIFY` (`Phép thử nhỏ nhất để bác bỏ`) · `CC2-VIEWOPS` (`zoom-in.*zoom-out.*shift`) · `CC2-OBSERVE` (`Rào cản quan sát`) · `CC2-HANDOFF` (`CC2_Handoff`) · `CC2-EVIDENCE` (`bằng chứng.*yếu`) · `CC2-SCOPE` (`≤ ?3 chức năng tới hạn`) · `CC2-LINT` (`cc2_sheet_lint`).
- [ ] **Step 2:** `bash evals/run-eval.sh helix-cc2` ⇒ mọi assertion PASS.
- [ ] **Step 3: Kiểm đột biến.** Với từng assertion: chép skill sang thư mục tạm, xoá **mọi dòng khớp chính regex của assertion đó** (không chọn tay), chạy lại eval trên bản chép ⇒ đúng assertion đó FAIL. Assertion nào vẫn PASS sau đột biến thì sửa regex. Ghi kết quả ra bảng trong mô tả PR.
- [ ] **Step 4:** `evals/helix-cc2-analyze.json`: `mode: "runtime"`. `test_input` là phân tích C&C² của một kẹp giấy lò xo bằng thép, chỉ cơ cấu công khai. Assertion: có WFP/LSS/Connector, có nhãn, có `Phép nên làm tiếp`. Chạy `bash evals/run-eval.sh helix-cc2-analyze` ⇒ PASS. Nếu môi trường không chạy được `claude -p`, ghi rõ «chưa chạy runtime» trong PR, không ghi PASS.
- [ ] **Step 5:** Commit `[HELIX] helix-cc2: eval static + runtime, kiem dot bien`.

---

### Task 10: Xác minh triển khai + PR

- [ ] **Step 1:** Trong worktree: `bash setup.sh --verify`. Kỳ vọng: 8 junction `helix-cc2*` resolve được. `bash setup.sh --status` thấy số skill helix tăng 8. Ghi số thật, không chép số cứng. **Lưu ý:** junction trỏ vào cây làm việc. Nếu `--install` trỏ sang worktree thì phải ghi rõ trong PR và trả junction về sau khi merge (bài học «commit việc chưa commit làm mất hiệu lực skill»).
- [ ] **Step 2:** `python -m pytest scripts/ -q` trên toàn bộ ⇒ không có test cũ nào mới hỏng. Nếu có test cũ vốn đã hỏng trên nhánh tích hợp: so với `git stash` / nhánh gốc, rồi ghi rõ.
- [ ] **Step 3:** Chạy thử một phiên khói: `/helix-cc2 --function "biến sự che khuất của đạn thành tín hiệu biên [quang→điện]" --out <scratchpad>` tới hết C1. Kiểm bằng mắt: ≥3 chuỗi, có Mermaid, có `Phép nên làm tiếp`. Đây chỉ là kiểm khói, ghi «chưa chạy trọn vòng tới C6» nếu đúng như vậy.
- [ ] **Step 4:** `git push -u origin feature/helix-cc2-form-function`; `gh pr create --base feature/evals-static-mode`. Mô tả PR có: tóm tắt · bảng kiểm đột biến · `## CHANGELOG` (đoạn để người merge dán, không ghi số phiên bản) · việc để sau (spec §7 bước 8: nối RE → `helix-cc2-analyze` + gỡ trùng `cc2-lens.md` sau khi `feature/design-re-v3.4-cc2` merge) · dòng `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
