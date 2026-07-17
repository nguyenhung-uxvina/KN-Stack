# `design_rules.json` — Contract schema (the GUIDE + the SENSOR's yardstick)

> The contract is the versioned, **read-only-to-agent** design-rule set. It is BOTH a Guide
> (nạp vào AGENTS.md/context trước khi agent vẽ) and the yardstick the Computational Sensor
> (`validate.py`) scores against. Only a **kỹ sư định danh** edits it; every edit bumps
> `contract_version` and re-derives the approved sha256.

## Top-level
```jsonc
{
  "meta": {
    "product": "VSN-1500-HKN",
    "rev": "A",
    "contract_version": "1.0.0",
    "classification": "HẠN-CHẾ",          // MẬT | HẠN-CHẾ | THƯỜNG
    "engineer_of_record": "Họ tên KS",     // người ký cổng cuối
    "approved_by": "",                      // ai duyệt contract này
    "notes": "Nguồn ràng buộc: RE VSN-1500 + TCVN/AWS D1.2/ISO 9606-2"
  },
  "rules": { ... }                          // xem dưới — chỉ khai báo rule muốn cưỡng chế
}
```

## Rules (mỗi rule tùy chọn — chỉ khai cái cần)
| Rule key | Ý nghĩa | Trường |
|---|---|---|
| `materials` | Whitelist/blacklist vật liệu | `allowed[]`, `forbidden[]`, `required` (bool), `severity` |
| `plate_thickness_mm` | Độ dày tấm tối thiểu | `min`, `required`, `min_confidence` (LOW/MED/HIGH), `severity` |
| `mass_kg` | Khối lượng tối đa | `max`, `required`, `severity` |
| `mass_reconciliation` | Đối chiếu khối lượng bottom-up ↔ lightship estimate (Sanity-Check vật lý cho tàu) | `reference_kg`, `tolerance_pct` (5.0), `part_tolerance_pct` (3.0), `scope` (`assembly`\|`part`), `required`, `require_complete`, `densities_kg_m3{}`, `severity` |
| `safety_factor` | Hệ số an toàn tối thiểu | `min`, `required`, `severity` |
| `tolerance_mm` | Dung sai tuyệt đối tối đa | `max`, `min_confidence`, `severity` |
| `mandatory_components` | Thành phần bắt buộc hiện diện | `items[]` (string hoặc list synonym), `severity` |
| `weld_standard` | Phải viện dẫn ≥1 chuẩn hàn | `required_any[]`, `severity` |
| `load_class` | Hạng tải phải có / cấm | `required[]`, `forbidden[]`, `severity` |
| `conflicts_block` | Chặn nếu extract còn CONFLICT | `enabled` (bool), `severity` |
| `bom_master` | Đối chiếu mã chi tiết với parts_master authoritative (đóng "BOM=0") | `master_csv` (đường dẫn CSV từ authoritative_bom.py), `required`, `ignore_codes[]` (mã gốc cụm bỏ qua), `enabled`, `severity` |
| `dfa_part_count` | DFA producibility (Boothroyd-Dewhurst): trần số chi tiết + tỷ lệ mối ghép + DFA index | `max_parts`, `max_fastener_ratio`, `min_dfa_index`, `fastener_keywords[]`, `advisory` (bool), `require_complete`, `required`, `scope`, `severity` |
| `confidence_gate` | Ngưỡng tin cậy mặc định cho rule critical | `min_for_critical` (HIGH) |

### `bom_master` chi tiết (2 check con)
- **`bom_present`** — fail-safe: thiếu/không đọc được `master_csv` → FAIL (BOM=0 không thể chứng nhận).
- **`bom_reconciled`** — mã `meta.code_in_dxf`/`part_id` của extract phải có trong master; mã gốc cụm (vd `GT.00.00.00`) khai trong `ignore_codes` để bỏ qua. *Lưu ý:* phát hiện **stale-code theo TÊN** (tên khớp mã khác) chỉ chạy khi tên extract sạch — tên DXF garble (unicode escape) thì để `check_bom.py` chấm trên tài liệu QTCN (tên sạch). Nguồn sự thật = CSV kỹ sư ký, KHÔNG phải title-block.

### `mass_reconciliation` chi tiết (Sanity-Check vật lý — Δ-C, phương pháp Fairley cho tàu)
Neo bằng **vật lý**, không "đo theo tỷ lệ thước": tổng khối lượng bottom-up phải khớp ước tính
lightship của naval-architect trong dung sai %. Lệch = dấu hiệu **sai trích xuất / thiếu part /
vật liệu-độ-dày sai** — bắt được lỗi mà không rule đơn lẻ nào bắt.
- **Nguồn bottom-up (thứ tự ưu tiên):** `mass_props.bottom_up_kg` (helix-cad-bridge/aggregate tính từ
  hình học — tin cậy nhất) → nếu không có, tính từ BOM: `Σ qty × area_m2 × (thickness_mm/1000) × ρ(material)`.
  validate.py **không bịa** diện tích tấm extract không có: BOM thiếu `area_m2`/`thickness_mm`/vật-liệu-lạ
  → `require_complete:true` (mặc định) cho **FAIL** (tổng thiếu ≠ tin cậy).
- **Dung sai:** `scope:"assembly"` dùng `tolerance_pct` (mặc định **±5%**); `scope:"part"` dùng
  `part_tolerance_pct` (mặc định **±3%**, cho part tới hạn). CEO chốt 2 ngưỡng này 2026-07-17.
- **reference_kg** do **kỹ sư định danh** khai (ước tính lightship). Thiếu reference / thiếu bottom-up khi
  `required:true` → FAIL (fail-safe). `ρ` mặc định tra bảng nội bộ (nhôm 5083=2660, 6082=2700, thép=7850…);
  ghi đè per-contract qua `densities_kg_m3`.

## Severity
- `critical` / `major` → mọi FAIL đều **đóng gate** (exit 2). `severity` chỉ để phân loại báo cáo.
- Rule không khai = không kiểm. **Fail-safe:** rule `required:true` mà thiếu dữ liệu → FAIL (không SKIP).

## Confidence gate (chống "đọc sai" lọt cổng)
`cad_extract.json` gắn `confidence` (HIGH/MED/LOW) cho mỗi giá trị (helix-cad-ingest). Rule critical
(độ dày, dung sai) chỉ PASS nếu giá trị nguồn đạt `min_confidence`; giá trị LOW/MED chưa được CEO
chứng nhận → FAIL "uncertified".

## Contract integrity (gate khóa quyền sửa rào của chính nó)
Chạy với `--approved-hash <sha256>`: nếu file contract không khớp hash kỹ sư đã duyệt → FAIL
`contract_integrity`. Ngăn agent lặng lẽ sửa luật để gate xanh. Lấy hash:
`python -c "import hashlib;print(hashlib.sha256(open('design_rules.json','rb').read()).hexdigest())"`
