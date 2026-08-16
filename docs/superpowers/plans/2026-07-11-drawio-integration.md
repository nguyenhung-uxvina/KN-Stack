# draw.io Integration (wx-diagram) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Thêm tầng xuất bản sơ đồ draw.io (skill `wx-diagram` + engine junction) vào BRIDGE-FORGE-HELIX theo spec `docs/superpowers/specs/2026-07-11-drawio-integration-design.md`.

**Architecture:** Engine drawio-skill (bên thứ 3, `D:\GitHub\drawio-skill`) được junction vào `~/.claude/skills/` — KHÔNG vendor. KN-Stack chỉ thêm 1 wrapper skill `skills/design/wx-diagram/SKILL.md` (routing + style + quy ước), 1 eval static, và các đoạn hook trong 13 block-skill hiện có (7 auto tại gate/handoff, 6 suggest-only).

**Tech Stack:** draw.io desktop CLI (≥ 30), PowerShell junction, bash (setup.sh, run-eval.sh), markdown skills.

## Global Constraints

- draw.io desktop CLI version ≥ 30 (Mermaid→drawio + ELK layout).
- Engine junction: `~/.claude/skills/drawio-skill` → `D:\GitHub\drawio-skill\skills\drawio-skill`.
- KHÔNG copy/fork code drawio-skill vào KN-Stack.
- Skill mới đúng chuẩn KN-Stack: `skills/design/wx-diagram/SKILL.md`, frontmatter `name:` = tên thư mục, `description:` có "Triggers on:" EN + VN.
- `aiicons.py` gọi CDN → CẤM với nội dung MẬT/HẠN-CHẾ (ghi trong SKILL.md).
- Output convention: cặp `.drawio` + `.drawio.png` (embedded XML, chạy `repair_png.py` sau export PNG).
- Commit format: `[DESIGN] ...` / `[HELIX] ...` / `[FORGE] ...` / `[BRIDGE] ...` theo domain; branch `feature/design-drawio-integration` (đã tạo).
- KHÔNG commit vào main. KHÔNG đụng các file đang modified sẵn trong working tree (`skills/book/book-ceo-insight`, `skills/mentors/mentor-chris-brose`, `skills/ops/nlm`, `evals/fixtures/`, `temp/`) — chúng thuộc nhánh việc khác.

---

### Task 1: Cài draw.io CLI + junction engine

**Files:**
- Không sửa file repo; chỉ thao tác hệ thống (winget + junction).

**Interfaces:**
- Produces: lệnh `drawio` chạy được (hoặc đường dẫn tuyệt đối `C:\Program Files\draw.io\draw.io.exe`), junction `~/.claude/skills/drawio-skill` resolve về `D:\GitHub\drawio-skill\skills\drawio-skill`. Task 4 (smoke test) và wx-diagram SKILL.md (Task 2) dùng đường dẫn này.

- [ ] **Step 1: Kiểm tra hiện trạng**

Run (PowerShell):
```powershell
Get-Command drawio -ErrorAction SilentlyContinue; Test-Path "C:\Program Files\draw.io\draw.io.exe"; Test-Path "$env:LOCALAPPDATA\Programs\draw.io\draw.io.exe"
```
Expected: cả 3 trả về rỗng/False (chưa cài). Nếu đã cài ở đâu đó → bỏ qua Step 2, ghi lại đường dẫn thật.

- [ ] **Step 2: Cài draw.io desktop qua winget**

Run (PowerShell):
```powershell
winget install --id JGraph.Draw -e --accept-source-agreements --accept-package-agreements
```
Expected: "Successfully installed". Nếu winget không có/bị chặn → báo CEO tải installer từ https://github.com/jgraph/drawio-desktop/releases (bản ≥ 30.x) và dừng task chờ cài xong.

- [ ] **Step 3: Verify version ≥ 30**

Run (PowerShell):
```powershell
& "C:\Program Files\draw.io\draw.io.exe" --version
```
Expected: in ra số version, major ≥ 30. (Nếu cài per-user thì exe ở `$env:LOCALAPPDATA\Programs\draw.io\draw.io.exe` — dùng đường dẫn đó nhất quán cho các bước sau.)

- [ ] **Step 4: Tạo junction engine**

Run (PowerShell):
```powershell
New-Item -ItemType Junction -Path "$env:USERPROFILE\.claude\skills\drawio-skill" -Target "D:\GitHub\drawio-skill\skills\drawio-skill"
```
Expected: junction tạo thành công. Nếu `~/.claude/skills` chưa tồn tại, tạo trước bằng `New-Item -ItemType Directory`.

- [ ] **Step 5: Verify junction**

Run (PowerShell):
```powershell
Test-Path "$env:USERPROFILE\.claude\skills\drawio-skill\SKILL.md"
```
Expected: `True`.

Không có gì để commit ở task này (thao tác ngoài repo).

---

### Task 2: Eval spec + wx-diagram SKILL.md (TDD)

**Files:**
- Create: `evals/wx-diagram.json`
- Create: `skills/design/wx-diagram/SKILL.md`
- Test: `bash evals/run-eval.sh wx-diagram`

**Interfaces:**
- Consumes: đường dẫn engine + exe từ Task 1.
- Produces: skill `/wx-diagram <type> <project> [--source <file>] [--format png|svg|pdf]` — tên lệnh này được 13 hook ở Task 5-6 tham chiếu nguyên văn là `/wx-diagram`.

- [ ] **Step 1: Viết eval spec (failing test)**

Tạo `evals/wx-diagram.json`:

```json
{
  "skill": "wx-diagram",
  "version": "1.0",
  "description": "Binary assertions for /wx-diagram publication-diagram wrapper (draw.io engine router)",
  "mode": "static",
  "test_input": "wx-diagram swimlane BB-01 --source Handoff_to_Fabrication.md",
  "assertions": [
    {
      "id": "WXD-ENGINE",
      "name": "engine_decision_table",
      "check": "skill defines when to use Excalidraw (helix-draw) vs draw.io",
      "regex": "helix-draw|Excalidraw.*draw\\.io|bảng quyết định|engine",
      "required": true
    },
    {
      "id": "WXD-PREREQ",
      "name": "prerequisite_check_and_fallback",
      "check": "skill checks drawio CLI >= 30 and degrades gracefully (XML-only) when missing",
      "regex": "--version|≥ ?30|>= ?30|fallback|chỉ sinh .?\\.drawio",
      "required": true
    },
    {
      "id": "WXD-JUNCTION",
      "name": "engine_junction_recovery",
      "check": "skill documents engine junction path and recreation command",
      "regex": "\\.claude[\\\\/]skills[\\\\/]drawio-skill|New-Item -ItemType Junction",
      "required": true
    },
    {
      "id": "WXD-MAP",
      "name": "pb_diagram_map",
      "check": "P&B -> drawio type map covers function structure, block diagram, swimlane F0-F5, C4",
      "regex": "function structure|swimlane|C4|block diagram",
      "required": true
    },
    {
      "id": "WXD-STYLE",
      "name": "wx_style_preset",
      "check": "Workshop X style preset defined via drawio-skill style-presets mechanism",
      "regex": "style.?preset|Workshop X|palette",
      "required": true
    },
    {
      "id": "WXD-OUTPUT",
      "name": "output_conventions",
      "check": "output pair .drawio + .drawio.png with repair_png and vault project folder",
      "regex": "\\.drawio\\.png|repair_png|1_Projects",
      "required": true
    },
    {
      "id": "WXD-SECURITY",
      "name": "security_rules",
      "check": "local-only render + aiicons CDN ban for classified content",
      "regex": "MẬT|HẠN.?CHẾ|aiicons.*CDN|CDN.*aiicons|local",
      "required": true
    },
    {
      "id": "WXD-SELFDOC",
      "name": "kn_stack_self_doc",
      "check": "self-doc mode draws KN-Stack 15-domain architecture",
      "regex": "SYSTEM_OVERVIEW|kiến trúc KN-Stack|self.?doc",
      "required": true
    },
    {
      "id": "WXD-HYBRID",
      "name": "hybrid_activation",
      "check": "documents which skills auto-call vs suggest-only",
      "regex": "auto|suggest.?only|gate|handoff",
      "required": true
    },
    {
      "id": "WXD-COD",
      "name": "cod_classification",
      "check": "COD classification present",
      "regex": "COD|Core|Offload|Default",
      "required": true
    }
  ],
  "passing_score": 10,
  "total_required": 10,
  "total_optional": 0
}
```

- [ ] **Step 2: Chạy eval để thấy FAIL**

Run: `bash evals/run-eval.sh wx-diagram`
Expected: FAIL (SKILL.md chưa tồn tại). Nếu runner lỗi "skill not found" thay vì fail assertions — chấp nhận, đó là trạng thái đỏ hợp lệ.

- [ ] **Step 3: Viết `skills/design/wx-diagram/SKILL.md`**

Nội dung đầy đủ:

````markdown
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
2. **CLI:** chạy `& "C:\Program Files\draw.io\draw.io.exe" --version` (hoặc `$env:LOCALAPPDATA\Programs\draw.io\draw.io.exe`). Yêu cầu version ≥ 30.
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
````

- [ ] **Step 4: Chạy eval để thấy PASS**

Run: `bash evals/run-eval.sh wx-diagram`
Expected: PASS 10/10 required. Nếu fail assertion nào → sửa SKILL.md (không sửa regex cho khớp bừa).

- [ ] **Step 5: Junction skill mới + verify**

Run: `bash setup.sh --install` rồi `bash setup.sh --verify`
Expected: install báo "1 linked, N skipped"; verify không lỗi. (setup.sh chỉ tạo junction còn thiếu, không đụng junction cũ.)

- [ ] **Step 6: Commit**

```bash
git add evals/wx-diagram.json skills/design/wx-diagram/SKILL.md
git commit -m "[DESIGN] wx-diagram — tang xuat ban so do draw.io (wrapper + eval static)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 3: Smoke test end-to-end (render thử swimlane F0-F5)

**Files:**
- Create (tạm, không commit): `temp/wx-diagram-smoke/F0-F5_QuyTrinh_Smoke.drawio` + `.drawio.png`

**Interfaces:**
- Consumes: `/wx-diagram` từ Task 2, CLI + junction từ Task 1.
- Produces: bằng chứng pipeline chạy được (tiêu chí hoàn thành #3 của spec).

- [ ] **Step 1: Render mẫu**

Chạy skill wx-diagram với input: swimlane 6 lane F0→F5 (Preflight → Material → Release → Execute → Acceptance → Invoice), mỗi lane 2-3 node tên tiếng Việt, style `wx-default`, output vào `temp/wx-diagram-smoke/`.

- [ ] **Step 2: Verify output**

Run (PowerShell):
```powershell
Get-ChildItem temp\wx-diagram-smoke\; python -c "print(open(r'temp/wx-diagram-smoke/F0-F5_QuyTrinh_Smoke.drawio').read(200))"
```
Expected: cả `.drawio` và `.drawio.png` tồn tại, PNG > 10KB, `.drawio` bắt đầu bằng XML `<mxfile`. Mở PNG kiểm tra mắt: 6 lane, không chữ tràn khung.

- [ ] **Step 3: Dọn (không commit smoke output)**

`temp/` đã untracked — giữ nguyên làm bằng chứng, KHÔNG `git add`.

---

### Task 4: Auto hooks — 7 skill tại gate/handoff

**Files:**
- Modify: `skills/helix/helix-p4-handoff/SKILL.md` (trước heading `## Next Command`)
- Modify: `skills/helix/helix-quality-gate/SKILL.md` (trước heading `## Rules`)
- Modify: `skills/forge/forge-fabrication/SKILL.md` (cuối section `## HELIX → FORGE Handoff Integration`)
- Modify: `skills/forge/forge-proposal-khcn/SKILL.md` (trước heading `## Gotchas`)
- Modify: `skills/system/gate1/SKILL.md`, `skills/system/gate2/SKILL.md`, `skills/system/gate3/SKILL.md` (append cuối file)

**Interfaces:**
- Consumes: lệnh `/wx-diagram <type> <project>` từ Task 2 (tên type đúng theo map: `block-diagram`, `gate-pack`, `swimlane`, `function-structure`).
- Produces: 7 skill có bước xuất bản vẽ tự động.

- [ ] **Step 1: helix-p4-handoff — thêm section trước `## Next Command`**

Chèn:

```markdown
## Publication diagrams (wx-diagram — AUTO)

Trước khi đóng gói handoff, xuất bản vẽ sơ đồ qua `/wx-diagram` (engine draw.io, xem bảng quyết định trong skill đó):

1. `/wx-diagram block-diagram {{project}}` — assembly/block diagram cho fab bundle.
2. Lưu vào `1_Projects/{{project}}/Phase4-Detail/diagrams/`, liệt kê 2 file (.drawio + .drawio.png) vào mục Files của handoff.

Nếu draw.io CLI chưa cài → wx-diagram tự degrade (chỉ sinh .drawio XML) — vẫn đính kèm, KHÔNG chặn handoff.
```

- [ ] **Step 2: helix-quality-gate — thêm section trước `## Rules`**

Chèn:

```markdown
## Publication gate pack (wx-diagram — AUTO)

Sau khi có gate decision, xuất 1 trang gate pack: `/wx-diagram gate-pack {{project}}` — dashboard scores + traffic light + decision (PASS/CONDITIONAL/FAIL), style `wx-default`. Đính vào file gate review. Degrade gracefully nếu thiếu CLI.
```

- [ ] **Step 3: forge-fabrication — thêm vào cuối section `## HELIX → FORGE Handoff Integration`**

Chèn (trước heading kế tiếp `## Compound Learning Hooks`):

```markdown
**Publication diagram (wx-diagram — AUTO):** khi F0 chấp nhận handoff, xuất quy trình công nghệ dạng swimlane: `/wx-diagram swimlane {{product}} --source Handoff_to_Fabrication.md` — 6 lane F0-F5, đính vào bộ quy trình công nghệ (dùng được thẳng trong hồ sơ TCVN/BQP). Degrade gracefully nếu thiếu draw.io CLI.
```

- [ ] **Step 4: forge-proposal-khcn — thêm section trước `## Gotchas`**

Chèn:

```markdown
## Sơ đồ trong hồ sơ (wx-diagram — AUTO)

Hồ sơ KHCN cần sơ đồ trình được. Khi soạn phiếu đề xuất/thuyết minh, xuất qua `/wx-diagram`:
- `/wx-diagram function-structure {{project}}` — sơ đồ chức năng tổng thể.
- `/wx-diagram swimlane {{project}}` — quy trình thực hiện nhiệm vụ (theo giai đoạn).
Format PDF khi mẫu biểu yêu cầu. CẤM aiicons.py (CDN) với nội dung MẬT/HẠN-CHẾ — xem rule bảo mật trong wx-diagram.
```

- [ ] **Step 5: gate1 / gate2 / gate3 — append cuối mỗi file**

Chèn (cuối file, sau dòng FLAG cuối):

```markdown

After the gate decision is recorded, render a one-page publication gate pack via `/wx-diagram gate-pack {{project}}` (draw.io engine; degrades to .drawio XML if CLI missing) and attach it next to the gate review file.
```

- [ ] **Step 6: Verify anchors đã chèn đúng**

Run: `grep -rn "wx-diagram" skills/helix/helix-p4-handoff skills/helix/helix-quality-gate skills/forge/forge-fabrication skills/forge/forge-proposal-khcn skills/system/gate1 skills/system/gate2 skills/system/gate3 | wc -l`
Expected: ≥ 7 (mỗi skill ít nhất 1 match).

- [ ] **Step 7: Chạy lại eval các skill có eval sẵn**

Run: `bash evals/run-eval.sh forge-fabrication && bash evals/run-eval.sh helix-quality-gate`
Expected: PASS như trước (hook mới không phá assertion cũ).

- [ ] **Step 8: Commit**

```bash
git add skills/helix/helix-p4-handoff/SKILL.md skills/helix/helix-quality-gate/SKILL.md skills/forge/forge-fabrication/SKILL.md skills/forge/forge-proposal-khcn/SKILL.md skills/system/gate1/SKILL.md skills/system/gate2/SKILL.md skills/system/gate3/SKILL.md
git commit -m "[DESIGN] Auto-hook wx-diagram tai 7 diem gate/handoff (P4, QG, fab, KHCN, G1-G3)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 5: Suggest-only hooks — 6 skill

**Files:**
- Modify: `skills/helix/helix-p1-compile/SKILL.md` (cuối section `## Output`)
- Modify: `skills/helix/helix-p2-select/SKILL.md` (cuối section `## Output`)
- Modify: `skills/helix/helix-p3-integrate/SKILL.md` (cuối section `## Output`)
- Modify: `skills/bridge/bridge-dashboard/SKILL.md` (cuối section `## Workflow`)
- Modify: `skills/bridge/bridge-knowledge-base/SKILL.md` (cuối section `## Integration Points`)
- Modify: `skills/bridge/bridge-flywheel/SKILL.md` (cuối section `## Integration Points`)

**Interfaces:**
- Consumes: `/wx-diagram` từ Task 2.
- Produces: 6 skill in 1 dòng gợi ý, KHÔNG auto-render.

- [ ] **Step 1: Chèn cùng 1 dòng vào cả 6 file** (cuối section nêu trên của từng file, trước heading kế tiếp):

```markdown

> 💡 Cần bản xuất bản (PNG/PDF cho báo cáo/trình duyệt)? Gợi ý: `/wx-diagram <type> {{project}}` — KHÔNG tự chạy, chỉ gợi ý.
```

Với 3 file HELIX dùng `{{project}}`; với 3 file BRIDGE thay `{{project}}` bằng tên báo cáo/dashboard đang làm.

- [ ] **Step 2: Verify**

Run: `grep -l "wx-diagram" skills/helix/helix-p1-compile/SKILL.md skills/helix/helix-p2-select/SKILL.md skills/helix/helix-p3-integrate/SKILL.md skills/bridge/bridge-dashboard/SKILL.md skills/bridge/bridge-knowledge-base/SKILL.md skills/bridge/bridge-flywheel/SKILL.md | wc -l`
Expected: `6`.

- [ ] **Step 3: Commit**

```bash
git add skills/helix/helix-p1-compile/SKILL.md skills/helix/helix-p2-select/SKILL.md skills/helix/helix-p3-integrate/SKILL.md skills/bridge/bridge-dashboard/SKILL.md skills/bridge/bridge-knowledge-base/SKILL.md skills/bridge/bridge-flywheel/SKILL.md
git commit -m "[DESIGN] Suggest-only wx-diagram o 6 block compile/BRIDGE

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 6: Housekeeping — CHANGELOG, VERSION, CLAUDE.md

**Files:**
- Modify: `CHANGELOG.md` (entry mới trên cùng)
- Modify: `VERSION` (bump minor)
- Modify: `CLAUDE.md` (dòng `design/ (8)` → `(9)` + thêm ghi chú wx-diagram)

**Interfaces:**
- Consumes: kết quả các task trước.
- Produces: repo nhất quán, sẵn sàng PR.

- [ ] **Step 1: Đọc VERSION hiện tại và bump minor**

Run: `cat VERSION` → ví dụ `1.2.0` → ghi `1.3.0`. (Ghi chú: memory có "bump VERSION chờ Assay" — nếu VERSION đã được nhánh khác bump trong lúc đó, chỉ bump 1 nấc minor từ giá trị hiện tại, ghi cả 2 thay đổi vào CHANGELOG.)

- [ ] **Step 2: CHANGELOG entry**

Thêm trên cùng (dưới header), khớp format entry sẵn có trong file:

```markdown
## [1.3.0] - 2026-07-11
### Added
- `design/wx-diagram` — tầng xuất bản sơ đồ draw.io (wrapper cho drawio-skill engine qua junction; PNG/SVG/PDF cho gate review, BQP docs, fab handoff, KHCN). Eval static `evals/wx-diagram.json` 10/10.
- Auto-hook wx-diagram tại 7 điểm gate/handoff: helix-p4-handoff, helix-quality-gate, forge-fabrication, forge-proposal-khcn, gate1-3.
- Suggest-only hook tại 6 block: helix-p1-compile, p2-select, p3-integrate, bridge-dashboard, bridge-knowledge-base, bridge-flywheel.
### Notes
- Engine KHÔNG vendor — junction `~/.claude/skills/drawio-skill` → `D:\GitHub\drawio-skill\skills\drawio-skill`; cập nhật bằng git pull ở repo ngoài.
- Prerequisite: draw.io desktop CLI ≥ 30 (`winget install --id JGraph.Draw -e`).
```

- [ ] **Step 3: CLAUDE.md — cập nhật count domain design**

Sửa dòng trong cây structure: `│   ├── design/       (8)  — Specialized tools only (odi, opt, wp, verify, reverse-engineering, reverse-mc, sdmodel, helm-aluminum-boat)` → `(9)` và thêm `wx-diagram` vào danh sách kèm chú thích ngắn `(+ wx-diagram: tầng xuất bản sơ đồ draw.io — engine junction, không vendor)`.

- [ ] **Step 4: Verify tổng**

Run: `bash setup.sh --status && bash evals/run-eval.sh wx-diagram`
Expected: status đếm design = 9; eval PASS.

- [ ] **Step 5: Commit + PR**

```bash
git add CHANGELOG.md VERSION CLAUDE.md
git commit -m "[DESIGN] Bump v1.3.0 — wx-diagram draw.io publication layer

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
git push -u origin feature/design-drawio-integration
gh pr create --base feature/evals-static-mode --title "[DESIGN] wx-diagram — draw.io publication layer cho BRIDGE-FORGE-HELIX" --body "$(cat <<'EOF'
## Summary
- Tầng xuất bản sơ đồ 2 (draw.io) bổ trợ helix-draw (Excalidraw) — spec docs/superpowers/specs/2026-07-11-drawio-integration-design.md
- Skill mới skills/design/wx-diagram + eval static 10/10
- 7 auto-hook (gate/handoff) + 6 suggest-only hook
- Engine junction, không vendor; prerequisite draw.io CLI ≥ 30

## Test plan
- [x] bash evals/run-eval.sh wx-diagram → PASS
- [x] Smoke render swimlane F0-F5 → .drawio + .drawio.png mở được
- [x] bash setup.sh --verify sạch

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

Expected: PR tạo thành công. (Base = `feature/evals-static-mode` theo cấu hình main-branch hiện tại của repo; nếu CEO muốn base khác, hỏi trước khi tạo.)
