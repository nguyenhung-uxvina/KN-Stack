---
name: book-to-learn
description: "Orchestrator học một cuốn sách đến mức ỨNG DỤNG ĐO ĐƯỢC vào Workshop X trong chu kỳ ~30 ngày: L0 mission (vấn đề thật + 3 dự đoán) → L1 trích cấu trúc (book-to-skill, /analyze) → L2 NotebookLM toàn văn theo chương → L3 mở rộng 4 hướng (phản biện, bối cảnh VN, bản mới, tri thức sẵn có) → L4 học cách học (chunking, Feynman, drill, interleaving, journal, rubric, ôn giãn cách) + cổng Feynman → L5 thẻ thí nghiệm DMIR → L6 chạy thật → L7 AAR + sổ meta-learning xuyên sách. Mọi cổng do scripts/btl_gate_check.py kiểm. Triggers on: 'book to learn', 'học sách', 'học một cuốn sách', 'áp dụng sách vào công việc', 'đọc hiểu thực hành ứng dụng', 'biến sách thành hành động', 'meta-learning sách', 'learn from book', 'apply book to business'."
argument-hint: "<file|thư mục sách> [--slug X] [--target <dự án>] [--notebook <id>] [--from Ln] [--only Ln] [--resume] [--quick]"
---

# /book-to-learn — Học sách đến ứng dụng đo được

> **Đích:** một chu kỳ chỉ XONG khi có ≥1 thí nghiệm ứng dụng vào vấn đề thật của Workshop X, được CEO duyệt, chạy thật, đo được, đóng vòng DMIR-R. Chu kỳ không có thí nghiệm vẫn đóng, nhưng ghi `applied:false` — không bao giờ gọi là "xong".
> **Spec:** `docs/superpowers/specs/2026-09-17-book-to-learn-design.md` · **Hợp đồng pha:** [references/phase-contracts.md](references/phase-contracts.md) · **DMIR + học cách học:** [references/dmir-unified.md](references/dmir-unified.md)

## Quy tắc cứng (đọc trước khi làm bất cứ gì)

1. **Cổng máy.** Không đánh dấu pha nào xong khi `python D:/KN-Stack/scripts/btl_gate_check.py <LEARN-dir> <pha>` chưa exit 0. Script tự ghi dấu vào `_pipeline_state.md`. Không tự tay thêm dòng `PASS`.
2. **DMIR = Diagnose–Model–Intervene–Reflect** (tầng meta). Bản nhẹ: D+M tối đa 2 phiên; `/sdmodel` chỉ khi CEO yêu cầu. Không trích các con số chưa có nguồn của tài liệu DMIR như sự thật.
3. **NotebookLM:** cấm `chat_configure` với goal tuỳ chỉnh (persona làm mất nền truy hồi). Mỗi truy vấn mở conversation mới; loại câu trả lời có `sources_used` = 0; số liệu NLM trả về phải grep lại trong `_source/` với `LC_ALL=C.UTF-8`, thử nhiều cách viết, và tự kiểm lại mình trước khi kết luận NLM sai. Hai lỗi nhanh liên tiếp (4–6 giây) → dừng, nghi hạn mức. Không tin kết quả in ra của `nlm source add`.
4. **Bản quyền:** notebook `btl-*` không bao giờ share public; `_source/` chỉ nằm trong vault; không chép nguyên văn dài. Chương bị loại khỏi NLM: không ghi lý do loại vào manifest hay truy vấn.
5. **Số liệu sách giữ bối cảnh gốc** (tiền tệ, luật, quy mô). Dùng ở VN phải có dòng CẦN-CHUYỂN-VN trong Claims.
6. **Quyết định CEO ghi bằng chữ đầy đủ**, không bằng nhãn (A)/(B).
7. **Galaxy:** chỉ đề xuất; qua `galaxy-gate` và đối chiếu `5_Galaxy` trước. AI không tự tạo ghi chú.
8. **Sửa ở tệp nguồn** (Brief, Claims, Learning_Kit), không vá vào tệp dựng ra.
9. **Không viết ký hiệu đô-la liền một chữ số** trong bất kỳ SKILL.md nào sinh ra (bộ nạp skill thay nó bằng tham số) — viết "USD 0–250K".

## Đường dẫn

```
VAULT = D:\Workshop_X
LEARN = VAULT\1_Projects\LEARN-<slug>\          chu kỳ học (dự án PARA)
BOOK  = VAULT\3_Resources\Books\<slug>\         tri thức bền: _source/, Leverage_Map.md, Claims.md, Learning_Kit.md
SKILL = ~\.claude\skills\<slug>\                skill tri thức
META  = VAULT\2_Areas\CEO-Self\Learning-Meta\   cycles.jsonl, calibration.md, transfer-map.md, skill-backlog.md
TPL   = D:\KN-Stack\skills\book\book-to-learn\references\templates\
```

## Phân tích lệnh

- Đối số đầu: đường dẫn sách (hoặc bỏ trống khi có `--notebook` / `--resume`).
- `--slug`: mặc định kebab-case từ tên sách.
- `--target <dự án>`: thư mục trong `1_Projects`.
- `--resume`: đọc `LEARN/_pipeline_state.md`, chạy pha đầu tiên chưa có dòng PASS.
- `--from Ln` / `--only Ln`: bắt đầu tại / chỉ chạy pha đó (vẫn chạy cổng).
- `--quick`: bỏ L3 và đặt `quick: true`. **Không bỏ được L0, cổng Feynman L4, L5, L7.** Mọi framework bị gắn nhãn CHƯA KIỂM trong thẻ L5.

## Các pha

| Pha | Ngày | COD | Cổng |
|---|---|---|---|
| L0 Mission | 0 | C | chặn cứng nếu thiếu vấn đề thật |
| L1 Trích | 1–2 | O | máy |
| L2 NLM | 2 | O | máy |
| L3 Mở rộng | 3–6 | O, C duyệt nguồn | máy + CEO |
| L4 Học + cổng Feynman | 3–10 | O+C | máy (câu trả lời do CEO viết) |
| L5 Thiết kế thí nghiệm | 8–12 | O soạn, C chọn | máy + CEO duyệt |
| L6 Chạy thật | 12–28 | C | nhắc trễ hạn |
| L7 Retro | 28–30 | O soạn, C quyết | máy + CEO |

L0 → L1 → L2 chạy liền. L3 (máy, nền) song song L4 (phiên CEO). L5 cần L3 và cổng Feynman.

### L0 Mission — vấn đề thật trước, sách sau
1. Nếu có `--target`: đọc `VAULT/1_Projects/<target>/Status.md` trước.
2. Tạo `LEARN/`; chép `TPL/pipeline-state.md` → `LEARN/_pipeline_state.md` (điền `slug`, `started`); chép `TPL/mission.md` → `LEARN/_Project_Brief.md`; chép `TPL/run-log.md` → `LEARN/Run_Log.md`; tạo `LEARN/Status.md` theo chuẩn dự án Tier 3.
3. Hỏi CEO (một câu một lần): vấn đề/quyết định thật của Workshop X mà cuốn sách phải phục vụ → `van_de_that`; 3 dự đoán về nội dung sách → `du_doan_1..3`; tự chấm Dreyfus 1–5 → `dreyfus_truoc`; `target` hoặc `noi_ap_dung`; tiêu chí thành công bằng số.
4. Không có vấn đề thật → DỪNG, không mở chu kỳ.
5. Cổng: `python D:/KN-Stack/scripts/btl_gate_check.py "LEARN" L0`

### L1 Trích cấu trúc
1. Chạy `book-to-skill` với DEPTH=study, lưu vào `SKILL`. Nếu skill đã có: rà theo quy tắc 9 và dùng lại.
2. Chép `TPL/leverage-map.md` → `BOOK/Leverage_Map.md`; gán mỗi framework một mức L1–L12 kèm lý do (xem thang trong dmir-unified.md).
3. Chạy `/analyze` Phần 3 (Meta-Learning) cho các framework đáng áp dụng; chép `TPL/learning-kit.md` → `BOOK/Learning_Kit.md`. Câu hỏi Feynman **không kèm đáp án**.
4. Cổng: `… L1`. Sau đó CEO chọn `framework_ung_vien` trong `_pipeline_state.md`.

### L2 NotebookLM — toàn văn theo chương
1. Tách chương vào `BOOK/_source/ch<NN>-<slug>.md`.
2. Tạo notebook `btl-<slug>-goc` (hoặc dùng `--notebook`); `nlm source add --file` từng chương. Ghi id vào `notebook_goc`.
3. Tải JSON theo `references/phase-contracts.md` mục "Tải JSON cho cổng L2".
4. Truy vấn thử 1 câu có đáp án biết trước trong một conversation mới; kiểm `sources_used` > 0.
5. Cổng: `… L2 --nlm-list "LEARN/_nlm/list.json" --nlm-content-dir "LEARN/_nlm/content"`

### L3 Mở rộng 4 hướng
1. Soạn 4 câu hỏi `/research`: (a) phản biện & bằng chứng, case thất bại, chỗ tác giả đổi quan điểm; (b) chuyển bối cảnh VN — luật, thuế, chuẩn, quốc phòng; (c) bản mới & tác phẩm sau của tác giả; (d) nối tri thức sẵn có — `5_Galaxy`, `mentor-board`, sách đã học (`META/transfer-map.md`).
2. **CEO duyệt danh sách nguồn trước khi nạp** vào notebook `btl-<slug>-mo-rong` (tách khỏi notebook gốc).
3. Chép `TPL/claims.md` → `BOOK/Claims.md`; mỗi luận điểm chính của sách một dòng với nhãn SUPPORTED / CONTESTED / CẦN-CHUYỂN-VN, nguồn và vị trí.
4. Cổng: `… L3`

### L4 Học cách học + cổng Feynman
Chỉ cho `framework_ung_vien`. Trình tự:
1. **Chunking** và **Feynman** — `learn-methodology` (dùng Learning_Kit).
2. **Drill** và **interleaving** — `learn-practice`; khối học sách xen khối việc thật của Workshop X, không hai khối liền nhau cùng chủ đề.
3. **Journal** và **rubric hành vi** — `learn-track`; journal có ≥1 câu về vòng lặp phản hồi, ≥1 câu về cách học.
4. Bài học tương tác + ôn giãn cách + đoán-trước-rồi-thử: `learn-teach` có `disable-model-invocation`, nên **CEO tự gõ `/learn-teach`** trong thư mục `LEARN/learn/` (MISSION đã có sẵn từ L0).
5. Nhịp micro-DMIR hằng tuần: D thứ Hai (khái niệm nào đang chặn việc thật) → M thứ Ba (vòng phản hồi học của tôi nhanh hay chậm) → I thứ Tư–Sáu (áp một khía cạnh) → R cuối tuần (journal).
6. **Cổng Feynman:** với mỗi framework ứng viên, chép `TPL/feynman.md` → `LEARN/learn/feynman-<framework>.md`. **CEO tự viết** 3 câu trả lời (≥ 40 từ mỗi câu) và tự chấm rubric. AI không điền. Cổng: `… L4`

### L5 Thiết kế thí nghiệm — DMIR
Chép `TPL/experiment-card.md` → `LEARN/Experiment_Card.md`.
1. **D:** `/archetype` rồi `/cld` trên tình huống thật của dự án đích (số thật, không số giả định).
2. **M:** 3 biến có giá trị hiện tại → mục tiêu. Tối đa 2 phiên cho D+M.
3. **I:** `/constraint` rồi `/leverage`; chọn một can thiệp; ghi mức đòn bẩy; framework phải nằm trong `framework_ung_vien`; nêu nhãn Claims và rủi ro nếu CONTESTED/CẦN-CHUYỂN-VN/CHƯA KIỂM.
4. Điền đủ ô: giả thuyết, chỉ số, baseline là số, ngưỡng, người chịu trách nhiệm, ngày bắt đầu/kết thúc (≤ 16 ngày), dự đoán ghi trước, đơn vị phân tích của framework = của thí nghiệm, mức tin cậy dữ liệu L1–L5.
5. CEO duyệt → điền `ceo_duyet`. Chỉ khi CEO đồng ý mới thêm một dòng liên kết tới thẻ vào dự án đích.
6. Cổng: `… L5`

### L6 Chạy thật
Mỗi ngày 10 và 25: nhắc CEO ghi `LEARN/Run_Log.md` và hỏi "điểm nghẽn còn đó không?". Quá `ngay_ket_thuc` chưa có số đo → ghi cảnh báo vào `LEARN/Status.md`.

### L7 Retro — AAR, vòng kép, sổ meta
1. Chép `TPL/aar.md` → `LEARN/AAR.md`; `/reflect` soạn 4 mục AAR từ Run_Log; `/paradigm` cho mục vòng kép (mục tiêu L3, mô hình tư duy L2).
2. CEO quyết `quyet_dinh`: keep / adapt / drop.
3. Nối một dòng vào `META/cycles.jsonl` (tạo tệp nếu chưa có) theo `TPL/cycles-row.json`: Dreyfus trước/sau (CEO chấm lại), mức đòn bẩy chạm tới, Perkins, `applied`, `decision`, số dự đoán trúng/3, `days_to_competence` (L0 → ngày `ceo_duyet`), điểm hữu ích từng kỹ thuật học 1–5, `illusion_gap` (lệch đoán–thực trong RETRIEVAL.md), `book_type`, điểm rơi, gợi ý sách kế tiếp. Thẻ L5 chưa qua cổng → `applied:false`.
4. Cập nhật (tạo mới nếu chưa có, kể cả thư mục `META/` và `cycles.jsonl`) `META/calibration.md` (dự đoán vs thực tế), `META/transfer-map.md` (framework sách này ↔ sách trước; kỹ thuật học nào hợp loại sách nào), `META/skill-backlog.md` (lỗi của chính pipeline này).
5. Ứng viên Galaxy: đối chiếu `5_Galaxy` trước, chạy `galaxy-gate`, chỉ đề xuất.
6. Gợi ý cuốn kế tiếp từ `transfer-map.md` và lỗ hổng năng lực lộ ra; CEO chọn.
7. Cổng: `… L7`. Xong chu kỳ → đề xuất chuyển `LEARN-<slug>` sang `4_Archives` (hỏi CEO trước).

## Báo cáo cuối mỗi phiên
- Pha vừa qua cổng (dán dòng PASS/FAIL của script).
- Việc CEO cần làm tiếp, kèm COD.
- Ngày của mốc kế tiếp (L5 duyệt, ngày kết thúc thí nghiệm, ngày retro).
