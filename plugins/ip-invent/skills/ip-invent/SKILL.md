---
name: ip-invent
description: "Orchestrator sở hữu trí tuệ TẤN CÔNG — từ ý tưởng đến bộ đơn nộp Cục SHTT, chỉ huy 5 block-skill (ip-criteria → ip-harvest → ip-screen → ip-claim → ip-dossier). Ngược chiều với FTO (QP-02-06 tránh claim người khác); đây là dựng claim của mình. Chấm thước đo chức danh TRƯỚC khi rà ứng viên (QĐ 431/QĐ-BQP CSDL chuyên gia KH&CN BQP + QĐ 12/2025/QĐ-TTg chức danh Chuyên gia CNQP-AN), rà khả thi hai trục (khả năng bảo hộ × giá trị chức danh), routing sáng chế/GPHI/nộp kép/sáng chế MẬT, rồi lập hồ sơ. Có cổng bộc lộ (chưa khóa priority date thì cấm công khai), cổng kiểm soát an ninh khi nộp ra nước ngoài (Điều 14 NĐ 65 sđ NĐ 100/2026), và cổng tác giả-AI (Điều 10a). Advisory-only, không thay đại diện SHTT. Triggers on: 'ip-invent', 'nộp đơn sáng chế', 'đăng ký sáng chế', 'giải pháp hữu ích', 'GPHI', 'lập hồ sơ sáng chế', 'patent filing', 'utility solution', 'văn bằng bảo hộ', 'chức danh chuyên gia CNQP', 'CSDL chuyên gia', 'sáng chế mật', 'thẩm định nhanh', 'khóa priority date', 'bộ đơn NOIP'."
---

# ip-invent — Orchestrator IP tấn công (ý tưởng → hồ sơ nộp đơn)

## ⛔ BƯỚC 0′ — đọc workspace TRƯỚC MỌI VIỆC KHÁC

Đọc `../ip-shared/references/active-workspace.md` → lấy tên file profile → đọc profile đó.
**Đọc không được thì DỪNG**, báo *"không đọc được tầng trỏ workspace"*, **không đoán, không chạy
tiếp bằng giá trị mặc định**. Một báo cáo trông đầy đủ mà chạy không có workspace là lỗi tệ hơn
không chạy gì.

Nếu profile khai `surface: cloud` → chạy cổng phân loại trong
`../ip-shared/references/co-mat-gate.md` **trước khi đụng nội dung ứng viên bất kỳ**.

In ở đầu mọi báo cáo:

```
Bề mặt: <surface> · Cổng phân loại: <trạng thái> · Căn cứ: <…>
```

Trường workspace nào bằng `none` → chạy **chế độ giảm** và **in dòng khai báo** (ví dụ
`1b chạy KHÔNG có TRIZ`). Cấm im lặng bỏ qua rồi vẫn in báo cáo trông đầy đủ.

> **Role:** Chỉ huy mỏng (thin commander). KHÔNG tự làm việc của block. Điều phối 5 block tuần tự,
> mỗi block một lượt, CEO checkpoint chặn từng block.
> **Vị trí:** cặp đối xứng của [[QP-02-06]] FTO. FTO = *tránh claim người khác* (gate chặn Design
> Freeze). `ip-invent` = *dựng claim của mình* (gate: khóa priority date trước khi vào P3).
> **Không thay thế:** đại diện sở hữu công nghiệp, cơ quan xét chức danh, cơ quan xác định bí mật nhà nước.

## ⛔ BA RÀO CỨNG — đọc trước khi chạy bất kỳ block

### 1. Cổng bộc lộ
Giải pháp **chưa khóa priority date** → **CẤM** đăng web, brochure, triển lãm, clip, hội thảo, mạng xã hội.
Bộc lộ = mất tính mới (novelty **tuyệt đối toàn cầu**, Điều 60 Luật SHTT). Mọi đầu ra của pipeline
mặc định phân loại **MẬT**, ghi vào `1_Projects/<proj>/IP/`, **không** đẩy ra tool ngoài.

### 2. Cổng dữ liệu ra ngoài
**KHÔNG** đưa nội dung giải pháp chưa bộc lộ vào NotebookLM, dịch vụ cloud, hay bất kỳ prompt gửi ra
ngoài. Nghiên cứu **luật công khai** thì được (notebook `ip-vn`); **nội dung sáng chế thì không**.
Tương tự: văn bản nội bộ BQP (vd QĐ 431/QĐ-BQP) đọc **local**, không upload.

### 3. Cổng advisory-only
Skill này soạn **bản nháp kỹ thuật** để giao đại diện SHTT. Nó **không**:
- thay tra cứu novelty chính thức (pre-search keyword ≠ FTO/tra cứu chính thức)
- kết luận thay cơ quan xét chức danh (tiêu chí phải đối chiếu nguyên văn)
- xác định thay cơ quan có thẩm quyền việc giải pháp có thuộc **danh mục bí mật nhà nước**

## ⚠️ LUẬT NỀN ĐỔI RẤT NHANH — bắt buộc xác minh chuỗi sửa đổi

Chuỗi đã biết tại **2026-08-06**:
- **Nghị định:** NĐ 65/2023/NĐ-CP → NĐ 15/2026 (14/01/2026) → NĐ 33/2026 (21/01/2026) → **NĐ 100/2026 (31/3/2026, hiệu lực 01/4/2026)**
- **Luật SHTT:** Luật 50/2005 sđ bởi 36/2009, 42/2019, 07/2022, **93/2025/QH15**, **131/2025/QH15**
- **NĐ 100/2026 đã bãi bỏ Điều 16–28, 30–32, 43–47, 108** của NĐ 65/2023 (đúng cụm quy cách bản mô tả
  + yêu cầu bảo hộ + thẩm định) và **thay toàn bộ Phụ lục I, Phụ lục II**; bãi bỏ Phụ lục III–VII.
- Hệ quả: nhiều trang hướng dẫn (kể cả ipvietnam.gov.vn) còn dẫn **neo cũ**.

> **Mọi block xuất quy cách/biểu mẫu/thời hạn/phí PHẢI in dòng:**
> `Chuỗi sửa đổi kiểm tại: <ngày> — nguồn: <văn bản mới nhất>`
> Không có dòng đó = đầu ra không dùng được. Trong một phiên dựng skill này, cùng một dữ kiện
> ("tờ khai mẫu nào") đã bị lật **ba lần**. Đừng tin ký ức, đừng tin trang tổng hợp.

## Pipeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      ip-invent (ORCHESTRATOR)                            │
│  Flags: --project <id> | --from <block> | --only <block>                 │
│         --ip-type sang-che|gphi|kep|mat   --target 431|12-2025|ca-hai    │
│                                                                          │
│  ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐                  │
│  │  B0  │──▶│  B1  │──▶│  B2  │──▶│  B3  │──▶│  B4  │                  │
│  │CRITE-│   │HAR-  │   │SCREEN│   │CLAIM │   │DOSS- │                  │
│  │RIA   │   │VEST  │   │      │   │      │   │IER   │                  │
│  └──┬───┘   └──┬───┘   └──┬───┘   └──┬───┘   └──┬───┘                  │
│     │✓CEO      │✓CEO      │✓CEO      │✓CEO      │✓CEO                  │
│  thước đo   ứng viên +  hai trục +  khung claim  bộ đơn +               │
│  6+2 đường  trạng thái  routing     + trần 10/2  chứng cứ              │
│  điều kiện  bộc lộ/ứng  mật/thường  + chi phí    áp dụng +              │
│  đăng ký    dụng/tác giả    │        điểm độc lập  handoff SHTT          │
│     │                       └─(LOẠI)→ hồ sơ đi thi / cửa 12 tháng       │
│     └─(đường ngắn hơn KHÔNG phải patent) → BÁO CEO, pipeline đổi vai     │
│        sang "bảo hộ sản phẩm" thay vì "đường găng chức danh"             │
└─────────────────────────────────────────────────────────────────────────┘
State: {{output_path}}/_pipeline_state.md   ← kênh DUY NHẤT giữa các block
```

## Sub-skills

| Block | Skill | Việc | CEO checkpoint |
|-------|-------|------|----------------|
| **B0** | `/ip-criteria` | Điều kiện đăng ký + bảng đối chiếu QĐ 431 ↔ QĐ 12/2025 + chấm **6 đường Điều 5 (431)** và **2 nhóm Điều 3.2 (12/2025)** theo chi phí × thời gian × độ chắc → **thước đo** cho B2 | Xác nhận bảng tiêu chí + **chọn đường** |
| **B1** | `/ip-harvest` | 1a thu hoạch vault (gồm sản phẩm **đã triển khai**); 1b sinh mới từ whitespace + TRIZ nếu 1a thiếu. Mỗi ứng viên bắt buộc có: trạng thái **bộc lộ** (kèm NGÀY) · trạng thái **ứng dụng** · **vai tác giả của CEO** · **xuất xứ đóng góp người/AI** | Chọn ứng viên đi tiếp |
| **B2** | `/ip-screen` | Hai trục (khả năng bảo hộ × giá trị chức danh) + routing **sáng chế / GPHI / nộp kép / MẬT** + disclosure audit tính **cửa 12 tháng Điều 60.3** + cổng **Điều 10a** tác giả-AI | Duyệt kết luận; quyết đổ tiền hay loại |
| **B3** | `/ip-claim` | 2–3 khung claim, bảng phân biệt prior art, **đếm điểm độc lập** vs trần thẩm định nhanh (≤10/≤2), chi phí theo điểm độc lập, kịch bản lùi claim | **Chọn khung claim** (Core) |
| **B4** | `/ip-dossier` | Bộ đơn theo **Phụ lục I hiện hành** + hồ sơ **chứng cứ áp dụng** (nếu đích 12/2025 nhánh trong LLVT) + **cổng Điều 14** nếu có ý định nộp nước ngoài + gói câu hỏi giao đại diện SHTT | Duyệt hồ sơ; ký giao đại diện |

## Cách dùng

```bash
# Toàn pipeline cho một dự án
/ip-invent --project VN-TLS-001 --target ca-hai

# Đã có Patent_Draft sẵn → bỏ B1, vào từ B2
/ip-invent --project VN-TLS-001 --from B2

# Chạy lẻ một block
/ip-criteria --target 431
/ip-screen --project VN-FWTP-001

# Thu hoạch toàn danh mục (không gắn 1 dự án)
/ip-harvest --portfolio
```

## Orchestrator workflow

### Step 1 — Parse + route
```
PROJECT   : --project <id>  (hoặc --portfolio cho B1 toàn danh mục)
TARGET    : --target 431 | 12-2025 | ca-hai   (mặc định ca-hai)
IP-TYPE   : --ip-type sang-che|gphi|kep|mat   (nếu CEO đã có ý định; nếu không → B2 quyết)
FLAGS     : --from <block> | --only <block>
OUTPUT    : 1_Projects/<project>/IP/   (mặc định; phân loại MẬT)
```

### Step 2 — Đọc ledger, xác định block kế
Đọc `{{output_path}}/_pipeline_state.md`. Nếu chưa có → tạo, bắt đầu B0.
**B0 là bắt buộc và không được bỏ qua** — kể cả khi `--from B2`, phải kiểm ledger đã có kết quả B0
đã được CEO xác nhận. Không có thước đo thì B2 chấm trục "giá trị chức danh" bằng gì?

### Step 3 — Gọi ĐÚNG MỘT block, dừng, chờ CEO
- Gọi block → block ghi kết quả vào ledger → in báo cáo + câu hỏi checkpoint
- **KHÔNG** tự sang block kế khi CEO chưa duyệt
- CEO duyệt → cập nhật ledger → gọi block kế

### Step 4 — Đóng pipeline
Khi B4 xong và CEO ký giao đại diện SHTT: ghi trạng thái `CLOSED — handed to IP agent <ngày>`,
append vào `_meta/decisions.md`, và **đăng ký ngày mục tiêu khóa priority date** vào Gate Register để
QP-02-07 chặn P3 nếu chưa khóa.

## Ledger — `_pipeline_state.md`

```markdown
# IP Pipeline State — <project>
Chuỗi sửa đổi kiểm tại: <ngày> — nguồn: <văn bản mới nhất>
Đích chức danh: 431 | 12-2025 | cả hai
Phân loại: MẬT

| Block | Trạng thái | Ngày | CEO duyệt | Kết quả chính |
|-------|-----------|------|-----------|---------------|
| B0 ip-criteria | DONE | | ✓ | đường chọn: … |
| B1 ip-harvest  | DONE | | ✓ | N ứng viên |
| B2 ip-screen   | ...  | | | routing: … |
| B3 ip-claim    | | | | khung: … |
| B4 ip-dossier  | | | | |

## Cờ ràng buộc
- [ ] Bộc lộ: chưa khóa priority date → cấm công khai
- [ ] Điều 10a: đã ghi xuất xứ đóng góp người/AI
- [ ] Điều 14: có ý định nộp nước ngoài? → cần phép BQP/BCA TRƯỚC
- [ ] Trần thẩm định nhanh: ≤10 điểm YCBH, ≤02 điểm độc lập
```

## Điều phối, KHÔNG làm thay

Orchestrator **không** tra cứu prior art, **không** viết claim, **không** soạn tờ khai. Nó chỉ:
parse → đọc ledger → gọi block → chuyển checkpoint cho CEO → cập nhật ledger.
Nếu bạn thấy mình đang viết nội dung claim trong file này — sai chỗ, đó là việc của `/ip-claim`.

## Reject conditions

```
REJECT IF:
  □ Không nêu được project hoặc --portfolio
  □ B0 chưa có kết quả CEO xác nhận mà đòi chạy B2 trở đi
  □ CEO yêu cầu công khai giải pháp chưa khóa priority date → TỪ CHỐI, giải thích Điều 60
  □ Yêu cầu đưa nội dung giải pháp chưa bộc lộ vào NLM/cloud → TỪ CHỐI
  □ Yêu cầu kết luận "đã đủ tiêu chí chức danh" → TỪ CHỐI, chỉ được trình bảng đối chiếu
```

## COD

| Việc | COD |
|------|-----|
| Tra cứu văn bản, chuỗi sửa đổi | Offload |
| **Chọn đường đạt chức danh (B0)** | **Core** |
| Thu hoạch ứng viên, pre-search | Offload |
| **Quyết đổ tiền / loại ứng viên (B2)** | **Core** |
| Sinh phương án claim, bảng phân biệt | Offload |
| **Chọn khung claim (B3)** | **Core** |
| Soạn bộ đơn, gói câu hỏi | Offload |
| **Ký giao đại diện SHTT (B4)** | **Core** |
| Xác định thuộc bí mật nhà nước | **Ngoài AI** — cơ quan có thẩm quyền |

## NLM reference

Notebook `ip-vn` — **chỉ nguồn luật công khai**. Nghiên cứu nền:
`3_Resources/Deep-Content-Analyzer-Outputs/RESEARCH_ip-sang-che-gphi-chuc-danh_2026-08-06.md`
(Phần A tiêu chí chức danh · Phần B pháp lý IP — **coi là chưa xác nhận, xem Phần D** ·
Phần C trạng thái CEO · **Phần D NĐ 100/2026 lật quy cách**).

## Rules

- **Một block một lượt**, CEO checkpoint chặn — không dồn block.
- **Ledger là kênh duy nhất** giữa các block; không truyền ngầm qua hội thoại.
- **B0 trước B2** — không có thước đo thì không chấm được trục chức danh.
- **In ngày kiểm chuỗi sửa đổi** ở mọi đầu ra có quy cách/biểu mẫu/thời hạn/phí.
- **Không bình quân hai trục** thành một điểm (xem `/ip-screen`).
- Ghi mọi quyết định vào `_meta/decisions.md`; bài học vào `_meta/learnings.md`.
