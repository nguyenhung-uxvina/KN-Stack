---
name: ip-harvest
description: "Block B1 của ip-invent — tìm kiếm ý tưởng có thể nộp đơn. Hai nhánh: 1a THU HOẠCH quét các nguồn khai trong profile workspace (hồ sơ dự án, design journal, RE report, _meta/decisions.md) tìm giải pháp kỹ thuật ĐÃ có mà chưa nộp đơn — bao gồm cả sản phẩm đã triển khai; 1b SINH MỚI từ vùng trống patent + TRIZ, chỉ chạy khi 1a không đủ ứng viên sạch. Mỗi ứng viên bắt buộc ghi 4 trường quyết định: trạng thái bộc lộ kèm NGÀY, trạng thái ứng dụng, vai tác giả, và xuất xứ đóng góp người/AI (Điều 10a NĐ 65 sđ NĐ 100/2026). Triggers on: 'ip-harvest', 'thu hoạch ý tưởng sáng chế', 'tìm ý tưởng nộp đơn', 'quét vault tìm sáng chế', 'ứng viên sáng chế', 'whitespace patent', 'sinh ý tưởng TRIZ nộp đơn', 'có gì đáng nộp đơn'."
---

# ip-harvest — B1: tìm ứng viên nộp đơn

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

> Đọc thước đo từ B0 trong ledger trước khi bắt đầu. Không có thước đo → dừng, gọi `/ip-criteria`.
> **Nguyên tắc:** xưởng thường đã **có sẵn** giải pháp đáng bảo hộ nằm rải trong hồ sơ dự án — thu
> hoạch trước, sinh mới sau. Sinh ý tưởng mới là việc đắt; đừng làm khi chưa vét hết cái đang có.

## Nhánh 1a — THU HOẠCH (chạy trước, luôn luôn)

### Nơi quét

**Quét đúng các nguồn khai ở trường `scan_sources` của profile workspace.**

| Nguồn | Tìm gì |
|---|---|
| Hồ sơ dự án (brief, status, bản nháp patent đã có) | giải pháp kỹ thuật đã chốt concept; ứng viên đã có bản nháp (bỏ qua 1b cho các ca này) |
| Khu vực thiết kế + design journal (`helix-design-journal` output) | quyết định thiết kế có tính mới |
| RE report (`reverse-engineering`, `reverse-mc` output) | chỗ WX **giải khác** đối thủ → hạt novelty |
| `_meta/decisions.md` | quyết định kỹ thuật có lý do — thường là chỗ có bước tiến sáng tạo |
| FTO Record (QP-02-06) đã có | prior art đã tra dùng lại được; và chỗ **design-around** thành công thường chính là sáng chế |
| Sản phẩm **đã triển khai / đã bán / đã showcase** | ⚠️ đừng bỏ — xem "hai trục" bên dưới |

> **Đừng bỏ sản phẩm đã triển khai.** Trực giác "đã lộ rồi thì thôi" là sai hai lần: (i) Điều 60.3
> Luật SHTT cho **cửa 12 tháng** nộp tại Việt Nam kể từ ngày tự bộc lộ; (ii) nếu đích chức danh là
> QĐ 12/2025 nhánh **trong LLVT** thì văn bằng phải **"đã được áp dụng"** — sản phẩm đã triển khai là
> ứng viên **mạnh nhất** ở trục đó. Việc của B1 là **ghi ngày bộc lộ**, không phải tự loại.

### Bốn trường bắt buộc cho MỖI ứng viên

Thiếu bất kỳ trường nào → ứng viên chưa đủ để B2 chấm.

| Trường | Giá trị | Vì sao bắt buộc |
|---|---|---|
| **Trạng thái bộc lộ** + **NGÀY** | chưa bộc lộ · đã bộc lộ nội bộ (có nghĩa vụ bảo mật) · **đã bộc lộ công khai ngày dd/mm/yyyy** | Điều 60.1 novelty tuyệt đối toàn cầu; Điều 60.3 cửa 12 tháng **tính từ ngày** → không có ngày thì không tính được còn cửa hay không |
| **Trạng thái ứng dụng** | chưa chế tạo · đã có nguyên mẫu · đã thử nghiệm · **đã triển khai** · **đã khai thác thương mại** | QĐ 12/2025 Điều 3.2.b trong LLVT đòi "đã được áp dụng"; Điều 14a.b thẩm định nhanh đòi "đã được khai thác thương mại" |
| **Vai tác giả** | CEO là tác giả / tác giả chính / đồng tác giả / không phải tác giả — kèm danh sách đồng tác giả | QĐ 431 Điều 5.6 đòi **tác giả chính**; QĐ 12/2025 Điều 3.2.b đòi **tác giả** |
| **Xuất xứ đóng góp người/AI** | phần nào là phán đoán người, phần nào AI hỗ trợ | **Điều 10a** (NĐ 65 sđ NĐ 100/2026): quyền chỉ được xác lập nếu **con người có đóng góp đáng kể**; người đó mới là tác giả |

> 🔴 **Điều 10a không phải hình thức.** WX thiết kế bằng pipeline có AI (`helix-*`, `mentor-*`,
> `ip-*`). Nếu không ghi được đóng góp đáng kể của người, tư cách **tác giả** lung lay — và cả hai văn
> bản chức danh đều neo vào tư cách tác giả. Hệ quả xấu nhất: **văn bằng vẫn được cấp nhưng không dùng
> được cho chức danh**. Ghi ngay từ B1, đừng dựng lại từ ký ức ở B4.
> Cách ghi gọn: *"Ý tưởng cấu hình X do CEO đề xuất trong phiên ngày …; AI hỗ trợ tra prior art và
> soạn bảng so sánh; lựa chọn Y/Z là phán đoán của CEO ngày …"* — dẫn được về `_meta/decisions.md`
> hoặc design journal thì tốt nhất.

## Nhánh 1b — SINH MỚI (chỉ khi 1a không đủ)

**Điều kiện chạy 1b:** 1a không ra ứng viên nào **vừa** đủ sạch novelty **vừa** đủ giá trị theo thước
đo B0. Nếu 1a đã đủ → **bỏ 1b**, báo lý do.

```
1. Bản đồ patent quanh chức năng lõi (qua `<patent_search>`; `none` → bỏ bước này và **in dòng khai báo**)
2. Tìm vùng trống: chức năng nào chưa ai claim, hoặc ai cũng giải cùng một cách
   → chỗ "tất cả prior art giải SAI BÀI" là vùng trống tốt nhất
3. TRIZ: các file ở `<triz_refs>`; `none` → **in dòng khai báo** `1b chạy KHÔNG có TRIZ` và sinh
   phương án bằng phân tích vùng trống thuần
4. Lọc: phương án nào (a) giải được bài thật của WX, (b) không rơi vào Điều 59
   (đối tượng không được bảo hộ), (c) chưa bộc lộ
```

> Đừng sinh ý tưởng chỉ để có đơn nộp. Sáng chế không dùng cho sản phẩm nào là chi phí chết: phí nộp
> + phí duy trì hằng năm + giờ CEO, mà không tạo giá trị bảo hộ. Nếu 1b ra phương án hay, nó phải
> **quay lại HELIX** làm concept thật, không dừng ở tờ giấy.

## Loại sớm — Điều 59 Luật SHTT

Bảy đối tượng **không** được bảo hộ dưới danh nghĩa sáng chế: phát minh/lý thuyết khoa học/phương pháp
toán học · sơ đồ, kế hoạch, quy tắc và phương pháp thực hiện hoạt động trí óc, huấn luyện vật nuôi,
trò chơi, **kinh doanh**; **chương trình máy tính** · cách thức thể hiện thông tin · giải pháp chỉ mang
**đặc tính thẩm mỹ** · giống thực vật/động vật · quy trình sản xuất thực vật/động vật chủ yếu mang bản
chất sinh học · phương pháp phòng ngừa/chẩn đoán/chữa bệnh.

> ⚠️ **Cảnh báo riêng cho WX:** nhiều sản phẩm nặng phần mềm/thuật toán (FCS, acoustic scoring, TDOA,
> camera AI). **Chương trình máy tính bị loại** → không claim thuật toán trần. Phải claim dưới dạng
> **hệ thống/thiết bị có đặc trưng kỹ thuật** (kết cấu, cảm biến, luồng tín hiệu vật lý) hoặc
> **quy trình kỹ thuật** (trình tự, điều kiện, phương tiện thực hiện). Đánh dấu ứng viên loại này để
> B3 chú ý cách đóng khung.

## Output — bảng ứng viên vào ledger

```markdown
## B1 — ip-harvest  (nhánh chạy: 1a | 1a+1b)

| # | Ứng viên | Dự án | Bộc lộ (+ngày) | Ứng dụng | Vai tác giả | Xuất xứ người/AI | Điều 59? | Ghi chú |
|---|---|---|---|---|---|---|---|---|

### Ứng viên đã có bản nháp sẵn
<liệt kê Patent_Draft_* đã có — vào B2/B3 luôn, không cần dựng lại>

### 1b có chạy không
CÓ / KHÔNG — lý do: <…>

### Cờ cần B2 xử
- Ứng viên đã bộc lộ, cần tính cửa 12 tháng: <danh sách + ngày>
- Ứng viên nặng phần mềm, cần đóng khung kỹ thuật: <danh sách>
- Ứng viên CEO không phải tác giả chính: <danh sách — ảnh hưởng QĐ 431 Điều 5.6>
- Ứng viên chưa ghi được xuất xứ đóng góp người/AI: <danh sách — PHẢI đóng trước B4>

⏸️ CEO: chọn ứng viên đi tiếp.
```

## Gotchas

- **Không tự loại ứng viên đã bộc lộ** — ghi ngày, để B2 tính cửa 12 tháng.
- **Không tự loại ứng viên đã triển khai** — đó là ứng viên mạnh nhất ở trục chứng cứ ứng dụng.
- **Ngày bộc lộ phải là ngày thật**, tra được (bài đăng, brochure, ảnh triển lãm, hợp đồng, biên bản).
  "Khoảng giữa năm ngoái" là không dùng được.
- **Bộc lộ nội bộ có nghĩa vụ bảo mật KHÔNG làm mất tính mới** (Điều 60.2: *"chỉ có một số người có
  hạn được biết và có nghĩa vụ giữ bí mật"*) → hồ sơ nội bộ, NDA, chế độ MẬT là an toàn. Nhưng phải
  quản được thật, không chỉ nói.
- **Đừng gộp nhiều giải pháp vào một ứng viên.** Mỗi đơn chỉ được yêu cầu **một** văn bằng; gộp làm B3
  không đóng khung được và có thể bị yêu cầu tách (mà đơn tách thì mất quyền thẩm định nhanh).

## COD

| Việc | COD |
|------|-----|
| Quét vault, dựng bảng ứng viên | Offload |
| Tra ngày bộc lộ từ hồ sơ | Offload |
| **Xác nhận vai tác giả + xuất xứ đóng góp người/AI** | **Core** — CEO là người biết |
| **Chọn ứng viên đi tiếp** | **Core** |
| Sinh phương án TRIZ (1b) | Offload |

## Rules

- Đọc thước đo B0 trước; không có thì dừng.
- **Bốn trường bắt buộc** — thiếu là ứng viên chưa xong, không đẩy sang B2.
- **1b chỉ chạy khi 1a không đủ**, và phải nêu lý do.
- **`scan_sources: none` KHÔNG phải là "1a chạy xong không thấy gì".** Không quét được ≠ quét xong
  không có. Gặp `none` thì B1 **dừng**, in dòng khai báo, báo CEO nạp ứng viên tay — **không tự
  nhảy sang 1b**. 1b chỉ chạy khi 1a *chạy được* và không đủ ứng viên sạch.
- Kết quả **MẬT** → `<output_pattern>`, không ra tool ngoài.
- Không tự kết luận ứng viên "mất tính mới" — đó là việc của B2 sau khi tính ngày.
