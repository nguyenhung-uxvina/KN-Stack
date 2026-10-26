---
name: helix-cc2
description: "Orchestrator bộ C&C² (Contact & Channel) cho thiết kế: đi từ chức năng tới hình thể (tổng hợp) và từ hình thể về chức năng (phân tích), qua 7 khối C0 khung chức năng → C1 ≥3 chuỗi WFP/LSS/Connector → C2 phương án hình thể → C3 bảng tham số hình thể ↔ thông số chức năng → C4 phiếu giả thuyết 9 mục + kế hoạch thử trên bàn thử → CA phân tích độc lập → C6 đối chiếu ngược + bàn giao P3 helix-embody-realize. Bốn chế độ --project / --function / --improve / --analyze, ba cổng CEO, phép biến đổi góc nhìn giữa phiên (--op zoom-in/zoom-out/shift/state/view/observe). Mọi gợi ý là giả thuyết có nhãn, không phải đáp án. Triggers on: 'function to form', 'form from function', 'C&C2 synthesis', 'C&C2 analysis', 'contact and channel', 'embodiment hypothesis', 'từ chức năng tới hình thể', 'tổng hợp hình thể', 'chuỗi C&C2', 'phân tích C&C2', 'hình thể là giả thuyết', 'phiếu giả thuyết kết cấu'."
---

# helix-cc2 — Orchestrator chức năng ⇄ hình thể qua C&C²

> **Vai:** điều phối 7 khối, giữ `_pipeline_state.md`, xử lý lệnh `--op` giữa phiên. Là **nhà chính** của tài liệu
> dùng chung `helix-cc2:references:*` (đường dự phòng `~/.claude/commands/helix-cc2/references/<tên>.md`).
> **Luận đề:** hình thể là giả thuyết. Bộ skill không đưa đáp án; mọi gợi ý mang nhãn **tri thức / phỏng đoán / giả định**
> (`helix-cc2:references:cc2-core` §Hai loại nhãn) kèm **Phép thử nhỏ nhất để bác bỏ**.

## Dòng mở phiên (bắt buộc, in trước mọi khối)

> ⚠ Cảnh báo: bằng chứng về hiệu quả C&C² còn yếu (bậc II/5, chủ yếu đo trên sinh viên, chưa có đối chứng độc lập). Dùng như
> kỷ luật tư duy, không như phương pháp đã chứng minh. Mọi quan hệ hình thể → chức năng dưới đây là giả thuyết cho tới
> khi qua bàn thử. Nguồn: `helix-cc2:references:cc2-core` §Giới hạn dùng và bằng chứng

## Khối

| Mã | Skill | Việc | Đầu ra |
|---|---|---|---|
| C0 | `/helix-cc2-frame` | Câu chức năng → đại lượng vào/ra, thông số chức năng có số + nhãn, Connector biên, ràng buộc môi trường. Chế độ dự án: sàng chức năng con | `{{prefix}}CC2_C0_Frame.md` |
| C1 | `/helix-cc2-chain` | ≥3 chuỗi WFP → LSS → WFP + Connector khác nhau thật *(quy ước bộ skill)*; cuối khối in «Phép nên làm tiếp» | `{{prefix}}CC2_C1_Chains.md` |
| C2 | `/helix-cc2-form` | Mỗi chuỗi đã chọn → 2–3 phương án hình thể *(quy ước bộ skill)*, lý do từ quy tắc hiện thân | `{{prefix}}CC2_C2_Forms.md` |
| C3 | `/helix-cc2-param` | Bảng tham số hình thể ↔ thông số chức năng theo WFP/LSS, đánh dấu tham số nhạy | `{{prefix}}CC2_C3_Params.md` |
| C4 | `/helix-cc2-hypo` | PHIẾU GIẢ THUYẾT 9 mục cho tham số nhạy + Phép thử nhỏ nhất để bác bỏ + kế hoạch thử trên bàn thử | `{{prefix}}CC2_C4_Hypotheses.md`, `{{prefix}}CC2_C4_Test_Plan.md` |
| CA | `/helix-cc2-analyze` | Chiều phân tích độc lập: hình thể có sẵn → mô hình C&C² một trang → giả thuyết chức năng | `{{prefix}}CC2_CA_Analysis.md` |
| C6 | `/helix-cc2-handoff` | Đối chiếu ngược (CA lên phương án chọn) + bàn giao P3 | `{{prefix}}CC2_C6_Crosscheck.md`, `{{prefix}}CC2_Handoff.md` |

Mỗi khối chạy riêng được (`/helix-cc2-param …`). Orchestrator chạy **từng khối một**, không song song.

## Bước 1 — Phân tích cờ

```
Chế độ (chọn đúng một):
  --project <đường dẫn dự án>              dự án: đọc Function_Structure P1, chạy lần lượt từng chức năng con được sàng
  --function "<câu chức năng>"             chức năng lẻ/cụm (nâng cấp, sửa, bổ sung)
  --improve <hình thể> "<chức năng mới>"   cải tiến: phân tích hình thể hiện có rồi mới tổng hợp
  --analyze <hình thể>                     chỉ phân tích (bản vẽ, cad_extract.json, ảnh, mô tả)
Cờ phụ:
  --out <thư mục>     nơi ghi (ưu tiên cao nhất)
  --from <khối>       chạy tiếp từ C0|C1|C2|C3|C4|CA|C6
  --only <khối>       chỉ chạy một khối
  --op <phép> <đích>  phép biến đổi góc nhìn trên một chuỗi (xem mục dưới); không chạy khối nào khác
  --crosscheck <thư mục trích> <X-n> <n>   chỉ C6 dùng, để gọi CA đối chiếu ngược trong tác tử con mới (CA chỉ đọc bản trích C0 + C2/C3 của phương án X-n, không đọc C1/C4; GT mới đánh từ n)
```

Có hơn một cờ chế độ → dừng, hỏi CEO. Thiếu cờ chế độ mà **không** có `--op`/`--from`/`--only` → dừng, hỏi CEO.
`<hình thể>` là đường dẫn tệp hoặc mô tả trong ngoặc kép.

**`--op`, `--from`, `--only` không cần cờ chế độ:** chúng đọc chế độ, nơi ghi và chức năng con hiện hành (`F-id`) từ
`_pipeline_state.md` (tìm ở `--out`, nếu không có thì ở các nơi ghi mặc định dưới đây). Không tìm thấy tệp trạng thái
→ dừng, hỏi CEO; không tự đoán chế độ.

**Đầu vào khi chạy tiếp (`--from` / `--only`):** trước khối bắt đầu, kiểm mọi tệp mà cột «Đọc bởi» của Data Bus ghi
khối ấy. Thiếu tệp nào → liệt kê tệp thiếu và dừng. Không bao giờ dựng giả tệp thượng nguồn; đề nghị CEO chạy khối
thượng nguồn ghi tệp đó (`--from <khối ghi>`).

**Nơi ghi và tiền tố** (spec §8 R4):
1. `--out <thư mục>` nếu có.
2. Không có `--out` mà đang chạy trong dự án (chế độ `--project`, hoặc thư mục làm việc là gốc một dự án có
   `Phase3-Embodiment/`) → `<dự án>/Phase3-Embodiment/CC2/` (hoặc `Phase3-Embodiment/<biến thể>/CC2/`).
3. Còn lại → `./_cc2/<slug>/`, `<slug>` = câu chức năng hoặc tên hình thể viết thường, không dấu, nối `-`.

`{{prefix}}` = tiền tố dự án/biến thể kiểu HELIX (`VN_ABC_V2_`) khi trong dự án, ngược lại `<slug>_`.
**Thư mục theo chức năng con (chế độ `--project`):** tên tệp Data Bus giữ nguyên; mỗi chức năng con có thư mục riêng
`<nơi ghi>/<F-id>/` (`F-id` = mã chức năng con trong Function_Structure, vd. `F3`) chứa C1, C2, C3, C4, CA và
`CC2_C6_Crosscheck.md` của nó. Ở gốc `<nơi ghi>/` chỉ có `{{prefix}}CC2_C0_Frame.md` (danh sách sàng + khung của
từng `F-id`) và `_pipeline_state.md`. Các chế độ khác không có thư mục `<F-id>/`.

Bàn giao P3 (`{{prefix}}CC2_Handoff.md`, một tệp gộp mọi `F-id`, không nằm trong thư mục `<F-id>/`) **chỉ sinh khi có thư mục dự án**, ghi vào `Phase3-Embodiment/` (hoặc `Phase3-Embodiment/<biến thể>/`, thư mục
`helix-embody-realize` đọc), không ghi vào `<nơi ghi>` (mặc định `Phase3-Embodiment/CC2/`). Ngoài dự án, C6 dừng ở `{{prefix}}CC2_C6_Crosscheck.md` + kế hoạch thử C4.

## Bước 2 — Kiểm đầu vào

| Chế độ | Phải có | Nên có |
|---|---|---|
| `--project` | `<dự án>/Phase1-Task/*Function_Structure.md` (đọc trong dự án của chính người dùng) | `Phase1-Task/*Requirements_List*.md`; P2 `Phase2-Concept/*Morphological_Matrix.md`, `*Concept_Selection.md` |
| `--function` | Câu chức năng; tốt nhất có thông số chức năng có số | Nguyên lý vật lý trong câu (vd. `[quang→điện]`) |
| `--improve` | Hình thể hiện có đọc được + câu chức năng mới | Biên bản hỏng / dữ liệu hiện trường |
| `--analyze` | Hình thể đọc được | Câu hỏi phân tích (mục đích bước (a)) |

In checklist ✓/✗ cho CEO trước khi chạy. Thiếu mục «Phải có» → dừng.

**Luật IP (cứng):** KHÔNG đọc hồ sơ trong `1_Projects/` của dự án có IP để lấy ví dụ minh hoạ, và cấm đưa hồ sơ ấy
cho tác tử con khi dựng nháp. Ví dụ trong khối dùng cơ cấu công khai hoặc nguyên lý chung từ sách. Chế độ `--project`
chỉ đọc tệp đầu vào của chính dự án được chỉ định, để chạy, không để làm ví dụ.

## Bước 3 — Trạng thái pipeline

Tạo hoặc đọc `<nơi ghi>/_pipeline_state.md`. Có tệp → hỏi tiếp tục hay làm lại.

```markdown
---
updated: YYYY-MM-DD
mode: project | function | improve | analyze
prefix: {{prefix}}
out: {{nơi ghi}}
current_f: {{F-id hiện hành, vd. F3 — chỉ chế độ project}}
---
# CC2 Pipeline — {{dự án hoặc slug}}

## Khối
| Chức năng con | C0 | C1 | Chuỗi chọn | C2 | C3 | C4 | Ký dự đoán | CA | C6 |
|---|---|---|---|---|---|---|---|---|---|
| {{F1}} | ✓ | ✓ | B.1 | ✓ | ✓ lint 0 | ✓ lint 0 | {{tên — ngày}} | — | ⏳ |

## Cổng CEO
| Cổng | Ngày | Quyết định | Lý do |
|---|---|---|---|
| 3 ký dự đoán · {{F1}} | YYYY-MM-DD | đã ký {{GT-001…GT-003}}; phương án đi tiếp: {{A-1}} | {{…}} |

## Nhật ký phép biến đổi
| Ngày | Phép | Đích | Phiên bản mới | Câu hỏi kích hoạt | Ai gọi |
|---|---|---|---|---|---|
| YYYY-MM-DD | zoom-in | F3/B:WFP2 | B.1 | {{câu hỏi}} | đề xuất / CEO |
```

Cập nhật sau mỗi khối, mỗi cổng, mỗi `--op`.

## Bước 4 — Chạy khối theo chế độ

**Phạm vi cứng.** Chỉ dựng C&C² cho chức năng quyết định giải pháp + ≤3 chức năng tới hạn *(con số 3 là quy ước bộ
skill)*, không mô hình hoá cả sản phẩm (`helix-cc2:references:cc2-core` §Phạm vi cứng).

**Cổng.** ⛔ = dừng, chờ CEO trả lời; không chạy khối kế khi chưa ghi quyết định vào bảng Cổng CEO.

### `--project`

1. **C0** liệt kê đủ mọi chức năng con rồi xếp mỗi cái vào một ô sàng: `dựng C&C²` · `chỉ bảng tham số` ·
   `không áp dụng`, mỗi ô một câu lý do.
   **⛔ Cổng CEO 1 — duyệt danh sách sàng.** CEO có thể đẩy thêm vào ô `dựng C&C²` và vượt trần 3, phải ghi lý do.
2. Với từng chức năng con ở ô `dựng C&C²`, lần lượt, chức năng tới hạn trước (ghi `current_f` vào trạng thái,
   tệp vào `<nơi ghi>/<F-id>/`):
   C1 → **⛔ Cổng CEO 2 — chọn chuỗi** → C2 → C3 → C4 → **⛔ Cổng CEO 3 — ký dự đoán** → C6.
   Ở Cổng CEO 3 (mọi chế độ có C6), CEO ghi thêm vào bảng Cổng CEO phương án đi tiếp `X-n` của chức năng con ấy (dạng `phương án đi tiếp: A-1`); C6 đọc từ đó, không tự chọn.
   Ô `chỉ bảng tham số` chỉ chạy C3. Ô `không áp dụng` ghi `C&C²: không áp dụng, vì …` và dừng.
3. C6 gộp một `{{prefix}}CC2_Handoff.md` cho cả dự án, đủ mọi `F-id`.

### `--function`

C0 → C1 → ⛔ chọn chuỗi → C2 → C3 → C4 → ⛔ ký dự đoán → C6.

### `--improve`

CA lên hình thể hiện có → C0 (chức năng mới + chỗ hỏng từ CA) → C1 → ⛔ chọn chuỗi → C2 → C3 → C4 → ⛔ ký dự đoán → C6.
C1 phải có ít nhất một chuỗi «hình thể hiện có, sửa tối thiểu».

### `--analyze`

Chỉ dùng cho **hình thể của chính Xưởng** (bản vẽ, CAD, ảnh, hiện vật của mình). Không có Purpose Gate, không có
ACCESS LEVEL, không OSINT. Phân tích sản phẩm của bên khác hay của đối thủ → dùng `/reverse-engineering`, không dùng
chế độ này.

Chỉ CA. Có thể kết thúc bằng C4 nếu CEO muốn lập phiếu: khi ấy C4 lấy các **giả thuyết nháp trong
`{{prefix}}CC2_CA_Analysis.md`** làm đầu vào, thay cho các tham số đánh dấu NHẠY của C3 (không có C3 ở luồng này).

### Luật từng khối (orchestrator kiểm trước khi qua khối sau)

- **C1:** ≥3 chuỗi *(quy ước bộ skill)*, khác nhau ở cách sắp WFP/LSS/Connector, không chỉ đổi kích thước
  (`helix-cc2:references:synthesis-moves` §Các nước đi). Mỗi chuỗi có sơ đồ vẽ tay lại được.
  Khi câu chức năng **không nêu nguyên lý vật lý**: C0 ghi `nguyên lý: chưa nêu`, C1 đề xuất chuỗi ở ≥2 miền vật lý
  khác nhau, mỗi chuỗi một dòng *vì sao miền này hợp với thông số C0* có nhãn. Đây chỉ là **nguồn ý, không phải
  quyết định concept**. Đã có P2 thì ưu tiên nguyên lý P2 chọn; chuỗi khác miền ghi «lệch P2 — CEO quyết».
  helix-cc2 **không** dựng ma trận hình thái, **không** chấm DSO/VDI 2225 (việc của `helix-p2-search`).
  Chuỗi đi vào điện tử/phần mềm phải ghi chỗ C&C² hết dùng được (`helix-cc2:references:multidomain` §Chỗ phải dừng).
- **C2:** 2–3 phương án mỗi chuỗi *(quy ước bộ skill)*, lý do trỏ quy tắc hiện thân (`helix-cc2:references:embodiment-rules`).
- **C3:** bảng theo `helix-cc2:references:param-bridge` §Khuôn bảng C3. Cổng máy:
  `python scripts/cc2_sheet_lint.py <C3> --kind params` — mã 0 mới qua; mã 1 → sửa ô thiếu nhãn rồi chạy lại; mã 2 → báo lỗi đọc, dừng.
- **C4:** mỗi PHIẾU GIẢ THUYẾT theo `helix-cc2:references:hypothesis-sheet` §Khuôn phiếu; «NẾU» là tham số ghi được
  lên bản vẽ, không phải tác dụng; định tuyến theo `helix-cc2:references:hypothesis-sheet` §Định tuyến độ tin × tầm ảnh hưởng.
  Cổng máy hai lượt: **trước** Cổng CEO 3 chạy `python scripts/cc2_sheet_lint.py <C4_Hypotheses> --kind hypo --allow-unsigned`
  (bỏ qua đúng mã PRED_UNSIGNED, mọi mã khác vẫn chặn) phải ra mã 0; **sau** khi CEO ký, chạy lại
  `python scripts/cc2_sheet_lint.py <C4_Hypotheses> --kind hypo` (không cờ) — mã 0 mới đóng Cổng CEO 3; C6 chạy lại lệnh
  không cờ này. Mục 7 (dự đoán) do CEO/kỹ sư ký, ngày ký trước ngày thử; AI không điền chữ ký.
- **C6:** đối chiếu ngược do **một tác tử con khác** làm, chỉ nhận C0 + C2/C3, không thấy lý lẽ C1. Mỗi chỗ lệch thành
  phiếu mới hoặc một dòng sửa C2. `CC2_Handoff` ghi rõ đây là *đối chiếu mức mô tả* và kèm mục **vòng lặp P3**: khi P3
  có `cad_extract.json`, chạy `/helix-cc2 --analyze` lên đó để đối chiếu mức hình học.

Sau mỗi khối: cập nhật `_pipeline_state.md`, in tóm tắt 3–5 dòng, hỏi CEO «tiếp / sửa / dừng».

## Phép biến đổi giữa phiên (`--op`)

```
/helix-cc2 --op <phép> <đích>        đích: [<F-id>/]<chuỗi>[:<phần tử>[→<phần tử>]]
vd.  --op zoom-in B:WFP2   --op zoom-out A   --op shift B:WFP1→WFP2
     --op state B          --op view B:bệ-thử   --op observe B:WFP2
     --op zoom-in F3/B:WFP2                     (chế độ dự án)
```

Tiền tố `<F-id>/` **bắt buộc** ở chế độ `--project` khi có hơn một chức năng con đang mở; còn lại tuỳ chọn (thiếu thì
dùng `current_f` trong `_pipeline_state.md`). Chuỗi `B` của `F3` và chuỗi `B` của `F5` là hai chuỗi khác nhau.

| Phép | Đổi gì trên mô hình | Định nghĩa |
|---|---|---|
| `zoom-in` | Tách một phần tử thành khung con có mục đích riêng | `helix-cc2:references:view-ops` §zoom-in |
| `zoom-out` | Gộp phần tử, nới biên để thấy tương tác | `helix-cc2:references:view-ops` §zoom-out |
| `shift` | Dời trọng tâm dọc lưới làm việc, mở biên | `helix-cc2:references:view-ops` §shift |
| `state` | Cắt chuỗi theo trạng thái / nhánh logic | `helix-cc2:references:view-ops` §state |
| `view` | Ảnh hệ mới từ chỗ đứng khác | `helix-cc2:references:view-ops` §view |
| `observe` | Chọn phương tiện quan sát tác động lên mẫu | `helix-cc2:references:view-ops` §observe |

Xử lý một `--op`:
1. Phép ngoài sáu phép trên, hoặc đích không khớp cú pháp / không có trong `{{prefix}}CC2_C1_Chains.md` (của `<F-id>/` nếu có) → từ chối, liệt kê chuỗi và phần tử hiện có.
2. Yêu cầu một **câu hỏi kích hoạt** (dòng «Khi nào:» của phép trong view-ops). Không có câu hỏi thì không chạy phép.
3. Ghi **phiên bản chuỗi mới** `B.1`, `B.2`… nối vào tệp C1 (hoặc CA), không ghi đè phiên bản cũ.
4. Thêm một dòng vào `## Nhật ký phép biến đổi` của `_pipeline_state.md`.
5. Khối sau (C2…) dùng phiên bản CEO chỉ định; mặc định là phiên bản đã chọn ở cổng 2.

Cuối C1, C2 và CA, khối in **«Phép nên làm tiếp»**: 1–3 dòng `phép · phần tử · câu hỏi kích hoạt`. Chọn phép theo
rào cản quan sát của chuỗi: quá nhanh / quá chậm → `state`; bị che → `observe` hoặc `shift`; quá nhỏ / quá lớn →
`zoom-in` hoặc mẫu tỉ lệ; sai góc nhìn → `view`; nguyên cớ ngoài biên → `shift`, `zoom-out` — xem
`helix-cc2:references:view-ops` §Rào cản quan sát. Skill tự đề xuất; CEO vẫn gọi tay được.

## Data Bus

| Tệp | Ghi bởi | Đọc bởi |
|---|---|---|
| `{{prefix}}CC2_C0_Frame.md` | helix-cc2-frame (C0) | C1, C3, C6 |
| `{{prefix}}CC2_C1_Chains.md` | helix-cc2-chain (C1); phiên bản `--op` do helix-cc2 nối | C2, orchestrator `--op` |
| `{{prefix}}CC2_C2_Forms.md` | helix-cc2-form (C2) | C3, C6 |
| `{{prefix}}CC2_C3_Params.md` | helix-cc2-param (C3) | C4, C6 |
| `{{prefix}}CC2_C4_Hypotheses.md` | helix-cc2-hypo (C4) | C6, CEO (ký dự đoán) |
| `{{prefix}}CC2_C4_Test_Plan.md` | helix-cc2-hypo (C4) | C6, bàn thử |
| `{{prefix}}CC2_CA_Analysis.md` | helix-cc2-analyze (CA); helix-cc2-handoff (C6) nối mục `## Đối chiếu ngược — phương án <X-n>` | C0 (`--improve`), C4 (`--analyze`), C6 |
| `{{prefix}}CC2_C6_Crosscheck.md` | helix-cc2-handoff (C6) | CEO |
| `{{prefix}}CC2_Handoff.md` | helix-cc2-handoff (C6), ghi vào `<dự án>/Phase3-Embodiment/` (hoặc thư mục biến thể), không vào `<nơi ghi>` | helix-embody-realize, helix-p3-layout |
| `_pipeline_state.md` | helix-cc2 (orchestrator) | mọi khối, `--from` |

Chế độ `--project`: tệp C1, C2, C3, C4, CA và `CC2_C6_Crosscheck.md` nằm trong `<nơi ghi>/<F-id>/`; C0 và
`_pipeline_state.md` ở gốc `<nơi ghi>/`; `CC2_Handoff.md` ở `Phase3-Embodiment/`, một tệp cho mọi `F-id`.

## Tích hợp

**READS FROM**
- `<dự án>/Phase1-Task/*Function_Structure.md`, `*Requirements_List*.md` (chỉ chế độ `--project`)
- `<dự án>/Phase2-Concept/*Morphological_Matrix.md`, `*Concept_Selection.md` (nếu có — để ưu tiên nguyên lý P2)
- Hình thể cho CA: bản vẽ, ảnh, mô tả, `cad_extract.json` từ `helix-cad-ingest` / `helix-cad-bridge`
- `helix-cc2:references:*` (cc2-core, view-ops, synthesis-moves, embodiment-rules, param-bridge, hypothesis-sheet, multidomain)

**WRITES TO**
- `<nơi ghi>/` (xem Bước 1): mọi tệp `{{prefix}}CC2_*` và `_pipeline_state.md`
- `<dự án>/Phase3-Embodiment/{{prefix}}CC2_Handoff.md` → đầu vào khuyến nghị của `/helix-embody-realize` (P3)

## COD

| Việc | Lớp | Ai |
|---|---|---|
| Dựng nháp khung, chuỗi, hình thể, bảng tham số, phiếu, kế hoạch thử, đối chiếu | **O** Offload | AI, CEO giám sát |
| Đề xuất «Phép nên làm tiếp» | **O** Offload | AI |
| Duyệt danh sách sàng C0 | **C** Core | CEO |
| Chọn chuỗi sau C1 | **C** Core | CEO / kỹ sư |
| Ký dự đoán (mục 7 phiếu) sau C4 | **C** Core | CEO / kỹ sư — AI không ký thay |
| Duyệt bàn giao P3 | **C** Core | CEO |
| Chạy `cc2_sheet_lint`, cập nhật trạng thái | **D** Default | tự động |

## Hoàn tất

In: số chức năng con đã chạy / đã sàng, chuỗi chọn của mỗi cái, số phiếu mở + mã lint, ngày thử sớm nhất, đường dẫn
`CC2_Handoff` (hoặc lý do không sinh). Nhắc: kế hoạch thử là bước kế tiếp tạo dữ liệu vật lý; chưa thử thì mọi
hình thể vẫn là giả thuyết.
