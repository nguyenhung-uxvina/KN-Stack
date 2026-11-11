---
name: helix-cad-crosscheck
description: "Kiểm NGƯỢC mô hình 3D về bản vẽ 2D mà nó được dựng từ — bản vẽ là GỐC, mô hình là nhân chứng. Chiếu lại mô hình theo từng hình chiếu khai trong sổ (OpenCascade HLR, chiếu song song) rồi so với thực thể DXF: X1 kích thước bao + gợi ý sai tỉ lệ · X2 nét thấy hai chiều · X3 nét khuất · X4 lỗ · X5 chữ kích thước ghi đè so số đo · X6 chân kích thước trên cạnh mô hình · X7 kích thước chung hai hình chiếu · X8 chú thích vẽ trên lớp nét hình học (khai trong sổ ⇒ đề xuất chuyển lớp) · X0 thể tích (CAx-IF 0,5 %). Quy lỗi theo PHƯƠNG LỆCH: mặc định lỗi của MÔ HÌNH (FAIL, sửa mô hình theo bản vẽ); chỉ quy cho BẢN VẼ (CONTESTED + đề xuất sửa 2D) khi một hình chiếu KHÁC thấy đúng phương lệch, đứng về phía mô hình và mâu thuẫn hình đang xét. Kèm mutate.py — đối chứng dương L6: cấy lỗi bản vẽ D1–D5 và lỗi tham số mô hình (tiến trình con) rồi đòi bắt đủ + quy đúng bên. Tất định, cục bộ, không LLM; báo cáo cùng định dạng helix-cad-gates, nạp vào audit_claims --profile reconstruct. Triggers on: 'crosscheck', 'kiểm 3D với 2D', 'kiểm ngược 2D', 'đối chiếu 3D bản vẽ', 'mô hình có đúng bản vẽ không', 'hình 3D vẽ đúng 2D chưa', '2D 3D consistency', 'drawing model consistency', 'HLR so DXF', 'đề xuất sửa bản vẽ', 'bản vẽ tự mâu thuẫn'."
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob"]
---

# helix-cad-crosscheck: Kiểm ngược 3D về 2D (bản vẽ là gốc)

> **Role:** Computational Sensor + Gate cho cặp (bản vẽ DXF, mô hình STEP). Đứng sau [[helix-cad-gates]] trong
> ứng dụng 10 của [[helix-cad-agents]] (dựng 3D từ 2D có kiểm ngược). Đầu ra vào
> `helix-cad-validate/audit_claims.py collect --profile reconstruct`.
> **Nguồn:** `/research` 2026-11-11 «kiểm nhất quán 2D–3D» (vault `3_Resources/Deep-Content-Analyzer-Outputs/RESEARCH_kiem-nhat-quan-2d-3d_2026-11-11.md`,
> notebook NLM 32 nguồn) — 6 lớp L1 thuộc tính tổng · L2 chiếu HLR so DXF · L3 lỗ/kích thước/chữ ghi đè ·
> L4 vị trí lắp · L5 danh mục đơn giản hoá · L6 cấy lỗi đối chứng dương. Skill này làm L1, L2, L3, L5, L6.
> L4 (lắp ráp) chưa làm.
> **Backend:** build123d 0.10 / OCP 7.8, ezdxf, numpy, scipy, matplotlib. Không LLM, không mạng.

## Why this exists
- **Bản vẽ 2D là gốc** (CEO chốt 2026-11-11). Mô hình 3D dựng từ bản vẽ (người hoặc AI) chỉ có giá trị khi
  kiểm ngược được về chính bản vẽ đó, từng nét, từng hình chiếu.
- Một bản vẽ có nhiều hình chiếu của cùng một vật ⇒ nó tự kiểm chéo được. Nếu hình bằng vẽ lỗ ở y = 41 còn
  hình cạnh (thấy được phương Y) và mô hình cùng ở y = 40, thì chính bản vẽ đang tự mâu thuẫn ⇒ đề xuất sửa 2D.
- **Bẫy đã gặp khi dựng skill (2026-11-11):** quy "lỗi bản vẽ" chỉ vì một hình chiếu khác *có* đặc trưng đó ở
  trục khác. M_L+1 (mô hình dài thêm 1 mm theo X) bị quy cho bản vẽ vì hình cạnh xác nhận đúng mép theo Y, một
  trục không hề lệch. Luật hiện hành: **chỉ hình chiếu thấy đúng phương lệch mới được phân xử**. Đối chứng
  dương bắt được lỗi này. Đọc phần Gotchas.

## Luật quy lỗi (máy, tất định)
| Tình huống | Quy cho | Trạng thái | Việc tiếp |
|---|---|---|---|
| Hình W khác cũng vẽ đúng như hình này mà mô hình không có | `model` | FAIL | Sửa mô hình |
| Đặc trưng lệch / sai cỡ, không hình nào khác thấy phương lệch | `model` | FAIL | Sửa mô hình theo bản vẽ (gốc) |
| Hình W thấy phương lệch, các cạnh của W khớp mô hình, W không vẽ ở vị trí của hình này | `drawing` | CONTESTED | Đề xuất sửa 2D, người duyệt |
| Mô hình có, hình này thiếu nét, hình W thấy đủ đặc trưng | `drawing` | CONTESTED | Đề xuất bổ sung nét |
| Chỉ hình này vẽ, hình W vẽ đủ nét khuất mà không có | `drawing` | CONTESTED | Đề xuất kiểm/xoá nét |
| Nằm trong `simplifications[]` đã khai | `simplified` | INFO | Không |
| Chữ kích thước ghi đè ≠ số đo hình vẽ (X5) | `drawing` | CONTESTED | Sửa chữ hoặc hình |
| Chú thích (khung dung sai, ký hiệu) trên lớp nét, kỹ sư khai `annotations[]` (X8) | `drawing` | CONTESTED | Chuyển lớp; loại khỏi so hình học |

FAIL và CONTESTED đều chặn. Máy **không bao giờ sửa bản vẽ**: `drawing_fix_proposals[]` chỉ là đề xuất, có
`witness_views` (hình chiếu làm chứng) và `region_view_mm`, để agent lập phiếu sửa và CEO quyết.

## Operational Envelope
| DO | DON'T |
|---|---|
| Lập sổ hình chiếu (`references/view_registry.schema.md`) trước, kỹ sư duyệt phương nhìn | Đoán phương nhìn / góc chiếu |
| Chạy `mutate.py` trên bộ đã PASS trước khi tin "0 lỗi" | Coi PASS không có đối chứng dương là bằng chứng |
| Khai `anchor` cho chi tiết có kích thước bao lệch | Đọc lệch nửa mm của lỗ khi bao đã lệch là lỗi riêng |
| Khai đơn giản hoá có `reason` | Khai `region_view` rộng để "che" lỗi |
| Đưa `crosscheck.json` + `mutate.json` vào audit_claims | Trình CEO bằng tóm tắt tự viết |

## Chạy
```bash
python crosscheck.py --step model.step --dxf sheet.dxf --registry views.json --out xc [--png-dir DIR]
#   exit 0 PASS · 2 FAIL/CONTESTED · 3 IO/sổ sai ; xc.json + xc.md (+ PNG: xanh nhạt=mô hình chiếu, đen=bản vẽ, đỏ=nét vẽ thừa, xanh=cạnh mô hình thiếu nét, tím=X8)
python mutate.py --step model.step --dxf sheet.dxf --registry views.json --out mut [--model model.py]
#   exit 0 = bộ gốc PASS và mọi lỗi cấy bị bắt ; từ chối khi bộ gốc chưa PASS
python ../helix-cad-validate/audit_claims.py collect --part ID --gates g.json --crosscheck xc.json \
       --mutate mut.json --profile reconstruct --out claims
```
`--model` dùng hợp đồng PARAMS/build của [[helix-cad-gates]]; mỗi tham số +1 mm được dựng trong **tiến trình con cách ly**
(`python -I`). Mã AI viết không bao giờ chạy trong tiến trình kiểm.

## Lỗi cấy (mutate.py)
| Mã | Cấy | Mong đợi |
|---|---|---|
| D1 | Dời vòng tròn lớn nhất 1 mm theo phương tờ (`_x`/`_y`) | `drawing` chỉ khi ở bộ gốc một hình khác **thấy chính đặc trưng đó** theo phương này; không ⇒ `model` |
| D2 | Tăng bán kính 0,25 mm thật | như D1 |
| D3 | Dời MỘT cạnh thẳng (LINE hoặc một đoạn LWPOLYLINE) 1 mm vuông góc chính nó — ưu tiên cạnh có hình khác làm chứng | như D1 |
| D4 | Xoá LINE/ARC dài nhất | như D1 |
| D5 | Chữ kích thước = số đo + 1 | `drawing` (X5) |
| M_* | Mỗi PARAM + 1 mm | `model` |
Test và `attribution_right` đòi **bắt đủ và quy về đúng MỘT bên**: lỗi mô hình không được sinh đề xuất sửa 2D.
Lỗi cấy vào bản vẽ mà không hình nào khác thấy (lỗ chỉ có ở hình bằng, hình cạnh không vẽ nét khuất) KHÔNG làm
bản vẽ tự mâu thuẫn ⇒ đáp đúng là `model`. Đó là giới hạn của mọi phép kiểm nhất quán: bản vẽ sai mà nhất quán
thì chỉ người (hoặc số đo vật thật) bắt được. Bộ gốc chỉ còn X8 (đề xuất chuyển lớp) vẫn chạy được đối chứng
(`baseline_verdict = PASS_GEOMETRY`).

## Gotchas
- **Đoạn bị cắt ≠ đặc trưng.** Cụm lệch là đoạn chưa khớp, bị cắt ~tol+step ở góc. So đầu mút chỉ khi cả hai
  bên là thực thể nguyên (LINE/ARC/CIRCLE, cạnh HLR). Đoạn của LWPOLYLINE so tâm. Bỏ luật này thì M_T+1 bị quy
  cho bản vẽ.
- **Cạnh khuất nằm dưới cạnh thấy** không tính là thiếu (quy ước vẽ: nét thấy che nét khuất).
- Bảng tra cạnh thấy và cạnh khuất **tách riêng** (`medges` / `medges_h`, `dents` / `dents_h`). Chỉ số trùng nhau
  từng làm cạnh khuất tra nhầm sang cạnh thấy.
- Lỗ nhìn nghiêng là hai đường hằng; nhìn thẳng là vòng tròn. `_seen_extent` nhận cả hai, và với dải suy biến
  (một đường bao) thì nhận cạnh bắt đầu hoặc kết thúc ở đó.
- X1 gợi ý "sai tỉ lệ" chỉ khi **cả hai** chiều lệch cùng tỉ số. 100/101 với 60/60 không phải sai tỉ lệ.
- **Khớp tịnh tiến là khớp CHUNG mọi hình chiếu** (`joint_fit`): mỗi trục thế giới một lựa chọn (ICP / tâm /
  mép min / mép max) dùng chung cho mọi hình thấy trục đó, chọn theo số điểm khớp lớn nhất. Hai lỗi đã đo:
  ICP trung vị dừng ở NỬA lệch khi một cạnh sai (điểm trên cạnh dọc trục cho dư 0) ⇒ mọi lỗ hiện lệch nửa mm;
  khớp từng hình riêng thì hai hình căn hai mép đối diện của cùng trục Y ⇒ phân xử chéo so hai hệ khác nhau.
- Dời CẢ đường bao một hình bị phép khớp hấp thụ (không phải lỗi quan sát được) — vì thế D3 dời một cạnh.
- **Chú thích trên lớp nét** (pilot 2026-11-11: khung dung sai trên lớp nét chính, nhô 6 mm khỏi mép tấm ⇒
  8 FAIL quy nhầm cho mô hình). Máy gợi ý trong thông điệp khi nét ra ngoài đường bao mô hình; kỹ sư khai
  `annotations[]` ⇒ X8 CONTESTED + đề xuất chuyển lớp. Máy không tự đoán cái gì là chú thích.

- **Pilot vòng 2 (3 chi tiết tấm thật, 2026-11-11)** lộ thêm 3 lỗi của bộ kiểm, đều do đối chứng dương bắt:
  (1) cạnh làm chứng phải khớp ở CẢ HAI ĐẦU, không chỉ ≥ 60 % chiều dài — cạnh xiên có chân đã dời vẫn "khớp"
  và làm chứng sai toạ độ; (2) đường bao LWPOLYLINE là MỘT thực thể, đầu mút của nó không nói gì — phép làm
  chứng dùng từng đoạn giữa hai đỉnh; (3) đoạn lệch của cạnh dài ghép cặp theo chính đoạn lệch khi tâm cạnh
  nguyên xa nhau (dự phòng, sau ghép theo đặc trưng nguyên).
- Đường bao hàng mua lắp kèm vẽ trùm lên lỗ thật: khai `annotations[].handles`, không khai vùng (vùng nuốt lỗ).
- Hình cạnh của tấm có bậc phải có nét ngang tại cao độ bậc (mặt trên phần thấp nhìn thấy được) — pilot bắt
  được tờ thiếu nét này; quy cho bản vẽ vì hình đứng làm chứng.

## COD
| Task | COD |
|---|---|
| Duyệt sổ hình chiếu (phương nhìn, tỉ lệ), quyết đề xuất sửa 2D, ký | **C** |
| Lập sổ nháp, chạy crosscheck/mutate, lập phiếu đề xuất | O |
| PNG chồng nét, định dạng báo cáo | D |
