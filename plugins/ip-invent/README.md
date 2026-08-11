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

## Các cổng chặn

**Đừng đếm "ba".** Số cổng khác nhau tuỳ chỗ đứng, nên ở đây liệt kê **đủ các cổng chặn thật** —
cổng chặn = không qua thì pipeline **dừng**, không phải khuyến nghị. Các cổng **độc lập với nhau**:
qua cổng này không miễn cổng kia.

| Cổng chặn | Ở đâu | Chặn cái gì |
|---|---|---|
| **Cổng bộc lộ** (Điều 60 Luật SHTT) | rào cứng #1 của `ip-invent` | Chưa khóa priority date thì cấm công khai bất kỳ nội dung ứng viên nào (bài đăng, demo, showcase, bản thảo gửi ngoài). |
| **Cổng phân loại bí mật nhà nước** | `skills/ip-shared/references/co-mat-gate.md` | Chỉ kích hoạt khi profile workspace đang bật khai `surface: cloud`. Chưa có văn bản xác định ⇒ coi như CHƯA RÕ ⇒ DỪNG, không suy diễn hộ. |
| **Cổng Điều 10a — tác giả/AI** | `ip-screen` mục I.5 | Không ghi được **đóng góp đáng kể của con người** ⇒ CHẶN, trả ứng viên về B1. Bỏ qua = rủi ro có bằng mà không dùng được cho chức danh. |
| **Cổng Điều 14 — nộp ra nước ngoài** | `ip-dossier` | Sáng chế thuộc danh mục bí mật nhà nước QP-AN chỉ được nộp ở nước ngoài **khi BQP/BCA cho phép** — xin phép TRƯỚC, không nộp rồi hợp thức hoá sau. |

> **Vì sao `co-mat-gate.md` viết "Ba cổng độc lập, phải qua cả ba"?** Câu đó đếm theo **nghĩa hẹp của
> riêng nó** — ba cổng mà *cổng phân loại* phải sống chung: **bộc lộ · phân loại · Điều 14**. Nó
> không đếm cổng Điều 10a (thuộc B2, ngoài phạm vi tài liệu ấy). Hai chỗ **không mâu thuẫn**, chỉ
> khác phạm vi đếm. Tương tự, `ip-invent/SKILL.md` gom **"BA RÀO CỨNG"** theo trục vận hành của
> orchestrator (bộc lộ · dữ liệu ra ngoài · advisory-only) — đó là cách chia việc, không phải danh
> sách cổng chặn.

**Advisory-only KHÔNG phải một cổng** — nó là **phạm vi trách nhiệm**, không có gì để "qua": plugin
không thay đại diện sở hữu công nghiệp, không thay cơ quan xét chức danh, không thay cơ quan xác
định bí mật nhà nước. Mọi kết luận là đề xuất, CEO quyết.

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

## Phụ thuộc ngoài plugin

Plugin tự chứa về **file**, nhưng **không** tự chứa về **tri thức**. Hai thứ được trích mà không nằm
trong cây plugin, không phải skill KN-Stack, và **không** phải một trường workspace:

| Phụ thuộc | Ai dùng | Không tiếp cận được thì sao |
|---|---|---|
| **QP-02-06 — Quy trình FTO** (quy trình nội bộ Workshop X) | `ip-screen` mượn khuôn phân loại prior art **§7.2** (4 lớp A/B/C/D) và **§8.4** (doctrine of equivalents, prosecution history estoppel); `ip-harvest` liệt **FTO Record** làm nguồn quét 1a | `ip-screen` chạy **chế độ giảm**: phân loại prior art bằng **khuôn rút gọn nêu ngay trong `SKILL.md`**, bỏ phần §8.4, và **bắt buộc in dòng khai báo** kèm hạ độ tin trục I. Trong Cowork QP-02-06 **không tồn tại** ⇒ chế độ giảm là mặc định. |
| **Nghiên cứu nền** `RESEARCH_ip-sang-che-gphi-chuc-danh_2026-08-06.md` đặt trong `<root>` | `ip-invent`, mục *NLM reference* | Skill **tìm thật** trong `<root>`; không thấy thì **in dòng khai báo** *"chạy KHÔNG có nghiên cứu nền"* rồi chạy tiếp — mọi dữ kiện pháp lý phải tra lại từ đầu. **Không** thêm trường workspace thứ tám cho nó. |

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

> **Bảy thư mục được chép nhưng chỉ sáu skill hiện ra — đúng như vậy, không thiếu gì.** Thư mục thứ
> bảy `ip-shared` **không có `SKILL.md`** (nó chỉ chứa `references/`), nên nó không phải một skill và
> **không bao giờ xuất hiện trong danh sách skill**. Cái đáng lo là ngược lại: `ip-shared` **không
> được chép**.

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

⚠️ `--install` **bỏ qua junction đã tồn tại — kể cả junction HỎNG.** Máy nâng cấp từ bố cục cũ
(6 junction `ip-*` trỏ vào `skills/ip/` trước khi plugin dời chỗ) sẽ thấy `--install` in *"skipped"*
và **tưởng là xong**, trong khi junction vẫn trỏ vào đường đã chết. **Quy tắc:** `--verify` báo
broken thì **xoá đúng junction đó rồi install lại** — chạy `--install` lần thứ hai không sửa được gì.

⚠️ `bash setup.sh --unlink` gỡ **cả bảy** junction cùng các skill khác. Sau `--unlink` chạy lại
`--install`; đừng dựng tay từng cái rồi quên `ip-shared`.

## Bảo trì

Sau mỗi lần sửa bất kỳ file nào trong `skills/ip-shared/references/` hoặc bất kỳ `SKILL.md` nào:

    python -m pytest scripts/test_ip_invent.py -v
    bash evals/run-eval.sh ip-invent
    bash evals/run-eval.sh ip-screen

> ⚠️ **Ba lệnh trên KHÔNG đi kèm bản copy.** `scripts/` và `evals/` nằm **ngoài** plugin, nên bản
> chép vào Cowork (hay bất kỳ nơi nào ngoài repo `KN-Stack`) **không có chúng** — gõ vào sẽ chỉ báo
> không tìm thấy file. Hệ quả thực tế: **sửa `SKILL.md` ngay trong bản copy là sửa không có lưới an
> toàn**. Sửa ở repo `KN-Stack`, chạy test, rồi chép lại.

Bộ test nằm ngoài plugin (ở `scripts/`) vì plugin phải thuần Markdown + JSON. Nó kiểm, gồm: bảy
trường workspace đủ và đúng thứ tự · mọi `../ip-shared/references/*.md` được trích tồn tại thật ·
cả sáu `SKILL.md` mang chốt Bước 0′ · không `SKILL.md` nào còn đường dẫn neo cứng · **SHA-256 đóng
băng toàn văn `co-mat-gate.md`** (`GATE_DOC_SHA256` trong `ip_invent_lint.py` — đổi một ký tự
trong file cũng làm lint đỏ) · **`lint_blocks_identical`** — khối Bước 0′ của cả sáu `SKILL.md`
phải byte-identical với nhau và với `STEP0_BLOCK_CANON`, bắt được bản sao lệch dù chỉ một ký tự.

### Hai giới hạn đã tuyên bố của bộ test

Hai lỗ này **đã biết và cố ý để mở** — chúng chỉ sống trong docstring Python và sổ tiến độ, mà người
dùng Cowork thì không bao giờ mở `scripts/`. Nêu ở đây để không ai tưởng lint là bất khả xâm phạm:

1. **Câu vô hiệu hoá đặt ở *phần tự do* của `SKILL.md` không bị bắt.** Lint đóng băng đúng khối
   Bước 0′ và neo vị trí của nó; phần còn lại của file là tự do. Một câu kiểu *"khối trên chỉ để
   tham khảo"* đặt ở **cuối file**, trong **`description:` của frontmatter**, hoặc **ngay sau khối
   dưới dạng blockquote** đều đi qua lint. (Văn xuôi đặt **trước** khối thì bị bắt — nó phá neo vị
   trí.) Người sửa `SKILL.md` phải tự canh chỗ này.
2. **Phần văn xuôi của `co-mat-gate.md` không có neo nào — nhưng cả file có hash.** SHA-256 bắt mọi
   sửa đổi trong file đó. Lỗ thật là ở chỗ khác: kẻ sửa **cả hai file** (tài liệu **và** hằng số
   `GATE_DOC_SHA256`/`GATE_DOC_CANON` trong `ip_invent_lint.py`) vẫn lừa được cổng — pytest chỉ đỏ
   trở lại nếu đột biến đụng **bảng 3 ngả** hoặc **khối kích hoạt**, vì các đột biến ấy có test
   riêng dựng lại từ file thật. Nghĩa là: **review commit đụng `ip_invent_lint.py` bằng mắt người**,
   đừng tin mỗi màu xanh của suite.
