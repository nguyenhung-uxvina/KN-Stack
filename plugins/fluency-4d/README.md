# fluency-4d

Plugin Claude tự chứa (Markdown/JSON thuần, không Python/hook/MCP) huấn luyện **AI Fluency** theo khung 4D —
Delegation · Description · Discernment · Diligence — ngay trên các phiên làm việc thật, không phải bài tập giả lập.

## Plugin làm gì

Ba skill chấm/huấn luyện một khung 12 ô năng lực chung (`del.problem`, `del.platform`, `del.task`,
`des.product`, `des.process`, `des.performance`, `dis.product`, `dis.process`, `dis.performance`,
`dil.creation`, `dil.transparency`, `dil.deployment`), cộng tám file tham chiếu dùng chung ở
`skills/fluency-4d-shared/references/`:

- `active-profile.md` — **tầng trỏ**: nêu tên profile đang bật. Ba `SKILL.md` đọc file này rồi mới mở profile; không skill nào còn gọi tên profile trực tiếp.
- `rubric-core.md` — 12 ô, thang điểm 0–3/`null`, ba chốt chống nịnh. Trung lập ngành, không sửa khi đổi tổ chức.
- `profile-template.md` — khuôn rỗng 48 ô `⟨CEO chốt: …⟩` để viết profile cho vai mới. Không bao giờ được bật.
- `profile-quan-doc.md` — **nháp** cho vai quản đốc phân xưởng: tín hiệu/ví dụ/cách cải tiến đã soạn sẵn để gạch xoá, **toàn bộ 12 trường Cờ đỏ bỏ trống**.
- `improvement-playbook.md` — menu cách cải tiến cho từng ô (cách làm · dấu hiệu đã ăn · bẫy · phần CEO phải tự chốt). Trung lập ngành. `fluency-4d-weekly` **chọn dòng** từ đây, bị cấm tự nghĩ ra cách mới.
- `profile-workshop-x.md` — tín hiệu, cờ đỏ, ví dụ ngành, và cách cải tiến tại chỗ cho từng ô — lớp hiệu chỉnh riêng Workshop X.
- `ledger-schema.md` — schema một dòng sổ điểm (`sessions.jsonl`).
- `experiment-protocol.md` — luật thí nghiệm hành vi (WIP=1, dạng nếu–thì, streak/đứt), **cộng phần chỉ `fluency-4d-weekly` dùng**: Bảng 1 (DMIR đọc ô nào ghi ra cái gì), Bảng 2 (bản đồ ô kéo ô, 18 cạnh), Bảng 3 (tầng đòn bẩy Meadows theo ô + luật leo tầng), và Luật bước R. Ba bảng là **hằng số** — weekly chọn dòng, chỉ CEO sửa.

### Ba lối vào — khi nào dùng cái nào

| Skill | Dùng khi nào | Ghi gì |
|---|---|---|
| **`fluency-4d-preflight`** | TRƯỚC khi giao một việc lớn cho AI | Không ghi sổ điểm — đây là cổng chặn (Delegation + Description), không phải phép đo. Trả về phiếu giao việc đã viết lại. |
| **`fluency-4d-review`** | NGAY SAU một phiên làm việc vừa xong | Chấm 12 ô kèm bằng chứng trích dẫn, nghiệm thu/kê thí nghiệm hành vi, append 1 dòng vào `sessions.jsonl` + cập nhật `experiments.md`. |
| **`fluency-4d-weekly`** | Cuối tuần, tổng hợp xu hướng + một vòng DMIR | Đọc `sessions.jsonl` 7 ngày, phát hiện ô đang tụt bằng ngưỡng số, rồi chạy bốn bước: **D** chốt ô *ràng buộc* (ô thượng nguồn theo Bảng 2 — thường KHÔNG phải ô thấp nhất), **M** chép bản đồ ô-kéo-ô + tầng đòn bẩy, **I** kê ứng viên thí nghiệm nhắm ràng buộc (WIP=1 vẫn thắng; lệch ô thì in cờ), **R** nghiệm thu vòng trước bằng số và chất vấn cạnh đã đặt cược. Bảng gợi ý vẫn chép từ playbook, câu nếu–thì vẫn **để trống cho CEO tự viết**. Chốt 1 D ưu tiên, ghi `weekly/<năm>-W<tuần>.md`. |

**Vì sao ràng buộc khác ô thấp nhất.** Ô tụt sâu nhất thường là *triệu chứng* của một ô thượng
nguồn còn hỏng: không nêu tiêu chí thì không có thước để soi, nên `dis.*` tụt vì `des.*` chưa
làm xong việc của nó. Nhắm ô thấp nhất là chữa triệu chứng. Bản đồ quyết định ô nào thượng
nguồn là **Bảng 2 viết sẵn và CEO duyệt sẵn**, không phải thứ AI suy ra từ sổ lúc chạy — vài
chục điểm nguyên một tuần không đủ cho bất kỳ tương quan nào, và một bản đồ dựng lúc chạy sẽ
luôn dựng thành cái biện minh cho ô vừa chọn.

**DMIR ở đây đã bị cắt gọn có chủ ý.** Không có mô hình System Dynamics, không có menu 8 system
archetype, không có bước exploit/subordinate/elevate của TOC, không có thách thức paradigm
L1–L2, và chỉ dùng 4 trong 12 tầng đòn bẩy Meadows. Lý do và điều kiện khôi phục ghi ngay
trong `experiment-protocol.md` dưới Bảng 1.

**Vì sao weekly không tự viết câu thí nghiệm.** Coach tự kê bài tập cho chính hành vi mà nó vừa
chấm thì nó đang chấm bài của mình, và sẽ nghiêng về ô dễ ghi streak. Nên ranh giới đặt ở đây:
AI đưa **menu và số liệu**, CEO viết **cam kết**. Cùng lý do đó, mọi dòng trong bảng gợi ý phải
chép từ `improvement-playbook.md` — một menu viết trước và CEO duyệt trước — chứ không sinh tại
lúc chạy.

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

`profile-*.md` chứa toàn bộ tín hiệu/cờ đỏ riêng một vai — `rubric-core.md` và
`improvement-playbook.md` KHÔNG bao giờ sửa theo tổ chức. Để phát cho vai khác:

1. Chép `skills/fluency-4d-shared/references/profile-template.md` → `profile-<tên vai>.md`
   (hoặc chép `profile-workshop-x.md` nếu muốn có sẵn nội dung để sửa).
2. Giữ nguyên khung mỗi khối: `## <mã ô>` + đúng bốn trường `**Tín hiệu:**` / `**Cờ đỏ:**` /
   `**Ví dụ ngành:**` / `**Cách cải tiến tại chỗ:**` cho đủ 12 mã ô, đúng thứ tự canonical.
3. Đổi **đúng một dòng** — tên file trong khối mã của `active-profile.md`. Không đụng vào `SKILL.md` nào.
4. `improvement-playbook.md` là tầng lõi trung lập ngành — **không** chép theo tổ chức, không sửa.
   Muốn thêm cách cải tiến riêng thì viết vào trường `Cách cải tiến tại chỗ` của profile.

### Giới hạn của việc đổi profile — đọc trước khi hứa với ai

Đổi profile chỉ thay được **tầng tín hiệu chấm điểm** (bốn trường cho 12 ô).
Những thứ sau vẫn **hardcode trong `SKILL.md`** và phải sửa tay cho từng tổ chức
(đã đếm lại 2026-08-01, sau khi dựng tầng trỏ):

| Thứ còn dính Workshop X | Nằm ở đâu |
|---|---|
| Đường dẫn sổ điểm `D:\Workshop_X\2_Areas\CEO-Self\AI-Fluency-Ledger\` | cả ba `SKILL.md` (và README này) |
| Chữ **"CEO"** làm tên vai người dùng — 15 chỗ | preflight 7 · weekly 6 · review 2 |
| Chữ **"MẬT"** trong ví dụ cờ đỏ Diligence | `fluency-4d-review/SKILL.md` |
| Danh sách khung quy trình **"3-Gate, VDI 2225, ODI, Pahl-Beitz"** | `fluency-4d-preflight/SKILL.md` |

Tầng trỏ `active-profile.md` đã gỡ được **một** mục khỏi danh sách này: tên file profile.
Bốn mục còn lại vẫn nằm trong skill. Nghĩa là **D4 ("đổi profile là phát cho tổ chức khác
dùng được") vẫn chưa trọn**: đổi vai giờ là sửa một dòng thay vì sửa ba file, nhưng người
nhận vẫn đọc thấy chữ "CEO" và đường dẫn ổ D của Workshop X. Nâng bốn mục còn lại thành
trường của profile là một đợt riêng, **cố ý chưa làm trong đợt này**.

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
