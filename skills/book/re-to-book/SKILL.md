---
name: re-to-book
description: "Orchestrator dựng SÁCH SỐNG nội bộ từ hồ sơ /reverse-engineering (MECHA/TECH/COMPARE/FULL…) cho kỹ sư Workshop X. Adapter của notebook-to-book: P2–P9 giao nguyên cho các khối book-*; P0 gom hồ sơ RE thành dự án riêng, P0.5 manifest lọc bằng script (chặn Idea_Log, cổng pháp lý, dự đoán GT chưa ký), P1 đọc bản chụp RE thay cho truy vấn NLM và giữ nhãn tri thức + neo xuất xứ, P7 kiểm GT/nhãn/Idea_Log bằng script, P8 thay mã RE bằng «phân tích nội bộ». Khung 5 phần: Công nghệ · Kiến trúc · Cấu trúc · Sản phẩm · Chỗ chưa biết. Flags: --re <dir>[,<dir>…], --project <RE-project>, --sync (RE đổi ⇒ dò chương bị ảnh hưởng, viết lại cục bộ, nhật ký ấn bản), --gapfill (tìm thêm cho chỗ trống RE, ghi ngược vào hồ sơ RE chờ CEO duyệt), cùng các cờ của notebook-to-book (--from/--only, --quick, --no-nlm, --lang). Triggers on: 're to book', 'reverse engineering to book', 'sách từ hồ sơ RE', 'biến RE thành sách', 'rtb'."
---

# RE-to-Book — Orchestrator (sách sống từ hồ sơ RE)

> **Role:** Chỉ huy trưởng — dựng và giữ cập nhật một cuốn sách nội bộ từ hồ sơ `/reverse-engineering`
> **Parent:** Adapter của `/notebook-to-book` — P2–P6 và P7.5/P7.6/P8/P8.5/P9 giữ nguyên; P0, P0.5, P1, P7 thay; thêm `--sync`, `--gapfill`
> **Người đọc:** kỹ sư Workshop X. Thước thành công: đọc xong có cái nhìn **đầy đủ nhất, cập nhật nhất** về công nghệ, kiến trúc, cấu trúc và sản phẩm mà RE phân tích.
> **Ca đầu:** bia chấm điểm tự động ISSF 25/50 m — Megalink 3D-Score, Meyton MF6R3 (ESTA NX), SIUS LS25/50, `TECH_ISSF25_Optical`.
> **Spec:** `docs/superpowers/specs/2026-10-27-re-to-book-design.md` (CEO duyệt 2026-10-27)

**Nguyên tắc nền:** hồ sơ RE là **nguồn sự thật duy nhất**; sách chỉ đọc RE (qua bản chụp đã lọc). Mọi luật dưới đây là **một lệnh có mã thoát**, không phải lời nhắc — mã ≠ 0 ⇒ không trình checkpoint.

## Pipeline Architecture

```
/re-to-book --re <dir>[,<dir>...] [--project <RE-project>] [--sync] [--gapfill] [cờ notebook-to-book]

 P0   CONSOLIDATE  — re_consolidate.py plan → CEO duyệt → apply   (một lần / dự án RE; hoãn được)
 P0.5 SOURCE GATE  — re_manifest.py build → _re_manifest.json + _re_snapshot/ (đã lọc)
 P1   RE-EXPLORE   — index/gaps → P1.2 CEO duyệt cụm → fan-out đọc _re_snapshot/ → check-p1
 P2–P6             — /book-position · /book-outline · /book-write · /book-review · /book-revise
                     (+ brief bắt buộc: provenance.json, nhãn ⟨…⟩, hợp đồng nhà chính)
 P7   AUDIT (adapter RE) — re_book_audit.py all + Phase7-IdeaLog-Overlap.md + trang ⛔ Phạm vi lưu hành
 P7.5 EPUB · P7.6 bản đồ sách · P8 notebook (qua re_nlm_redact.py) · P8.5 audio · P9 CEO insight
                     — như /notebook-to-book

 --gapfill : _re_gaps.md → CEO chọn → tìm → RE/<hồ sơ>/RE_<SP>_Book_GapFill.md (chờ CEO duyệt)
 --sync    : build lại → diff → impact → CEO duyệt → P1 cục bộ → P4/P6 cục bộ → P7 → _editions.md

Data Bus: D:\Workshop_X\1_Projects\<RE-project>\Book\   (sách sống gắn với nguồn của nó)
State:    <Book>/_pipeline_state.md
Scripts:  RTB=<KN-Stack>/skills/book/re-to-book/scripts   — luôn gọi `python -X utf8 "$RTB/…"`
```

## Differences vs `notebook-to-book`

| Pha | notebook-to-book | re-to-book |
|---|---|---|
| P0 | — | Gom hồ sơ RE thành dự án `1_Projects/<RE-project>/` (`re_consolidate.py plan/apply`), CEO duyệt từng tệp sửa đường dẫn |
| P0.5 | — | Manifest + bản chụp lọc bằng script; tệp chưa xếp lớp ⇒ dừng hỏi CEO |
| P1 | NLM multi-query | Đọc `_re_snapshot/` theo cụm khung 5 phần; mỗi ý mang nhãn tri thức + neo xuất xứ; cổng `check-p1` |
| P4/P6 brief | chuẩn | + `ChNN.provenance.json`, nhãn hiển thị `⟨…⟩`, hợp đồng nhà chính trước fan-out |
| P7 | attribution + IP | + `re_book_audit.py all` (GT · nhãn · Idea_Log · neo còn sống) + bảng trùng Idea_Log + trang phạm vi mỗi ấn bản |
| P8 | tải `chunks/` | tải bản đã thay mã RE (`re_nlm_redact.py`); mã 1 ⇒ không tải |
| sync | — | `--sync`: diff manifest → chương bị ảnh hưởng → viết lại cục bộ → `_editions.md` |
| gapfill | — | `--gapfill`: tìm cho chỗ trống RE tự khai, **ghi ngược vào hồ sơ RE**, CEO duyệt |
| Data Bus | `3_Resources/Books/<slug>/` | `1_Projects/<RE-project>/Book/` |

## How to Use

```
/re-to-book --re "D:\Workshop_X\1_Projects\BB-02_LOMAH\RE\Megalink_3D-Score,...\TECH_ISSF25_Optical" --project RE-ISSF25-Scoring
/re-to-book --project RE-ISSF25-Scoring --sync        # sau bàn thử: ấn bản mới
/re-to-book --project RE-ISSF25-Scoring --gapfill     # tìm thêm cho chỗ trống RE
/re-to-book --project RE-ISSF25-Scoring --only P0     # chuyển hồ sơ (ca ISSF: sau bàn thử 2026-11-04, Q7)
/re-to-book --project RE-ISSF25-Scoring --from P4
```

---

## Orchestrator Workflow

### Step 1: Parse Arguments

```
--re <dir>[,<dir>...]   → thư mục hồ sơ RE (≥1). Tên thư mục = khoá neo, phải khác nhau.
                          Không có ⇒ đọc re_roots trong <Book>/_pipeline_state.md
--project <RE-project>  → dự án RE chứa Book/ (ca đầu: RE-ISSF25-Scoring — CEO đổi được)
--classes <json>        → bảng lớp riêng của dự án (mặc định $RTB/re_classes.json)
--sync | --gapfill      → hai chế độ riêng (xem dưới); không chạy cùng P0.5→P9 trong một lệnh
--from X | --only X     → P0, P0.5, P1…P9
--quick | --no-nlm | --no-audio | --lang vi|en | --audience → như notebook-to-book
```

### Step 1.5: Resolve Book + scope preview

- `Book = D:\Workshop_X\1_Projects\<RE-project>\Book\`. Chưa có vỏ dự án ⇒ đề xuất tạo `_Project_Brief.md` + `Status.md` (Tier 3) + `Book/`, **hỏi CEO trước khi tạo**. Ngoài vault ⇒ `<cwd>/book-output/<slug>/`.
- Đọc `Book/` trước khi ghi (một pipeline khác có thể đã ghi vào đó).
- Trình scope: danh sách hồ sơ `--re`, chúng nằm trong dự án RE hay chưa (⇒ hỏi chạy P0 ngay / **hoãn P0, đọc tại chỗ**), số ấn bản, ước tính chi phí. **Chờ CEO.**

---

## Đơn vị, nhãn tri thức, phiếu GT (định nghĩa dùng chung mọi pha)

**Mã đơn vị** (do `re_units.py` cắt; neo = `<thư mục hồ sơ>/<tệp>#<mã đơn vị>`, đường dẫn TƯƠNG ĐỐI theo tên hồ sơ — P0 chuyển chỗ không làm neo đổi):

| Đơn vị | Mã | Ví dụ neo |
|---|---|---|
| Mục phiếu giả thuyết | `GT-<id>.<n>` (`.0` tiêu đề, `.6` KẾT QUẢ, `.7` DỰ ĐOÁN VIẾT TRƯỚC) | `Megalink_3D-Score/RE_3DS_Hypotheses.md#GT-3DS-001.6` |
| Dòng bảng có mã ở cột đầu | `row:<mã>` | `…/RE_3DS_Precision_Debt.md#row:N-013` |
| Mục văn xuôi `##`/`###` | tiêu đề nguyên văn; trùng tên ⇒ `~2`, `~3` | `…/RE_3DS_S1A_Deconstruction.md#Khung chính` |
| Phần trước tiêu đề đầu | `_preamble` | |
| Tệp không có tiêu đề | `file` | |

**Phiếu GT (khuôn 9 mục RE v3.4):**
- `.7` **đã ký** = có «người ký» điền chữ **và** «ngày» chứa chữ số. Chưa ký ⇒ lớp CẮT: bản chụp hiện `⟨chờ ký⟩`, sách không được nêu số dự đoán.
- `.6` **trống** (`*(điền sau)*` hoặc rỗng) ⇒ bản chụp hiện `⟨chờ đo⟩`, sách viết «chờ đo», không viết số.
- Kết quả bàn thử CEO ghi vào **mục 6** của phiếu `## GT-…` trong hồ sơ RE — đó là thứ `--sync` thấy (mục 7 là dự đoán viết trước, không phải kết quả).

**Nhãn tri thức** (`re_labels.py`; manifest ghi `label`, `label_source`, `confidence`):

| Từ trong RE | Nhãn | Hiển thị trong sách |
|---|---|---|
| đã biết / tri thức / knowledge | `knowledge` | không cần nhãn |
| phỏng đoán / conjecture | `conjecture` | `⟨phỏng đoán⟩` |
| giả định / assumption | `assumption` | `⟨giả định⟩` |
| (không tìm thấy) | `chưa gán` | **không** viết như tri thức — xem P1.4 |
| GT `.6` trống · `.7` chưa ký · `.7` đã ký | — | `⟨chờ đo⟩` · `⟨chờ ký⟩` · `⟨dự đoán⟩` |

Luật kế thừa: nhãn tại chỗ (câu/ô) → tuyên bố cấp tệp («Mọi … ≤ phỏng đoán» — được kế thừa và **giới hạn** nhãn tại chỗ) → **nhãn yếu nhất thắng**. `confidence_ceiling` trong `_pipeline_state.md` của hồ sơ chỉ hạ **mức tin** (lấy chữ thấp nhất), **không bao giờ** tạo ra nhãn tri thức. Mức tin trong bảng chỉ đọc từ cột tiêu đề «Mức tin»/confidence.

---

## P0 — Consolidate (gom hồ sơ RE thành dự án riêng)

Chỉ chạy khi `--re` nằm ngoài một dự án RE; chạy lại là no-op. Ca ISSF: **sau bàn thử 2026-11-04** (Q7) — ấn bản 1 đọc tại chỗ cũ.

```bash
# 1. Kế hoạch — chỉ đọc, ghi plan JSON (đặt NGOÀI các thư mục sẽ chuyển)
python -X utf8 "$RTB/re_consolidate.py" plan \
  --src-root "D:/Workshop_X/1_Projects/BB-02_LOMAH/RE" --dossiers "<hồ sơ 1>,<hồ sơ 2>,..." \
  --dest-root "D:/Workshop_X/1_Projects/RE-ISSF25-Scoring/RE" \
  --scan "D:/Workshop_X/1_Projects/BB-02_LOMAH" --old-project BB-02_LOMAH \
  --new-project RE-ISSF25-Scoring --out "<Book>/_p0/plan_$(date +%Y-%m-%d_%H%M).json"
```

2. Trình CEO **nguyên văn** ba khối plan in ra: `Di chuyển` (kèm số tệp) · `Tự sửa được` (`auto_rewrites`, từng dòng −/+) · `Phải sửa tay` (`manual` — gồm tệp không giải mã được `⟨không đọc được: mã hoá⟩` và liên kết lồng). **Không chuyển khi chưa duyệt.** Không chuyển `Phase1-Task/V1/RE-Reference/` (hiện vật bàn giao HELIX) và `VnV/` (thuộc BB-02).
3. CEO duyệt **từng tệp** `auto_rewrites` ⇒
   ```bash
   python -X utf8 "$RTB/re_consolidate.py" apply --plan <plan.json> --approve "<tệp 1>,<tệp 2>"
   # --approve-all-auto CHỈ khi CEO nói rõ "duyệt hết"; --no-rewrite = chỉ chuyển, không sửa
   ```
   `apply` từ chối (mã 2) junction/symlink (kể cả lồng bên trong), plan cũ (`StalePlanError`), đích đã tồn tại; chỉ dùng rename; đếm tệp trước/sau (`CountMismatchError`); tự ghi `BB-02_LOMAH/RE/README.md` trỏ sang và sửa `project:` trong `_pipeline_state.md` của từng hồ sơ.
   **`PartialMoveError` ⇒ DỪNG**, trình CEO nguyên văn thông báo (nó liệt kê chính xác cái đã chuyển), không chạy lại, không tự dọn.
4. Dòng `manual`: sửa tay **sau khi** CEO duyệt từng dòng. Cập nhật `Status.md` hai dự án.
5. Cập nhật `re_roots` trong `<Book>/_pipeline_state.md` sang gốc mới; lần `--sync` kế tiếp phải báo `root_moved`, không phải xoá + thêm.
6. **B5 (bàn giao HELIX) sau khi chuyển** — dự án thiết kế vẫn nhận bàn giao:
   ```bash
   python -X utf8 scripts/re_handoff_to_helix.py --re-dir "<RE-ISSF25-Scoring>/RE/<hồ sơ>" --project-dir "<BB-02_LOMAH>"   # dry-run; --apply sau khi CEO duyệt
   ```

---

## P0.5 — Source Gate (manifest + bản chụp lọc)

```bash
python -X utf8 "$RTB/re_manifest.py" build --re "<dir1>,<dir2>,..." --book "<Book>" [--classes <project_classes.json>]
```

Ghi `<Book>/_re_manifest.json` (mỗi tệp: lớp, hash, mtime; mỗi đơn vị: hash, nhãn, mức tin, cắt/chờ đo; trường `created` = **ngày chụp manifest**) và `<Book>/_re_snapshot/` (chỉ lớp READ + CUT, đã thay dự đoán chưa ký/kết quả trống bằng `⟨chờ ký⟩`/`⟨chờ đo⟩`, đã bỏ mục GapFill chưa duyệt).

| Lớp | Tệp (`re_classes.json`) | Đi đâu |
|---|---|---|
| READ | `*_S0_Patent_CC2.md`, `*_S1A_*`, `*_S1B_*`, `*_S1C_*`, `*_S1M_*`, `*_S2B_*`, `*_S2M_*`, `TECH_T*.md`, `*_Precision_Debt.md`, GapFill **đã duyệt** | `_re_snapshot/` → P1 |
| CUT | `*_Hypotheses.md` | `_re_snapshot/` với `⟨chờ ký⟩` / `⟨chờ đo⟩` |
| BLOCK | `*_Idea_Log.md`, `*_S0_Legal_Gate.md`, `*BOM*`, `*.backup`, GapFill chưa duyệt | không vào bản chụp; chỉ đối chiếu ở P7 |
| DECISION | `_pipeline_state.md`, `*_S1_Source_Gate.md`, `_source/_ma_nguon.md` | chỉ cho `gaps` và P7 |
| SOURCE / IGNORE | `_source/*`, `_analysis/*`, `_source/video/*`, `*.json`, `*.py`, `*_out.txt` | chỉ băm (sync thấy đổi), không đọc |

- **Mã 2 kèm `Tep chua phan lop (N):`** (`UnclassifiedError`) ⇒ có tệp **chưa xếp lớp**; `build` không ghi gì. Trình CEO danh sách, CEO chọn lớp ⇒ thêm mẫu vào `re_classes.json` (khuôn chung) hoặc tệp lớp riêng của dự án truyền bằng `--classes`, rồi chạy lại. **Không tự đoán lớp.**
- Mã 2 khác (trùng tên hồ sơ, thiếu thư mục, lỗi đọc) ⇒ sửa đầu vào, chạy lại.
- **Tác tử viết CHỈ đọc `_re_snapshot/`, không bao giờ đọc thư mục RE gốc.** Brief của mọi tác tử P1/P4/P6 ghi đường dẫn `_re_snapshot/`, không ghi `--re`.

---

## P1 — RE-Explore (thay P1 NLM; đầu ra tương thích schema `book-explore`)

### P1.1 Bảng đơn vị + chỗ trống (script)
```bash
python -X utf8 "$RTB/re_manifest.py" index --book "<Book>"   # → Phase1-Exploration/_units_index.md (neo · lớp · nhãn · mức tin · 80 ký tự)
python -X utf8 "$RTB/re_manifest.py" gaps  --book "<Book>"   # → Phase1-Exploration/_re_gaps.md
```

### P1.2 CEO duyệt bảng cụm (checkpoint TRƯỚC fan-out)
Mặc định 5 cụm = khung 5 phần (spec §5, CEO duyệt "khung này đủ"):

| Cụm | Lấy chủ yếu từ |
|---|---|
| I. Công nghệ | `TECH_T1/T2/T3`, `S1C_Tolerance_Perf` |
| II. Kiến trúc | `S2B_Function_Structure`, `S2B_Solution_Det_SF`, `S2M` |
| III. Cấu trúc | `S1A_CC2_Models`, `S1B`, `S1C_Step_f` |
| IV. Sản phẩm | `S0_Patent_CC2`, `S1A_Deconstruction`, `S1A_Component_Inventory` (mỗi sản phẩm một chương) |
| V. Chỗ chưa biết | `Hypotheses`, `Precision_Debt` |

Trình bảng **tệp→cụm** đề xuất (từ `_units_index.md`). CEO: duyệt / gộp / thêm. **Chờ duyệt.**

### P1.3 Fan-out (một tác tử mỗi cụm, cùng một message)
Brief mỗi tác tử theo `references/p1-re-explore.md`: đọc `_units_index.md` + tệp trong `_re_snapshot/`; mỗi ý mang **nhãn + mức tin + neo**. **Neo đặt TRONG BACKTICK** (mã đơn vị có dấu cách): `` `Megalink_3D-Score/RE_3DS_Hypotheses.md#GT-3DS-001.6` `` — neo trần bị cắt ở dấu cách và hỏng cổng.

### P1.4 Tổng hợp — `Phase1-Exploration/P1_Synthesis.md`
Schema `book-explore` + hai mục bắt buộc:
- `## Chỗ trống RE tự khai` — gom từ `_re_gaps.md`: Precision_Debt, mâu thuẫn mở `N-xxx`, stage bỏ, sản phẩm/hãng chưa có hồ sơ. Đầu vào của `--gapfill`.
- `## Nhãn chưa gán cần quyết` — mọi neo `chưa gán` các cụm đã dùng làm nội dung. CEO quyết ở P1.5 (gán nhãn nào); chưa quyết ⇒ người viết hiện `⟨chưa gán nhãn⟩`, **không bao giờ** viết như tri thức.

### P1.5 Cổng + checkpoint
```bash
python -X utf8 "$RTB/re_provenance.py" check-p1 --book "<Book>"
python skills/book/codebase-to-book/scripts/databus_check.py "<Book>" --phase P1
```
`check-p1` mã ≠ 0 (cụm không có neo nào; neo sai dạng; tệp không có trong manifest; lớp không được neo; không có đơn vị) ⇒ **CẤM checkpoint** — sửa ghi chú, chạy lại. Checkpoint P1 nêu: số cụm, số neo, số neo `chưa gán`, `kiểm N phiếu GT`.

---

## P2–P6 — giao nguyên khối `book-*` (như notebook-to-book)

P2 `/book-position` (Core) · P3 `/book-outline` (Core — khung 5 phần là mặc định, dàn ý chi tiết CEO duyệt) · P4 `/book-write` · P5 `/book-review` · P6 `/book-revise`.

**Bổ sung bắt buộc vào brief P4 và P6:**
1. **Nguồn:** chỉ `Phase1-Exploration/` + `_re_snapshot/`. Không Idea_Log, không thư mục RE gốc.
2. **Provenance:** mỗi chương ghi tệp kèm **cạnh tệp chương**, tên = tên tệp chương bỏ `.md` + `.provenance.json`, trường `chapter` = đúng tên đó:
   ```json
   {"chapter": "Ch05_kien-truc_Draft", "sections": {"§05.2": ["Megalink_3D-Score/RE_3DS_S2B_Function_Structure.md#Cây SF"]}}
   ```
   Tiêu đề mục trong chương **chứa số mục** (`## 05.2 …`) để `labels` tìm được. P6 ghi lại tệp provenance cho `Phase6-Revised/Ch<NN>_<slug>_v2.md` (`"chapter": "Ch<NN>_<slug>_v2"`). Chương thiếu provenance = phát hiện. **Không** ghi neo bằng chú thích HTML trong thân (lọt vào EPUB).
3. **Nhãn hiển thị:** câu dựa trên ý `conjecture` ⇒ `⟨phỏng đoán⟩`; `assumption` ⇒ `⟨giả định⟩`; GT `.6` trống ⇒ `⟨chờ đo⟩`; dự đoán chưa ký ⇒ `⟨chờ ký⟩`, không số.
4. **Hợp đồng nhà chính** (khái niệm → chương sở hữu) ghi vào brief **trước khi** chia tác tử song song; không đính chính giữa đợt.

**Cổng trước checkpoint P4 và P6:**
```bash
python -X utf8 "$RTB/re_provenance.py" check --prov "<Book>/Phase4-Chapters" --book "<Book>"      # P6: --prov "<Book>/Phase6-Revised"
python -X utf8 "$RTB/re_book_audit.py" labels --book "<Book>" --stage P4                           # P6: --stage P6
python skills/book/codebase-to-book/scripts/databus_check.py "<Book>" --phase P4                  # P5 · P6 tương tự
```
Mã ≠ 0 ⇒ sửa chương/provenance trước, không trình checkpoint.

---

## P7 — Audit (adapter RE)

Chạy `/book-audit` ở attribution mode (như notebook-to-book) **và**:

```bash
# 1. Gợi ý trùng Idea_Log — chỉ từ vựng/số, KHÔNG chép nội dung Idea_Log
python -X utf8 "$RTB/re_book_audit.py" idea-candidates --book "<Book>" --re "<dir1>,<dir2>,..."
```
2. **Một lượt tác tử** điền `<Book>/Phase7-IdeaLog-Overlap.md`: bảng có cột `Mã` và `Kết luận`, **một dòng cho MỌI mã Idea_Log**, kết luận ∈ `trùng` / `không trùng` / `một phần` (+ vị trí chương/đoạn). Tác tử đọc Idea_Log chỉ để đối chiếu; bảng nêu mã + chỗ trong sách, không chép văn bản Idea_Log. Tệp này **không** vào `book.md`, không lên NLM.
3. Cổng tổng:
   ```bash
   python -X utf8 "$RTB/re_book_audit.py" all --book "<Book>" --re "<dir1>,<dir2>,..."
   ```
   Gồm `gt` (in `kiểm N phiếu GT (k chờ đo, m chờ ký)`; GT nhắc trong sách mà không có trong manifest; nhắc GT chưa đo thiếu `⟨chờ đo⟩`; nhắc dự đoán chưa ký thiếu `⟨chờ ký⟩`) · `labels` · `idea-coverage` · `provenance` (neo còn sống). **`re_book_audit.py all` mã ≠ 0 ⇒ CẤM trình IP sign-off.**
4. **CEO quyết giữ/bỏ** từng dòng `trùng`/`một phần` (Core, **mỗi ấn bản**). Không tự xoá — CEO K54 từng chọn giữ.
5. **Trang `# ⛔ Phạm vi lưu hành`** ở đầu `book.md` — trang này ghi **ngày chụp manifest** (`created` của `_re_manifest.json`), phạm vi NỘI BỘ, danh sách hồ sơ RE, số ấn bản, quyết định Idea_Log của CEO, dòng: *«Ch08b/08c sách K54 (`lomah-sung-ngan-k54`) là bản chụp 2026-10-26 của cùng hồ sơ; bản hiện hành là sách này.»* và dòng ký `CEO ký: ________ Ngày: ________`. **Đường ống không bao giờ điền chữ ký thay CEO.**
6. `databus_check.py "<Book>" --phase P7` rồi mới trình IP sign-off (Core).

---

## P7.5 · P7.6 · P8 · P8.5 · P9 — như `/notebook-to-book`

Theo đúng mục P7.5 (EPUB), P7.6 (bản đồ sách), P8 (`/book-notebook`), P8.5 (audio), P9 (`/book-ceo-insight`) trong `/notebook-to-book` — không chép lại. **Một thay đổi ở P8:** tải bản đã thay mã RE, không tải `chunks/` trực tiếp:

```bash
python -X utf8 "$RTB/re_nlm_redact.py" --book "<Book>" --src "<Book>/chunks" --out "<RE-project>/_nlm_upload/ed<N>"
```
`--out` phải nằm **ngoài** `<Book>` và `--src`. Mã 0 ⇒ tải từ `--out`. **Mã 1 (còn mã sót) ⇒ KHÔNG tải**; script đã xoá hẳn `--out` — **không bao giờ tải từ một `--out` cũ**; sửa nguồn rồi chạy lại. `book.md` trong máy giữ mã RE.

---

## `--gapfill` — tìm thêm cho chỗ trống RE, ghi ngược vào RE

1. Đọc `## Chỗ trống RE tự khai` (`P1_Synthesis.md`; làm mới bằng `re_manifest.py gaps`). Trình CEO: chỗ trống · kênh đề xuất (Exa / NLM / sổ tay hãng / sáng chế) · ước tính chi phí. **CEO chọn mục nào đi tìm.**
2. Tìm. Nguồn tải về lưu vào `RE/<hồ sơ>/_source/gapfill/<ngày>_<chủ đề>/` — **một thư mục mới cho mỗi lần tải** (tệp tải về không tin cậy; đọc bằng `python -I`).
3. Truy vấn NLM: áp **nguyên** cổng `0/0` từng truy vấn của `/notebook-to-book` (mục «ĐỌC TRƯỚC: … `0/0`», `-j`, `sources_used/references`) — trỏ, không chép. `0/0` ⇒ loại, không ghi vào GapFill.
4. Ghi `RE/<hồ sơ>/RE_<SP>_Book_GapFill.md` theo `references/gapfill-template.md` — frontmatter `status: chờ CEO duyệt`, mỗi mục `## GF-NNN` có dòng `**Trạng thái:** chờ CEO duyệt`. Chỗ trống liên miền (không thuộc một sản phẩm) ⇒ ghi vào hồ sơ **TECH**. **Không sửa tệp RE nào khác.**
5. CEO duyệt: cả tệp (`status: đã duyệt` ở frontmatter) hoặc từng mục (`**Trạng thái:** đã duyệt`). Không mục nào duyệt ⇒ manifest xếp lớp BLOCK. Đã duyệt ⇒ lớp READ ⇒ lần `--sync` sau đưa vào sách.

---

## `--sync` — sách sống

Điều kiện: ấn bản trước đã lưu `<Book>/_manifests/ed<N>.json` (bản sao `_re_manifest.json` lúc CEO ký phạm vi ấn bản N). Không có ⇒ HALT, không so được.

```bash
cp -r "<Book>/_re_snapshot/." "<Book>/_re_snapshot_$(date +%Y-%m-%d_%H%M)/"
cp -r "<Book>/Phase6-Revised/." "<Book>/Phase6-Revised_$(date +%Y-%m-%d_%H%M)/"
python -X utf8 "$RTB/re_manifest.py" build --re "<re_roots hiện hành>" --book "<Book>"
python -X utf8 "$RTB/re_manifest.py" diff --old "<Book>/_manifests/ed<N>.json" --new "<Book>/_re_manifest.json" --out "<Book>/_sync/ed<N+1>_diff.json"
python -X utf8 "$RTB/re_provenance.py" impact --prov "<Book>/Phase6-Revised" --diff "<Book>/_sync/ed<N+1>_diff.json" --out "<Book>/_sync/ed<N+1>_impact.json"
# --quick (không có Phase6): --prov "<Book>/Phase4-Chapters" và sao lưu Phase4-Chapters thay Phase6-Revised
```

Trình CEO bảng thay đổi (tệp RE · đơn vị · thêm/đổi/xoá · chương/mục bị ảnh hưởng), và **nêu riêng**:
- `root_moved` — gốc hồ sơ đổi chỗ (sau P0), báo riêng khỏi thay đổi nội dung;
- `status_changes` — `chờ đo → đã đo`, `chờ ký → đã ký`, kèm chương;
- `unanchored_new` — đơn vị mới chưa có neo ⇒ đề xuất chương nhận theo cụm P1;
- `sources_changed` — `_source/` đổi (PDF mới…).

Thay đổi cần chương mới hoặc đổi khung (vd. thêm hồ sơ Suooter) ⇒ **quay về P3**, CEO duyệt dàn ý. "Không đổi" chỉ được báo **kèm `compared_units`** (in sẵn ở dòng đầu của `diff`) — `compared_units: 0` là "không so được", không phải "không đổi".

CEO duyệt ⇒ P1 cục bộ (chỉ đơn vị đổi) → P4/P6 cục bộ cho mục bị ảnh hưởng (brief như trên) → P7 đầy đủ cho chương đổi → hợp `book.md` → P8 thay nguồn tương ứng. Cuối cùng ghi `<Book>/_editions.md`: ấn bản · ngày · ngày chụp manifest · đơn vị RE đổi · chương viết lại · GT đổi trạng thái · CEO ký phạm vi (để trống cho CEO). Sau khi CEO ký: `cp "<Book>/_re_manifest.json" "<Book>/_manifests/ed<N+1>.json"`.

Sách K54 (Ch08b/08c) **ngoài phạm vi sync** (Q9).

---

## Pipeline State Schema

```markdown
---
source_type: re-dossier
re_roots: ["D:/Workshop_X/1_Projects/BB-02_LOMAH/RE/<hồ sơ>", ...]   # P0 cập nhật
re_project: RE-ISSF25-Scoring
classes: {{$RTB/re_classes.json | <project_classes.json>}}
edition: {{N}}
manifest_created: {{created của _re_manifest.json}}
slug: {{slug}}
pipeline: re-to-book v1.0
started: {{today}}
updated: {{today}}
flags: {lang: vi, audience: engineer, quick: false, no_nlm: false}
---
```
Progress table + Block Ledger: như `codebase-to-book/_pipeline_state.md`.

## Data Bus — bổ sung so với notebook-to-book

| Tệp | Ghi bởi | Nội dung |
|---|---|---|
| `_re_manifest.json` · `_re_snapshot/` | P0.5 `build` | manifest + bản chụp lọc (nguồn duy nhất của tác tử viết) |
| `Phase1-Exploration/_units_index.md` · `_re_gaps.md` | P1 `index` · `gaps` | bảng đơn vị · chỗ trống RE tự khai |
| `Phase4-Chapters/*.provenance.json` · `Phase6-Revised/*.provenance.json` | P4 · P6 | mục sách → neo |
| `Phase7-IdeaLog-Overlap.md` | P7 | gợi ý (script) + bảng kết luận mọi mã Idea_Log |
| `_manifests/ed<N>.json` · `_sync/` · `_editions.md` | sync | manifest mỗi ấn bản · diff/impact · nhật ký ấn bản |
| `_p0/plan_*.json` | P0 | kế hoạch chuyển |

---

## Rules

- **⛔ ONE BLOCK PER TURN — STOP AND WAIT** — #1 rule. Không bao giờ chạy 2+ blocks trong 1 turn.
- **⛔ CỔNG DATA BUS — không có hiện vật thì KHÔNG được báo xong.** Trước mỗi CEO checkpoint, chạy:
  ```bash
  python skills/book/codebase-to-book/scripts/databus_check.py <output_dir> --phase P5
  ```
  **Mã thoát != 0 ⇒ CẤM trình checkpoint.** Làm ra hiện vật trước. (Lý do: xem `/notebook-to-book` — lần chạy `pahl-beitz-tap2` báo P5/P6/P8 xong mà không có file nào.)
- **⛔ Sao lưu theo mốc phải có TÊN KHÁC NHAU — kèm GIỜ, không chỉ ngày.** `cp -r <nguon>/. "<dich>_$(date +%Y-%m-%d_%H%M)/"`. Bắt buộc trước mọi lần `build` lại và mọi lần viết lại Phase6 khi sync.
- **CEO checkpoints**: Không auto-continue. Minimal checkpoint nếu CEO nói "chạy hết" (1-line + "tiếp?").
- **Mọi cổng script mã ≠ 0 ⇒ cấm checkpoint**: `build` (P0.5) · `check-p1` (P1) · `check` + `labels` (P4/P6) · `re_book_audit.py all` (P7) · `re_nlm_redact.py` (P8).
- **Hồ sơ RE là READ-ONLY** — ngoại lệ duy nhất: tệp `RE_<SP>_Book_GapFill.md` + `_source/gapfill/` (`--gapfill`) và việc chuyển/sửa đường dẫn đã duyệt (P0).
- **Không tự đoán**: lớp tệp (P0.5), nhãn `chưa gán` (P1), kết luận Idea_Log (P7) — đều trình CEO.
- **Không điền chữ ký thay CEO** — trang phạm vi, `_editions.md`, GapFill `đã duyệt`, GT mục 7.
- **Báo cáo của tác tử không phải bằng chứng** — kiểm hiện vật bằng lệnh, không bằng lời tác tử.
- **Đối chứng âm trước khi tin cổng** (spec §6): lần chạy thật đầu tiên của mỗi sách, cho mỗi cổng một ca phải bị chặn (neo trần có dấu cách cho `check-p1`; mục `conjecture` thiếu `⟨phỏng đoán⟩` cho `labels`) ⇒ phải mã 1, rồi gỡ ca đó.

---

## COD Classification

- P0 duyệt danh sách chuyển + từng tệp sửa đường dẫn: **Core (C)**
- P0.5 xếp lớp tệp chưa xếp lớp: **Core (C)** (script dừng, CEO chọn)
- P1.2 bảng cụm: **Core (C)** · fan-out đọc + tổng hợp: Offload (O2)
- P1.5 quyết nhãn `chưa gán`: **Core (C)**
- P2 thesis · P3 dàn ý: **Core (C)**
- P4–P6 viết/rà/sửa: Offload (O2)
- P7 IP sign-off + giữ/bỏ ý trùng Idea_Log: **Core (C)**, mỗi ấn bản
- Ký trang phạm vi mỗi ấn bản: **Core (C)**
- `--gapfill` chọn chỗ trống + duyệt GapFill: **Core (C)** · tìm và ghi nháp: Offload (O2)
- `--sync` duyệt bảng thay đổi / quay P3: **Core (C)** · build/diff/impact: Default (D — script)

---

## Integration

```
re-to-book READS:   hồ sơ /reverse-engineering (qua _re_snapshot/ do re_manifest.py build sinh)
re-to-book RUNS:    $RTB/re_manifest.py (build|diff|gaps|index) · re_provenance.py (check|impact|check-p1)
                    re_book_audit.py (gt|labels|idea-candidates|idea-coverage|all) · re_nlm_redact.py
                    re_consolidate.py (plan|apply) · codebase-to-book/scripts/databus_check.py
                    scripts/re_handoff_to_helix.py --project-dir (B5 sau P0)
re-to-book DELEGATES: /book-position (P2) · /book-outline (P3) · /book-write (P4) · /book-review (P5)
                    /book-revise (P6) · /book-audit (P7) · /md-to-epub (P7.5) · /book-map (P7.6)
                    /book-notebook (P8) · /book-ceo-insight (P9)
re-to-book INHERITS từ /notebook-to-book: Rules, P7.5/P7.6/P8/P8.5, cổng NLM 0/0 (cho --gapfill)
re-to-book WRITES:  <RE-project>/Book/** · RE/<hồ sơ>/RE_<SP>_Book_GapFill.md + _source/gapfill/ (--gapfill)
                    <RE-project>/_nlm_upload/ (P8) · NotebookLM: 1 notebook sách (P8)
UPSTREAM:           /reverse-engineering (RE v3.4) — chạy stage RE ở đó, không ở đây
```
