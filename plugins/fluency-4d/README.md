# fluency-4d

Plugin Claude tự chứa (Markdown/JSON thuần, không Python/hook/MCP) huấn luyện **AI Fluency** theo khung 4D —
Delegation · Description · Discernment · Diligence — ngay trên các phiên làm việc thật, không phải bài tập giả lập.

## Plugin làm gì

Ba skill chấm/huấn luyện một khung 12 ô năng lực chung (`del.problem`, `del.platform`, `del.task`,
`des.product`, `des.process`, `des.performance`, `dis.product`, `dis.process`, `dis.performance`,
`dil.creation`, `dil.transparency`, `dil.deployment`), cộng bốn file tham chiếu dùng chung ở
`skills/_shared/references/`:

- `rubric-core.md` — 12 ô, thang điểm 0–3/`null`, ba chốt chống nịnh. Trung lập ngành, không sửa khi đổi tổ chức.
- `profile-workshop-x.md` — tín hiệu, cờ đỏ, ví dụ ngành cho từng ô — lớp hiệu chỉnh riêng Workshop X.
- `ledger-schema.md` — schema một dòng sổ điểm (`sessions.jsonl`).
- `experiment-protocol.md` — luật thí nghiệm hành vi (WIP=1, dạng nếu–thì, streak/đứt).

### Ba lối vào — khi nào dùng cái nào

| Skill | Dùng khi nào | Ghi gì |
|---|---|---|
| **`fluency-4d-preflight`** | TRƯỚC khi giao một việc lớn cho AI | Không ghi sổ điểm — đây là cổng chặn (Delegation + Description), không phải phép đo. Trả về phiếu giao việc đã viết lại. |
| **`fluency-4d-review`** | NGAY SAU một phiên làm việc vừa xong | Chấm 12 ô kèm bằng chứng trích dẫn, nghiệm thu/kê thí nghiệm hành vi, append 1 dòng vào `sessions.jsonl` + cập nhật `experiments.md`. |
| **`fluency-4d-weekly`** | Cuối tuần, tổng hợp xu hướng | Đọc `sessions.jsonl` 7 ngày, chốt 1 D ưu tiên tuần tới, ghi `weekly/<năm>-W<tuần>.md`. |

Vòng dùng bình thường: `preflight` trước việc lớn → làm việc → `review` ngay sau → lặp lại nhiều phiên trong tuần → `weekly` để thấy xu hướng.

## Import vào Cowork

Copy nguyên thư mục `plugins/fluency-4d/` (gồm `.claude-plugin/plugin.json` + `skills/`) vào thư mục
plugin của Cowork, hoặc trỏ marketplace của Cowork tới repo `KN-Stack` này. Sau khi import, xác nhận
**ba skill xuất hiện**: `fluency-4d-preflight`, `fluency-4d-review`, `fluency-4d-weekly`.

Plugin không chứa Python/hook/MCP — chỉ Markdown + JSON — nên không có bước cài đặt phụ thuộc nào khác.

## Quyền cần cấp

Cấp quyền **đọc/ghi** thư mục sổ điểm: `D:\Workshop_X\2_Areas\CEO-Self\AI-Fluency-Ledger\`
(gồm `sessions.jsonl`, `experiments.md`, `weekly/`). Không có quyền này thì `fluency-4d-review` và
`fluency-4d-weekly` không chạy được — cả hai đều đọc/ghi trực tiếp vào thư mục này.
`fluency-4d-preflight` chỉ cần quyền đọc `experiments.md` (không ghi gì).

## Dùng trong Claude Code

Ba skill được junction vào `~/.claude/commands/` (Windows: `C:\Users\Admin\.claude\commands\`),
trỏ thẳng về thư mục trong `KN-Stack` này — sửa `SKILL.md` ở đây có hiệu lực ngay, không cần cài lại:

```
C:\Users\Admin\.claude\commands\fluency-4d-preflight → D:\KN-Stack\plugins\fluency-4d\skills\fluency-4d-preflight
C:\Users\Admin\.claude\commands\fluency-4d-review     → D:\KN-Stack\plugins\fluency-4d\skills\fluency-4d-review
C:\Users\Admin\.claude\commands\fluency-4d-weekly     → D:\KN-Stack\plugins\fluency-4d\skills\fluency-4d-weekly
```

Gọi bằng `/fluency-4d-preflight`, `/fluency-4d-review`, `/fluency-4d-weekly` (hoặc các cụm trigger
tiếng Việt/Anh khai trong `description` của từng `SKILL.md`).

## Đổi profile (dùng cho tổ chức khác)

`profile-workshop-x.md` chứa toàn bộ tín hiệu/cờ đỏ riêng Workshop X — `rubric-core.md` KHÔNG bao giờ
sửa theo tổ chức. Để phát cho tổ chức khác:

1. Chép `skills/_shared/references/profile-workshop-x.md` → `profile-<tên tổ chức>.md`.
2. Giữ nguyên khung mỗi khối: `## <mã ô>` + đúng ba trường `**Tín hiệu:**` / `**Cờ đỏ:**` / `**Ví dụ ngành:**`
   cho đủ 12 mã ô, đúng thứ tự canonical.
3. Đổi dòng trỏ tới file profile trong cả ba `SKILL.md` (`fluency-4d-preflight`, `fluency-4d-review`,
   `fluency-4d-weekly`) từ `profile-workshop-x.md` sang `profile-<tên tổ chức>.md`.

## Bảo trì

Sau mỗi lần sửa bất kỳ file nào trong `skills/_shared/references/`, chạy:

```bash
python -m pytest scripts/test_fluency_4d.py -v
```

Bộ test (nằm ngoài plugin, ở `scripts/`, vì plugin phải thuần Markdown/JSON) khớp-chéo bốn file tham
chiếu với nhau qua `scripts/fluency_4d_lint.py` — rubric trung lập ngành, profile phủ đủ 12 ô, schema
sổ điểm hợp lệ, vòng đời thí nghiệm (streak/đứt/WIP=1) đúng luật. Ba eval tĩnh
(`evals/fluency-4d-review.json`, `evals/fluency-4d-preflight.json`, `evals/fluency-4d-weekly.json`)
chạy qua `bash evals/run-eval.sh <skill-name>` để audit nội dung `SKILL.md`.

## Bản quyền khung gốc

Khung **AI Fluency Framework** là công trình gốc của **Rick Dakan, Joseph Feller, và Anthropic**,
cấp phép **CC BY-NC-SA 4.0**. `rubric-core.md` trong plugin này là bản chuyển khung gốc sang dạng
chấm-được (12 ô, thang điểm, ba chốt chống nịnh) — không phải bản sao nguyên văn nhưng bám sát cấu
trúc gốc; mọi phần diễn giải riêng của Workshop X nằm tách biệt ở `profile-workshop-x.md`.
