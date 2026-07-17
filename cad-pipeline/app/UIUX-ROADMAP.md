# UI/UX ROADMAP — Phần mềm điều khiển WX Pipeline

> Lập 2026-07-17 (GUI v0.5.3). Bản trình bày có mockup: artifact "Kế hoạch UI/UX — WX
> Pipeline" trên claude.ai (CEO giữ link). Quy trình mỗi mốc: smoke-test offline →
> CHANGELOG → commit; tag v0.5 sau khi U2 chạy thật 1 tuần.

## Ràng buộc (không thương lượng)

1. **Lớp vỏ tuyệt đối** — GUI chỉ subprocess script đã field-test, không chạm lõi.
2. **Air-gap** — 0 phụ thuộc ngoài Tkinter, không cổng mạng, không CDN.
3. **Kỷ luật gate** — UI không làm gate dễ lách hơn (FAIL đỏ, --force bắt lý do + nhật ký).
4. **Người dùng xưởng** — không quen dòng lệnh, màn scale 125%, chữ to màu rõ.

## U1 — ĐÃ GIAO (v0.5.1 → v0.5.3)

Viewer lỗi dạng cây (bấm rule → cách sửa) · kỷ luật --force + runs.jsonl · nhớ config
+ thư mục gần đây · nút Dừng/Lưu log · console kiểu PowerShell: kéo-giãn (PanedWindow),
màu 4 mức, giữ lịch sử các lần chạy, nút Nhật ký…

## U2 — KẾ TIẾP (~1 buổi code, làm theo thứ tự)

| # | Việc | Ước lượng | Nghiệm thu khi |
|---|---|---|---|
| 1 | **Khóa nút khi đang chạy** + đồng hồ giây trên status ("Đang chạy… 01:24") | ~1h | đang chạy không bấm được nút ▶ khác |
| 2 | **Thanh sản phẩm + stepper**: chọn sản phẩm MỘT lần trên đầu cửa sổ; stepper 5 bước (Kiểm bản vẽ → Trích xuất → Phát hành → 5 đầu ra/trace → Actuals) với trạng thái đọc từ report JSON có sẵn qua `scan_status(dir)` (tái dùng parser viewer v0.5.2) | ~3h | mở app chọn Tong lap → thấy ngay bước nào FAIL mà chưa cần chạy gì |
| 3 | **Pill GATE + badge tab**: pill FAIL/WARNING/PASS (verdict xấu nhất) trên thanh sản phẩm; badge đỏ số lỗi trên tab có việc (Thiết kế: D1/SEC · KS: S1–S4) | ~1h | sau 1 lần chạy FAIL, tab đúng người hiện badge đúng số |
| 4 | **Phím tắt + tooltip**: F5 chạy lại lệnh gần nhất, Ctrl+L xóa, Ctrl+S lưu log, Ctrl+1..6 chuyển tab; tooltip mọi nút (nút gọi script nào, đọc HD nào) | ~1h | F5 lặp đúng lệnh + cờ gần nhất |

Kỹ thuật mục 2: frame ctx trên Notebook; các tab vẫn đọc `self.var("k_dir")` (tự điền
theo thanh sản phẩm, vẫn sửa lệch được từng tab) — không phá lớp vỏ.

## U3 — SAU KHI DÙNG ỔN ĐỊNH (mỗi mục có điều kiện kích hoạt)

- **a. Dashboard trong app** (tab CEO render bảng + blocker, không mở .md ngoài) — khi CEO dùng dashboard ≥1 tuần.
- **b. Hàng đợi tác vụ** (kiểm nhiều sản phẩm tuần tự) — khi có nhu cầu chạy lô thật.
- **c. Đóng gói .exe** (PyInstaller onefile, máy xưởng khỏi cài Python; kèm SHA) — khi app ổn định; là mốc v0.6.
- **d. Cỡ chữ xưởng** (nút A−/A+ lưu config) — khi có phản hồi người dùng xưởng.
- **e. Theme sáng** cho phần chrome (console giữ PowerShell) — chỉ khi có yêu cầu thật.

## KHÔNG LÀM (đã cân nhắc)

- Web dashboard LAN — lộ dữ liệu MẬT + thêm server, trái air-gap.
- Thư viện UI ngoài (ttkbootstrap/customtkinter) — vỡ nguyên tắc 0-dependency.
- Auto-run khi chọn thư mục — gate phải là hành động chủ động của con người.

## Điểm đau → hạng mục (căn cứ)

| Điểm đau | Trả lời |
|---|---|
| 6 tab ngang hàng, người mới không biết luồng HD-01→06 | U2-2 stepper |
| Cùng sản phẩm phải chọn đường dẫn nhiều lần (18 biến) | U2-2 thanh sản phẩm |
| Verdict trôi trong console, muốn biết đang FAIL gì phải mở viewer | U2-3 pill + badge |
| Đang chạy bấm nút khác → messagebox khó chịu | U2-1 khóa nút |
| Vòng sửa-chạy lại (phổ biến nhất) chưa có phím tắt | U2-4 F5 |
| Dashboard CEO phải mở file .md ngoài app | U3-a |
| Máy xưởng không Python không chạy được | U3-c |
