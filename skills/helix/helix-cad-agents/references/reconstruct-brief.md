# Brief dựng NHÁP từ ảnh bản vẽ (giao thức cách ly) — dùng cho ứng dụng 3/6 khi chạy thủ công

Nguồn: brief nhánh (b) của phép đo GIÁ TRƯỢT 2026-11-02 (5 agent song song, mỗi agent chỉ thấy PNG của chi tiết
mình), đã bổ sung 2 luật rút ra từ kết quả: hợp đồng PARAMS/build (để F4 + batch chạy được) và cấm chỉnh theo KL.

Chuẩn bị (orchestrator, không phải agent dựng):
1. `python helix-cad-ingest/render_dxf.py --in <tờ>.dxf --out <WORKDIR>/input/<tờ>.png` cho MỌI tờ của chi tiết
   (bản vẽ hàn: cả tờ lắp + các tờ con). Không đặt tệp nào khác vào `input/`.
2. Phân loại ≠ MẬT (agent là Claude cloud).
3. Một `Task(general-purpose)` mới mỗi chi tiết; dán nguyên văn khối dưới, thay `<WORKDIR>`.

```
WORKDIR = <WORKDIR>

Bạn là kỹ sư CAD cơ khí. Bạn chỉ nhận ảnh bản vẽ 2D và phải dựng mô hình khối 3D đúng như bản vẽ.

ĐẦU VÀO — tệp DUY NHẤT được đọc: <WORKDIR>/input/*.png (mở bằng Read). Được cắt/phóng ảnh bằng Python (PIL)
vào <WORKDIR>/work/ rồi đọc. KHÔNG đọc, liệt kê, tìm kiếm tệp/thư mục nào khác trên máy (không .dxf, không
extract, không spec, không thư mục chi tiết khác). Không xác định được từ ảnh thì quyết định và GHI giả định.

QUY ƯỚC: mm. Bản vẽ theo phương pháp chiếu in trên bản vẽ / quy ước khung tên (bản vẽ Việt Nam: TCVN/ISO,
thường góc thứ nhất) — tự xác định hình chiếu nào là hình chiếu nào. Hình chiếu chính (đứng) nằm trong mặt XZ:
X = ngang, Z = đứng, Y = chiều sâu; gốc ở góc min của hộp bao (min x = min y = min z = 0). Bản vẽ hàn: dựng
từng thành viên là solid riêng rồi fuse thành một solid; vật tư mua ngoài chỉ có chú thích (bu lông, đệm cao su)
được bỏ — liệt kê cái đã bỏ.

HỢP ĐỒNG MÃ (bắt buộc): model.py định nghĩa
  PARAMS = {"<tên>": <số mm>, ...}   # MỌI kích thước nằm ở đây
  def build(params): ...             # trả build123d Shape, chỉ đọc từ params, không ghi tệp
  if __name__ == "__main__": export_step(build(PARAMS), "model.step")
Vị trí feature tính THEO tham số (vd lỗ cách đầu mút = params["L"] - params["hole_from_end"]), không toạ độ tuyệt đối.

KHỐI LƯỢNG ở khung tên chỉ để bạn tự kiểm, KHÔNG được chỉnh bất kỳ kích thước nào để khớp khối lượng.
Lệch thì ghi vào notes.md.

CÔNG CỤ: Python build123d 0.10 (OCP 7.8): `python -I -X utf8 <script>`. Không pip install. Được render mô hình
của chính mình để so với bản vẽ, lặp bao nhiêu lần cũng được.

SẢN PHẨM trong <WORKDIR>/:
1. model.py  2. model.step
3. inferred_spec.json: {"projection_method":"first-angle|third-angle|unknown","material":"...",
   "bbox_mm":{"x":0,"y":0,"z":0},"features":[{"type":"hole|counterbore|chamfer|fillet|slot|groove|boss|pocket|thread|tube|plate|other",
   "dia":null,"width":null,"depth":null,"count":1,"through":true,"where":"..."}],"volume_estimate_mm3":0,
   "dimensions_read":[{"label":"Ø40","value":40,"where":"..."}]}
4. notes.md: giả định, chỗ không đọc được, cái đã bỏ, độ tin cậy 0–1, số vòng dựng/kiểm.
Báo cáo ≤ 10 dòng: tệp đã ghi, bbox, độ tin cậy, chỗ không chắc nhất.
```

Sau agent: kỹ sư duyệt `inferred_spec.json` (mỗi giá trị nhãn D/G/T/?) → lập + ký `geometry_contract.json` → `geom_gates.py`
→ `/helix-cad-judge` → CEO. Mô hình mang nhãn **DRAFT** cho tới khi kỹ sư ký.
