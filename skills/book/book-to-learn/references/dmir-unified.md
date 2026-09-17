# DMIR hợp nhất — tham chiếu cho /book-to-learn

## Nguồn và cảnh báo
- Nguồn: 3 tài liệu CEO cung cấp 2026-09-17 — *D-M-I-R × ODI × Engineering Design (Pahl & Beitz)* v1.0; *The D-M-I-R Unified Model for Systemic Change: A Deep Dive*; *Unified Model for Systemic Change (D–M–I–R) — Deep Research & Playbook v1.0 (02/11/2025)*. Bối cảnh vault: `2_Areas/CEO-Self/Learning-Architecture/DMIR_Skill_Architecture_v2.md`.
- Chỉ dùng **cấu trúc, câu hỏi, template**. Các con số trong tài liệu gốc không có nguồn kiểm được ("70% nỗ lực thay đổi thất bại", "nhanh hơn 15 lần", "ROI 10–50x", các case ghi "giả lập") — **không trích như sự thật**.
- Tên: **Diagnose–Model–Intervene–Reflect**. `1_Projects/BB-01_LOMAH/References/dmir1…4` dùng Diagnose–Measure–Improve–Review — biến thể khác, không trộn.
- DMIR là **tầng meta**, không phải framework thứ tư cạnh BRIDGE/FORGE/HELIX.

## Bốn pha
| Pha | Trường phái | Câu hỏi chính | Skill KN-Stack | Đòn bẩy hay chạm |
|---|---|---|---|---|
| D | Systems Thinking | Ranh giới hệ ở đâu? Archetype nào đang chạy? Mô hình tư duy ngầm nào sinh ra hành vi này? | `/archetype`, `/cld` | L1–L4, L6 |
| M | System Dynamics | Stock nào, flow nào, trễ bao lâu, vòng R/B nào trội? Biến then chốt hiện tại → mục tiêu? | `/cld`, `/sdmodel` (chỉ khi CEO yêu cầu) | L7–L10 |
| I | Theory of Constraints | Điểm nghẽn là gì? Khai thác → phối thuộc → nâng cấp → quay lại? Can thiệp ở mức đòn bẩy nào? | `/constraint`, `/leverage` | L5, L10 |
| R | Meta-learning | Định xảy ra gì / thực tế / vì sao khác / lần sau? Mục tiêu (L3) và mô hình tư duy (L2) có sai? | `/reflect`, `/paradigm` | L1–L3 |

## DMIR bản nhẹ cho chu kỳ 30 ngày
- D + M tối đa 2 phiên. M = 1 CLD + 3 biến có số hiện tại → mục tiêu. Không dựng mô hình SD trừ khi CEO yêu cầu.
- I = một can thiệp, một chỉ số, baseline là số, thời lượng ≤ 16 ngày, dự đoán ghi trước.
- R = AAR 4 câu + vòng kép + cập nhật sổ meta.

## Thang đòn bẩy Meadows
L12 tham số · L11 buffer · L10 cấu trúc stock/flow · L9 độ trễ · L8 vòng cân bằng · L7 vòng tăng cường · L6 dòng thông tin · L5 luật chơi · L4 tự tổ chức · L3 mục tiêu · L2 paradigm · L1 vượt paradigm.
Qua các chu kỳ, mục tiêu là leo dần: L10 → L6 → L5 → L3 → L2.
Ví dụ gán mức cho framework của sách (Profit First): tỉ lệ phân bổ % = L12; "Doanh thu − Lợi nhuận = Chi phí" = L5; hỏi "lành mạnh?" thay vì "to cỡ nào?" = L3.

## Archetype cần nhận diện (D)
Fixes That Fail · Shifting the Burden · Limits to Growth · Success to the Successful · Escalation · Tragedy of the Commons · Drift to Low Performance · Seeking the Wrong Goal (Goodhart) · Rule Beating · Policy Resistance.

## Năm bước tập trung TOC (I)
1 Xác định điểm nghẽn · 2 Khai thác (chưa thêm năng lực) · 3 Phối thuộc mọi thứ khác theo điểm nghẽn · 4 Nâng cấp (tốn tiền — làm sau 2 và 3) · 5 Điểm nghẽn dời thì quay lại bước 1, tránh quán tính.

## AAR và học vòng kép (R)
- AAR: Định xảy ra gì · Thực tế ra sao · Vì sao khác · Lần sau làm gì.
- Vòng đơn: sửa hành động trong giả định cũ. Vòng kép: chất vấn mục tiêu và luật chơi. Deutero-learning: học từ chính các lần học.
- Mức siêu nhận thức Perkins: tacit → aware → strategic → reflective.

## Học cách học (meta-learning trong từng cuốn)
Nguồn: `3_Resources/Tools & Software/Skills/deep-content-analyzer-v3/` Phần 3 (KN-Stack: `/analyze`) và `5_Skills_AI_Cant_Replace_Multi_Framework_Analysis.md`.

| Kỹ thuật | Tiêu chí chất lượng | Skill |
|---|---|---|
| Chunking | Ghi chỗ thứ tự phụ thuộc ≠ thứ tự trình bày | `learn-methodology` |
| Feynman | 60 giây + phép so sánh + 3 câu: hiểu → áp dụng → tầng hệ thống | `learn-methodology` |
| Mnemonic | Mỗi chữ là một hành động | `learn-methodology` |
| Rubric | Chỉ báo hành vi, không phải kiến thức | `learn-track` |
| Drill | Nhắm framework đòn bẩy cao nhất hoặc chỗ hay sai | `learn-practice` |
| Interleaving | Không hai khối liền nhau cùng chủ đề; khối sách xen việc thật | `learn-practice` |
| Journal | ≥1 câu về vòng lặp phản hồi, ≥1 câu về cách học | `learn-track` |
| Ôn giãn cách + đoán trước | Lệch đoán–thực ghi thành số | `learn-teach` |

## Meta-learning là một stock
- Đơn vị: tốc độ thích nghi — trong skill đo bằng `days_to_competence` (L0 → thẻ L5 được duyệt).
- Dòng vào: luyện tập siêu nhận thức có chủ đích; trải nghiệm đa dạng. Dòng ra: tự mãn.
- Vòng R4 lợi thế học tập cộng dồn: học nhanh → sớm có năng lực → việc thú vị hơn → đa dạng hơn → học nhanh hơn. Mức đòn bẩy L2.

## Khi KHÔNG dùng DMIR đầy đủ
Vấn đề đơn giản, nhân quả rõ; khủng hoảng cần hành động ngay (làm trước, DMIR sau); ràng buộc thật là ý chí chính trị bên ngoài.
