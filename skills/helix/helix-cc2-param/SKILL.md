---
name: helix-cc2-param
description: "Khối C3 của bộ helix-cc2 — mỗi phương án hình thể ở C2 một bảng cầu nối tham số hình thể ↔ thông số chức năng theo WFP/LSS/Connector kèm mã trạng thái, đúng 8 cột của param-bridge (Phần tử, Tham số hình thể, Thông số chức năng, Chiều ảnh hưởng, Ước lượng, Khoảng chọn, Nhãn, Nguồn số); đánh dấu NHẠY tối đa 3 tham số mỗi phương án; ước lượng giải tích ghi suy ra (từ …). Cột tham số chỉ chứa thứ ghi được lên bản vẽ, không phải tác dụng. Cuối khối bắt buộc chạy cc2_sheet_lint --kind params; mã khác 0 thì không sang C4. Triggers on: 'parameter bridge', 'form function parameters', 'sensitive parameters', 'C&C2 parameter table', 'bảng tham số hình thể', 'tham số nhạy', 'cầu nối tham số', 'helix-cc2-param'."
---

# helix-cc2-param — Khối C3: bảng tham số hình thể ↔ thông số chức năng

> **Vai:** sau C2, trước C4. Với mỗi phương án hình thể, nối từng phần tử với tham số ghi được lên bản vẽ và thông số chức
> năng nó ảnh hưởng; chỉ ra tối đa 3 tham số nhạy đi tiếp sang phiếu C4.
> **Đầu vào:** `{{prefix}}CC2_C2_Forms.md`, `{{prefix}}CC2_C0_Frame.md` (thông số chức năng, ở **gốc** nơi ghi) |
> **Đầu ra:** `{{prefix}}CC2_C3_Params.md` | **Đọc bởi:** C4, C6
> **Nguồn dùng chung:** `helix-cc2:references:param-bridge` (§Tham số, không phải tác dụng; §WSPO / WSPA;
> §Độ nhạy và thứ hạng; §Dải đã kiểm; §Khuôn bảng C3), `helix-cc2:references:cc2-core` (§Hai loại nhãn).

## Đầu vào

- Bắt buộc: `{{prefix}}CC2_C2_Forms.md` và `{{prefix}}CC2_C0_Frame.md`. Thiếu tệp nào → liệt kê tệp thiếu và dừng; không
  dựng giả tệp thượng nguồn (`--from C2` hoặc `--from C0` để chạy lại khối ghi tệp đó).
- Chế độ dự án: chạy theo từng `F-id`; đọc C2 và ghi C3 trong `<nơi ghi>/<F-id>/`, đọc C0 ở gốc `<nơi ghi>/`. Chức năng con ở
  ô `chỉ bảng tham số` của C0 chạy C3 mà không có C1/C2: lấy phần tử và tham số trực tiếp từ C0.

## Luật cứng

1. **Một bảng mỗi phương án** (`A-1`, `A-2`…), **đúng 8 cột** theo `helix-cc2:references:param-bridge` §Khuôn bảng C3:
   `Phần tử | Tham số hình thể | Thông số chức năng | Chiều ảnh hưởng | Ước lượng | Khoảng chọn | Nhãn | Nguồn số`. Không đổi tên,
   không thêm bớt cột. Mỗi dòng một tham số, gắn với **đúng một** phần tử (WFP, LSS hay Connector) kèm mã trạng thái.
2. **Tham số, không phải tác dụng.** Cột *Tham số hình thể* chỉ chứa thứ ghi được lên bản vẽ (góc, chiều dài, khe hở, độ
   nhám, lớp phủ, vật liệu). Phép thử ba giây: viết được giá trị ô ấy lên bản vẽ không? Không → đó là tác dụng, tìm tham số
   đứng sau (`param-bridge` §Tham số, không phải tác dụng). Mối ghép ma sát luôn kèm một dòng `giả định` cho hệ số ma sát
   và tham số đứng sau nó (cặp vật liệu, lớp phủ, độ nhám).
3. **Nhãn và Nguồn số** (`cc2-core` §Hai loại nhãn): *Nhãn* là `tri thức` / `phỏng đoán` / `giả định`. *Nguồn số* bắt đầu bằng
   `đo được` / `suy ra (từ …)` / `chưa biết`. `tri thức` không đi với `chưa biết`. Con số không nguồn là `chưa biết` hoặc
   `giả định`, không bao giờ `tri thức`.
4. **Ước lượng giải tích** luôn ghi `suy ra (từ <công thức hoặc nguồn>)` ở cột Nguồn số; ô *Ước lượng* mặc định là so tương đối
   với đối chứng (nấc 3 của thang lượng hoá), hoặc `—` ở nấc 0. Không ngoại suy ra ngoài dải đã kiểm
   (`param-bridge` §Dải đã kiểm). Trước khi lượng hoá, ghi đủ ba ô: một đại lượng chức năng đo được, một tham số hình thể
   nghi ngờ, một phương án đối chứng.
5. **Đánh dấu `NHẠY`: ≤3 tham số mỗi phương án** *(quy ước bộ skill)*. NHẠY = ô "Chiều ảnh hưởng" bắt đầu bằng `NHẠY` (quy ước bộ skill); C4 lấy đúng các dòng này. Không thêm
   cột. **Tiêu chí chọn** *(quy ước bộ skill, sách không định nghĩa chữ này; xem `param-bridge` §Độ nhạy và thứ hạng)*:
   tham số nhạy là tham số có **thứ hạng cao nhất *và* độ tin thấp nhất ở trạng thái tới hạn**. Nhiều hơn ba ứng viên thì giữ
   ba tham số có thứ hạng cao nhất, các tham số còn lại ghi thứ hạng bình thường, không `NHẠY`. Mỗi tham số `NHẠY` ghi thêm
   sai lệch tới hạn (dung sai, mòn, nhiệt) trong ô *Chiều ảnh hưởng*.
6. **Ô *Chiều ảnh hưởng*** ghi dấu (tăng thì chức năng tốt lên hay xấu đi), thứ hạng trong các tham số nghi, mã trạng thái;
   ô *Khoảng chọn* ghi dải và công sức đổi trên sản phẩm. Thiếu công sức đổi thì đội đổi cái dễ đổi, không phải cái đáng đổi.
7. Một ngưỡng tham số đúng chỉ là điều kiện cần cho chức năng con, không đủ cho chức năng tổng; không ghi «đủ bền» khi chỉ
   so tương đối.

## Bước

1. Đọc C2 và các thông số chức năng của C0; với mỗi phương án liệt kê WFP/LSS/Connector và trạng thái.
2. Với mỗi phần tử nghi: ghi pháp tuyến và diện tích chiếu của WFP, chiều dài làm cánh tay đòn của LSS
   (`param-bridge` §WSPO / WSPA); rút tham số hình thể ghi được lên bản vẽ.
3. Điền từng dòng đủ 8 cột; gắn nhãn và nguồn số (luật 3–4).
4. Xếp thứ hạng, chọn ≤3 tham số `NHẠY` theo tiêu chí ở luật 5.
5. Ghi tệp, rồi chạy **lệnh bắt buộc** (mục cuối), sửa tới khi sạch.

## Khuôn đầu ra: `{{prefix}}CC2_C3_Params.md`

````markdown
---
updated: YYYY-MM-DD
f_id: {{F-id hoặc —}}
---
# CC2 C3 — Bảng tham số: {{chức năng}}

> Mọi quan hệ dưới đây là giả thuyết. `NHẠY` = quy ước bộ skill, tối đa 3 mỗi phương án.

## Phương án {{X}}-1

| Phần tử | Tham số hình thể | Thông số chức năng | Chiều ảnh hưởng | Ước lượng | Khoảng chọn | Nhãn | Nguồn số |
|---|---|---|---|---|---|---|---|
| {{X:WFP1 (S2)}} | {{góc, chiều dài, khe…}} | {{đại lượng đo được}} | {{NHẠY nếu được chọn; ↑/↓, thứ hạng}} | {{giá trị hoặc —}} | {{min–max}} | {{tri thức/phỏng đoán/giả định}} | {{đo được / suy ra (từ …) / chưa biết}} |

## Phương án {{X}}-2
…
````

## Ví dụ ngắn (nắp gài bằng móc đàn hồi, phương án A-1; minh hoạ, không số)

| Phần tử | Tham số hình thể | Thông số chức năng | Chiều ảnh hưởng | Ước lượng | Khoảng chọn | Nhãn | Nguồn số |
|---|---|---|---|---|---|---|---|
| A-1:móc//gờ (S2 gài) | góc mặt vào của móc | lực đóng nắp bằng tay | NHẠY; góc tăng → lực đóng tăng; hạng 2; sai lệch tới hạn: dung sai móc | — | chọn sau phép so | phỏng đoán | chưa biết |
| A-1:móc//gờ (S3 tháo) | góc mặt rút của móc | lực tháo nắp | NHẠY; góc tăng → lực tháo tăng; hạng 1; sai lệch tới hạn: dung sai gờ | so tương đối với góc hiện dùng | quanh góc hiện dùng | phỏng đoán | suy ra (từ phân tích lực trên mặt nghiêng) |
| A-1:cần đàn hồi (LSS, S2 gài) | chiều dài cần | lực đóng, biến dạng còn lại sau nhiều lần mở | NHẠY; dài hơn → lực đóng giảm; hạng 3; sai lệch tới hạn: mòn sau nhiều lần mở | so tương đối với cần hiện dùng | giới hạn bởi không gian nắp | giả định | suy ra (từ công thức dầm ngàm một đầu) |
| A-1:cần đàn hồi (LSS) | vật liệu cần | biến dạng còn lại sau nhiều lần mở | vật liệu đàn hồi hơn → biến dạng còn lại giảm; hạng 4 | — | chọn trong vật liệu xưởng gia công được | giả định | chưa biết |

## Lệnh bắt buộc cuối khối

```
python scripts/cc2_sheet_lint.py {{prefix}}CC2_C3_Params.md --kind params
```

- Exit 0 → sạch, mới được sang C4.
- Exit 1 → còn ô thiếu nhãn hay nguồn số, hoặc `tri thức` đi với `chưa biết`, hoặc bảng rỗng (`EMPTY_TABLE`) hay không có
  bảng nào khớp (`NO_TABLE`): sửa rồi chạy lại.
- Exit 2 → lỗi đọc tệp; dừng, báo CEO.
- Exit ≠ 0 thì không sang C4 và không đánh dấu C3 `lint 0` trong `_pipeline_state.md`.
- Luật cứng: báo cáo "đã kiểm" không thay output của lệnh. In nguyên output lệnh và mã thoát vào tóm tắt khối; không có
  output thật thì chưa kiểm.

Sau lệnh: ghi mã lint vào cột C3 của `_pipeline_state.md`, in tóm tắt 3–5 dòng (số phương án, tham số `NHẠY` mỗi phương
án), hỏi CEO «tiếp / sửa / dừng».

## Chạy riêng

```
/helix-cc2-param [--out <thư mục>]
```

Đầu vào tối thiểu: `{{prefix}}CC2_C2_Forms.md` ở nơi ghi và `{{prefix}}CC2_C0_Frame.md` ở gốc (chạy `/helix-cc2-form` trước
nếu chưa có). Chế độ dự án: truyền `--out <nơi ghi>/<F-id>` hoặc để C3 đọc `current_f`.

## COD

| Việc | Lớp | Ai |
|---|---|---|
| Dựng bảng, xếp hạng, đề xuất tham số `NHẠY` | **O** Offload | AI |
| Duyệt tham số nhạy đi tiếp sang C4, nhập số đo thật | **C** Core | CEO / kỹ sư |
| Chạy `cc2_sheet_lint`, ghi mã vào `_pipeline_state.md` | **D** Default | tự động |
