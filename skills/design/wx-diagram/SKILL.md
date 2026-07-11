---
name: wx-diagram
description: "Publication-grade diagram layer for BRIDGE-FORGE-HELIX — routes to the drawio-skill engine (draw.io desktop CLI) to render professional PNG/SVG/PDF diagrams for gate reviews, BQP documents, fabrication handoff, and KHCN proposals. Complements helix-draw (Excalidraw = internal vault sketches); wx-diagram = deliverables leaving the workshop. Triggers on: 'wx-diagram', 'publication diagram', 'export diagram', 'diagram for gate review', 'sơ đồ xuất bản', 'bản vẽ sơ đồ trình duyệt', 'xuất sơ đồ PDF', 'sơ đồ hồ sơ KHCN', 'vẽ quy trình công nghệ', 'vẽ kiến trúc KN-Stack'."
allowed-tools: ["Read", "Write", "Glob", "Grep", "Bash", "PowerShell"]
---

# wx-diagram — Tầng xuất bản sơ đồ (draw.io engine router)

> **Purpose:** Render sơ đồ chất lượng xuất bản (PNG/SVG/PDF) cho deliverable "ra khỏi xưởng".
> **Engine:** drawio-skill (Agents365-ai) qua junction `~/.claude/skills/drawio-skill` → `D:\GitHub\drawio-skill\skills\drawio-skill`.
> **Không thay thế** helix-draw (Excalidraw) — hai tầng bổ trợ.

## Usage

```
/wx-diagram <type> <project> [--source <file>] [--out <dir>] [--format png|svg|pdf]
```

Ví dụ:
```
/wx-diagram swimlane BB-01 --source Handoff_to_Fabrication.md
/wx-diagram block-diagram VN-CUAV-SIM-001 --format pdf
/wx-diagram kn-stack-arch --out docs/
```

## Bảng quyết định engine (block-skills tham chiếu bảng này, không tự quyết)

| Tình huống | Engine | Skill |
|---|---|---|
| Sơ đồ làm việc nội bộ, nhúng Obsidian vault, iterate nhanh | Excalidraw | `helix-draw` |
| Deliverable ra ngoài: gate review pack, tài liệu BQP, fab handoff, hồ sơ KHCN, pitch | draw.io | `wx-diagram` (skill này) |
| Cần shape chuẩn UML/BPMN/P&ID/electrical, swimlane, C4 drill-down | draw.io | `wx-diagram` |
| Diagram-as-code render trong Markdown/GitHub | Mermaid | viết trực tiếp |

## Bước 0 — Prerequisite check (LUÔN chạy trước)

1. **Engine junction:** kiểm tra `~/.claude/skills/drawio-skill/SKILL.md` tồn tại.
   Nếu mất (ví dụ sau dọn máy), tái tạo:
   ```powershell
   New-Item -ItemType Junction -Path "$env:USERPROFILE\.claude\skills\drawio-skill" -Target "D:\GitHub\drawio-skill\skills\drawio-skill"
   ```
2. **CLI:** chạy `& "$env:LOCALAPPDATA\Programs\draw.io\draw.io.exe" --version` (hoặc `C:\Program Files\draw.io\draw.io.exe`). Yêu cầu version ≥ 30.
3. **Fallback (degrade gracefully):** nếu CLI thiếu/quá cũ → vẫn sinh file `.drawio` XML (mở tay trong draw.io desktop/app.diagrams.net) + báo CEO lệnh cài: `winget install --id JGraph.Draw -e`. KHÔNG chặn pipeline.

## Map loại sơ đồ P&B → drawio

| Lệnh `<type>` | Nguồn (P&B / pipeline) | Kiểu drawio | Ghi chú engine |
|---|---|---|---|
| `function-structure` | P1 function structure (helix-p1-structure) | flowchart phân tầng | đọc `references/xml-authoring.md` của engine |
| `block-diagram` | Block diagram SS1-SS5 (P1/P3) | architecture | shapesearch.py cho icon chuẩn |
| `swimlane` | Quy trình công nghệ F0-F5 (forge-fabrication) | swimlane/BPMN | 1 lane / phân xưởng hoặc block F |
| `org-process` | Org chart / process map (BRIDGE) | hierarchy / BPMN | |
| `c4` | Kiến trúc hệ thống (helix-system-arch) | C4 drill-down | `scripts/c4.py` của engine |
| `morpho-result` | Kết quả morpho + concept chọn (P2) | grid + highlight path | chỉ concept ĐÃ CHỌN, không cả matrix |
| `gate-pack` | Gate review G1-G3 / quality-gate | dashboard 1 trang | scores + traffic light + decision |
| `kn-stack-arch` | Self-doc: kiến trúc KN-Stack | architecture | xem mục Self-doc |

Với type chuẩn không cần style riêng → ưu tiên đường Mermaid→drawio của engine (`references/mermaid-authoring.md`, cần CLI ≥ 30) — rẻ token hơn hand-placed XML.

## Style preset Workshop X

Dùng cơ chế style-presets của engine (`references/style-presets.md`). Preset `wx-default`:
- Palette: nền trắng, fill `#dae8fc` (khối chính) / `#d5e8d4` (đạt/GO) / `#f8cecc` (rủi ro/NO-GO) / `#fff2cc` (chờ quyết định), stroke `#333333`.
- Font: Helvetica, 12pt node / 10pt edge label; nhãn tiếng Việt có dấu.
- Mọi sơ đồ có khung tiêu đề: tên dự án + phase + ngày (YYYY-MM-DD) + version.
- Lần đầu chạy: nếu preset chưa tồn tại, tạo bằng flow "learn style" của engine từ các giá trị trên, lưu tên `wx-default`.

## Quy ước output

- Lưu **cặp file**: `<Ten>.drawio` (editable) + `<Ten>.drawio.png` (export `-e` embedded XML — mở lại trong draw.io là sửa được).
- Sau export PNG **luôn** chạy `python ~/.claude/skills/drawio-skill/scripts/repair_png.py <file>` (fix IEND chunk).
- Vị trí: folder dự án trong vault — `D:\Workshop_X\1_Projects\<project>\<phase-folder>\diagrams\`. Self-doc KN-Stack → `docs/` của repo KN-Stack.
- Format PDF chỉ khi hồ sơ yêu cầu (KHCN, BQP); mặc định PNG.

## Bảo mật

- Render 100% **local** qua draw.io desktop CLI — không upload cloud, không browser automation.
- **CẤM** dùng `aiicons.py` (gọi CDN lobe-icons) cho nội dung MẬT/HẠN-CHẾ. Sơ đồ MẬT chỉ dùng shape built-in/offline.
- Không nhúng số liệu MẬT vào diagram gửi ra ngoài — tuân thủ rule "No classified data in prompts".

## Self-doc mode (`kn-stack-arch`)

Vẽ kiến trúc KN-Stack cho `docs/SYSTEM_OVERVIEW.md` / codebase-to-book:
1. Scan `skills/*/` đếm domain + số skill (`bash setup.sh --status`).
2. Sinh architecture diagram: 15 domain làm container, pipeline chính (BRIDGE→FORGE→HELIX, book, mentor) làm edge.
3. Output vào `docs/` cặp `.drawio` + `.drawio.png`.

## Cơ chế kích hoạt (hybrid theo gate)

- **Auto** (các skill này gọi wx-diagram như một bước): `helix-p4-handoff`, `forge-fabrication` (handoff), `forge-proposal-khcn`, `gate1`/`gate2`/`gate3`, `helix-quality-gate`.
- **Suggest-only** (chỉ in 1 dòng gợi ý): `helix-p1-compile`, `helix-p2-select`, `helix-p3-integrate`, `bridge-dashboard`, `bridge-knowledge-base`, `bridge-flywheel`.
- Lý do: mỗi render + vision self-check tốn token — chỉ auto ở điểm "ra khỏi xưởng".

## Workflow

1. Bước 0 prerequisite check (trên).
2. Đọc `--source` (hoặc tự tìm artifact mới nhất của `<project>` theo map).
3. Đọc SKILL.md engine (`~/.claude/skills/drawio-skill/SKILL.md`) + reference tương ứng loại sơ đồ. Làm theo workflow engine: plan layout → sinh XML/Mermaid → export → self-check (tối đa 2 vòng) → repair_png.
4. Áp style preset `wx-default`.
5. Lưu theo quy ước output, báo đường dẫn 2 file cho CEO.

## COD Classification

- **O (Offload):** toàn bộ render/layout/export — AI làm dưới giám sát.
- **C (Core):** CEO duyệt sơ đồ trước khi đưa vào hồ sơ BQP/KHCN (nội dung kỹ thuật là trách nhiệm CEO).
- **D (Default):** repair_png, đặt tên file, tạo folder `diagrams/` — tự động không hỏi.
