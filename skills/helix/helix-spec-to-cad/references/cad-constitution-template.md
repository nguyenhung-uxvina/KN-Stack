# CAD Constitution — {{project}} / {{part_id}}

> **Vai trò:** Văn bản nguyên tắc BẤT KHẢ THƯƠNG LƯỢNG cho mọi part đi qua pipeline Spec-to-CAD.
> Đây là nguồn human-canonical; section "Machine-Checkable Extract" ở cuối được compile thành
> `design_rules.json` (yardstick của [[helix-cad-validate]]). Điều I–IV không machine-checkable
> → cưỡng chế qua **Constitution Check gate** ở block `helix-s2c-plan`.
> Mượn khái niệm "constitution" từ GitHub spec-kit (SDD methodology) — bản địa hóa cho CAD cơ khí Workshop X.

**Version:** {{x.y.z}} · **Ratified:** {{YYYY-MM-DD}} · **Last Amended:** {{YYYY-MM-DD}}
**Classification:** [MẬT | HẠN-CHẾ | THƯỜNG] — đặt một lần, downstream chỉ ĐỌC.

---

## Điều I — Metric-only
Mọi kích thước tính bằng **mm**, tỷ lệ 1:1, khối lượng **kg**, góc **độ**. Không inch, không tỷ lệ ẩn.

## Điều II — Local / Air-gapped
Mọi bước sinh + kiểm hình học chạy **100% LOCAL** (build123d/CadQuery/OpenSCAD, ezdxf, stdlib).
KHÔNG SaaS CAD (Leo/Zoo/Fusion/Onshape), KHÔNG cloud OCR, KHÔNG network egress lúc runtime.

## Điều III — Classification propagation
Label MẬT/HẠN-CHẾ/THƯỜNG đặt MỘT LẦN (helix-p1-validate sacred constraints, hoặc CEO tại
`helix-s2c-preflight` cho part standalone). Mọi block downstream chỉ ĐỌC label và bật egress guard.
MẬT = offline-only tuyệt đối; vi phạm → `[CLASSIFICATION-VIOLATION]` + STOP.

## Điều IV — LLM Spatial Blindness
AI KHÔNG bịa kích thước, KHÔNG tự chứng nhận hình học. Số thiếu = `[NEEDS CLARIFICATION]`,
không phải số đoán. Render PNG là bằng chứng — CEO kiểm, AI không tự duyệt.
Part không tham số hóa được → Geometry Source Gate route sang Flow D (người vẽ ngoài).

## Điều V — Vật liệu & độ dày chuẩn Workshop X
Chỉ dùng vật liệu trong whitelist (kê ở Machine-Checkable Extract). Độ dày tấm theo kho chuẩn
của xưởng. Vật liệu ngoài whitelist → cần phê duyệt kỹ sư định danh + amendment constitution.

## Điều VI — Ngân sách khối lượng & hệ số an toàn
Mỗi part có `mass_kg.max` (từ budget P51/spec) và `safety_factor.min` khai trong Extract.
Vượt budget = FAIL gate, không thương lượng trong pipeline.

## Điều VII — DFM mặc định
Min wall thickness, min hole-to-edge, fillet policy, dung sai gia công đạt được của xưởng —
khai số trong Extract. Spec nào vi phạm DFM → block `helix-s2c-plan` phải ghi vào Complexity
Tracking với justification hoặc bị chặn.

## Điều VIII — Cổng ra duy nhất
Part CHỈ rời pipeline khi: (1) `validate.py` exit 0 (PASS, contract đúng approved-hash),
(2) CEO đã kiểm render PNG (Điều IV), (3) kỹ sư định danh ký sign-off block. PASS = đạt chuẩn
TỐI THIỂU, không thay chữ ký kỹ sư.

---

## Machine-Checkable Extract → `design_rules.json`

> Block `helix-s2c-preflight` copy JSON dưới đây thành `design_rules.json` của project.
> **Kỹ sư định danh** điền số thật (không placeholder), rồi ghi sha256 (`--approved-hash`).
> Key theo `helix-cad-validate/references/design_rules.schema.md`. Chỉ khai rule cần cưỡng chế.

```jsonc
{
  "meta": {
    "product": "{{project}}",
    "rev": "{{rev}}",
    "contract_version": "1.0.0",
    "classification": "{{label}}",
    "engineer_of_record": "{{họ tên KS}}",
    "approved_by": "",
    "notes": "Compiled from CAD Constitution v{{x.y.z}} Điều V–VII"
  },
  "rules": {
    "materials":          { "allowed": ["{{...}}"], "forbidden": [], "required": true, "severity": "critical" },
    "plate_thickness_mm": { "min": 0.0, "required": true, "min_confidence": "HIGH", "severity": "critical" },
    "mass_kg":            { "max": 0.0, "required": true, "severity": "critical" },
    "safety_factor":      { "min": 0.0, "required": false, "severity": "critical" },
    "tolerance_mm":       { "max": 0.0, "min_confidence": "HIGH", "severity": "major" },
    "mandatory_components": { "items": [], "severity": "major" },
    "conflicts_block":    { "enabled": true, "severity": "critical" },
    "confidence_gate":    { "min_for_critical": "HIGH" }
  }
}
```

## Amendment rule
- CHỈ kỹ sư định danh sửa constitution + Extract. Agent read-only.
- Mọi sửa đổi: bump **Version**, cập nhật **Last Amended**, re-compile `design_rules.json`,
  re-derive sha256, ghi log lý do sửa dưới đây.

| Ngày | Version | Điều sửa | Lý do | Người ký |
|---|---|---|---|---|
