# helix-p3-form — Khối P3 «Chức năng → Hình thể» (C&C² + hướng dẫn hiện thân + đối chiếu giải pháp hiện có)

> Spec thiết kế · 2026-10-27 · người yêu cầu: CEO · trạng thái: CHỜ CEO DUYỆT
> Dự án chạy thử đầu: `D:\Workshop_X\1_Projects\VN-TGT-F` (TGT-10)

## 1. Ý định và lý do

Khi chạy P3 (Thiết kế Hiện thân) cho VN-TGT-F, CEO thấy **thiếu bước C&C²**: layout (BA) đi thẳng vào kích thước
và bố trí, không có chỗ nào dẫn **từng chức năng** sang **các phương án hình thể có lập luận**, rồi đánh giá và so
với giải pháp đã có trên đời cho cùng chức năng đó.

Hiện trạng đã kiểm (2026-10-27):
- Bộ `/helix-cc2` (C0→C6) tồn tại nhưng **nằm cạnh** P3: P3 chỉ đọc `CC2_Handoff.md` như đầu vào *khuyến nghị*
  (`helix-embody-realize` §1.5a); thiếu tệp thì P3 vẫn chạy, không báo.
- Hướng dẫn hiện thân trong `helix-cc2:references:embodiment-rules` chỉ là chỉ mục 54 dòng — mỏng so với ba cuốn
  sách đã làm (≈ 900 nghìn từ).
- Không có bước nào so phương án với **giải pháp hiện có** (RE, sáng chế, thị trường).
- Không có chấm định lượng phương án hình thể theo danh sách yêu cầu P1 × trọng số HOQ.

CEO muốn: từ các chức năng → phân tích cụ thể các giải pháp hiện thân có thể có bằng C&C² + hướng dẫn hiện thân **cụ
thể, ứng dụng cao** → hình thành hình thể → đánh giá ưu nhược → so với giải pháp hiện có cho chức năng đó.

## 2. Quyết định của CEO (nguyên văn ý)

| # | Quyết định |
|---|---|
| Q1 | Viết **một khối P3 riêng** (không mở rộng `/helix-cc2`). |
| Q2 | **Áp dụng đầy đủ** ba sách: `3_Resources/Books/thiet-ke-ky-thuat-he-thong` (TKKTHT), `thiet-ke-hien-than` (TKHT), `pahl-beitz-konstruktionslehre` (KL9). |
| Q3 | Giải pháp hiện có: **tư liệu trong dự án + tìm thêm trên web + sáng chế mới** mỗi lần chạy. |
| Q4 | Đánh giá: **chấm định lượng theo danh sách yêu cầu P1 và trọng số HOQ**. |
| Q5 | Bước này là khối **bắt buộc** trong P3, chạy **trước layout** (CEO không phản đối đề xuất). |

## 3. Mục tiêu · không-mục-tiêu · phản-mục-tiêu

**Mục tiêu**
1. Với mỗi chức năng quyết định hiện thân: ≥3 phương án hình thể dựng bằng C&C² (WFP/LSS/Connector), mỗi phương án
   có lý do trỏ **quy tắc cụ thể** trong ba sách (sách·chương·mục) và **tham số bị khoá** kèm con số/khoảng nếu sách có.
2. Với cùng chức năng: danh sách giải pháp hiện có từ 3 tầng nguồn, mỗi giải pháp **đọc ngược thành chuỗi C&C²** để
   so cùng ngôn ngữ.
3. Một bảng chấm duy nhất: phương án của mình + giải pháp hiện có, lọc D, chấm W × trọng số HOQ, có độ nhạy.
4. CEO chọn hình thể cho từng chức năng ở cổng → BA layout nhận **khoảng tham số đã khoá** + kế hoạch thử trên bàn.

**Không-mục-tiêu**
- Không vẽ hình học / CAD (đó là BA + `helix-cad-*`). Khối này dừng ở mức hình thể mô tả + khoảng tham số.
- Không thay BB DfX: BB vẫn **kiểm** layout sau; khối mới dùng hướng dẫn để **sinh và chọn** hình thể.
- Không thay `/helix-cc2` cho việc dùng độc lập (ngoài dự án, `--analyze`, `--improve`).

**Phản-mục-tiêu (chạy được mà vẫn là thất bại)**
- Phương án chỉ ghi tên nguyên tắc («áp dụng phân chia nhiệm vụ») mà không nói hình thể đổi gì, tham số nào.
- Điểm số cho giải pháp đối thủ bịa từ suy đoán mà không gắn nhãn tri thức / không nêu ô thiếu dữ liệu.
- Trích sách sai chương/mục, hoặc «trích» câu không có trong sách (lớp lỗi đã gặp nhiều lần ở pipeline sách).
- Khối sinh thêm báo cáo phân tích mà không dẫn tới kế hoạch thử vật lý (Analyst Trap — `rules/areas-helix`).
- Sáu khối P3 hiện có bị gãy hợp đồng tệp (BA không còn tìm thấy đầu vào cũ).

## 4. Vị trí trong P3

```
B0 preflight ──▶ BF form (MỚI) ──▶ BA layout ──▶ BA½ ──▶ BB DfX ──▶ BC ──▶ BD ──▶ BE
                    ✓CEO: chọn hình thể / chức năng
```

- Skill: `skills/helix/helix-p3-form/SKILL.md`, ID khối **BF**.
- Bắt buộc. Bỏ qua chỉ bằng cờ orchestrator `--skip-form "<lý do>"`; lý do ghi vào `_pipeline_state.md`
  (Adjustments Log) và BE in lại ở báo cáo Gate 3.
- `--quick`: BF vẫn chạy nhưng tầng nguồn chỉ 1 (tư liệu dự án), 2 phương án/chức năng. *(quyết định của tôi)*
- Chạy độc lập được: `/helix-p3-form <project> [--variant <V>] [--function <F-id>]`.

## 5. Đầu vào

| Tệp | Nguồn | Bắt buộc |
|---|---|---|
| `{{prefix}}Function_Structure.md` | P1/P2 | Có |
| `{{prefix}}Requirements_List_v*.md` (đã phân D/W) | P1 | Có — thiếu/chưa phân D/W: xem §13 |
| `HOQ_Design_Parameters_v*.md` | FORGE / P2 | Có (thiếu → chấm không trọng số, đánh dấu ĐỎ) |
| `{{prefix}}Concept_Selection.md` (+ `Morphological_Matrix`) | P2 | Có — nguyên lý làm việc đã chọn cho từng chức năng con |
| `{{prefix}}B0_Preflight_Report.md` | B0 | Có — danh sách yêu cầu quyết định hiện thân |
| `{{prefix}}CC2_Handoff.md` | `/helix-cc2` | Không — có thì **nhập** chuỗi C&C², không dựng lại |
| `RE/`, `Phase2-Concept/FTO_*`, sáng chế PDF trong dự án | dự án | Không — tầng nguồn 1 |

## 6. Quy trình bên trong khối BF

**F1 — Chọn chức năng.** Từ Function_Structure × B0 (yêu cầu quyết định hiện thân), đề xuất danh sách chức năng cần
đi qua BF, xếp theo mức quyết định hiện thân. **Cổng CEO 1:** duyệt danh sách (thêm/bớt). Chức năng bị bỏ ghi lý do.

**F2 — Mô hình C&C² của nguyên lý đã chọn.** Mỗi chức năng: ≥1 chuỗi WFP–LSS–Connector đóng kín, có mô hình môi
trường (Connector ra ngoài hệ), dùng lại `helix-cc2:references:cc2-core`, `view-ops`. Có `CC2_Handoff` → nhập.

**F3 — Sinh phương án hình thể (≥3/chức năng).** Dùng phép tổng hợp (`helix-cc2:references:synthesis-moves`) và
**chỉ mục chức năng → hướng dẫn** (§7). Mỗi phương án ghi:
- thay đổi trên chuỗi C&C² (WFP nào, LSS nào, Connector nào);
- quy tắc áp dụng — trỏ `[TKHT ChNN §x]` / `[TKKTHT ChNN]` / `[KL9 ChNN / Kap. x]`;
- tham số bị khoá + khoảng/con số nếu sách cho, kèm điều kiện đúng của quy tắc;
- kiểu hỏng khi vi phạm (từ sách);
- nhãn tri thức: *tri thức / phỏng đoán / giả định* (đúng quy ước bộ helix-cc2).

**F4 — Giải pháp hiện có (3 tầng).**
1. Tầng 1 — dự án: `RE/*`, `FTO_*`, `ban-do-sang-che*`, PDF sáng chế trong thư mục dự án.
2. Tầng 2 — web: Exa (`mcp__exa__web_search_exa`, `web_fetch_exa`) theo **chức năng** (không theo tên sản phẩm).
3. Tầng 3 — sáng chế mới: Google Patents / Espacenet qua Exa; ưu tiên công bố ≤ 5 năm; **đọc hình vẽ**, không chỉ
   phần thuyết minh (bài học RE sáng chế).
Mỗi giải pháp: nguồn (URL / số công bố / tệp), ngày truy cập, chuỗi C&C² đọc ngược, nhãn tri thức. Sáng chế còn hiệu
lực có liên quan → cờ FTO (không phán định, chỉ chuyển `ip-*`/QP-02-06). Giới hạn ≤ 8 giải pháp/chức năng *(quyết
định của tôi)*.

**F5 — Kiểm theo checklist 14 mục P&B** (TKKTHT Ch13, Figure 7.3): ≥1 tiêu chí cho **mỗi** mục; bỏ mục phải ghi lý do
(TKKTHT Ch22 §7.6 — cơ chế, không phải lời khuyên). Áp lên cả phương án mình và giải pháp hiện có, **cùng mức cụ thể hoá**.

**F6 — Chấm định lượng.**
- Lọc: mọi yêu cầu **D** → đạt / không đạt / chưa biết. Không đạt → loại; chưa biết → giữ, cờ.
- Chấm: mỗi yêu cầu **W** liên quan đến chức năng, thang 0–4 (VDI 2225), × trọng số HOQ (ánh xạ yêu cầu → DP qua cột
  nguồn `HOQ-DPx` của danh sách yêu cầu). Ra điểm có trọng số và Rt.
- W không có DP / HOQ proxy: giữ, cờ ĐỎ, trọng số trống (§13 Q7).
- Ô thiếu dữ liệu: ghi `?` + lý do; **không đoán điểm**. Điểm cho giải pháp hiện có gắn nhãn tri thức của nguồn.
- Độ nhạy: thứ hạng có đổi khi trọng số ±20% hoặc ô `?` lấy 0/4 không; in rõ.
- Ưu/nhược bằng lời đi kèm từng hàng (CEO đọc được không cần bảng).

**F7 — Cổng CEO 2 + bàn giao.** CEO chọn hình thể cho từng chức năng (ghi quyết định bằng **tên phương án**, không chỉ
nhãn chữ). Sinh phiếu giả thuyết + kế hoạch thử trên bàn cho phương án chọn (`helix-cc2:references:hypothesis-sheet`)
→ đầu ra vật lý bắt buộc.

## 7. Bộ tham chiếu chưng cất từ ba sách (phần lớn công việc)

Thư mục `skills/helix/helix-p3-form/references/`:

| Tệp | Nguồn | Nội dung |
|---|---|---|
| `tkht-rules.md` | TKHT Ch01–Ch20 (đọc `Phase6-Revised/` hoặc `book.md`) | Mỗi quy tắc: điều kiện đúng · câu hỏi kiểm hình thể · tham số khoá · con số/khoảng · ví dụ sách · kiểu hỏng · `[TKHT ChNN §x]`. Gồm C&C² 7 bước (Ch02a), giả thuyết kết cấu (Ch03a/b), nổi-ổn định (Ch05b), nhôm hàn (Ch13b), ca TG-2 (Ch20). |
| `tkktht-guidelines.md` | TKKTHT Tập 1 Ch13–Ch28 (+ Tập 2 chỗ trỏ) | 15 bước + 3 cổng; **checklist 14 mục** đầy đủ kèm câu hỏi; clarity/simplicity/safety; truyền lực; chia nhiệm vụ/tự trợ/ổn định/không lỗi; nhiệt-ăn mòn-mòn; con người; sản xuất-lắp-bảo dưỡng-tái chế; rủi ro tối thiểu; **bảng tra mối ghép §8.1.5**; cơ điện tử; dãy cỡ; mô-đun. |
| `kl9-gestaltung.md` | KL9 Ch07–Ch10, Ch13–Ch17 | Quá trình/mô hình hiện thân (Kap. 13.1–13.5), phân tích & tổng hợp (13.6–13.8), thiết kế công nghiệp (16.9), sản xuất bồi đắp (16.13), chi phí, sinh thái, tiêu chuẩn, sở hữu công nghiệp — phần **khác hoặc mới hơn** TKKTHT ghi rõ. |
| `function-index.md` | tổng hợp ba tệp trên | **Chỉ mục theo loại chức năng** (vd. nhận/tiêu tán va đập, truyền lực, định vị/dẫn hướng, nối ghép, bịt kín, giữ nổi/ổn định, bảo vệ cảm biến, dẫn điện/tín hiệu, tản nhiệt, thao tác người) → quy tắc + mục catalog liên quan. Đây là cửa vào F3. |
| `scoring.md` | KL9/TKKTHT đánh giá + VDI 2225 | Thang 0–4, ánh xạ yêu cầu → DP, luật ô `?`, độ nhạy. |
| `benchmark-search.md` | — | Quy trình 3 tầng, truy vấn theo chức năng, đọc hình sáng chế, mẫu hồ sơ một giải pháp. |

Luật chưng cất:
- **Diễn ý**, không chép đoạn dài; trích nguyên văn ≤ 1 câu khi cần, đặt trong `“…”` và có vị trí.
- Mỗi mục có con trỏ kiểm được về chương/mục của sách phái sinh (và trang bản gốc nếu sách đã ghi).
- Cấm bổ sung kiến thức ngoài sách vào bộ tham chiếu; thêm gì phải gắn `[ngoài sách]`.
- Sau chưng cất: kiểm máy con trỏ (mục trỏ tới có tồn tại trong `book.md`) + kiểm mẫu ngẫu nhiên ≥ 10% mục bằng
  đọc lại chương nguồn. Báo cáo của tác tử chưng cất **không** tính là bằng chứng.
- `helix-cc2:references:embodiment-rules` giữ nguyên, thêm một dòng trỏ sang bộ mới *(quyết định của tôi)*.

## 8. Đầu ra (Data Bus, cùng thư mục P3 của dự án / biến thể)

| Tệp | Đọc bởi |
|---|---|
| `{{prefix}}BF_Function_Selection.md` | BF (cổng 1), BE |
| `{{prefix}}BF_Form_Variants.md` — chuỗi C&C², phương án, quy tắc, tham số | BA, BB |
| `{{prefix}}BF_Benchmark.md` — giải pháp hiện có + nguồn + chuỗi đọc ngược | BE, `ip-*` |
| `{{prefix}}BF_Scoring.md` — bảng lọc D, chấm W×HOQ, checklist 14 mục, độ nhạy | BE |
| `{{prefix}}BF_Form_Selection.md` — quyết định CEO, khoảng tham số khoá, phiếu GT + kế hoạch thử | **BA**, BB, BE, Phase 4 |
| `{{prefix}}CC2_Handoff.md` — sinh nếu chưa có, cùng định dạng C6 | BA (hợp đồng cũ giữ nguyên) |

## 9. Thay đổi các tệp khác

- `helix-embody-realize/SKILL.md`: sơ đồ pipeline, bảng khối, `_pipeline_state` (thêm dòng BF), Data Bus, cờ
  `--skip-form`, hành vi `--quick`/`--from`/`--only`, mục Integration.
- `helix-p3-preflight`: B0 xuất danh sách yêu cầu quyết định hiện thân ở dạng BF đọc được (nếu chưa).
- `helix-p3-layout`: đọc `BF_Form_Selection.md` là nguồn khoảng tham số; đổi khoảng phải quay lại BF.
- `helix-p3-compile` (BE): kiểm nhất quán layout ↔ hình thể đã chọn; in lý do nếu BF bị bỏ qua.
- `docs/HELIX_Architecture.md`, `CLAUDE.md` (dòng helix), `docs/SYSTEM_OVERVIEW.md` nếu liệt kê khối P3.
- Eval: `evals/helix-p3-form.json`, `mode: "static"`.
- Cổng máy: `scripts/p3_form_lint.py` + `scripts/test_p3_form_lint.py` — kiểm đầu ra BF: mỗi phương án có ≥1 con trỏ
  sách hợp lệ và ≥1 tham số khoá; mỗi giải pháp hiện có có nguồn + nhãn tri thức; bảng chấm đủ mọi W liên quan,
  có trọng số, ô `?` có lý do; checklist đủ 14 mục hoặc lý do bỏ; có kế hoạch thử cho mỗi phương án chọn.
  Kiểm bằng đột biến theo chính regex của assert (bài học eval).
- **Không** đụng `VERSION`, `CHANGELOG.md`, `_codify_ledger.md` — changelog để trong mô tả PR.

## 10. Ràng buộc

- Nhánh `feature/helix-p3-form`, tách từ `origin/feature/evals-static-mode` bằng worktree riêng; nhánh hiện tại có
  nhiều thay đổi chưa commit của việc khác — không mang theo.
- Ba sách nằm ở vault `D:\Workshop_X\3_Resources\Books\` (ngoài repo). Skill chỉ chứa bản chưng cất; đường dẫn sách
  ghi để người kiểm tra cứu.
- Grep tiếng Việt dùng `LC_ALL=C.UTF-8`; Python chạy `-X utf8`.
- Không dữ liệu mật; không giá nhà cung cấp trong bộ tham chiếu.
- COD: chưng cất, tìm nguồn, dựng bảng = Offload; chọn chức năng, chọn hình thể, phân D/W = Core (CEO).

## 11. Để lại cho người dựng

- Cách chia việc chưng cất cho tác tử con (theo chương), định dạng nội bộ từng tệp tham chiếu, câu truy vấn Exa cụ thể.
- Bố cục chi tiết từng tệp đầu ra, miễn đủ trường ở §6/§8 và qua `p3_form_lint.py`.
- Mức chi tiết của sửa đổi BE/B0, miễn hợp đồng tệp cũ không gãy.

## 11b. Quyết định của tôi sau vòng đọc soát (CEO kiểm khi đọc)

- **BF chọn hình thể theo chức năng; BE vẫn chấm Rt/Re ở mức layout.** BA có thể ra nhiều phương án *bố trí* từ các
  hình thể đã chọn; BF không thay BE.
- **P2 chỉ chọn khái niệm cấp hệ** → F2 suy nguyên lý từng chức năng con từ `Concept_Selection` (+ `Morphological_Matrix`
  nếu có), ghi là *phỏng đoán* và đưa CEO xác nhận ở Cổng 1.
- **Glob linh hoạt tên tệp**: chấp nhận cả tệp không tiền tố (`BE_Concept_Selection.md`) như các khối P2 đang làm.
- **Hai đợt giao**: Đợt 1 = bộ tham chiếu §7 (kiểm máy con trỏ + kiểm mẫu 10%, CEO đọc mẫu trước khi dùng). Đợt 2 =
  skill BF + sửa P3 + lint + eval. Mỗi tệp tham chiếu ≤ ~1.500 dòng; SKILL chỉ nạp phần cần qua `function-index.md`.

## 12. Chạy thử nghiệm thu

`/helix-embody-realize VN-TGT-F --variant TGT-10` (tiền tố `VN_TGT_F_TGT_` theo luật VARIANT_SHORT — `<V0>` = `<V>` cắt tại dấu `-` đầu tiên, phán quyết R13; thư mục P3 `Phase3-Embodiment/TGT-10/`) qua B0 → BF đến hết cổng CEO 2; `p3_form_lint.py --draft` sạch trước cổng CEO 2 và lint chính thức (không `--draft`) sạch sau cổng; BA đọc được
`BF_Form_Selection.md`. Câu hỏi nhận: CEO đọc `BF_Scoring.md` có quyết được hình thể cho «nhận va chạm đầu đạn» và
«giữ nổi thẳng đứng» mà không phải hỏi lại không.

**Điều anh sẽ gặp:** chưa có thư mục Phase3 cho TGT-10 (B0 sẽ tạo); Phase 2 chưa đủ (B0 sẽ báo, anh override để chạy tiếp); các dự phòng R15 (thiếu Function_Structure), Q6 (D/W tạm), Q7 (HOQ proxy) đều kích hoạt → mọi dòng W mang 🔴 với ô trọng số trống cho tới khi anh gán trọng số ở Cổng CEO 2.

## 13. Quyết định CEO vòng 2 (2026-10-27)

| # | Tình huống | Quyết định |
|---|---|---|
| Q6 | Danh sách yêu cầu chưa phân D/W (hoặc chỉ có `Requirements_Draft`) | **Chạy tạm**: BF đề xuất D/W, mọi dòng gắn nhãn `D/W tạm`, CEO duyệt tại Cổng 1. Bảng chấm in rõ đang dùng phân loại tạm; BE nhắc chưa được qua Gate 3 khi còn nhãn tạm. |
| Q7 | Yêu cầu W không ánh xạ được DP nào của HOQ (hoặc HOQ là bản proxy) | **Giữ lại trong bảng, gắn cờ ĐỎ, trọng số để trống** cho CEO gán; tổng điểm in hai cột: chỉ phần có trọng số, và phần cờ đỏ chưa gán. Lint cho phép ô trọng số trống *chỉ khi* có cờ đỏ. |
| Q8 | Phạm vi chạy thử | **Chạy riêng biến thể TGT-10** (`--variant TGT-10`). |
