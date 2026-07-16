# HD-07 — XỬ LÝ SỰ CỐ (TRA TRƯỚC KHI HỎI)

> Mọi lỗi dưới đây đều đã xảy ra THẬT ít nhất một lần. Gặp lỗi mới không có trong bảng:
> ghi lại nguyên văn thông báo + lệnh đã gõ, báo người giữ pipeline — và sau khi xử lý
> xong, THÊM DÒNG vào bảng này (luật golden áp cho cả tài liệu: lỗi một lần, không lần hai).

## 1. Tra theo exit code

| Exit | Nghĩa | Làm gì |
|---|---|---|
| 0 | ĐẠT | Vẫn đọc WARNING nếu có |
| 1 | ĐẠT có WARNING | Đọc danh sách → mục nào là G2 thì xử theo HD-04 §2 |
| 2 | FAIL — gate chặn | Mở `*.validation.json` / report tương ứng, sửa NGUỒN, chạy lại. Không nới ngưỡng |
| 3 | Lỗi môi trường/đầu vào | Thiếu file, thiếu freecadcmd (env `FREECADCMD`), thiếu thư viện pip |
| 4 | merge từ chối seed | Seed chưa validate / verdict FAIL / validation cũ hơn seed → validate lại trước |

## 2. FreeCAD / STEP

| Triệu chứng | Nguyên nhân | Xử lý |
|---|---|---|
| freecadcmd chạy xong nhưng console TRỐNG | Quirk: có args sau tên script thì stdout bị nuốt (script vẫn chạy, report vẫn ghi) | Truyền tham số qua ENV: `FC_FILE`, `FC_OUT`, `FC_NAME`, `FC_SELFTEST` — không truyền args |
| STEP mất tên chi tiết (part thành `Solid1…`) | Xuất bằng `Part.export` | Trong script FreeCAD phải dùng `Import.export` |
| Mass một nhóm lệch hàng trăm % giữa 2 nguồn | Từng là bug nhóm `mass_varies` (đã vá + golden case) | Nếu tái hiện dạng tương tự: nghi extractor, chạy `--golden`, báo người giữ pipeline |

## 3. Inventor / iLogic

| Triệu chứng | Nguyên nhân | Xử lý |
|---|---|---|
| `'Path' is ambiguous` / `'File' is ambiguous` (nhiều dòng) | iLogic tự import namespace Inventor (có class Path/File riêng) đụng `Imports System.IO` | Rule mới: KHÔNG `Imports System.IO`, gọi tường minh `System.IO.Path`/`System.IO.File` |
| `All other Sub's or Function's must be after Sub Main()` | Dán rule NỐI vào nội dung cũ, hoặc khai Sub lồng trong Main | Ctrl+A → Delete rồi dán lại; tốt nhất dùng External Rule trỏ thẳng file trong repo |
| BOM.csv lỗi `E_INVALIDARG` | Tra BOM view theo TÊN (`"Parts Only"`) — tên phụ thuộc ngôn ngữ/trạng thái | Rule hiện hành đã tra theo ViewType enum + fallback; nếu vẫn lỗi: bật Parts Only view (Tools → Bill of Materials → Enable) |
| Export ra "xml only" / thiếu xlsx | Máy không có Excel | Bình thường — rule tự ghi CSV bằng StreamWriter, pipeline nhận CSV |
| Apprentice `Invalid class string` | ProgID sai | ProgID thật là `Inventor.ApprenticeServer` (không phải `...ServerComponent`) — script hiện hành thử cả hai |
| Mass từ Apprentice = 0 hàng loạt | Part chưa gán vật liệu / mass chưa cache (chưa Update+Save) | Việc của bên thiết kế: HD-01 §1; mass Inventor chỉ tin sau khi hết Generic |
| Số từ API Inventor lệch ×10³/10⁶ | API trả đơn vị database: **cm / cm³** (mass kg) | Đổi đơn vị trong script, không "sửa số cho đẹp" |

## 4. Bản vẽ 2D / tiếng Việt / encoding

| Triệu chứng | Nguyên nhân | Xử lý |
|---|---|---|
| PDF chữ thành mojibake (dòng ký tự vô nghĩa) | PDF nhúng font VN cũ hoặc scan | Bỏ PDF, xin DXF/DWG gốc; đó là quy tắc cứng của mảng trích 2D |
| Chữ trong DXF/DWG vẫn mojibake | Font TCVN3 (ABC) thời cũ | Decode bằng bảng map TCVN3 (đã có sẵn trong đường X-UUV) — KHÔNG đoán bằng mắt |
| Python đọc JSON báo lỗi ở ký tự đầu file | File có BOM (UTF-8-SIG) — thường do PowerShell/Excel ghi | Script pipeline đã đọc `utf-8-sig`; script mới phải mở `encoding="utf-8-sig"` |
| Console Windows in tiếng Việt lỗi | Codepage console | Script pipeline đã `reconfigure(encoding="utf-8")`; hoặc `chcp 65001` |

## 5. Kiểm chéo / merge / trace

| Triệu chứng | Nguyên nhân | Xử lý |
|---|---|---|
| S2 lệch mass 2 nguồn hàng loạt, model BM cũ | Mass Inventor tính trên Generic (ρ=1,0) | Số đúng = V(STEP) × ρ(vật liệu bản vẽ 2D) qua merge; gốc rễ vẫn là gán vật liệu (HD-01) |
| S2 báo WARNING thay vì FAIL ở 10% | Chủ đích: một đường phải ĐOÁN ρ (`density_assumed`) thì ngưỡng nới 0,5%→10% | Không phải bug — nhưng phát hành vẫn cần cả 2 nguồn sạch |
| merge exit 4 dù seed "vừa chạy xong" | `*.validation.json` cũ hơn seed (seed bị ghi lại sau khi validate) | Validate lại seed rồi merge |
| trace_numbers bắt số bạn CHẮC là đúng | Số đúng nhưng khác thứ nguyên trường khớp (vd 44 kg khớp qty=44) — trace cố ý chặt | Tìm nguồn thật của số; nếu là hằng số kỹ thuật → khai vào `--constants` kèm công thức trong tài liệu |
| weld-report ra số hàn khổng lồ | Đọc nhầm nhóm: tổng cả `interference`+`duplicates` | Chỉ nhóm `weld` là ứng viên hàn; và vẫn là CẬN TRÊN chưa qua G3 (HD-02 §4) |

## 6. Battery / commit

| Triệu chứng | Nguyên nhân | Xử lý |
|---|---|---|
| Commit bị chặn, log battery đỏ | Sửa code/schema/golden làm hồi quy | Sửa cho battery xanh — KHÔNG `--no-verify` trừ khi cố ý và ghi lý do vào message |
| Battery FAIL ngay case golden STEP sau khi đổi máy | Thiếu FreeCAD hoặc đường dẫn khác | Cài FreeCAD 1.1 / đặt env `FREECADCMD`; chạy lại `run_battery.py --regen` |
