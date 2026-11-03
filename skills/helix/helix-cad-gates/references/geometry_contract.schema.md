# geometry_contract.json — schema (helix-cad-gates)

Hợp đồng hình học mà kỹ sư định danh **ký** cho một chi tiết. `geom_gates.py` đo STEP do AI dựng **so với
hợp đồng này**, không so với mô hình mẫu (lúc dùng thật không có STEP đáp án).

Khoá chống tự sửa: sau khi kỹ sư duyệt, tính `sha256` một lần (`certutil -hashfile geometry_contract.json SHA256`
hoặc `sha256sum`) và luôn chạy `geom_gates.py --approved-hash <sha>`. Hợp đồng là **read-only với agent**.

```json
{
  "part_id": "GT.00.03.01",
  "classification": "KHÔNG-NHẠY-CẢM | HẠN-CHẾ | MẬT",
  "projection_method": "first-angle | third-angle",
  "axis_convention": "front view = XZ; X ngang, Z đứng, Y chiều sâu; gốc ở góc min của hộp bao",
  "bbox": [194, 40, 40],
  "bbox_tol": 0.5,
  "probes": [
    {"why": "lỗ ngang Ø5,5 thông, tâm cách đầu mút 8,5", "pt": [185.5, 20, 20], "inside": false},
    {"why": "thân đặc giữa chốt", "pt": [100, 20, 20], "inside": true}
  ],
  "cyl_features": [
    {"what": "shaft_d28", "dia": 28, "tol": 0.3, "min_faces": 1}
  ],
  "f4_params": ["L_SHAFT", "D_SHAFT"],
  "f4_flex": 0.10,
  "material": "C45",
  "title_kg": 1.1
}
```

| Trường | Bắt buộc | Ý nghĩa |
|---|---|---|
| `bbox`, `bbox_tol` | ✅ | Kích thước hộp bao **theo từng trục** X, Y, Z (mm). Sai thứ tự ⇒ báo `ĐẢO TRỤC`. |
| `projection_method`, `axis_convention` | ✅ | Ghi rõ — bản nháp spec đầu tiên của phép đo GIÁ TRƯỢT đã **lật gương** hình chiếu góc 1. |
| `probes[]` | ✅ (≥1 / feature quan trọng) | Điểm phải có (`inside: true`) / không có (`false`) vật liệu. **Bắt buộc** cho mọi lỗ, rãnh, trục, hướng côn — `cyl_features` một mình từng cho qua nhầm (mũ Ø20 khớp check trục Ø19). Thiếu ⇒ `SKIP` (không bao giờ PASS im lặng). Đặt điểm ở giữa feature, xa biên ≥ 1 mm. |
| `cyl_features[]` | khuyên | Đếm mặt trụ theo Ø (≥ `min_faces`). Rẻ, bắt "thiếu lỗ", nhưng không bắt "sai chỗ". |
| `f4_params`, `f4_flex` | tuỳ | Tham số đem uốn ±flex (mặc định mọi số dương trong `PARAMS`, ±10%). Cần `--model`. |
| `material`, `title_kg` | tuỳ | Chỉ cho `MASS_vs_title` = **INFO, không gating**. Agent **không được** chỉnh kích thước để khớp KL. |

Khoá vật liệu nhận được: `C45, STEEL, CT3, SS400, INOX304, SUS304, INOX316, AL5083, AL6061, AL, PTFE, TEFLON, POM, DELRIN`.

Nguồn mỗi giá trị khi lập hợp đồng từ bản vẽ (ghi trong spec đi kèm): **D** ghi trên bản vẽ · **G** đo từ hình học
DXF 1:1 · **T** khung tên · **?** suy luận — mọi `?` phải được kỹ sư xác nhận trước khi ký.
