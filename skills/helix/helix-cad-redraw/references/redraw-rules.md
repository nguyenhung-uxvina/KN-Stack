# Luật vẽ lại bản vẽ 2D theo gốc — mỗi luật là một lỗi đã xảy ra thật

> Nguồn: một đợt vẽ lại ~30 tờ chi tiết từ một bộ DXF tách tờ (2026-11-04 → 11-05). Mọi lỗi dưới đây đã lọt
> tới tay chủ đầu tư hoặc chỉ bị bắt khi nhìn ảnh. Cột **Cơ chế** là chỗ luật được thực thi; luật không có cơ chế
> = lời nhắc, và lời nhắc đã thất bại.

| # | Luật | Lỗi đã xảy ra | Cơ chế |
|---|---|---|---|
| R1 | **Khuôn = tờ GỐC đã tách**, không bao giờ là tờ đã vẽ lại | Chạy lại script trên tờ đã vẽ ⇒ ô khối lượng khung tên ghi chồng 2–3 lần ở 14 tờ (một tờ chồng hai giá trị khác nhau) | `text_overlap.py` DUPLICATE (mọi lớp); SKILL bước R3 ghi đường dẫn khuôn vào ledger |
| R2 | Trước khi vẽ: **liệt kê lệch nội tại** (số ghi ≠ hình đo, nhãn tỷ lệ ≠ hệ số kích thước, số làm tròn) và để chủ đầu tư quyết **bằng lời** từng điểm | Bản gốc ghi đè số lên hình đo khác; một hình chi tiết ghi «1:2» nhưng vẽ ~1:3,2; «22,5» hiện «22» | `written_vs_drawn.py` (MISMATCH / FACTOR / ROUNDED) |
| R3 | Chọn cách làm **theo từng tờ**: (A) giữ hình học gốc + sửa đúng điểm đã duyệt, hoặc (B) dựng tham số đầy đủ. Hình cắt **sơ đồ không theo tỷ lệ** ⇒ A | Dựng tham số cho hình sơ đồ sẽ đổi hẳn hình so với gốc | SKILL bước R2 — chủ đầu tư chọn, ghi ledger |
| R4 | **Mở ảnh bản gốc, chép bố trí kích thước** (phía đặt, góc phần tư, tầng) trước khi tự đặt | «0 chồng chữ» nhưng bố trí «không khoa học»: nhãn dồn giữa, Ø không xuyên tâm | cặp ảnh gốc–mới bắt buộc ở R5; `location=` + `dimtih/dimtoh=1` cho Ø/R |
| R5 | Đường kích thước cách chi tiết **≥ 7 mm giấy**, tầng cách **≥ 4 mm**, **giữ tầng của gốc** | Đường kích thước nằm trên đường bao; giãn đều 7 mm dồn hai tầng gốc thành một; xếp tầng dây chuyền đẩy tầng ngoài đè tiêu đề hình | `dim_spacing.py fix` (F-TIER, F-CARRY, F-STACK) + `check` |
| R6 | «Kích thước gốc» = **cùng giá trị + cùng phương + cả hai điểm đo trùng (< 5 mm)** — không theo giá trị | Một tờ có nhiều «100»/«200»: khớp nhầm ⇒ dời kích thước lên chữ của hình khác | `dim_spacing.py` MATCH |
| R7 | Giữ **nét rời trong khối ghi chú** (ký hiệu hàn) trước khi xoá hình | Script xoá «hình», giữ «chữ» ⇒ tam giác mối hàn biến mất, không cổng nào thấy | `notes_strokes.py` + `redraw_helpers.keep_handles` |
| R8 | Kích thước **không ra ngoài khung** bản vẽ | Xếp tầng đẩy kích thước tổng vượt viền khung; script đặt hình sát viền 1–2 mm | `dim_spacing.py` F-FRAME, F-FRAME-IN, `check` OUTSIDE FRAME (outward / view) |
| R9 | Chữ kích thước đặt tay: **`override().set_location()`**, không gán cờ 128 + `text_midpoint` | ezdxf render xoá cờ ⇒ chữ nhảy về giữa đường kích thước | `redraw_helpers.place_dim_text` + test |
| R10 | Kích thước thẳng góc **180°** ⇒ đổi **0°** trước khi vẽ lại | Chữ lộn ngược sau khi vẽ lại | `redraw_helpers.fix_180` |
| R11 | Sửa hình gốc: dời **đồng thời** LINE, LWPOLYLINE, đường bao HATCH, điểm đo DIMENSION; **phá khối** trước (kể cả bản lật gương) | Một mép chi tiết nằm trong khối chèn có bản lật gương ⇒ co hình mà khối không co | `redraw_helpers.stretch`, `explode_named` |
| R12 | Sau khi sửa hình: **vẽ lại khối hình mọi kích thước** | Số đo đúng, nhưng đường gióng còn ở vị trí cũ | `redraw_helpers.rerender_dims` |
| R13 | Vẽ lại hình chi tiết đúng tỷ lệ: phóng hình, **giữ cỡ chữ**, dòng thứ hai của chú thích **đi theo dòng trên**, mặt gạch **giữ tỷ lệ mẫu**, kích thước **đo thật** (`dimlfac`), bỏ vị trí chữ đặt tay | Phóng cả vị trí chữ ⇒ «(3mm)» trôi xa dòng của nó; giữ chữ đặt tay ⇒ chữ rời đường kích thước | `redraw_helpers.scale_region` + test |
| R14 | Mọi số mới thêm phải từ **số ghi đã duyệt**; mọi chữ mất phải có lý do | — | `label_diff.py` |
| R15 | Báo cáo của script / agent **không phải bằng chứng**: xem ảnh cặp gốc–mới từng tờ đổi | Cổng xanh mà ảnh sai: kích thước bị đẩy vào trong chi tiết, ra ngoài khung | SKILL bước R5 — CEO duyệt ảnh, không duyệt bảng số |
| R16 | Ghép bộ: **audit + đếm + mở lại**; cập nhật sha256 từng tờ | Đếm đối tượng «khớp» trong khi khối hình kích thước bị mất | `sheet_merge.py` (exit 2 nếu audit lỗi) |
| R18 | Kích thước thẳng: **điểm đo thứ nhất ở đầu «bắt đầu» theo hướng kích thước** | Gõ điểm trên trước điểm dưới (kích thước đứng) ⇒ ezdxf vẽ mũi tên lộn chiều, đường kích thước thò quá đường gióng một mũi tên ở cả hai đầu — có ở 17/30 tờ vẽ lại, đẩy kích thước qua viền khung | `dim_spacing.py` F-ORIENT (đảo + vẽ lại) + `check` FLIPPED ARROWS (đo trên khối hình; `--orig-dir` bỏ cờ mà gốc AutoCAD cũng có); `fix_180` đảo luôn điểm |
| R19 | Bước hậu xử lý **nhận diện kích thước không theo thứ tự điểm đo** (so cặp điểm không thứ tự) | Sau khi chuẩn hoá chiều, bước «đặt lại như gốc» không còn nhận ra kích thước ⇒ kích thước bị đẩy lên xà bên cạnh | quy ước viết script; `dim_spacing.counterpart` so cặp không thứ tự |
| R17 | **Kiểm công cụ bằng đột biến**: gỡ từng chốt ⇒ test tương ứng phải đỏ | Test đầu tiên của chốt «dời theo» không bao giờ đỏ (vòng chính sửa lại hộ) | `scripts/test_helix_cad_redraw.py` — mỗi luật có test; danh sách đột biến trong SKILL |

## Không phải lỗi — đừng «sửa»
- Kích thước bản gốc **cố ý vắt ngang chi tiết** (< 1 mm, cùng chỗ ở gốc) ⇒ giữ (F-ORIG).
- Chỗ chật bản gốc cũng chật (hai bên là chi tiết khác) ⇒ giữ cách đặt của gốc, ghi lý do.
- Khung tên chòi ra viền ~2 mm là bình thường ⇒ `frame_box` dung sai 5 mm giấy.
