# Khuôn `RE_<SP>_Book_GapFill.md`

> Dùng ở `--gapfill` của `/re-to-book`. Đặt tại `RE/<hồ sơ>/RE_<SP>_Book_GapFill.md`; chỗ trống liên miền
> (không thuộc một sản phẩm) ⇒ đặt trong hồ sơ TECH (`RE/TECH_<…>/`). Đây là tệp duy nhất của hồ sơ RE mà
> `/re-to-book` được ghi.

## Cách manifest đọc tệp này (`re_manifest.py build`)

| Trạng thái | Điều kiện (khớp bằng máy) | Lớp |
|---|---|---|
| Duyệt cả tệp | frontmatter có dòng `status:` chứa `đã duyệt` | READ (cả tệp) |
| Duyệt từng mục | một số mục `## GF-NNN` có dòng `**Trạng thái:** đã duyệt` | READ (chỉ các mục đã duyệt; mục khác bị bỏ khỏi bản chụp) |
| Chưa duyệt gì | không có hai điều kiện trên | BLOCK |

Chữ phải đúng nguyên văn (có dấu): `đã duyệt`. Chỉ CEO đổi trạng thái — tác tử luôn ghi `chờ CEO duyệt`.

## Khuôn

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: re-gapfill
product: <SP>
book: <RE-project>/Book
status: chờ CEO duyệt
---

# GapFill cho sách — <SP>

> Ghi bởi `/re-to-book --gapfill`. Không sửa phân tích RE khác. CEO duyệt từng mục hoặc cả tệp.

## GF-001 <tên chỗ trống ngắn>

**Trạng thái:** chờ CEO duyệt
**Chỗ trống:** `<hồ sơ>/<tệp>#<mã đơn vị>` (lấy từ `## Chỗ trống RE tự khai` / `_re_gaps.md`)
**Tìm thấy:** <tóm bằng lời mình, không chép dài nguồn>
**Nguồn:** <tiêu đề · URL/mã sáng chế · trang> — bản tải: `_source/gapfill/<ngày>_<chủ đề>/<tệp>`
**Kênh:** Exa | NLM (`sources_used`/`references` ≠ 0/0) | sổ tay hãng | sáng chế
**Nhãn tri thức đề xuất:** knowledge | phỏng đoán | giả định
**Mức tin đề xuất:** L | M | H
**Còn mở:** <điều nguồn chưa trả lời>

## GF-002 …
```

## Luật

- Mỗi lần tải nguồn ⇒ **một thư mục mới** `_source/gapfill/<ngày>_<chủ đề>/`; đọc tệp tải về bằng `python -I`.
- Truy vấn NLM trả `0/0` ⇒ không ghi thành mục GF (cổng `0/0` của `/notebook-to-book`).
- Nhãn đề xuất dùng đúng từ vựng `re_labels.py` (`đã biết`/`tri thức`, `phỏng đoán`, `giả định`) để manifest gán được nhãn.
- Không ghi giá nhà cung cấp, không ghi dữ liệu mật.
