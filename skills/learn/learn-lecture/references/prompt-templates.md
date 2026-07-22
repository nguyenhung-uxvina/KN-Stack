# learn-lecture — Prompt Templates

Placeholder: `{{N}}` = số phần · `{{TÊN_BÀI}}` = tên bài · `{{DÀN_Ý}}` = dàn ý đánh
số N phần (mỗi dòng: `N. <Tiêu đề> — <ý chính, số liệu giữ nguyên>`) ·
`{{SLIDE_CONTENT}}` = nội dung slide THẬT trích ở bước 3.4 (mỗi slide: tiêu đề +
bullet). Nguồn: đã tick sẵn đúng source_ids của bài trước khi gửi prompt.

## TEMPLATE 1 — SLIDE (studio_create, artifact_type=slide_deck)

```
Tạo một slide deck bài giảng tiếng Việt cho "{{TÊN_BÀI}}". Giữ nguyên thuật ngữ
tiếng Anh. CHỈ dùng thông tin trong nguồn đã chọn, KHÔNG thêm kiến thức ngoài,
KHÔNG bịa số liệu.

Bắt buộc đủ {{N}} slide RIÊNG BIỆT, không gộp, ĐÚNG thứ tự và tiêu đề dưới đây;
mỗi slide 1 ý chính + 3–5 gạch đầu dòng NGẮN (không đoạn văn dài):

{{DÀN_Ý}}

Phong cách: sạch, ít chữ, mỗi slide một khái niệm; ưu tiên bảng/mũi tên cho slide
so sánh và sơ đồ. Ngôn ngữ: tiếng Việt.
```

## TEMPLATE 2 — AUDIO (studio_create, artifact_type=audio, language=vi BẮT BUỘC)

```
Tạo một bài giảng audio tiếng Việt cho "{{TÊN_BÀI}}". Giữ nguyên thuật ngữ tiếng
Anh. CHỈ dùng thông tin trong nguồn đã chọn, KHÔNG thêm kiến thức ngoài, KHÔNG bịa
số liệu.

QUAN TRỌNG — audio này phải ĐỒNG BỘ với một slide deck {{N}} slide. Chia lời giảng
thành ĐÚNG {{N}} đoạn, ĐÚNG thứ tự dưới đây. Ở đầu mỗi đoạn, XƯỚNG RÕ số và tên
phần (ví dụ: "Phần 4 — <tiêu đề>") để người nghe lật đúng slide. Mỗi đoạn chỉ diễn
giảng nội dung của slide tương ứng, không lan man sang phần khác.

Nội dung {{N}} phần (khớp 1-1 với slide thật):
{{SLIDE_CONTENT}}

Giọng: người dẫn giảng bài rõ ràng, mạch lạc, sư phạm. Ngôn ngữ: tiếng Việt.
```

## Checklist tự kiểm trước khi gửi TEMPLATE 2

- [ ] Số đoạn == số slide thật (không phải N kế hoạch, nếu đã chấp-nhận-có-ghi-chú)
- [ ] Tiêu đề từng đoạn == tiêu đề slide thật, đúng thứ tự
- [ ] `language=vi` đã set
