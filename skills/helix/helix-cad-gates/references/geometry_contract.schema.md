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
    {"what": "shaft_d28", "dia": 28, "tol": 0.3, "min_faces": 1, "max_faces": 1},
    {"what": "cross_hole_d5_5", "dia": 5.5, "tol": 0.2, "min_faces": 1, "max_faces": 1}
  ],
  "cyl_exhaustive": true,
  "f4_params": ["L_TOTAL", "D_HEAD"],
  "f4_flex": 0.10,
  "param_probes": [
    {"why": "lỗ ngang luôn cách đầu mút 8,5 (PARAMS có L_TOTAL = 194, D_HEAD = 40)",
     "pt": ["L_TOTAL-8.5", "D_HEAD/2", "D_HEAD/2"], "inside": false}
  ],
  "waivers": {},
  "judge_questions": [
    {"id": "Q1", "q": "Lỗ ngang có tiết diện TRÒN (không vuông, không lục giác)?",
     "spec_line": "Lỗ ngang Ø5,5 thông, tâm cách đầu mút 8,5", "severity": "block"}
  ],
  "material": "C45",
  "title_kg": 1.1
}
```

| Trường | Bắt buộc | Ý nghĩa |
|---|---|---|
| `bbox`, `bbox_tol` | ✅ | Kích thước hộp bao **theo từng trục** X, Y, Z (mm). Sai thứ tự ⇒ báo `ĐẢO TRỤC`. |
| `projection_method`, `axis_convention` | ✅ | Ghi rõ — bản nháp spec đầu tiên của phép đo GIÁ TRƯỢT đã **lật gương** hình chiếu góc 1. |
| `probes[]` | ✅ (≥1 / feature quan trọng) | Điểm phải có (`inside: true`) / không có (`false`) vật liệu. **Bắt buộc** cho mọi lỗ, rãnh, trục, hướng côn — `cyl_features` một mình từng cho qua nhầm (mũ Ø20 khớp check trục Ø19). Thiếu ⇒ `SKIP` ở `--mode draft`, **`FAIL` ở `--mode release`** (mặc định). Đặt điểm ở giữa feature, xa biên ≥ 1 mm. |
| `cyl_features[]` | khuyên | Đếm mặt trụ theo Ø: `min_faces ≤ n ≤ max_faces` (`max_faces` tuỳ; một lỗ thông trơn thường = 1 mặt). Bắt "thiếu lỗ" và "thừa lỗ cùng Ø", không bắt "sai chỗ". |
| `cyl_exhaustive` | mặc định `true` | Khi có `cyl_features`: mọi mặt trụ của mô hình phải thuộc một mục ⇒ lỗ/trục **thừa** mà spec không có ⇒ `F3_unlisted` FAIL. **Bo cung (fillet) cũng là mặt trụ Ø = 2r** — liệt kê chúng, hoặc kỹ sư đặt `false` (đã ký). |
| `f4_params`, `f4_flex` | tuỳ | Tham số đem uốn ±flex (mặc định mọi số dương trong `PARAMS`, ±10%). Cần `--model`. Tham số mà uốn ± đều cho **hình y hệt** (hộp bao, thể tích, trọng tâm) ⇒ FAIL "không tác động" — `build()` bỏ qua params. Tham số thật sự không đổi hình (vd số lượng nguyên) thì bỏ khỏi `f4_params`. |
| `param_probes[]` | ✅ ở release khi có `--model` | Như `probes` nhưng toạ độ viết theo **biểu thức PARAMS** (`+ - * /`, số, tên PARAMS — không gì khác). Kiểm ở mọi biến thể uốn ⇒ bắt feature đặt bằng **toạ độ tuyệt đối** (lỗ đứng yên khi chiều dài đổi). Ghi quan hệ ý đồ: "cách đầu mút 30" = `"length-30"`, không phải `70`. |
| `waivers{}` | tuỳ | `{"<rule_id>": "<lý do>"}` cho `F2_probes`, `F4_param_flex`, `F4_relations` — miễn ép FAIL ở release (vd chi tiết mua sẵn không có `model.py`). Nằm trong hợp đồng ⇒ được khoá bằng hash ⇒ agent không tự thêm được. |
| `judge_questions[]` | ✅ khi chạy judge | 1–12 câu Có/Không cho [[helix-cad-judge]] (`id`, `q`, `spec_line`, `severity` block\|comment). `geom_gates.py` bỏ qua trường này; nó nằm đây để **cùng hash** ⇒ agent không tự đổi câu hỏi. Luật soạn: `helix-cad-judge/references/question-rules.md`. |
| `material`, `title_kg` | tuỳ | Chỉ cho `MASS_vs_title` = **INFO, không gating**. Agent **không được** chỉnh kích thước để khớp KL. |

**`--mode release` (mặc định)** ép FAIL khi: thiếu `probes[]`, thiếu `--model`, thiếu `param_probes[]`, thiếu
`--approved-hash` — trừ khi có `waivers` cho rule đó. **`--mode draft`** để lặp khi đang dựng: giữ SKIP, verdict
`DRAFT-PASS`, exit 4 — judge và cổng CEO chỉ nhận `verdict == "PASS"`, khối gọi theo mã thoát chỉ mở khi exit 0,
nên bản nháp không lọt qua được.

Khoá vật liệu nhận được: `C45, STEEL, CT3, SS400, INOX304, SUS304, INOX316, AL5083, AL6061, AL, PTFE, TEFLON, POM, DELRIN`.

Nguồn mỗi giá trị khi lập hợp đồng từ bản vẽ (ghi trong spec đi kèm): **D** ghi trên bản vẽ · **G** đo từ hình học
DXF 1:1 · **T** khung tên · **?** suy luận — mọi `?` phải được kỹ sư xác nhận trước khi ký.
