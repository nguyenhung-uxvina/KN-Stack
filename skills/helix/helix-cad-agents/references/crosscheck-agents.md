# Ứng dụng 10 — Dựng 3D từ 2D có kiểm ngược: brief 4 agent

Bản vẽ 2D là **gốc**. Mô hình 3D là **nhân chứng**: dựng từ bản vẽ, rồi chiếu lại so từng hình chiếu
([[helix-cad-crosscheck]]). Chỗ mô hình sai thì sửa mô hình. Chỗ chính bản vẽ tự mâu thuẫn (một hình chiếu khác
thấy đúng phương lệch và đứng về phía mô hình) thì lập **đề xuất sửa 2D** để CEO quyết. Máy không sửa bản vẽ.

Luật chung cho cả 4 agent:
- Phân loại MẬT ⇒ **không chạy agent nào**: chỉ chạy script (render, crosscheck, mutate, audit_claims) và người làm.
- Mỗi agent là một `Task` **mới**. Agent dựng ≠ agent chẩn đoán ≠ agent lập phiếu (giám khảo khác người dựng).
- Số liệu do script tính. Agent không tự đo, không tự đổi `attribution`, không đổi trạng thái claim.
- Quyết định CEO phải được viết lại thành câu khẳng định trong `spec.md` / `views.json` trước khi agent đọc.
  Agent không đọc `_pipeline_state.md`.

---

## A1 — Lập sổ hình chiếu (`views.json`) + spec nháp

Chuẩn bị (orchestrator): `render_dxf.py` mọi tờ → `<WORKDIR>/input/*.png`; `ingest.py --measure-geometry` →
`<WORKDIR>/input/<part>.cad_extract.json`; đặt `<WORKDIR>/input/layers.txt` (danh sách lớp + số thực thể,
từ `acad_layers` / ezdxf) và `<WORKDIR>/input/extents.json` (ô bao của từng cụm thực thể trên tờ).

```
WORKDIR = <WORKDIR>
Bạn lập SỔ HÌNH CHIẾU cho bản vẽ chi tiết <PART>. Chỉ đọc <WORKDIR>/input/ (ảnh PNG, cad_extract.json,
layers.txt, extents.json). Không đọc tệp nào khác.
Đọc schema: <KNSTACK>/skills/helix/helix-cad-crosscheck/references/view_registry.schema.md
Với MỖI hình chiếu / mặt cắt trên tờ, ghi một mục views[]: id (tên trên bản vẽ), region (đơn vị tờ, lấy từ
extents.json, KHÔNG ước lượng từ ảnh), scale (mẫu số, theo khung tên hoặc ghi chú riêng của hình),
look_dir + up (hệ mô hình X ngang hình đứng, Z đứng, Y sâu; góc chiếu theo ký hiệu khung tên, TCVN thường
góc thứ nhất), layers_visible / layers_hidden (từ layers.txt; KHÔNG đưa lớp kích thước, trục, chữ),
hidden_lines (full chỉ khi hình vẽ đủ nét khuất), kind (+ section.point cho mặt cắt).
Mỗi giá trị bạn suy ra (không đọc thẳng được) đánh dấu trong views_notes.md với nhãn D (đọc từ DXF) /
G (hình học) / T (chữ) / ? (đoán). Không có simplifications[] — chỉ kỹ sư khai.
SẢN PHẨM: <WORKDIR>/views.json, <WORKDIR>/views_notes.md. Báo cáo ≤ 8 dòng: số hình chiếu, góc chiếu,
mọi giá trị '?'.
```
Sau A1: kỹ sư duyệt phương nhìn và tỉ lệ (**C**). Không còn `?` thì mới qua A2 (`audit_claims.py spec`
áp cho `views_notes.md`).

---

## A2 — Dựng mô hình, vòng kiểm ngược bên trong

Dùng nguyên văn `reconstruct-brief.md` (giao thức cách ly, hợp đồng PARAMS/build, cấm chỉnh theo khối lượng),
**thêm** khối dưới. `input/` có thêm `views.json` (đã duyệt) và tệp `.dxf` của tờ (crosscheck cần DXF).

```
KIỂM NGƯỢC TRONG KHI DỰNG (bắt buộc, lặp tới khi hết FAIL hoặc 8 vòng):
  python -I -X utf8 <KNSTACK>/skills/helix/helix-cad-crosscheck/crosscheck.py --step <WORKDIR>/model.step \
      --dxf <WORKDIR>/input/<tờ>.dxf --registry <WORKDIR>/input/views.json --out <WORKDIR>/work/xc_<n> \
      --png-dir <WORKDIR>/work/xc_<n>_png
Đọc xc_<n>.md và ảnh PNG.
- Claim attribution = model (FAIL): sửa PARAMS/build cho khớp BẢN VẼ. Bản vẽ là gốc.
- Claim attribution = drawing (CONTESTED): KHÔNG sửa mô hình theo hình chiếu bị nghi. Giữ mô hình theo các
  hình chiếu làm chứng (witness_views). Ghi vào notes.md: claim, hình chiếu nghi sai, hình làm chứng.
- Không được thêm simplifications[] vào views.json. Thấy cần đơn giản hoá thì ghi notes.md để kỹ sư quyết.
- Không đổi views.json để cho qua. Thấy sổ sai (cả hình lệch cùng vectơ, X1 báo tỉ số) thì DỪNG, ghi notes.md.
Báo cáo thêm: số vòng kiểm, số FAIL còn lại, danh sách CONTESTED.
```

---

## A3 — Cổng tất định (script, không agent)

```
geom_gates.py (hợp đồng đã ký) → crosscheck.py → mutate.py --model model.py → audit_claims.py collect
  --gates g.json --crosscheck xc.json --mutate mut.json --profile reconstruct
```
- `mutate.py` từ chối khi crosscheck chưa PASS ⇒ claim `L6_positive_control` = NEEDS_EVIDENCE ⇒ BLOCKED.
  Đúng ý đồ: "0 lỗi" chỉ được tin khi đối chứng dương chạy được. Còn CONTESTED thì đi A5 trước.
- MẬT: A3 vẫn chạy (cục bộ), A4/A5 do người làm.

---

## A4 — Chẩn đoán (agent KHÁC A2)

```
Bạn chẩn đoán kết quả kiểm ngược 3D↔2D của <PART>. Chỉ đọc: <WORKDIR>/claims.json, <WORKDIR>/xc.json,
<WORKDIR>/xc_png/*.png, <WORKDIR>/mut.json. Không đọc model.py, notes.md của agent dựng.
Với MỖI claim chặn: một dòng bảng | [claim_id] | hình | loại (sổ sai / mô hình sai / bản vẽ tự mâu thuẫn /
đơn giản hoá chưa khai) | bằng chứng (vùng, hình làm chứng) | việc tiếp |.
KHÔNG đổi attribution hay trạng thái của máy. Nếu bạn cho rằng máy quy sai bên, ghi cột "ý kiến khác" và lý do
— người quyết. Mọi dòng phát hiện phải trích [claim_id] có trong claims.json.
SẢN PHẨM: <WORKDIR>/chan_doan.md
```
Orchestrator chạy `audit_claims.py check-report --claims claims.json --report chan_doan.md` (exit 2 ⇒ trả lại).

---

## A5 — Phiếu đề xuất sửa bản vẽ (agent KHÁC A2, A4)

Chỉ chạy khi `xc.json → drawing_fix_proposals[]` không rỗng.

```
Bạn lập PHIẾU ĐỀ XUẤT SỬA BẢN VẼ cho <PART>, tờ <TỜ>. Chỉ đọc: <WORKDIR>/xc.json (drawing_fix_proposals[],
checks[]), <WORKDIR>/claims.json, <WORKDIR>/xc_png/*.png, <WORKDIR>/input/*.png.
Mỗi đề xuất một mục:
  SUA-<TỜ>-<n> · [claim_id] · hình chiếu cần sửa · hình làm chứng (witness_views) · thực thể DXF (handle)
  · hiện trạng (observed) · đề xuất (sửa vị trí / xoá / bổ sung nét / sửa chữ kích thước) · vì sao
  (một câu, theo hình làm chứng) · ảnh: vùng cắt từ PNG crosscheck.
Không đề xuất gì ngoài drawing_fix_proposals[] và claim X5/X7 có attribution = drawing.
Không ghi tên người, không ghi "đã duyệt", không tạo ô chữ ký có tên. Cuối phiếu: "Trạng thái: CHỜ CEO QUYẾT
— máy không sửa bản vẽ." Mọi dòng phải trích [claim_id].
SẢN PHẨM: <WORKDIR>/de_xuat_sua_ban_ve.md
```
Sau A5: `check-report` trên phiếu → CEO duyệt từng mục (**C**) → người (hoặc [[helix-cad-roundtrip]] theo
lệnh CEO) sửa DXF → quay lại A3 với DXF mới. Mục CEO bác: khai vào `simplifications[]` có `reason` (nếu là
cố ý) hoặc ghi rõ hình nào là đúng vào `spec.md`, rồi A2 sửa mô hình.
