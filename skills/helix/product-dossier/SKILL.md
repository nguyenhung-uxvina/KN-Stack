---
name: product-dossier
description: Pipeline trọn gói từ một THƯ MỤC bản vẽ sản phẩm (PDF + DXF/DWG) ra bộ hồ sơ sản xuất. Chỉ cần đưa địa chỉ thư mục; hệ thống tự trích xuất bản vẽ → lập BOM + "data spine" → để CEO chọn xuất Quy trình công nghệ (QTCN), Định mức kinh tế – kỹ thuật (ĐMKTKT), Sổ tay Quản lý chất lượng (QLCL/QMS), BOM, Life-Cycle Cost, phiếu kiểm tra nghiệm thu, datasheet chi tiết — rồi đóng gói hồ sơ + xuất DOCX. Triggers on "hồ sơ sản phẩm", "product dossier", "từ thư mục bản vẽ", "tài liệu sản xuất từ CAD", "quy trình + định mức + sổ tay chất lượng", "pipeline sản xuất", "xuất bộ tài liệu sản phẩm", "định mức kinh tế kỹ thuật", "ĐMKTKT", "sổ tay chất lượng", "sổ tay QLCL", "QMS", hoặc khi CEO đưa một thư mục chứa PDF/DXF/DWG và muốn ra tài liệu sản xuất.
---

# Product Dossier — Từ thư mục bản vẽ → bộ hồ sơ sản xuất (pipeline)

Một **orchestrator**: đầu vào duy nhất là **địa chỉ thư mục** chứa file bản vẽ sản phẩm (`.pdf` + `.dxf`/`.dwg`). Pipeline tự trích xuất, hợp nhất thành **data spine**, rồi để CEO **chọn** các tài liệu cần xuất và sinh chúng từ cùng một nguồn dữ liệu — đảm bảo mọi tài liệu **nhất quán số liệu**.

Skill này **không tự làm lại** việc của các skill con — nó **điều phối**: [mech-drawing-extract](../../extract/mech-drawing-extract/SKILL.md) (trích xuất), [qtcn](../qtcn/SKILL.md) (quy trình công nghệ), [bom](../../design/bom/SKILL.md) / `helix-p4-bom`, [lcc](../../design/lcc/SKILL.md) / [forge-cost](../../forge/forge-cost/SKILL.md) (giá thành), [verify](../../design/verify/SKILL.md) / `helix-p4-inspection` (nghiệm thu). Hai bộ tài liệu **mới** (ĐMKTKT, Sổ tay QLCL) được định nghĩa ngay trong references của skill này.

Chi tiết khối & schema: [references/pipeline-blocks.md](references/pipeline-blocks.md). Mẫu ĐMKTKT: [references/dmktkt-template.md](references/dmktkt-template.md). Mẫu Sổ tay QLCL: [references/qms-template.md](references/qms-template.md). **Đọc trước khi chạy khối tương ứng.**

## Ý tưởng cốt lõi — Data Spine

Toàn bộ giá trị nằm ở chỗ **một nguồn dữ liệu duy nhất** (`product-spine.json`) nuôi mọi tài liệu:

```
                                    ┌─→ QTCN (quy trình + checkpoint + định mức lao động)
Thư mục PDF/DXF/DWG                 │
  → EXTRACT → BOM + specs → SPINE ──┼─→ ĐMKTKT  (định mức vật tư + lao động + đơn giá → giá thành)
                                    │
                                    └─→ Sổ tay QLCL (control plan từ checkpoint QTCN)
```

**QTCN `--json` là xương sống**: nó chứa BOM+VT, định mức lao động (giờ công/nguyên công) và **checkpoint nghiệm thu**. ĐMKTKT lấy định mức lao động + vật tư từ đây; Sổ tay QLCL lấy checkpoint từ đây. ⇒ Nếu CEO chọn ĐMKTKT hoặc QLCL mà **chưa** chọn QTCN, pipeline **tự chạy QTCN `--json` ngầm** để lấy spine (không bắt buộc xuất bản in QTCN).

## Đầu vào

**Bắt buộc:** đường dẫn **thư mục** chứa bản vẽ. Chấp nhận: nhiều cặp `Trang-N.pdf` + `Trang-N.dxf`, hoặc một `.dwg` gói cả sản phẩm, hoặc trộn. Nếu thiếu, hỏi CEO đúng 1 câu: "Thư mục bản vẽ ở đâu?".

**Tùy chọn (hỏi ở P3 nếu chưa có):** tên sản phẩm & mã hiệu; đơn giá vật tư / đơn giá giờ công (cho ĐMKTKT — nếu chưa có thì để placeholder và đánh dấu `[CẦN ĐƠN GIÁ]`); cấp bền bu lông / dung sai / môi trường khai thác (cho QTCN — xem qtcn Đầu vào).

## Pipeline (5 pha)

### P0 — Preflight (quét thư mục)
Liệt kê file, ghép cặp PDF↔DXF theo tên, phát hiện `.dwg`. Xác định số tờ, đoán tên sản phẩm từ tiêu đề/tên file. Báo CEO bảng "N tờ, M cặp PDF+DXF, K DWG" và tên sản phẩm dự kiến để xác nhận.

### P1 — Extract (Offload, codified)
Chạy `mech-drawing-extract` / `parse_mech_drawing.py` cho **từng** bản vẽ → per-sheet JSON (title block, dimensions, layers, specs, TCVN3 decode). Đọc **trang bảng kê / bản lắp** trước để lấy BOM (mã bản vẽ, tên, SL, vật liệu). Xử lý PDF scan/mojibake theo đúng rule của mech-drawing-extract (đọc DXF, không tin PDF garbled).

### P2 — Data Spine (hợp nhất, codified)
Chạy cầu nối codified [cad-pipeline/scripts/extract/extract_to_qtcn_seed.py](../../../cad-pipeline/scripts/extract/extract_to_qtcn_seed.py) `--extracted <extracted/>` → **`qtcn-seed.json`**: sản phẩm + principal particulars + BOM (**VT gán tự động** ↔ mã bản vẽ ↔ tên ↔ SL ↔ vật liệu) + specs mỗi chi tiết (section/plate/tolerances/key-dims) + vật tư mua + flags. Đây là **lõi của `product-spine.json`** (bổ sung thêm `relationships` mối ghép + `est_mass` do skill suy luận) và là **đầu vào `--seed` trực tiếp cho khối QTCN**. Là **hợp đồng dữ liệu** — mọi tài liệu ở P4 truy về đây; lệch số = lỗi.

### P3 — Menu CEO (Core, dùng AskUserQuestion)
Trình CEO **danh mục tài liệu** (multi-select) — xem §Menu. CEO chọn cần xuất gì; hỏi thêm tham số riêng của lựa chọn (vd QTCN full A+B+C hay `--B`; có đơn giá cho ĐMKTKT không; có xuất DOCX không). **Không tự quyết thay CEO** danh mục & phạm vi.

### P4 — Generate (fan-out từ spine)
Với mỗi lựa chọn, chạy khối tương ứng, **truyền spine làm đầu vào** (không trích xuất lại). Thứ tự ưu tiên: **QTCN trước** (vì nuôi ĐMKTKT & QLCL) → ĐMKTKT → QLCL → còn lại. Bảng ánh xạ ở §Menu.

### P5 — Rollup & xuất bản
Ghi tất cả vào `<thư mục>\HO-SO-SAN-PHAM\`; lập **`INDEX.md`** liên kết mọi tài liệu + spine. Nếu CEO chọn DOCX: chạy `convert_md_to_docx` cho từng tài liệu. Báo cáo: đã xuất gì, số liệu chốt (số chi tiết, tổng giờ công, số checkpoint, giá thành nếu có), và các mục `[CẦN …]` còn chờ CEO.

## Menu tài liệu (P3) → khối sinh (P4)

| # | Tài liệu | Khối / skill sinh | Nguồn từ spine |
|---|----------|-------------------|----------------|
| 1 | **Quy trình công nghệ (QTCN)** | `qtcn` (mặc định `--cad --json`; hỏi full A+B+C hay `--B`) | BOM+VT, quan hệ lắp ghép |
| 2 | **Định mức kinh tế – kỹ thuật (ĐMKTKT)** | khối `dmktkt` (references dmktkt-template) | BOM (vật tư) + QTCN.json (giờ công) + đơn giá |
| 3 | **Sổ tay Quản lý chất lượng (QLCL/QMS)** | khối `qms` (references qms-template) | checkpoint[] + YCKT từ QTCN.json |
| 4 | Bill of Materials (BOM.md) | `bom` / `helix-p4-bom` | BOM |
| 5 | Life-Cycle Cost / đơn giá | `lcc` / `forge-cost` | BOM + ĐMKTKT |
| 6 | Phiếu kiểm tra – nghiệm thu | `verify` / `helix-p4-inspection` | checkpoint[] |
| 7 | Datasheet từng chi tiết | `mech-drawing-extract` (bản MD/chi tiết) | per-sheet JSON |
| — | *(cờ)* Xuất **DOCX** | `convert_md_to_docx` | mọi MD đã chọn |

CEO có thể chọn **nhiều mục**; QTCN được ưu tiên chạy nếu mục 2/3/6 được chọn.

## Output Contract

| File/thư mục | Nội dung |
|--------------|----------|
| `HO-SO-SAN-PHAM\product-spine.json` | Xương sống dữ liệu (BOM+VT+specs) — nguồn của mọi tài liệu |
| `…\QTCN-<sp>-*.md` + `.json` | Quy trình công nghệ (khi chọn) — từ skill `qtcn` |
| `…\DMKTKT-<sp>.md` + `.json` | Định mức kinh tế – kỹ thuật (khi chọn) |
| `…\SO-TAY-QLCL-<sp>.md` | Sổ tay Quản lý chất lượng + Quality Plan (khi chọn) |
| `…\BOM.md`, `…\LCC-*.md`, `…\phieu-kiem-tra-*.md`, `…\datasheets\*` | Các tài liệu tùy chọn |
| `…\*.docx` | Bản in/ký (khi chọn DOCX) |
| `HO-SO-SAN-PHAM\INDEX.md` | Mục lục hồ sơ, liên kết tất cả |

## Việc nào AI làm vs CEO quyết (COD)

| AI (Offload/Default) | CEO/Công nghệ (Core) |
|----------------------|----------------------|
| Quét thư mục, trích xuất, lập spine, hợp nhất BOM | Xác nhận tên sản phẩm & phạm vi |
| Sinh tài liệu từ spine theo template, giữ nhất quán số liệu | **Chọn danh mục tài liệu** & tham số (QTCN full/`--B`, có đơn giá…) |
| Đề xuất định mức/đơn giá từ chuẩn, đánh dấu `[CẦN …]` | Chốt **đơn giá, lực siết, dung sai, tiêu chuẩn nghiệm thu** |
| Đóng gói INDEX, xuất DOCX | Duyệt & ký ban hành |

- Trích xuất + lập spine + sinh thảo: **Offload/Default**. Chọn tài liệu + chốt số liệu kinh tế-kỹ thuật + duyệt: **Core**.

## Nguyên tắc thực thi

1. **Một nguồn sự thật:** mọi tài liệu đọc từ `product-spine.json` (và `QTCN.json`). Không nhập tay lại số đã có. Lệch số giữa các tài liệu = lỗi phải sửa ở spine.
2. **Không bịa số kinh tế-kỹ thuật:** đơn giá/định mức chưa có → placeholder `[CẦN ĐƠN GIÁ]` / `[CẦN ĐỊNH MỨC]`, không đoán bừa.
3. **Truy xuất nguồn gốc:** mọi dòng vật tư/nguyên công/điểm kiểm tra gắn **mã VT / mã bản vẽ / mã nguyên công** để đối soát chéo.
4. **Bám rule skill con:** QTCN theo qtcn-engineering-rules (gá lỏng→căn chỉnh→siết, IP67, bộ đệm…); trích xuất theo mech-drawing-extract (TCVN3, mojibake PDF, bare-number trap).

## Giới hạn

- Chất lượng hồ sơ phụ thuộc chất lượng bản vẽ đầu vào; bản vẽ scan/mojibake cho ít dữ liệu tự động hơn (đọc DXF là chính).
- ĐMKTKT ra **khung định mức + công thức**; con số đơn giá & định mức cuối **CEO/phòng kế hoạch chốt**.
- Sổ tay QLCL sinh **Quality Plan theo sản phẩm** từ checkpoint; **không thay** hệ thống QMS cấp công ty (ISO 9001 toàn doanh nghiệp) — nó là sổ tay chất lượng cho một sản phẩm/lô sản xuất.
- Không tự ban hành: người ký chịu trách nhiệm kỹ thuật & pháp lý.
