# Mastery Track — Làm Chủ Khung Harness Engineering v1.0

> Dùng bởi mode `--mastery`. Lộ trình 6 module bám 11 mục khung v1.0, đưa CEO từ HIỂU → ÁP DỤNG → LÀM CHỦ.
> Mỗi module: (a) Khái niệm cốt lõi + trích nguồn → (b) Áp dụng 1 sản phẩm WX cụ thể → (c) 1 bài tập build cấu phần harness THẬT trong tuần.
> Nguyên lý chủ đạo: "mỗi lỗi → một bản sửa vĩnh viễn" — làm chủ = build được harness thật, không phải đọc xong.

## Bản đồ lộ trình

| Module | Tên | Mục khung v1.0 | Năng lực đạt được | Bài tập build thật |
|:------:|-----|----------------|-------------------|--------------------|
| 1 | Định vị & Vocabulary | §1, §3, §4 | Phân biệt 3 tầng; nói đúng Guides/Sensors/Gates, Computational/Inferential | Viết 1 trang phân loại: liệt kê 5 "quy trình duyệt người" hiện có của WX → map vào Guide/Sensor/Gate |
| 2 | AGENTS.md & Bộ nhớ ngoài | §6, §3.3 | Thiết kế AGENTS.md "bản đồ không bách khoa"; externalize memory | Tạo AGENTS.md thật cho 1 codebase (vd FCS/C-UAS) — mỗi dòng truy về 1 lỗi quan sát được |
| 3 | Gates cưỡng chế (Lập trình) | §5.1, §4 | "Cơ chế không phải prompt"; CI gate; chặn auto-merge firmware | Dựng 1 CI gate (linter/test) chặn merge; khóa quyền agent sửa cấu hình rào của chính nó |
| 4 | Eval Harness & Improvement Engine | §3.3, §4, §10-GĐ2 | Đo "thay đổi harness có cải thiện thật"; vòng vá lỗi vĩnh viễn | Lập 1 bộ eval kịch bản cố định + ghi metric cho 1 agent; chạy lại sau mỗi sửa AGENTS.md |
| 5 | Harness Vật Lý (khác biệt hóa) | §5.2, §5.3, §5.4, §7 | Tự xây sensor cho artefact vật lý (FEA/NDT/coupon) | Chọn 1: surrogate-FEA validator (Thiết kế) HOẶC pipeline AI-QC hàn false-negative (Chế tạo) HOẶC eval coupon (Thử nghiệm) — viết spec sensor đầu tiên |
| 6 | Chủ Quyền & Lộ Trình | §8, §9, §10, §11 | Air-gapped, mô hình cắm-rút, khả chuyển bộ nhớ; gắn hồ sơ chuyên gia | Viết bản đồ tài sản WX hiện có → harness (Improvement Engine / earned-autonomy / 2-vùng staging) + lộ trình GĐ1-3 cho 1 dòng SP |

## Chi tiết từng module (query template cho NLM)

### Module 1 — Định vị & Vocabulary
- Query: "Giải thích 3 tầng prompt/context/harness và vì sao harness là tầng quyết định. Định nghĩa Guides vs Sensors, Computational vs Inferential. Cho ví dụ mỗi loại trong môi trường khí tài."
- Self-check: Quiz 5Q (artifact 8dc888d3). Đạt khi giải thích được "vì sao prompt sẽ bị quên ở lượt thứ 47".

### Module 2 — AGENTS.md & Bộ nhớ ngoài
- Query: "Nguyên tắc thiết kế AGENTS.md (bản đồ không bách khoa, lớn dần theo lỗi, mọi tri thức có phiên bản). 5 cấu phần bắt buộc: sandbox, bộ nhớ ngoài, sub-agent tường lửa ngữ cảnh, approval gate, eval harness. Lưu ý mật/air-gapped."
- Bài tập: AGENTS.md thật + claude-progress.txt cho 1 dự án.

### Module 3 — Gates cưỡng chế (pha Lập trình)
- Query: "Bảng Guides–Sensors–Gates pha Lập trình. Bẫy điển hình: agent tự sửa .eslintrc tắt luật. Vì sao cấm auto-merge mã AI vào firmware tới hạn. Cơ chế không phải prompt."
- Bài tập: 1 CI gate thật.

### Module 4 — Eval Harness & Improvement Engine
- Query: "Eval harness là gì, cách dùng để biết thay đổi harness có cải thiện. Improvement Engine (mỗi lỗi → bản sửa vĩnh viễn). Cách LangChain tăng 13.7 điểm chỉ sửa harness."
- Bài tập: bộ eval + metric.

### Module 5 — Harness Vật Lý
- Query: "Vì sao harness hiện chỉ xoay quanh coding agent? Các sensor vật lý cần tự xây (FEA validator, NDT integration, design validator, eval coupon). Bảng Guides–Sensors–Gates cho 3 pha Thiết kế/Chế tạo/Thử nghiệm. Logic giống chuẩn hóa ISO 9606-2."
- Bài tập: spec 1 sensor vật lý.

### Module 6 — Chủ Quyền & Lộ Trình
- Query: "Harness là tầng chủ quyền. Air-gapped: cấu phần nào chạy offline. Bản đồ tài sản WX hiện có ↔ harness engineering. Lộ trình GĐ1-3. Gắn hồ sơ chuyên gia CNQP (3 điểm nhấn)."
- Bài tập: bản đồ tài sản + lộ trình.

## Tracking
Ghi tiến độ trong `D:/Workshop_X/3_Resources/Mentor-Board/harness-engineering-council/profile.md` mục `### Mastery Progress`:
| Module | Date done | Self quiz | Cấu phần harness đã build THẬT | Retro |
Làm chủ thật = cột "đã build THẬT" đầy, không phải cột "đã đọc".
