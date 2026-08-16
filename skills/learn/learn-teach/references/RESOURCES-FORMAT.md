# Định Dạng RESOURCES.md

`RESOURCES.md` là tập hợp các nguồn đáng tin được tuyển chọn cho chủ đề này. Kiến thức cho các phần giải thích phải được lấy từ đây, không phải từ đoán mò tham số. Trí tuệ thực tiễn đến từ các cộng đồng được liệt kê ở đây.

File này là **đầu ra của pha S0** trong [SOURCING.md](./SOURCING.md) — nó chỉ được ghi sau khi người dùng đã qua cổng duyệt nguồn.

## Cấu Trúc

```md
# Tài Nguyên {Chủ Đề}

**Notebook NLM:** `learn-{slug}` — `{notebook-id}`
**Cập nhật nguồn lần cuối:** {YYYY-MM-DD}
**Trọng tài độ tươi:** [{nguồn sống của nhà sản xuất}]({url}) — phân xử mọi câu hỏi "hiện tại đúng là gì"

Hạng: tin cậy **S/A/B/C** (chuẩn · thẩm quyền · chuyên nghiệp · cộng đồng)
× sư phạm **E1/E2/E3** (giảng được · tra được · mồi được).

## Kiến Thức

### {Vùng kiến thức 1 — bám gạch đầu dòng trong MISSION.md}

- [Sách: _The Science and Practice of Strength Training_ — Zatsiorsky & Kraemer](https://example.com) — **B · E1**
  Tài liệu nền tảng về lập trình và thích ứng. Dùng cho: mọi thứ liên quan đến chu kỳ hóa, phục hồi, vùng cường độ.
- [Bài viết: "How Much Should I Train?" — Greg Nuckols (Stronger By Science)](https://example.com) — **B · E1**
  Đánh giá dựa trên bằng chứng về các mốc khối lượng. Dùng cho: mục tiêu số set hàng tuần theo nhóm cơ.
- [Meta-analysis: Schoenfeld et al., _J Sports Sci_ 2017](https://example.com) — **S · E2**
  Số liệu gốc về quan hệ khối lượng–phì đại. Dùng cho: chốt mọi con số trích từ hai nguồn trên.
- [Trang hướng dẫn chính thức của {nhà sản xuất}](https://example.com) — **A · E1** ⏱ kiểm 2026-08-14
  Mang sự thật dễ trôi (gói, nền tảng, giới hạn). Đánh dấu ⏱ + ngày kiểm; hết hạn thì không được trích số.

## Trí Tuệ Thực Tiễn (Cộng Đồng)

- [r/weightroom](https://reddit.com/r/weightroom) — **C · E3**
  Subreddit tín hiệu cao, được kiểm duyệt chống lại bro-science. Dùng cho: phê bình chương trình, giải quyết bình nguyên.
- Tại chỗ: Lớp sức mạnh thứ Ba tại {tên phòng tập} — **E3**
  Dùng cho: phản hồi huấn luyện trực tiếp về các động tác.

## Khoảng Trống

- {Vùng kiến thức chưa có nguồn E1 — chưa dạy được, chỉ tra được}
- {Vùng chưa có nguồn S/A — chưa chốt số được}
- {Mâu thuẫn chưa giải quyết giữa hai nguồn, kèm hướng xử lý}
```

## Quy Tắc

- **Chỉ đáng tin cao.** Ưu tiên nguồn gốc, chuyên gia được công nhận, công trình được đánh giá ngang hàng và cộng đồng có kiểm duyệt mạnh. Nếu một tài nguyên là marketing được mặc áo giáo dục, hãy bỏ qua.
- **Chấm đủ hai trục cho mọi mục.** Tin cậy (S/A/B/C) và sư phạm (E1/E2/E3) là hai câu hỏi khác nhau: "tin được không" và "dạy được không". Chấm thiếu một trục là lỗi thường gặp nhất — một chuẩn Tier S có thể hoàn toàn không dạy được cho người mới. Chấm E bằng cách mở nguồn ra đọc, đừng đoán từ tên miền. Chi tiết ở [SOURCING.md](./SOURCING.md).
- **Đánh dấu ⏱ + ngày kiểm cho nguồn mang sự thật dễ trôi** (gói, giá, nền tảng, giới hạn số, các bước thao tác). Hai trục chấm nguồn, không chấm việc nguồn còn đúng hay không — một nguồn `A · E1` vẫn có thể đang nói sai hiện trạng. Nguồn không có ngày kiểm thì không được trích số, ngày tháng hay thao tác.
- **Ghi phần `## Đã Loại Bỏ` khi cắt nguồn vì đã cũ**, kèm một dòng nói nó sai chỗ nào so với hiện tại. Không có phần này thì vòng S0 sau sẽ tìm lại đúng những nguồn đó và đưa vào lần nữa.
- **Nhóm theo vùng kiến thức của mission**, không phải theo loại nguồn. Mỗi vùng phải có ≥1 nguồn **E1** và ≥1 nguồn **S/A** — thiếu thì ghi vào `## Khoảng Trống`, đừng lặng lẽ dạy qua.
- **Chú thích mọi mục.** Một link trơ sẽ vô dụng sau ba tháng. Thêm một dòng: nó bao quát gì và khi nào cần dùng đến.
- **Nhóm theo Kiến Thức / Trí Tuệ Thực Tiễn.** Phản ánh triết lý trong [SKILL.md](../SKILL.md). Một tài nguyên chỉ xuất hiện trong một nhóm là ổn.
- **Nêu rõ các khoảng trống.** Nếu không có tài nguyên tốt cho một lĩnh vực mission cần, viết phần `## Khoảng Trống` liệt kê những gì còn thiếu. Điều này thúc đẩy tìm kiếm trong tương lai. Khoảng trống là thứ để đọc trước khi soạn bài, không phải để dọn dẹp cho gọn file — một vùng nằm trong Khoảng Trống thì chưa được viết bài học.
- **Cắt tỉa quyết đoán.** Tài nguyên hóa ra sai, nông cạn hoặc lạc khỏi mission nên được xóa, không phải chôn vùi. Năm nguồn sắc nét tốt hơn ba mươi nguồn tầm thường.
- **Ghi lại sở thích về cộng đồng.** Nếu người dùng không muốn tham gia cộng đồng, ghi chú ở đây để các phiên sau không tiếp tục đề xuất.
