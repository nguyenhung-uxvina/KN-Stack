# Spec — Plugin `fluency-4d`: huấn luyện viên AI Fluency tại chỗ

> Ngày: 2026-08-01 · Trạng thái: đã duyệt thiết kế, chờ kế hoạch thực thi
> Phạm vi: một plugin tự chứa, import được vào Cowork, huấn luyện năng lực AI Fluency 4D của CEO trên công việc thật.

---

## 1. Vấn đề

Tầng "dạy" 4D đã đủ: bộ bài giảng AI Fluency 9/9 (video + audio), Student D–D Drills 12 bài, khóa Cowork Mastery 19 bài. Cái còn thiếu là tầng **đo và sửa hành vi trên việc thật** — không có gì chấm được rằng một phiên làm việc thực tế đã Delegation/Description/Discernment/Diligence tốt hay tệ, và không có gì bắt buộc thói quen thay đổi giữa các phiên.

Plugin này lấp đúng khoảng đó: **huấn luyện viên tại chỗ**, không phải giáo trình, không phải bài tập giả.

## 2. Quyết định đã chốt

| # | Quyết định | Lý do |
|---|---|---|
| D1 | Lõi = coach việc thật, không phải thư viện drill | Giáo trình đã có; thiếu đo lường trên việc thật |
| D2 | Ba thời điểm: pre-flight · mổ xẻ cuối phiên · tổng hợp tuần. **Không hook giữa phiên** | Cowork chưa chắc chạy `hooks/`; ba điểm này đều gọi tường minh nên chắc chạy |
| D3 | Sổ điểm ở một chỗ cố định trong vault | Tổng hợp tuần cần dữ liệu gộp, không vỡ vụn theo dự án |
| D4 | Rubric gốc tách rời lớp hiệu chỉnh (profile) | Đổi profile là phát cho trợ lý/quản đốc dùng được, không đụng rubric |
| D5 | Can thiệp = kê thí nghiệm hành vi cho việc thật kế tiếp | Đóng được vòng học; chỉ chỉ lỗi thì không đổi thói quen |
| D6 | Đóng gói: 3 skill mỏng + tầng tham chiếu dùng chung, thuần Markdown | Mỗi skill một việc; dạng chắc chắn nhất Cowork nạp được |

Đã cân nhắc và loại: một skill đa chế độ (một file gánh 3 quy trình → dài, dễ lẫn), và MCP server ghi sổ (đại bác bắn chim sẻ ở nhịp ~1 bản ghi/ngày; để dành khi sổ đủ lớn mà thống kê bắt đầu sai).

## 3. Kiến trúc

```
plugins/fluency-4d/
├── .claude-plugin/plugin.json
├── README.md                       ← cách import vào Cowork + quyền truy cập sổ
└── skills/
    ├── fluency-4d-preflight/SKILL.md
    ├── fluency-4d-review/SKILL.md
    ├── fluency-4d-weekly/SKILL.md
    └── fluency-4d-shared/references/
        ├── active-profile.md          ← tầng trỏ: profile nào đang bật
        ├── rubric-core.md
        ├── improvement-playbook.md
        ├── profile-template.md        ← khuôn rỗng, không bao giờ được bật
        ├── profile-workshop-x.md
        ├── profile-quan-doc.md        ← nháp, cờ đỏ chờ CEO chốt
        ├── ledger-schema.md
        └── experiment-protocol.md
```

| Skill | Mục đích | Đọc | Ghi |
|---|---|---|---|
| `fluency-4d-preflight` | Cổng trước khi giao việc lớn | rubric · profile · thí nghiệm đang mở | *(không ghi)* |
| `fluency-4d-review` | Mổ xẻ phiên vừa xong, chấm 4D, kê thí nghiệm | rubric · profile · phiên hiện tại · `experiments.md` | 1 dòng `sessions.jsonl` + cập nhật `experiments.md` |
| `fluency-4d-weekly` | Xu hướng, bảng gợi ý cải tiến, chọn D ưu tiên tuần tới | `sessions.jsonl` (cửa sổ 7 ngày) · `experiments.md` · playbook · profile | `weekly/<năm>-W<tuần>.md` |

**Ranh giới bắt buộc giữ:**
- `rubric-core.md` không được nhắc tới Workshop X, dự án, hay quy ước nội bộ nào.
- `profile-*.md` không được định nghĩa lại thang điểm; chỉ bổ sung *tín hiệu cần soi*, *cờ đỏ*, *ví dụ ngành*, *cách cải tiến tại chỗ*.
- `improvement-playbook.md` cũng trung lập ngành như rubric. Weekly **chọn dòng** từ menu này, cấm tự sinh cách cải tiến lúc chạy — coach tự kê bài tập cho hành vi nó vừa chấm là vòng lặp tự phục vụ.
- Weekly **không** tự viết câu nếu–thì. Nó đưa ứng viên kèm số; câu cam kết do người dùng viết.
- Skill không chứa logic tính toán ngoài số học đơn giản (trung bình, đếm streak).

**Cố tình không làm:** không hook, không Python, không nhân bản vào `skills/learn/` (một nguồn duy nhất, tránh trôi lệch). Muốn dùng trong Claude Code thì tạo junction từ `~/.claude/commands/`.

## 4. Rubric lõi

Bám nguyên bản AI Fluency Framework (Dakan–Feller / Anthropic, CC BY-NC-SA 4.0). Nguồn gốc đối chiếu: `D:\Workshop_X\3_Resources\Technical-References\AI-Fluency-Course-Source\` bài 03, 06, 08, 10, 12.

**12 ô chấm:**

| D | 3 thành phần con |
|---|---|
| Delegation | Problem Awareness · Platform Awareness · Task Delegation |
| Description | Product · Process · Performance |
| Discernment | Product · Process · Performance |
| Diligence | Creation · Transparency · Deployment |

**Trường ngữ cảnh:** chế độ tương tác của phiên — `automation` / `augmentation` / `agency`. Delegation phải được chấm theo chế độ (giao Agency mà mô tả kiểu Automation là lỗi Delegation, không phải lỗi Description).

**Thang điểm:**

| Điểm | Nghĩa |
|---|---|
| 3 | Chủ động, nhất quán, trích dẫn được bằng chứng |
| 2 | Có làm nhưng thiếu hoặc không nhất quán |
| 1 | Chỉ xảy ra khi AI hoặc hoàn cảnh nhắc, không tự phát |
| 0 | Có cơ hội rõ ràng mà bỏ qua, hậu quả quan sát được trong phiên |
| `n/a` | Phiên không tạo cơ hội để quan sát (khác 0) |

**Ba chốt chống coach nịnh** — coach đang chấm chính cuộc hợp tác mà nó là một nửa:
1. **Không bằng chứng, không điểm.** Mọi ô ≠ 3 phải kèm trích dẫn nguyên văn từ phiên. Không trích dẫn được → `n/a`.
2. **Bắt buộc tìm điểm đau.** Báo cáo phải nêu ít nhất một ô ≤ 1, hoặc tuyên bố thẳng "không tìm thấy ô nào dưới 2" kèm lý do.
3. **Chấm trước, khen sau.** Điểm và trích dẫn ra trước; phần ghi nhận điểm mạnh viết sau khi đã chốt điểm.

## 5. Lớp hiệu chỉnh (`profile-workshop-x.md`)

Cấu trúc cố định — mỗi ô là một khối `## <mã ô>` chứa `**Tín hiệu:**` / `**Cờ đỏ:**` / `**Ví dụ ngành:**` / `**Cách cải tiến tại chỗ:**`.

| Ô | Tín hiệu Workshop X |
|---|---|
| `del.problem` | Task đã phân loại COD chưa? Core mà giao AI → điểm thấp bất kể kết quả tốt. Trần C < 60% |
| `del.platform` | Đúng tầng model (Opus: kiến trúc/gate; Haiku: đọc file/docs/test)? Có skill KN-Stack sẵn mà vẫn làm tay? |
| `del.task` | Chia việc theo phase Pahl-Beitz hay quăng cả cục? Giữ lại phán đoán thiết kế? |
| `des.product` | Nêu tiêu chí "xong" và định dạng bàn giao? Đơn vị mét tuyệt đối? |
| `des.process` | Chỉ định quy trình sẵn (3-Gate, VDI 2225, ODI) hay để AI tự chế? |
| `des.performance` | Có yêu cầu AI phản biện thay vì gật? |
| `dis.product` | Chạy ratio-check / đòi bằng chứng vật lý (dP/dt) trước khi tin số? |
| `dis.process` | Nguồn có phân tier S/A/B/C? Có kiểm chéo? |
| `dis.performance` | Bắt được lúc AI trôi sang analyst-trap (đẻ thêm phân tích thay vì dữ liệu vật lý)? |
| `dil.creation` | Không dữ liệu MẬT, không giá nhà cung cấp vào prompt |
| `dil.transparency` | Tài liệu giao ngoài (BQP, hội đồng) ghi rõ phần AI tham gia? |
| `dil.deployment` | Không commit thẳng main, chạy test trước PR, tự chịu trách nhiệm nội dung ký tên |

Phát cho người khác: viết `profile-<tên>.md` theo đúng khung trên rồi đổi **một dòng** trong
khối mã của `active-profile.md`. Ba skill không gọi tên profile nữa nên không phải sửa.

Chốt của tầng trỏ: profile còn ô `⟨CEO chốt: …⟩` **không được bật**, và `profile-template.md`
không bao giờ được bật. Bật một profile chưa điền xong nghĩa là chấm điểm theo tín hiệu chưa
ai chốt — báo cáo vẫn ra đủ hình, nên lỗi này im lặng nếu không có cổng chặn.

## 6. Sổ điểm

**Nơi lưu:** `D:\Workshop_X\2_Areas\CEO-Self\AI-Fluency-Ledger\`

```
AI-Fluency-Ledger/
├── sessions.jsonl        ← mỗi lần mổ xẻ = 1 dòng, chỉ APPEND
├── experiments.md        ← thí nghiệm hành vi, có trạng thái
└── weekly/2026-W31.md    ← báo cáo tuần
```

**Schema một dòng `sessions.jsonl`** (bản mẫu này nằm nguyên văn trong `ledger-schema.md` để sao chép):

```json
{"id":"2026-08-01-1","date":"2026-08-01","project":"VN-TGT-F","mode":"augmentation",
 "scores":{"del":{"problem":2,"platform":3,"task":1},
           "des":{"product":2,"process":0,"performance":null},
           "dis":{"product":1,"process":2,"performance":3},
           "dil":{"creation":3,"transparency":null,"deployment":2}},
 "weakest":"des.process","exp_active":"EXP-014","exp_held":true}
```

- `null` = `n/a`. Mọi khóa luôn có mặt, kể cả khi `null`.
- `id` = `<ngày>-<số thứ tự phiên trong ngày>`.
- Trích dẫn bằng chứng **không** vào JSONL (làm hỏng file) — nó nằm trong báo cáo mổ xẻ in ra màn hình. Sổ chỉ giữ con số.
- Nếu chưa có thí nghiệm nào mở: `"exp_active":null,"exp_held":null`.

## 7. Vòng thí nghiệm (`experiment-protocol.md`)

- **WIP = 1.** Chỉ một thí nghiệm mở tại một thời điểm. Coach phát hiện 5 điểm yếu vẫn chỉ được kê 1. Ràng buộc cứng.
- Viết dạng **nếu–thì**, hành vi quan sát được: *"Khi giao task > 30 phút, tôi nêu tiêu chí 'xong' trước khi bấm gửi."* Cấm viết kiểu "chú ý Description hơn".
- **Cách đo:** quan sát được ngay trong phiên sau → `exp_held: true/false`.
- **Nghiệm thu:** giữ được **3 phiên liên tiếp** → `PASSED`, đóng, mở thí nghiệm mới. Đứt giữa chừng → streak đếm lại từ 0. Đứt 3 lần → `FAILED`; coach phải kê thí nghiệm **nhỏ hơn**, không kê lại nguyên văn cái cũ.

**Bảng `experiments.md`:** `ID | ô mục tiêu | câu nếu–thì | streak | đứt | trạng thái | ngày mở | ngày đóng`
Cột `đứt` đếm số lần streak bị phá; đạt 3 → `FAILED`.
Trạng thái: `OPEN` · `PASSED` · `FAILED`.

## 8. Ba quy trình

### 8.1 `fluency-4d-preflight`
1. Đọc thí nghiệm `OPEN` trong `experiments.md`, nhắc lại một dòng.
2. **Cổng Delegation** — việc này C/O/D? Chế độ nào? Phần nào giữ lại tự làm? Nếu là Core mà định giao → chặn, hỏi lại.
3. **Cổng Description** — sản phẩm (tiêu chí "xong", định dạng), quy trình (khung nào), vai (phản biện hay thừa hành).
4. Trả về *phiếu giao việc* đã viết lại, sẵn sàng dùng.
Không ghi gì vào sổ.

### 8.2 `fluency-4d-review` — 6 bước cố định
1. Trích bằng chứng nguyên văn từ **phiên hội thoại hiện tại** (nội dung đang có trong ngữ cảnh, không đọc file log ngoài).
2. Chấm 12 ô theo `rubric-core.md` + tín hiệu `profile-workshop-x.md`.
3. **Nghiệm thu thí nghiệm đang mở trước** khi làm gì khác — giữ hay đứt, cập nhật streak.
4. Chọn ô yếu nhất: điểm thấp nhất. Hòa → ô xuất hiện làm `weakest` nhiều lần nhất trong `sessions.jsonl` 30 ngày gần nhất. Vẫn hòa → theo thứ tự ưu tiên `dil` > `dis` > `des` > `del`.
5. Kê thí nghiệm mới **chỉ khi** không còn thí nghiệm `OPEN`. Còn `OPEN` → giữ nguyên, dù tìm được điểm yếu nặng hơn.
6. Append 1 dòng vào `sessions.jsonl`; cập nhật `experiments.md`.

**Ngoại lệ cờ đỏ:** `dil.*` = 0 (rò rỉ MẬT, giá nhà cung cấp, commit thẳng main) **không** đi vào vòng thí nghiệm — bật cảnh báo xử ngay trong phiên, đặt trên đầu báo cáo.

### 8.3 `fluency-4d-weekly`
1. Đọc `sessions.jsonl`, lọc cửa sổ 7 ngày.
2. Trung bình từng ô (bỏ qua `null`), so với cửa sổ 7 ngày liền trước.
3. Liệt kê ô yếu dai dẳng (thấp ≥ 2 tuần liên tiếp) + tình trạng streak thí nghiệm.
4. Chốt **1 D ưu tiên** cho tuần tới.
5. Ghi `weekly/<năm>-W<tuần ISO>.md`.

**Chốt dữ liệu mỏng:** dưới 3 phiên trong cửa sổ → in thẳng "dữ liệu mỏng, không kết luận xu hướng" và dừng ở bước liệt kê, không vẽ xu hướng.

## 9. Kiểm chứng

1. **Eval tĩnh** `evals/fluency-4d-review.json` (`mode: "static"`) — soi `SKILL.md` có đủ: 6 bước theo đúng thứ tự, 3 chốt chống nịnh, ràng buộc WIP = 1, ngoại lệ cờ đỏ Diligence, schema JSONL khớp `ledger-schema.md`.
2. **Fixture hội thoại mẫu** đặt tại `evals/fixtures/fluency-4d-session.md`, cài sẵn lỗi biết trước: mô tả sản phẩm mơ hồ, nhận số liệu không kiểm chứng, dán giá nhà cung cấp vào prompt. Chạy `fluency-4d-review` lên fixture phải cho: `des.product` ≤ 1, `dis.product` ≤ 1, và bật cờ đỏ `dil.creation` = 0. Không đạt → rubric chưa dùng được.
3. **Thử vòng đời sổ:** chạy review 4 lần liên tiếp **trên cùng một fixture**, kiểm `sessions.jsonl` có đúng 4 dòng hợp lệ JSON, `experiments.md` chạy đúng đứt 1→2→3→`FAILED`.

   Chạy lại cùng fixture thì **`FAILED` mới là kết quả đúng, không phải `PASSED`.** Fixture ở mục 2 cài sẵn chính lỗi mà thí nghiệm nhắm tới (`dil.creation` = 0 vì dán giá nhà cung cấp); lỗi đó có mặt trong mọi lần chạy, nên hành vi bị đứt mọi lần, streak không thể nhích. Đòi vừa chạy cùng fixture vừa lên `PASSED` là đòi hai thứ loại trừ nhau — bản spec trước mắc đúng lỗi này.

   Muốn thử nhánh `PASSED` thì phải là **fixture thứ hai đã sửa lỗi đó**, chạy 3 lần: streak 1→2→3→`PASSED`. Hai nhánh là hai phép thử khác nhau, đừng gộp.
4. **README.md** ghi các bước import vào Cowork và đường dẫn sổ cần cấp quyền đọc/ghi.

## 10. Ngoài phạm vi

- Hook tự động giữa phiên (phụ thuộc Cowork chạy `hooks/` — chưa xác nhận).
- MCP server ghi sổ.
- Thư viện drill / bài tập giả — đã có ở Student D–D Drills.
- Đồng bộ điểm sang Galaxy note hay Tana.
- Phát hành profile cho trợ lý/quản đốc (kiến trúc đã chừa chỗ, nhưng không làm trong đợt này).

## 11. Tài liệu nguồn

- `D:\Workshop_X\3_Resources\Technical-References\AI-Fluency-Course-Source\` — bài 03 (khung 4D + 3 chế độ), 06 (Delegation), 08 (Description), 10 (Discernment), 12 (Diligence).
- Bản quyền khung gốc: Rick Dakan, Joseph Feller, Anthropic — CC BY-NC-SA 4.0. `rubric-core.md` phải ghi nhận nguồn này.
