# ip-invent

Plugin Claude tự chứa (Markdown/JSON thuần — không Python, không hook, không MCP) dựng hồ sơ sở
hữu trí tuệ **TẤN CÔNG**: từ ý tưởng đến bộ đơn giao đại diện sở hữu công nghiệp. Đây là **cặp đối
xứng của QP-02-06 FTO** — FTO tránh claim của người khác, `ip-invent` dựng claim của chính mình.

## Plugin làm gì

| Skill | Block | Vai trò | CEO checkpoint |
|---|---|---|---|
| `ip-invent` | orchestrator | Thin-commander, chạy **một block một lượt**, ledger `_pipeline_state.md` là kênh duy nhất giữa các block — không truyền ngầm qua hội thoại. | Duyệt chuyển block kế tiếp; đọc lại ledger trước mỗi lần gọi. |
| `ip-criteria` | B0 — CHẶN | Dựng thước đo "cái gì được tính" cho chức danh (QĐ 431/QĐ-BQP ↔ QĐ 12/2025/QĐ-TTg) **trước khi** rà bất kỳ ứng viên nào. | Chốt đích chức danh (431 / 12-2025 / cả hai) và căn cứ pháp lý đang dùng. |
| `ip-harvest` | B1 | Thu hoạch ứng viên **trước**, sinh ý tưởng mới **sau**; mỗi ứng viên phải mang đủ 4 trường bắt buộc. | Duyệt danh sách ứng viên trước khi sang B2. |
| `ip-screen` | B2 | Rà theo hai trục, cấm bình quân điểm; routing 4 đường — gồm cả đường sáng chế **MẬT**. | Duyệt routing của từng ứng viên, đặc biệt đường MẬT. |
| `ip-claim` | B3 | Dựng 2–3 khung claim; đếm điểm độc lập đối chiếu trần thẩm định nhanh. | Chốt khung claim và xác nhận không vượt trần thẩm định nhanh. |
| `ip-dossier` | B4 | Dựng bộ đơn theo Phụ lục I hiện hành + handoff cho đại diện sở hữu công nghiệp. | Duyệt bộ đơn trước khi giao đại diện — advisory-only, không thay đại diện. |

## Ba cổng chặn

Ba cổng **độc lập với nhau, phải qua cả ba** — qua cổng này không miễn cổng kia:

- **Cổng bộc lộ** (Điều 60 Luật SHTT) — chưa khóa priority date thì cấm công khai bất kỳ nội dung
  ứng viên nào (bài đăng, demo, showcase, bản thảo gửi ngoài).
- **Cổng phân loại bí mật nhà nước** (`skills/ip-shared/references/co-mat-gate.md`) — chỉ chạy khi
  profile workspace đang bật khai `surface: cloud`. Chưa có văn bản xác định ⇒ coi như CHƯA RÕ ⇒
  DỪNG, không suy diễn hộ.
- **Cổng advisory-only** — plugin không thay đại diện sở hữu công nghiệp, không thay cơ quan xét
  chức danh, không thay cơ quan xác định bí mật nhà nước. Mọi kết luận là đề xuất, CEO quyết.

## Luật nền đổi rất nhanh

Chuỗi nghị định hướng dẫn: NĐ 65/2023 → 15/2026 → 33/2026 → 100/2026. Luật gốc: Luật SHTT
50/2005, sửa đổi bởi 36/2009, 42/2019, 07/2022, 93/2025, 131/2025.

Vì chuỗi này đổi liên tục, **mọi đầu ra có quy cách/biểu mẫu/thời hạn/phí phải in dòng**:

```
Chuỗi sửa đổi kiểm tại: <ngày> — nguồn: <văn bản mới nhất>
```

Không có dòng này = đầu ra không đáng tin về mặt thủ tục, bất kể nội dung kỹ thuật đúng hay sai.

## Tầng trỏ workspace

Bảy trường, đọc từ `active-workspace.md` → tên file profile → nội dung profile đó:

| Trường | Ý nghĩa |
|---|---|
| `surface` | `local` hoặc `cloud` — quyết định cổng phân loại có kích hoạt hay không. |
| `root` | Gốc làm việc của môi trường đang chạy. |
| `output_pattern` | Nơi ghi ledger + đầu ra từng block. |
| `scan_sources` | Nguồn B1 quét để thu hoạch ứng viên, hoặc `none`. |
| `triz_refs` | Đường dẫn tham chiếu TRIZ, hoặc `none`. |
| `patent_search` | Công cụ tra cứu patent, hoặc `none`. |
| `nlm_notebook` | Notebook NotebookLM tra luật công khai, hoặc `none`. |

Ba profile có sẵn trong `skills/ip-shared/references/`: `workspace-knstack.md` (Claude Code + vault
Workshop X, `surface: local`), `workspace-cowork.md` (Claude Cowork, `surface: cloud`),
`workspace-template.md` (khuôn rỗng cho môi trường thứ ba — **không bao giờ được bật** trực tiếp,
chỉ để chép ra và điền).

Đổi môi trường = **sửa đúng một dòng** trong `active-workspace.md` (tên file profile trong khối
mã) — không đụng `SKILL.md` nào.

Trường nào bằng `none` → skill phải chạy **chế độ giảm** và **in dòng khai báo** (ví dụ "B1 chạy
KHÔNG có TRIZ"). Cấm im lặng bỏ qua rồi vẫn in báo cáo trông đầy đủ.

## Khởi tạo ledger

Plugin **không tự dựng sổ**. Trước lần chạy đầu tiên của mỗi dự án, chép
`templates/_pipeline_state.md` vào `<output_pattern>` (giá trị lấy từ profile workspace đang bật).

Ledger là **kênh duy nhất** giữa các block — trạng thái, kết quả, cờ ràng buộc đều đọc/ghi qua
ledger, không truyền ngầm qua hội thoại hay giả định block trước "chắc đã làm".

## Import vào Cowork

> ⚠️ **CHƯA KIỂM CHỨNG.** Hai cách dưới đây chép theo khuôn plugin `fluency-4d`; chưa lần nào
> chạy thật trong Cowork. Chạy được rồi thì sửa mục này cho đúng, đừng để nguyên câu hứa.

Copy nguyên thư mục `plugins/ip-invent/` (gồm `.claude-plugin/plugin.json` + `skills/` +
`templates/`) vào thư mục plugin của Cowork, hoặc trỏ marketplace của Cowork tới repo `KN-Stack`.
Sau khi import, xác nhận **sáu skill xuất hiện**: `ip-invent`, `ip-criteria`, `ip-harvest`,
`ip-screen`, `ip-claim`, `ip-dossier`.

Copy **nguyên cây**, đừng copy lẻ từng thư mục skill: `skills/ip-shared/references/` phải nằm cạnh
sáu thư mục skill thì `../ip-shared/references/…` trong `SKILL.md` mới resolve được.

Sau khi import, **đổi `active-workspace.md` sang `workspace-cowork.md`** — nếu quên, plugin chạy
với profile `local` và sẽ đi tìm vault không tồn tại.

## Dùng trong Claude Code

Bảy thư mục được junction vào `~/.claude/commands/`. **Junction `ip-shared` là BẮT BUỘC, không
phải tuỳ chọn.** Khi chạy qua junction, mỗi skill nằm trực tiếp dưới `~/.claude/commands/`, nên
`..` không còn là `skills/` của plugin mà là chính `~/.claude/commands/`. Thiếu junction thứ bảy
thì `../ip-shared/references/` không tồn tại — nhưng chốt Bước 0′ trong cả sáu `SKILL.md` sẽ
**DỪNG** thay vì chạy tiếp âm thầm.

    bash setup.sh --install    # tạo junction còn thiếu
    bash setup.sh --verify     # kỳ vọng: cả 7 thư mục của ip-invent (6 skill + ip-shared) verified

⚠️ `bash setup.sh --unlink` gỡ **cả bảy** junction cùng các skill khác. Sau `--unlink` chạy lại
`--install`; đừng dựng tay từng cái rồi quên `ip-shared`.

## Bảo trì

Sau mỗi lần sửa bất kỳ file nào trong `skills/ip-shared/references/` hoặc bất kỳ `SKILL.md` nào:

    python -m pytest scripts/test_ip_invent.py -v
    bash evals/run-eval.sh ip-invent
    bash evals/run-eval.sh ip-screen

Bộ test nằm ngoài plugin (ở `scripts/`) vì plugin phải thuần Markdown + JSON. Nó kiểm, gồm: bảy
trường workspace đủ và đúng thứ tự · mọi `../ip-shared/references/*.md` được trích tồn tại thật ·
cả sáu `SKILL.md` mang chốt Bước 0′ · không `SKILL.md` nào còn đường dẫn neo cứng · **SHA-256 đóng
băng toàn văn `co-mat-gate.md`** (`GATE_DOC_SHA256` trong `ip_invent_lint.py` — đổi một ký tự
trong file cũng làm lint đỏ) · **`lint_blocks_identical`** — khối Bước 0′ của cả sáu `SKILL.md`
phải byte-identical với nhau và với `STEP0_BLOCK_CANON`, bắt được bản sao lệch dù chỉ một ký tự.
