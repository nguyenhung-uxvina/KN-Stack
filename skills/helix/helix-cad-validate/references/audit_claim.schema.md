# audit_claim — bản ghi claim chung (G0, lộ trình kiểm bản vẽ P–C–C)

Nguồn kiến trúc: Chen & Cheng 2026, IJCIM, DOI 10.1080/0951192X.2026.2714117 — bảng 2 (hợp đồng tầng, trạng thái an toàn)
và bảng 4 (kiểm báo cáo trôi). Sinh bởi `audit_claims.py`; công cụ gốc (ingest/validate/gates/judge) KHÔNG đổi.

## Một claim
```json
{"claim_id": "C-1a2b3c4d5e", "part_id": "…", "tool": "helix-cad-gates", "tool_version": "1.1/release",
 "rule_id": "F2_probes", "locator": "checks[3]", "observed": "…", "expected": "…", "severity": "critical",
 "status": "FAIL", "message": "…", "source": "cad_gates_report.json"}
```
- `claim_id` = `C-` + sha1(tool|part|rule|locator)[:10] — tất định: chạy lại cùng dữ liệu ra cùng id.
- `locator` hiện là đường dẫn trong báo cáo gốc; G1 sẽ thêm DXF handle + toạ độ + view_id.

## Trạng thái
| Trạng thái | Chặn? | Sinh khi |
|---|---|---|
| PASS | không | luật tất định đạt; judge trả "yes" có chứng cứ |
| ADVISORY | không | INFO của cổng; BREAK-VIEW đã giải theo luật; judge "no" ở câu mức comment; extra_findings của judge |
| FAIL | **có** | luật tất định trượt với đủ dữ liệu; judge "no" ở câu mức block |
| NEEDS_EVIDENCE | **có** | fail-safe thiếu dữ liệu (`observed="(none)"`); SKIP của cổng; thiếu vật liệu; lỗ chỉ đo từ hình học, không ghi Ø |
| NEEDS_RECOGNITION_REVIEW | **có** | giá trị độ tin cậy thấp (`conf=`); hình học chưa nhận dạng (ARC/OCR) |
| NEEDS_RULE_REVIEW | **có** | (G2b) chưa có luật/điều khoản đã duyệt |
| NEEDS_CONTEXT | **có** | mã khung tên không tin cậy; trùng mã chi tiết giữa các tờ (trừ tờ tiếp theo); mã trong bảng kê không có tờ |
| CONTESTED | **có** | chữ ghi đè lệch nét (TEXT-OVERRIDE); cùng claim_id hai quan sát khác nhau; **G2a:** tên bảng kê ≠ tên tờ con, vật liệu bảng kê ≠ tờ con hoặc khung tên ≠ YCKT, số lượng tờ con ∉ bảng kê cha, dạng mã không thống nhất |
| NEEDS_HUMAN_RELEASE | **có** | judge trả "unclear" (hoặc bị hạ vì thiếu chứng cứ) |
| ABSTAINED | **có** | hồ sơ yêu cầu một báo cáo mà không được cung cấp |

Kết luận máy: còn ≥ 1 claim chặn ⇒ `BLOCKED`; không còn ⇒ `READY_FOR_HUMAN_RELEASE`. `RELEASED` chỉ xuất hiện trong
`release.json` do `audit_claims.py release --signer "<tên>"` — tên do chính người ký gõ, máy và agent không điền thay.

## Cổng spec (`audit_claims.py spec`)
Chặn khi spec còn: nhãn `**?**` hoặc ô `| ? |`; mục `## Câu hỏi…`; hoặc mục "Câu hỏi đã được CEO trả lời" (phải viết
lại thành câu khẳng định — agent dựng chỉ đọc spec). Viết quyết định vào `## Quyết định CEO` dạng "KHÔNG dựng …", "Ø14".

## Luật G2a (`set-check`, cả bộ bản vẽ)
`part_code_unique` · `part_code_format` (`--code-case upper|lower` nếu dự án có quy ước; không có thì bộ dùng lẫn ⇒ báo
mọi tờ) · `bom_code_matches_sheet` (mã cụm "X" khớp tờ "X BL") · `bom_name_matches_sheet` · `material_consistent`
(cùng vật liệu khi tập từ bên này nằm trong bên kia) · `qty_matches_parent`. Tên và vật liệu lấy từ khung tên đọc
theo vị trí (G1), không dùng heuristic cũ. Đo trên 157 lỗi đã phân xử: `evals/drawing-audit-bench/RESULTS-2026-11-05.md`.
