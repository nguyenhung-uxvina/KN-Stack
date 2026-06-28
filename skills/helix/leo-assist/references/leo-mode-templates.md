# Leo AI — 6 MODE theo THẾ MẠNH THẬT (A–F)

> **Tái định khung (quan trọng):** Leo **KHÔNG sinh CAD tham số/production từ text** (text-to-CAD 2026 chỉ ra mesh STL/OBJ, vô dụng gia công). Leo = copilot **TRI THỨC · TÌM KIẾM · TÍNH TOÁN**. Mọi prompt chĩa vào 6 mode dưới; KHÔNG dùng Leo để "vẽ ra part".
> **Quan hệ với phase:** mode = *loại việc* (A–F); phase (P0–P4/QC/Install) = *khi nào*. Xem ma trận phase×mode trong SKILL.md. Sinh hình học concept → [[leo-prompt]] (mode concept-only, ưu tiên thấp nhất).
> **Ranh giới MẬT (mọi mode):** Leo = cloud SaaS → chỉ **THƯỜNG + COTS + tra cứu generic**. TUYỆT ĐỐI không đưa hình học/PLM MẬT (UUV/FCS) lên Leo. Cuối mỗi prompt liệt kê **GIẢ ĐỊNH** để CEO kiểm.

| Mode | Thế mạnh | Dùng khi | Phase chính |
|---|---|---|---|
| **A** Part Search & Reuse | lõi giá trị Leo (60–80% part vẽ mới là trùng lặp) | cần 1 part → tìm trước khi vẽ | P2,P3 ⭐ |
| **B** Engineering Q&A | trả lời có cite từ 1M+ nguồn | tra tiêu chuẩn/fit/quy tắc | P0,P1,P4,QC,Install |
| **C** Calculation / Sizing | tính hiện công thức + logic + nguồn | thay bảng tính (ứng suất/nhiệt/lưu chất) | P1,P3,QC,Install |
| **D** DFM / Standards Inspect | soi vi phạm, mỗi flag có cite | review thiết kế trước phát hành | P3,P4 |
| **E** Documentation / BOM | E1 9-point summary · E2 datasheet/BOM-text · E3 gắp mfg-data có sẵn (KHÔNG làm quy trình CN/QMS/nghiệm thu) | đặc tả thiết kế + tài liệu nhanh | P1,P4,Install |
| **F** Material Selection | so vật liệu có cite + trade-off | chọn vật liệu theo ràng buộc | P2,P3 |

---

## A. PART SEARCH & REUSE — *ưu tiên trước mọi thiết kế mới*
```
[Phân loại: THƯỜNG | MẬT→generic/COTS only]
[MODE] PART SEARCH — tìm & tái dùng
[FUNCTION] Part làm gì: [chức năng + động học]
[ENVELOPE] Không gian/mating: [kích thước bao, lỗ bắt, ren, Ø trục/ống, khoảng cách tâm]
[SPEC] Ràng buộc: [tải, vật liệu, nhiệt độ, tiêu chuẩn cần đạt]
[SOURCE] Tìm trong: [PDM nội bộ (THƯỜNG) / kho vendor 120M / cả hai]
[ASK]
1. Liệt kê 5 part ứng viên, xếp theo độ khớp hình học (%).
2. Mỗi ứng viên: so kích thước vs envelope, độ phổ biến, revision/drawing/manufacturing data nếu có.
3. Kết luận: tái dùng được không? Sửa nhỏ thì sửa gì? Chỉ thiết kế mới khi không có khớp ≥[85]%.
[GIẢ ĐỊNH] [...]
```

## B. ENGINEERING Q&A — *có cite, không bịa*
```
[Phân loại: ...]
[MODE] ENGINEERING Q&A
[QUESTION] [câu hỏi kỹ thuật chính xác]
[CONTEXT] [vật liệu / quá trình / điều kiện liên quan]
[ASK]
- Trả lời ngắn gọn; nêu rõ tiêu chuẩn/điều khoản/datasheet làm nguồn cho TỪNG số liệu.
- Không có nguồn đáng tin → nói thẳng "không đủ nguồn", KHÔNG suy đoán.
- Có nhiều giá trị/quan điểm → liệt kê + nguồn từng cái.
```

## C. CALCULATION / SIZING — *thay bảng tính*
```
[Phân loại: ...]
[MODE] CALCULATION — hiện công thức + logic + nguồn
[GOAL] Tính/định cỡ: [ứng suất / FoS / độ dày / lưu lượng / nhiệt...]
[KNOWNS] [tải, kích thước, vật liệu, điều kiện biên — KÈM ĐƠN VỊ]
[UNKNOWN] [biến cần giải]
[ASK]
1. Chọn công thức/tiêu chuẩn phù hợp, giải thích vì sao, trích nguồn.
2. Hiện đầy đủ bước tính (và logic Python nếu có) — không cho số "hộp đen".
3. Lấy cơ tính vật liệu/hệ số từ datasheet CÓ NGUỒN.
4. Kết quả + FoS + kiểm đơn vị + độ nhạy với giả định chính.
[GIẢ ĐỊNH] [liệt kê để kiểm tra]
```

## D. DFM / STANDARDS INSPECTION — *Leo Inspect*
```
[Phân loại: THƯỜNG — KHÔNG đính kèm hình học MẬT]
[MODE] INSPECT — soi DFM + tiêu chuẩn cho thiết kế đã có
[SUBJECT] [part/assembly — mô tả; THƯỜNG]
[PROCESS] Chế tạo bằng: [FDM / CNC / sheet metal / đúc / tiện...]
[STANDARDS] Áp tiêu chuẩn: [ISO / ASME / TCVN / nội bộ...]
[ASK]
1. Liệt kê vi phạm DFM (draft, wall, bán kính, dung sai không chế tạo được...).
2. Vấn đề chọn part / vật liệu / lắp ghép.
3. Vi phạm tiêu chuẩn → MỖI flag cite tiêu chuẩn/điều khoản cụ thể.
Xếp theo mức nghiêm trọng. Ưu tiên gợi ý part đã validated thay vì tạo mới.
[GIẢ ĐỊNH] [...]
> Lưu ý: Leo soi QUY PHẠM/DFM; thẩm định HÌNH HỌC bản vẽ vẫn CEO + CAD.
```

## E. DOCUMENTATION / BOM / SPEC

> **Ranh giới tài liệu của Leo (research-confirmed):** Leo CHỈ sinh tài liệu **giai đoạn thiết kế (upstream)** — 3 việc E1/E2/E3 dưới. Leo **KHÔNG** sinh: ❌ Quy trình công nghệ chế tạo/routing · ❌ Sổ tay QLCL/QMS ISO 9001 · ❌ Quy trình thử nghiệm/nghiệm thu/inspection plan. Ba thứ đó → skill nội bộ: `forge-fabrication` F0 (quy trình công nghệ TCVN) · `helix-p4-inspection` (nghiệm thu) · `erp-quality` (QLCL) — chạy LOCAL, an toàn MẬT. Đừng ép Leo làm; nó sẽ trả lời chung chung vô dụng.

### E1. 9-POINT ENGINEERING SUMMARY (Leo Ideation) — *đặc tả thiết kế từ ý tưởng*
```
[Phân loại: THƯỜNG | MẬT→trừu tượng hóa, không tên khí tài]
[MODE] LEO IDEATION — sinh Bản tóm tắt kỹ thuật 9 điểm
[IDEA] Mô tả sản phẩm 1 đoạn: [chức năng + bối cảnh dùng + ràng buộc chính]
[KNOWNS] Tải/kích thước/môi trường/vật liệu đã biết: [... kèm đơn vị]
[ASK] Sinh 9-point engineering summary đầy đủ:
 (1) Giới thiệu (2) Tổng quan sản phẩm (3) Yêu cầu cơ khí (4) Yêu cầu điện
 (5) Yêu cầu phần mềm (6) Giao diện/công thái (7) Môi trường & điều kiện
 (8) An toàn & tuân thủ (cite tiêu chuẩn) (9) Phụ lục bản vẽ.
 Đánh dấu rõ mục nào "N/A" và mục nào thiếu dữ liệu đầu vào. Xuất được PDF/Word.
[GIẢ ĐỊNH] [...]
LƯU Ý: đây là ĐẶC TẢ thiết kế (input cho helix-p1-requirements), KHÔNG phải quy trình chế tạo.
```

### E2. TECH SUMMARY / DATASHEET / BOM-TEXT — *draft tài liệu kỹ thuật*
```
[Phân loại: ...]
[MODE] DOCUMENT — draft datasheet / spec sheet / BOM-text / báo cáo thiết kế
[DOCTYPE] Loại: [datasheet 1 part / spec sheet cụm / BOM dạng bảng / design report]
[SOURCE] Dữ liệu nguồn: [part/assembly/thông số dự án — THƯỜNG/COTS]
[STRUCTURE] Section bắt buộc: [...]
[FIELDS] Trường bắt buộc: [part no, vật liệu, SL, nhà cung cấp, tiêu chuẩn, khối lượng]
[ASK] Sinh draft theo cấu trúc trên; mỗi số kỹ thuật kèm nguồn; đánh dấu rõ chỗ thiếu dữ liệu.
       Xuất PDF/Word/Google Docs để chia sẻ nhóm.
[GIẢ ĐỊNH] [...]
LƯU Ý: DRAFT — kỹ sư review trước khi phát hành; số liệu → CEO/CAD verify trước khi vào hồ sơ MẬT.
```

### E3. RETRIEVE EXISTING MANUFACTURING DATA — *gắp dữ liệu sản xuất CÓ SẴN (không viết mới)*
```
[Phân loại: THƯỜNG — chỉ chạy được nếu PLM/PDM nội bộ đã kết nối Leo]
[MODE] PART SEARCH → PULL MFG DATA (biến thể của Mode A)
[PART] Tìm part/cụm: [mô tả + envelope/mating thật]
[ASK]
1. Tìm part khớp trong PDM/PLM nội bộ.
2. Với mỗi part khớp, KÉO RA dữ liệu sản xuất đã kiểm định ĐI KÈM:
   revision history · bản vẽ liên quan · manufacturing data · nhà cung cấp đã duyệt.
3. KHÔNG tự "viết" quy trình mới — chỉ truy xuất cái đã tồn tại & validated.
[GIẢ ĐỊNH] [...]
LƯU Ý: đây là tái dùng hồ sơ sản xuất CŨ; để LẬP quy trình công nghệ MỚI → forge-fabrication F0 (local).
```

## F. MATERIAL SELECTION
```
[Phân loại: ...]
[MODE] MATERIAL SELECTION — chọn vật liệu có cite
[PART] [part + chức năng]
[REQUIREMENTS] Tải/ứng suất: [...]; Nhiệt: [...]; Môi trường: [mồ hôi/UV/muối/hóa chất];
Ưu tiên: [cost / khối lượng / độ bền / tính chế tạo]
[PROCESS] [FDM / CNC / đúc / tiện...]
[ASK]
1. Đề 3–5 vật liệu ứng viên, bảng so cơ tính CÓ NGUỒN (datasheet/tiêu chuẩn).
2. Trade-off từng loại theo ưu tiên đã nêu.
3. Khuyến nghị + lý do + rủi ro của lựa chọn.
[GIẢ ĐỊNH] [...]
```

---

## Router meta-prompt — *chọn mode + điền template tự động*
> Dán vào Claude/LLM, điền 1 dòng tác vụ → nhận về prompt Leo đúng mode.
```
Bạn là chuyên gia điều phối tác vụ cho Leo AI (getleo.ai).
Leo = copilot TRI THỨC/TÌM KIẾM/TÍNH TOÁN cơ khí, KHÔNG phải công cụ sinh CAD production.
Thế mạnh: (A) part-search & reuse, (B) Q&A có cite, (C) tính toán hiện logic,
(D) inspect DFM/tiêu chuẩn, (E) draft tài liệu/BOM, (F) chọn vật liệu.

Từ tác vụ một dòng của tôi:
1. Xác định Leo có phù hợp không. Nếu tác vụ là "vẽ hình học production từ text"
   → CẢNH BÁO Leo không làm được; tách thành (part-search + tính + concept) rồi dựng CAD ngoài (helix-cad-bridge).
2. Chọn 1–2 mode (A–F) phù hợp nhất.
3. Điền template tương ứng; suy ra thông số định lượng + giả định (đánh dấu cần xác minh).
4. Nhắc ranh giới: chỉ dữ liệu THƯỜNG/COTS/generic — KHÔNG hình học/PLM MẬT.

Tác vụ: [__1 dòng__]
```

## Checklist trước khi gửi Leo
- [ ] Tác vụ khớp 1 trong 6 mode? (Nếu "vẽ part" → sai công cụ, đổi sang part-search A.)
- [ ] Mode A: đã cho envelope/mating thật để search hình học?
- [ ] Mode B/C/F: đã ÉP trích nguồn cho mọi số liệu?
- [ ] Mode C: đã cho knowns + đơn vị + yêu cầu hiện công thức?
- [ ] Mode D: đã nêu process + tiêu chuẩn áp dụng?
- [ ] Mode E: tài liệu cần thuộc 3 việc Leo làm (E1/E2/E3)? Nếu là **quy trình công nghệ / QMS / nghiệm thu** → KHÔNG dùng Leo, chuyển `forge-fabrication` F0 / `helix-p4-inspection` / `erp-quality`.
- [ ] Dữ liệu đưa lên là THƯỜNG/COTS — không có gì MẬT?
