# Định Dạng Nhật Ký Học Tập

Nhật ký học tập nằm trong `./learning-records/` và được đánh số tuần tự: `0001-slug.md`, `0002-slug.md`, v.v. Tạo thư mục theo nhu cầu — chỉ khi viết bản ghi đầu tiên.

Chúng tương đương với ADR trong dạy học: ghi lại những bài học không hiển nhiên, insight quan trọng và kiến thức nền được khai báo sẽ định hướng các phiên tiếp theo. Dùng để xác định vùng phát triển gần nhất.

## Template

```md
# {Tiêu đề ngắn về điều đã được học hoặc xác lập}

{1-3 câu: điều đã học (hoặc kiến thức nền được xác lập), và tại sao nó quan trọng cho các phiên tiếp theo.}
```

Đó là toàn bộ định dạng. Một nhật ký học tập có thể chỉ là một đoạn văn. Giá trị nằm ở việc ghi lại _rằng_ điều này đã được biết và _tại sao_ nó thay đổi những gì cần dạy tiếp — không phải ở việc điền đầy đủ các phần.

## Các Phần Tùy Chọn

Chỉ thêm khi chúng thực sự có giá trị. Hầu hết các bản ghi sẽ không cần đến.

- **Trạng thái** frontmatter (`active | superseded by LR-NNNN`) — hữu ích khi hiểu biết trước đó hóa ra sai và bị thay thế.
- **Bằng chứng** — người dùng đã thể hiện sự hiểu biết như thế nào (câu hỏi được trả lời, bài tập hoàn thành, kinh nghiệm trước đó được trích dẫn). Hữu ích khi tuyên bố có thể cần xem lại.
- **Hệ quả** — điều này mở khóa hoặc loại trừ gì cho các phiên tiếp theo. Đáng ghi lại khi không hiển nhiên.

## Đánh Số

Quét `./learning-records/` để tìm số cao nhất hiện có và tăng thêm một.

## Khi Nào Viết Nhật Ký Học Tập

Viết một bản khi bất kỳ điều nào sau đây là đúng:

1. **Người dùng đã thể hiện hiểu biết thật sự về điều gì đó không tầm thường** — không chỉ là tiếp xúc, mà là bằng chứng họ có thể dùng khái niệm đúng cách. Điều này đặt ra nền tảng mới cho những gì cần dạy tiếp theo.
2. **Người dùng khai báo kiến thức nền** — "Tôi đã biết X." Ghi lại để các phiên sau không dạy lại. Cũng ghi lại _độ sâu_ được tuyên bố.
3. **Một hiểu lầm được sửa** — người dùng trước đây tin vào điều sai và giờ hiểu tại sao. Đây là loại có giá trị cao: chúng dự đoán những khúc mắc trong tương lai với các chủ đề liên quan.
4. **Mission thay đổi do việc học** — người dùng phát hiện họ quan tâm đến thứ gì đó khác với những gì họ nghĩ. Liên kết chéo đến [[MISSION.md]] và cập nhật nó.

### Những Gì _Không_ Đủ Tiêu Chuẩn

- Nội dung chỉ được đề cập. Đề cập không phải là học. Hãy đợi bằng chứng.
- Bất cứ điều gì đã được ghi súc tích trong [[GLOSSARY.md]] dưới dạng định nghĩa thuật ngữ. Không duplicate.
- Nhật ký hoạt động theo từng phiên. Nhật ký học tập không phải là tạp chí — chúng là insight ở cấp độ quyết định.

## Thay Thế

Khi một bản ghi sau mâu thuẫn với bản ghi trước (hiểu biết của người dùng đã sâu hơn hoặc được sửa lại), đánh dấu bản ghi cũ là `Status: superseded by LR-NNNN` thay vì xóa nó. Lịch sử về cách hiểu biết phát triển bản thân nó là tín hiệu hữu ích.
