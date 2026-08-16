---
name: md-to-epub
description: >-
  Convert any Markdown file to EPUB via pandoc, rendering mermaid diagrams to
  embedded PNG images entirely offline. Handles IPARAG YAML frontmatter that
  breaks pandoc's YAML parser, counts hidden HTML comments before they ship
  inside the EPUB, and verifies the built file by reopening it as a zip. Use for
  books, project reports, KHCN proposals, or any long Markdown deliverable that
  needs to be read on a tablet or e-reader. Triggers on: "convert to epub",
  "markdown to epub", "make an ebook", "xuất file epub", "chuyển sang epub",
  "tạo ebook", "đóng sách điện tử", "md to epub".
---

Chuyển một tệp Markdown thành EPUB, có dựng sơ đồ mermaid.

Cách gọi: `/md-to-epub <đường-dẫn.md>`

## Chạy

Toàn bộ logic nằm ở `scripts/md_to_epub.py` — gọi thẳng, đừng dựng lại bằng tay:

```bash
python D:/KN-Stack/scripts/md_to_epub.py "<input.md>" -o "<output.epub>"
```

Cờ có sẵn:

| Cờ | Dùng khi |
|---|---|
| `-o <path>` | Đặt nơi ra. Bỏ trống thì cùng thư mục, cùng tên, đuôi `.epub` |
| `--title` `--author` `--lang` | Ghi đè metadata. Không đặt thì title lấy từ H1 đầu tiên, `--lang` mặc định `vi` |
| `--strip-comments` | Gỡ hết chú thích HTML ẩn khỏi bản xuất |
| `--split-level N` | Cấp tiêu đề dùng để tách tệp và làm mục lục. Mặc định 2 (H1 = phần, H2 = chương) |
| `--scale N` | Độ phân giải sơ đồ, mặc định 3. Hạ xuống 2 nếu tệp quá nặng |
| `--no-diagrams` | Máy không có `mmdc`. Sơ đồ sẽ hiện ra chữ trần — chỉ dùng khi chấp nhận điều đó |

Nếu không có đường dẫn trong `$ARGUMENTS`, hỏi người dùng cần chuyển tệp nào.

## Bốn điều script làm mà pandoc trần không làm

1. **Sơ đồ mermaid.** Pandoc không dựng mermaid — nó đổ nguyên mã nguồn ra thành khối chữ, và trình đọc EPUB không chạy JavaScript nên chẳng có gì dựng chúng lên. Script tách khối mermaid, dựng bằng `mmdc` thành PNG, rồi nhúng vào.
2. **Frontmatter IPARAG.** `tags: [#type/book]` — dấu `#` mở comment YAML ngay giữa flow sequence nên chuỗi không bao giờ đóng, pandoc chết với *"did not find expected node content"*. Script tự bóc frontmatter trước khi giao cho pandoc.
3. **Chú thích ẩn.** EPUB là tệp zip chứa HTML: mọi `<!-- ... -->` đi thẳng vào bản xuất và ai giải nén cũng đọc được. Script đếm và báo số lượng.
4. **Nghiệm thu.** Mở lại EPUB như zip, đối chiếu số ảnh với số thẻ `<img>`, đếm tham chiếu gãy và sơ đồ còn sót. Sai thì thoát khác 0 — không giao file hỏng mà tưởng xong.

## An ninh — ràng buộc cứng

Sơ đồ dựng **offline tuyệt đối**. Script không gọi kroki.io, mermaid.ink hay bất kỳ dịch vụ web nào, và không được sửa thành như vậy. Tài liệu nội bộ Xưởng không rời máy. Đây là ràng buộc kiến trúc, không phải tùy chọn.

## Đọc bảng nghiệm thu

Script in một bảng cuối lượt chạy. Ba dòng cần nhìn:

- **`tham chieu gay`** phải bằng 0. Khác 0 nghĩa là có thẻ `<img>` trỏ vào ảnh không nằm trong tệp — người đọc sẽ thấy ô trống.
- **`mermaid sot`** phải bằng 0 (trừ khi cố tình dùng `--no-diagrams`). Khác 0 là sơ đồ lọt ra dạng chữ trần.
- **`chu thich an`** — nếu khác 0 thì nói rõ con số đó với người dùng trước khi họ gửi tệp đi đâu. Đừng tự ý gỡ; mặc định là giữ, vì tự sửa nội dung tài liệu nguy hiểm hơn là để người ta thấy con số rồi tự quyết.

## Khi thiếu công cụ

- Thiếu pandoc → `winget install JohnMacFarlane.Pandoc`
- Thiếu `mmdc` → `npm install -g @mermaid-js/mermaid-cli`, hoặc trỏ biến môi trường `MMDC_BIN` tới bản đã cài, hoặc chạy `--no-diagrams` nếu chấp nhận mất sơ đồ.
- Chỉ tài liệu **có** mermaid mới cần `mmdc`. Không có sơ đồ thì không cần Node.

## Giới hạn đã biết

- Sơ đồ dọc nhiều tầng (kiểu flowchart 8 bậc) dựng đúng nhưng trên điện thoại sẽ co vừa bề ngang, chữ nhỏ, phải chạm để phóng. Muốn đọc thoải mái thì tách sơ đồ trong nguồn, không phải chỉnh ở đây.
- Ảnh ra dạng PNG, không phải SVG — đổi lấy độ tương thích với trình đọc cũ.
- Không xử lý: LaTeX, sơ đồ dạng khác mermaid (PlantUML, graphviz).

## Kiểm hồi quy

`python D:/KN-Stack/scripts/test_md_to_epub.py` — 23 phép thử, tự sinh fixture, không cần mạng. Cần `MMDC_BIN` hoặc `mmdc` trên PATH.

Việc chuyển định dạng là **Offload** (COD): máy làm, người chỉ quyết có gửi đi hay không.
