# Codify Ledger — append-only registry of markdown→Python codifications

| Date | Target Skill | Script | LOC | Tests | Annual LLM saving (est.) | CEO sign-off |
|------|-------------|--------|-----|-------|--------------------------|--------------|
| 2026-07-23 | learn-lecture (bước 3.9 VIDEO) | `lecture_video.py` | ~170 | logic tests pass (marker detect + interpolation + số/chữ VN + punctuation) | thay ~1 phiên ad-hoc scripting/bài × mỗi bài giảng | pending |
| 2026-07-26 | learn-lecture (3.8 MARKS + 3.9 VIDEO) | `lecture_video.py` v1.1 — `--detect-only`/`--marks`/`--redetect`, mốc "Phần N" ghi `<audio>.marks.json` + `<audio>.transcript.txt` | ~320 | e2e pass 2 fixture: (a) speech VN thật (edge-tts 12s, 3 slide) → detect 3/3 mốc + transcript đúng → build reuse marks, whisper skipped; (b) sine 20s/4 slide → found/missing + gợi ý đọc transcript · marks lệch `audio_bytes` → tự dò lại + WARNING · `mm:ss` hand-edit · `--timings` vẫn override · 2 error path | bỏ 3–5 phút whisper CPU MỖI lần dựng lại video (nay 1 lần/bài) + bỏ hẳn lần transcribe thứ 2 khi audio podcast không xướng "Phần N" | pending |

