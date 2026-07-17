# `dfa_part_count` — DFA producibility rule (design spec for the gate)

> Nguồn động lực: benchmark WX-Pipeline 2026-07-17 (`RESEARCH_benchmark-wx-pipeline_2026-07-17.md`).
> Phát hiện: ROI của should-cost engine tập trung ở **đàm phán mua hàng** ($20.4M) chứ không ở thiết
> kế ($2.5M) — WX tích hợp dọc + air-gap KHÔNG có procurement spend để ép → CAD-costing thương mại
> ROI≈0. Đòn bẩy chi phí THẬT của WX = **DFA của Boothroyd-Dewhurst**: hạ chi phí *cấu trúc* bằng
> **giảm số chi tiết / gộp cụm / bỏ mối ghép rời** TRƯỚC khi lập tool-path. Nạp đòn bẩy đó vào gate.

## 1. Ranh giới Sensor vs con người (trung thực)
Boothroyd DFA thật cần trả lời **3 câu hỏi** cho MỖI chi tiết (xác định "theoretical minimum part"):
1. Chi tiết có **chuyển động tương đối** với cụm đã lắp không?
2. Có **bắt buộc vật liệu khác / cách ly** không?
3. Có **bắt buộc rời** để lắp-tháo được chi tiết khác không?

→ NẾU **không** cả 3 → chi tiết là **ứng viên loại/gộp** (`dfa_essential = false`).

Computational Sensor (`validate.py`) **KHÔNG phán 3 câu này** (đó là suy luận kỹ thuật — Inferential).
Nó chỉ làm phần **tất định**:
- (a) cưỡng chế **trần** số chi tiết + tỷ lệ mối ghép rời (đếm được từ BOM);
- (b) tính **DFA index = Σqty(essential)/Σqty(all)** CHỈ KHI BOM mang cờ `dfa_essential` (kỹ sư/agent
  trả lời 3 câu trong embodiment). Thiếu cờ → fail-safe theo `require_complete` (giống
  `mass_reconciliation`). Đây là split Computational–Inferential mà contract đã theo.

## 2. Contract schema (rule mới — thêm vào `rules{}`)
```jsonc
"dfa_part_count": {
  "scope": "assembly",              // thao tác trên extract.bom[] như một cụm lắp
  "max_parts": 40,                  // trần tổng số chi tiết (Σ qty). null = không kiểm
  "max_fastener_ratio": 0.30,       // fasteners / tổng instance. null = không kiểm
  "min_dfa_index": 0.60,            // Σqty(essential)/Σqty(all); cần cờ dfa_essential trên mỗi row
  "fastener_keywords": ["bolt","screw","nut","washer","rivet","stud",
                        "bu lông","bu long","vít","vit","đai ốc","dai oc",
                        "long đen","long den","đinh tán","dinh tan","ốc","oc"],
  "advisory": true,                 // true → vi phạm phát WARN (gate MỞ); false → FAIL (gate ĐÓNG)
  "require_complete": true,         // đặt min_dfa_index mà thiếu cờ dfa_essential → WARN(advisory)/FAIL(gating)
  "required": false,                // không có BOM: required→(advisory?WARN:FAIL); else SKIP
  "severity": "major",             // chỉ phân loại báo cáo
  "notes": "Ngưỡng PLACEHOLDER — kỹ sư định danh calibrate theo họ sản phẩm. advisory:true tới khi BOM mang cờ dfa_essential."
}
```
**Vòng đời (theo đúng nếp `mass_reconciliation`):** ra đời `advisory:true` + `required:false` →
kỹ sư calibrate `max_parts`/`max_fastener_ratio`/`min_dfa_index` theo dữ liệu thật → khi BOM đã
mang `dfa_essential` ổn định → nâng `advisory:false` để DFA **đóng gate**.

**BOM cần thêm 1 trường** (mỗi row `extract.bom[]`): `"dfa_essential": true|false` — kết quả 3 câu
Boothroyd. Không có trường này thì DFA index không tính (fail-safe); trần part/fastener vẫn chạy.

## 3. Drop-in cho `validate.py` (dán sau khối "8. Load class", trước `return r`)
Khớp đúng style hiện có (`r.add`, `_norm`, WARN không gating).
```python
    # 9. DFA part-count (producibility — Boothroyd-Dewhurst Design for Assembly).
    # Tất định: trần số chi tiết + tỷ lệ mối ghép rời (fastener = ứng viên loại #1 của DFMA);
    # DFA index = essential/total CHỈ khi BOM mang cờ dfa_essential (3 câu Boothroyd — kỹ sư trả
    # lời ở embodiment; Sensor KHÔNG phán). advisory:true => WARN (gate mở); false => FAIL (gate đóng).
    dfa = rs.get("dfa_part_count")
    if dfa:
        sev = dfa.get("severity", "major")
        st = "WARN" if dfa.get("advisory", True) else "FAIL"
        bom = extract.get("bom", []) or []
        kws = [_norm(k) for k in dfa.get("fastener_keywords", [])]
        if not bom:
            if dfa.get("required", False):
                r.add("dfa_part_count", st, sev, "(no BOM)", "assembly BOM",
                      "Không có BOM để tính DFA — " + ("cảnh báo" if st == "WARN" else "fail-safe") + ".",
                      fix="Cấp BOM cụm (extract.bom[]) với qty + tên part.", source="extract.bom")
        else:
            total = fasteners = essential = 0.0
            flagged = 0
            for b in bom:
                try:
                    qty = float(b.get("qty") or 1)
                except (TypeError, ValueError):
                    qty = 1.0
                total += qty
                tag = _norm(b.get("name") or b.get("item") or b.get("code"))
                if kws and any(k in tag for k in kws):
                    fasteners += qty
                fl = b.get("dfa_essential")
                if isinstance(fl, bool):
                    flagged += 1
                    if fl:
                        essential += qty
            mp = dfa.get("max_parts")
            if mp is not None:
                ok = total <= float(mp)
                r.add("dfa_part_count.max_parts", "PASS" if ok else st, sev,
                      f"{int(total)} parts", f"<= {mp}",
                      "Số chi tiết trong trần DFA." if ok else
                      f"Số chi tiết {int(total)} > trần {mp} — gộp cụm / bớt part.",
                      fix="" if ok else "Gộp chi tiết chức năng liền, loại part thừa (3 câu Boothroyd).",
                      source="extract.bom")
            mfr = dfa.get("max_fastener_ratio")
            if mfr is not None and total > 0:
                ratio = fasteners / total
                ok = ratio <= float(mfr)
                r.add("dfa_part_count.fastener_ratio", "PASS" if ok else st, sev,
                      f"{ratio:.0%} ({int(fasteners)}/{int(total)})", f"<= {float(mfr):.0%}",
                      "Tỷ lệ mối ghép rời đạt." if ok else
                      f"Tỷ lệ mối ghép rời {ratio:.0%} > {float(mfr):.0%} — thay bằng snap-fit/hàn/liền khối.",
                      fix="" if ok else "Giảm bu lông/vít; ghép tích hợp (DFMA: fastener = ứng viên loại #1).",
                      source="extract.bom")
            mdi = dfa.get("min_dfa_index")
            if mdi is not None:
                if flagged < len(bom) and dfa.get("require_complete", True):
                    r.add("dfa_part_count.dfa_index", st, sev,
                          f"{flagged}/{len(bom)} rows có cờ", "mọi row có dfa_essential",
                          "Chưa đủ cờ dfa_essential (3 câu Boothroyd) để tính DFA index — "
                          + ("cảnh báo" if st == "WARN" else "fail-safe") + ".",
                          fix="Gán dfa_essential (true/false) cho mọi row: chuyển động? / vật liệu khác? / cần rời để tháo-lắp?",
                          source="extract.bom")
                elif total > 0:
                    idx = essential / total
                    ok = idx >= float(mdi)
                    r.add("dfa_part_count.dfa_index", "PASS" if ok else st, sev,
                          f"{idx:.2f} ({int(essential)}/{int(total)})", f">= {mdi}",
                          "DFA index đạt." if ok else
                          f"DFA index {idx:.2f} < {mdi} — nhiều part không thiết yếu.",
                          fix="" if ok else "Loại/gộp part có dfa_essential=false.", source="extract.bom")
```

## 4. Vị trí trong G1–G3 (Guide + Sensor, hai vai)
| Gate | Pha P&B | Vai của `dfa_part_count` |
|---|---|---|
| **Guide (trước khi vẽ)** | P2→P3 (embodiment) | Nạp rule vào AGENTS.md/context: agent embody phải **tối thiểu số chi tiết + tránh mối ghép rời**, và **gán `dfa_essential`** cho mỗi part khi dựng BOM cụm. |
| **G1** (helix-p3-* / design-journal) | P3 layout | `advisory:true` — validate.py chạy, DFA phát **WARN** để KS thấy sớm; gate KHÔNG chặn (đang phác hình). |
| **G2** (helix-design-review / quality-gate) | P3 cuối | Vẫn advisory hoặc `advisory:false` sau calibrate — DFA index + fastener ratio vào review rubric; FAIL nếu vượt trần đã chốt. |
| **G3** (Handoff_to_Fabrication / freeze ICD) | P3→P4 | `advisory:false` — DFA **đóng gate** (exit 2) chặn handoff sang forge-fabrication nếu part-count/fastener/DFA-index không đạt. Cùng cơ chế `--approved-hash` chống sửa rào. |

**Nguyên tắc giữ nguyên:** PASS = đạt chuẩn TỐI THIỂU, không thay chữ ký kỹ sư định danh. DFA index
do KS trả lời 3 câu (Inferential); Sensor chỉ cưỡng chế phần đếm được (Computational).

## 5. schema.md — dòng thêm vào bảng Rules
```
| `dfa_part_count` | DFA producibility (Boothroyd-Dewhurst): trần số chi tiết + tỷ lệ mối ghép + DFA index | `max_parts`, `max_fastener_ratio`, `min_dfa_index`, `fastener_keywords[]`, `advisory` (bool), `require_complete`, `required`, `scope`, `severity` |
```

## 6. Đã WIRE + hermetic xanh (2026-07-17)
- ✅ `validate.py` §9 (sau §8, trước `return r`) — dán đúng style, WARN không gating.
- ✅ `design_rules.schema.md` — dòng rule + trường.
- ✅ `design_rules.vsn1500.example.json` — rule mẫu `dfa_part_count` (advisory:true, required:false).
- ✅ Fixtures `examples/dfa_{pass,fail,failsafe}.cad_extract.json` + `dfa_rules_{gating,advisory}.json`
  + `dfa_corpus.json` (5 case regression).
- ✅ **Hermetic 5/5 xanh** (exit-code trực tiếp, k=3 tất định `02020`×3):
  PASS-clean(0) · FAIL-gating(2) · **WARN-advisory(0)** · FAILSAFE-gating(2) · **FAILSAFE-advisory(0)**.
  Cùng fixture 44-part/82%-fastener/index-0.02: advisory→3×WARN→gate MỞ; gating→3×FAIL→gate ĐÓNG.

**Còn lại (khi BOM thật có `dfa_essential`):** kỹ sư calibrate `max_parts`/`max_fastener_ratio`/
`min_dfa_index` theo họ sản phẩm → nâng `advisory:false` để DFA đóng gate G3.
> ⚠️ 2026-07-17: `examples/eval_harness.py` + fixtures `mr_*` + `corpus.json` bị một tiến trình song
> song XOÁ khi wire (không phải do DFA). DFA chứng minh bằng exit-code trực tiếp (không cần harness).
> Khi harness được khôi phục, merge 5 case DFA từ `dfa_corpus.json` vào `corpus.json`.
