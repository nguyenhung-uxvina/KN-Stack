---
name: helix-cad-gates
description: "Geometry Computational Sensor + Gate cho mô hình CAD do AI dựng — đo STEP so với geometry_contract.json kỹ sư đã ký (KHÔNG cần STEP đáp án): F1 B-Rep kín/hợp lệ · F2 hộp bao TỪNG TRỤC + phát hiện ĐẢO TRỤC + điểm dò point-in-solid bắt ẢNH GƯƠNG và SAI VỊ TRÍ · F3 đếm feature trụ theo Ø (thiếu VÀ thừa) · F4 uốn tham số ±10% dựng lại + hình PHẢI đổi + param_probes bắt toạ độ tuyệt đối (hợp đồng PARAMS/build) · --mode release mặc định ép FAIL khi hợp đồng mỏng (thiếu điểm dò / --model / --approved-hash) · khối lượng so khung tên chỉ là INFO. Kèm cad_runner.py (chạy model.py trong tiến trình con cách ly, timeout) và render_views.py (6 hình chiếu + trục đo PNG cho cổng CEO và giám khảo ý đồ). Tất định, cục bộ, không LLM; báo cáo cùng định dạng helix-cad-validate (PASS/FAIL/SKIP/INFO, exit 0/2/3 + 4 DRAFT-PASS, --approved-hash). Triggers on: 'cad gates', 'geometry gate', 'kiểm mô hình AI dựng', 'cổng hình học', 'B-Rep kín', 'đảo trục', 'ảnh gương', 'point probe', 'điểm dò', 'đếm lỗ', 'parametric flex', 'uốn tham số', 'render views', 'kiểm STEP', 'verify STEP', 'geom gates'."
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob"]
---

# helix-cad-gates: Geometry Gate cho mô hình AI dựng

> **Role:** Cross-phase **Computational Sensor + Gate** cho HÌNH HỌC. Đứng ngay sau khi có `model.step`
> ([[helix-cad-bridge]] Step 4, [[helix-s2c-implement]], [[helix-cad-batch]], `helix-cad-reconstruct` đợt 2)
> và TRƯỚC giám khảo ý đồ [[helix-cad-judge]] và cổng CEO xem render.
> Chị em của [[helix-cad-validate]]: validate chấm **dữ liệu** (extract + luật thiết kế), gates chấm **hình học**.
> **Backend:** Python cục bộ — build123d 0.10 / OCP 7.8, matplotlib. Không LLM, không mạng.

## Why this exists
Đo 2026-11-02 (`/research --deep "CAD claude"` + phép thử 5 bản vẽ GIÁ TRƯỢT):
- Lỗi thật của mô hình AI dựng: shell hở (64%), **đảo trục hình chiếu** (58%), **sót lỗ/bậc** (78%),
  **toạ độ cứng gãy khi sửa kích thước** (88%) — CAD-CUA 2026.
- Lúc dùng thật **không có STEP đáp án** ⇒ cổng phải so với **hợp đồng đã ký**, không so mô hình mẫu.
- **Đếm feature cho qua nhầm**: P4 puly — trục Ø12 sai, nhưng mũ Ø20 khớp check "Ø19–20" ⇒ F3 PASS;
  chỉ **điểm dò** bắt được (0/2). ⇒ mọi feature quan trọng phải có `probes[]`.
- Agent dựng **tự chỉnh độ dày tấm cho khớp KL khung tên** ⇒ KL chỉ là INFO, cấm làm mục tiêu.
- **Rà điểm mù 2026-11-05** (đối chiếu CADCodeVerify, arXiv 2410.05340): 4 đột biến từng PASS cổng v1.0 —
  M1 `build()` khai PARAMS nhưng bỏ qua (F4 chỉ kiểm B-Rep kín) · M2 lỗ đặt toạ độ tuyệt đối (đứng yên khi
  chiều dài đổi) · M3 hợp đồng chỉ có bbox + khối hộp **không có lỗ** ⇒ verdict PASS (SKIP không chặn) ·
  M4 lỗ thừa ngoài spec (F3 chỉ đếm ≥). v1.1 vá cả 4; mỗi đột biến có test và FAIL trên v1.0.

## Operational Envelope
| DO | DON'T |
|---|---|
| Chấm STEP so với `geometry_contract.json` đã ký | So với "cảm giác đúng" hay render đẹp |
| Chạy `model.py` qua `cad_runner.py` (tiến trình con `-I`, timeout) | `exec`/import mã AI viết vào tiến trình chính |
| Báo FAIL rõ khi thiếu solid, thiếu hợp đồng PARAMS | Văng lỗi / SKIP im lặng |
| `--mode release` khi đưa cho judge/CEO; `--mode draft` chỉ khi đang lặp dựng | Đưa `DRAFT-PASS` cho judge/CEO như PASS |
| Ghi KL là INFO | Đóng/mở cổng theo KL; gợi ý chỉnh kích thước cho khớp KL |
| Dùng `--approved-hash` | Để agent sửa hợp đồng cho cổng xanh |

## Hợp đồng model.py (bắt buộc cho F4 + batch)
```python
PARAMS = {"L_SHAFT": 186.0, "D_SHAFT": 28.0, ...}   # mọi kích thước, mm
def build(params): ...                              # trả build123d Shape, chỉ đọc từ params
if __name__ == "__main__": export_step(build(PARAMS), "model.step")
```

## Workflow
### Step 1: Hợp đồng (CORE — kỹ sư)
Lập `geometry_contract.json` theo `references/geometry_contract.schema.md` từ spec đã duyệt (nguồn D/G/T/?).
Kỹ sư ký → tính sha256 một lần → ghi vào `_pipeline_state.md`.

### Step 2: Chạy mô hình (Offload)
```bash
python cad_runner.py run --model model.py            # → model.step ; exit 2 nếu lỗi/không có STEP
```

### Step 3: Cổng (Offload — mỗi vòng lặp)
```bash
python geom_gates.py --step model.step --contract geometry_contract.json --model model.py \
                     --out cad_gates_report --approved-hash <sha256>          # --mode release (mặc định)
```
Exit 0 = PASS (mở cho judge + CEO) · 2 = FAIL (gửi `fix_hint` về khối dựng, 1 vòng/lượt) · 3 = lỗi IO.
Đang lặp dựng, hợp đồng chưa đủ: thêm `--mode draft` ⇒ verdict `DRAFT-PASS` (**exit 4**, cố ý ≠ 0) — **không** mở judge/CEO.

### Step 4: Render cho người (Offload → CORE)
```bash
python render_views.py --step model.step --out model_views.png --title "<part_id>"
```
CEO/kỹ sư xem 6 hình chiếu + trục đo (Spatial Blindness gate của [[helix-cad-bridge]] Step 5).

## Gotchas
- `is_inside` chỉ có trên solid — STEP chỉ có shell ⇒ `F2_probes` FAIL kèm "xem F1" (không văng lỗi).
- Điểm dò đặt **giữa** feature, cách biên ≥ 1 mm; điểm sát biên cho kết quả bấp bênh.
- F4 FAIL vì "không theo hợp đồng PARAMS/build" ≠ "số cứng" — mô hình có thể có hằng số tên nhưng không gọi được `build(params)`.
- F4 "không tác động" = uốn ±10% cho hình y hệt (hộp bao + thể tích + trọng tâm). Tham số thật sự không đổi
  hình (số nguyên đếm, cờ) ⇒ bỏ khỏi `f4_params`, đừng nới cổng.
- `F4_model_matches_step` FAIL ⇒ STEP đang kiểm không phải đầu ra của `model.py` — xuất lại, đừng sửa hợp đồng.
- `F3_unlisted` bắt cả **bo cung** (mặt trụ Ø = 2r): liệt kê fillet trong `cyl_features` hoặc kỹ sư đặt
  `cyl_exhaustive: false` rồi ký lại.
- `param_probes` chỉ nhận `+ - * /`, số, tên PARAMS (không `eval`) — biểu thức khác ⇒ FAIL kèm lỗi.
- Render bằng sắp xếp độ sâu + bỏ mặt quay lưng; đủ để soi hướng/feature, không phải ảnh kỹ thuật.

## Integration Map
| Gọi bởi | Khi |
|---|---|
| [[helix-cad-bridge]] Step 4 | sau mỗi lần xuất STEP |
| [[helix-s2c-validate]] (BE) | cùng `validate.py` — validate cho dữ liệu, gates cho hình học |
| [[helix-cad-batch]] | mỗi biến thể |
| [[helix-cad-agents]] | ứng dụng 1, 4, 5 |

## Output
`cad_gates_report.json` + `.md` (bảng kiểm, FAIL detail, ô ký kỹ sư) · `model_views.png`.

## CEO/Engineer Checkpoint
- Ký hợp đồng hình học (Step 1) — **Core**.
- Xem render + ký (Step 4) — **Core**. PASS = khớp hợp đồng, **không** = hợp đồng đúng hay chi tiết an toàn.

## COD
| Task | COD |
|---|---|
| Lập/ký geometry_contract, chọn điểm dò | **C** |
| Chạy runner, gates, render | O |
| Đọc báo cáo FAIL, sửa mô hình | O (agent dựng) |
| Duyệt render + ký | **C** |

## Tests
`python -m pytest scripts/test_helix_cad_gates.py -v` — 23 ca: 12 đột biến gốc (shell hở, đảo trục, lỗ đúng Ø
sai chỗ, thiếu lỗ, không điểm dò ⇒ SKIP, KL không gating, F4 có/không hợp đồng, fillet giòn, hash lệch, mã thoát
— ca này nay chạy `--mode draft`) + 11 ca điểm mù 2026-11-05 (M1–M4, đối chứng dương lỗ theo tham số, model≠STEP,
release/draft, waiver, biểu thức probe không chạy mã). Đối chứng âm: chạy bộ test này trên `geom_gates.py` v1.0 ⇒
10/11 ca mới FAIL; ca còn lại (`test_release_full_contract_passes`) là đối chứng dương nên PASS ở cả hai bản.
