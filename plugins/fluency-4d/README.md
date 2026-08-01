# fluency-4d

Plugin Claude tự chứa (Markdown/JSON thuần, không Python/hook/MCP) huấn luyện **AI Fluency** theo khung 4D —
Delegation · Description · Discernment · Diligence — ngay trên các phiên làm việc thật, không phải bài tập giả lập.

## Plugin làm gì

Ba skill chấm/huấn luyện một khung 12 ô năng lực chung (`del.problem`, `del.platform`, `del.task`,
`des.product`, `des.process`, `des.performance`, `dis.product`, `dis.process`, `dis.performance`,
`dil.creation`, `dil.transparency`, `dil.deployment`), cộng bốn file tham chiếu dùng chung ở
`skills/fluency-4d-shared/references/`:

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

Copy nguyên thư mục `plugins/fluency-4d/` (gồm `.claude-plugin/plugin.json` + `skills/` + `templates/`)
vào thư mục plugin của Cowork, hoặc trỏ marketplace của Cowork tới repo `KN-Stack` này. Sau khi import,
xác nhận **ba skill xuất hiện**: `fluency-4d-preflight`, `fluency-4d-review`, `fluency-4d-weekly`.

Copy **nguyên cây**, đừng copy lẻ từng thư mục skill: `skills/fluency-4d-shared/references/` phải nằm cạnh ba
thư mục skill thì đường dẫn `../fluency-4d-shared/references/…` trong `SKILL.md` mới resolve được. Xong bước
import thì làm tiếp mục **Khởi tạo sổ điểm** bên dưới — plugin không tự dựng sổ.

Plugin không chứa Python/hook/MCP — chỉ Markdown + JSON — nên không có bước cài đặt phụ thuộc nào khác.

## Quyền cần cấp

Cấp quyền **đọc/ghi** thư mục sổ điểm: `D:\Workshop_X\2_Areas\CEO-Self\AI-Fluency-Ledger\`
(gồm `sessions.jsonl`, `experiments.md`, `weekly/`). Không có quyền này thì `fluency-4d-review` và
`fluency-4d-weekly` không chạy được — cả hai đều đọc/ghi trực tiếp vào thư mục này.
`fluency-4d-preflight` chỉ cần quyền đọc `experiments.md` (không ghi gì).

## Khởi tạo sổ điểm — làm MỘT LẦN trước phiên đầu tiên

Plugin không tự dựng sổ khi import. Trước lần chạy `fluency-4d-review` đầu tiên, tạo ba thứ sau
(`fluency-4d-review` Bước 6 cũng tự tạo nếu thiếu, nhưng làm tay trước thì chắc hơn và không phụ
thuộc quyền ghi thư mục mới):

```bash
mkdir -p "D:/Workshop_X/2_Areas/CEO-Self/AI-Fluency-Ledger/weekly"
: > "D:/Workshop_X/2_Areas/CEO-Self/AI-Fluency-Ledger/sessions.jsonl"
cp plugins/fluency-4d/templates/experiments.md \
   "D:/Workshop_X/2_Areas/CEO-Self/AI-Fluency-Ledger/experiments.md"
```

`templates/experiments.md` là bản mẫu đi kèm plugin: nó mang **đúng dòng tiêu đề 8 cột**
(`ID | ô mục tiêu | câu nếu–thì | streak | đứt | trạng thái | ngày mở | ngày đóng`) mà
`scripts/fluency_4d_lint.py` đọc được. Đừng để AI tự bịa bảng — sai một cột là cả bảng không parse
được và `fluency-4d-weekly` mất luôn tình trạng streak. `sessions.jsonl` bắt đầu bằng file rỗng
(0 byte), không phải `[]`.

## Dùng trong Claude Code

Bốn thư mục được junction vào `~/.claude/commands/` (Windows: `C:\Users\Admin\.claude\commands\`),
trỏ thẳng về thư mục trong `KN-Stack` này — sửa `SKILL.md` ở đây có hiệu lực ngay, không cần cài lại:

```
C:\Users\Admin\.claude\commands\fluency-4d-preflight → D:\KN-Stack\plugins\fluency-4d\skills\fluency-4d-preflight
C:\Users\Admin\.claude\commands\fluency-4d-review    → D:\KN-Stack\plugins\fluency-4d\skills\fluency-4d-review
C:\Users\Admin\.claude\commands\fluency-4d-weekly    → D:\KN-Stack\plugins\fluency-4d\skills\fluency-4d-weekly
C:\Users\Admin\.claude\commands\fluency-4d-shared              → D:\KN-Stack\plugins\fluency-4d\skills\fluency-4d-shared
```

**Junction `fluency-4d-shared` là BẮT BUỘC, không phải tuỳ chọn.** Ba `SKILL.md` trỏ tới file tham chiếu bằng
đường dẫn tương đối `../fluency-4d-shared/references/…`. Khi chạy qua junction, mỗi skill nằm trực tiếp dưới
`~/.claude/commands/`, nên `..` không còn là `skills/` của plugin mà là chính `~/.claude/commands/`.
Thiếu junction thứ tư này thì `../fluency-4d-shared/references/` không tồn tại — skill sẽ chạy **không có
rubric và không có profile**, vẫn in ra một báo cáo trông đầy đủ. Có junction thì cùng một đường dẫn
tương đối resolve đúng ở **cả hai** kiểu triển khai (junction rời và cây plugin nguyên vẹn trong
Cowork), nên không `SKILL.md` nào phải sửa. Ba `SKILL.md` cũng đã có chốt "đọc không được thì DỪNG"
để lỗi này không còn im lặng nữa.

Tạo/kiểm cả bốn junction bằng đúng công cụ của repo — `setup.sh` đã biết đi vào `plugins/*/skills/*/`,
không phải bước tay:

```bash
bash setup.sh --install    # tạo junction còn thiếu (bỏ qua cái đã có)
bash setup.sh --verify     # báo "All 4 plugin skill dirs verified"
```

⚠️ `bash setup.sh --unlink` gỡ **cả bốn** junction này cùng với các skill khác. Sau `--unlink`, chạy
lại `--install` để dựng lại; đừng dựng tay từng cái rồi quên mất `fluency-4d-shared`.

Gọi bằng `/fluency-4d-preflight`, `/fluency-4d-review`, `/fluency-4d-weekly` (hoặc các cụm trigger
tiếng Việt/Anh khai trong `description` của từng `SKILL.md`).

## Đổi profile (dùng cho tổ chức khác)

`profile-workshop-x.md` chứa toàn bộ tín hiệu/cờ đỏ riêng Workshop X — `rubric-core.md` KHÔNG bao giờ
sửa theo tổ chức. Để phát cho tổ chức khác:

1. Chép `skills/fluency-4d-shared/references/profile-workshop-x.md` → `profile-<tên tổ chức>.md`.
2. Giữ nguyên khung mỗi khối: `## <mã ô>` + đúng ba trường `**Tín hiệu:**` / `**Cờ đỏ:**` / `**Ví dụ ngành:**`
   cho đủ 12 mã ô, đúng thứ tự canonical.
3. Đổi dòng trỏ tới file profile trong **đúng hai** `SKILL.md` — `fluency-4d-preflight` và
   `fluency-4d-review` — từ `profile-workshop-x.md` sang `profile-<tên tổ chức>.md`.
   `fluency-4d-weekly` **không** trỏ tới profile và không cần sửa: nó chỉ đọc sổ điểm, không chấm ô nào.

### Giới hạn của việc đổi profile — đọc trước khi hứa với ai

Đổi profile chỉ thay được **tầng tín hiệu chấm điểm** (tín hiệu / cờ đỏ / ví dụ ngành cho 12 ô).
Những thứ sau vẫn **hardcode trong `SKILL.md`** và phải sửa tay cho từng tổ chức:

| Thứ còn dính Workshop X | Nằm ở đâu |
|---|---|
| Đường dẫn sổ điểm `D:\Workshop_X\2_Areas\CEO-Self\AI-Fluency-Ledger\` | cả ba `SKILL.md` (và README này) |
| Chữ **"CEO"** làm tên vai người dùng | cả ba `SKILL.md` |
| Chữ **"MẬT"** trong ví dụ cờ đỏ Diligence | `fluency-4d-review/SKILL.md` |
| Danh sách khung quy trình **"3-Gate, VDI 2225, ODI, Pahl-Beitz"** | `fluency-4d-preflight/SKILL.md` |

Nghĩa là **D4 ("đổi profile là phát cho tổ chức khác dùng được") mới đúng một nửa**: rubric lõi thật
sự trung lập ngành và không phải đụng, nhưng ba skill thì chưa. Nâng bốn mục trên lên thành trường
của profile là một đợt tái cấu trúc riêng, **cố ý chưa làm trong đợt này**.

## Bảo trì

Sau mỗi lần sửa bất kỳ file nào trong `skills/fluency-4d-shared/references/`, chạy:

```bash
python -m pytest scripts/test_fluency_4d.py -v
```

Bộ test (nằm ngoài plugin, ở `scripts/`, vì plugin phải thuần Markdown/JSON) khớp-chéo bốn file tham
chiếu với nhau qua `scripts/fluency_4d_lint.py` — rubric trung lập ngành, profile phủ đủ 12 ô, schema
sổ điểm hợp lệ, vòng đời thí nghiệm (streak/đứt/WIP=1) đúng luật. `lint_skills()` soi thêm chính ba
`SKILL.md`: mọi `../fluency-4d-shared/references/<file>.md` được trích dẫn phải tồn tại thật, và đường dẫn sổ
điểm phải giống hệt nhau ở mọi file `.md` của plugin (kể cả README này) — đây là chốt bắt được lỗi
"trỏ tới file tham chiếu không có thật". Ba eval tĩnh
(`evals/fluency-4d-review.json`, `evals/fluency-4d-preflight.json`, `evals/fluency-4d-weekly.json`)
chạy qua `bash evals/run-eval.sh <skill-name>` để audit nội dung `SKILL.md`.

## Bản quyền khung gốc

Khung **AI Fluency Framework** là công trình gốc của **Rick Dakan, Joseph Feller, và Anthropic**,
cấp phép **CC BY-NC-SA 4.0**. `rubric-core.md` trong plugin này là bản chuyển khung gốc sang dạng
chấm-được (12 ô, thang điểm, ba chốt chống nịnh) — không phải bản sao nguyên văn nhưng bám sát cấu
trúc gốc; mọi phần diễn giải riêng của Workshop X nằm tách biệt ở `profile-workshop-x.md`.
