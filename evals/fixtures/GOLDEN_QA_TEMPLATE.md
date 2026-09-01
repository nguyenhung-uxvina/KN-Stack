# Golden Q&A Authoring — bộ test độ chính xác extraction (CEO Core)

> **Mục đích:** soạn bộ 40–50 câu hỏi CÓ ĐÁP ÁN CHUẨN trên một set bản vẽ THẬT (ví dụ
> GIÁ TRƯỢT UUV, 41 DXF), để mỗi khi sửa `ingest.py`/pipeline chạy lại và đo được
> "cải thiện hay thoái hóa" — thay vì tin cảm tính. Đây là lớp đo lường mà pipeline
> extraction còn thiếu (bài học ConstructIQ: index một lần, query từ text, **chấm theo
> ground truth**).
>
> **Falsifiable:** harness `accuracy-eval.py` đã tự kiểm bằng fixture tự-sinh
> (`sample_part.dxf`, 14/14). Bộ này chỉ đổi fixture → set thật + đáp án CEO chứng thực.

## Ba nguyên tắc (vá đúng điểm yếu của video)

1. **KHÔNG tự ra đề một mình.** Điểm yếu số 1 của video là tác giả tự đặt 44 câu → overfit
   vào loại câu anh ta nghĩ ra. Lấy câu hỏi từ **nhu cầu thật**: quản đốc hỏi gì khi lập
   QTCN? định mức cần con số nào? tổ QC đo gì? → đó là câu hỏi vàng.
2. **Đáp án là CEO/kỹ sư chứng thực, KHÔNG phải AI đọc rồi tin.** Với bản vẽ MẬT/thật, con
   số đúng do người đo/ký (Core). AI không được điền đáp án cho chính bài nó sẽ bị chấm —
   đó là gian lận thước đo.
3. **Ghi rõ phương pháp thu thập đáp án** (đếm vector / đọc schedule / đo theo scale) vào
   cột `min_confidence`. Đáp án đo-theo-scale = tin cậy thấp → đừng đặt `min_confidence: HIGH`.

## Cách làm (4 bước)

1. Copy `helix-cad-ingest.accuracy.json` → `helix-cad-ingest.gia-truot.accuracy.json`.
2. Trỏ `fixture` sang set thật:
   ```json
   "fixture": { "dxf": "fixtures/gia-truot/<một-part>.dxf", "classification": "MẬT" }
   ```
   (Nhiều part → tạm thời một spec / một part tiêu biểu; mở rộng multi-part khi cần.)
   ⚠️ Bản vẽ MẬT: giữ trong vault, **không commit** vào repo công khai — thêm path vào
   `.gitignore`. Chỉ commit spec câu hỏi + đáp án nếu đáp án không lộ hình học nhạy cảm.
3. Với mỗi câu hỏi thật, điền một dòng vào `questions[]` (xem cú pháp query bên dưới).
4. Chạy: `bash evals/run-eval.sh helix-cad-ingest --accuracy` (hoặc trỏ thẳng
   `python evals/accuracy-eval.py evals/helix-cad-ingest.gia-truot.accuracy.json`).
    Chưa đạt 95% → hoặc `ingest.py` cần sửa (lỗi thật), hoặc câu hỏi vượt năng lực hiện tại
   của pipeline (ghi nhận làm roadmap). **Đừng hạ đáp án cho khớp** — đó là làm hỏng thước đo.

## Cú pháp query (resolve vào `cad_extract.json`)

| Loại câu hỏi | `query` | Ví dụ đáp án |
|---|---|---|
| Trường meta | `meta.material` · `meta.scale` · `meta.units` · `meta.code_in_dxf` | "NHÔM 5083" |
| Đếm lỗ theo Ø | `holes[dia=6.6].count` | 4 |
| Tổng số lỗ | `holes[]\|sum-of:count` | 6 |
| Số nhóm Ø khác nhau | `holes[]\|count` | 2 |
| Ø lớn nhất | `holes[]\|max-of:dia` | 12.0 |
| Giá trị 1 kích thước | `dimensions[0].value` | 100.0 |
| Số kích thước bóc được | `dimensions[]\|count` | 12 |
| Số ghi chú công nghệ | `process_notes\|count` | 5 |

`match`: `exact` (mặc định) · `approx` (số, cần `tolerance`) · `contains` (chuỗi con) · `regex`.

**Provenance (tùy chọn, nên dùng cho câu tới hạn):** thêm
`"confidence_query": "holes[dia=6.6].confidence", "min_confidence": "HIGH"` → câu chỉ PASS
khi giá trị đạt độ tin cậy tối thiểu. Đây là mầm của "confidence theo phương pháp thu thập"
(item 2 roadmap): buộc gate hạ lưu từ chối số tin cậy thấp.

## Gợi ý 8 nhóm câu (mở rộng thành 40–50)

1. **Nhận diện** — vật liệu, mã chi tiết, tỷ lệ, đơn vị, sản phẩm, tổ chức thiết kế.
2. **Lỗ** — số lỗ mỗi đường kính, tổng lỗ, số nhóm Ø, Ø lớn/nhỏ nhất.
3. **Kích thước** — kích thước bao (dài/rộng/cao), số kích thước bóc được, dung sai chung.
4. **Vật liệu & phôi** — độ dày tấm, mác hợp kim (khớp whitelist).
5. **Provenance** — mã khung tên có LOW-confidence không? kích thước nào là HIGH?
6. **Ghi chú công nghệ** — số ghi chú, có yêu cầu vát mép/làm sạch ba via không.
7. **Sanity chéo** (chuẩn bị cho item 3) — tổng ≈ tổng thành phần; bbox ≤ envelope cụm.
8. **Conflict/Missing** — số conflict break-view; số mục cần xác nhận (ARC chưa quy thành lỗ).

## Đầu ra kép
`cad_extract.json` mà bộ này chấm cũng chính là **điểm nhập BOM/định mức vào ERPNext**
(`erp-bom import-cad`). Đo được extraction = tin được số đưa vào ERP. Một mũi tên hai đích.
