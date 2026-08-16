---
name: forge-pulse
description: Ingest /last30days research briefings into the IPARAG ecosystem — reads raw research files from ~/Documents/Last30Days, distills findings into a 0_Inbox capture note with why-context, proposes Galaxy permanent-note candidates (propose-only, never auto-create), optionally pushes the raw file into a NotebookLM notebook and routes insights to forge-market-intel or a mentor-board consult. Triggers on: "forge pulse", "pulse ingest", "ingest last30days", "nạp last30days vào vault", "đưa research vào Galaxy", "chuyển briefing vào Inbox", "pulse to notebooklm", "đẩy kết quả research vào hệ thống".
---

# forge-pulse — Last30Days → IPARAG Ingestion

Nối đầu ra của `/last30days` (social-listening briefing) vào vòng THỊNH:
**Thu** (Inbox capture) → **Hóa** (Galaxy candidates, propose-only) → **Ích** (wikilinks) → **Hành** (route sang forge-market-intel / mentor-board).

> Vault: `D:\Workshop_X\` (KHÔNG dùng đường dẫn E:\ cũ).
> Raw files: `$LAST30DAYS_MEMORY_DIR/*-raw*.md` — hiện trỏ về `D:\Workshop_X\3_Resources\Last30Days-Research\` (set trong `~/.config/last30days/.env`); fallback `~/Documents/Last30Days/` nếu biến trống. Mỗi entity một file; comparison runs có nhiều file.

## Invocation

```
/forge-pulse                          # ingest raw file mới nhất
/forge-pulse <slug>                   # ingest file khớp slug (vd: openclaw, ai-agent-harness)
/forge-pulse <slug> --nlm <notebook>  # + đẩy raw file vào NotebookLM notebook
/forge-pulse <slug> --consult <mentor># + gợi ý câu hỏi consult cho mentor skill
```

## Pipeline (4 bước)

### P0 — Locate & Read (Offload)
1. Resolve thư mục: đọc `LAST30DAYS_MEMORY_DIR` từ `~/.config/last30days/.env` (hiện: `D:\Workshop_X\3_Resources\Last30Days-Research\`), fallback `~/Documents/Last30Days/`. List thư mục đó, chọn file theo slug hoặc mới nhất (mtime).
2. Comparison run → đọc TẤT CẢ file per-entity liên quan (main + peers).
3. Đọc cả phần `## WebSearch Supplemental Results` — đó là citation bền.

### P1 — Thu: Inbox Capture (Offload, auto-write OK)
Tạo MỘT file capture tại `D:\Workshop_X\0_Inbox\YYYY-MM-DD-pulse-<slug>.md`:
- Frontmatter chuẩn PARA (`type: clipping`, `status: inbox`, tags `#type/clipping #status/inbox #topic/...`).
- **Why-context bắt buộc**: 1-2 câu vì sao CEO quan tâm topic này (liên hệ sản phẩm/quyết định nào của Workshop X).
- 3-5 findings đắt nhất, mỗi finding kèm nguồn (per @handle / r/sub / kênh YouTube).
- Con số cứng (stars, %, benchmark) tách riêng thành bảng để tra nhanh.
- Link về raw file gốc.

### P2 — Hóa: Galaxy Candidates (Core — PROPOSE ONLY)
Từ findings, nhận diện 1-3 **khái niệm atomic** đáng thành permanent note:
- Mỗi candidate: tên note đề xuất, 1 đoạn tóm tắt khái niệm, ≥2 wikilink đề xuất tới note Galaxy hiện có, cluster tag (#sys/#product/#defense/#meta...).
- **KHÔNG tự tạo file trong 5_Galaxy/** — hiển thị draft và hỏi CEO duyệt. CEO duyệt → gọi flow `/galaxy-note` cho từng note.
- Test atomic: nếu khái niệm chỉ đúng trong 30 ngày (tin tức) → KHÔNG đề xuất; chỉ đề xuất khái niệm sống lâu (nguyên lý, pattern, trade-off).

### P3 — Hành: Route (Offload, đề xuất)
Đề xuất tối đa 2 tuyến hành động, nêu rõ COD:
- **forge-market-intel**: nếu briefing chứa tín hiệu thị trường/đối thủ liên quan danh mục sản phẩm (V-SMASH, VN-CUAS-001, BB-01...) → soạn sẵn 1 đoạn input cho phiên forge-market-intel kế tiếp.
- **mentor-board**: nếu briefing chạm chuyên môn của mentor có sẵn (vd harness engineering → mentor-harness-engineering-council) → soạn sẵn 1 câu hỏi consult cụ thể, trích số liệu từ briefing.
- `--nlm <notebook>`: dùng notebooklm-mcp `source_add` (source_type=file) đẩy raw file vào notebook chỉ định; báo lại số source hiện có.

## Quy tắc cứng
1. Galaxy = propose-only. Không có ngoại lệ (AI Permissions, global CLAUDE.md).
2. Inbox capture PHẢI có why-context — capture không có "vì sao" là rác.
3. Không nhét >1 khái niệm vào 1 Galaxy candidate (atomic principle).
4. Mọi claim số liệu giữ nguyên citation từ briefing — không citation nào tự chế.
5. Phân loại COD cho mọi đề xuất hành động (C = CEO tự làm, O = AI làm dưới giám sát, D = bỏ qua).

## Output chuẩn
```
📥 PULSE INGEST — <topic> (<ngày run>)
├─ Inbox: 0_Inbox/YYYY-MM-DD-pulse-<slug>.md ✅ (đã tạo)
├─ Galaxy candidates (chờ CEO duyệt):
│   1. [[<tên note>]] — <1 câu> (links: [[A]], [[B]]) — #<cluster>
│   2. ...
├─ Route đề xuất:
│   • [O] forge-market-intel: <1 câu input>
│   • [C] mentor-board consult <mentor>: "<câu hỏi>"
└─ NLM: <notebook> +1 source (nếu --nlm)
```
