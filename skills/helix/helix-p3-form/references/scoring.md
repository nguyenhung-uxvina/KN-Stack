# Bảng chấm phương án hình thể (bước F5, khối BF)

Tệp này quy định cách lập `<P>BF_Scoring.md`. Định dạng dưới đây khớp với cổng máy `scripts/p3_form_lint.py`: sai khuôn bảng thì lint báo `BAD_CELL`, `EMPTY_WEIGHT_NO_FLAG`, `QUESTION_NO_REASON`, `CHECKLIST_INCOMPLETE` hoặc `NO_SENSITIVITY`. Quy tắc nền của sách về đánh giá ở pha hiện thân nằm ở `tkktht-guidelines § Đánh giá ở pha hiện thân` (PB-R175 [TKKTHT Ch22 §1.2]: chỉ so phương án cùng mức cụ thể hoá; PB-R176 [TKKTHT Ch22 §1.1]: điểm kỹ thuật tách khỏi điểm kinh tế; PB-R177 [TKKTHT Ch22 §1.3]: mỗi mục checklist có ít nhất một tiêu chí; PB-R178 [TKKTHT Ch22 §1.3]: bản bố trí cuối thì thẩm định điểm yếu chứ không chọn) và `tkktht-guidelines § Checklist 14 mục`.

## Thang 0–4 (VDI 2225)

| Điểm | Mức | Ý nghĩa khi chấm một yêu cầu W | Nguồn |
|---|---|---|---|
| 0 | Không dùng được | Không đáp ứng, hoặc phá chức năng | [ngoài sách] |
| 1 | Chưa đạt | Đáp ứng một phần, cần sửa lớn | [ngoài sách] |
| 2 | Tạm chấp nhận | Đáp ứng ở mức chịu được, có điểm yếu đã biết | [ngoài sách] |
| 3 | Tốt | Đáp ứng đủ, sai lệch nhỏ | [ngoài sách] |
| 4 | Rất tốt (lý tưởng) | Đáp ứng trọn vẹn, có dư địa | [ngoài sách] |

Ghi chú nguồn: thang 0–4 theo VDI 2225 là cách P&B dùng ở bước đánh giá hiện thân cuối (không trọng số khi chỉ còn một phương án) [TKKTHT Ch22 §2.9]; trong BF thang này dùng cho mọi phương án PA và mọi chuẩn đối sánh HC, có trọng số cho yêu cầu W.

## Ba loại ô và miền giá trị

- Dòng `D` (yêu cầu cứng, demand): mỗi ô phương án chỉ nhận `Đạt` hoặc `Loại`. Một `Loại` loại phương án khỏi vòng chọn; không cộng điểm.
- Dòng `W` (mong muốn, wish): mỗi ô nhận một số nguyên `0`–`4`. Điểm có trọng số = trọng số × điểm; tổng cộng theo cột phương án.
- Ô `?(<lý do>)` (chưa có số liệu): cho phép ở cả dòng D và W, bắt buộc có lý do trong ngoặc, ví dụ `?(chưa có số liệu va đập đầu đạn)`. `?` trần, không lý do, bị lint báo `QUESTION_NO_REASON`. Ô `?` không được tự đổi thành số; xử lý ở mục Độ nhạy.

## Ánh xạ yêu cầu → DP

Cột `DP` lấy từ cột nguồn `HOQ-DPx` của bảng yêu cầu (khối B2/HOQ): mỗi yêu cầu `Req-ID` trỏ tới thông số thiết kế `DP-x` mà phương án hình thể phải quyết. Chấm phương án trên đúng DP đó: điểm cho yêu cầu = mức phương án thoả DP ấy, không phải ấn tượng chung. Yêu cầu không ánh xạ được DP nào thì vẫn giữ trong bảng, để ô DP là `—`, và xử lý theo luật Q7 bên dưới.

## Luật D/W tạm (Q6)

Khi bảng yêu cầu chưa chốt một yêu cầu là cứng hay mong muốn, ghi `D tạm` hoặc `W tạm` ở cột D/W thay vì tự quyết. Lint chấp nhận hai giá trị này (bỏ chữ «tạm» khi kiểm miền ô). Dòng `D tạm` chấm theo `Đạt`/`Loại`, dòng `W tạm` chấm theo `0`–`4`. Mọi dòng «tạm» phải nằm trong danh sách việc chờ CEO chốt, vì chốt D hay W là quyết định của CEO, không phải của khối BF.

## Luật cờ đỏ trọng số trống (Q7)

Yêu cầu W không có DP, hoặc chưa có trọng số vì CEO chưa chốt: GIỮ dòng, để ô `Trọng số` TRỐNG, và ghi `🔴` trong cột Ghi chú kèm việc cần làm (ví dụ `🔴 CEO chốt trọng số`). Không tự điền trọng số để bảng trông đầy. Lint báo `EMPTY_WEIGHT_NO_FLAG` nếu ô trống mà dòng không có `🔴`. Ô Trọng số có giá trị phải là số (`3`, `2,5`, `15%`).

## Khuôn tệp

Khuôn đầy đủ nằm ở `references/templates/scoring-template.txt` (tách khỏi tệp này để bộ kiểm con trỏ sách không đọc các dòng bảng mẫu như dòng dữ liệu); dán nguyên, thay giá trị mẫu, giữ nguyên tiêu đề và tên cột. Các dòng chốt của khuôn:

- Mục `# Bảng chấm`, rồi `## Checklist 14 mục` với tiêu đề bảng `# | Mục | Tiêu chí` (14 dòng), rồi `## Bảng chấm`, rồi `## Độ nhạy`.
- Mỗi chức năng một mục `### F-<id>` với tiêu đề bảng `Req-ID | D/W | DP | Trọng số | PA-<id>-1 | … | HC-<id>-1 | … | Ghi chú`.
- Dòng mẫu: D → `R-11 | D | DP-1 | 1 | Đạt | Loại | Đạt`; W → `R-12 | W | DP-2 | 3 | 3 | 4 | 1`; ô chưa biết → `?(chưa có số liệu)`; W tạm không trọng số → ô Trọng số trống và Ghi chú `🔴 CEO chốt trọng số`.


Quy ước về cấu trúc, mỗi điều khớp một mã lint:

- Đúng 14 dòng trong `## Checklist 14 mục` (đánh số 1–14), mỗi dòng có tiêu chí; mục bỏ phải ghi `Bỏ — lý do: …` (nếu không là `CHECKLIST_SKIP_NO_REASON`). Tên 14 mục lấy từ `tkktht-guidelines § Checklist 14 mục`, không nghĩ ra.
- `## Bảng chấm` có một mục `### F-<id>` cho mỗi chức năng của F2; trong mỗi mục là một bảng có cột đầu `Req-ID`, bốn cột cố định `Req-ID | D/W | DP | Trọng số`, tiếp theo là các cột `PA-<id>-<n>` (phương án hình thể) và `HC-<id>-<n>` (chuẩn đối sánh từ benchmark), cột cuối là `Ghi chú`. Mọi `PA-`/`HC-` khai ở F4/benchmark phải có cột, thiếu thì `CANDIDATE_MISSING`.
- Số ô mỗi dòng bằng số cột tiêu đề.
- Mục `## Độ nhạy` bắt buộc (thiếu thì `NO_SENSITIVITY`).

## Độ nhạy (±20% và ô `?`)

Sau khi chấm, kiểm hai lần và ghi kết quả ở `## Độ nhạy`:

1. Đổi từng trọng số ±20% (làm đồng thời mọi trọng số theo cả hai chiều và từng trọng số riêng nếu nghi ngờ): phương án dẫn đầu có đổi không? Nếu đổi, phương án dẫn đầu không vững; ghi nó là «dẫn đầu mong manh».
2. Thay mọi ô `?(…)` bằng `0` rồi bằng `4`: phương án dẫn đầu có đổi không? Nếu đổi, ô `?` nào quyết định, và việc thử/đo nào đóng được ô đó; việc này đi vào kế hoạch thử của F6.

Kết luận độ nhạy chỉ nói dẫn đầu vững hay mong manh và vì sao; chọn phương án là quyết định của CEO.
