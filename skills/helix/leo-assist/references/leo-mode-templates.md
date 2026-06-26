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
| **E** Documentation / BOM | draft tài liệu từ dữ liệu dự án | sinh BOM/spec/báo cáo nhanh | P4,Install |
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
```
[Phân loại: ...]
[MODE] DOCUMENT — draft tài liệu kỹ thuật
[DOCTYPE] Loại: [BOM / spec sheet / báo cáo thiết kế / hướng dẫn]
[SOURCE] Dữ liệu nguồn: [assembly / part / dữ liệu dự án — THƯỜNG]
[STRUCTURE] Section bắt buộc: [...]
[FIELDS] Trường bắt buộc: [part no, vật liệu, SL, nhà cung cấp, tiêu chuẩn]
[ASK] Sinh draft theo cấu trúc trên, đánh dấu rõ chỗ thiếu dữ liệu.
LƯU Ý: đây là DRAFT, kỹ sư review trước khi phát hành.
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
- [ ] Dữ liệu đưa lên là THƯỜNG/COTS — không có gì MẬT?
