# Spec: `/learn-lecture` — NotebookLM → bộ bài giảng slide + audio đồng bộ

> Date: 2026-07-22 · Status: approved-design · Domain: learn/
> Nguồn gốc: tự động hóa quy trình chạy tay 2026-07-22 (bài 1.10 Claude 101 — slide 12 phần + audio xướng "Phần N").

## 1. Mục đích

CEO đưa tên một NotebookLM notebook → skill quét toàn bộ nguồn, đề xuất bộ bài giảng
(giáo trình) theo 3 chế độ chi tiết, cho CEO chọn từng bài để sản xuất. Mỗi bài: tự
chọn đúng nguồn, tạo slide deck, đọc nội dung slide thật, tạo audio thuyết giảng khớp
1-1 với slide (xướng "Phần N" khi chuyển), kiểm đồng bộ, tải cả hai về vault, rồi hỏi
bài tiếp theo.

## 2. Định danh & giao diện

- Vị trí: `skills/learn/learn-lecture/SKILL.md` + `skills/learn/learn-lecture/references/prompt-templates.md`
- Frontmatter: `name: learn-lecture`, description có "Triggers on:" EN + VI
  (learn lecture, tạo bài giảng, notebook thành bài giảng, lecture from notebook,
  slide audio đồng bộ, giáo trình từ notebook…)
- Gọi: `/learn-lecture <notebook-name-or-alias>`
- Flags:
  - `--mode compact|full|extend` — bỏ qua bước hỏi mode
  - `--resume` — alias tường minh cho hành vi resume mặc định
  - `--lesson <N>` — nhảy thẳng tới bài N trong Curriculum.md
- Engine: MCP `notebooklm-mcp` (`notebook_list`, `notebook_get`/`source_describe`,
  `notebook_query` với `source_ids`, `studio_create`/`studio_status`/`studio_revise`,
  `download_artifact`/`export_artifact`). Auth hết phiên → báo CEO chạy `nlm login`,
  retry tối đa 2 lần.
- Kế thừa rule từ `/nlm`: **audio LUÔN `language=vi`** trừ khi CEO yêu cầu rõ tiếng Anh.

## 3. Luồng 5 phase

```
Phase 0  INTAKE      resolve notebook (fuzzy match tên/alias → CEO xác nhận nếu mơ hồ);
                     check auth
Phase 1  SCAN        notebook_get → Claude gom cụm chủ đề từ title (+ source_describe
                     khi title mơ hồ); KHÔNG query từng nguồn
Phase 2  CURRICULUM  ▸ nếu không có --mode: hiển thị tóm tắt cụm chủ đề + ước tính
                       số bài của CẢ 3 chế độ → CEO chọn mode
                     ▸ đề xuất giáo trình chi tiết theo mode → CEO duyệt/sửa
                       (gộp/tách/đổi thứ tự/loại bài) — CORE gate
                     ▸ ghi Curriculum.md vào vault
Phase 3  LESSON LOOP 8 bước per bài (xem §5) → cập nhật Curriculum.md → hỏi bài tiếp
Phase 4  WRAP        khi dừng: tóm tắt tiến độ + nhắc lệnh resume
```

**Resume:** `/learn-lecture <notebook>` ở session mới → nếu Curriculum.md của notebook
đó đã tồn tại → bỏ qua Phase 1-2, vào thẳng Phase 3 với các bài pending.

**COD:** Phase 1, 3 (sản xuất) = Offload · Phase 2 duyệt giáo trình + chọn bài mỗi
vòng lặp = Core.

## 4. Ba chế độ & Curriculum.md

| | compact | full | extend |
|---|---|---|---|
| Nguyên tắc gom | Gộp nhiều cụm → ít bài tổng quan | Mỗi cụm chủ đề = 1 bài đầy đủ | full + bài deep-dive/case-study cho cụm trọng yếu |
| Slide/bài (N) | ~8 | ~12 | 12; bài mở rộng ~15 |
| Audio/bài | ~8–10 phút | ~13–16 phút | 15–25 phút |
| Dùng khi | Ôn nhanh, notebook <15 nguồn | Học chính quy | Chủ đề cần master |

Đề xuất giáo trình: mỗi bài gồm số thứ tự, tên, 1 câu mô tả, danh sách nguồn dự kiến
(title + source_id), ước tính slide/phút.

**Curriculum.md** — state file tại
`D:\Workshop_X\2_Areas\CEO-Self\Learning-Architecture\<notebook-slug>\Curriculum.md`:

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
notebook: <tên notebook>
notebook_id: <uuid>
mode: full
status: active          # active | completed
tags: [#type/sop, #status/active, #topic/learning]
---
| # | Bài | Nguồn (id rút gọn) | Slide | Trạng thái | Ngày | Thư mục |
|---|-----|--------------------|-------|------------|------|---------|
| 1 | ... | 0c2942, 0b0e28     | 12    | ✅ done    | ...  | Bai-01-... |
| 2 | ... | ...                | 12    | ⬜ pending  |      |         |
```

Bài lỗi bỏ qua → đánh dấu ⚠ skipped kèm lý do. Tất cả bài ✅ → `status: completed`.

## 5. Vòng lặp per-lesson (8 bước) — lõi đồng bộ

Thứ tự thực thi (verify slide chạy TRƯỚC khi tạo audio):

```
3.1 PICK      CEO chọn bài (mặc định: bài pending đầu tiên; --lesson N chỉ định)
3.2 OUTLINE   notebook_query CHỈ với source_ids của bài: trích dàn ý đầy đủ theo
              thứ tự (mục tiêu, đề mục, khái niệm, ví dụ, thao tác, ghi nhớ; giữ
              nguyên số liệu/tên riêng) → Claude chưng cất thành DÀN Ý ĐÁNH SỐ
              N phần (N theo mode)
3.3 SLIDES    studio_create(slide_deck) — prompt nhúng dàn ý N phần + ràng buộc:
              "Tạo ĐÚNG N slide riêng biệt, không gộp; đúng thứ tự + tiêu đề;
              CHỈ dùng nguồn đã chọn, không thêm kiến thức ngoài; tiếng Việt,
              giữ thuật ngữ EN" → poll studio_status
3.4 EXTRACT   download/export artifact slide → đọc nội dung slide THẬT
              (tiêu đề + bullet từng slide) = ground truth
3.5 VERIFY-S  So slide thật vs dàn ý duyệt: đủ N slide? tiêu đề khớp? →
              lệch → 3.6 REPAIR; PASS → 3.7
3.6 REPAIR    tối đa 1 vòng: studio_revise (hoặc tạo lại) → quay lại 3.4.
              Vẫn lệch → CEO quyết: chấp nhận có ghi chú / bỏ bài
3.7 AUDIO     Sinh prompt audio TỪ nội dung slide thật (không dùng dàn ý gốc):
              N đoạn khớp 1-1, mỗi đoạn mở bằng "Phần N — <tiêu đề slide thật>",
              nội dung = diễn giảng bullet của slide đó. Tự kiểm prompt có đủ
              N callout khớp tiêu đề trước khi gửi.
              studio_create(audio, language=vi) → poll studio_status
3.8 SAVE      Tải PPTX + MP3 → ...\<notebook-slug>\Bai-NN-<slug>\
              + outline.md (dàn ý duyệt + nội dung slide trích + Sync Report
              PASS/lệch-ở-đâu) + cập nhật Curriculum.md
              → hỏi "Tạo bài tiếp theo? (bài N+1)"
```

**Hai nguyên tắc đồng bộ:**
1. Slide trước — audio sau — audio sinh từ slide THẬT: NLM có tự gộp slide thì audio
   vẫn khớp bộ slide thực tế.
2. Verify slide trước khi tạo audio: không đốt 10–20 phút audio cho bộ slide hỏng.

**Fallback 3.4:** nếu API không trả được nội dung text của slide → dùng dàn ý duyệt
ở 3.2 làm nguồn cho audio prompt, Sync Report ghi rõ "đồng bộ mức dàn ý, chưa đối
chiếu slide thật".

## 6. Xử lý lỗi

| Tình huống | Xử lý |
|---|---|
| Auth NLM hết phiên (~20 min) | Báo CEO chạy `nlm login` → retry ≤2 → dừng có trạng thái (resume được) |
| Không tìm thấy notebook | Fuzzy match → đề xuất ứng viên, CEO xác nhận |
| studio_create fail/timeout | Retry 1 lần → vẫn fail: ghi ⚠ vào Curriculum.md, hỏi CEO bỏ bài hay dừng |
| Slide lệch sau 1 vòng repair | CEO quyết: chấp nhận có ghi chú / bỏ bài — không lặp vô hạn |
| Notebook >45 nguồn / cụm quá lớn | Cảnh báo ở SCAN, đề xuất extend mode hoặc thu hẹp phạm vi |

## 7. Eval & deployment

- `evals/learn-lecture.json`, `mode: "static"` — kiểm: frontmatter hợp lệ; đủ 5 phase;
  CORE gate ở Phase 2; thứ tự slide-trước-audio-sau + audio-từ-slide-thật; verify
  trước audio; rule `language=vi`; repair ≤1 vòng; cơ chế resume qua Curriculum.md;
  fallback 3.4.
- Sau build: bump VERSION + CHANGELOG entry; junction làm skill hiệu lực ngay.

## 8. Không làm (YAGNI)

- Không tự thêm nguồn mới vào notebook (việc của `/nlm add` / deep-research)
- Không transcribe audio để kiểm chứng sâu
- Không tạo video/infographic/quiz — chỉ slide + audio
- Không tự sản xuất bài khi CEO chưa chọn — mỗi vòng lặp có gate Core
