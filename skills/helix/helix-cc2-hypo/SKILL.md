---
name: helix-cc2-hypo
description: "Khối C4 của bộ helix-cc2 — lấy đúng các dòng NHẠY của bảng tham số C3 (hoặc giả thuyết nháp của CA ở chế độ --analyze), viết mỗi dòng một PHIẾU GIẢ THUYẾT 9 mục theo khuôn hypothesis-sheet (NẾU là tham số ghi được lên bản vẽ, đổi đúng một biến, có đối chứng, VÌ một cơ chế), thêm dòng «Phép thử nhỏ nhất để bác bỏ» cho từng phiếu, rồi lập kế hoạch thử trên bàn thử một hàng mỗi phiếu, xếp theo định tuyến độ tin × tầm ảnh hưởng. Mục 7 để trống cho CEO ký; lint --allow-unsigned trước Cổng CEO 3, lint không cờ sau khi ký. Triggers on: 'hypothesis sheet', 'structural hypothesis', 'test bench plan', 'refutation test', 'C&C2 hypotheses', 'phiếu giả thuyết', 'kế hoạch thử trên bàn thử', 'phép thử bác bỏ', 'ký dự đoán', 'helix-cc2-hypo'."
---

# helix-cc2-hypo — Khối C4: phiếu giả thuyết 9 mục + kế hoạch thử trên bàn thử

> **Vai:** sau C3 (hoặc sau CA ở `--analyze`), trước C6. Biến mỗi tham số nhạy thành một phỏng đoán kiểm được, kèm phép
> thử rẻ nhất có thể bác nó, rồi xếp thứ tự thử. Không ký thay CEO.
> **Đầu vào:** `{{prefix}}CC2_C3_Params.md` (dòng `NHẠY`), `{{prefix}}CC2_C0_Frame.md` (thông số chức năng, ở **gốc** nơi ghi);
> chế độ `--analyze`: `{{prefix}}CC2_CA_Analysis.md` |
> **Đầu ra:** `{{prefix}}CC2_C4_Hypotheses.md`, `{{prefix}}CC2_C4_Test_Plan.md` | **Đọc bởi:** C6, CEO (ký dự đoán), bàn thử
> **Nguồn dùng chung:** `helix-cc2:references:hypothesis-sheet` (§Khuôn phiếu, §Điều kiện hợp lệ, §Khuôn kế hoạch thử trên
> bàn thử, §Định tuyến độ tin × tầm ảnh hưởng, §Phiếu mẫu đã điền), `helix-cc2:references:param-bridge` (§Khuôn bảng C3,
> §Độ nhạy và thứ hạng, §Dải đã kiểm), `helix-cc2:references:cc2-core` (§Hai loại nhãn), `helix-cc2:references:view-ops`
> (§Rào cản quan sát), `helix-cc2:references:multidomain` (§Chỗ phải dừng).

## Đầu vào

- Bắt buộc: `{{prefix}}CC2_C3_Params.md` và `{{prefix}}CC2_C0_Frame.md`. Thiếu tệp nào → liệt kê tệp thiếu và dừng; không
  dựng giả tệp thượng nguồn (`--from C3` hoặc `--from C0` để chạy lại khối ghi tệp đó).
- Chế độ `--analyze`: không có C3; C4 lấy mục `## Giả thuyết nháp` của `{{prefix}}CC2_CA_Analysis.md` làm đầu vào, mỗi phiếu nháp thành một phiếu C4, giữ nguyên mã GT nếu CA đã đánh; dòng truy ngược của mỗi phiếu là `Nguồn CA:` (dạng `Nguồn CA: <mục CA> · <đặc điểm hình học>`) thay cho `Dòng C3:` (không có C3 ở luồng này).
- Chế độ dự án: chạy theo từng `F-id`; đọc C3 và ghi C4 trong `<nơi ghi>/<F-id>/`, đọc C0 ở gốc `<nơi ghi>/`. Chức năng con
  ở ô `chỉ bảng tham số` dừng ở C3, không có phiếu.

## Luật cứng

1. **Chọn dòng.** NHẠY = ô "Chiều ảnh hưởng" bắt đầu bằng `NHẠY` (quy ước bộ skill); C4 lấy đúng các dòng này, không
   thêm, không bớt, không tự chấm lại độ nhạy. Dòng không `NHẠY` (kể cả dòng `tri thức`) không có phiếu.
2. **mỗi dòng `NHẠY` đúng một phiếu**, mã `GT-001`, `GT-002`… theo thứ tự dòng trong C3 (qua mọi phương án). Mỗi phiếu có
   dòng `Dòng C3: <Phần tử> · <Tham số hình thể>` chép đúng hai ô đầu của dòng C3, để C6 truy ngược được. Hai ngoại lệ:
   - VÌ cần hai cơ chế → tách hai phiếu, cả hai cùng một `Dòng C3:` (`hypothesis-sheet` §Điều kiện hợp lệ).
   - Không viết được VÌ → không lập phiếu; ghi dòng ấy vào `## Dòng NHẠY chưa có mô hình` kèm một câu vì sao, đề nghị
     CEO quay về phân tích (CA hoặc `--from C1`). Chưa có mô hình thì chưa lên bàn thử.
3. **Khuôn 9 mục** đúng `hypothesis-sheet` §Khuôn phiếu, mỗi phiếu một khối `text`:
   - Mục 2 (NẾU) là **tham số ghi được lên bản vẽ**, lấy từ cột *Tham số hình thể*, với **một** dấu `=` trước `|`; đối chứng
     chỉ khác đúng tham số ấy. Không đặt tác dụng (ma sát, mòn, độ kín, tín hiệu) ở mục 2, kể cả ở phần đối chứng.
   - Mục 3 (THÌ) là đại lượng chức năng đo được, lấy từ cột *Thông số chức năng*, ghi *so với* đối chứng.
   - Mục 4 (VÌ) đúng một cơ chế vật lý.
   - Mục 5 có `ngày thử: YYYY-MM-DD` (AI đề xuất, CEO đổi được trước khi ký) và tên người đọc kết quả ≠ người lập phiếu.
   - Mục 6 để `{{điền SAU}}`.
   - Mục 7: AI có thể nháp *nội dung* dự đoán, nhưng phần `người ký {{…}} — ngày {{…}}` để nguyên cho CEO/kỹ sư điền.
     **AI không điền chữ ký**, không điền tên, không điền ngày ký. Ngày ký phải trước ngày thử.
   - Mục 8 ghi hai nấc `thấp`/`trung`/`cao`, mỗi nấc một lý do trong ngoặc: độ tin trước, tầm ảnh hưởng sau. Phỏng đoán
     chạm an toàn con người ghi chữ `an toàn` ở mục 8.
   - Mục 9 ghi `lặp trong pha` hoặc `lặp xuyên cổng → mở lại quyết định <cổng nào>`.
4. **Phép thử nhỏ nhất để bác bỏ.** Mỗi phiếu thêm một dòng `Phép thử nhỏ nhất để bác bỏ: …` ngay sau mục 9: quan sát rẻ
   nhất, ít mẫu nhất, mà nếu thấy thì phiếu bị bác. Ghi rõ quan sát nào sẽ khác đi nếu giả thuyết sai. Phép này không lớn
   hơn mục 5; nếu không nghĩ ra phép nào rẻ hơn mục 5 thì chép tóm tắt mục 5 và ghi `(= mục 5)`.
5. **Không ngoại suy** ra ngoài dải đã kiểm của C3 (`param-bridge` §Dải đã kiểm); dải tham số và dải điều kiện biên ghi ở mục 5.
6. **Chỗ C&C² dừng.** Dòng `NHẠY` mà quan hệ nằm chủ yếu ở mạch điện tử hay phần mềm thì không lập phiếu C&C²; ghi câu khuôn
   của `multidomain` §Chỗ phải dừng và chuyển sang tài liệu của ngành đó.
7. Định tuyến kiểm được *(quy ước bộ skill)*, cụ thể hoá `hypothesis-sheet` §Định tuyến độ tin × tầm ảnh hưởng:
   - Đọc hai nấc ở mục 8. Nấc `trung` tính như `cao` ở trục tầm ảnh hưởng và như `thấp` ở trục độ tin (phía thận trọng).
   - Đường: tầm ảnh hưởng `cao`/`trung` → `3`; tầm `thấp` + độ tin `cao` → `1–2`; tầm `thấp` + độ tin `thấp`/`trung`
     → `2`; mục 8 có chữ `an toàn` → `3` bất kể trục. Đường 3 chỉ hạ xuống 2 khi CEO ký lý do trên phiếu.
   - Thứ tự hàng trong kế hoạch: (1) phiếu mở lại cổng (mục 9 ghi `lặp xuyên cổng`) lên trước, bất kể trục kia;
     (2) đường `3` → `2` → `1–2`; (3) tầm ảnh hưởng `cao` → `trung` → `thấp`; (4) độ tin `thấp` → `trung` → `cao`;
     (5) mã phiếu. Chế độ `--improve`: trong cùng nấc (1)–(4), chỗ đổi hình thể hay đổi nguyên lý trước, rồi phần mang
     sang đã chỉnh, rồi phần mang sang nguyên mà Connector đã đổi (`hypothesis-sheet` §Định tuyến độ tin × tầm ảnh hưởng).
8. **Kế hoạch thử: một hàng mỗi phiếu**, theo `hypothesis-sheet` §Khuôn kế hoạch thử trên bàn thử. Hàng đường `3` có
   *Loại thử* là `thực nghiệm` (đổi một tham số giữa các mẫu, nên không phải kiểm chứng). Hàng đường `2` ghi
   `lý giải nhóm có phản biện` kèm phép thử nhỏ nhất; hàng đường `1–2` ghi `dùng phỏng đoán, ghi nhãn`. *Ngày thử* của
   hàng trùng ngày thử ở mục 5 của phiếu. Đại lượng không đo được ở chỗ trong thì đo ở giao diện có sẵn; rào cản quan sát
   (quá nhanh, bị che…) ghi vào cột *Mẫu + đối chứng* cùng phép phá (`view-ops` §Rào cản quan sát).

## Bước

1. Đọc C3 (hoặc CA ở `--analyze`) và các thông số chức năng của C0. Lọc đúng các dòng `NHẠY` (luật 1).
2. Với mỗi dòng: viết phiếu 9 mục (luật 2–3), dòng `Dòng C3:` và dòng `Phép thử nhỏ nhất để bác bỏ:` (luật 4).
3. Tính đường và thứ tự từ mục 8, 9 (luật 7); lập `{{prefix}}CC2_C4_Test_Plan.md` một hàng mỗi phiếu (luật 8).
4. Ghi `{{prefix}}CC2_C4_Hypotheses.md` với mục 7 chưa ký, rồi chạy lượt lint trước cổng (bỏ qua đúng mã `PRED_UNSIGNED`,
   mọi mã khác vẫn chặn):

   ```
   python D:/KN-Stack/scripts/cc2_sheet_lint.py {{prefix}}CC2_C4_Hypotheses.md --kind hypo --allow-unsigned
   ```

   Exit ≠ 0 → sửa phiếu rồi chạy lại; chưa được trình CEO.
5. ⛔ **Cổng CEO 3 — ký dự đoán.** Trình phiếu và kế hoạch thử. CEO/kỹ sư đọc, sửa dự đoán nếu cần, rồi điền
   `người ký <tên> — ngày YYYY-MM-DD` ở mục 7 của từng phiếu, ngày ký trước ngày thử. AI không điền chữ ký thay.
   Ở cổng này CEO cũng ghi phương án đi tiếp `X-n` của chức năng con vào bảng Cổng CEO của `_pipeline_state.md`
   (dạng `phương án đi tiếp: A-1`); AI không chọn thay.
   Dừng. Không chạy bước 6 cho tới khi CEO báo đã ký; lint không cờ ra mã 1 với PRED_UNSIGNED thì báo CEO, không sửa mục 7.
   Tên người ký chứa placeholder hay chỉ AI (`{{`, `<`, chữ `AI` đứng riêng, `Claude`, `trợ lý`, `TBD`, `n/a`, `chưa ký`, hoặc đúng chữ `tên`; không phân biệt hoa thường) bị lint tính là chưa ký.
6. Sau khi CEO ký, chạy lượt lint không cờ:

   ```
   python D:/KN-Stack/scripts/cc2_sheet_lint.py {{prefix}}CC2_C4_Hypotheses.md --kind hypo
   ```

   Exit 0 → ghi tên — ngày ký vào cột *Ký dự đoán* và `lint 0` vào cột C4 của `_pipeline_state.md`; Cổng CEO 3 đóng.
   C6 chạy lại đúng lệnh không cờ này trước khi bàn giao.

## Mã thoát (cả hai lượt)

- Exit 0 → sạch cho lượt ấy.
- Exit 1 → còn mục thiếu (`MISSING_ITEM`, `NO_BECAUSE` — mục chỉ có nhãn như `4 VÌ:` cũng là trống; mục 7 không có dự
  đoán trước `người ký` cũng là thiếu), tác dụng ở mục 2 (`EFFECT_IN_IF`), hơn một biến (`IF_MULTI_VAR`), mục 2 không có
  `| Đối chứng:` (`NO_CONTROL`), thiếu ngày thử hay ngày ký không trước ngày thử (`PRED_NOT_BEFORE_TEST`), ngày ký sau hôm nay
  (`PRED_FUTURE_SIGN`), dòng giống tiêu đề phiếu mà không đúng dạng `PHIẾU GIẢ THUYẾT — GT-nnn` (`HEADER_UNPARSED`), không có
  phiếu nào (`NO_SHEETS`), hoặc — chỉ ở lượt không cờ — mục 7 chưa ký (`PRED_UNSIGNED`).
- Exit 2 → lỗi đọc tệp; dừng, báo CEO.
- Exit ≠ 0 ở lượt nào thì không đóng Cổng CEO 3 và không ghi `lint 0` vào `_pipeline_state.md`.
- Luật cứng: báo cáo "đã kiểm" không thay output của lệnh. In nguyên output lệnh và mã thoát vào tóm tắt khối; không có
  output thật thì chưa kiểm.

## Khuôn đầu ra: `{{prefix}}CC2_C4_Hypotheses.md`

````markdown
---
updated: YYYY-MM-DD
f_id: {{F-id hoặc —}}
nguồn: {{CC2_C3_Params.md | CC2_CA_Analysis.md (--analyze)}}
---
# CC2 C4 — Phiếu giả thuyết: {{chức năng}}

> Mọi phiếu là phỏng đoán cho tới khi qua bàn thử. Mục 7 do CEO/kỹ sư ký; AI không ký.

```text
PHIẾU GIẢ THUYẾT — GT-{{nnn}}
1 Tiêu đề: {{nnn}} {{tham số hình thể}} — phần tử {{X-n:WFP/LSS/C (mã trạng thái)}}
2 NẾU: {{tham số hình thể}} {{ký hiệu}} = {{giá trị}} | Đối chứng: {{giá trị đối chứng, chỉ khác đúng tham số này}}
3 THÌ: {{đại lượng chức năng đo được}} {{hơn/kém}} đối chứng
4 VÌ: {{một cơ chế vật lý}}
5 KIỂM: {{bàn thử, số mẫu, điều kiện biên, dải, khoảng tin cậy chọn trước}}; người đọc kết quả {{tên}}; ngày thử: {{YYYY-MM-DD}}
6 KẾT QUẢ + khuyến nghị: {{điền SAU}}
7 DỰ ĐOÁN VIẾT TRƯỚC: {{số hoặc hiện tượng kỳ vọng}}; người ký {{tên — CEO điền}} — ngày {{YYYY-MM-DD — CEO điền}}
8 ĐỘ TIN / TẦM ẢNH HƯỞNG: {{thấp/trung/cao}} ({{lý do}}) / {{thấp/trung/cao}} ({{lý do}})
9 NẾU BỊ BÁC: {{lặp trong pha | lặp xuyên cổng → mở lại quyết định cổng nào}}; điểm đầu tư gần nhất {{…}}
Dòng C3: {{Phần tử}} · {{Tham số hình thể}}
Phép thử nhỏ nhất để bác bỏ: {{quan sát rẻ nhất mà nếu thấy thì phiếu bị bác}}
```

## Dòng NHẠY chưa có mô hình
- {{Phần tử}} · {{Tham số hình thể}} — {{vì sao chưa viết được VÌ}} | không có
````

## Khuôn đầu ra: `{{prefix}}CC2_C4_Test_Plan.md`

````markdown
---
updated: YYYY-MM-DD
f_id: {{F-id hoặc —}}
---
# CC2 C4 — Kế hoạch thử trên bàn thử: {{chức năng}}

> Xếp theo định tuyến kiểm được (quy ước bộ skill). Một hàng mỗi phiếu.

| Thứ tự | Phiếu | Mở lại cổng | Đường | Độ tin / Tầm ảnh hưởng | Loại thử | Đại lượng mục tiêu | Mẫu + đối chứng | Ngày thử | Người đọc kết quả |
|---|---|---|---|---|---|---|---|---|---|
| {{1}} | {{GT-nnn}} | {{có (cổng nào) / không}} | {{3 / 2 / 1–2}} | {{nấc / nấc}} | {{thực nghiệm / lý giải nhóm có phản biện / dùng phỏng đoán, ghi nhãn}} | {{đại lượng, đo ở đâu}} | {{số mẫu, đối chứng đo đầu và cuối loạt, rào cản + phép phá}} | {{YYYY-MM-DD}} | {{tên ≠ người lập}} |
````

## Ví dụ ngắn (nắp gài bằng móc đàn hồi, tiếp ví dụ C3; số, tên và ngày là minh hoạ)

### Đầu vào: dòng C3 của phương án A-1

Bảng C3 của ví dụ `helix-cc2-param`. Ba dòng `NHẠY` → ba phiếu; hai dòng không `NHẠY` (một dòng `tri thức`) không có phiếu.

| Phần tử | Tham số hình thể | Thông số chức năng | Chiều ảnh hưởng | Ước lượng | Khoảng chọn | Nhãn | Nguồn số |
|---|---|---|---|---|---|---|---|
| A-1:móc//gờ (S2 gài) | góc mặt vào của móc | lực đóng nắp bằng tay | NHẠY; góc tăng → lực đóng tăng; hạng 3; sai lệch tới hạn: dung sai móc | — | chọn sau phép so | phỏng đoán | chưa biết |
| A-1:móc//gờ (S3 tháo) | góc mặt rút của móc | lực tháo nắp | NHẠY; góc tăng → lực tháo tăng; hạng 2; sai lệch tới hạn: dung sai gờ | so tương đối với góc hiện dùng | quanh góc hiện dùng | phỏng đoán | suy ra (từ phân tích lực trên mặt nghiêng) |
| A-1:cần đàn hồi (LSS, S2 gài) | chiều dài cần | lực đóng, biến dạng còn lại sau nhiều lần mở | NHẠY; dài hơn → lực đóng giảm; hạng 4; sai lệch tới hạn: mòn sau nhiều lần mở | so tương đối với cần hiện dùng | giới hạn bởi không gian nắp | giả định | suy ra (từ công thức dầm ngàm một đầu) |
| A-1:cần đàn hồi (LSS) | bề dày cần | lực đóng nắp bằng tay | dày hơn → lực đóng tăng; hạng 1 | — | trong dải đã đo trên mẫu | tri thức | đo được (mẫu cần ba bề dày, cùng vật liệu, ghi ngày đo) |
| A-1:cần đàn hồi (LSS) | vật liệu cần | biến dạng còn lại sau nhiều lần mở | vật liệu đàn hồi hơn → biến dạng còn lại giảm; hạng 5 | — | chọn trong vật liệu xưởng gia công được | giả định | chưa biết |

### Phiếu (minh hoạ đã ký)

Ba phiếu dưới đây là **minh hoạ đã ký**: mục 7 đã điền để thấy dạng một phiếu qua được lượt lint không cờ. Trong tệp
thật, C4 ghi `người ký {{…}} — ngày {{…}}` và chỉ CEO/kỹ sư điền phần ấy ở Cổng CEO 3.

```text
PHIẾU GIẢ THUYẾT — GT-001
1 Tiêu đề: 001 góc mặt vào của móc — phần tử A-1:móc//gờ (S2 gài)
2 NẾU: góc mặt vào của móc β = 30° | Đối chứng: β = 45°, cùng vật liệu, cùng khuôn in, chỉ khác góc
3 THÌ: lực đóng nắp bằng tay nhỏ hơn đối chứng
4 VÌ: mặt vào thoải hơn chia lực ấn thành thành phần đẩy cần móc sang ngang lớn hơn, nên cần uốn đủ để vượt gờ với lực ấn nhỏ hơn
5 KIỂM: mười nắp mỗi biến thể trên gá ấn thẳng, đo lực đóng bằng lực kế, cùng nhiệt độ phòng, đối chứng đo đầu và cuối loạt; người đọc kết quả Kỹ thuật viên B; ngày thử: 2026-11-20
6 KẾT QUẢ + khuyến nghị: {{điền SAU}}
7 DỰ ĐOÁN VIẾT TRƯỚC: lực đóng trung bình của biến thể 30° nhỏ hơn đối chứng ít nhất 15%; người ký Kỹ sư A — ngày 2026-10-20
8 ĐỘ TIN / TẦM ẢNH HƯỞNG: trung (cơ chế mặt nghiêng quen, chưa đo trên vật liệu này) / trung (lực đóng là thứ người dùng cảm nhận trực tiếp)
9 NẾU BỊ BÁC: lặp trong pha — giữ góc hiện dùng, chuyển sang GT-003; không mở lại quyết định cổng nào
Dòng C3: A-1:móc//gờ (S2 gài) · góc mặt vào của móc
Phép thử nhỏ nhất để bác bỏ: ba nắp mỗi biến thể ấn bằng lực kế tay; lực đóng của biến thể 30° không nhỏ hơn đối chứng thì bác.
```

```text
PHIẾU GIẢ THUYẾT — GT-002
1 Tiêu đề: 002 góc mặt rút của móc — phần tử A-1:móc//gờ (S3 tháo)
2 NẾU: góc mặt rút của móc α = 45° | Đối chứng: α = 30°, cùng vật liệu, cùng khuôn in, chỉ khác góc
3 THÌ: lực tháo nắp bằng tay lớn hơn đối chứng
4 VÌ: mặt rút dốc hơn làm thành phần lực đẩy cần móc ra ngoài nhỏ đi, nên cần móc phải uốn nhiều hơn mới nhả
5 KIỂM: mười nắp mỗi biến thể trên gá kéo thẳng, đo lực tháo bằng lực kế, cùng nhiệt độ phòng, đối chứng đo đầu và cuối loạt; người đọc kết quả Kỹ thuật viên B; ngày thử: 2026-11-22
6 KẾT QUẢ + khuyến nghị: {{điền SAU}}
7 DỰ ĐOÁN VIẾT TRƯỚC: lực tháo trung bình của biến thể 45° lớn hơn đối chứng ít nhất 20%; người ký Kỹ sư A — ngày 2026-10-20
8 ĐỘ TIN / TẦM ẢNH HƯỞNG: trung (cơ chế mặt nghiêng quen, chưa đo trên vật liệu này) / thấp (sửa khuôn in rẻ, đảo lại được)
9 NẾU BỊ BÁC: lặp trong pha — giữ góc hiện dùng; không mở lại quyết định cổng nào
Dòng C3: A-1:móc//gờ (S3 tháo) · góc mặt rút của móc
Phép thử nhỏ nhất để bác bỏ: hai người tháo tay ba nắp mỗi biến thể, không biết nắp nào là biến thể nào; không ai thấy nắp 45° khó tháo hơn thì bác.
```

```text
PHIẾU GIẢ THUYẾT — GT-003
1 Tiêu đề: 003 chiều dài cần đàn hồi — phần tử A-1:cần đàn hồi (LSS, S2 gài)
2 NẾU: chiều dài cần đàn hồi L = 14 mm | Đối chứng: L = 10 mm, cùng bề dày, cùng vật liệu, chỉ khác chiều dài
3 THÌ: biến dạng còn lại của móc sau một loạt lần mở nhỏ hơn đối chứng
4 VÌ: cần dài hơn đạt cùng độ võng với ứng suất ở chân ngàm nhỏ hơn, nên vật liệu ít chảy dẻo hơn mỗi lần gài
5 KIỂM: sáu nắp mỗi biến thể trên gá đóng mở lặp, đo độ võng còn lại của móc bằng thước đo độ sâu sau mỗi chặng; người đọc kết quả Kỹ thuật viên B; ngày thử: 2026-11-18
6 KẾT QUẢ + khuyến nghị: {{điền SAU}}
7 DỰ ĐOÁN VIẾT TRƯỚC: sau cùng số lần mở, biến dạng còn lại của biến thể 14 mm nhỏ hơn một nửa đối chứng; người ký Kỹ sư A — ngày 2026-10-20
8 ĐỘ TIN / TẦM ẢNH HƯỞNG: thấp (vật liệu cần chưa biết, chưa đo) / cao (cần dài hơn có thể không vừa không gian nắp)
9 NẾU BỊ BÁC: lặp xuyên cổng → mở lại quyết định Cổng CEO 2 (chọn chuỗi), vì móc đàn hồi không giữ được qua vòng đời; điểm đầu tư gần nhất là ngày đặt khuôn ép
Dòng C3: A-1:cần đàn hồi (LSS, S2 gài) · chiều dài cần
Phép thử nhỏ nhất để bác bỏ: hai mẫu in mỗi biến thể, đóng mở tay một chặng ngắn rồi so độ võng còn lại; biến thể 14 mm không nhỏ hơn đối chứng thì bác.
```

### Kế hoạch thử (minh hoạ)

GT-003 lên đầu vì nếu bị bác sẽ mở lại Cổng CEO 2; GT-001 đường 3 trước GT-002 đường 2.

| Thứ tự | Phiếu | Mở lại cổng | Đường | Độ tin / Tầm ảnh hưởng | Loại thử | Đại lượng mục tiêu | Mẫu + đối chứng | Ngày thử | Người đọc kết quả |
|---|---|---|---|---|---|---|---|---|---|
| 1 | GT-003 | có (Cổng CEO 2) | 3 | thấp / cao | thực nghiệm | biến dạng còn lại của móc, đo ở mặt ngoài móc | sáu nắp mỗi biến thể; rào cản quá chậm → `state` theo chặng mở, ảnh cùng góc mỗi chặng | 2026-11-18 | Kỹ thuật viên B |
| 2 | GT-001 | không | 3 | trung / trung | thực nghiệm | lực đóng nắp, đo ở mặt nắp | mười nắp mỗi biến thể; đối chứng đo đầu và cuối loạt | 2026-11-20 | Kỹ thuật viên B |
| 3 | GT-002 | không | 2 | trung / thấp | lý giải nhóm có phản biện, kèm phép thử nhỏ nhất | lực tháo nắp, đo ở mép nắp | mười nắp mỗi biến thể nếu CEO chọn lên bàn thử | 2026-11-22 | Kỹ thuật viên B |

## Chạy riêng

```
/helix-cc2-hypo [--analyze] [--out <thư mục>]
```

Đầu vào tối thiểu: `{{prefix}}CC2_C3_Params.md` ở nơi ghi và `{{prefix}}CC2_C0_Frame.md` ở gốc (chạy `/helix-cc2-param` trước
nếu chưa có); với `--analyze`: `{{prefix}}CC2_CA_Analysis.md` (chạy `/helix-cc2-analyze` trước). Chế độ dự án: truyền
`--out <nơi ghi>/<F-id>` hoặc để C4 đọc `current_f` trong `_pipeline_state.md`.

## COD

| Việc | Lớp | Ai |
|---|---|---|
| Viết phiếu, phép thử nhỏ nhất, kế hoạch thử, tính đường và thứ tự | **O** Offload | AI |
| Ký dự đoán ở mục 7 (Cổng CEO 3), hạ đường 3 xuống 2 | **C** Core | CEO / kỹ sư — AI không ký thay |
| Đọc kết quả thử, điền mục 6 | **C** Core | người đọc kết quả ≠ người lập phiếu |
| Chạy `cc2_sheet_lint` hai lượt, ghi mã vào `_pipeline_state.md` | **D** Default | tự động |
