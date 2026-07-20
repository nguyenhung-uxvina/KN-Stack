# Worked Example — Tay đỡ cổ tay (phụ kiện gym) chạy recipe `leo-part-brief`

> Ví dụ end-to-end MỘT chi tiết THƯỜNG đi hết chuỗi 6 mode Leo. Dùng làm mẫu dạy cho `leo-assist` +
> `leo-prompt`. Sản phẩm: phụ kiện tay đỡ cổ tay kẹp vào ống tay cầm máy cáp, tạo điểm tựa mặt lưng cổ tay
> khi lateral raise 1 tay. Đây là **hình dạng thật** của một brief CPTRF đa-mode — mỗi task ↔ 1 mode.

## Bước 0 — CLASSIFY
Đồ tập cá nhân, không context khí tài → **THƯỜNG** ✅ → dùng Leo cloud đầy đủ. (Nếu là chi tiết khí tài →
dừng, chuyển `helix-cad-bridge` local.)

## Bước 1 — SEARCH FIRST  [Mode A] — mua vs chế tạo
```
[Phân loại: THƯỜNG]
[MODE] PART SEARCH — tìm & tái dùng
[FUNCTION] Tạo điểm tựa cứng cho mặt lưng cổ tay khi tập cáp 1 tay; giữ cổ tay trung tính, không cản abduct 0–90°.
[ENVELOPE] Kẹp quanh ống tay cầm Ø28–32 mm (split-clamp); lắp/tháo không dụng cụ.
[SPEC] Tải tiếp xúc ngang ~150 N; tiếp xúc mồ hôi; tải lặp hàng nghìn rep.
[SOURCE] Kho vendor COTS.
[ASK] 1. 5 ứng viên (wrist wrap cứng / clamp-on support / strap gắn tay cầm) + độ khớp.
      4. MUA vs CHẾ TẠO: nếu không có COTS ôm đúng ống Ø28–32 + giữ trung tính → khuyến nghị in FDM đơn chiếc.
[GIẢ ĐỊNH] Ø tay cầm 28–32 — ĐO tay cầm máy thật trước khi chốt.
```
→ Kết luận điển hình: COTS wrist-wrap không kẹp vào ống tay cầm → **CHẾ TẠO** (FDM đơn chiếc). Sang bước 2.

## Bước 2 — CONCEPT + DFMA  [Mode B/D]
3 concept: **(a) clamp cứng** (split-clamp + vít tai hồng M5) · **(b) clamp + strap velcro** · **(c) dạng máng ôm**.
Trade-off DFMA: (a) cứng nhất, cần vít; (b) lắp nhanh <15s, strap chịu mỏi kém hơn; (c) ít part nhất, ôm kém khi
Ø thay đổi. Chọn theo ưu tiên an toàn > printability > cơ động → thường **(a) hoặc (b)**.

## Bước 3 — LOAD-CASE + CALC  [Mode C]
```
[MODE] CALCULATION — hiện công thức + logic + nguồn
[LOAD-CASE CHAIN]  tải cáp làm việc 15 kg (≈150 N) × thành phần ngang 60% × hệ số động 1.5
   → làm tròn F_design = 150 N.  Lever tâm ống→pad ≈ 50 mm  → M = 150 N × 0,05 m = 7,5 N·m.
[UNKNOWN] Tiết diện chân tay đỡ (b×t) để σ_uốn ≤ giới hạn với FoS ≥ 3.
[MATERIAL LADDER]  PETG → PA (Nylon) → PA-CF.  Báo vật liệu đầu tiên đạt FoS ≥ 3.
[ASK] 1. σ = M·c/I = 6M/(b·t²) cho tiết diện chữ nhật — trích nguồn công thức uốn.
      3. Giới hạn chảy từng vật liệu từ datasheet CÓ NGUỒN (PETG ~50 MPa; PA ~40–70; PA-CF cao hơn — Leo cite).
      4. FoS = σ_giới-hạn / σ_làm-việc từng vật liệu; kiểm với σ_Z (dị hướng) nếu FoS sát.
[GIẢ ĐỊNH] tải làm việc 15 kg; thành phần ngang 60%; hệ số động 1.5; lever 50 mm — xác minh thực tế.
```
> Logic chọn tiết diện: với M=7,5 N·m và σ_cho-phép = σ_chảy/3, giải b·t² ≥ 6M/σ_cho-phép. Nếu PETG không đạt
> khi t bị giới hạn bởi bao hình → leo tự nhảy sang PA/PA-CF trong ladder.

## Bước 4 — ERGONOMICS  [Mode B-HF]
```
[MODE] HUMAN-FACTORS — nhân trắc + công thái, ép cite bộ dữ liệu
[BODY PART] Cổ tay (mặt lưng/ngoài).   [POPULATION] Người trưởng thành (nêu nếu cần dữ liệu VN/châu Á).
[POSTURE] Cổ tay trung tính khi vai abduct 0–90° (tránh ulnar deviation).
[ASK] 1. Bề rộng & chu vi cổ tay P5/P50/P95 — nguồn ANSUR II / DINED / ISO 7250-1.
      2. Góc cổ tay trung tính an toàn — nguồn cơ sinh học.
      3. Ngưỡng áp lực tiếp xúc an toàn (kPa) tránh cấn thần kinh trụ — nguồn.
      4. Suy diện tích pad A ≥ F/P_limit (F=150 N) + bán kính bo phân tán áp lực; pad phủ P5–P95.
[GIẢ ĐỊNH] "bên đeo đồng hồ" = mặt lưng/ngoài cổ tay — xác nhận đúng bên tiếp xúc.
```

## Bước 5 — SPEC + BOM + DOCS  [Mode E2]
Output contract: **Concepts | Dimensions | Print Setup | Assembly | Safety Checklist | Variants**.
- Bảng in: | Nozzle 0.4 | Layer 0.2 | Infill 45% gyroid | Support tối thiểu (overhang ≤45°) | Time | PETG/PA |
- BOM: thân FDM · pad TPU 95A · vít tai hồng M5 HOẶC dây velcro · lót TPU trong clamp.
- Safety Checklist: bo mọi cạnh tiếp xúc R ≥ 2 mm; không điểm cấn; tải giới hạn ghi rõ; kiểm nứt tách lớp.
- Variants: **basic** (clamp cứng) / **padded** (thêm pad TPU dày) / **adjustable** (strap velcro chỉnh Ø).

## Bước 6 — GEOMETRY CONCEPT (tuỳ chọn)  [[leo-prompt]]
Nếu cần mesh hình dung: sinh prompt với DIMENSIONS (D_grip 28–32, t chân, θ ôm, R pad) + DATUM (gốc = tâm ống,
+Z = hướng in) + **hướng in đặt ứng suất uốn IN-PLANE** (chống tách lớp tại chân). NHẮC: mesh chỉ ideation.

## Assumption ledger (đưa xuống cuối MỌI bước để CEO kiểm)
| # | Giả định | Cách xác minh |
|---|---|---|
| 1 | Tải cáp làm việc 15 kg | Chỉnh theo mức tập thực tế |
| 2 | Thành phần lực ngang 60% + hệ số động 1.5 | Cảm nhận/đo thực tế |
| 3 | Lever 50 mm | Tính lại theo hình học concept cuối |
| 4 | Ø ống tay cầm 28–32 mm | **ĐO tay cầm máy thật trước khi in** |
| 5 | Vật liệu PETG | Chuyển PA/PA-CF nếu 7,5 N·m không đạt FoS ≥ 3 |
| 6 | Bên tiếp xúc = mặt lưng/ngoài cổ tay | Xác nhận đúng bên |

> Bài học recipe: một brief tốt KHÔNG rơi vào 1 mode — nó xâu A→(C+F)→B-HF→E→leo-prompt. Số Leo trả về luôn
> CEO mở nguồn verify (đặc biệt calc chịu lực + ngưỡng áp lực thần kinh) trước khi in/dùng.
