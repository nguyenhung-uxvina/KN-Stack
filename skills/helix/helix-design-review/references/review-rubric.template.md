# review_rubric.md — Template (Guide cho helix-design-review)

> Kỹ sư định danh SỞ HỮU file này. Điền chiều chấm + severity + confidence THẬT cho dự án trước khi review.
> Rubric là Guide: biến review từ cảm tính thành có kỷ luật. Có phiên bản (rubric_version).

```yaml
meta:
  product: VSN-1500-HKN
  rubric_version: "0.1.0"
  owner: "(tên kỹ sư định danh)"
  classification: HẠN-CHẾ        # MẬT/HẠN-CHẾ → model LOCAL, không cloud

severity_scale:
  advisory: "nên xem, không cản freeze"
  concern: "nên sửa trước freeze"
  blocker_candidate: "NÊN thành luật cứng — đề xuất nâng vào design_rules.json (KHÔNG tự chặn)"

confidence_scale:
  HIGH: "bằng chứng trực tiếp, rõ ràng"
  MED: "suy luận từ bằng chứng gián tiếp"
  LOW: "nghi ngờ, thiếu bằng chứng — KHÔNG được trình như chắc chắn"

dimensions:
  - key: intent_naming
    hỏi: "Tên chi tiết/feature có nhất quán, đúng quy ước dự án không?"
  - key: bom_model_consistency
    hỏi: "BOM có khớp mô hình (số lượng, mã, vật liệu) không? Có mã title-block cũ dán nhầm không?"
  - key: revision_lineage
    hỏi: "Revision có mạch lạc không? Có bản mồ côi / rev nhảy cóc không?"
  - key: cross_doc_conflict
    hỏi: "Note vẽ / dim / ICD / requirements có mâu thuẫn nhau không?"
  - key: nonstructural_judgment
    hỏi: "Yếu tố phi cấu trúc (thủy động khoang phao, khả lắp, ergonomics) có smell không?"
  - key: dfm_soft
    hỏi: "Có vấn đề chế tạo NGOÀI luật cứng (trình tự hàn, tiếp cận dụng cụ) không?"
  - key: completeness
    hỏi: "Thiếu GD&T / dung sai ở nơi chức năng thực sự cần không?"

quy_tac:
  - "Mỗi finding PHẢI trỏ evidence cụ thể (field/dòng), không phán chung chung."
  - "Thiếu bằng chứng → confidence LOW, KHÔNG bịa."
  - "Chiều nào sạch → ghi 'clean', đừng bịa finding cho đủ."
  - "blocker_candidate = ĐỀ XUẤT nâng luật, KHÔNG tự chặn gate."
```
