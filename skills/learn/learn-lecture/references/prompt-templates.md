# learn-lecture — Prompt Templates

Placeholder: `{{N}}` = số phần · `{{TÊN_BÀI}}` = tên bài · `{{PHẠM_VI}}` = khối "PHẠM VI
BẮT BUỘC" (số mục + tiêu đề tiếng Anh gốc + khoảng trang + câu BỎ QUA phần còn lại) ·
`{{DÀN_Ý}}` = dàn ý-nguồn đánh số N phần chưng cất từ source_get_content (mỗi dòng:
`N. <Tiêu đề> — <ý chính, ví dụ, số liệu giữ nguyên>`) · `{{TIÊU_ĐỀ_SLIDE}}` = cột tiêu
đề đọc từ `slide-script.md` (KHÔNG trích lại từ PDF) · `{{DÀN_Ý_NGUỒN}}` = khung N phần
cho audio, mỗi dòng `N. [<tiêu đề slide N trong slide-script.md>] — <nội dung NGUỒN đầy
đủ của phần đó: khái niệm, ví dụ, số liệu, thao tác>`. Nguồn: đã tick sẵn đúng
source_ids của bài trước khi gửi prompt.

**Nguyên tắc:** slide (TEMPLATE 1) nén nguồn thành bullet; audio (TEMPLATE 2) giảng
ĐẦY ĐỦ nội dung nguồn, chỉ mượn TIÊU ĐỀ từ `slide-script.md` làm mốc đồng bộ. Audio phải
giàu hơn slide, không đọc lại bullet.

**Sau khi gửi TEMPLATE 1, ghi ngay `slide-script.md`** (định dạng ở SKILL.md) từ chính
`{{DÀN_Ý}}` vừa gửi. Từ đó trở đi mọi bước đọc file này, không mở lại PDF.

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

QUAN TRỌNG — nội dung lời giảng lấy TRỰC TIẾP & ĐẦY ĐỦ TỪ NGUỒN (chi tiết, ví dụ,
số liệu, thao tác — sâu hơn hẳn gạch đầu dòng trên slide). Slide chỉ là KHUNG đồng bộ.

Chia lời giảng thành ĐÚNG {{N}} đoạn, ĐÚNG thứ tự dưới đây, khớp 1-1 với {{N}} slide.
Ở đầu mỗi đoạn, XƯỚNG RÕ số và TIÊU ĐỀ SLIDE THẬT (ví dụ: "Phần 4 — <tiêu đề slide
thật>") để người nghe lật đúng slide. Mỗi đoạn giảng ĐẦY ĐỦ nội dung nguồn thuộc
phần đó, KHÔNG chỉ đọc lại bullet slide, KHÔNG lan sang phần khác.

Khung {{N}} phần — [Tiêu đề slide thật để xướng] ⇐ nội dung NGUỒN để khai triển:
{{DÀN_Ý_NGUỒN}}

Giọng: người dẫn giảng bài rõ ràng, mạch lạc, sư phạm. Ngôn ngữ: tiếng Việt.
```

## Checklist tự kiểm trước khi gửi TEMPLATE 2

- [ ] Nội dung mỗi đoạn KHAI TRIỂN từ nguồn (đầy đủ ví dụ/số liệu/thao tác), KHÔNG chỉ đọc lại bullet slide
- [ ] Số đoạn == số slide thật (không phải N kế hoạch nếu NLM đã gộp); callout đầu đoạn == TIÊU ĐỀ SLIDE THẬT, đúng thứ tự
- [ ] `language=vi` đã set
