# Schema sổ điểm

Sổ nằm ở: `D:\Workshop_X\2_Areas\CEO-Self\AI-Fluency-Ledger\`

```
AI-Fluency-Ledger/
├── sessions.jsonl        ← mỗi lần mổ xẻ = 1 dòng, CHỈ APPEND
├── experiments.md        ← thí nghiệm hành vi
└── weekly/2026-W31.md    ← báo cáo tuần
```

## Bản mẫu — sao chép nguyên khung này

```json
{"id":"2026-08-01-1","date":"2026-08-01","project":"VN-TGT-F","mode":"augmentation","scores":{"del":{"problem":2,"platform":3,"task":1},"des":{"product":2,"process":0,"performance":null},"dis":{"product":1,"process":2,"performance":3},"dil":{"creation":3,"transparency":null,"deployment":2}},"weakest":"des.process","exp_active":"EXP-014","exp_held":true}
```

## Luật

| Khóa | Kiểu | Luật |
|---|---|---|
| `id` | chuỗi | `<YYYY-MM-DD>-<số thứ tự phiên trong ngày>` |
| `date` | chuỗi | `YYYY-MM-DD` |
| `project` | chuỗi | Mã dự án hoặc chủ đề phiên. Không để rỗng |
| `mode` | chuỗi | `automation` · `augmentation` · `agency` |
| `scores` | object | Đúng 4 nhóm `del`/`des`/`dis`/`dil`, mỗi nhóm đúng 3 khóa con. **Mọi khóa luôn có mặt**, kể cả khi `null` |
| giá trị điểm | số / null | Số nguyên `0`–`3`, hoặc `null` (= `n/a`) |
| `weakest` | chuỗi / null | Ô có điểm **thấp nhất tuyệt đối** trong phiên, **kể cả** ô `dil.*` đang bị cờ đỏ. `null` nếu không có ô nào ≤ 2 |
| `exp_active` | chuỗi / null | `EXP-###` của thí nghiệm đang mở |
| `exp_held` | bool / null | Phiên này có giữ được thí nghiệm không |

**Ràng buộc chéo:** `exp_active` và `exp_held` phải cùng `null` hoặc cùng có giá trị.

**Phiên mở thí nghiệm.** Phiên MỞ thí nghiệm ghi `"exp_active": null, "exp_held": null` — thí nghiệm
chỉ được tính từ phiên KẾ TIẾP trở đi. Không thể "giữ" một cam kết chưa tồn tại lúc phiên đó diễn ra.
Luật này ghi giống hệt ở `experiment-protocol.md` luật 3.

**`weakest` không phải ô mục tiêu thí nghiệm.** `weakest` giữ ô thấp nhất tuyệt đối, kể cả cờ đỏ
`dil.*` = 0 — để một thất bại Diligence mạn tính vẫn nhìn thấy được trong lịch sử `weakest` 30 ngày. **Hòa** → ô xuất hiện làm `weakest` nhiều lần nhất trong `sessions.jsonl` 30 ngày gần nhất. **Vẫn hòa** → thứ tự ưu tiên `dil` > `dis` > `des` > `del`, trong cùng nhóm theo thứ tự chính tắc (`problem`/`platform`/`task` cho `del`; `product`/`process`/`performance` cho `des` và `dis`; `creation`/`transparency`/`deployment` cho `dil`).
Ô mà thí nghiệm nhắm tới (đã loại cờ đỏ) nằm ở cột `ô mục tiêu` của `experiments.md`, không có
trường riêng trong sổ này.

**Trích dẫn bằng chứng KHÔNG vào file này** — xuống dòng và ký tự đặc biệt sẽ làm hỏng JSONL. Bằng chứng nằm trong báo cáo mổ xẻ in ra màn hình. Sổ chỉ giữ con số.

**Chỉ append.** Không sửa, không xóa dòng cũ. Chấm sai thì ghi dòng mới cùng ngày với số thứ tự kế tiếp và ghi chú trong báo cáo.
