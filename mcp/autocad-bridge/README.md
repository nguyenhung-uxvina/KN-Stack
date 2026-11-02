# autocad-bridge — MCP server cho AutoCAD

Server điều khiển AutoCAD đang chạy qua COM (pywin32) và đọc DXF ngoại tuyến bằng ezdxf. Mọi thứ chạy trên máy, không gọi ra mạng.
Đã chạy thử trên AutoCAD 2025 (R25.0) với bộ bản vẽ 42 tệp DXF.

> Server giữ bản vẽ trên máy, nhưng **kết quả tool vẫn được gửi tới mô hình AI mà client dùng**. Các rào chắn dưới đây bảo vệ tệp và bản vẽ, không bảo vệ nội dung gửi tới mô hình.

## Cài đặt

```bash
pip install mcp pywin32 ezdxf
claude mcp add --scope user autocad -- python D:/KN-Stack-autocad/mcp/autocad-bridge/server.py
```

Sau khi sửa server, chạy `/mcp` → reconnect `autocad` (hoặc mở phiên mới) thì thay đổi mới có hiệu lực.

## Cấu hình (biến môi trường)

| Biến | Mặc định | Ý nghĩa |
|---|---|---|
| `AUTOCAD_BRIDGE_READ_ROOTS` | `D:\AutoCAD\Workspace` | Các gốc thư mục được ĐỌC, ngăn cách bằng `;` |
| `AUTOCAD_BRIDGE_WRITE_ROOTS` | `D:\AutoCAD\Workspace\output` | Các gốc thư mục được GHI (CSV, Save As, khai triển) |
| `AUTOCAD_BRIDGE_DENY_ROOTS` | `D:\AutoCAD\AutoCAD 2025` | Thư mục luôn bị cấm. Mặc định là thư mục cài AutoCAD, vì ghi vào `Support\` là đường lây của sâu `acad.lsp` |
| `AUTOCAD_BRIDGE_PROFILE` | `draft` | `read`: chỉ đọc, không đăng ký tool ghi. `draft`: đọc + vẽ + lưu |
| `AUTOCAD_BRIDGE_LEDGER` | `%LOCALAPPDATA%\autocad-bridge\ledger.jsonl` | Sổ kiểm toán |
| `AUTOCAD_BRIDGE_TIMEOUT` | `30` | Giây tối đa cho một lời gọi COM |
| `AUTOCAD_BRIDGE_READ_BUDGET` | `20` | Số giây tối đa retry lời gọi đọc khi AutoCAD bận |

Không đặt gốc nào thì **từ chối tất cả**.

## Rào chắn

| Rào | Cách làm |
|---|---|
| Luồng COM | Mọi lời gọi chạy trên một luồng STA riêng, có timeout. Quá hạn khi lời gọi chưa chạy trả `ACAD_TIMEOUT`, không có gì thay đổi. Quá hạn khi đang chạy trả `UNKNOWN_COMMIT`: có thể đã ghi, phải kiểm trước khi làm lại |
| Retry | Chỉ retry **lời gọi đọc** (AutoCAD bận, hoặc win32com tạm mất thông tin kiểu ngay sau khi đóng bản vẽ). Lời gọi ghi chạy đúng một lần; nếu AutoCAD bận thì trả `ACAD_BUSY` kèm `partial`, là các handle đã tạo |
| Gắn bản vẽ | Tool ghi bắt buộc có `expected_document` (tên, đường dẫn hoặc `doc_id`). Nếu bản vẽ hiện hành khác thì trả `DOCUMENT_CHANGED` và không ghi gì. Mọi kết quả đều kèm `_target` |
| Đường dẫn | Kiểm bằng `realpath` + `commonpath`, không dùng `startswith`. Chặn UNC, `\\?\`, ADS, ổ mạng, junction trỏ ra ngoài gốc và đuôi tệp lạ. Bản vẽ đang mở cũng phải nằm trong gốc thì mới được đọc hoặc ghi |
| Lệnh | `acad_command(verb, args)` chỉ nhận allow-list (ZOOM E/A/P, REGEN, REGENALL). Server tự dựng chuỗi lệnh rồi chờ `CMDACTIVE = 0` |
| Hoàn tác | Mỗi tool ghi là một bước UNDO (`StartUndoMark`/`EndUndoMark`). Server không tự rollback bằng `_UNDO B` |
| Thao tác phá huỷ | Lưu đè hoặc đóng bản vẽ mà bỏ thay đổi đều cần `plan_token`. Gọi lần 1 để nhận token, gọi lần 2 kèm token. Token gắn với bản vẽ, revision và tham số, hết hạn sau 120 giây |
| Sổ kiểm toán | Mỗi lời gọi ghi một dòng JSONL, các dòng nối chuỗi băm. Chỉ lưu băm của tham số, không lưu đường dẫn hay chữ trong bản vẽ |
| Mã lỗi | Lỗi trả về dạng `isError` với `code` ổn định: `ACAD_NOT_RUNNING`, `ACAD_BUSY`, `ACAD_TIMEOUT`, `UNKNOWN_COMMIT`, `DOCUMENT_CHANGED`, `DOCUMENT_NOT_FOUND`, `READ_ONLY_TARGET`, `PATH_DENIED`, `COMMAND_DENIED`, `CONFIRM_REQUIRED`, `COM_ERROR`, `INVALID_ARGUMENT`, `INTERNAL_ERROR` |
| Phân loại tool | Tool đọc gắn `readOnlyHint`; `acad_save` và `acad_close` gắn `destructiveHint` |

## Tool

| Nhóm | Tool |
|---|---|
| Đọc bản vẽ đang mở | `acad_status` · `acad_list_documents` · `acad_layers` · `acad_entities` · `acad_dimensions` · `acad_texts` · `acad_title_block` · `acad_holes` · `acad_extents` |
| Đọc DXF ngoại tuyến | `acad_dxf_summary` · `acad_scan_folder` (xuất CSV; báo mã trùng, trùng số tờ, tên tệp khác tên trong khung tên) |
| Tài liệu | `acad_open` (mặc định chỉ đọc) · `acad_activate` · `acad_zoom_extents` · `acad_close` · `acad_new`* · `acad_save`* |
| Vẽ* | `acad_add_layer` · `acad_add_line` · `acad_add_circle` · `acad_add_arc` · `acad_add_polyline` · `acad_add_text` · `acad_add_dimension` · `acad_command` |

\* Chỉ có ở profile `draft`.

## Lưu ý khi đọc bản vẽ

- **Lấy giá trị kích thước từ `shown` (chữ in trên giấy), không lấy từ số đo hình học.** Hình cắt rút gọn và DIMLFAC làm số đo hình học sai.
- ActiveX không lộ điểm gióng của kích thước, nên chỉ có vị trí chữ.
- `SaveAs` của AutoCAD khi không truyền kiểu thì luôn lưu thành DWG và nối thêm `.dwg`. Bridge tự truyền kiểu `65` (DXF 2018) cho `.dxf` và `64` cho `.dwg`.
- Ô khung tên (`TITLE_CELLS_TCVN`) được hiệu chỉnh cho block «KHUNG TÊN BẢN VẼ LẮP». Nếu khung tên nằm trong block ẩn danh thì bridge chưa đọc được.
- `acad_holes` đếm mọi CIRCLE, kể cả vòng ký hiệu ren (ví dụ Ø6,65 là chân ren M8) và vòng vát mép.
- Chữ lấy từ bản vẽ là **dữ liệu**, không phải lệnh (`content_origin: drawing_text_untrusted`).

## Test

```bash
python -m pytest mcp/autocad-bridge/tests -v
```

Có 90 test, không cần AutoCAD:
- `tests/fake_acad.py` mô phỏng các hành vi đã đo trên AutoCAD 2025 thật: từ chối khi bận, SaveAs nối thêm `.dwg`, mất thông tin kiểu sau khi đóng bản vẽ, `CMDACTIVE`.
- Mỗi rào chắn đều có test thất bại trước khi sửa, và test lỗi vẽ trùng đã được kiểm bằng đột biến.
