# Cổng phân loại — chạy khi `surface: cloud`

> Kích hoạt: chỉ khi profile workspace đang bật khai `surface: cloud`.
> Ở `surface: local` cổng này KHÔNG chạy, hành vi pipeline giữ nguyên như cũ.

## Vì sao có cổng này

Rào cứng #2 của `ip-invent` từng gộp hai thứ khác hẳn nhau vào một câu cấm. Tách ra:

- **Bí mật nhà nước — bí mật quân sự.** Cấm tuyệt đối đưa ra bất kỳ dịch vụ ngoài nào, không
  ngoại lệ, bất kể có bộc lộ công khai hay không. Đây là cái cổng thật.
- **Chưa bộc lộ nhưng không thuộc bí mật nhà nước.** Điều 60.2 Luật SHTT: bộc lộ cho *"một số
  người có hạn được biết và có nghĩa vụ giữ bí mật"* **không** làm mất tính mới. Dịch vụ có nghĩa
  vụ bảo mật theo hợp đồng rơi vào diện đó.

Việc coi một bề mặt cloud cụ thể là "có nghĩa vụ bảo mật" là **quyết định của CEO, không phải kết
luận pháp lý** của skill này — cùng tinh thần cổng advisory-only đã có trong `ip-invent`.

## Bước 0′ — chạy TRƯỚC khi đụng nội dung ứng viên bất kỳ

Hỏi CEO phân loại từng ứng viên, **kèm căn cứ** (văn bản/quyết định nào nói thế). Không nhận câu
trả lời trống, không suy diễn hộ.

| Phân loại | Xử |
|---|---|
| Thuộc / nghi thuộc **bí mật nhà nước — bí mật quân sự** | **DỪNG.** Không xử nội dung, không tóm tắt, không diễn giải. Chỉ CEO quay về **Claude Code local** (đổi `active-workspace.md` sang `workspace-knstack.md`). |
| **Chưa rõ** — chưa có văn bản xác định | **coi như thuộc** → **DỪNG.** Bám đúng nguyên tắc `ip-dossier` đã có: *"Chưa có văn bản xác định bí mật nhà nước ⇒ coi như CHƯA RÕ"*. Mặc định thận trọng, nên bấm bừa không mở được cổng. |
| **Không thuộc** — dân dụng, hoặc lưỡng dụng đã tách phần MẬT, hoặc đã khóa priority date | Chạy tiếp. |

## Ghi và in lại

- Ghi trạng thái cổng vào ledger `_pipeline_state.md`, mục **Cờ ràng buộc**.
- **Mỗi block in lại ở đầu báo cáo:** `Bề mặt: <surface> · Cổng phân loại: <trạng thái> · Căn cứ: <…>`
  CEO không bao giờ được đọc một đầu ra mà không biết nó chạy trên bề mặt nào.

## Cái cổng này KHÔNG làm

- Không thay cơ quan có thẩm quyền xác định danh mục bí mật nhà nước.
- Không kết luận một giải pháp "an toàn để đưa lên cloud" — nó chỉ chặn, không cấp phép.
- Không thay cổng bộc lộ (Điều 60) và cổng Điều 14 nộp nước ngoài. Ba cổng độc lập, phải qua cả ba.
