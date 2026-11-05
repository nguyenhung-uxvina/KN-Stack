---
name: helix-cad-redraw
description: "Vẽ lại bộ bản vẽ 2D (DXF) THEO BẢN GỐC rồi chuẩn hoá bố trí — khối của helix-cad-agents (ứng dụng 10). Tách tờ → liệt kê lệch nội tại (số ghi ≠ hình đo, nhãn tỷ lệ ≠ hệ số) cho chủ đầu tư quyết bằng lời → chọn theo từng tờ: giữ hình học gốc + sửa điểm đã duyệt, hay dựng tham số → cổng bố trí tất định (đường kích thước ≥ 7 mm, tầng ≥ 4 mm giữ tầng gốc, không ra ngoài khung, không chồng/trùng chữ, giữ ký hiệu hàn trong khối ghi chú) → cặp ảnh gốc–mới → ghép bộ + sha256. 17 luật, mỗi luật là một lỗi đã xảy ra thật, mỗi luật có script/test thực thi. Triggers on: 'redraw drawing', 'redraw DXF', 'vẽ lại bản vẽ', 'vẽ lại theo bản gốc', 'chuẩn hoá bản vẽ', 'kích thước quá sát', 'đường kích thước sát', 'kích thước chồng chữ', 'bố trí kích thước', 'tham số hoá bản vẽ', 'sửa bản vẽ theo phiếu', 'ghép bộ bản vẽ', 'dimension spacing', 'dimension layout', 'drawing cleanup'."
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob"]
---

# helix-cad-redraw: Vẽ lại bản vẽ 2D theo gốc + cổng bố trí tất định

> **Vị trí:** khối của [[helix-cad-agents]] (ứng dụng **10**). Tách tờ / đọc khung tên bằng MCP `autocad-bridge`
> (`acad_split_sheets`, `acad_extract_dossier`); ảnh cho người xem qua `helix-cad-ingest/render_dxf.py`.
> **Nguyên tắc:** bản gốc là chuẩn. AI chỉ được thay đổi những gì chủ đầu tư đã duyệt **bằng lời**; mọi thứ khác phải
> giữ như gốc, kể cả cách bố trí kích thước. Cổng xanh ≠ duyệt: chủ đầu tư duyệt **ảnh**.
> **Luật:** `references/redraw-rules.md` (R1–R17 — mỗi luật một lỗi đã xảy ra + chỗ thực thi). Đọc trước khi vẽ.

## Công cụ (tất định, chạy cục bộ — dùng được cả với hồ sơ MẬT)
| Script | Việc | Exit |
|---|---|---|
| `written_vs_drawn.py <dxf>` | lệch nội tại của **bản gốc**: MISMATCH (số ghi ≠ đo), FACTOR (hình chi tiết vẽ tỷ lệ khác nhãn), ROUNDED | 0 / 2 |
| `dim_spacing.py check <dxf…>` | kích thước < 5 mm giấy tới điểm đo; kích thước ra ngoài khung (`outward` / `view`) | 0 / 2 |
| `dim_spacing.py fix <dxf> --orig <gốc>` | giãn ra 7 mm; giữ tầng + phía của **kích thước gốc** (cùng giá trị, cùng phương, cùng điểm đo); dời theo tầng ngoài; xếp tầng; không ra khung; kéo vào khung | 0 |
| `text_overlap.py <dxf…> [--skip-layer L]` | chữ chồng (TEXT/MTEXT/chữ kích thước) + chữ **trùng điểm đặt ở mọi lớp** | 0 / 2 |
| `notes_strokes.py <gốc> <mới> [--write] [--skip N]` | nét rời trong khối «Yêu cầu kỹ thuật» (ký hiệu hàn) còn đủ | 0 / 2 |
| `label_diff.py <gốc> <mới> <tờ…>` | chữ / số kích thước mất – thêm so với gốc | 0 / 2 |
| `sheet_merge.py <MANIFEST> <thư mục tờ> <ra.dxf> [--update-manifest]` | ghép bộ về đúng chỗ, audit, sha256 | 0 / 2 |
| `redraw_helpers.py` (thư viện) | `place_dim_text`, `fix_180`, `stretch`, `explode_named`, `rerender_dims`, `scale_region`, `keep_handles` | — |

Tỷ lệ giấy = `xscale` của INSERT khung tên (`--frame-regex`, mặc định `khung ten|title`); khung = đường bao kín nhỏ
nhất chứa khung tên (dung sai 5 mm).

## Quy trình — MỘT bước mỗi lượt, ghi `_pipeline_state.md`, dừng chờ chủ đầu tư
**R0 Phân loại + tách tờ.** Phân loại hồ sơ (MẬT ⇒ chỉ script cục bộ, không agent LLM đọc hình). `acad_split_sheets` →
thư mục **tờ gốc đã tách** + MANIFEST. Ghi đường dẫn thư mục gốc vào ledger: **mọi script vẽ lại chỉ nhận khuôn từ
đây** (R1).

**R1 Lệch nội tại.** `written_vs_drawn.py` từng tờ + đối chiếu chéo giữa các tờ (cùng chi tiết, số khác nhau).
Trình bảng: *chỗ — số ghi — số đo — đề xuất*. ⛔ Chủ đầu tư trả lời **bằng lời từng điểm** (không bằng nhãn A/B);
ghi nguyên văn vào ledger.

**R2 Cách làm từng tờ.** (A) giữ hình học gốc + sửa điểm đã duyệt (`redraw_helpers.stretch/scale_region`), hoặc
(B) dựng tham số (`PARAMS` + hàm vẽ, khuôn = tờ gốc, giữ nét ghi chú bằng `keep_handles`). Hình cắt sơ đồ ⇒ A.
⛔ Chủ đầu tư chọn.

**R3 Vẽ.** Trước khi đặt kích thước: mở ảnh tờ gốc, chép phía / góc phần tư / tầng (R4). Ø, R: `location=` ra
ngoài + `override={"dimtih":1,"dimtoh":1}`; góc: `add_angular_dim_3p`; chữ đặt tay: `place_dim_text`; góc 180°:
`fix_180`; sau khi sửa hình: `rerender_dims`.

**R4 Cổng bố trí** (chuỗi cố định, từng tờ):
```
dim_spacing.py fix <tờ> --orig <tờ gốc>  →  dim_spacing.py check  →  text_overlap.py  →  notes_strokes.py  →  label_diff.py
```
Còn FAIL: `outward` ⇒ sửa phía/khoảng trong script; `view` ⇒ dời **hình chiếu** trong script (chi tiết sát viền);
chỗ gốc cũng chật ⇒ giữ như gốc, ghi lý do vào ledger (không ép cổng xanh bằng cách khác gốc).

**R5 Ảnh.** Render cặp **gốc | mới** mọi tờ đã đổi (`render_dxf.py`, mặt gạch dày ⇒ bỏ HATCH trong bản sao để
render). ⛔ Chủ đầu tư duyệt ảnh (R15). Người vẽ cũng phải tự mở ảnh: bảng số đã báo xanh cho các lỗi chỉ ảnh mới thấy.

**R6 Ghép bộ.** `sheet_merge.py … --update-manifest` (audit 0, sha256 từng tờ + bản tổng), chạy lại R4 trên **cả
bộ**, ghi biên bản: quyết định → đã làm → còn lại (cố ý / chưa vẽ lại).

## Ledger `_pipeline_state.md`
```markdown
# Redraw — {{bộ bản vẽ}}
Phân loại: {{}} · Tờ gốc đã tách: {{đường dẫn}} · Bộ cuối: {{đường dẫn}}
| Tờ | Cách (A/B) | Script | Cổng R4 | Ảnh duyệt | Ghi chú |
## Quyết định chủ đầu tư (nguyên văn, theo từng điểm)
## Còn lại cố ý (như gốc) / chưa vẽ lại
```

## COD
| Việc | COD |
|---|---|
| Quyết lệch nội tại, chọn A/B, duyệt ảnh | **C** |
| Tách tờ, liệt kê lệch, vẽ, chạy cổng, render, ghép bộ | O |
| Định dạng ledger, sha256 | D |

## Kiểm công cụ
`python -m pytest scripts/test_helix_cad_redraw.py -v` — mỗi luật có script có ≥ 1 test trên bản vẽ tổng hợp.
Đột biến (gỡ đúng chốt ⇒ test đỏ): chốt dời theo · dời theo · tầng gốc · phía gốc · khớp theo điểm đo · xếp tầng ·
vắt ngang cố ý · chọn phía theo nét chắn · không ra khung · kéo vào khung · trùng điểm đặt · `set_location` · 180° ·
dòng chú thích theo dòng trên · ROUNDED. Thêm luật mới ⇒ thêm test + đột biến.

## Gotchas
- ezdxf: bbox của MTEXT không có `width` sai; `width=100000` làm nổ bbox ⇒ dùng `text_overlap.mtext_box`.
- `DimStyleOverride` của ezdxf bản này không có `set_linear_factor` ⇒ `update({"dimlfac": k}); commit()`.
- `dimdec = 0` làm «22,5» hiện «22» ⇒ ghi chữ rõ «22,5».
- `add_diameter_dim` tự thêm «Ø» — đừng gõ «Ø<>».
- DXF đang mở trong AutoCAD bị khoá ghi ⇒ ghi ra thư mục mới; đừng xoá thư mục bằng glob.
- Render tờ có mặt gạch mẫu tỷ lệ rất nhỏ có thể treo ⇒ bỏ HATCH trong bản sao rồi render.
