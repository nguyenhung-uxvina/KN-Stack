# P1 RE-Explore — brief cho tác tử đọc một cụm

> Dùng ở P1.3 của `/re-to-book`. Orchestrator điền `{{…}}` rồi giao nguyên văn cho mỗi tác tử (một cụm/tác tử, cùng một message).

## ⛔ NEO PHẢI NẰM TRONG BACKTICK

Mã đơn vị có dấu cách (`#Khung chính`, `#Cây SF`). Neo trần bị cổng cắt ở dấu cách đầu tiên ⇒ "không có đơn vị" ⇒ `check-p1` mã 1.

```
ĐÚNG:  `Megalink_3D-Score/RE_3DS_Hypotheses.md#GT-3DS-001.6`
ĐÚNG:  `Megalink_3D-Score/RE_3DS_S1A_Deconstruction.md#Khung chính`
SAI :  Megalink_3D-Score/RE_3DS_S1A_Deconstruction.md#Khung chính      ← bị cắt thành #Khung
SAI :  D:/Workshop_X/.../RE_3DS_Hypotheses.md#GT-3DS-001.6            ← đường dẫn tuyệt đối
```

Neo = `<thư mục hồ sơ>/<tệp>#<mã đơn vị>`, **chép nguyên cột `anchor` của `_units_index.md`** — không tự gõ, không tự đặt mã.

## Brief

```
Bạn đọc cụm "{{cluster_name}}" ({{cluster_scope}}) cho sách nội bộ "{{slug}}".
Người đọc: kỹ sư Workshop X.

NGUỒN — CHỈ HAI CHỖ NÀY:
  - {{Book}}/Phase1-Exploration/_units_index.md   (bảng neo · lớp · nhãn · mức tin)
  - {{Book}}/_re_snapshot/<các tệp của cụm: {{file_list}}>
KHÔNG đọc thư mục RE gốc, Idea_Log, Legal_Gate, BOM, GapFill chưa duyệt — chúng không có trong
bản chụp là có chủ ý. Ô `⟨chờ ký⟩` / `⟨chờ đo⟩` là chỗ chưa có dữ liệu: KHÔNG suy ra số.

MỖI Ý PHẢI MANG BA THỨ:
  1. Nhãn tri thức + mức tin — LẤY TỪ CỘT `nhãn`/`mức tin` của _units_index.md, không tự gán.
     knowledge | conjecture | assumption | chưa gán. Mức tin "-" ⇒ ghi "-".
  2. Neo trong backtick: `<hồ sơ>/<tệp>#<mã đơn vị>`
  3. Mã nguồn công khai (sáng chế, sổ tay, tiêu chuẩn) nếu ý dựa trên tài liệu ngoài — để P7 kiểm trích.

Dạng một dòng ý:
  - <ý, viết bằng lời của bạn> — [conjecture · M] `Megalink_3D-Score/RE_3DS_S1A_Deconstruction.md#Khung chính` · nguồn: US1234567B2

Ý `chưa gán`: ghi đúng `[chưa gán]` — KHÔNG nâng thành knowledge. Orchestrator gom vào
`## Nhãn chưa gán cần quyết` để CEO quyết.
Ý `conjecture`/`assumption`: viết rõ là phỏng đoán/giả định ngay trong câu.

GHI: {{Book}}/Phase1-Exploration/{{cluster_slug}}_Exploration.md theo schema dưới.
Mọi tệp Exploration phải có ÍT NHẤT một neo (cổng check-p1).
```

## Schema đầu ra (tương thích `book-explore` — P2+ không cần biết nguồn là RE)

```markdown
# Exploration — {{cluster_name}}
Date: {{date}} | Agent: {{id}} | Nguồn: _re_snapshot/ (manifest {{manifest_created}})

## Architecture and Module Boundaries
## Key Abstractions
## Data Flow
## Design Patterns
## Integration Points
## Surprising Decisions
## Open Questions
## Nhãn và neo đã dùng
| Neo | Nhãn | Mức tin | Dùng ở mục |
|---|---|---|---|
```

Mục nào cụm không có nội dung ⇒ ghi `(không có trong hồ sơ RE)`, không bịa cho đủ mục. Cụm V (Chỗ chưa biết) dùng
`## Open Questions` làm thân chính: phiếu GT (trạng thái `⟨chờ đo⟩`/`⟨chờ ký⟩`/đã đo), mâu thuẫn `N-xxx`, Precision_Debt.

## Orchestrator kiểm sau fan-out

```bash
python -X utf8 "$RTB/re_provenance.py" check-p1 --book "<Book>"   # mã ≠ 0 ⇒ trả lại tác tử, cấm checkpoint
```
Kiểm tra cổng được tin: trước lần chạy thật đầu tiên, viết một tệp `zz_neg_Exploration.md` chứa một neo trần có dấu cách ⇒ phải mã 1; xoá tệp đó rồi chạy lại.
