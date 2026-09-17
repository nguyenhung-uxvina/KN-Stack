# Hợp đồng từng pha — /book-to-learn

Biến dùng dưới đây: `VAULT=D:\Workshop_X`, `SLUG=<slug>`, `LEARN=$VAULT/1_Projects/LEARN-<slug>`, `BOOK=$VAULT/3_Resources/Books/<slug>`, `KN=D:\KN-Stack`.
Cổng máy: `python "$KN/scripts/btl_gate_check.py" "$LEARN" <pha> [cờ]` — exit 0 mới được đánh dấu xong.

| Pha | Đầu vào | Đầu ra | Gọi | Lệnh cổng |
|---|---|---|---|---|
| L0 | file sách, `--target` | `LEARN/_Project_Brief.md` (khuôn `mission.md`), `LEARN/_pipeline_state.md` (khuôn `pipeline-state.md`, điền slug, started) | đọc `Status.md` dự án đích | `btl_gate_check.py "$LEARN" L0` |
| L1 | file sách | `~/.claude/skills/<slug>/`, `BOOK/Leverage_Map.md`, `BOOK/Learning_Kit.md` | `book-to-skill` (DEPTH=study), `/analyze` Phần 3 | `… L1` |
| L2 | `BOOK/_source/*` (mỗi chương một tệp, tên tệp = title nguồn) | notebook `btl-<slug>-goc`, `LEARN/_nlm/list.json`, `LEARN/_nlm/content/<id>.json` | `nlm notebook create`, `nlm source add --file`, `nlm source list -j`, `nlm source content -j` | `… L2 --nlm-list "$LEARN/_nlm/list.json" --nlm-content-dir "$LEARN/_nlm/content"` |
| L3 | câu hỏi 4 hướng | notebook `btl-<slug>-mo-rong`, `BOOK/Claims.md` | `/research` ×4 | `… L3` |
| L4 | `framework_ung_vien` | `LEARN/learn/` (bài học, RETRIEVAL.md), `LEARN/learn/feynman-<framework>.md` | `learn-methodology`, `learn-practice`, `learn-track`; CEO tự gõ `/learn-teach` | `… L4` |
| L5 | Claims, Leverage_Map, dữ liệu thật dự án đích | `LEARN/Experiment_Card.md` | `/archetype`, `/cld`, `/constraint`, `/leverage` | `… L5` |
| L6 | thẻ đã duyệt | `LEARN/Run_Log.md`, cảnh báo trong `LEARN/Status.md` | — | (không có cổng máy) |
| L7 | Run_Log, thẻ | `LEARN/AAR.md`, dòng `VAULT/2_Areas/CEO-Self/Learning-Meta/cycles.jsonl`, `calibration.md`, `transfer-map.md`, `skill-backlog.md` | `/reflect`, `/paradigm`, `galaxy-gate` | `… L7` |

## Tải JSON cho cổng L2

```bash
mkdir -p "$LEARN/_nlm/content"
nlm source list "$NOTEBOOK_GOC" -j > "$LEARN/_nlm/list.json"
python - "$LEARN" <<'PY'
import json, subprocess, sys, pathlib
learn = pathlib.Path(sys.argv[1])
for item in json.loads((learn / "_nlm" / "list.json").read_text(encoding="utf-8")):
    out = learn / "_nlm" / "content" / f"{item['id']}.json"
    out.write_text(subprocess.run(["nlm", "source", "content", item["id"], "-j"],
                                  capture_output=True, text=True, encoding="utf-8").stdout,
                   encoding="utf-8")
PY
```
