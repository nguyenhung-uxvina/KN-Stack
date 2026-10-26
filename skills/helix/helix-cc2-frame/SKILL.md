---
name: helix-cc2-frame
description: "Khối C0 của bộ helix-cc2 — đóng khung chức năng trước khi dựng chuỗi C&C²: câu chức năng → đại lượng vào/ra, thông số chức năng có Nhãn + Nguồn số, Connector biên, nguyên lý (đã nêu / chưa nêu + miền ứng viên). Chế độ dự án: sàng mọi chức năng con vào ba ô (dựng C&C² / chỉ bảng tham số / không áp dụng), trần = chức năng quyết định giải pháp + ≤3 tới hạn, CEO duyệt. Chế độ --improve đọc CC2_CA_Analysis.md. Chạy riêng được. Triggers on: 'frame function', 'C&C2 frame', 'function screening', 'sàng chức năng con', 'đóng khung chức năng', 'thông số chức năng', 'khung C0', 'helix-cc2-frame'."
---

# helix-cc2-frame — Khối C0: khung chức năng

> **Vai:** đứng đầu pipeline `helix-cc2`; biến một câu chức năng thành khung có số và có nhãn để C1 dựng chuỗi.
> **Đầu ra:** `{{prefix}}CC2_C0_Frame.md` | **Đọc bởi:** C1, C3, C6 | **Nguồn dùng chung:** `helix-cc2:references:cc2-core`
> (§Từ vựng, §Phạm vi cứng, §Hai loại nhãn), `helix-cc2:references:multidomain` (§Chỗ phải dừng).

In dòng mở phiên của orchestrator (cảnh báo bằng chứng yếu) trước khi chạy. Mọi con số do khối này viết ra mang
nhãn; số thuộc về bộ skill (không phải của sách) ghi *(quy ước bộ skill)*.

## Đầu vào

| Chế độ | Đọc |
|---|---|
| `--function` | Câu chức năng; thông số có số nếu CEO có |
| `--improve` | Câu chức năng mới + `{{prefix}}CC2_CA_Analysis.md` (chỗ hỏng, hình thể hiện có) |
| `--project` | Glob như `helix-embody-realize` Step 1.5a: `Phase1-Task/{{variant}}/` → `Function_Structure.md`, `Requirements_List_v*.md`; nếu có, `Phase2-Concept/{{variant}}/` → `Concept_Selection.md`, `Morphological_Matrix.md` (cả hai thư mục nằm dưới thư mục dự án được chỉ định) |

Chỉ đọc tệp đầu vào của chính dự án được chỉ định để chạy, không để lấy ví dụ; không đưa hồ sơ ấy cho tác tử con (luật IP
của orchestrator). Thiếu `Function_Structure.md` ở chế độ dự án → dừng, báo CEO.

## Bước

### Bước 1 — Chức năng và đại lượng

Viết câu chức năng dạng *động từ + đối tượng*, rồi liệt kê đại lượng vào / ra (năng lượng, vật chất, thông tin).
Câu nào hỏi *sửa thế nào* thay vì *đặc điểm nào quyết định hiện tượng* thì viết lại về dạng hỏi (`helix-cc2:references:cc2-core` §Bảy bước dựng mô hình, bước a).

### Bước 2 — Thông số chức năng

Bảng bắt buộc có đúng hai cột `Nhãn` và `Nguồn số`:

- `Nhãn` ∈ `tri thức` / `phỏng đoán` / `giả định` (`cc2-core` §Hai loại nhãn, loại a).
- `Nguồn số` bắt đầu bằng `đo được` / `suy ra (từ …)` / `chưa biết` (loại b). `tri thức` không đi với `chưa biết` *(quy ước bộ skill)*.
- Thiếu số thì để `—` ở cột giá trị và ghi `chưa biết`; không bịa số cho đủ bảng.

### Bước 3 — Connector biên

Mỗi đầu vào/ra giao với môi trường là một Connector kèm lời hứa «phần ngoài không liên quan». Ghi mỗi Connector một dòng:
tên, hứa gì, kiểm lời hứa bằng gì. Ràng buộc môi trường (nhiệt, rung, ẩm, bụi, điện từ…) ghi ngay dưới bảng Connector. Chỗ chức năng đi vào điện tử / phần mềm: ghi chỗ dừng bằng câu khuôn của
`helix-cc2:references:multidomain` §Câu khuôn.

### Bước 4 — Nguyên lý

- Câu chức năng hoặc P2 đã nêu nguyên lý → ghi `đã nêu: <nguyên lý>` và nguồn (câu chức năng / Concept_Selection).
- Chưa nêu → ghi `chưa nêu` và danh sách `miền ứng viên` (≥2 miền vật lý khác nhau *(quy ước bộ skill)*), mỗi miền một dòng
  vì sao hợp với thông số ở Bước 2, có nhãn. Đây là **nguồn ý**, chưa phải quyết định concept.
- Có P2 mà nguyên lý trong câu khác P2 → nêu mâu thuẫn, mặc định theo P2, hỏi CEO.

### Bước 5 — Sàng chức năng con (chỉ `--project`)

Liệt kê **đủ** mọi chức năng con trong `Function_Structure.md`, xếp mỗi cái vào đúng một ô, kèm đúng một câu lý do
(tiêu chí ở `cc2-core` §Phạm vi cứng): `dựng C&C²` · `chỉ bảng tham số` · `không áp dụng`.

- Trần mặc định: chức năng quyết định giải pháp + **≤3 chức năng tới hạn** *(quy ước bộ skill)*; xếp tới hạn trước.
- Ô `không áp dụng` ghi câu khuôn «C&C²: không áp dụng, vì …» (`multidomain` §Câu khuôn).
- ⛔ **Cổng CEO 1 — duyệt danh sách sàng.** Dừng, chờ CEO. CEO có thể đẩy thêm vào ô `dựng C&C²` và vượt trần, **phải
  ghi lý do bằng văn bản**. Quyết định của CEO, dù duyệt nguyên trạng hay có vượt trần, được ghi vào bảng Cổng CEO của
  `_pipeline_state.md` **trước khi** C1 chạy (không chạy khối kế khi chưa ghi quyết định).
- Với mỗi `F-id` ở ô `dựng C&C²`, Bước 1–4 chạy riêng; khung của từng `F-id` nằm trong cùng tệp C0 ở gốc nơi ghi.

### Bước 6 — Hình thể hiện có (chỉ `--improve`)

Không chép lại phân tích: trỏ tới `{{prefix}}CC2_CA_Analysis.md`, nêu chỗ hỏng hoặc chỗ chức năng mới không đạt, và
phần tử nào sẽ giữ nguyên cho chuỗi «sửa tối thiểu» của C1.

### Bước 7 — Cổng máy

```bash
python D:/KN-Stack/scripts/cc2_sheet_lint.py <tệp C0> --kind params
```

Mã 0 mới qua; mã 1 → sửa ô thiếu Nhãn / Nguồn số rồi chạy lại; mã 2 → báo lỗi đọc, dừng. Bảng «Thông số chức năng» là bảng
tham số mà lint này tìm.

## Khuôn đầu ra: `{{prefix}}CC2_C0_Frame.md`

```markdown
---
updated: YYYY-MM-DD
mode: project | function | improve
---
# CC2 C0 — Khung chức năng: {{tên}}

## Chức năng
{{động từ + đối tượng}} · Vào: {{…}} · Ra: {{…}}

## Thông số chức năng
| Thông số | Giá trị | Đơn vị | Nhãn | Nguồn số |
|---|---|---|---|---|
| {{đại lượng}} | {{số hoặc —}} | {{SI}} | {{tri thức/phỏng đoán/giả định}} | {{đo được / suy ra (từ …) / chưa biết}} |

## Connector biên
| Connector | Lời hứa «ngoài không liên quan» | Kiểm bằng |
|---|---|---|

### Ràng buộc môi trường
{{nhiệt độ, rung, ẩm, bụi, điện từ… — nhãn tri thức/phỏng đoán/giả định; không số thì ghi chưa biết}}

## Nguyên lý
đã nêu: {{…}}  |  chưa nêu
miền ứng viên (nguồn ý, không phải quyết định concept): {{miền 1 — vì sao hợp, nhãn}}; {{miền 2 — …}}

## Sàng chức năng con
<!-- chỉ --project -->
| F-id | Chức năng con | Ô sàng | Lý do (một câu) |
|---|---|---|---|

## Hình thể hiện có
<!-- chỉ --improve -->
Xem {{prefix}}CC2_CA_Analysis.md — chỗ hỏng: {{…}}; giữ nguyên: {{…}}
```

## Ví dụ ngắn: quang → điện, mức nguyên lý (giả định, không số)

Câu chức năng: «phát hiện có vật đi qua một lối» — không nêu nguyên lý. Đầu vào: vật che; đầu ra: tín hiệu điện hai mức.

| Thông số | Giá trị | Đơn vị | Nhãn | Nguồn số |
|---|---|---|---|---|
| ngưỡng phát hiện kích thước vật nhỏ nhất | — | — | giả định | chưa biết |
| thời gian đáp ứng | — | — | giả định | chưa biết |

Nguyên lý: `chưa nêu`; miền ứng viên: quang (vật che cắt chùm tia), cơ (vật chạm cần gạt). Không số, không tên sản phẩm;
quyết nguyên lý là việc P2 / CEO.

## Chạy riêng

```
/helix-cc2-frame --function "<câu chức năng>" [--out <thư mục>]
/helix-cc2-frame --improve <hình thể> "<chức năng mới>"     (cần CC2_CA_Analysis.md)
/helix-cc2-frame --project <đường dẫn dự án>                (cần Function_Structure.md)
```

Đầu vào tối thiểu: một câu chức năng. Nơi ghi và tiền tố theo Bước 1 của orchestrator `helix-cc2`; chế độ dự án chỉ có
một tệp C0 ở gốc nơi ghi.

## COD

| Việc | Lớp | Ai |
|---|---|---|
| Dựng nháp khung, bảng thông số, danh sách sàng | **O** Offload | AI |
| Duyệt danh sách sàng, vượt trần ≤3 | **C** Core | CEO — ghi lý do bằng văn bản |
| Chọn nguyên lý khi `chưa nêu` | **C** Core | CEO / P2 |
| Chạy `cc2_sheet_lint --kind params` | **D** Default | tự động |
