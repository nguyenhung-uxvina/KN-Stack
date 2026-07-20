# Leo AI — Bộ template prompt theo phase (P0–P4 + QC + Lắp đặt)

> Điền các ô `[...]`. Mọi template tuân 5 nguyên tắc Leo: load định lượng+FoS · interface thật · process+thông số · **bắt buộc trích nguồn** · **search-before-generate**.
> Dòng đầu LUÔN khai **Phân loại**. MẬT → trừu tượng hóa, KHÔNG tên khí tài / KHÔNG upload bản vẽ/PLM. Cuối prompt LUÔN liệt kê **GIẢ ĐỊNH** để CEO kiểm.
> Output Leo: markdown, tiếng Việt, có bảng, mỗi số liệu có nguồn.

---

## P0 — PRE-STUDY / Cơ hội (→ forge-pre-study · odi · forge-cost)
**Leo làm:** tra tiêu chuẩn + sản phẩm/giải pháp tương đương, khả thi sơ bộ, COTS có sẵn + ước cost generic.
```
[Phân loại: THƯỜNG | MẬT→generic only]
Persona: kỹ sư khảo sát khả thi cơ khí, ưu tiên độ tin cậy nguồn.
Bối cảnh: cần đánh giá nhanh khả thi [chức năng/sản phẩm 1 câu], môi trường [nhiệt/ẩm/biển...].
Yêu cầu Leo (search-before-generate, trích nguồn từng mục):
1. Có GIẢI PHÁP/SẢN PHẨM tiêu chuẩn nào đang giải bài toán [chức năng]? Liệt kê 3 + nguồn.
2. TIÊU CHUẨN/quy phạm áp dụng (ISO/MIL/ASTM/TCVN)? Trích số hiệu.
3. Khả thi sơ bộ: tải/kích thước bậc thang [order-of-magnitude], rào cản kỹ thuật chính.
4. COTS sẵn có (vendor part) cho khối chức năng chính + dải giá generic.
Output: bảng [Phương án | Nguồn | Ưu | Nhược | COTS/Giá]. GIẢ ĐỊNH: [...].
```

## P1 — REQUIREMENTS / Làm rõ yêu cầu (→ helix-p1-requirements · helix-p1-validate)
**Leo làm:** liệt kê tiêu chuẩn áp dụng + **giá trị mục tiêu có cite**, tra interface COTS, điều kiện môi trường.
```
[Phân loại: ...]
Persona: kỹ sư yêu cầu, am hiểu [lĩnh vực] + tiêu chuẩn liên quan.
Bối cảnh: lập danh mục yêu cầu cho [cụm/chi tiết]; load case: [lực/khối lượng, hướng, tĩnh/động], FoS≥[..].
Interface thật: [lắp vào Ø__/ren__/chốt__]. Môi trường: [25–55°C, ẩm, muối...].
Yêu cầu Leo (trích nguồn từng số):
1. TIÊU CHUẨN áp dụng cho [chức năng/an toàn/môi trường] — số hiệu + điều khoản.
2. GIÁ TRỊ MỤC TIÊU đề xuất cho [tham số]: dải hợp lý + công thức/nguồn.
3. Kích thước/giới hạn từ COTS sẽ ràng buộc thiết kế (ray/bạc đạn/fastener tiêu chuẩn).
4. Điều kiện môi trường định lượng (ăn mòn, nhiệt) + tiêu chuẩn thử.
Output: bảng [Yêu cầu | Giá trị mục tiêu | Nguồn | D/W]. GIẢ ĐỊNH: [...].
```

## P2 — CONCEPT / Thiết kế ý tưởng (→ helix-concept-generate)
**Leo làm:** tìm **nguyên lý/part** hiện thực, chọn vật liệu, DFMA trade-off, concept mesh (chỉ THƯỜNG).
```
[Phân loại: ...]
Persona: kỹ sư concept, ưu tiên DFMA + tái sử dụng part chuẩn.
Bài toán (solution-neutral): đạt [chức năng] dưới [load+FoS], interface [..], môi trường [..].
Yêu cầu Leo (search-before-generate):
1. Đề xuất 2–3 NGUYÊN LÝ làm việc + part/cụm tiêu chuẩn hiện thực mỗi nguyên lý (vendor/PLM).
2. So sánh DFMA (số chi tiết, gia công, lắp ráp, chi phí) — bảng trade-off có nguồn.
3. Chọn VẬT LIỆU sơ bộ cho phương án tốt + lý do (cơ tính, ăn mòn) trích nguồn.
4. [THƯỜNG] Sinh mesh concept để hình dung — GHI RÕ chỉ là ideation, không production.
Output: bảng nguyên lý + DFMA + vật liệu (có nguồn). GIẢ ĐỊNH: [...].
⚠ Mesh concept KHÔNG dùng cho gia công → dựng tham số bằng helix-cad-bridge.
```

## P3 — EMBODIMENT / Thiết kế tổng thể ⭐ (→ helix-p3-layout/-dfx/-bom)
**Leo MẠNH NHẤT:** part-search COTS + tính sức bền/sizing có cite + vật liệu + DFMA + BOM standard-part.
```
[Phân loại: ...]
Persona: kỹ sư embodiment, ưu tiên tái sử dụng part validated.
Cụm: [tên]. Load case: [lực/mômen, hướng, tĩnh/động], FoS≥[..]. Interface: [Ø__h7, ren__, ray__].
Yêu cầu Leo (search-before-generate, trích nguồn):
1. ⭐ TÌM PART TIÊU CHUẨN khớp [load + interface]: bạc đạn / ray tuyến tính / fastener / vú mỡ /
   gối đỡ — liệt kê vendor part + thông số + lý do fit. (vd "ray tuyến tính chịu [..]N, hành trình [..]mm").
2. TÍNH sức bền/sizing cho chi tiết chịu lực: công thức + chạy số + FoS + nguồn (HIỆN logic).
3. Chọn VẬT LIỆU + xử lý nhiệt (cơ tính cần, ăn mòn) có nguồn; gợi ý thay thế.
4. DFMA review: cảnh báo over-engineering, gợi part reuse.
5. BOM: phân biệt part MUA (COTS Leo tìm) vs CHẾ TẠO.
Output: bảng [Part | Vendor/Spec | Nguồn] + bảng tính sức bền + BOM mua/chế tạo. GIẢ ĐỊNH: [...].
→ Part Leo tìm → forge-fabrication "mua ngoài"; calc → helix-p3-dfx verify; hình học → helix-cad-bridge.
```

## P4 — DETAIL / Thiết kế chi tiết (→ helix-p4-drawing/-inspection)
**Leo làm:** kiểm **quy phạm** (GD&T/ASME/ISO) có cite, tra dung sai/ren/fit, verify vendor-part BOM. (KHÔNG thẩm định hình học.)
```
[Phân loại: ...]
Persona: kỹ sư chi tiết, am hiểu GD&T/dung sai/ren.
Chi tiết: [tên], lắp ghép [trục Ø__h7 ↔ bạc Ø__H7/F7], ren [M__], vật liệu [..].
Yêu cầu Leo (trích nguồn):
1. Cặp lắp ghép [Ø__] nên dùng KIỂU LẮP nào (h7/H7/F7/m6...) cho [chức năng quay/ép]? — bảng tra + nguồn (ISO 286).
2. GD&T/quy phạm áp dụng cho [chi tiết] (độ đồng tâm, độ phẳng) — điều khoản + nguồn (ASME Y14.5/ISO 1101).
3. Tra ren [M__]: thông số, mô-men siết khuyến nghị, nguồn.
4. Verify vendor-part trong BOM còn hợp lệ (còn hàng/thay thế).
Output: bảng [Đặc trưng | Quy phạm/Giá trị | Nguồn]. GIẢ ĐỊNH: [...].
⚠ Leo kiểm QUY PHẠM; hình học/dung sai tới hạn vẫn CEO+CAD chốt.
```

## QC — Nghiệm thu / Kiểm tra (→ helix-p4-inspection · erp-quality)
**Leo làm:** tiêu chí nghiệm thu + phương pháp kiểm (VT/PT/UT/NDT) theo tiêu chuẩn, tính đo.
```
[Phân loại: ...]
Persona: kỹ sư KCS/QC, am hiểu NDT + tiêu chuẩn nghiệm thu.
Đối tượng kiểm: [mối hàn chịu lực / kích thước tới hạn Ø__h7 / lớp phủ...]. Vật liệu [..].
Yêu cầu Leo (trích nguồn):
1. TIÊU CHÍ NGHIỆM THU cho [đối tượng] theo tiêu chuẩn nào? (vd mối hàn: ISO 5817 mức chất lượng) — điều khoản.
2. PHƯƠNG PHÁP kiểm phù hợp (VT/PT/UT/RT/đo) + mức lấy mẫu/AQL — nguồn.
3. Dụng cụ đo + cấp chính xác cho [dung sai] (panme/đồng hồ so) — nguồn.
4. Công thức/tính toán liên quan (vd chiều cao mối góc a≥0,7t) — trích nguồn.
Output: bảng [Đặc trưng | Tiêu chí | Phương pháp | Tiêu chuẩn]. GIẢ ĐỊNH: [...].
```

## LẮP ĐẶT — Installation / Assembly (→ forge-fabrication · helix-p4-handoff)
**Leo làm:** trình tự lắp, **mô-men siết/preload có cite**, fit/căn chỉnh, checklist ATLĐ.
```
[Phân loại: ...]
Persona: kỹ sư lắp đặt, am hiểu mối ghép ren + căn chỉnh.
Cụm lắp: [tên], gồm [bu-lông M__ cấp__, ray__, bạc__, ổ__]. Tải làm việc [..].
Yêu cầu Leo (trích nguồn):
1. TRÌNH TỰ lắp hợp lý (cụm con → trung → tổng) + điểm dễ sai.
2. MÔ-MEN SIẾT / preload cho bu-lông [M__ cấp__] theo [khô/bôi trơn] — giá trị + nguồn (vd VDI 2230/bảng siết).
3. FIT/căn chỉnh: dung sai lắp, khe hở, độ đồng trục cho [ray/ổ] — nguồn.
4. Checklist AN TOÀN lắp (nâng cụm [__]kg, kẹp, mô-men dụng cụ).
Output: bảng [Bước | Nội dung | Mô-men/Fit | Tiêu chuẩn] + checklist ATLĐ. GIẢ ĐỊNH: [...].
```

---

## RECIPE — `leo-part-brief`: thiết kế 1 chi tiết nhỏ HOÀN CHỈNH (THƯỜNG, FDM)
> Khi 1 deliverable cần **cả chuỗi mode** chứ không 1 mode rời (vd phụ kiện gym, jig/gá, tay cầm, đồ đeo):
> xâu 6 bước dưới thành MỘT brief. Đây là "hình dạng" của một brief CPTRF đa-mode chuẩn.
> Mỗi bước = 1 mode leo-assist; chạy tuần tự, kết quả bước trước là input bước sau.

```
Bước 0 — CLASSIFY: THƯỜNG? (đồ cá nhân/gym/R&D không nhạy cảm) → tiếp. MẬT → dừng, chuyển helix-cad-bridge.

Bước 1 — SEARCH FIRST  [Mode A]  → có COTS đáp ứng chức năng không? Liệt kê 3 + kết luận MUA vs CHẾ TẠO.
         Nếu MUA được → dừng, xuất phương án mua. Nếu không → tiếp.

Bước 2 — CONCEPT + DFMA  [Mode B/D + P2]  → 2–3 concept (vd clamp cứng / clamp+strap / dạng máng),
         trade-off DFMA từng concept → chọn 1.

Bước 3 — LOAD-CASE + CALC  [Mode C]  → LOAD-CASE CHAIN (tải làm việc → thành phần → hệ số động → F_design;
         lever → M). Tính ứng suất tại tiết diện tới hạn. MATERIAL LADDER [PETG→PA→PA-CF]:
         báo vật liệu đầu tiên đạt FoS mục tiêu. Kiểm dị hướng in (σ_Z nếu FoS sát ngưỡng).

Bước 4 — ERGONOMICS  [Mode B-HF]  → nhân trắc bộ phận tiếp xúc (percentile, ANSUR II/DINED/ISO 7250) +
         góc trung tính + ngưỡng áp lực an toàn → suy bán kính/diện tích pad (A ≥ F/P_limit).

Bước 5 — SPEC + BOM + DOCS  [Mode E2]  → output contract: Concepts | Dimensions | Print Setup |
         Assembly | Safety Checklist | Variants (basic/padded/adjustable). Bảng in Nozzle|Layer|Infill|
         Support|Time|Material. BOM gồm vít/dây/lót.

Bước 6 — GEOMETRY CONCEPT (tuỳ chọn, THƯỜNG)  [[leo-prompt]]  → nếu cần mesh hình dung: sinh prompt
         text-to-CAD với DIMENSIONS + DATUM + hướng in IN-PLANE. NHẮC: mesh chỉ ideation, không gia công.
```
> Ví dụ chạy đủ chuỗi: [worked-example-wrist-support.md](worked-example-wrist-support.md) (phụ kiện tay đỡ cổ tay).
> Mỗi bước vẫn tuân 5 nguyên tắc Leo + cuối mỗi bước liệt kê GIẢ ĐỊNH (gồm số cần ĐO thực tế: Ø tay cầm, tải thật).

---

## Quy tắc dùng template
- **MẬT:** mọi prompt trừu tượng hóa — chỉ tham số generic (Ø/N/vật liệu), KHÔNG tên khí tài, KHÔNG upload bản vẽ/PLM. Hình học production → helix-cad-bridge local.
- **Geometry generation** (cần ra hình) → dùng [[leo-prompt]] (mesh concept, THƯỜNG) thay vì template ở đây.
- **Verify:** mọi số Leo trả về (kích thước/sức bền/siết) phải mở nguồn + CEO/CAD chốt trước khi vào bản vẽ/BOM MẬT.
