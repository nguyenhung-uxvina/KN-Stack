# Design: Tích hợp draw.io vào BRIDGE-FORGE-HELIX (wx-diagram)

> Date: 2026-07-11
> Status: Approved by CEO (brainstorming session)
> Engine source: `D:\GitHub\drawio-skill` (Agents365-ai/drawio-skill v1.28.1, MIT)

## 1. Mục tiêu

Thêm **tầng xuất bản sơ đồ** (publication-grade diagrams) vào hệ skill KN-Stack,
dùng draw.io desktop CLI để render PNG/SVG/PDF chuyên nghiệp cho các deliverable
"ra khỏi xưởng": gate review, tài liệu BQP, handoff fabrication, hồ sơ KHCN.

## 2. Kiến trúc 2 tầng sơ đồ

| Tầng | Engine | Skill | Dùng cho |
|------|--------|-------|----------|
| Sketch nội bộ | Excalidraw | `helix-draw` (giữ nguyên) | Sơ đồ làm việc nhúng Obsidian vault, 12 loại HELIX-specific |
| Xuất bản | draw.io CLI | `wx-diagram` (mới) + engine junction | Deliverable trình ra ngoài: PNG/SVG/PDF, shape chuẩn UML/BPMN/P&ID, swimlane |

Hai tầng **bổ trợ, không thay thế nhau**. helix-draw không bị deprecated.

## 3. Thành phần

### 3.1 Prerequisite — draw.io desktop CLI

- Máy hiện **chưa có** `drawio` trên PATH.
- Cài draw.io desktop từ jgraph/drawio-desktop (Windows installer), **version ≥ 30**
  (mở khóa Mermaid→drawio conversion + ELK `--layout`).
- Graphviz (`dot`) tùy chọn — cần cho `autolayout.py` (sơ đồ >15 node).
- Verify: `drawio --version`.

### 3.2 Junction engine gốc

```
~/.claude/skills/drawio-skill  →  D:\GitHub\drawio-skill\skills\drawio-skill
```

- Upstream cập nhật bằng `git pull` trong `D:\GitHub\drawio-skill` — KN-Stack
  KHÔNG vendor/fork code ngoài.
- KN-Stack chỉ chứa wrapper `wx-diagram` (mỏng, tự viết).

### 3.3 Skill wrapper mới: `skills/design/wx-diagram/`

`SKILL.md` với frontmatter chuẩn KN-Stack (name + description có Triggers on EN/VN). Nội dung:

1. **Bảng quyết định engine** — khi nào dùng Excalidraw (nội bộ vault) vs
   draw.io (deliverable ra ngoài). Block-skills tham chiếu bảng này, không tự quyết.
2. **Map loại sơ đồ P&B → drawio type:**
   - Function structure (P1) → flowchart phân tầng
   - Block diagram SS1-SS5 (P1/P3) → architecture diagram
   - Quy trình công nghệ F0-F5 (FORGE) → swimlane
   - Org chart / process map (BRIDGE) → hierarchy / BPMN
   - Kiến trúc hệ thống → C4 drill-down (`c4.py`)
3. **Style preset Workshop X** — dùng cơ chế style-presets sẵn của drawio-skill;
   palette + font thống nhất, nhãn tiếng Việt.
4. **Quy ước output:** lưu cặp `.drawio` (editable) + `.drawio.png` (embedded XML,
   chạy `repair_png.py` sau export) vào folder dự án trong vault
   (`1_Projects/<project>/...`). Mở lại được trong draw.io để sửa tay.
5. **Ghi chú bảo mật:** render 100% local qua desktop CLI, không upload cloud.
   Riêng `aiicons.py` gọi CDN (lobe-icons) → **CẤM dùng cho nội dung MẬT/HẠN-CHẾ**.
6. **Self-doc mode:** lệnh "vẽ kiến trúc KN-Stack" — scan 15 domain trong `skills/`
   → architecture diagram cho SYSTEM_OVERVIEW / codebase-to-book.

### 3.4 Hook vào block-skills (cơ chế hybrid theo gate)

**Auto** — điểm "ra khỏi xưởng", thêm bước xuất bản vẽ qua wx-diagram:

| Skill | Sơ đồ xuất |
|-------|-----------|
| `helix-p4-handoff` | Assembly / block diagram cho fab bundle |
| `forge-fabrication` (handoff block) | Quy trình công nghệ F0-F5 swimlane |
| `forge-proposal-khcn` | Sơ đồ trong hồ sơ KHCN |
| `gate1` / `gate2` / `gate3` + `helix-quality-gate` | Gate review pack |

**Suggest-only** — thêm 1 dòng gợi ý `/wx-diagram`, không auto-render:
các block compile P1-P3 (`helix-p1-compile`, `helix-p2-select`, `helix-p3-integrate`),
`bridge-dashboard`, `bridge-knowledge-base`, `bridge-flywheel`.

Lý do hybrid: mỗi lần render + vision self-check tốn token đáng kể (Cost Management
rule trong CLAUDE.md global).

### 3.5 Eval + housekeeping

- Eval spec static-mode: `evals/wx-diagram.json` (chuẩn KN-Stack cho skill orchestrator).
- CHANGELOG entry + VERSION bump (gộp với bump Assay đang chờ).
- Branch: `feature/design-drawio-integration`.

## 4. KHÔNG làm (YAGNI)

- KHÔNG viết lại 12 diagram type của helix-draw sang draw.io.
- KHÔNG fork/vendor drawio-skill vào KN-Stack.
- KHÔNG auto-render ở mọi block (chỉ auto tại gate/handoff).
- KHÔNG dùng browser automation / cloud render.

## 5. Rủi ro & giảm thiểu

| Rủi ro | Giảm thiểu |
|--------|-----------|
| draw.io CLI chưa cài / version < 30 | wx-diagram check `drawio --version` trước, hướng dẫn cài; fallback: chỉ sinh `.drawio` XML không export |
| Upstream drawio-skill đổi cấu trúc | Wrapper chỉ tham chiếu SKILL.md + scripts qua đường dẫn junction ổn định; pin bằng ghi chú version trong wx-diagram |
| Token cost vision self-check | Hybrid activation; suggest-only ở block thường |
| Nội dung MẬT lọt CDN | Rule cấm aiicons.py cho MẬT/HẠN-CHẾ ghi thẳng trong SKILL.md |
| Junction bị mất khi setup.sh --unlink | wx-diagram degrade gracefully: báo thiếu engine + lệnh tái tạo junction |

## 6. Tiêu chí hoàn thành

1. `drawio --version` chạy được, ≥ 30.
2. Junction resolve đúng, engine gọi được từ Claude Code.
3. `/wx-diagram` render thử 1 sơ đồ swimlane F0-F5 mẫu → `.drawio` + `.drawio.png` mở được trong draw.io.
4. 7 skill auto-hook (bảng 3.4) + 6 skill suggest-only đã có đoạn tham chiếu wx-diagram.
5. Eval static `bash evals/run-eval.sh wx-diagram` pass.
