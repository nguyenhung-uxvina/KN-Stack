---
created: 2026-10-27
updated: 2026-10-27
type: design
status: approved — CEO duyệt 2026-10-27
---

# `/re-to-book` — Sách sống dựng từ hồ sơ Reverse-Engineering

> Thiết kế workflow mới trong `skills/book/`. Thừa hưởng kiến trúc `/notebook-to-book` (P2→P9 giao
> nguyên cho các khối `book-*`), nhưng **nguồn là hồ sơ `/reverse-engineering`**, và sách **sống** —
> tự cập nhật khi hồ sơ RE đổi.

## 1. Mục đích và lý do

**Người đọc:** kỹ sư Workshop X (nội bộ).

**Thước thành công (lời CEO):** đọc xong, kỹ sư có **cái nhìn đầy đủ nhất, cập nhật nhất** về
**công nghệ, kiến trúc, cấu trúc và sản phẩm** mà RE được giao phân tích.

**Ca chạy đầu tiên:** ba hồ sơ RE sản phẩm của bia bắn súng chấm điểm tự động ISSF 25/50 m —
Meyton MF6R3 (phần mềm ESTA NX), SIUS LS25/50, Megalink 3D-Score — cùng hồ sơ TECH
`TECH_ISSF25_Optical` (4 hãng, 3 họ kiến trúc). Hiện nằm ở `D:\Workshop_X\1_Projects\BB-02_LOMAH\RE\`.

**Vì sao cần workflow riêng, không dùng `/notebook-to-book`:**
- Hồ sơ RE là tệp markdown có cấu trúc cố định (Stage 0/1/2, tiền tố `RE_<SP>_`, `_pipeline_state.md`),
  có **nhãn tri thức** (knowledge / conjecture / assumption) và **mức tin** (L/M/H theo ACCESS LEVEL).
  Hỏi qua NLM làm mất cả hai và thêm rủi ro `0/0`-bịa đã đo (~27%).
- Hồ sơ RE **chứa thứ không được lên sách**: Idea_Log (ý của Xưởng, ngoài clean-room), dự đoán
  bàn thử chưa ký, bàn luận pháp lý nội bộ, BOM.
- Hồ sơ RE **còn đang đổi** (bàn thử 2026-11-04 cho GT-001 / GT-LS-001 / GT-3DS-001; mâu thuẫn
  N-013 mở; Suooter chưa có hồ sơ riêng). Sách một lần chụp sẽ cũ ngay tuần sau.

**Tiền lệ đã chạy tay:** P10 của sách K54 (`3_Resources/Books/lomah-sung-ngan-k54/`, Ch08b/08c,
2026-10-26) đã lấy chính các hồ sơ này làm nguồn. Workflow này biến các bài học của lượt đó thành
**cơ chế** (xem §7).

## 2. Mục tiêu · Không phải mục tiêu · Phản mục tiêu

**Mục tiêu**
1. Một lệnh dựng sách hoàn chỉnh từ ≥1 thư mục RE (bất kỳ mode: MECHA/TECH/COMPARE/FULL…).
2. Sách phủ đủ bốn tầng (khung §5) và mang nhãn tri thức của RE tới người đọc.
3. `--sync`: phát hiện thay đổi trong hồ sơ RE, chỉ viết lại các chương bị ảnh hưởng, ghi nhật ký ấn bản.
4. `--gapfill`: tự tìm thêm (Exa / NLM / sổ tay hãng) cho chỗ trống của RE, **ghi ngược vào hồ sơ RE**.
5. Dùng chung cho miền khác về sau (UUV, mìn…); BB-02 chỉ là ca đầu.

**Không phải mục tiêu**
- Không thay `/reverse-engineering`. Không chạy stage RE nào, không sửa phân tích RE (trừ tệp GapFill).
- Không xuất bản ra ngoài. Phạm vi mặc định NỘI BỘ.
- Không tự quyết việc bảo hộ / tính mới của ý Xưởng.

**Phản mục tiêu (chạy được nhưng vẫn là thất bại)**
- Sách viết phỏng đoán RE như dữ kiện (mất nhãn tri thức).
- Ý trong Idea_Log lọt vào sách **mà CEO không biết** (lặp lỗi K54 P10).
- Dự đoán bàn thử chưa ký, hoặc ô kết quả chưa đo, xuất hiện như đã có số.
- Sách và hồ sơ RE nói khác nhau về cùng một điều (hai nguồn sự thật).
- Sync âm thầm viết lại chương mà không ai duyệt, hoặc báo "không đổi" khi RE đã đổi.

## 3. Quyết định của CEO (2026-10-27, ghi bằng lời)

| # | Câu hỏi | CEO chọn |
|---|---|---|
| Q1 | Sách cập nhật kiểu nào | **Sách sống** — RE đổi thì dò chương bị ảnh hưởng và viết lại cục bộ |
| Q2 | Chỗ trống của RE | **Được tự tìm thêm** |
| Q3 | Kết quả tìm thêm nằm đâu | **Ghi ngược vào hồ sơ RE** (tệp GapFill, CEO duyệt) — RE là nguồn sự thật duy nhất; sách chỉ đọc RE |
| Q4 | Tổ chức hồ sơ | **Gom kết quả RE thành một dự án riêng trong `1_Projects/`**, tách khỏi BB-02 |
| Q5 | Chuyển hay sao | **Chuyển hẳn**; BB-02 giữ README trỏ sang; đường dẫn tham chiếu được cập nhật sau khi CEO duyệt danh sách |
| Q6 | Khung sách | **Khung 5 phần (§5) — "khung này đủ"** |
| Q7 | Chuyển hồ sơ RE khi nào | **Sau bàn thử 2026-11-04** |
| Q8 | Phạm vi việc lần này | **Dựng skill rồi chạy luôn ấn bản 1 cho bia ISSF, sau đó sync một lần khi có kết quả 04/11** |
| Q9 | Sách K54 (Ch08b/08c viết từ cùng hồ sơ) | **Giữ nguyên làm bản chụp 2026-10-26** — ngoài phạm vi sync |

### Trình tự giao hàng (hệ quả của Q7 + Q8)

```
1. Dựng skill /re-to-book (SKILL.md + scripts + eval static)          ← trước 2026-11-04
2. Tạo vỏ dự án RE-ISSF25-Scoring (_Project_Brief, Status, Book/)     ← chưa chuyển RE
3. Ấn bản 1: P0.5 → P9, ĐỌC hồ sơ tại chỗ cũ BB-02_LOMAH/RE/           ← trước 2026-11-04
4. Bàn thử 2026-11-04 (BB-02) — CEO ghi kết quả vào mục 6 phiếu GT
5. P0: chuyển hồ sơ RE sang RE-ISSF25-Scoring/RE/ (CEO duyệt danh sách)
6. --sync lần 1 ⇒ ấn bản 2 (kết quả bàn thử vào Phần V)
```

Hệ quả thiết kế bắt buộc: **manifest và neo xuất xứ dùng đường dẫn TƯƠNG ĐỐI theo tên thư mục hồ sơ RE**
(`Megalink_3D-Score/RE_3DS_Hypotheses.md#GT-3DS-001.6`), không dùng đường dẫn tuyệt đối — để việc chuyển ở
bước 5 không làm sync bước 6 coi mọi mục là "xoá + thêm". Gốc hồ sơ RE là một tham số (`--re`) ghi trong
`_pipeline_state.md` của sách; P0 cập nhật tham số này. Sync phải phân biệt "gốc đổi chỗ" với "nội dung đổi"
và báo riêng.

Ấn bản 1 chạy trên hồ sơ đang được phiên khác ghi ⇒ ghi rõ ngày chụp manifest trong trang phạm vi.

**K54:** không sửa. Trang phạm vi của sách mới ghi một dòng: Ch08b/08c sách K54 là bản chụp 2026-10-26
của cùng hồ sơ; bản hiện hành là sách này.

## 4. Kiến trúc

```
/re-to-book --re <dir>[,<dir>...] [--project <RE-project>] [--sync] [--gapfill] [flags notebook-to-book]

 P0  CONSOLIDATE (một lần / mỗi dự án RE) — đề xuất chuyển, CEO duyệt, chuyển, sửa tham chiếu
 P0.5 SOURCE GATE  — lập manifest: tệp/mục nào được đọc, tệp nào chặn; băm từng mục
 P1  RE-EXPLORE    — thay P1 NLM: đọc tệp RE theo manifest, rút ý + nhãn tri thức + neo xuất xứ
 P2–P6             — giao nguyên `book-position/outline/write/review/revise` (như notebook-to-book)
 P7  AUDIT (adapter RE) — IP + quét trùng Idea_Log + dự đoán chưa ký + đổi mã RE cho bản NLM
 P7.5/P7.6/P8/P8.5/P9 — như notebook-to-book

 --gapfill : đọc chỗ trống RE tự khai → tìm thêm → ghi RE_<SP>_Book_GapFill.md + _source/ → CEO duyệt
 --sync    : băm lại manifest → diff → chương bị ảnh hưởng → P4→P7 cục bộ → nhật ký ấn bản
```

Một khối mỗi lượt, CEO checkpoint giữa các pha — **giữ nguyên luật của `/notebook-to-book`**
(ONE BLOCK PER TURN, cổng `databus_check.py`, sao lưu theo mốc có giờ, v.v.).

### 4.1 P0 — Gom thành dự án RE riêng

- Tạo `D:\Workshop_X\1_Projects\<RE-project>\` với `_Project_Brief.md` + `Status.md` (Tier 3).
  Tên đề xuất cho ca đầu: `RE-ISSF25-Scoring` *(quyết định của Claude — CEO đổi được)*.
- Cấu trúc:
  ```
  <RE-project>/
    _Project_Brief.md, Status.md
    RE/<các thư mục RE chuyển sang, giữ nguyên tên và nội dung>
    Book/                 ← data bus của sách (thay cho 3_Resources/Books/<slug>/)
  ```
  *(Đặt sách trong dự án thay vì `3_Resources/Books/` là quyết định của Claude: sách sống gắn với
  nguồn của nó.)*
- Trình tự (mỗi bước dừng cho CEO):
  1. Liệt kê thư mục RE sẽ chuyển + **mọi tệp ngoài thư mục RE có trỏ vào chúng** (grep đường dẫn
     tương đối và tuyệt đối, cả dạng `\` và `/`, cả `.md/.py/.json`). Ca BB-02 đã thấy:
     `Phase1-Task/V1/BB02_V1_Function_Structure.md`, `…/BB02_V1_Handoff_RE_to_HELIX.md`,
     hai tệp trong `Phase1-Task/V1/RE-Reference/`, `Status.md`, `VnV/GT-001_Ban_Thu_BOM.md`,
     `VnV/GT-001_Bench/README.md`, `VnV/GT-001_Bench/run_config_gt3ds001_template.json`.
     Đường dẫn chéo giữa các thư mục RE (`../TECH_ISSF25_Optical/_source/`) giữ nguyên vì chuyển cùng nhau.
  2. CEO duyệt danh sách. **Không chuyển khi chưa duyệt** (luật toàn cục: không move khi chưa hỏi).
  3. Kiểm thư mục cha không phải symlink/junction (memory `feedback_windows_symlink_check`); chuyển;
     đếm tệp trước/sau bằng máy, phải bằng nhau.
  4. Sửa các đường dẫn đã duyệt; ghi `BB-02_LOMAH/RE/README.md` trỏ sang dự án mới.
  5. Cập nhật `project:` trong `_pipeline_state.md` của từng thư mục RE và `Status.md` của cả hai dự án.
- **Không chuyển:** bản sao `Phase1-Task/V1/RE-Reference/` (là hiện vật bàn giao HELIX của BB-02, không phải nguồn) và gói bàn thử `VnV/` (thuộc BB-02).
- **Luồng kết quả bàn thử sau khi chuyển:** bàn thử vẫn chạy ở BB-02; kết quả GT được CEO ghi vào
  **mục 6 «KẾT QUẢ + khuyến nghị»** của phiếu `## GT-…` trong `RE_<SP>_Hypotheses.md` **trong dự án RE** —
  đó là thứ `--sync` sẽ thấy. (Mục 7 là dự đoán viết trước, không phải kết quả.)
- **Công cụ RE sau khi chuyển** *(quyết định của Claude)*: `scripts/re_handoff_to_helix.py` (B5) hiện giả định
  `1_Projects/{project}/RE/{product}/` và ghi vào `{project}/Phase1-Task/`. Thêm tham số dự án nhận bàn giao
  (`--handoff-project BB-02_LOMAH`) để B5 vẫn ghi vào Phase1-Task của dự án thiết kế. Đây là sửa công cụ, không
  sửa phân tích RE.
- P0 chỉ chạy khi `--re` trỏ vào thư mục RE nằm ngoài một dự án RE; chạy lại là no-op.

### 4.2 P0.5 — Source Gate (manifest)

Sinh `Book/_re_manifest.json` bằng script (không bằng lời nhắc). Với mỗi tệp RE:

| Lớp | Tệp | Xử lý |
|---|---|---|
| ĐỌC | S0_Patent_CC2, S1A_*, S1B, S1C_*, S1M, S2B_*, S2M, TECH_T1/T2/T3, Precision_Debt, Hypotheses (trừ mục dự đoán chưa ký), `_source/` công khai, GapFill **đã duyệt** | vào P1 |
| CHẶN | `*_Idea_Log.md`, `*_S0_Legal_Gate.md`, BOM/giá, `*.backup`, GapFill **chưa duyệt** | không đưa cho tác tử viết; chỉ dùng để **đối chiếu** ở P7 |
| CẮT | Hypotheses: dự đoán GT chưa có chữ ký và ô kết quả trống | thay bằng nhãn "chờ ký / chờ đo"; giữ khung giả thuyết |
| ĐỌC-QUYẾT ĐỊNH | `_pipeline_state.md`, `*_S1_Source_Gate.md`, `_source/_ma_nguon.md` | không vào thân sách; chỉ lấy danh sách việc mở / stage bỏ / bảng mã nguồn cho `## Chỗ trống RE tự khai` và cho P7 kiểm trích |
| BỎ QUA | `_analysis/*.py`, `*_out.txt`, `_source/video/*` (mp4, khung cắt), `*.json` cấu hình | không đọc; vẫn băm vào danh mục `_source/` để sync thấy đổi |

**Định nghĩa trên phiếu giả thuyết** (khuôn 9 mục của RE v3.4):
- *Dự đoán đã ký* = mục 7 có cả «người ký» lẫn «ngày» khác `___`. Chưa ký ⇒ CẮT. Đã ký ⇒ được vào sách, gắn nhãn «dự đoán».
- *Kết quả trống* = mục 6 là `*(điền sau)*` hoặc rỗng ⇒ sách viết «chờ đo», không viết số.
- *Chờ đo → đã đo* (sync) = mục 6 chuyển từ trống sang có nội dung.

**Đơn vị băm** *(quyết định của Claude, thay cho «mục `##`» cứng)*: đơn vị nhỏ nhất có nhận diện ổn định —
phiếu `## GT-…` tách tiếp theo mục đánh số 1–9; bảng (Precision_Debt, Component_Inventory…) băm **theo dòng**
có mã ở cột đầu (N-xxx, C-x…); mục `##`/`###` cho văn xuôi; tệp không có tiêu đề ⇒ băm cả tệp. Neo xuất xứ
dùng cùng nhận diện: `<tệp>#<tiêu đề>` · `<tệp>#<GT-id>.<mục>` · `<tệp>#row:<mã>` · `<tệp>#file`.

- Tệp không thuộc bảng ⇒ script **dừng và hỏi CEO** xếp lớp, không tự đoán. Bảng mặc định trên đủ phủ
  khuôn RE v3.4 nên lần chạy đầu không dừng hàng loạt.
- Bảng lớp là cấu hình (`references/re-source-classes.md` hoặc tương đương), để miền khác chỉnh được.
- Đường đọc hồ sơ RE **đang được phiên khác ghi**: manifest ghi mtime + hash tại thời điểm đọc; sync sau sẽ bắt phần đổi.

### 4.3 P1 — RE-Explore (thay P1 NLM)

- Đầu vào: manifest lớp ĐỌC. Đầu ra **tương thích schema `book-explore`** để P2+ không biết nguồn là RE:
  `Book/Phase1-Exploration/<cụm>_Exploration.md` + `P1_Synthesis.md`.
- Cụm = theo bốn tầng + "chỗ chưa biết" (khung §5), không theo tệp RE. Ánh xạ tệp→cụm là bảng
  đề xuất, CEO duyệt ở checkpoint P1.2 (như notebook-to-book).
- Mỗi ý rút ra mang ba thứ:
  1. **Nhãn tri thức** lấy từ RE + mức tin L/M/H. Bảng từ vựng cố định *(quyết định của Claude)*:
     «đã biết / tri thức» → knowledge · «phỏng đoán» → conjecture · «giả định» → assumption.
     Thứ tự kế thừa: nhãn tại chỗ (ô bảng, câu) → tuyên bố cấp tệp («mọi phần tử ≤ phỏng đoán») →
     trần mức tin theo miền trong `_pipeline_state.md` (`confidence_ceiling`). Nhãn kế thừa ghi kèm
     nguồn kế thừa (`kế thừa: tệp` / `kế thừa: trần miền`) và không bao giờ cao hơn trần miền.
     Không tìm được ở cả ba tầng ⇒ `chưa gán` (không tự gán).
  2. **Neo xuất xứ** `RE/<thư mục>/<tệp>#<tiêu đề mục>` + hash mục.
  3. **Mã nguồn công khai** nếu ý dựa trên tài liệu ngoài (sáng chế, sổ tay) — để P7 kiểm trích.
- Thêm mục `## Chỗ trống RE tự khai` trong `P1_Synthesis.md`: gom Precision_Debt, mâu thuẫn mở
  (N-xxx), stage bỏ (D2), sản phẩm/hãng chưa có hồ sơ. Đây là đầu vào của `--gapfill`.

### 4.4 P2–P6

Giao nguyên khối `book-*`. Bổ sung bắt buộc vào brief P4/P6:
- Mọi câu mang nội dung từ ý `conjecture/assumption` phải hiện nhãn cho người đọc thấy
  (dạng hiển thị do builder chọn; yêu cầu là người đọc phân biệt được).
- Mỗi chương ghi tệp kèm `Book/Phase4-Chapters/ChNN.provenance.json`: danh sách mục sách (`§NN.x`)
  → danh sách neo xuất xứ đã dùng. **Không** ghi neo bằng chú thích HTML trong thân chương
  (chú thích lọt vào EPUB — bẫy `chu thich an` của P7.5).
- Ghi "nhà chính" của từng khái niệm trong hợp đồng sửa **trước khi** chia tác tử song song
  (memory `feedback_nha_chinh_hai_chieu_roi_noi_dung`).

### 4.5 P7 — Audit (adapter RE)

Giữ attribution mode của notebook-to-book, thêm bốn kiểm bằng script:
1. **Quét trùng Idea_Log**: so từng chương với mọi `*_Idea_Log.md` (lớp CHẶN, chỉ đối chiếu) →
   bảng "ý trong sách ↔ mục Idea_Log". **Trình CEO, không tự xoá** — CEO K54 đã chọn giữ; đó là quyết định Core mỗi ấn bản.
2. **Dự đoán / kết quả chưa có**: chặn mọi số dự đoán GT chưa ký và mọi câu nói kết quả bàn thử khi ô kết quả trống.
3. **Nhãn tri thức**: mọi mục sách có neo tới ý `conjecture/assumption` mà thân không hiện nhãn ⇒ báo.
4. **Neo còn sống**: mọi neo trong `*.provenance.json` phải trỏ tới mục còn tồn tại trong manifest hiện hành.

Bản cho NLM (P8): đổi mã RE (`RE_3DS_…`, `N-013`, `GT-…`) thành "phân tích nội bộ" bằng script
(tiền lệ `_tools/p8_ban_nlm.py` của K54). Bản trong máy giữ mã.

Trang `# ⛔ Phạm vi lưu hành` trong thân sách, CEO ký **mỗi ấn bản** (như K54).

### 4.6 `--gapfill`

1. Đọc `## Chỗ trống RE tự khai`. Trình CEO danh sách chỗ trống + đề xuất kênh tìm (Exa / NLM /
   sổ tay hãng / sáng chế) + ước tính chi phí. CEO chọn mục nào đi tìm.
2. Tìm; lưu nguồn tải được vào `RE/<thư mục>/_source/gapfill/` (thư mục riêng cho mỗi lần tải, theo luật
   tệp tải về không tin cậy).
3. Ghi `RE/<thư mục>/RE_<SP>_Book_GapFill.md`: mỗi mục = chỗ trống nào · tìm thấy gì · nguồn · nhãn tri
   thức đề xuất · mức tin đề xuất. Frontmatter `status: chờ CEO duyệt`.
   Chỗ trống liên miền (không thuộc một sản phẩm) ⇒ ghi vào thư mục TECH.
4. Không sửa tệp RE nào khác. CEO duyệt (đổi `status: đã duyệt`, có thể duyệt từng mục) ⇒ manifest
   xếp lớp ĐỌC ⇒ lần `--sync` sau đưa vào sách.
5. Áp nguyên các cổng NLM đã đo (gate `0/0` từng truy vấn, `-j`, `sources_used/references`).

### 4.7 `--sync`

1. Sinh manifest mới, so với manifest của ấn bản trước → danh sách mục RE **thêm / đổi / xoá**.
2. Tra ngược qua `*.provenance.json` → chương và mục sách bị ảnh hưởng. Mục RE **mới** chưa có neo
   nào ⇒ xếp theo cụm P1 → đề xuất chương nhận.
3. Trình CEO: bảng thay đổi (tệp RE · mục · loại · chương bị ảnh hưởng). Đặc biệt nêu riêng:
   - giả thuyết đổi trạng thái (chờ đo → đã đo; dự đoán được ký);
   - thay đổi cần chương mới hoặc đổi khung (vd. thêm hồ sơ Suooter) ⇒ **quay về P3, CEO duyệt
     dàn ý**, không tự chạy.
4. CEO duyệt ⇒ chạy P1 cục bộ (chỉ mục đổi) → P4/P6 viết lại các mục sách bị ảnh hưởng → P7 đầy đủ
   cho chương bị đổi → hợp `book.md` → P8 thay nguồn tương ứng trên notebook sách.
5. Ghi `Book/_editions.md`: ấn bản N · ngày · mục RE đổi · chương viết lại · giả thuyết đổi trạng thái ·
   CEO ký phạm vi.
6. Không có thay đổi ⇒ báo "không đổi" **kèm số mục đã so** (để phân biệt "không đổi" với "không so được").
7. Sao lưu `Phase6-Revised/` theo mốc có giờ trước khi viết lại.

## 5. Khung sách (CEO duyệt "khung này đủ")

| Phần | Nội dung (ca BB-02) | Lấy chủ yếu từ |
|---|---|---|
| I. Công nghệ | Vật lý báo trúng: quang đo mức / đo thời điểm, âm học; giới hạn SNR; chuẩn ISSF | TECH_T1/T2/T3, S1C_Tolerance_Perf |
| II. Kiến trúc | Ba họ: quạt nguồn điểm · nhiều màn · âm học · lai; cây SF chung | S2B_Function_Structure, S2B_Solution_Det_SF, S2M |
| III. Cấu trúc | C&C² khung, chắn sáng, chuẩn trực, vật liệu và chế tạo | S1A_CC2_Models, S1B, S1C_Step_f |
| IV. Sản phẩm | Mỗi sản phẩm một chương (MF6R3/ESTA NX · LS25/50 · 3D-Score) + sáng chế và tình trạng hiệu lực | S0_Patent_CC2, S1A_Deconstruction, S1A_Component_Inventory |
| V. Chỗ chưa biết | Giả thuyết, mâu thuẫn mở, bàn thử, trạng thái đo — phần đổi nhiều nhất khi sync | Hypotheses, Precision_Debt |

Khung này là **mặc định của workflow**; P3 vẫn để CEO duyệt dàn ý chi tiết cho từng sách.

## 6. Ràng buộc

- Tiếng Việt cho thân sách và tài liệu nội bộ; tiếng Anh cho mã. Đơn vị mét.
- Không đưa dữ liệu mật, giá nhà cung cấp vào prompt.
- Feature branch `feature/book-re-to-book`; không đụng `VERSION`/`CHANGELOG.md` (ghi changelog vào PR).
- Skill: `skills/book/re-to-book/SKILL.md` (+ `references/`, `scripts/`), frontmatter `name` + `description`
  có "Triggers on:" Anh + Việt. Thêm eval spec `evals/re-to-book.json` mode `static`.
- Script Python chạy được dưới Git Bash và PowerShell; đọc UTF-8 (`-X utf8`); grep tiếng Việt cần locale UTF-8.
- Mọi cổng phải có đối chứng âm (một ca phải bị chặn) và đối chứng dương trước khi tin.

## 7. Bài học K54 P10 → cơ chế

| Bài học (K54 P10, 2026-10-26) | Cơ chế trong workflow |
|---|---|
| Phải dùng bản nguồn "đã cắt ⛔" | Manifest lớp CHẶN/CẮT do script sinh (§4.2) |
| Mã RE phải thành "phân tích nội bộ" trên NLM | Script đổi mã ở bản P8 (§4.5) |
| ≥5 ý trùng Idea_Log lọt vào sách | Không đưa Idea_Log cho tác tử viết + quét trùng ở P7, trình CEO (§4.5) |
| Dự đoán GT chưa ký / bảng kết quả trống | Lớp CẮT + kiểm P7 số 2 |
| Hồ sơ RE đang được phiên khác ghi | Manifest ghi hash tại lúc đọc; sync bắt phần đổi |
| Brief sai "nhà chính" phải đính chính giữa đợt | Hợp đồng nhà chính trước fan-out (§4.4) |

## 8. Để lại cho builder

- Định dạng hiển thị nhãn tri thức trong thân sách.
- Lược đồ chi tiết của `_re_manifest.json`, `*.provenance.json`, `_editions.md`.
- Thuật toán ánh xạ mục RE mới → chương (miễn là CEO duyệt đề xuất).
- Chia script: một script manifest/sync hay nhiều; tái dùng `databus_check.py`, `md_to_epub.py`,
  `p8_ban_nlm.py`-tương-đương ở đâu.
- Cách chạy cục bộ P4/P6 cho một tập mục sách (gọi lại `book-write`/`book-revise` với phạm vi hẹp).
- Ước tính chi phí trình CEO ở scope preview.

## 9. Mở / rủi ro đã biết

- Dự án Tier 3 cần "done criteria" trong khi sách sống không có điểm kết. Done của việc lần này (Q8) =
  ấn bản 1 + ấn bản 2 sau sync kết quả bàn thử 2026-11-04. Sau đó dự án ở lại Projects hay chuyển sang
  Area là việc CEO quyết sau.
- Sync chỉ thấy thay đổi trong **mục `##`**; thay đổi trong `_source/` (PDF mới) không có mục ⇒ manifest
  băm thêm danh mục tệp `_source/` (tên + kích thước + hash) để không bỏ sót.
