---
name: helix-cc2-handoff
description: "Khối C6 của bộ helix-cc2 — đọc phương án đi tiếp CEO ghi ở Cổng CEO 3, chạy lại lint phiếu C4 không cờ, cắt bản trích C0 + C2/C3 của đúng phương án ấy rồi gọi CA đối chiếu ngược trong một tác tử con mới (--crosscheck), gộp danh sách lệch thành CC2_C6_Crosscheck.md (mỗi chỗ lệch một phiếu nháp GT-nnn hoặc một dòng sửa C2), nối mục đối chiếu ngược vào CC2_CA_Analysis.md, và — chỉ khi có thư mục dự án — viết bàn giao P3 CC2_Handoff.md vào Phase3-Embodiment/ cho helix-embody-realize và helix-p3-layout, kèm vòng lặp P3 đối chiếu mức hình học trên cad_extract.json. Triggers on: 'C&C2 handoff', 'handoff to embodiment', 'cross-check form variant', 'back-check embodiment', 'P3 handoff', 'bàn giao P3', 'đối chiếu ngược', 'bàn giao C&C2', 'chuyển sang thiết kế hiện thân', 'helix-cc2-handoff'."
---

# helix-cc2-handoff — Khối C6: đối chiếu ngược + bàn giao P3

> **Vai:** khối cuối, sau Cổng CEO 3. Cho một người đọc khác người lập soi lại phương án đi tiếp, rồi gói kết quả C0–C4 thành
> một tệp P3 đọc được. Không chọn phương án, không ký phiếu, không sửa C2 thay CEO.
> **Đầu vào:** `{{prefix}}CC2_C0_Frame.md` (ở **gốc** nơi ghi), `{{prefix}}CC2_C2_Forms.md`, `{{prefix}}CC2_C3_Params.md`,
> `{{prefix}}CC2_C4_Hypotheses.md`, `{{prefix}}CC2_C4_Test_Plan.md`, `{{prefix}}CC2_CA_Analysis.md` (nếu có), `_pipeline_state.md` |
> **Đầu ra:** `{{prefix}}CC2_C6_Crosscheck.md`, `{{prefix}}CC2_Handoff.md` (chỉ khi có thư mục dự án), mục nối vào
> `{{prefix}}CC2_CA_Analysis.md` | **Đọc bởi:** CEO; Handoff: `helix-embody-realize`, `helix-p3-layout`
> **Nguồn dùng chung:** `helix-cc2:references:hypothesis-sheet` (§Khuôn phiếu, §Điều kiện hợp lệ, §Định tuyến độ tin × tầm ảnh
> hưởng), `helix-cc2:references:param-bridge` (§Dải đã kiểm), `helix-cc2:references:multidomain` (§Chỗ phải dừng),
> `helix-cc2:references:cc2-core` (§Giới hạn dùng và bằng chứng).

## Đầu vào

- Bắt buộc: mọi tệp ở dòng **Đầu vào** trên, trừ CA. Thiếu tệp nào → liệt kê tệp thiếu và dừng; không dựng giả tệp thượng
  nguồn (`--from <khối ghi>` để chạy lại khối ghi tệp đó).
- **Phương án đi tiếp** của từng chức năng con: đọc ở bảng Cổng CEO của `_pipeline_state.md`, hàng Cổng CEO 3, dạng
  `phương án đi tiếp: A-1`. CEO ghi ô này lúc ký dự đoán; C6 chỉ đọc.
- Chế độ dự án: chạy theo từng `F-id`; đọc C2, C3, C4, CA và ghi `CC2_C6_Crosscheck.md` trong `<nơi ghi>/<F-id>/`, đọc C0 ở
  gốc `<nơi ghi>/`. Chức năng con ở ô `chỉ bảng tham số` không có đối chiếu ngược; bảng C3 của nó vào thẳng Handoff.
- Chế độ `--analyze` không có C6 (luồng ấy chỉ có CA, có thể nối C4).

## Luật cứng

1. **Không chọn phương án.** C6 chỉ đối chiếu phương án CEO đã ghi; các phương án khác của C2 không vào bản trích, không vào
   Handoff.
2. **Người đọc ≠ người lập.** CA chạy trong một tác tử con mới, không mang ngữ cảnh phiên lập C1–C4, chỉ nhận thư mục trích, mã
   phương án và số GT kế tiếp. Không đưa C1, C4 hay lý lẽ chọn chuỗi vào thư mục trích.
3. **Không bàn giao khi phiếu chưa sạch.** Lint không cờ trên C4 phải ra mã 0 ngay trong lượt C6, kể cả khi C4 đã ghi `lint 0`
   trước đó; phiếu có thể đã bị sửa sau cổng.
4. **Mỗi chỗ lệch đúng một xử lý:** `phiếu nháp GT-nnn` hoặc `dòng sửa C2: …`, như CA trả về. C6 không gộp, không bỏ dòng
   lệch nào; dòng sửa C2 chờ CEO quyết, C6 không tự sửa `{{prefix}}CC2_C2_Forms.md`.
5. **Mức đối chiếu là mô tả.** Crosscheck và Handoff đều ghi ở đầu tệp `Mức đối chiếu: mô tả (chưa có hình học)`. Đối chiếu
   mức hình học chỉ có ở vòng lặp P3, khi đã có `cad_extract.json`.
6. **Nơi ghi Handoff.** `{{prefix}}CC2_Handoff.md` ghi vào `Phase3-Embodiment/` (hoặc `Phase3-Embodiment/<biến thể>/`), là chỗ P3 đọc; không ghi vào `<nơi ghi>` (mặc định `Phase3-Embodiment/CC2/`). Chế độ dự án gộp mọi chức năng con vào một tệp.
7. **Chỉ trong dự án.** «Trong dự án» đúng như orchestrator định nghĩa ở nơi ghi và tiền tố: chế độ `--project`, hoặc thư mục làm việc là gốc một dự án có `Phase3-Embodiment/`.
   Ngoài dự án thì không có Handoff (bước 7).
8. Không thêm số: Handoff chép khoảng chọn, nhãn và nguồn số từ C3 nguyên dạng; không ngoại suy ra ngoài dải đã kiểm
   (`param-bridge` §Dải đã kiểm), không đổi nhãn `phỏng đoán` thành `tri thức`.

## Bước

1. **Đọc phương án đi tiếp** của chức năng con hiện hành (`current_f` ở chế độ dự án) trong bảng Cổng CEO.
   Thiếu phương án đi tiếp (không có hàng Cổng CEO 3, hoặc hàng ấy không có `phương án đi tiếp: <X-n>`) → in các phương án có trong C2, dừng, hỏi CEO; không tự chọn, kể cả khi C2 chỉ có một phương án.
   Mã phương án không có trong C2 → dừng, hỏi CEO.
2. **Chạy lại lint không cờ** trên phiếu C4 (cùng lệnh C4 chạy sau khi CEO ký, không dùng cờ bỏ qua chữ ký):

   ```
   python D:/KN-Stack/scripts/cc2_sheet_lint.py {{prefix}}CC2_C4_Hypotheses.md --kind hypo
   ```

   Exit ≠ 0 → dừng, không sinh bàn giao; in nguyên output và mã thoát, báo CEO (PRED_UNSIGNED thì CEO ký; mã khác thì
   `--from C4`). Luật cứng: báo cáo "đã kiểm" không thay output của lệnh.
3. **Cắt bản trích** vào một thư mục nháp mới ngoài `<nơi ghi>` (vd. thư mục tạm của phiên, tên `cc2_trich_<F-id>_<X-n>/`),
   tên tệp không tiền tố. Chép đúng phần cần, bỏ frontmatter và mọi câu nhắc lý do chọn chuỗi.
   Bản trích:
   - `<thư mục trích>/CC2_C0_Frame.md`: chỉ khung của chức năng con đang xét (thông số chức năng, Connector biên, ràng buộc môi trường)
   - `<thư mục trích>/CC2_C2_Forms.md`: chỉ mục của phương án `<X-n>` (mô tả, phác, bảng quy tắc)
   - `<thư mục trích>/CC2_C3_Params.md`: chỉ bảng của phương án `<X-n>`

4. **Tính số GT kế tiếp** `<n>` = số GT lớn nhất trong `{{prefix}}CC2_C4_Hypotheses.md` của chức năng con (và trong
   `{{prefix}}CC2_C6_Crosscheck.md` cũ nếu chạy lại) cộng 1.
5. **Mở một tác tử con mới**, không mang ngữ cảnh phiên này, chỉ truyền ba tham số, rồi chờ nó xong:

   ```
   /helix-cc2-analyze --crosscheck <thư mục trích> <X-n> <n>
   ```

   Không trả lời câu hỏi của tác tử con bằng thông tin ngoài thư mục trích; thiếu thì để nó ghi `chưa rõ`.
6. **Đọc lại và gộp.** Đọc `<thư mục trích>/CA_Crosscheck_<X-n>.md`. Không có tệp, hoặc tệp không có bảng lệch có cột
   `Xử lý` → dừng, báo CEO; không tự dựng bảng lệch.
   - Chép bảng lệch và phiếu nháp vào `{{prefix}}CC2_C6_Crosscheck.md` theo khuôn dưới.
   - Nối nguyên mục `## Đối chiếu ngược — phương án <X-n>` của tệp ấy vào cuối `{{prefix}}CC2_CA_Analysis.md` (tạo tệp
     nếu chưa có, với frontmatter `f_id` và `hình thể: phương án <X-n> (mô tả C2)`). Không ghi đè mục cũ; chạy lại thì thêm
     ngày vào tiêu đề mục mới.
   - Có phiếu nháp thì kiểm khuôn (phiếu nháp chưa ký nên dùng `--allow-unsigned`; mọi mã khác vẫn chặn):

     ```
     python D:/KN-Stack/scripts/cc2_sheet_lint.py {{prefix}}CC2_C6_Crosscheck.md --kind hypo --allow-unsigned
     ```

     Exit ≠ 0 → không sinh bàn giao; báo CEO dòng lỗi. Không có phiếu nháp thì không chạy lệnh này (nó ra `NO_SHEETS`).
7. **Kiểm thư mục dự án** theo luật 7. Ngoài dự án: dừng ở `{{prefix}}CC2_C6_Crosscheck.md` + `{{prefix}}CC2_C4_Test_Plan.md`, in «không sinh bàn giao P3 vì không có thư mục dự án», cập nhật trạng thái, xong.
8. **Viết Handoff** (trong dự án). Chế độ dự án: chỉ viết khi mọi chức năng con ở ô `dựng C&C²` đã qua bước 1–6; còn thiếu
   thì in danh sách `F-id` còn thiếu và chưa viết. Chạy lại C6 cho một `F-id` thì viết lại cả tệp từ các tệp hiện có.
9. Cập nhật cột C6 của `_pipeline_state.md` (`✓ lệch <số> · GT mới <số>` hoặc lý do dừng), in tóm tắt 3–5 dòng (số chỗ lệch,
   số phiếu nháp, dòng sửa C2 chờ CEO, ngày thử sớm nhất, đường dẫn Handoff hoặc lý do không sinh), hỏi CEO «tiếp / sửa / dừng».
   Duyệt bàn giao là việc của CEO.

## Khuôn đầu ra: `{{prefix}}CC2_C6_Crosscheck.md`

````markdown
---
updated: YYYY-MM-DD
f_id: {{F-id hoặc —}}
phương án: {{X-n}}
---
# CC2 C6 — Đối chiếu ngược: phương án {{X-n}} — {{chức năng}}

> Mức đối chiếu: mô tả (chưa có hình học)
> Người đối chiếu: tác tử con mới, chỉ đọc bản trích C0 + C2/C3 của {{X-n}}. Lint C4 không cờ: mã {{0}}.

## Bảng lệch
| Lệch | Loại | Thấy ở | Xử lý |
|---|---|---|---|
| {{mô tả}} | {{L1–L5}} | {{X-n:phần tử (trạng thái)}} | {{phiếu nháp GT-nnn: … / dòng sửa C2: …}} |

## Phiếu nháp
(khối text theo hypothesis-sheet §Khuôn phiếu, đánh số từ {{n}}, mục 7 để trống cho CEO | không có)

## Dòng sửa C2 chờ CEO
- {{dòng sửa C2: …}} — {{chờ / CEO nhận / CEO bỏ}}
````

## Khuôn đầu ra: `{{prefix}}CC2_Handoff.md`

````markdown
---
updated: YYYY-MM-DD
dự án: {{dự án / biến thể}}
nguồn: {{<nơi ghi>}}
---
# CC2 Handoff → P3 — {{dự án}}

> Mức đối chiếu: mô tả (chưa có hình học)
> Mọi quan hệ hình thể → chức năng dưới đây là giả thuyết có nhãn cho tới khi qua bàn thử. Không phải đáp án.

## Chuỗi đã chọn theo chức năng con
| Chức năng con | Chuỗi chọn | Phương án đi tiếp | Một dòng mô tả (từ C2) | Ngày Cổng CEO 3 |
|---|---|---|---|---|

## Tham số hình thể và khoảng chọn
(bảng C3 của phương án đi tiếp, mỗi chức năng con một bảng; giữ các cột Phần tử, Tham số hình thể, Thông số chức năng,
Khoảng chọn, Nhãn, Nguồn số; chức năng con ở ô `chỉ bảng tham số` cũng vào đây)

## Tham số nhạy
| Chức năng con | Dòng C3 | Sai lệch tới hạn | Phiếu |
|---|---|---|---|

## Phiếu giả thuyết đang mở
| Phiếu | Chức năng con | Dòng C3 | Trạng thái | Đường | Ngày thử |
|---|---|---|---|---|---|
(trạng thái: `đã ký, chờ thử` cho phiếu C4; `nháp từ đối chiếu ngược, chưa ký` cho phiếu C6 — chưa có hàng thử, CEO quyết
đưa vào C4; kèm số dòng sửa C2 còn chờ)

## Kế hoạch thử
(trỏ `{{prefix}}CC2_C4_Test_Plan.md` của từng chức năng con; chép thứ tự, phiếu, ngày thử, người đọc kết quả; ngày thử sớm nhất)

## Chỗ C&C² không áp dụng
(chức năng con ở ô `không áp dụng` của C0 kèm lý do; chỗ dừng theo multidomain §Chỗ phải dừng; dòng NHẠY chưa có mô hình)

## Vòng lặp P3
Khi BA hay `helix-cad-bridge` có `cad_extract.json` cho phần mang các tham số trên, chạy
`/helix-cc2 --analyze <cad_extract.json>` để đối chiếu mức hình học. Lệch mới thành phiếu hoặc dòng sửa C2 như ở C6; đổi một
khoảng ở bảng trên thì mở hoặc sửa phiếu tương ứng, không tự chọn lại.
````

## Ví dụ ngắn (nắp gài bằng móc đàn hồi, tiếp ví dụ C3/C4; chế độ `--function`, số và ngày là minh hoạ)

**Phương án đi tiếp.** Hàng Cổng CEO 3 trong `_pipeline_state.md`:

| Cổng | Ngày | Quyết định | Lý do |
|---|---|---|---|
| 3 ký dự đoán | 2026-10-20 | đã ký GT-001…GT-003; phương án đi tiếp: A-1 | một cần, ít dung sai chặt hơn A-2 |

**Lint lại C4:** lệnh không cờ ra mã 0. **Số GT kế tiếp:** C4 có GT-001…GT-003 nên `<n>` = 4.

**Gọi CA** trong tác tử con mới: `/helix-cc2-analyze --crosscheck <thư mục trích> A-1 4`. Bảng lệch đọc lại từ
`CA_Crosscheck_A-1.md` (ba dòng như ví dụ `--crosscheck` của `helix-cc2-analyze`):

| Lệch | Loại | Thấy ở | Xử lý |
|---|---|---|---|
| Gờ trên thân hộp mỏng, có thể uốn cùng móc khi gài — một LSS thứ hai | L1 | A-1:gờ thân hộp (LSS, S2 gài) | phiếu nháp GT-004: bề dày gờ thân hộp, đối chứng gờ dày hơn, THÌ lực đóng |
| Phác A-1 không ghi khe giữa móc và vách nắp ở trạng thái gài | L2 | A-1:móc//gờ (S2 gài) | dòng sửa C2: ghi khe móc–vách ở S2 vào phác A-1 |
| C0 có Connector ngón tay tháo nắp, phác không chừa chỗ đặt ngón | L4 | C0 Connector biên | dòng sửa C2: thêm mặt đặt ngón ở mép nắp vào phương án A-1 |

**Không có thư mục dự án** (chạy từ `./_cc2/nap-gai-moc-dan-hoi/`): C6 ghi Crosscheck, nối mục vào CA, rồi in
«không sinh bàn giao P3 vì không có thư mục dự án».

**Nếu chạy trong dự án**, Handoff có ở `## Tham số nhạy` ba dòng (góc mặt vào, góc mặt rút, chiều dài cần → GT-001…GT-003),
ở `## Phiếu giả thuyết đang mở` ba phiếu `đã ký, chờ thử` và GT-004 `nháp từ đối chiếu ngược, chưa ký`, kèm 2 dòng sửa C2 chờ
CEO; ngày thử sớm nhất 2026-11-18 (GT-003).

## Chạy riêng

```
/helix-cc2-handoff [--out <thư mục>]
```

Đầu vào tối thiểu: C0 ở gốc nơi ghi, C2, C3, C4 (đã ký, lint không cờ mã 0) và hàng Cổng CEO 3 có phương án đi tiếp trong
`_pipeline_state.md`. Chế độ dự án: truyền `--out <nơi ghi>/<F-id>` hoặc để C6 đọc `current_f`; Handoff vẫn ghi vào
`Phase3-Embodiment/`.

## COD

| Việc | Lớp | Ai |
|---|---|---|
| Cắt bản trích, gộp bảng lệch, viết Crosscheck và Handoff | **O** Offload | AI |
| Đối chiếu ngược `--crosscheck` | **O** Offload | tác tử con mới, khác người lập C1–C4 |
| Chọn phương án đi tiếp (ở Cổng CEO 3), nhận hay bỏ dòng sửa C2, ký phiếu nháp mới, duyệt bàn giao P3 | **C** Core | CEO / kỹ sư — AI không chọn, không ký |
| Chạy `cc2_sheet_lint`, cập nhật `_pipeline_state.md` | **D** Default | tự động |
