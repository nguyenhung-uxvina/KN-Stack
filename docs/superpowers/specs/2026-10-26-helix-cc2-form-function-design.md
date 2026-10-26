# Thiết kế — Bộ skill `helix-cc2`: phân tích ⇄ tổng hợp, chức năng ⇄ hình thể qua C&C²

> Ngày: 2026-10-26 · Người yêu cầu: CEO · Trạng thái: CHỜ CEO DUYỆT
> Nguồn tri thức: `D:\Workshop_X\3_Resources\Books\cc2-gia-thuyet-ket-cau\book.md` (gọi tắt **CC**) và
> `D:\Workshop_X\3_Resources\Books\thiet-ke-hien-than\book.md` (gọi tắt **TK**).

## 1. Ý định và lý do

CEO có một chức năng đã phát biểu, ví dụ *«biến sự che khuất của đạn thành tín hiệu biên [quang→điện]»*, và
không biết: (a) có những lựa chọn hình thể nào, (b) phải dựng chuỗi C&C² ra sao, (c) thông số hình thể nào
quyết định thông số chức năng nào. KN-Stack hiện chỉ có chiều **phân tích** (hình thể → chức năng), nằm chìm
trong `/reverse-engineering` (`references/cc2-lens.md`). Chiều **tổng hợp** (chức năng → hình thể) chưa có.

Luận đề chung của hai quyển là *hình thể là giả thuyết*. Vì vậy bộ skill **không đưa ra đáp án**. Mọi gợi ý
ra đời dưới dạng giả thuyết có nhãn, kèm phép thử nhỏ nhất để bác bỏ (CEO đã duyệt).

## 2. Mục tiêu · Không phải mục tiêu · Phản mục tiêu

**Mục tiêu**
1. **Chiều tổng hợp.** Từ một chức năng con có thông số chức năng → ≥3 chuỗi C&C² khác nhau → mỗi chuỗi 2–3 hình
   thể → bảng nối thông số hình thể ↔ thông số chức năng → phiếu giả thuyết 9 mục + kế hoạch thử trên bàn thử
   → bàn giao P3 `helix-embody-realize`. Đây là ý của CEO.
2. **Chiều phân tích độc lập.** Đọc hình thể có sẵn (bản vẽ, CAD, ảnh, hiện vật) của chính Xưởng → mô hình C&C²
   → giả thuyết chức năng, **không** phải qua Purpose Gate/ACCESS LEVEL/OSINT của RE. CEO đã duyệt tách.
3. **Hai chiều đối chiếu được.** Hình thể vừa tổng hợp được chạy lại qua chiều phân tích (Ch04 CC «phân tích dẫn
   dắt bởi tổng hợp»). Chế độ cải tiến thì bắt đầu bằng phân tích hình thể hiện có rồi mới tổng hợp.
4. **Phép biến đổi góc nhìn** trên từng chuỗi: Zoom-In, Zoom-Out, Shift, đổi trạng thái/thời gian, đổi góc nhìn,
   và phương tiện quan sát («camera») để phá rào cản quan sát (CC Ch04 §04.3). Skill **tự đề xuất** phép nên
   làm tiếp, kèm lý do. CEO vẫn **gọi tay giữa phiên** được (CEO đã duyệt).
5. **Hai chế độ đầu vào** (CEO đã nêu): **dự án** (đọc `Function_Structure.md` P1, chạy lần lượt từng chức năng con)
   và **chức năng lẻ/cụm** (nâng cấp, sửa, bổ sung, cải tiến).

**Không phải mục tiêu**
- Không thay `helix-p2-search`: không dựng ma trận hình thái, không chấm DSO/VDI 2225. Khi câu chức năng đã nêu
  nguyên lý («quang→điện»), các chuỗi khác nhau ở **cách sắp WFP/LSS/Connector**. Khi chưa nêu, C1 đề xuất chuỗi ở
  nhiều miền, nhưng chỉ làm nguồn ý, không phải quyết định concept (xem §9 Q1).
- Không sinh CAD. Đầu ra là tham số và khoảng giá trị. Hình học thật do `helix-cad-bridge` ở P3.
- Không gỡ phần trùng trong `reverse-engineering/references/cc2-lens.md` ở đợt này (xem §7).

**Phản mục tiêu** (chạy được nhưng vẫn là thất bại)
- Bảng thông số nhìn như đã tính, nhưng ước lượng không ghi nhãn ⇒ «phỏng đoán mặc áo kết luận» (cc2-lens §13).
- Mô hình hoá mọi chức năng con của sản phẩm. CC đặt phạm vi cứng là chức năng quyết định giải pháp + ≤3 chức
  năng tới hạn (cc2-lens §1, CC:2042).
- Phiếu giả thuyết có «NẾU» là một **tác dụng** (ma sát, «tín hiệu mạnh hơn») thay vì một tham số ghi được lên
  bản vẽ (CC:2818).
- «Chuyển cho P3» chỉ là câu chữ, P3 không đọc gì (bài học `reverse-engineering/references/handoff-helix.md`:
  8/13 nối là dòng chảy không tồn tại).
- Bộ skill tự nhận là phương pháp đã chứng minh. Bằng chứng về C&C² yếu (bậc II/5, chủ yếu đo trên sinh viên,
  CC Ch11). Skill phải nói điều này ở đầu mỗi phiên.

## 3. Ràng buộc

- **Quy ước KN-Stack** (`CLAUDE.md`): thư mục `skills/<domain>/<tên>/SKILL.md`, frontmatter `name` + `description`
  có «Triggers on:» tiếng Anh + tiếng Việt; nhánh `feature/helix-cc2-form-function`; commit `[HELIX] …`;
  **không** sửa `VERSION`/`CHANGELOG.md` trên nhánh (đoạn changelog để trong mô tả PR mục `## CHANGELOG`).
- **Junction:** tham chiếu kiểu `../_shared/` hỏng dưới junction. Tài liệu dùng chung chỉ có **một nhà chính** và
  được gọi bằng tên skill (`helix-cc2:references:<tên>`), giống cách `reverse-engineering:references:cc2-lens` đang
  được nạp.
- **Cây làm việc bẩn:** nhánh hiện tại (`feature/book-fidelity-backmatter`) có nhiều thay đổi chưa commit của việc
  khác, gồm cả `reverse-engineering/SKILL.md`. Làm trong **worktree riêng** tách từ nhánh tích hợp
  `feature/evals-static-mode`. Không commit việc chưa commit của người khác.
- **IP:** ví dụ quang→điện nằm sát vùng IP LOMAH/BB-02. Skill và ví dụ trong skill chỉ dùng nguyên lý chung từ
  sách. **Không** đọc hồ sơ dự án có IP để làm ví dụ, không đưa hồ sơ đó cho tác tử con.
- **Đa miền.** cc2-lens §1 nói nên *bỏ qua* C&C² khi chức năng chủ yếu nằm ở điện/phần mềm. Ví dụ của CEO là
  quang→điện. Skill phải dùng lớp đa miền (CC Ch15, cc2-lens §9 MECHA): WFP quang = mặt phát / không khí / bóng
  đạn / mặt thu. Khi chuỗi đi vào miền điện tử hay phần mềm, skill phải ghi rõ chỗ C&C² hết dùng được, kèm lý do.
- **Tri thức phải có nguồn.** Mọi quy tắc trong `references/` ghi chương/mục của CC hoặc TK, kèm số trang P&B nếu
  sách có ghi. Không chép đoạn dài, viết lại bằng lời mình.
- **COD:** AI dựng nháp chuỗi/hình thể/phiếu (**Offload**). Chọn chuỗi, ký dự đoán, duyệt bàn giao là việc của
  CEO/kỹ sư (**Core**).

## 4. Phần CEO đã quyết

| # | Quyết định |
|---|---|
| D1 | Mỗi gợi ý là giả thuyết có nhãn **tri thức / phỏng đoán / giả định**, kèm phép thử nhỏ nhất để bác bỏ |
| D2 | Chiều phân tích lấy từ phần đã có trong `/reverse-engineering`; chiều tổng hợp làm mới; hai chiều đối chiếu nhau |
| D3 | Sau ≈3 chuỗi + hình thể + bảng thông số: đi tiếp sang phiếu giả thuyết, kế hoạch thử trên bàn thử, rồi bàn giao `helix-embody-realize` |
| D4 | **Tách** chiều phân tích thành skill độc lập (RE gọi lại nó) |
| D5 | Hai chế độ: dự án (`Function_Structure.md` P1, lần lượt từng chức năng con) và chức năng lẻ/cụm (nâng cấp/sửa/bổ sung/cải tiến) |
| D6 | Mỗi chuỗi cho phép Zoom-In/Out, Shift, đổi trạng thái, đổi góc nhìn, phương tiện quan sát; skill tự đề xuất, CEO gọi tay được |

## 5. Cấu trúc đề xuất (quyết định của người viết, CEO sửa được)

Domain `helix/` (vì đầu ra đổ vào P3). Một orchestrator + 7 khối, mỗi khối chạy riêng được (giống các pipeline
HELIX hiện có).

| Skill | Vai | Đầu vào chính | Đầu ra chính |
|---|---|---|---|
| `helix-cc2` | Orchestrator + router 3 chế độ: `--project`, `--function "<câu>"`, `--analyze <hình thể>`; giữ `_pipeline_state.md`; xử lý lệnh phép biến đổi giữa phiên. **Nhà chính** của tài liệu dùng chung | cờ + đường dẫn | trạng thái pipeline |
| `helix-cc2-frame` (C0) | Khung chức năng: câu chức năng → đại lượng vào/ra, **thông số chức năng có số** (mục tiêu, ngưỡng, dải), Connector biên, ràng buộc môi trường; nhãn cho từng số. Chế độ dự án: sàng chức năng con nào **đáng** dựng C&C² (§6.2) | câu chức năng hoặc `Function_Structure.md` (+ `Requirements_List`, + P2 `Concept_Selection`/`Morphological_Matrix` nếu có) | `CC2_C0_Frame.md` |
| `helix-cc2-chain` (C1) | Sinh **≥3 chuỗi** WFP → LSS → WFP + Connector, khác nhau thật (không chỉ đổi kích thước). Mỗi chuỗi có sơ đồ Mermaid vẽ tay lại được, trạng thái logic, mặt biên. Cuối khối: **đề xuất phép biến đổi** | C0 | `CC2_C1_Chains.md` |
| `helix-cc2-form` (C2) | Mỗi chuỗi → 2–3 phương án hình thể, lý do lấy từ quy tắc hiện thân TK (rõ ràng/đơn giản/an toàn, truyền lực, phân chia nhiệm vụ, tự tăng lực, ổn định, giãn nở, ăn mòn, chế tạo, dung sai…) | C1 | `CC2_C2_Forms.md` |
| `helix-cc2-param` (C3) | Bảng **thông số hình thể ↔ thông số chức năng** theo từng WFP/LSS (WSPO/WSPA, CC Ch13): tham số nào, ảnh hưởng chiều nào, ước lượng giải tích nếu có (ghi «suy ra từ …»), khoảng chọn đề xuất, chỗ «chưa biết». Đánh dấu tham số nhạy nhất | C2 + C0 | `CC2_C3_Params.md` |
| `helix-cc2-hypo` (C4) | Phiếu giả thuyết **9 mục** (đúng khuôn cc2-lens §10) cho các tham số nhạy nhất + **phép thử nhỏ nhất để bác bỏ** + kế hoạch thử trên bàn thử (CC Ch08–Ch10: đại lượng mục tiêu, đối chứng, đổi một biến, dòng dự đoán ký TRƯỚC ngày thử). Định tuyến độ tin × tầm ảnh hưởng (cc2-lens §11) | C3 | `CC2_C4_Hypotheses.md`, `CC2_C4_Test_Plan.md` |
| `helix-cc2-analyze` (CA) | **Chiều phân tích độc lập**: hình thể có sẵn → mô hình C&C² một trang → «vì sao hình học này» → giả thuyết. Dùng ở ba chỗ: chế độ `--analyze`; bước đầu của chế độ cải tiến; **đối chiếu ngược** (C5) lên hình thể vừa tổng hợp | bản vẽ/CAD (`cad_extract.json`)/ảnh/mô tả | `CC2_CA_Analysis.md` |
| `helix-cc2-handoff` (C6) | Đối chiếu ngược (gọi CA lên phương án chọn: hình thể có thật sự sinh ra chức năng C0 không, chỗ lệch thành phiếu mới) + **bàn giao P3** | C0–C4 + CA | `CC2_C6_Crosscheck.md`, `{{prefix}}CC2_Handoff.md` |

**Luồng chế độ dự án:** C0 (sàng) → với mỗi chức năng con được chọn: C1 → [CEO chọn chuỗi] → C2 → C3 → C4
→ [CEO ký dự đoán] → C6 → gộp một `CC2_Handoff.md` cho cả dự án.
**Luồng chế độ cải tiến:** CA lên hình thể hiện có → C0 (chức năng mới/nâng cấp + chỗ hỏng từ CA) → C1…C6.
Trong C1 phải có ít nhất một chuỗi là «hình thể hiện có, sửa tối thiểu».
**Luồng `--analyze`:** chỉ CA, có thể kết thúc bằng phiếu giả thuyết (C4).

### 5.1 Tài liệu dùng chung (nhà chính: `helix-cc2/references/`)

| Tệp | Nội dung | Rút từ |
|---|---|---|
| `cc2-core.md` | Bộ từ vựng WFP/LSS/Connector/mặt biên/trạng thái logic, bảy bước dựng mô hình, giới hạn dùng + bằng chứng yếu, phạm vi cứng, hai loại nhãn | CC Ch02, Ch05, Ch11; cc2-lens §0–2 |
| `view-ops.md` | 5 phép biến đổi + phương tiện quan sát: mỗi phép có *khi nào dùng* (câu hỏi kích hoạt), *làm gì với mô hình*, *dấu hiệu dùng sai*; bảng rào cản quan sát (quá nhanh/chậm, bị che, quá nhỏ/lớn, sai góc nhìn, ngoài biên) → phép/phương tiện phá | CC Ch04 §04.3 (P&B tr.435–443) |
| `synthesis-moves.md` | Các «nước đi» tổng hợp trên chuỗi: thêm/bớt/tách/gộp WFP, đổi LSS, dời Connector, đổi trạng thái, đổi miền (cơ/quang/điện) | CC Ch02, Ch04, Ch05, Ch15 |
| `embodiment-rules.md` | Chỉ mục quy tắc hiện thân → câu hỏi kiểm cho hình thể (mỗi quy tắc: hỏi gì, tham số nào bị khoá, chương nguồn) | TK Ch04–Ch16 |
| `param-bridge.md` | Cách lập bảng tham số hình thể ↔ chức năng: WSPO/WSPA, tham số vs tác dụng, nhạy, dải đã kiểm | CC Ch13, Ch14 |
| `hypothesis-sheet.md` | Khuôn phiếu 9 mục + điều kiện hợp lệ + khuôn kế hoạch thử trên bàn thử | cc2-lens §10–11; CC Ch06, Ch08–Ch10 |
| `multidomain.md` | C&C² cho cơ–điện–phần mềm nhúng: chỗ mô hình còn dùng được, chỗ phải dừng | CC Ch15; cc2-lens §9 |

### 5.2 Phép biến đổi giữa phiên

- Cuối C1, C2 và CA, skill in khối **«Phép nên làm tiếp»**: 1–3 phép, mỗi phép một dòng *phép · trên phần tử nào · vì
  câu hỏi kích hoạt nào trong `view-ops.md`*.
- CEO gọi tay: `/helix-cc2 --op zoom-in B:WFP2`, `--op zoom-out A`, `--op shift B:WFP1→WFP2`, `--op state B`,
  `--op view B:bệ-thử`, `--op observe B:WFP2`. Mỗi phép ghi một **phiên bản chuỗi mới** (`A.1`, `A.2`…), không ghi đè.
  Mỗi phép kèm một dòng nhật ký trong `_pipeline_state.md`.

### 5.3 Cơ chế thay cho lời nhắc

Một script `scripts/cc2_sheet_lint.py` (+ `scripts/test_cc2_sheet_lint.py`), chạy cuối C4 và C6, **chặn** khi:
phiếu thiếu mục nào trong 9 mục; «NẾU» chứa từ tác dụng trong danh sách đen (ma sát, mòn, tín hiệu, nhiễu… hiệu
chỉnh được); «VÌ» trống; dự đoán (mục 7) không có người ký + ngày; ngày ký dự đoán ≥ ngày thử; bảng C3 có ô số
không có nhãn. Lý do cần script: ghi nhớ «cơ chế, không phải lời nhắc». Lỗi này đã lặp 6 lần trong KN-Stack.

### 5.4 Bàn giao P3: hợp đồng hai phía

- C6 ghi `{{prefix}}CC2_Handoff.md` vào `Phase3-Embodiment/` (hoặc thư mục biến thể), gồm: chuỗi đã chọn cho mỗi
  chức năng con, tham số hình thể + khoảng chọn, tham số nhạy, phiếu giả thuyết đang mở, kế hoạch thử, chỗ C&C²
  không dùng được.
- Sửa **phía P3**: thêm `CC2_Handoff.md` vào RECOMMENDED INPUTS ở Step 1.5a và vào `READS FROM` của
  `helix-embody-realize`. Thêm một câu ở block BA (`helix-p3-layout`): nếu có tệp thì layout lấy khoảng tham số từ
  đó, mở phiếu giả thuyết tương ứng chứ không tự chọn lại.
- RE: thêm vào `reverse-engineering` một dòng «0A/1A có thể gọi `/helix-cc2-analyze`» trong Loại 2 của
  `handoff-helix.md`. **Chỉ làm sau khi** việc chưa commit trên `reverse-engineering/` đã vào nhánh tích hợp (§7).

### 5.5 Eval

`evals/helix-cc2.json` ở `mode: "static"`. Rà SKILL.md + references: có 3 chế độ, có ≥3 chuỗi, có khuôn 9 mục, có
`view-ops` đủ 5 phép + quan sát, có hợp đồng bàn giao hai phía, có câu cảnh báo bằng chứng yếu, có phạm vi cứng.
Kiểm assertion bằng đột biến: xoá theo chính regex của assertion (ghi nhớ «eval mutation by regex»).
`evals/helix-cc2-analyze.json` ở `mode: "runtime"`, dùng một hình thể công khai, không phải sản phẩm Xưởng.

## 6. Chỗ để người xây quyết

1. Lời văn của từng SKILL.md và references, miễn giữ đúng nguồn chương/mục.
2. Danh sách đen từ tác dụng cho `cc2_sheet_lint.py`, khởi đầu từ CC:2818.
3. Ví dụ mẫu trong mỗi skill: dùng cơ cấu công khai, không thuộc dự án có IP. Ví dụ quang→điện viết ở mức
   nguyên lý chung (rào sáng xuyên / phản xạ / bóng đổ lên mảng), không có số của LOMAH.
4. Tên tệp đầu ra chi tiết, miễn theo khuôn `{{prefix}}CC2_*`.
5. Cách gộp nhiều chức năng con thành một `CC2_Handoff.md`.

### 6.2 Sàng chức năng con ở chế độ dự án (quyết định của người viết)

CEO muốn «chạy lần lượt từng chức năng con». Sách đặt phạm vi cứng là chức năng quyết định giải pháp + ≤3 chức năng
tới hạn. Cách dung hoà: C0 **liệt kê đủ** mọi chức năng con, rồi xếp mỗi cái vào một trong ba ô kèm một câu lý do:
**dựng C&C²** · **chỉ bảng tham số** (quan hệ đã chuẩn hoá thành công thức/bảng) · **không áp dụng** (thuần điện
tử/phần mềm). CEO duyệt danh sách rồi pipeline mới chạy. CEO có thể đẩy thêm chức năng vào ô «dựng C&C²» và vượt
trần 3, nhưng phải ghi lý do.

## 7. Thứ tự làm

1. Worktree `feature/helix-cc2-form-function` từ `feature/evals-static-mode`.
2. Rút references từ CC/TK (đọc chương thật; mỗi quy tắc có nguồn; người kiểm grep lại nguồn, không tin báo cáo
   tác tử).
3. Orchestrator + 7 khối.
4. `cc2_sheet_lint.py` + test.
5. Sửa phía P3 (`helix-embody-realize`, `helix-p3-layout`).
6. Eval + kiểm đột biến.
7. `bash setup.sh --verify`, chạy test, PR (changelog trong mô tả PR).
8. **Sau** khi việc dở của RE đã vào nhánh tích hợp: PR nhỏ riêng nối RE → `helix-cc2-analyze` và gỡ trùng `cc2-lens.md`.

## 8. Quyết định của người viết sau lượt rà (CEO kiểm khi đọc)

- **R1 — Nhánh gốc.** `cc2-lens.md` **không** có trên `feature/evals-static-mode`. Nó chỉ có trên nhánh chưa merge
  `feature/design-re-v3.4-cc2` (commit 1e6e91e, dfc8d81; đã kiểm bằng `git ls-tree`). Cách xử lý: tách nhánh từ nhánh
  tích hợp. `helix-cc2/references/` rút **thẳng từ hai quyển CC/TK** và trở thành nhà chính ngay từ đầu, không trích
  `cc2-lens` như một phụ thuộc. Khuôn 9 mục được viết lại trong `hypothesis-sheet.md`, ghi nguồn CC chứ không ghi
  «cc2-lens §10». Trong thời gian chờ, hai bản cùng tồn tại. Bước 8 ở §7 gỡ trùng theo hướng RE trỏ sang `helix-cc2`.
  Mọi chỗ ghi «cc2-lens §x» trong tài liệu này chỉ để người xây biết nội dung lấy từ đâu.
- **R2 — Đối chiếu ngược C6 khi chưa có CAD.** C6 chạy CA lên **mô tả hình thể + bảng tham số** của phương án đã
  chọn. Việc này do **một tác tử con khác** làm, chỉ được nhận C0 và C2/C3, không được thấy lý lẽ C1. Lý do là
  «người đọc kết quả khác người lập giả thuyết». Đầu ra là một danh sách lệch. Mỗi chỗ lệch thành một phiếu mới
  hoặc một dòng sửa C2. `CC2_Handoff.md` ghi rõ đây là *đối chiếu mức mô tả*. Bàn giao kèm một mục **vòng lặp
  P3**: khi BA/`helix-cad-bridge` có hình học (`cad_extract.json`), chạy `/helix-cc2 --analyze` lên đó để đối chiếu
  mức hình học. Câu nhắc thêm ở `helix-p3-layout` (§5.4) phải nói điều này.
- **R4 — Chế độ cải tiến và nơi ghi.** Thêm cờ thứ tư `--improve <hình thể> "<chức năng mới/nâng cấp>"` (luồng CA →
  C0 → C1…, có chuỗi «sửa tối thiểu»). Nơi ghi: `--out <thư mục>`. Nếu thiếu thì là `Phase3-Embodiment/CC2/` khi
  chạy trong dự án, còn không thì `./_cc2/<slug>/`. Bàn giao P3 chỉ sinh khi có thư mục dự án. Ngoài dự án, C6 dừng
  ở `CC2_C6_Crosscheck.md` + kế hoạch thử, và tiền tố tệp là `<slug>_`.

## 9. Câu hỏi đã hỏi CEO

- **Q1 — Câu chức năng không nêu nguyên lý vật lý** (ví dụ «phát hiện đạn qua mặt bia», không có «quang→điện»).
  **CEO quyết (2026-10-26): (b)** — C1 tự đề xuất chuỗi ở **nhiều miền** (quang, âm, áp điện, tiếp điểm cơ…).
  Hệ quả cho người xây:
  - C0 ghi `nguyên lý: chưa nêu` và đặt ô *miền ứng viên*. C1 phải có ≥3 chuỗi, trong đó ≥2 miền vật lý khác
    nhau. Mỗi chuỗi một dòng *vì sao miền này hợp với thông số chức năng C0*, có nhãn tri thức.
  - Khi đã có P2 (`Morphological_Matrix`/`Concept_Selection`), nguyên lý P2 chọn được ưu tiên. C1 chỉ thêm chuỗi
    khác miền nếu có lý do ghi rõ, và đánh dấu «lệch P2 — CEO quyết».
  - Sửa mục *Không phải mục tiêu* (§2) cho đúng: `helix-cc2` **không dựng ma trận hình thái và không chấm
    DSO/VDI 2225**. Việc so sánh nguyên lý ở chế độ dự án vẫn thuộc `helix-p2-search`. Đề xuất đa miền ở C1 là
    nguồn ý cho anh, không phải quyết định concept.
