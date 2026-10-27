---
name: helix-p3-form
description: "Block BF of Phase 3 pipeline (helix-embody-realize), runs between B0 preflight and BA layout — dẫn TỪNG chức năng sang ≥3 phương án hình thể có lập luận bằng C&C² (WFP/LSS/Connector) và quy tắc hiện thân trích từ ba sách TKHT · TKKTHT · KL9, đối chiếu với giải pháp hiện có từ 3 tầng nguồn (hồ sơ dự án → web Exa → sáng chế mới, đọc hình vẽ), kiểm checklist 14 mục P&B, lọc yêu cầu D rồi chấm W thang 0–4 × trọng số HOQ có độ nhạy, hai cổng CEO (duyệt danh sách chức năng; chọn hình thể theo tên phương án), bàn giao khoảng tham số đã khoá + phiếu giả thuyết + kế hoạch thử trên bàn cho BA. Cổng máy p3_form_lint.py. Can run standalone. Triggers on: 'function to form', 'embodiment alternatives', 'form variants per function', 'C&C2 embodiment', 'benchmark existing solutions', 'P3 form block', 'BF form', 'chức năng thành hình thể', 'phương án hiện thân', 'phương án hình thể', 'so sánh giải pháp hiện có', 'đối chiếu giải pháp đã có', 'chọn hình thể cho chức năng'."
---

# Block BF: Form — Chức năng → Hình thể (C&C² + hướng dẫn hiện thân + giải pháp hiện có)

> **P&B:** 7.1 (bước 2–5, phát triển vật mang chức năng chính) + 7.2–7.4 (quy tắc, nguyên tắc hiện thân) | **Pipeline:** helix-embody-realize → Block BF (bắt buộc)
> **Vị trí:** `B0 preflight ──▶ BF form ──▶ BA layout ──▶ BA½ ──▶ BB DfX ──▶ BC ──▶ BD ──▶ BE`
> **Input:** Function_Structure + Requirements_List (D/W) + HOQ + Concept_Selection + B0_Preflight_Report (+ CC2_Handoff nếu có)
> **Output:** `{{prefix}}BF_Function_Selection.md`, `{{prefix}}BF_Form_Variants.md`, `{{prefix}}BF_Benchmark.md`, `{{prefix}}BF_Scoring.md`, `{{prefix}}BF_Form_Selection.md` (+ `{{prefix}}CC2_Handoff.md` nếu chưa có)
> **Spec:** `docs/superpowers/specs/2026-10-27-helix-p3-form-design.md` (§4–§8, §11b, §13 Q6–Q8)

Luận đề: hình thể là giả thuyết. BF không đưa đáp án; nó dựng phương án có lý do trỏ đúng quy tắc sách, đặt cạnh lời giải đã có trên đời, chấm cùng một thước, rồi để CEO chọn — và mọi hình thể được chọn phải đi ra bàn thử.

## Luật cứng

1. **Hai cổng CEO:** Cổng CEO 1 duyệt danh sách chức năng (+ nguyên lý suy ra, + D/W tạm); Cổng CEO 2 chọn hình thể cho từng chức năng. AI không tự qua cổng nào.
2. **≥3 phương án hình thể mỗi chức năng** (`--quick`: ≥2). Phương án chỉ ghi tên nguyên tắc («phân chia nhiệm vụ») mà không nói hình thể đổi gì, tham số nào = không tính.
3. **Mỗi phương án trỏ quy tắc cụ thể** bằng **mã quy tắc** có trong `references/` (`TKHT-Rnnn` / `PB-Rnnn` / `PB-Mnnn` / `KL-Rnnn`) kèm con trỏ sách dạng `[TKHT ChNN §x.y]` / `[TKKTHT ChNN §x.y]` / `[KL9 ChNN §x.y]` chép từ chính dòng của mã đó; không trích câu không có trong tham chiếu, không bịa chương/mục. Lint đối chiếu với references: thiếu mã → `RULE_CODE_MISSING`, mã không có → `RULE_CODE_UNKNOWN`, con trỏ không nằm trong dòng của mã → `CITATION_NOT_IN_RULE`.
4. **Nhãn tri thức bắt buộc** trên mọi phương án và mọi giải pháp hiện có: `tri thức` / `phỏng đoán` / `giả định` (`helix-cc2:references:cc2-core` §Hai loại nhãn).
5. **Không đoán điểm.** Ô thiếu dữ liệu ghi `?(<lý do>)`; điểm cho đối thủ không bịa từ suy đoán.
6. **Quyết định CEO ghi bằng TÊN + mã phương án**, ví dụ `Chọn: PA-1-2 — Vỏ thép lò xo lá`; không bao giờ chỉ một nhãn chữ trần (A/B, «phương án 2») — lỗi đã gặp: quyết định ghi bằng nhãn bị ghi sai.
7. **Analyst Trap:** mỗi hình thể được chọn PHẢI có phiếu giả thuyết + Kế hoạch thử trên bàn. BF không kết thúc bằng một báo cáo phân tích suông (`rules/areas-helix` § Analyst Trap Guard).
8. **Không vẽ hình học / CAD** (việc của BA + `helix-cad-*`). BF dừng ở hình thể mô tả + khoảng tham số. Câu có từ không gian (above, adjacent, coaxial, đồng trục, kề…) mà không dẫn sketch CEO → gắn `[SPATIAL — CEO VERIFY]` như BA.
9. **FTO:** sáng chế còn hiệu lực có liên quan → chỉ ghi `Cờ FTO:` và chuyển `ip-*` (vd. `ip-screen`) / QP-02-06. BF không phán định vi phạm hay hết hiệu lực.
10. **Cổng máy:** `p3_form_lint.py --draft` phải exit 0 trước Cổng CEO 2 (Selection nháp, `Chọn: (chờ CEO)`); sau khi CEO chọn, lint chính thức (không `--draft`) phải exit 0 trước khi bàn giao BA. Báo cáo «đã kiểm» không thay output của lệnh.

## Cờ

```
/helix-p3-form <project> [--variant <V>] [--function <F-id>] [--quick]
```

| Cờ | Tác dụng |
|---|---|
| `--variant <V>` | Thư mục biến thể `<thư mục P3>/<V>/` (giữ nguyên `<V>`), tiền tố `<PROJECT>_<V0>_`; B0 chỉ lấy từ `<thư mục P3>/<V>/`; tiền tố trên tên tệp B0 khác tiền tố tính ra → dừng, hỏi CEO |
| `--function <F-id>` | Chỉ chạy F2–F7 cho một chức năng đã qua Cổng CEO 1. Ghi đè đúng mục `## F-<id>` của nó trong `{{prefix}}BF_Form_Variants.md`, `{{prefix}}BF_Benchmark.md`, `{{prefix}}BF_Form_Selection.md`, và đúng mục `### F-<id>` dưới `## Checklist 14 mục` và dưới `## Bảng chấm` trong `{{prefix}}BF_Scoring.md`; `## Độ nhạy` của `{{prefix}}BF_Scoring.md` là phần dùng chung — chỉ sửa/thêm dòng liên quan tới F này, không xoá phần của F khác |
| `--quick` | Tầng nguồn chỉ 1 (hồ sơ dự án), ≥2 phương án/chức năng; tầng 1 không ra HC nào cho một chức năng → nâng lên tầng 2 (web) cho riêng chức năng đó; lint chạy với `--quick` |
| (orchestrator) `--skip-form "<lý do>"` | Bỏ BF; lý do vào `_pipeline_state.md` Adjustments Log, BE in lại ở báo cáo Gate 3 |

### Nơi ghi và tiền tố (luật VARIANT_SHORT của P3 — giống `helix-embody-realize` §Variant Subfolder Convention và `helix-cc2`)

- `<thư mục P3>` = `1_Projects/<project>/Phase3-Embodiment/` hoặc `Phase3-Embody/` (thư mục đang có). Có cả hai → dừng, hỏi CEO.
- Không variant: ghi vào `<thư mục P3>/`, `{{prefix}}` = `<PROJECT>_` với mọi `-` của PROJECT đổi thành `_` (`VN-XUONG-UUV` → `VN_XUONG_UUV_`).
- Có `--variant <V>`: ghi vào `<thư mục P3>/<V>/`, `{{prefix}}` = `<PROJECT>_<V0>_`, `<V0>` = `<V>` cắt tại dấu `-` đầu tiên (`V5-MOTORIZED` → `VN_MGM_V5_`).
- Áp luật nguyên văn: `VN-TGT-F --variant TGT-10` → thư mục `Phase3-Embodiment/TGT-10/`, tiền tố `VN_TGT_F_TGT_` (KHÔNG phải `VN_TGT_F_TGT10_`).
- ⚠ Hệ quả: TGT-9, TGT-10, TGT-14… cùng ra tiền tố `VN_TGT_F_TGT_`; chỉ thư mục biến thể phân biệt chúng. Không tự chế luật khác — đọc tên tệp `*B0_Preflight_Report.md` của B0 P3: có `--variant <V>` thì CHỈ trong `<thư mục P3>/<V>/`, không variant thì trong `<thư mục P3>/` (không lấy B0 ở Phase1-Task — đó là B0 của P1, pipeline helix-task-clarify). Tiền tố trên tên tệp B0 khác tiền tố tính theo luật trên → dừng, in cả hai, hỏi CEO dùng tiền tố nào. In tiền tố đã chốt ra đầu phiên để CEO thấy.
- Mã chức năng `F-<id>`: `<id>` chỉ gồm chữ/số (lint đọc `F-([A-Za-z0-9]+)`). Function_Structure ghi `F1.2` → dùng `F-12` hoặc `F-1b` và ghi ánh xạ ở `BF_Function_Selection.md`.

## Đầu vào

| Tệp | Nguồn | Bắt buộc | Thiếu thì |
|---|---|---|---|
| `{{prefix}}Function_Structure.md` | P1/P2 | Có | Không dừng: dự phòng R15 — suy danh sách chức năng từ bảng «Yêu cầu quyết định hiện thân» của B0 P3 + Concept_Selection + Requirements, mỗi chức năng nhãn *phỏng đoán*, CEO xác nhận ở Cổng CEO 1; khuyên chạy `/helix-p1-structure` sau |
| `{{prefix}}Requirements_List_v*.md` (đã phân D/W, cột nguồn `HOQ-DPx`) | P1 | Có | Chỉ có `Requirements_Draft*` / chưa phân D/W → chạy D/W tạm (Q6) |
| `HOQ_Design_Parameters_v*.md` | FORGE / P2 | Có | Chấm không trọng số, mọi dòng W cờ 🔴 (Q7) |
| `{{prefix}}Concept_Selection.md` (+ `Morphological_Matrix*`) | P2 | Có | Dừng, chỉ `/helix-p2-select` |
| `{{prefix}}B0_Preflight_Report.md` | B0 của P3 (`--variant`: chỉ trong `<thư mục P3>/<V>/`; không variant: `<thư mục P3>/`) | Có | Dừng, chạy `/helix-p3-preflight` trước |
| `{{prefix}}CC2_Handoff.md` | `/helix-cc2` C6 | Không | F2 tự dựng chuỗi; BF sinh Handoff ở F7 |
| `RE/`, `Phase2-Concept/FTO_*`, `ban-do-sang-che*`, PDF sáng chế trong dự án | dự án | Không | Tầng nguồn 1 rỗng — ghi rõ |

**Glob linh hoạt** (spec §11b): với mỗi tệp, thử lần lượt `{{prefix}}<Tên>*`, `*_<Tên>*`, rồi `<Tên>*` không tiền tố (vd. `BE_Concept_Selection.md`, `Requirements_Draft.md`), trong `Phase2-Concept/<V>/`, `Phase2-Concept/`, `Phase1-Task/<V>/`, `Phase1-Task/`, `Phase0-Forge/` (hoặc `FORGE/`), `Phase0-Plan/<V>/`, `<project>/<V>/`. Riêng B0_Preflight_Report chỉ tìm trong `<thư mục P3>/<V>/` khi có `--variant` (trong `<thư mục P3>/` khi không variant), CC2_Handoff chỉ tìm trong `<thư mục P3>/<V>/` và `<thư mục P3>/` — không lấy B0 ở Phase1-Task — đó là B0 của P1 (vd. `Phase1-Task/VN_TGT_F_B0_Preflight_Report.md` của helix-task-clarify). Nhiều bản → lấy phiên bản cao nhất, in tên tệp đã chọn; không chắc → hỏi CEO.

## Nạp tham chiếu (kỷ luật — không nạp cả tệp)

Bộ tham chiếu ở `references/` (đường dự phòng `~/.claude/commands/helix-p3-form/references/`), chưng cất từ ba sách TKHT (*Thiết kế hiện thân*) · TKKTHT (*Thiết kế kỹ thuật hệ thống*, P&B) · KL9 (*Konstruktionslehre* 9):

| Tệp | Mã | Dùng ở |
|---|---|---|
| `function-index.md` | — | **Cửa vào duy nhất của F3**: loại chức năng → mã quy tắc + câu hỏi mở đầu |
| `tkht-rules.md` | `TKHT-Rnnn` | F2 (§ C&C² 7 bước dựng mô hình), F3, F7 (§ Giả thuyết → thử → tổng hợp) |
| `tkktht-guidelines.md` | `PB-Rnnn`, `PB-Mnnn` | F3; F5 (§ Checklist 14 mục); § Bảng tra mối ghép (§8.1.5); § Đánh giá ở pha hiện thân |
| `kl9-gestaltung.md` | `KL-Rnnn` | F3 (phần khác/mới hơn TKKTHT), F4 (sở hữu công nghiệp KL-R119…R125) |
| `benchmark-search.md` | — | F4: 3 tầng, truy vấn theo chức năng, khuôn hồ sơ HC |
| `scoring.md` + `templates/scoring-template.txt` | — | F6: thang 0–4, ánh xạ DP, luật ô `?`, Q6/Q7, độ nhạy, khuôn bảng |

Cách nạp: đọc `function-index.md` (24 dòng) → với mỗi mã cần, `LC_ALL=C.UTF-8 grep -n "<mã>" references/<tệp>.md` rồi chỉ đọc dòng đó (grep tiếng Việt phải có `LC_ALL=C.UTF-8`, nếu không ra âm tính giả). Mục lớn (checklist, bảng tra mối ghép) đọc theo tiêu đề `##` bằng `sed -n '/^## <tiêu đề>/,/^## /p'`. Loại chức năng không có trong chỉ mục → grep từ khoá trong ba kho, ghi mã tìm được.

Nguồn C&C² dùng chung (không chép lại): `helix-cc2:references:cc2-core` (từ vựng, 7 bước, §Hai loại nhãn), `helix-cc2:references:view-ops` (zoom-in/zoom-out/shift/state/view/observe), `helix-cc2:references:synthesis-moves` (nước đi tổng hợp), `helix-cc2:references:hypothesis-sheet` (§Khuôn phiếu, §Khuôn kế hoạch thử trên bàn thử), `helix-cc2:references:param-bridge` (§Dải đã kiểm, §Độ nhạy và thứ hạng).

## Quy trình F1 → F7

### F1 — Chọn chức năng (Core · Cổng CEO 1)

1. Đọc Function_Structure × danh sách «yêu cầu quyết định hiện thân» trong B0_Preflight_Report của P3. **Không có Function_Structure (R15):** suy danh sách chức năng từ bảng «Yêu cầu quyết định hiện thân» của B0 P3 + Concept_Selection + Requirements, gắn mỗi chức năng suy ra nhãn *phỏng đoán*, in ở đầu `BF_Function_Selection.md` câu «Chưa có cấu trúc chức năng P1 — danh sách dưới đây suy từ B0 P3 + Concept_Selection + Requirements, nhãn phỏng đoán, chờ CEO xác nhận tại Cổng CEO 1; nên chạy /helix-p1-structure sau.» Đề xuất các chức năng cần đi qua BF, xếp theo mức quyết định hiện thân (chức năng nào mà hình thể sai thì hỏng sản phẩm đứng đầu).
2. Gán mỗi chức năng một (hoặc hai) **loại chức năng** theo hàng của `function-index.md`.
3. **Nguyên lý làm việc của từng chức năng con:** P2 thường chỉ chọn khái niệm cấp hệ → suy nguyên lý từng chức năng con từ Concept_Selection (+ Morphological_Matrix nếu có), gắn nhãn *phỏng đoán*, đưa CEO xác nhận ở Cổng CEO 1.
4. **D/W tạm (Q6):** danh sách yêu cầu chưa phân D/W hoặc chỉ có Requirements_Draft → BF đề xuất D/W, MỌI dòng ghi `D tạm` / `W tạm` cho tới khi CEO duyệt tại Cổng CEO 1; đầu `BF_Scoring.md` in câu đang dùng phân loại D/W tạm; BE không được khuyến nghị qua Gate 3 khi còn nhãn tạm.
5. Ghi `{{prefix}}BF_Function_Selection.md`, in bảng, hỏi CEO: thêm/bớt chức năng, xác nhận nguyên lý, duyệt D/W. Chức năng bị bỏ ghi lý do. CEO duyệt → ghi ngày + quyết định vào `_pipeline_state.md`.

### F2 — Mô hình C&C² của nguyên lý đã chọn (Offload)

- Có `{{prefix}}CC2_Handoff.md` → **nhập** chuỗi đã chọn và bảng tham số theo chức năng con, không dựng lại; chỉ dựng cho chức năng không có trong Handoff.
- Chưa có → mỗi chức năng ≥1 chuỗi WFP → LSS → … → WFP đóng kín, có mô hình môi trường (Connector ra ngoài hệ), theo 7 bước `cc2-core` / `tkht-rules § C&C² 7 bước dựng mô hình`; đổi góc nhìn bằng `view-ops` khi chuỗi chưa đóng.
- Mỗi quan hệ «do hình thể X nên chức năng Y» mang nhãn tri thức / phỏng đoán / giả định.

### F3 — Sinh phương án hình thể (Offload)

Với mỗi chức năng, dựng **≥3 phương án hình thể** khác nhau thật (khác WFP, LSS hoặc Connector — không chỉ khác kích thước), bằng nước đi của `synthesis-moves` và mã quy tắc từ `function-index.md`. Bắt đầu bằng «Câu hỏi mở đầu» của hàng chỉ mục. Mỗi phương án ghi:
- thay đổi trên chuỗi C&C² (WFP nào, LSS nào, Connector nào);
- `Nguồn quy tắc:` — mã + con trỏ sách, ví dụ `TKHT-R300 [TKHT Ch13b §13b.9]`, chỉ trỏ quy tắc có «điều kiện đúng» khớp hoàn cảnh;
- `Tham số khoá:` — tham số bị khoá + con số/khoảng nếu sách cho, kèm điều kiện đúng (sách không cho số → `—` kèm tên tham số, không bịa số);
- kiểu hỏng khi vi phạm (từ ô «Kiểu hỏng» của quy tắc);
- `Nhãn:` tri thức / phỏng đoán / giả định.

### F4 — Giải pháp hiện có, 3 tầng (Offload)

Theo `benchmark-search.md`, đi đúng thứ tự: tầng 1 hồ sơ dự án → tầng 2 web → tầng 3 sáng chế mới:
1. **Tầng 1 — hồ sơ dự án:** `RE/*`, `Phase2-Concept/FTO_*`, `ban-do-sang-che*`, PDF sáng chế trong thư mục dự án; `Nguồn:` ghi đường dẫn tương đối.
2. **Tầng 2 — web:** `mcp__exa__web_search_exa` để tìm, `mcp__exa__web_fetch_exa` để đọc; truy vấn theo **chức năng** (động từ + điều kiện), không theo tên sản phẩm; chỉ ghi nguồn đã mở đọc.
3. **Tầng 3 — sáng chế:** Exa trên patents.google.com / Espacenet; ưu tiên công bố ≤ 5 năm; ĐỌC HÌNH VẼ (figures) và claims, không chỉ tóm tắt/thuyết minh — số chú thích trên hình là chỗ lộ WFP/LSS. Không mở được hình vẽ → nhãn `giả định`, ghi «chưa đọc hình».

Tối đa **≤8 giải pháp (HC) mỗi chức năng**; dừng sớm khi giải pháp mới chỉ lặp một chuỗi C&C² đã có. Mỗi HC: nguồn (URL / số công bố / tệp), ngày truy cập, **chuỗi C&C² đọc ngược** (đọc sáng chế bằng bảng WFP/LSS/Connector của `reverse-engineering:references:cc2-lens`; nếu không có, dùng `helix-cc2:references:cc2-core`), nhãn tri thức, `Cờ FTO:` nếu có. `--quick` chỉ tầng 1, nhưng tầng 1 trống cho chức năng nào thì nâng lên tầng 2 cho chức năng đó.

**Không tìm được HC nào:** chức năng kết thúc F4 với 0 HC phải có trong mục `## F-<id>` của `{{prefix}}BF_Benchmark.md` dòng `- Không tìm thấy HC — lý do: <các tầng đã tìm + truy vấn chính + vì sao không có>` (lý do không rỗng; lint chấp nhận thay cho HC, thiếu dòng hoặc lý do rỗng → `NO_BENCH`). Bảng chấm của chức năng đó khi ấy chỉ có cột PA.

### F5 — Checklist 14 mục P&B (Offload)

Áp `tkktht-guidelines § Checklist 14 mục` (TKKTHT Ch13, Figure 7.3) **cho từng chức năng**: trong `## Checklist 14 mục` của `{{prefix}}BF_Scoring.md`, mỗi chức năng một mục `### F-<id>` với bảng `| # | Mục | Tiêu chí | <mọi PA/HC của F này> |`, đủ 14 dòng đánh số 1–14 (tên mục đúng như `tkktht-guidelines`), ≥1 tiêu chí kiểm cho **mỗi** mục, xét lần lượt từng mục. Ô ứng viên chỉ nhận `Đạt` / `Không đạt` / `?(<lý do>)`. Bỏ mục nào thì cột Tiêu chí ghi `Bỏ — lý do: …` và mọi ô ứng viên của dòng đó là `—` (cơ chế, không phải lời khuyên). Lint: thiếu bảng/dòng → `CHECKLIST_INCOMPLETE`; bỏ không lý do → `CHECKLIST_SKIP_NO_REASON`; thiếu cột PA/HC → `CHECKLIST_CANDIDATE_MISSING`; ô ngoài miền → `BAD_CELL`. Áp lên cả phương án mình (PA) và giải pháp hiện có (HC) ở **cùng mức cụ thể hoá** (PB-R175) — HC chi tiết hơn PA thì hạ về mức mô tả của PA.

### F6 — Chấm định lượng (Offload)

Theo `scoring.md` và khuôn `references/templates/scoring-template.txt` (dán nguyên, thay giá trị — không chép lại khuôn vào đây):
- **Lọc:** mọi yêu cầu D → lọc trước, ô `Đạt` / `Loại` / `?(lý do)`. `Loại` → phương án ra khỏi vòng chọn; `?` → giữ, cờ.
- **Chấm:** mỗi yêu cầu W liên quan đến chức năng, thang 0–4 (VDI 2225) × trọng số HOQ (ánh xạ yêu cầu → DP qua cột nguồn `HOQ-DPx`). Chấm đúng DP, không chấm ấn tượng chung.
- **W không có DP / HOQ chỉ là proxy (Q7):** giữ dòng, ô Trọng số trống, DP `—`, Ghi chú `🔴 CEO gán trọng số`. Tổng in hai cột: phần có trọng số, và phần cờ đỏ chưa gán — không cộng gộp.
- **Ô thiếu dữ liệu:** `?(<lý do>)`, không đoán. Điểm của HC mang nhãn tri thức của nguồn.
- **Độ nhạy:** trọng số ±20% và ô `?` lấy 0 rồi 4 — thứ hạng có đổi không; in «dẫn đầu vững» / «dẫn đầu mong manh» + ô `?` nào quyết định (→ đi vào kế hoạch thử).
- **Ưu/nhược bằng lời** dưới mỗi bảng, 1–2 câu cho mỗi ứng viên, để CEO đọc được mà không cần bảng.

### Cổng máy (hai lần: nháp trước Cổng CEO 2, chính thức sau Cổng CEO 2)

```
python -X utf8 D:/KN-Stack/scripts/p3_form_lint.py <thư mục P3 hoặc thư mục biến thể> --prefix <PREFIX> [--quick] --draft   # trước Cổng CEO 2
python -X utf8 D:/KN-Stack/scripts/p3_form_lint.py <thư mục P3 hoặc thư mục biến thể> --prefix <PREFIX> [--quick]           # sau Cổng CEO 2, trước BA
```

Ví dụ: `python -X utf8 D:/KN-Stack/scripts/p3_form_lint.py "D:/Workshop_X/1_Projects/VN-TGT-F/Phase3-Embodiment/TGT-10" --prefix VN_TGT_F_TGT_ --draft`.

- **Lần nháp (`--draft`):** lint đọc cả `{{prefix}}BF_Form_Selection.md`, nên trước Cổng CEO 2 ghi tệp này ở dạng nháp (khuôn «nháp» bên dưới): mỗi `## F-<id>` có `Chọn: (chờ CEO)` — **KHÔNG điền sẵn ứng viên dẫn đầu, không ghi mã PA/HC nào trong `Chọn:`** (lint báo `SELECTION_DRAFT`) — cùng `Khoảng tham số:` và `Kế hoạch thử:` nháp. Không mở Cổng CEO 2 khi lần nháp chưa exit 0.
- **Lần chính thức (không `--draft`):** sau khi CEO chọn, ghi Selection chính thức (khuôn bên dưới) rồi chạy lại; lint đòi đúng một dòng `Cổng CEO 2 — ngày YYYY-MM-DD` (`NO_GATE2_DATE`), `Chọn: <PA-/HC-mã> — <tên>` (`SELECTION_NO_NAME`), `Lý do CEO:` không rỗng mỗi F (`NO_CEO_REASON`), và không còn `chờ CEO`/`đề xuất` (`SELECTION_DRAFT`). Chưa exit 0 → không bàn giao BA.

Exit 0 = sạch; exit 1 → sửa đúng dòng lint báo (mã lỗi trong docstring script) rồi chạy lại; exit 2 → lỗi đường dẫn/tệp. In nguyên output + mã thoát của cả hai lần vào `_pipeline_state.md`.

### F7 — Cổng CEO 2 + bàn giao (Core)

1. Trình CEO, mỗi chức năng: top-3 theo điểm có trọng số, cờ 🔴 chưa gán, ô `?` quyết định, kết luận độ nhạy, ưu/nhược bằng lời, cờ FTO. Không khuyến nghị «chọn X» thay CEO.
2. CEO chọn hình thể (PA hoặc HC) cho từng chức năng → ghi `Chọn: <mã> — <tên phương án>` + `Lý do CEO:` (lời CEO) + dòng đầu tệp `Cổng CEO 2 — ngày YYYY-MM-DD`; CEO có thể gán trọng số cho dòng 🔴 và chốt D/W tạm ở đây.
3. Khoá **khoảng tham số** cho phương án chọn (từ `Tham số khoá` của F3 + `param-bridge` §Dải đã kiểm; không ngoại suy ra ngoài dải).
4. **Phiếu giả thuyết + Kế hoạch thử trên bàn** cho tham số nhạy nhất của mỗi hình thể chọn, theo `hypothesis-sheet` §Khuôn phiếu (9 mục, «Phép thử nhỏ nhất để bác bỏ», dự đoán viết trước do CEO ký) — đầu ra vật lý bắt buộc. Ô `?` quyết định thứ hạng ở F6 → thành một phép thử trong kế hoạch.
5. Ghi `{{prefix}}BF_Form_Selection.md` chính thức, chạy lint chính thức (không `--draft`) → phải exit 0 trước khi bàn giao BA, sinh `{{prefix}}CC2_Handoff.md` nếu chưa có, cập nhật `_pipeline_state.md`, in tóm tắt 3–5 dòng, hỏi CEO «tiếp BA / sửa / dừng».

## Khuôn đầu ra

Tiêu đề và nhãn trường dưới đây là thứ `p3_form_lint.py` đọc — giữ nguyên chữ, dấu và thứ tự cấp `##`/`###`.

### `{{prefix}}BF_Function_Selection.md` (không lint; BF Cổng CEO 1, BE đọc)

```markdown
# Chọn chức năng đi qua BF — {{project}} / {{variant}}

Tiền tố: {{prefix}} · Nguồn: {{tệp Function_Structure, B0, Concept_Selection, Requirements đã chọn}}
Phân loại yêu cầu: {{chính thức | D/W tạm, chờ CEO duyệt tại Cổng CEO 1}}

| F-id | Chức năng (mã gốc) | Loại chức năng (function-index) | Nguyên lý làm việc | Nhãn nguyên lý | Yêu cầu quyết định hiện thân | Đề xuất |
|---|---|---|---|---|---|---|
| F-1 | {{tên}} ({{F1.2}}) | {{hàng chỉ mục}} | {{từ Concept_Selection}} | phỏng đoán | R-11 (D tạm), R-12 (W tạm) | đi qua BF |

## Chức năng không đi qua BF
- {{F-id}} — {{lý do}}

## Cổng CEO 1
- Ngày: {{YYYY-MM-DD}} · Quyết định: {{danh sách F-id duyệt, nguyên lý xác nhận, D/W đã chốt hay còn tạm}}
```

### `{{prefix}}BF_Form_Variants.md`

```markdown
# Phương án hình thể

## F-<id> — <tên chức năng>

Chuỗi C&C² nền: <WFP1 → LSS1 → Connector → WFP2> (Nhãn: <tri thức | phỏng đoán | giả định>; nhập từ CC2_Handoff | dựng ở F2)

### PA-<id>-1 — <tên phương án>
- Thay đổi C&C²: <WFP/LSS/Connector nào đổi, đổi thế nào>
- Nguồn quy tắc: <TKHT-Rnnn> [TKHT ChNN §x.y], <KL-Rnnn> [KL9 ChNN §x.y]   (mã có trong references/; con trỏ chép từ đúng dòng của mã, vd. «TKHT-R300 [TKHT Ch13b §13b.9]»)
- Tham số khoá: <tham số = con số/khoảng; điều kiện đúng>
- Kiểu hỏng khi vi phạm: <từ sách>
- Nhãn: <tri thức | phỏng đoán | giả định>
```

### `{{prefix}}BF_Benchmark.md`

```markdown
# Chuẩn đối sánh

## F-<id> — <tên chức năng>

### HC-<id>-1 — <tên giải pháp>
- Nguồn: <URL đầy đủ | số sáng chế như US 9,097,498 B2 | đường dẫn RE/…>
- Truy cập: <YYYY-MM-DD>
- Nhãn: <tri thức | phỏng đoán | giả định>
- Chuỗi C&C²: <WFP1 → LSS1 → Connector → WFP2>
- Cờ FTO: <tuỳ chọn: số sáng chế; lãnh thổ; chuyển ip-* / QP-02-06>

## F-<id> — <tên chức năng không có HC>
- Không tìm thấy HC — lý do: <tầng 1: RE/, FTO_* …; tầng 2: Exa web «<truy vấn>»; tầng 3: Exa patents «<truy vấn>» — không có lời giải cùng chức năng>
```

### `{{prefix}}BF_Scoring.md`

Dán nguyên `references/templates/scoring-template.txt`. Bố cục lint đòi: `# Bảng chấm` → `## Checklist 14 mục` với một `### F-<id>` mỗi chức năng (bảng `# | Mục | Tiêu chí | PA-<id>-1 | … | HC-<id>-1 | …`, mọi PA/HC của F có cột, đủ dòng 1–14, ô `Đạt`/`Không đạt`/`?(<lý do>)`; mục bỏ: Tiêu chí `Bỏ — lý do: …`, ô ứng viên `—`) → `## Bảng chấm` với một `### F-<id>` mỗi chức năng (bảng `Req-ID | D/W | DP | Trọng số | PA-<id>-1 | … | HC-<id>-1 | … | Ghi chú`, mọi PA/HC đã khai đều có cột) → `## Độ nhạy`. Ô D: `Đạt`/`Loại`; ô W: `0`–`4`; ô thiếu: `?(<lý do>)`; Trọng số trống: dòng W phải có `🔴`, dòng D được để trống.

### `{{prefix}}BF_Form_Selection.md` — nháp (trước Cổng CEO 2, lint `--draft`)

```markdown
# Chọn hình thể (nháp — chờ Cổng CEO 2)

## F-<id> — <tên chức năng>
- Chọn: (chờ CEO)
- Khoảng tham số: <nháp: tham số = khoảng từ Tham số khoá F3>
- Kế hoạch thử: <nháp: bàn thử, đại lượng đo cho ô ? quyết định>
```

### `{{prefix}}BF_Form_Selection.md` — chính thức (sau Cổng CEO 2, lint không `--draft`)

```markdown
# Chọn hình thể

Cổng CEO 2 — ngày YYYY-MM-DD · lint p3_form_lint: exit 0

## F-<id> — <tên chức năng>
- Chọn: <id> — <tên>
- Lý do CEO: <lời CEO, không rỗng>
- Khoảng tham số: <tham số = khoảng đã khoá; nguồn số; nhãn>
- Kế hoạch thử: <bàn thử, số mẫu, đại lượng đo, ngày thử; phiếu GT-nnn>

(khối text PHIẾU GIẢ THUYẾT — GT-nnn theo helix-cc2:references:hypothesis-sheet §Khuôn phiếu, mục 7 để CEO ký)
```

### `{{prefix}}CC2_Handoff.md` (chỉ sinh khi chưa có)

Đúng định dạng C6 của `helix-cc2-handoff` §Khuôn đầu ra: `{{prefix}}CC2_Handoff.md` (giữ nguyên các mục `## Chuỗi đã chọn theo chức năng con`, `## Tham số hình thể và khoảng chọn`, `## Tham số nhạy`, `## Phiếu giả thuyết đang mở`, `## Kế hoạch thử`, `## Chỗ C&C² không áp dụng`, `## Vòng lặp P3`), với: «Phương án đi tiếp» = `<mã> — <tên>` từ BF_Form_Selection; cột «Ngày Cổng CEO 3» ghi ngày Cổng CEO 2 của BF kèm chữ «(BF)»; thêm dòng `nguồn: helix-p3-form BF` ở frontmatter. Đã có Handoff từ `/helix-cc2` → không ghi đè; hình thể chọn ở BF khác Handoff → ghi chỗ khác vào BF_Form_Selection và báo CEO.

## Data Bus

| Tệp | Đọc bởi |
|---|---|
| `{{prefix}}BF_Function_Selection.md` | BF (Cổng CEO 1), BE |
| `{{prefix}}BF_Form_Variants.md` | BA, BB |
| `{{prefix}}BF_Benchmark.md` | BE, `ip-*` |
| `{{prefix}}BF_Scoring.md` | BE |
| `{{prefix}}BF_Form_Selection.md` | **BA** (nguồn khoảng tham số — đổi khoảng phải quay lại BF; BA từ chối Selection trượt lint chính thức), BB, BE, Phase 4 |
| `{{prefix}}CC2_Handoff.md` | BA (hợp đồng cũ giữ nguyên) |

BF chọn hình thể **theo chức năng**; BE vẫn chấm Rt/Re ở mức layout. BA có thể ra nhiều phương án *bố trí* từ các hình thể đã chọn.

`_pipeline_state.md`: dòng BF ghi `✓ F-ids {{n}} · PA {{n}} · HC {{n}} · lint exit 0 · Cổng CEO 1 {{ngày}} · Cổng CEO 2 {{ngày}}` hoặc lý do dừng; bảng cổng ghi quyết định CEO bằng tên + mã.

## COD

| Việc | Lớp | Ai |
|---|---|---|
| F1 chọn chức năng, xác nhận nguyên lý, duyệt D/W (Cổng CEO 1) | **C** Core | CEO |
| F2 mô hình C&C², F3 sinh phương án, F4 tìm giải pháp hiện có, F5 checklist, F6 dựng bảng chấm | **O** Offload | AI, CEO soát |
| F7 chọn hình thể, gán trọng số 🔴, ký dự đoán phiếu (Cổng CEO 2) | **C** Core | CEO — AI không chọn, không ký |
| Chạy `p3_form_lint.py`, cập nhật `_pipeline_state.md` | **D** Default | tự động |

## Chạy riêng

`/helix-p3-form <project> [--variant <V>] [--function <F-id>] [--quick]` — cần B0 đã chạy trong cùng thư mục P3/biến thể; thiếu B0 → dừng, chỉ `/helix-p3-preflight`. Kết thúc: in đường dẫn 5 tệp, mã thoát lint, ngày thử sớm nhất, và nhắc bước kế: `/helix-p3-layout` (BA) đọc `BF_Form_Selection.md`.

## Integration

- **Trước:** `helix-p3-preflight` (B0) — danh sách yêu cầu quyết định hiện thân; `helix-cc2` (C0–C6) — nếu đã chạy, BF nhập Handoff.
- **Sau:** `helix-p3-layout` (BA) — khoảng tham số đã khoá; `helix-p3-dfx` (BB) — kiểm layout bằng hướng dẫn mà BF đã dùng để sinh; `helix-p3-compile` (BE) — nhất quán layout ↔ hình thể chọn, cấm qua Gate 3 khi còn D/W tạm.
- **Cạnh:** `ip-*` / QP-02-06 (cờ FTO), `reverse-engineering` (tầng 1, đọc sáng chế bằng C&C²), `analyst-trap` (mọi đầu ra dẫn tới bàn thử).
