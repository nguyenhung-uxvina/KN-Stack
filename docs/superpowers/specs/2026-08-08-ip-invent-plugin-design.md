# Đóng gói pipeline `/ip-invent` thành plugin dùng được trong Cowork

Ngày: 2026-08-08 · Nhánh: `feature/ip-patent-pipeline` · Trạng thái: CEO đã duyệt thiết kế

## Vấn đề

Sáu skill IP (`ip-invent` orchestrator + 5 block `ip-criteria`/`ip-harvest`/`ip-screen`/`ip-claim`/`ip-dossier`,
tổng 1120 dòng Markdown) hiện chỉ chạy được trong Claude Code trên máy có KN-Stack. CEO muốn dùng
pipeline này trong **Cowork** (app Claude Cowork của Anthropic, chạy trên hạ tầng cloud).

Bê nguyên sang Cowork không được, vì ba lý do độc lập nhau:

1. **Xung đột cổng.** Rào cứng #2 của `ip-invent` cấm *"đưa nội dung giải pháp chưa bộc lộ vào
   NotebookLM, dịch vụ cloud, hay bất kỳ prompt gửi ra ngoài"*, và mặc định phân loại mọi đầu ra là
   MẬT. Chạy trong Cowork là tự vi phạm cổng do chính pipeline dựng.
2. **Đường dẫn vault hardcode.** Đầu ra ghi vào `1_Projects/<project>/IP/`; `ip-harvest` nhánh 1a
   quét `1_Projects/*/`, `2_Areas/HELIX*/`, `_meta/decisions.md`. Cowork không có cây thư mục đó.
3. **Ba tham chiếu dangling khi rời KN-Stack** — đã hỏng sẵn, chưa ai bắt được:
   - `ip-harvest` dòng 59 → `skills/helix/helix-concept-generate/references/triz-40-principles.md`
     và `triz-sufield-76solutions.md` (13 KB, nằm ngoài phạm vi plugin)
   - `ip-harvest` dòng 56 → `/research --patents` (skill khác của KN-Stack)
   - `ip-invent` dòng 181 → `3_Resources/Deep-Content-Analyzer-Outputs/RESEARCH_ip-sang-che-gphi-chuc-danh_2026-08-06.md`

## Tiền lệ trong repo

Repo có sẵn hai khuôn plugin khác nhau:

| Khuôn | Ai dùng | Nguồn chuẩn ở |
|---|---|---|
| Dời hẳn | `fluency-4d` (nhánh `feature/fluency-4d-plugin`) | `plugins/<tên>/skills/` |
| Sinh bản sao | `leo-ai` | `skills/` chuẩn, `build.sh` chép sang `plugins/` |

Thiết kế này theo khuôn **dời hẳn** của `fluency-4d`, kể cả các bài học đã trả giá ở đó (namespace
phẳng, junction thư mục shared là bắt buộc, chốt "đọc không được thì DỪNG").

## Ba quyết định nền — CEO đã chốt

| # | Câu hỏi | Chốt |
|---|---|---|
| 1 | Xử cổng MẬT/cloud thế nào? | Đóng gói **cả 5 block**, thêm **cổng phân loại** đầu phiên. Ranh giới nằm ở *loại ứng viên*, không phải *loại block*. |
| 2 | Plugin biết vault ở đâu bằng cách nào? | **Tầng trỏ workspace** — một file dùng chung khai gốc làm việc. Đổi môi trường = sửa một dòng. |
| 3 | Nguồn chuẩn nằm ở đâu? | **Dời hẳn** `skills/ip/*` → `plugins/ip-invent/skills/`. Một nguồn duy nhất, không trôi bản. |

## Kiến trúc

```
plugins/ip-invent/
├── .claude-plugin/plugin.json
├── README.md
├── skills/
│   ├── ip-invent/SKILL.md      ← orchestrator (git mv từ skills/ip/)
│   ├── ip-criteria/SKILL.md    ← B0
│   ├── ip-harvest/SKILL.md     ← B1
│   ├── ip-screen/SKILL.md      ← B2
│   ├── ip-claim/SKILL.md       ← B3
│   ├── ip-dossier/SKILL.md     ← B4
│   └── ip-shared/references/   ← tầng dùng chung (mới)
│       ├── active-workspace.md
│       ├── workspace-knstack.md
│       ├── workspace-cowork.md
│       ├── workspace-template.md
│       └── co-mat-gate.md
└── templates/_pipeline_state.md
```

Plugin **thuần Markdown + JSON**. Không Python, không hook, không MCP — lint và test nằm ngoài plugin
ở `scripts/`, giống `fluency-4d`.

Tên thư mục shared là **`ip-shared`**, không phải `_shared`/`common`/`refs`: `~/.claude/commands/` là
namespace **phẳng** dùng chung mọi plugin, tên chung chung sẽ đụng nhau giữa các plugin.

## Thành phần 1 — Tầng trỏ workspace

`ip-shared/references/active-workspace.md` chứa **một khối mã nêu tên file profile đang bật**. Sáu
`SKILL.md` đọc file này rồi mới mở profile; **không `SKILL.md` nào được gọi tên file workspace trực tiếp**.

Mỗi file `workspace-*.md` khai bảy trường:

| Trường | Ý nghĩa | Giá trị ở `workspace-knstack.md` | Giá trị ở `workspace-cowork.md` |
|---|---|---|---|
| `surface` | bề mặt chạy | `local` | `cloud` |
| `root` | gốc làm việc | `D:\Workshop_X\` | thư mục workspace của Cowork |
| `output_pattern` | nơi ghi đầu ra | `<root>/1_Projects/<project>/IP/` | `<root>/IP/<project>/` |
| `scan_sources` | nguồn B1-1a quét | `1_Projects/*/`, `2_Areas/HELIX*/`, `_meta/decisions.md`, RE report, FTO Record | `none` |
| `triz_refs` | đường dẫn TRIZ cho B1-1b | `skills/helix/helix-concept-generate/references/` | `none` |
| `patent_search` | công cụ tra patent | `/research --patents` | `none` |
| `nlm_notebook` | notebook luật công khai | `ip-vn` | `none` |

`workspace-template.md` là khuôn rỗng cho môi trường thứ ba, không bao giờ được bật.

**Trỏ chứ không chép.** TRIZ 13 KB không nhân đôi vào plugin.

**Chế độ giảm phải khai rõ.** Khi một trường = `none`, block liên quan vẫn chạy nhưng **bắt buộc in
dòng khai báo** — ví dụ `1b chạy KHÔNG có TRIZ` hoặc `B1-1a KHÔNG quét được nguồn nào, ứng viên phải
CEO tự nạp`. Cấm im lặng bỏ qua rồi vẫn in ra báo cáo trông đầy đủ. Đây là đúng mode lỗi đã bắt được
ở `fluency-4d` (thiếu junction shared → skill chạy không rubric mà vẫn in báo cáo đủ).

Khi `scan_sources: none`, `ip-harvest` **không được tự nhảy sang 1b**: 1b chỉ chạy khi 1a *chạy được
và không đủ ứng viên sạch*. Không quét được ≠ quét xong không thấy gì. Trường hợp `none` thì B1 dừng,
báo CEO, chờ CEO nạp ứng viên tay.

## Thành phần 2 — Cổng phân loại (`co-mat-gate.md`)

Điểm mới **duy nhất về hành vi** của plugin so với 6 skill hiện tại.

- `surface: local` → hành vi y hệt hiện nay, cổng không kích hoạt.
- `surface: cloud` → mọi block chạy **Bước 0′** trước khi đụng nội dung ứng viên:

| Phân loại ứng viên | Xử |
|---|---|
| Thuộc / nghi thuộc **bí mật nhà nước – bí mật quân sự** | **DỪNG.** Không xử nội dung. Chỉ CEO về Claude Code local. |
| **Chưa rõ** | Coi như **thuộc** → dừng. Bám nguyên tắc `ip-dossier` đã có: *"Chưa có văn bản xác định bí mật nhà nước ⇒ coi như CHƯA RÕ"*. |
| **Không thuộc** — dân dụng, hoặc lưỡng dụng đã tách phần MẬT, hoặc đã khóa priority date | Chạy. |

Trạng thái cổng ghi vào ledger `_pipeline_state.md`; **mỗi block in lại ở đầu báo cáo** — để CEO không
bao giờ đọc một đầu ra mà không biết nó chạy trên bề mặt nào.

### Viết lại rào cứng #2 của `ip-invent`

Rào cứng #2 hiện gộp hai thứ khác hẳn nhau vào một câu cấm. Tách ra:

- **Bí mật nhà nước** — cấm tuyệt đối ra bất kỳ dịch vụ ngoài nào, không ngoại lệ. Đây là cổng thật.
- **Chưa bộc lộ nhưng không MẬT** — Điều 60.2 Luật SHTT: bộc lộ cho *"một số người có hạn được biết
  và có nghĩa vụ giữ bí mật"* **không** làm mất tính mới. Dịch vụ có nghĩa vụ bảo mật theo hợp đồng
  rơi vào diện đó.

`co-mat-gate.md` phải **ghi thẳng** rằng đây là **quyết định của CEO, không phải kết luận pháp lý của
AI** — cùng tinh thần cổng advisory-only #3 đã có sẵn trong `ip-invent`.

## Thành phần 3 — Chốt chống lỗi im lặng

1. **Chốt DỪNG trong mỗi `SKILL.md`.** Mở đầu mỗi skill: đọc `../ip-shared/references/active-workspace.md`;
   đọc không được thì **DỪNG**, không đoán, không chạy tiếp bằng giá trị mặc định.
2. **Junction thứ 7 (`ip-shared`) là bắt buộc, không tuỳ chọn.** Khi chạy qua junction, mỗi skill nằm
   trực tiếp dưới `~/.claude/commands/`, nên `..` là chính `~/.claude/commands/` chứ không phải
   `skills/` của plugin. Có junction thứ 7 thì cùng một đường dẫn tương đối `../ip-shared/references/…`
   resolve đúng ở **cả hai** kiểu triển khai (junction rời trong Claude Code, và cây plugin nguyên vẹn
   trong Cowork) — nên không `SKILL.md` nào phải sửa theo môi trường.
3. **Lint + test** (`scripts/ip_invent_lint.py`, `scripts/test_ip_invent.py`), chạy bằng
   `python -m pytest scripts/test_ip_invent.py -v`:
   - mọi `../ip-shared/references/<file>.md` được trích trong 6 `SKILL.md` phải tồn tại thật
   - không còn đường dẫn tuyệt đối (`D:\`, `E:\`) và không còn đường dẫn vault **neo cứng ở gốc**
     (`1_Projects/…`, `2_Areas/…`, `3_Resources/…`, `5_Galaxy/…`) trong `SKILL.md` nào — mọi đường
     dẫn loại này phải đi qua tầng trỏ, viết dạng `<output_pattern>` hoặc `<root>/…`.
     Ngoại lệ duy nhất được phép giữ nguyên: `_meta/decisions.md` và `_meta/learnings.md`, vì chúng
     là đường dẫn **tương đối trong dự án**, resolve từ `output_pattern` chứ không từ gốc vault.
     Lint mang đúng allowlist hai mục này, không nới thêm.
   - cả 6 `SKILL.md` đều mang chốt cổng phân loại và chốt DỪNG
   - `workspace-*.md` khai đủ 7 trường, đúng tên, đúng thứ tự
4. **Eval** `evals/ip-invent.json` lên **v1.2**: giữ nguyên 15 assertion hiện có (14 bắt buộc), thêm
   assertion cho cổng phân loại và tầng trỏ, và **bump `total_required` + `passing_score`** theo số
   assertion mới — quên bump là eval tự nới chuẩn mà không ai thấy. `evals/ip-screen.json` giữ nguyên.

Lint không phải vẽ vời: lỗi "trỏ tới file tham chiếu không tồn tại" **đã có trong code hiện tại**
(dòng TRIZ ở `ip-harvest`), chưa cơ chế nào bắt được.

## Cố ý KHÔNG làm

- **Không gỡ chữ "CEO"** khỏi `SKILL.md`. Plugin này dùng cho chính CEO, không phát cho tổ chức khác.
  (Khác `fluency-4d`, nơi việc đó là món nợ có thật.)
- **Không đổi logic 5 block**, không đụng nội dung pháp lý, không sửa bảng đối chiếu QĐ 431 ↔ QĐ 12/2025.
- **Không viết `build.sh`.** Dời hẳn thì chỉ có một nguồn, không có gì để sinh.
- **Không thêm Python/hook/MCP vào plugin.**

## Di chuyển và hạ tầng

1. `git mv skills/ip/<6 thư mục> plugins/ip-invent/skills/` — `skills/ip/` đang staged, chưa commit,
   nên dời bây giờ không phải viết lại lịch sử.
2. `git checkout feature/fluency-4d-plugin -- setup.sh` — đã đo: diff giữa hai nhánh là **119 dòng
   thêm thuần, 0 dòng xoá**, nên đây là phép cộng sạch, không conflict. Bản đó biết đi vào
   `plugins/*/skills/*/` và junction cả thư mục shared.
3. `bash setup.sh --install` → tạo 7 junction; `bash setup.sh --verify` → báo đủ plugin skill dirs.
4. `CLAUDE.md`: gỡ mục `ip/ (6)` khỏi cây `skills/`, chuyển mô tả sang phần `plugins/`.
5. Bump `VERSION` + thêm mục `CHANGELOG.md`.

⚠️ `bash setup.sh --unlink` gỡ **cả 7** junction cùng các skill khác. Sau `--unlink` phải chạy lại
`--install`, đừng dựng tay từng cái rồi quên `ip-shared`.

## Kiểm chứng

Theo thứ tự, mỗi bước phải xanh trước khi sang bước sau:

1. `bash setup.sh --verify` — 7 junction resolve đúng
2. `python -m pytest scripts/test_ip_invent.py -v` — lint tham chiếu + đường dẫn + chốt
3. `bash evals/run-eval.sh ip-invent` và `bash evals/run-eval.sh ip-screen` — eval tĩnh
4. Chạy thật `/ip-criteria` qua junction. Chọn B0 vì nó thuần **luật công khai**, không đụng nội dung
   ứng viên nào — an toàn để thử ngay cả khi cổng phân loại chưa được kiểm chứng thực địa.

## Rủi ro và chỗ chưa kiểm chứng

| Rủi ro | Xử |
|---|---|
| **Cơ chế import plugin của Cowork chưa được kiểm chứng.** README `fluency-4d` nêu hai cách (copy thư mục / trỏ marketplace về repo `KN-Stack`) nhưng không có bằng chứng đã chạy thật lần nào. | README của plugin IP viết theo đúng khuôn đó và **ghi rõ là chưa kiểm chứng**. CEO chạy import một lần rồi báo lại để sửa README cho đúng. Không hứa trước điều chưa chạy. |
| **Cổng phân loại có thể bị CEO bấm qua theo thói quen** — cổng nào cũng có nguy cơ này. | Cổng bắt khai phân loại **kèm căn cứ** (văn bản/quyết định nào), không nhận câu trả lời trống. Mặc định "chưa rõ" = dừng, nên bấm bừa không mở được cổng. |
| **`feature/fluency-4d-plugin` chưa merge** — `setup.sh` lấy từ nhánh chưa merge có thể lệch nếu nhánh đó tiếp tục đổi. | Lấy một lần tại thời điểm triển khai, ghi commit hash nguồn vào `CHANGELOG.md`. Merge hai nhánh là việc riêng, ngoài phạm vi spec này. |
