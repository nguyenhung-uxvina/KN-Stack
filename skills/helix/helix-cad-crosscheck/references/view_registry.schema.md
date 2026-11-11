# Sổ hình chiếu (`views.json`) — hợp đồng giữa bản vẽ DXF và `crosscheck.py`

Sổ này nói cho máy biết **hình chiếu nào nằm ở đâu trên tờ, nhìn theo phương nào, tỉ lệ bao nhiêu**. Máy không
tự đoán: đoán sai phương nhìn thì mọi so sánh sau đó đều vô nghĩa. Người lập sổ (agent nháp, kỹ sư duyệt) đọc
khung tên và bố cục tờ; `crosscheck.py` từ chối sổ thiếu trường bắt buộc (exit 3).

## Cấu trúc

```json
{
  "part_id": "DEMO.01",
  "tolerances": {"tol": 0.2, "tol_dia": 0.1, "step": 0.25, "min_cluster": 1.0, "witness_ratio": 0.6, "pair_max": 5.0},
  "expected": {"volume_mm3": 48000, "tolerance_pct": 0.5},
  "views": [
    {"id": "top", "region": [15, 25, 75, 65], "scale": 2,
     "look_dir": [0, 0, -1], "up": [0, 1, 0],
     "layers_visible": ["NET CO BAN"], "layers_hidden": ["NET KHUAT"],
     "hidden_lines": "partial", "kind": "projection",
     "anchor": {"model": [0, 0, 8], "sheet": [20, 30]},
     "annotations": [{"region": [60, 30, 76, 34], "reason": "khung dung sai vẽ trên lớp nét chính"}]},
    {"id": "A-A", "region": [95, 25, 140, 40], "scale": 2,
     "look_dir": [1, 0, 0], "up": [0, 0, 1], "layers_visible": ["NET CO BAN", "MAT CAT"],
     "hidden_lines": "none", "kind": "section", "section": {"point": [70, 0, 0]}}
  ],
  "simplifications": [
    {"view": "*", "side": "model", "region_view": [-35, -15, -25, -5], "reason": "lỗ thoát khí không vẽ"}
  ]
}
```

## Trường

| Trường | Bắt buộc | Nghĩa |
|---|---|---|
| `views[].id` | ✅ | Tên hình chiếu như trên bản vẽ (`top`, `A-A`, `B`) — dùng trong locator và đề xuất sửa |
| `views[].region` | ✅ | `[x0, y0, x1, y1]` **đơn vị tờ** (model space DXF). Thực thể có ≥ 50 % điểm trong ô thuộc hình này |
| `views[].scale` | ✅ | **Mẫu số** tỉ lệ k (1:2 ⇒ 2): mm thật = đơn vị tờ × k. Hình trích có tỉ lệ riêng thì khai riêng |
| `views[].look_dir` | ✅ | Phương **mắt nhìn** trong hệ mô hình (từ người xem vào vật). Hình chiếu bằng nhìn xuống: `[0,0,-1]` |
| `views[].up` | ✅ | Phương hệ mô hình hiện **lên trên** trên tờ. Màn hình phải = look_dir × up |
| `layers_visible` | — | Lớp nét thấy (mặc định `["0"]`). Lớp kích thước, trục, chữ KHÔNG đưa vào đây |
| `layers_hidden` | — | Lớp nét khuất |
| `hidden_lines` | — | `full` (vẽ đủ nét khuất — thiếu nét khuất là lỗi) · `partial` (mặc định, chỉ kiểm nét khuất đã vẽ) · `none` |
| `kind` | — | `projection` (mặc định) · `section` (cần `section.point`: một điểm trên mặt cắt, hệ mô hình; giữ phần vật phía sau mặt cắt theo look_dir) |
| `anchor` | — | Ghim tịnh tiến: điểm mô hình `model` (mm) nằm ở `sheet` (đơn vị tờ). Không khai ⇒ khớp chung mọi hình chiếu (mỗi trục thế giới một lựa chọn ICP/tâm/mép min/mép max, nhiều điểm khớp nhất). Khai khi biết chắc mốc chuẩn (mặt chuẩn A) |
| `annotations[]` | — | `handles` (danh sách handle DXF — dùng khi vùng sẽ nuốt cả nét thật, vd đường bao hàng mua lắp kèm vẽ trùm lên lỗ của chi tiết) hoặc vùng `region` (đơn vị tờ) chứa chú thích vẽ trên lớp nét hình học (khung dung sai, ký hiệu). Thực thể ≥ 50 % trong vùng bị loại khỏi so hình học và mỗi thực thể thành claim X8 CONTESTED + đề xuất chuyển lớp. Bắt buộc `reason`; kỹ sư khai, không phải agent dựng |
| `expected.volume_mm3` | — | Thể tích đã biết (L1, CAx-IF 0,5 %). Không khai ⇒ X0 chỉ INFO |
| `simplifications[]` | — | Danh mục đơn giản hoá đã duyệt (L5). `side`: `model` (mô hình có, bản vẽ cố ý không vẽ) · `drawing` (bản vẽ có, mô hình cố ý không dựng, vd ren vẽ quy ước) · `both`. `region_view` theo **mm thật, hệ hình chiếu đã khớp** (lấy từ `observed` của báo cáo). Mỗi mục bắt buộc có `reason` |

## Kiểm phương nhìn trước khi chạy

`test_frame_matches_hlr` khoá quy ước: phải = look_dir × up, lên = phải × look_dir, khớp `project_to_viewport`
của build123d. Hình chiếu cạnh trái theo TCVN (góc thứ nhất, đặt bên PHẢI hình đứng): mắt nhìn từ trái sang,
`look_dir = [1,0,0]`. Đặt nhầm góc thứ nhất / thứ ba ⇒ X1 báo hai chiều lệch, X2 báo đối xứng gương — sửa sổ,
không sửa mô hình.

## Khi nào sổ sai chứ không phải bản vẽ / mô hình sai
- X1 CONTESTED kèm "cả hai chiều lệch cùng tỉ số" ⇒ `scale` khai sai (hoặc hình vẽ sai tỉ lệ — người xem khung tên).
- X2_visible FAIL "không có nét thấy" ⇒ `region` / `layers_visible` sai.
- Mọi cạnh lệch cùng một vectơ ⇒ `anchor` sai.
