---
name: qtcn
description: Lập Quy trình công nghệ (QTCN) lắp ráp / hiệu chỉnh / gia công cho một sản phẩm cơ khí — quân sự, theo đúng cấu trúc chuẩn xưởng Việt Nam. Phân rã sản phẩm thành chuỗi nguyên công tối ưu (optimized flow), mỗi nguyên công có Yêu cầu kỹ thuật, Định mức (bậc thợ / thời gian / nơi thực hiện) và Danh mục nguyên vật liệu + thiết bị công nghệ; kèm Quy định chung kỹ thuật & an toàn và Bảng tổng hợp tiến trình. Hỗ trợ cờ: --B (chỉ Lắp ráp & Hiệu chỉnh + Thử nghiệm & Bàn giao, bỏ phần chế tạo chi tiết), --cad (kèm đặc tả hình minh họa CAD cho từng nguyên công để họa viên vẽ và chèn), --json (xuất bản JSON máy đọc gồm checkpoint nghiệm thu + spec minh họa CAD làm cơ sở kiểm tra quy trình sau này). Triggers on "quy trình công nghệ", "QTCN", "lập quy trình", "lập qui trình công nghệ", "quy trình lắp ráp", "quy trình hiệu chỉnh", "nguyên công", "work instructions", "assembly process", "manufacturing process route", "định mức nguyên công", "lập quy trình gia công", "--B", "--cad", "--json", hoặc khi CEO/kỹ thuật cần soạn QTCN cho một sản phẩm từ BOM / bản vẽ / mô tả lắp ráp.
---

# QTCN — Lập Quy trình Công nghệ Lắp ráp / Hiệu chỉnh / Gia công

Soạn một **Quy trình công nghệ (QTCN)** hoàn chỉnh cho sản phẩm cơ khí của Workshop X, theo đúng cấu trúc tài liệu chuẩn xưởng: phân rã thành **nguyên công** theo dòng công nghệ tối ưu, mỗi nguyên công đầy đủ **Yêu cầu kỹ thuật → Định mức → Vật tư + Thiết bị**, đóng khung bởi **Quy định chung kỹ thuật & an toàn** và **Bảng tổng hợp tiến trình công nghệ**.

Giá trị cốt lõi của skill không phải là điền template — mà là **trình tự công nghệ đúng và tối ưu** cùng **thông số kỹ thuật chính xác** (lực siết, dung sai, quy tắc lắp ghép, an toàn). Toàn bộ tri thức công nghệ nằm ở [references/qtcn-engineering-rules.md](references/qtcn-engineering-rules.md); các mẫu đầu ra ở [references/qtcn-templates.md](references/qtcn-templates.md). **Đọc cả hai trước khi soạn.**

## Chế độ chạy (Flags)

Nhận cờ tùy chọn, **kết hợp được** (vd `/qtcn BM-01 --B --cad --json`):

| Cờ | Loại | Ảnh hưởng đầu ra |
|----|------|------------------|
| *(mặc định)* | phạm vi | QTCN **tổng thể end-to-end**: Phần A Chế tạo chi tiết + Phần B Lắp ráp & Hiệu chỉnh + Phần C Thử nghiệm & Bàn giao. |
| `--B` | phạm vi | **Bỏ Phần A (chế tạo)**; chỉ xuất **Phần B Lắp ráp & Hiệu chỉnh + Phần C Thử nghiệm & Bàn giao**. Dùng khi chi tiết đã có sẵn / mua ngoài, chỉ cần quy trình lắp–hiệu chỉnh–thử–bàn giao. Đánh số nguyên công vẫn theo cụm B*/C* để truy vết. |
| `--cad` | bổ sung | Thêm mục **IV. Minh họa / Bản vẽ đề xuất** vào mỗi nguyên công: loại hình (chiếu/cắt/trích/exploded/rigging/sơ đồ đấu nối), nội dung phải thể hiện, **callout** (kích thước, dung sai, lực siết, bộ đệm, hướng), và **nguồn bản vẽ** — để họa viên dựng trong CAD rồi chèn `[ẢNH: …]`. Skill **đặc tả hình**, không vẽ hình. Quy ước ở references §9, mẫu khối ở references §D. |
| `--json` | bổ sung | Xuất thêm `QTCN-<sp>.json` — toàn bộ QTCN có cấu trúc (BOM+VT, nguyên công, thông số, **checkpoint nghiệm thu định lượng**, và **spec minh họa CAD cần có**) làm cơ sở **đối soát/kiểm tra quy trình về sau** (verify, inspection, audit). Schema ở references §E. |

Mặc định (không cờ) = bản đầy đủ A+B+C dạng Markdown. `--cad`/`--json` là bổ sung độc lập; `--B` chọn phạm vi. Khi có `--json` **và** `--cad`, mỗi nguyên công trong JSON có nhánh `cad_illustration` được điền đầy đủ.

## Khi nào dùng

- CEO/kỹ thuật cần lập QTCN lắp ráp/hiệu chỉnh cho một sản phẩm (ví dụ: thiết bị bia nổi BM-01, xuồng, giá đỡ, kết cấu thép).
- Sau khi có BOM (`/bom` hoặc `helix-p4-bom`) và bản vẽ chi tiết (`helix-detail-finalize` / `helix-p4-drawing`) → cần biến gói thiết kế thành tài liệu sản xuất cho phân xưởng.
- Chuẩn hóa / tối ưu lại một quy trình lắp ráp đang làm thủ công (giảm số lần định vị lại, tách căn chỉnh khỏi siết lực, đưa cụm nhẹ lên trước để tối ưu tải).
- Đầu vào cho `helix-p4-handoff` → `forge-fabrication` và cho biên bản nghiệm thu.

## Đầu vào

Skill chạy được **độc lập** từ một mô tả sản phẩm + danh mục chi tiết, hoặc **nạp nền từ extract-cad** (khuyến nghị), hoặc tích hợp với pipeline. Thu thập:

0. **`qtcn-seed.json` từ extract-cad (nền tảng — ưu tiên).** Nếu đã trích xuất bản vẽ bằng [mech-drawing-extract](../../extract/mech-drawing-extract/SKILL.md), chạy cầu nối [cad-pipeline/scripts/extract/extract_to_qtcn_seed.py](../../../cad-pipeline/scripts/extract/extract_to_qtcn_seed.py) → `qtcn-seed.json` (product + BOM có **VT gán sẵn** + vật liệu + SL + section/plate/tolerances mỗi chi tiết + vật tư mua). **Đây là nguồn cho Bước 0 & Bước 1** — không nhập tay lại. Truyền qua `--seed <qtcn-seed.json>`.
   - **Nếu phần mềm thiết kế là Autodesk Inventor → dùng thẳng BOM Inventor xuất (nguồn VÀNG).** Trong Inventor: *Assemble → Bill of Materials → Export* ra `.xlsx`/`.csv` với các cột **Part Number · Description · QTY · Material · Mass · Stock Number** (Mass ghi rõ đơn vị kg/g). Chạy [cad-pipeline/scripts/extract/bom_xlsx_to_seed.py](../../../cad-pipeline/scripts/extract/bom_xlsx_to_seed.py) `--bom <BOM.xlsx>` → cùng `qtcn-seed/v1`, nhưng **`est_mass_kg` THẬT** (Inventor tính, không đoán ρ), **QTY lắp thật** (không lệch 1-instance như STEP), **drawing_no = Part Number** (hết null). Đây là seed tốt hơn cả 2D lẫn 3D suy diễn. Dung sai/GD&T không có trong BOM ⇒ nếu cần, ghép thêm seed 2D (DXF) qua [merge_qtcn_seeds.py](../../../cad-pipeline/scripts/extract/merge_qtcn_seeds.py). Lưu ý: FreeCAD/script **không đọc được `.ipt`/`.iam`** — Inventor bắt buộc xuất định dạng trung lập (BOM.xlsx/STEP/DXF).
1. **Danh mục chi tiết (BOM)** — tên gọi + **mã vị trí (VT1, VT2, …)** + số lượng + vật liệu. Mã VT là xương sống để tham chiếu trong từng nguyên công. Nếu có `qtcn-seed.json` thì lấy từ đó; nếu chưa, chạy `/bom` hoặc lập nhanh từ bản vẽ.
2. **Quan hệ lắp ghép** — chi tiết nào nối với chi tiết nào, bằng mối ghép gì (bu lông M?, hàn, cáp chằng, ma ní…), bản vẽ bố trí nếu có.
3. **Loại quy trình** — *lắp ráp & hiệu chỉnh* (assembly) hay *gia công cơ khí* (machining) hay hỗn hợp. (Template & nguyên công khác nhau — xem references.)
4. **Môi trường & ràng buộc khai thác** — quyết định yêu cầu kỹ thuật. Ví dụ: làm việc **ngoài biển / ngoài trời** ⇒ bắt buộc chống tự nới lỏng (đệm phẳng + đệm vênh + vạch sơn) và chống nước **IP67** cho mối nối điện; có **làm việc trên cao / nâng hạ** ⇒ điều khoản an toàn cẩu + dây đai.
5. **Tài liệu chuẩn áp dụng & các thông số bắt buộc** — cấp bền bu lông (5.6/8.8…), mô-men siết yêu cầu, dung sai lắp ghép, tiêu chuẩn nghiệm thu. Lấy từ bản vẽ/thiết kế; **không tự bịa lực siết** — xem bảng tham chiếu nhưng phải chốt theo cấp bền & thiết kế thực.

Nếu thiếu thông tin chốt chặn (mã VT, cấp bền bu lông, dung sai tới hạn, môi trường khai thác), **hỏi CEO** thay vì giả định.

## Quy trình thực hiện

### Bước 0 — Nạp nền từ extract-cad (nếu có `qtcn-seed.json`)

Nếu được truyền `--seed <qtcn-seed.json>` (do `extract_to_qtcn_seed.py` sinh từ đầu ra mech-drawing-extract, hoặc `bom_xlsx_to_seed.py` từ BOM Inventor): đọc file này làm **nền tảng**. Nó cung cấp sẵn `product` (mã, tên, thông số chủ yếu), `bom[]` (VT ↔ mã bản vẽ ↔ tên ↔ SL ↔ vật liệu + `specs.sections`/`plate_mm`/`tolerances`/`key_dims`), và `consumables[]` (vật tư mua). ⇒ **Bỏ qua nhập tay** ở Bước 1; chỉ cần rà đối chiếu & bổ sung. Lưu ý `specs.est_mass_kg` = null nếu seed từ bản vẽ scale (còn seed **từ Inventor BOM có khối lượng THẬT**); `relationships` để trống — Bước 2 suy ra mối ghép. Xem cờ `flags.mass_source`/`*_complete` để biết seed đủ chưa. Nếu **không** có seed, làm Bước 1 thủ công như thường.

### Bước 1 — Lập / rà danh mục chi tiết & mã VT

Chốt danh sách chi tiết với mã VT, số lượng, vật liệu. Nếu đã có seed (Bước 0) thì **đây là bước rà soát**: xác nhận VT gán tự động hợp lý, bổ sung vật tư phụ còn thiếu (đệm, lạt nhựa, băng keo, mỡ…). Đây là từ điển tham chiếu cho toàn bộ QTCN. Liệt kê cả vật tư phụ và mối liên kết.

### Bước 2 — Phân rã & TỐI ƯU dòng công nghệ (giá trị kỹ thuật chính)

Phân rã sản phẩm thành chuỗi **nguyên công** từ kiểm tra đầu vào → lắp ráp → hiệu chỉnh → kiểm tra tổng thể & bàn giao. Sau đó **tối ưu trình tự** theo các nguyên tắc ở references (mục *Flow Optimization*), gồm:

- **Gá lỏng trước, siết chặt sau:** lắp toàn bộ mối ghép ở trạng thái gá lỏng (vặn tay) → căn chỉnh đồng tâm / vuông góc / thẳng đứng cho cả cụm → mới siết lực. Không bao giờ siết chặt trước khi căn chỉnh xong.
- **Tách căn chỉnh khỏi siết lực** thành nguyên công riêng khi cụm lớn (như tách "căn thẳng đứng & siết bích" thành 1 nguyên công riêng).
- **Chuẩn bị dưới mặt đất trước khi làm trên cao:** cắt/bấm cáp chằng, lắp sẵn cóc cáp, lắp đèn báo hiệu + luồn ống bảo vệ lên cụm *trước* khi dựng để giảm thao tác trên cao và tối ưu tải.
- **Gộp nguyên công** cùng vị trí/đồ gá để giảm số lần định vị lại.
- **Phân bố tải đối xứng:** lắp các chi tiết quanh tâm theo trình tự đối xứng (vd cánh 1→2→3→4 theo chiều kim đồng hồ) tránh lệch tâm gây lật/nghiêng.

Chia nguyên công theo **3 pha** để hỗ trợ phạm vi: **A — Chế tạo chi tiết** (cắt phôi, gá-hàn, NDT, làm sạch & sơn, khoan lỗ bích, nghiệm thu chi tiết), **B — Lắp ráp & Hiệu chỉnh**, **C — Thử nghiệm & Bàn giao**. Với `--B`, **bỏ toàn bộ pha A**, chỉ soạn B+C (đánh số B1…Bn, C1…Ck). Mặc định soạn cả A+B+C.

Trình bày kết quả là **Bảng tổng hợp tiến trình công nghệ tối ưu** (STT | Tên nguyên công | Thiết bị chủ chốt | Bậc thợ | Định mức phút). Xin CEO xác nhận trình tự trước khi viết chi tiết.

### Bước 3 — Soạn chi tiết từng nguyên công

Mỗi nguyên công gồm 3 phần (mẫu ở references):

- **I. Yêu cầu kỹ thuật** — các bước thao tác đánh số, kèm **thông số định lượng**: kích thước/dung sai (vd $1530 \pm 10\text{mm}$, $\Delta \le 5\text{mm}$), mô-men siết (vd M12: $45\div55\text{ Nm}$; M10: $25\div30\text{ Nm}$ — chốt theo cấp bền), quy tắc lắp ghép (bộ đệm đầy đủ, siết đối xứng chữ X, hướng cóc cáp, IP67…), và **quy tắc cốt lõi** in đậm khi có (vd "chưa siết chặt ở nguyên công này").
- **II. Thông số định mức & phân công** — Bậc thợ (vd 4/7), Định mức thời gian (phút), Nơi thực hiện.
- **III. Danh mục nguyên vật liệu & thiết bị công nghệ** — tách *Nguyên vật liệu* (chi tiết + vật tư tiêu hao, có SL) và *Thiết bị, trang bị công nghệ* (dụng cụ/đồ gá, có SL). Mọi mã VT phải khớp với BOM ở Bước 1.

Áp dụng nghiêm bộ quy tắc kỹ thuật ở references cho từng loại mối ghép (bu lông, cáp chằng + tăng đơ, điện DC, nâng hạ). Mỗi con số kỹ thuật phải truy được về thiết kế/tiêu chuẩn — đánh dấu giả định nếu phải suy luận.

### Bước 3b — (khi `--cad`) Đặc tả hình minh họa mỗi nguyên công

Với mỗi nguyên công, thêm mục **IV. Minh họa / Bản vẽ đề xuất** (mẫu khối ở references §D). Chọn **loại hình theo bản chất thao tác** (references §9): hình chiếu bằng cho định vị cụm, exploded + detail bubble cho mối bu lông nhiều đệm, sơ đồ siết đánh số chữ X cho siết lực, detail cóc cáp/ma ní cho rigging, sơ đồ nâng cho dựng cột, sơ đồ đấu nối cho điện DC, hình mớn nước cho thử nổi. Mỗi hình ghi: **mã hình `H-<mã NC>`**, loại hình, nội dung thể hiện, **callout bắt buộc** (số phải khớp mục I. YCKT), **nguồn** (trích bản vẽ chế tạo có sẵn — ghi mã; hoặc "dựng mới"), và chỗ chèn `[ẢNH: …]`. Skill **không vẽ** — chỉ đặc tả để họa viên dựng trong CAD (AutoCAD/Inventor/SolidWorks) và chèn.

### Bước 4 — Quy định chung & đóng gói

- Viết **I. Quy định chung về kỹ thuật và an toàn** (đào tạo, tuân thủ bản vẽ, bộ đệm chống nới lỏng, IP67, an toàn nâng hạ/điện/PCCC — mẫu ở references).
- Ghép **Bảng tổng hợp tiến trình** (Bước 2) + **toàn bộ nguyên công chi tiết** (Bước 3).
- Sản phẩm có thể ra **2 dạng** (xem Output Contract): bản chi tiết đầy đủ và/hoặc bản tổng hợp tối ưu gọn.

### Bước 4b — (khi `--json`) Sinh bản JSON kiểm tra quy trình

Xuất `QTCN-<sp>.json` theo schema references §E. Đây là **nguồn máy đọc để đối soát/kiểm tra quy trình về sau** (feed `verify` / `helix-p4-inspection` / audit), không phải bản đọc cho người. Điền đầy đủ:
- **`bom`** (VT, mã bản vẽ, tên, SL, vật liệu) — khớp Bước 1.
- **`operations[]`**: `id` (vd `B3`), `seq`, `name`, `phase` (A/B/C), `vt_refs`, `tech_requirements[]`, `core_rule`, `labor`, `materials[]`, `equipment[]`.
- **`checkpoints[]`** cho mỗi nguyên công — các **tiêu chí nghiệm thu định lượng** rút từ mục I. YCKT: `{param, nominal, tol, method}` (vd `{param:"mô-men siết M12", nominal:"45–55", unit:"Nm", method:"cờ lê lực"}`, `{param:"khoảng cách tâm 2 phao", nominal:"1530", tol:"±10mm", method:"thước cuộn đo 2 đầu"}`). Đây là phần **quan trọng nhất** để kiểm tra quy trình.
- **`cad_illustration`** cho mỗi nguyên công (khi có `--cad`): `{required, figure_id, view_type, shows, callouts[], source_drawing}` — chốt "nội dung minh họa CAD cần có".

Mọi con số trong JSON phải khớp bản Markdown; JSON là **hợp đồng kiểm tra**, sai lệch = lỗi.

**Codified (COD: Offload).** Việc bóc tách MD → JSON là xác định, đã được codify ở [scripts/helix/qtcn_to_json.py](../../../scripts/helix/qtcn_to_json.py) — **đừng chép tay JSON từ MD**. Chạy:
```bash
python scripts/helix/qtcn_to_json.py --in QTCN-<sp>.md --out <dir> --name QTCN-<sp> [--scope full|B] [--cad]
```
Script parse `# PHẦN A/B/C` → `## NGUYÊN CÔNG <id>` → `### I/II/III`, và **tự khai thác `checkpoints[]`** (mô-men Nm, dung sai ±, Δ đường chéo, khoảng cách mm, điện áp V, góc °, IP) từ text YCKT — kể cả khi tiêu chí nằm ở gạch đầu dòng con của một bước. `--scope B` loại phase A; `--cad` bật cờ `cad_included`. Sau khi chạy, **rà** các checkpoint mined (miner best-effort) và **bổ sung** `cad_illustration` (đặc tả hình là việc phán đoán, không codify) nếu chạy `--cad`.

### Bước 4c — (khi `--cad`) Sinh PHỤ LỤC sổ đăng ký hình minh họa

Sau khi có `QTCN-<sp>.json` với `cad_illustration` đầy đủ, sinh **PHỤ LỤC — Sổ đăng ký hình minh họa (figure register)** để họa viên **nhận việc một lượt**: bảng danh mục toàn bộ hình `H-A/B/C` (loại hình, thể hiện, callout, nguồn bản vẽ, ô ✔) + bảng **tổng hợp bản vẽ nguồn** (gom mỗi bản vẽ → các hình dùng, để trích 1 lượt) + tiến độ. **Codified (COD: Offload)** ở [scripts/helix/qtcn_figure_register.py](../../../scripts/helix/qtcn_figure_register.py) — sinh thẳng từ JSON, **khớp tuyệt đối thân QTCN**, đừng gõ tay:
```bash
python scripts/helix/qtcn_figure_register.py --in QTCN-<sp>.json --out QTCN-<sp>-figure-register.md --append QTCN-<sp>.md
```
`--append` chèn/thay phụ lục vào thân QTCN idempotent (giữa marker `<!-- QTCN-FIGURE-REGISTER -->`); `--out` ghi bản riêng để giao việc. Bảng nguồn tự **mở rộng dải** (vd `02.00–08.00` → mọi bản vẽ trung gian) và tách nhóm **hình dựng mới / từ hồ sơ**. Chạy lại sau mỗi lần đổi QTCN.

### Bước 5 — Rà soát & xuất bản

Trình CEO/cán bộ công nghệ rà: trình tự hợp lý? lực siết & dung sai đúng thiết kế? an toàn đủ? định mức sát thực tế? vật tư khớp BOM? Sau khi duyệt, có thể chuyển sang định dạng văn bản xưởng:
- `convert_md_to_docx` — xuất MD → DOCX để in/ký.
- Hoặc dựng theo **biểu mẫu QTCN chính thức** (khối tiêu đề từng nguyên công + ô ký Xưởng trưởng/An toàn/Kiểm tra/Công nghệ + dòng sửa đổi) — mẫu bảng ở references.

## Output Contract

| File | Nội dung |
|------|----------|
| `QTCN-<sản phẩm>-chi-tiet.md` | Bản chi tiết: từng nguyên công với I. YCKT / II. Định mức / III. Vật tư+Thiết bị (+ **IV. Minh họa** khi `--cad`). Phạm vi A+B+C, hoặc chỉ B+C khi `--B` |
| `QTCN-<sản phẩm>-tong-hop.md` | Bản tối ưu gọn: Quy định chung + Bảng tổng hợp tiến trình + nội dung cô đọng mỗi nguyên công (như `quy-trinh-tong-hop`) |
| `QTCN-<sản phẩm>.json` (khi `--json`) | Bản máy đọc: BOM+VT + nguyên công + thông số + **checkpoint nghiệm thu** + **spec minh họa CAD** — cơ sở đối soát/kiểm tra quy trình (schema §E) |
| `QTCN-<sản phẩm>-figure-register.md` (khi `--cad`) | **PHỤ LỤC sổ đăng ký hình**: danh mục toàn bộ hình `H-A/B/C` + bảng tổng hợp bản vẽ nguồn (trích 1 lượt) + tiến độ — sinh từ JSON qua `qtcn_figure_register.py`, cũng append được vào thân QTCN |
| `QTCN-<sản phẩm>.docx` (tùy chọn) | Văn bản xưởng chính thức để ký, qua `convert_md_to_docx` hoặc biểu mẫu form |

> Khi `--cad`: hình do họa viên dựng để riêng trong `figures/H-<mã NC>.<png/dwg>` và chèn vào MD tại chỗ `[ẢNH: …]`; JSON tham chiếu cùng `figure_id`; **PHỤ LỤC sổ đăng ký hình** (Bước 4c) là bảng giao việc tổng hợp toàn bộ hình + bản vẽ nguồn.

## Việc nào AI làm vs CEO quyết (COD)

| AI soạn (kiểm tra lại) | CEO/Công nghệ quyết (Core) |
|------------------------|----------------------------|
| Cấu trúc QTCN, đánh số bước, gom nguyên công, bảng tổng hợp | Trình tự công nghệ cuối cùng có khả thi với xưởng không |
| Áp bộ quy tắc kỹ thuật (đệm chống nới lỏng, siết chữ X, cóc cáp, IP67) | Lực siết / dung sai / cấp bền **chốt theo thiết kế thực** |
| Đề xuất định mức thời gian & bậc thợ từ chuẩn | Định mức thực tế của phân xưởng & duyệt vật tư |
| Soạn điều khoản an toàn theo môi trường | Phương án an toàn đặc thù & nghiệm thu |

- Phân rã + soạn thảo: **Offload** (AI).
- Trình tự, thông số chốt, duyệt: **Core** (CEO/Công nghệ).
- Xuất file MD/DOCX: **Default** (tự động).

## Tích hợp

- **Đầu vào:** `helix-p4-bom` / `/bom` (danh mục VT), `helix-p4-drawing` / `helix-detail-finalize` (bản vẽ), `helix-p4-assembly` (assembly instructions tiếng Anh → QTCN hình thức VN).
- **Đầu ra:** `helix-p4-handoff` → `forge-fabrication` (gói sản xuất), biên bản nghiệm thu, `verify`/`helix-p4-inspection` (gate kiểm tra lấy từ YCKT).
- **Xuất bản:** `convert_md_to_docx`.

## Giới hạn

- Skill **không thay** kỹ sư công nghệ duyệt khả thi gia công — nó soạn theo chuẩn, người ký chịu trách nhiệm kỹ thuật.
- **Lực siết, dung sai, cấp bền** là số tham chiếu/định hướng; **bắt buộc chốt theo bản vẽ & tiêu chuẩn áp dụng** trước khi ban hành.
- Định mức thời gian/bậc thợ là ước lượng khởi điểm — hiệu chỉnh theo năng lực phân xưởng thực tế.
- Mặc định cho **lắp ráp & hiệu chỉnh kết cấu cơ khí**; QTCN **gia công cắt gọt** (tiện/phay/hàn) dùng khung nguyên công khác — xem mục tương ứng ở references.
