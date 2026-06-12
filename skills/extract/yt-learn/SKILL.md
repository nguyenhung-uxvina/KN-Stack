---
name: yt-learn
description: Deep learning analysis pipeline for YouTube videos. Takes a YouTube URL → creates NotebookLM notebook → runs 9 structured learning queries (Q1-Q8 generic + Q9 WX defense context) → synthesizes into a complete video analysis file. Triggers when user pastes a youtube.com or youtu.be URL, or explicitly calls /yt-learn. Different from /yt-extract (short metadata extract) and /yt-search (discovery). This skill is for deep mastery extraction from a single video.
---

# YT Learn — Phân Tích Học Tập Sâu từ YouTube Video

Nhận YouTube URL → tạo NotebookLM notebook → chạy 9 query phân tích học tập (Q1–Q8 generic + Q9 WX context) → tổng hợp thành file phân tích hoàn chỉnh.

## When to Use

- Khi CEO dán link YouTube video và muốn phân tích sâu để học tập
- Khi phát hiện video có giá trị học tập cao cần khai thác 9 chiều
- Khác với `/yt-extract` (trích metadata ngắn) — skill này **deep learning pipeline**
- Khác với `/yt-search` (tìm video) — skill này xử lý 1 video cụ thể đã có sẵn

## Input

User cung cấp YouTube URL. Accepted formats:
- `https://www.youtube.com/watch?v=XXXXXXXXXXX`
- `https://youtu.be/XXXXXXXXXXX`
- `https://youtube.com/shorts/XXXXXXXXXXX`

## Workflow

### STEP 1 — Preflight & URL Validation

**Auth check:**
```
mcp__notebooklm-mcp__refresh_auth
```
- Nếu auth expired → HALT. Báo CEO: "Auth expired — chạy `nlm login` trong terminal rồi thử lại."

**Fetch video title via Bash:**
```bash
"C:/Users/Admin/AppData/Local/Programs/Python/Python312/Scripts/yt-dlp.exe" \
  --get-title --no-playlist "{youtube_url}"
```
- Nếu yt-dlp fail → dùng video ID làm fallback title (extract từ URL: `watch?v=XXXXXXX` → `XXXXXXX`)

**Extract video ID** cho alias (8 ký tự đầu của video ID): `ytl-{first8chars}`

---

### STEP 2 — Create NotebookLM Notebook

```
mcp__notebooklm-mcp__notebook_create(title="YT-Learn: {video_title}")
```

Lưu `notebook_id` từ response để dùng ở các bước sau.

---

### STEP 3 — Add YouTube Source

```
mcp__notebooklm-mcp__source_add(source_type="url", url="{youtube_url}")
```

NLM hỗ trợ YouTube URL trực tiếp như một nguồn. Không cần convert.

---

### STEP 3.5 — Source Processing Poll

Sau khi add source, NLM cần thời gian ingest. Poll thay vì wait cố định:

```
attempt = 1
while attempt ≤ 3:
    đợi 8 giây
    mcp__notebooklm-mcp__notebook_describe(notebook_id="{notebook_id}")
    if source_count >= 1 → BREAK (source ready)
    attempt += 1
```

Lý do: Video dài hoặc NLM tải nặng có thể cần 15–24 giây — 5s fixed không đủ reliable.

---

### STEP 3.6 — Rename Notebook theo Title từ Source

Sau khi source đã ingest (source_count ≥ 1), lấy title thực từ NLM và rename notebook:

```
mcp__notebooklm-mcp__source_describe(notebook_id="{notebook_id}")
→ Lấy title từ response (trường title hoặc display_name của source)
→ source_title = {title NLM đã parse từ YouTube}
```

Rename notebook theo title thực tế:
```
mcp__notebooklm-mcp__notebook_rename(
  notebook_id="{notebook_id}",
  title="YT-Learn: {source_title}"
)
```

**Lý do:** yt-dlp có thể fail hoặc trả về title bị cắt. NLM parse title trực tiếp từ metadata YouTube — chính xác và đầy đủ hơn. Notebook name phản ánh đúng nội dung.

**Fallback:** Nếu `source_describe` không trả về title → giữ nguyên title từ Step 1 (không rename).

---

### STEP 4 — Source Quality Gate

Verify sau poll Step 3.5:

```
mcp__notebooklm-mcp__notebook_describe(notebook_id="{notebook_id}")
```

Kiểm tra `source_count`:
- `source_count >= 1` → PASS, tiến hành Step 5
- `source_count = 0` sau 3 lần poll → HALT. Báo CEO: "NLM không thể ingest video này. Có thể video bị private, không có transcript/phụ đề, hoặc URL không hợp lệ."

---

### STEP 5 — Learning Queries (Sequential hoặc Batch)

**Chọn mode trước khi chạy:**

| Video duration | Mode | Tool |
|---------------|------|------|
| ≤ 20 phút | **Sequential** (default) | `notebook_query` × 8 lần |
| > 20 phút | **Batch** (parallel) | `mcp__notebooklm-mcp__batch` |

**Option A — Sequential (video ngắn):**
```
mcp__notebooklm-mcp__notebook_query(notebook_id="{notebook_id}", query="{Qi}")
```
Chạy lần lượt Q1 → Q8, lưu từng response.

**Option B — Batch (video > 20 phút):**
```
mcp__notebooklm-mcp__batch(
  notebook_id="{notebook_id}",
  queries=[Q1_text, Q2_text, Q3_text, Q4_text, Q5_text, Q6_text, Q7_text, Q8_text]
)
```
Batch chạy tất cả queries song song, trả về list responses theo thứ tự. Tốc độ nhanh hơn ~4–6× so với sequential.

Lưu toàn bộ response Q1–Q8 (dù mode nào) để tổng hợp ở Step 6.

---

**Q1 — Cấu Trúc Giảng Dạy:**

> Dựa trên nguồn video YouTube trong notebook này, phân tích cấu trúc giảng dạy theo 3 phần rõ ràng. **A. Bản đồ nội dung** (danh sách có số, tối đa 6 phần theo thứ tự thời gian): [Tên phần] — [Mục tiêu học tập 1 câu] — [Khái niệm trọng tâm]. **B. Logic kết nối** (2-3 câu): Khái niệm nào PHẢI hiểu trước mới có thể hiểu khái niệm sau — trình bày như chuỗi phụ thuộc. **C. 3 Bước Ngoặt Nhận Thức** (đúng 3, không hơn không kém): Xác định 3 thời điểm người xem thay đổi hoàn toàn cách nhìn nhận vấn đề. Mỗi bước ngoặt: [Người xem tin gì trước] → [Video chứng minh điều gì là sai hoặc thiếu] → [Hành vi nào thay đổi sau đó].

---

**Q2 — Skill Tree:**

> Từ video YouTube này, xây dựng skill tree (tối đa 12 kỹ năng) theo đúng cấu trúc sau, dùng ký tự ├── và └── để thể hiện phân cấp:
>
> [Nền tảng — PHẢI có trước]
>   ├── Skill A: [tên] — [1 câu: mô tả + lý do thiết yếu]
>   └── Skill B: [tên] — [1 câu]
> [Thực thi — dùng được sau khi có nền tảng]
>   ├── Skill C: [tên] — [1 câu]
>   └── Skill D: [tên] — [1 câu]
> [Nâng cao — tối ưu hoá]
>   └── Skill E: [tên] — [1 câu]
>
> ⭐ MVP Set (chỉ có 5 giờ để học): [liệt kê 2-3 kỹ năng tối thiểu để tạo ra kết quả đầu tiên có thể đo được]

---

**Q3 — Pareto Insights (80/20):**

> Từ video YouTube này, xác định đúng 5 insights có tác động lớn nhất nếu áp dụng ngay, trình bày theo bảng:
>
> | # | Insight | Tại sao là 80/20 | Nếu bỏ qua insight này |
> |---|---------|-----------------|----------------------|
> | 1 | ...     | ...             | ...                  |
>
> Sau bảng, thêm mục **Những gì KHÔNG phải 80/20**: Liệt kê 2-3 thứ trong video trông có vẻ quan trọng nhưng thực ra là detail — không phải leverage point — và giải thích tại sao.

---

**Q4 — Playbook Thực Thi:**

> Từ video YouTube này, tạo playbook thực thi 3 tầng. **Tầng 1 — Chuẩn bị** (làm TRƯỚC khi bắt đầu): Liệt kê 3-5 điều kiện tiên quyết hoặc tài nguyên cần có sẵn. Format mỗi dòng: [điều kiện] — [cách đáp ứng nếu chưa có]. **Tầng 2 — Thực thi** (tối đa 6 bước, không nhiều hơn): [Tên bước] → [Hành động cụ thể] → [Output/deliverable đo được]. **Tầng 3 — Điểm quyết định nóng** (3 nơi hay bị kẹt nhất): [Triệu chứng bị kẹt] → [Câu hỏi tự hỏi để thoát] → [Hành động cụ thể]. Cuối cùng: **Hành động 24h đầu tiên** — 1 câu duy nhất, điều đầu tiên ai đó có thể làm ngay sau khi xem xong video này.

---

**Q5 — Mental Models:**

> Dựa trên video YouTube này, xác định các mental model mà người trình bày **sử dụng hoặc đề cập rõ ràng** — chỉ những gì có bằng chứng trực tiếp từ video, không suy diễn hay bổ sung từ kiến thức bên ngoài. Với mỗi mental model (tối đa 5), trình bày: **[Tên model]** — Định nghĩa đơn giản (1 câu) — Bằng chứng từ video: [trích dẫn hoặc mô tả cụ thể khoảnh khắc trong video] — Công thức quyết định: "Khi gặp [X] → áp dụng model bằng cách [Y] → kết quả mong đợi [Z]".

---

**Q6 — Tình Huống Thực Tế:**

> Từ video YouTube này, tạo đúng 3 tình huống kích hoạt cụ thể — mỗi tình huống đặt trong một bối cảnh nghề nghiệp KHÁC NHAU, không chung chung. (Khác Q4 là procedure — Q6 là WHEN/WHERE: khi nào và trong bối cảnh nào thì cần dùng kiến thức này.) Với mỗi tình huống: **[Số]: [Tên ngắn]** — Ai + đang làm gì: [bối cảnh cụ thể] — Vấn đề kích hoạt: [điều gì xảy ra khiến họ CẦN kiến thức từ video, không phải "muốn"] — Họ làm gì: [hành động cụ thể, không phải lý thuyết] — Kết quả đo được: [thay đổi gì, làm sao biết nó hoạt động] — Dấu hiệu áp dụng SAI: [triệu chứng nếu hiểu nhầm và làm sai].

---

**Q7 — Sai Lầm Người Mới:**

> Từ video YouTube này, xác định đúng 5 sai lầm phổ biến nhất khi áp dụng kiến thức này, sắp xếp từ nguy hiểm nhất đến ít nguy hiểm nhất. Với mỗi sai lầm: **Sai lầm [số] [🔴/🟡/🟢]**: [Tên ngắn] — Biểu hiện: [người mới làm gì hoặc nghĩ gì sai cụ thể] — Tại sao bẫy này hấp dẫn: [lý do logic khiến nó có vẻ đúng] — Hậu quả: [điều gì xảy ra nếu không phát hiện sớm] — Phòng tránh: [câu hỏi tự kiểm tra TRƯỚC khi mắc phải] — Khắc phục (nếu đã mắc rồi): [bước đầu tiên cụ thể để thoát khỏi tình trạng này].

---

**Q8 — Lộ Trình Làm Chủ:**

> Dựa trên video YouTube này, thiết kế lộ trình làm chủ với 3-4 giai đoạn PHÙ HỢP VỚI CHỦ ĐỀ TRONG VIDEO (không cứng nhắc 4 giai đoạn — chủ đề đơn giản thì 3, phức tạp thì 4). Với mỗi giai đoạn: **Giai đoạn [số]: [Tên]** | Thời gian ước tính: [X tuần/tháng] — Mục tiêu quan sát được (KHÔNG dùng "hiểu được", phải là hành động): "Sau giai đoạn này tôi CÓ THỂ LÀM [X] đủ tốt để [kết quả cụ thể]" — Dự án cột mốc: [output cụ thể là gì, ai có thể đánh giá chất lượng] — Bẫy thường gặp tại giai đoạn này: [1 câu] — Test để lên giai đoạn tiếp: [1 câu hỏi hoặc challenge cụ thể — làm được = sẵn sàng].

---

**Q9 — WX Defense Context:**

> Áp dụng kiến thức từ video YouTube này vào bối cảnh Workshop X — công ty kỹ thuật quốc phòng Việt Nam (đội: CEO + 3 chuyên gia cơ khí/điện tử/phần mềm AI nhúng; sản phẩm: BB-01/LOMAH acoustic detection, V-SMASH, MTB-20, TDR; constraints: ngân sách R&D hạn chế, MIL-STD compliance, chuỗi cung ứng nội địa VN). Phân tích theo bảng:
>
> | Insight từ video | Áp dụng | Sản phẩm WX liên quan | Hành động cụ thể |
> |-----------------|---------|----------------------|-----------------|
> | [insight 1]     | ✅ Trực tiếp / ⚠️ Cần điều chỉnh / ❌ Không phù hợp | BB-01/LOMAH / V-SMASH / MTB-20 / TDR / Tất cả | [động từ + đối tượng + timeline cụ thể] |
>
> Sau bảng: **Câu hỏi cho team tuần này** — 1 câu hỏi kỹ thuật cụ thể CEO đặt ra trong buổi họp gần nhất, dựa trực tiếp trên insight quan trọng nhất từ video (không phải câu hỏi chung chung).

---

### STEP 5.9 — /analyze Phase 3A + Phase 4 (Systems Thinking + First-Principles Debate)

Sau khi có đủ Q1–Q9 responses, chạy /analyze trên nội dung tổng hợp để deepening:

**Chuẩn bị input:**
```
Synthesize Q1–Q9 thành 1 block văn bản liên tục (raw content, không cần format đẹp):
input_text = "{Q1_response}\n\n{Q2_response}\n\n...{Q9_response}"
```

**Chạy /analyze — chỉ Phase 3A và Phase 4:**

Phase 3A — Systems Thinking (bắt buộc):
- Stock-Flow Map: xác định stocks (kiến thức, kỹ năng, năng lực) và flows
- Feedback Loop Detection: R (reinforcing) + B (balancing), dominance ranking
- System Archetype: match với Shifting the Burden, Fixes That Fail, Limits to Growth, etc.
- Leverage Point Analysis (Meadows L1-L12): ưu tiên L1-L6 (paradigm, goals, information)

Phase 4 — First-Principles Debate + ARCHITECT (bắt buộc):
- Debate 3–5 major claims từ video (Step 1-6 trong /analyze Phase 4A)
- ARCHITECT framework: Irreducible Elements → Layered Architecture → Mnemonic
- Distill Three Laws: 3 laws memorable + generative từ toàn bộ video content

**Lưu output:**
```
analyze_3A_output = {systems_thinking_analysis}
analyze_4_output  = {first_principles_debate + ARCHITECT + Three Laws}
```

Dùng ở Step 6 để append vào Sections 10 và 11.

---

### STEP 6 — Synthesize Output File

Tổng hợp Q1–Q9 + /analyze (Phase 3A + Phase 4) thành file Markdown với cấu trúc sau:

```markdown
---
created: {YYYY-MM-DD}
source_url: {youtube_url}
notebook_id: {notebook_id}
video_title: {title}
type: video-analysis
tags: [#type/article, #status/active, #topic/learning]
---

# Phân Tích Video: {video_title}

**Nguồn:** {youtube_url}
**Notebook NLM:** {notebook_id} (alias: {ytl-alias})
**Phân tích ngày:** {date}

---

## Tóm Tắt Điều Hành
[5 bullet points tổng hợp insight quan trọng nhất rút ra từ 11 phân tích — ưu tiên: Three Laws (Section 11) + WX action (Q9) + Leverage Points (Section 10)]

---

## 1. Cấu Trúc Giảng Dạy
{Q1_response}

---

## 2. Skill Tree
{Q2_response}

---

## 3. Pareto Insights (80/20)
{Q3_response}

---

## 4. Playbook Thực Thi
{Q4_response}

---

## 5. Mental Models
{Q5_response}

---

## 6. Tình Huống Thực Tế
{Q6_response}

---

## 7. Sai Lầm Người Mới
{Q7_response}

---

## 8. Lộ Trình Làm Chủ
{Q8_response}

---

## 9. WX Defense Context
{Q9_response}

---

## 10. Systems Thinking Analysis
{analyze_3A_output}

*Stock-Flow Map | Feedback Loops (R/B) | System Archetypes | Leverage Points (L1-L12)*

---

## 11. First-Principles Debate + ARCHITECT
{analyze_4_output}

*Debate Points | Current vs Fundamental Limitations | ARCHITECT Reduction | Three Laws*

---

## Galaxy Candidates
[AI đề xuất — CEO quyết định promote]

| Concept | Cluster | Confidence | Draft Title |
|---------|---------|------------|-------------|
| (điền từ phân tích trên) | A–I | ★★★/★★ | Tên note tiếng Việt |
```

---

### STEP 6.5 — Galaxy Connection Check

Trước khi save, search Galaxy để tìm existing notes liên quan — tránh duplicate và enrich wikilinks cho Galaxy candidates:

```bash
# Extract top 3 keywords từ video title + Q3 Pareto insights
grep -ril "{keyword1}\|{keyword2}\|{keyword3}" "D:/Workshop_X/5_Galaxy/" 2>/dev/null | head -10
```

Đọc nhanh các file match để xác nhận relevance. Nếu không có match → ghi "(không tìm thấy match)" và tiếp tục.

Dùng kết quả để:
1. **Enrich Galaxy Candidates table** — thêm cột "Existing Links" với notes đã có trong Galaxy
2. **Prevent duplicate** — nếu concept đã có note → ghi "(đã có: [[Note X]])" thay vì đề xuất tạo mới
3. **Suggest wikilinks** — ghi vào Galaxy Candidates table những hub notes nên link đến

**Format cập nhật Galaxy Candidates table:**

| Concept | Cluster | Confidence | Draft Title | Existing Galaxy Links |
|---------|---------|------------|-------------|----------------------|
| ... | A–I | ★★★/★★ | Tên note tiếng Việt | [[Note X]], [[Note Y]] hoặc "(chưa có)" |

Nếu `search_galaxy` không trả về kết quả → ghi "(không tìm thấy match)" và tiếp tục.

---

### STEP 7 — Save & Report

**Save to:** `D:/Workshop_X/3_Resources/Deep-Content-Analyzer-Outputs/YT-Learn-{video_slug}-{YYYY-MM-DD}.md`

**Report to CEO:**
```
✅ yt-learn complete
📹 Video: {title}
📓 Notebook: {notebook_id} (alias: ytl-{8chars})
📄 File: 3_Resources/Deep-Content-Analyzer-Outputs/YT-Learn-{slug}-{date}.md
⏱ Estimated read time: ~{word_count/200} min
🌟 Galaxy candidates: {N} đề xuất — CEO review để promote
🔬 Analyze: Systems Thinking + First-Principles Debate appended (Sections 10-11)
   → Three Laws: [{Law1}] / [{Law2}] / [{Law3}]
🎧 Audio: chưa tạo — CEO muốn nghe khi lái xe? (xem Audio Option bên dưới)
```

**Audio Option (tuỳ chọn — CEO kích hoạt):**

Nếu CEO muốn audio tóm tắt để nghe khi di chuyển:

```
mcp__notebooklm-mcp__studio_create(
  notebook_id="{notebook_id}",
  artifact_type="audio",
  language="vi"
)
```

Sau đó poll cho đến khi complete:
```
mcp__notebooklm-mcp__studio_status(notebook_id="{notebook_id}", artifact_type="audio")
→ poll mỗi 15 giây cho đến khi status = "complete"
```

Download khi xong:
```
mcp__notebooklm-mcp__download_artifact(notebook_id="{notebook_id}", artifact_type="audio")
```

Lưu audio vào: `D:/Workshop_X/3_Resources/Deep-Content-Analyzer-Outputs/YT-Learn-{slug}-{date}.mp3`

---

## Edge Cases

| Situation | Action |
|-----------|--------|
| Video private / restricted | HALT at Step 4 — source_count = 0 |
| Video không có transcript/phụ đề | HALT at Step 4 — báo CEO cụ thể |
| Auth expired | HALT at Step 1 — instruct `nlm login` |
| yt-dlp không lấy được title | Dùng video ID làm title, tiếp tục |
| NLM query trả về empty | Ghi rõ "(NLM không có đủ data cho query này)" vào section đó |
| Video dài > 2h | Cảnh báo CEO: NLM có thể bị giới hạn — kết quả có thể không đầy đủ |
| Batch mode timeout | Nếu batch không trả về sau 60s → fallback sequential từ Q1 |
| studio_create audio fail | Ghi "(audio unavailable)" trong report, tiếp tục — không block save |
| search_galaxy trả về empty | Ghi "(không tìm thấy match)" trong Galaxy table, tiếp tục |

---

## vs /yt-extract vs /yt-search

| | `/yt-search` | `/yt-extract` | `/yt-learn` |
|---|---|---|---|
| Input | Topic/keyword | YouTube URL | YouTube URL |
| Purpose | Discovery | Metadata extract | Deep learning analysis |
| NLM | Optional | Optional | Required (core engine) |
| Output | List of videos | 1-page summary | 11-section analysis + Systems Thinking + Debate + audio |
| Time | ~1 min | ~2 min | ~15-20 min (batch) / ~25 min (sequential) |
| When | "Tìm video về X" | "Tóm tắt video này" | "Học sâu từ video này" |

## Integration Points

- Notebook còn lại trên NLM để query tiếp sau này qua `/nlm query {alias}`
- Galaxy candidates → `/galaxy-note` nếu CEO approve
- Output file → có thể add vào NLM notebook khác làm source qua `/nlm add`
- Dùng sau `/yt-search` khi CEO chọn được video chất lượng cao

## COD Classification

| Task | COD | Reason |
|------|-----|--------|
| URL detection + auth check | **O** | Pattern matching + automated |
| Notebook creation + source add | **O** | Automated MCP calls |
| Source quality gate | **O** | Automated verify |
| 9 NLM queries (Q1–Q9) | **O** | Automated pipeline |
| Executive summary synthesis | **O** | AI synthesis từ 9 responses |
| Saving output file | **O** | Auto-default path |
| /analyze Phase 3A + Phase 4 | **O** | AI-generated Systems Thinking + Debate từ 9 responses |
| Galaxy candidate promotion | **C** | CEO judgment — không bao giờ auto-promote |
| Promote Three Laws sang Galaxy | **C** | CEO review Three Laws từ Section 11 trước khi promote |
| Quyết định có dùng skill không | **C** | CEO chọn video nào xứng đáng deep-learn |
