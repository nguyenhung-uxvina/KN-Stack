# learn-lecture — Mốc + Video build (bước 3.8 MARKS · 3.9 VIDEO)

Dò mốc "Phần N" một lần rồi dựng MP4 đồng bộ từ slide PDF + audio đã tải về vault.
Script codified: `D:\KN-Stack\scripts\lecture_video.py`. Proven live 2026-07-22
(Bài 1 AI Fluency, 12 slide, 12/12 mốc tìm thấy, 0 nội suy).

## 2 lệnh chuẩn

```bash
# 3.8 — ngay sau khi audio tải xong (chạy nối tiếp trong script nền download)
python D:/KN-Stack/scripts/lecture_video.py \
  --audio  "<vault>/Bai-NN-<slug>/Bai-NN-audio.mp3" \
  --slides 12 --detect-only
# → <vault>/Bai-NN-<slug>/Bai-NN-audio.marks.json      (mốc giây của "Phần 1..N")
# → <vault>/Bai-NN-<slug>/Bai-NN-audio.transcript.txt  (bản ghi [mm:ss] — miễn phí)
# in ra: markers found k/N + WARNING missing [...]  → chép vào Sync Report

# 3.9 — dựng video, KHÔNG transcribe lại (đọc marks.json bên cạnh audio)
python D:/KN-Stack/scripts/lecture_video.py \
  --pdf   "<vault>/Bai-NN-<slug>/Bai-NN-slides.pdf" \
  --audio "<vault>/Bai-NN-<slug>/Bai-NN-audio.mp3" \
  --out   "<vault>/Bai-NN-<slug>/Bai-NN-video.mp4"
# flags phụ: --marks <path.json> · --redetect · --timings · --scratch · --lang · --model · --syncmap
```

`--slides N` lấy từ `slide-script.md` — 3.8 không cần mở PDF. Nếu thiếu `--slides`
thì truyền `--pdf` để script tự đếm trang.

**Chạy ở đâu:** 3.8 `run_in_background` (transcribe ~15 phút audio ≈ 3–5 phút CPU;
lần đầu tải model whisper `small` ~460MB từ HuggingFace). 3.9 khi ĐÃ có marks file
chỉ còn ffmpeg → foreground, vài giây đến vài chục giây.

## Thứ tự ưu tiên nguồn mốc (trong script)

1. `--timings "0,1:01,2:35,…"` — CEO chỉ định tay, thắng tất cả (nhận giây hoặc `mm:ss`).
   ⚠ **Giá trị đầu tiên PHẢI là 0.** Ảnh phát từ t=0, nên mốc của slide 1 không phải
   "chỗ audio bắt đầu nói nội dung slide 1" mà là 0 — phần mở đầu thuộc slide 1. Ghi
   mốc nội dung (vd `1:28`) vào ô đầu = đẩy TOÀN BỘ slide sớm 88 giây (bug 2026-07-28,
   5 video khoá cowork lệch 74–111s). Script nay tự ép về 0 kèm WARNING và từ chối
   build nếu tổng thời lượng slide lệch audio > 1s, nhưng đừng dựa vào đó: viết đúng
   từ đầu, rồi đọc syncmap xác nhận `| 1 | 0.0 | 0:00 |`.
2. `<audio>.marks.json` — mặc định; bỏ qua hẳn whisper. Ghi đè đường dẫn bằng `--marks`.
3. Dò mới bằng whisper — chỉ khi file mốc thiếu / hỏng / lệch `audio_bytes`, hoặc
   ép bằng `--redetect`. Dò xong GHI LẠI file mốc.

Syncmap có dòng `Nguồn mốc:` ghi rõ lần dựng này lấy mốc từ đâu.

## marks.json

```json
{ "version": 1, "audio": "Bai-01-audio.mp3", "audio_bytes": 17342114,
  "audio_duration": 913.4, "lang": "vi", "model": "small", "n_slides": 12,
  "found": [1,2,3], "missing": [4], "marks": { "1": 0.0, "2": 61.3, "3": 154.9 } }
```

- Nằm cạnh AUDIO (không phải cạnh video) vì nó mô tả audio — 1 audio, nhiều lần dựng video.
- `audio_bytes` là chốt chống lệch: audio sinh lại → tự dò lại, không im lặng dùng mốc cũ.
- **Sửa tay được:** thêm/sửa khóa trong `marks`, giá trị là số giây (`154.9`) hoặc
  `"2:35"`. Đây là cách vá lệch đồng bộ rẻ nhất — không phải liệt kê lại cả N mốc như
  `--timings`.
- **`<audio>.transcript.txt` sinh kèm** (dòng `[mm:ss] câu`): whisper đã chạy nên không
  tốn thêm gì. Dùng nó cho hai việc:
  1. **Sót 1–2 mốc** (ca thường gặp nhất): gần như luôn là whisper nghe nhầm SỐ ĐẾM
     tiếng Việt — đã gặp "phần chín"→"phần triển", "phần sáu"→"phần solve",
     "Phần bảy"→"Phần B", "Phần năm"→"Phật nằm". Dump transcript trong KHOẢNG TRỐNG giữa
     hai mốc kề là thấy ngay, kèm đúng tiêu đề slide → điền `marks`, KHÔNG sinh lại audio.
  2. **Audio không xướng "Phần N" chút nào**: tìm câu mở đầu từng chủ đề rồi điền `marks` —
     thay hẳn script dump transcript ad-hoc và lần transcribe thứ hai.
  Lưu ý: podcast 2 giọng VẪN thường xướng đủ "Phần N" (live-run 2026-07-31) — đừng mặc
  định là không, và đừng loại bản audio chỉ vì nó hai giọng.

## Cơ chế

1. **Dò mốc** (3.8): faster-whisper (`small`, CPU int8, `language=vi`, word_timestamps,
   vad_filter) → quét chuỗi từ tìm `Phần N` — bắt cả số (`4`, `4.`) lẫn chữ (`hai`,
   `mười hai`); chuẩn hóa bỏ dấu + bỏ dấu câu dính (`'ba,'`→`ba`); chỉ nhận N tăng đơn
   điệu (chống nhận nhầm "phần" giữa câu). Slide 1 luôn được ghim 0.0.
2. **Tách slide** (3.9): PyMuPDF render mỗi trang PDF → PNG 1920px (giữ tỷ lệ, 1920×1072
   với deck NLM 16:9 — số chẵn, h264 hợp lệ). Số trang render ≠ số slide đã tính → dừng lỗi.
3. **Timing**: slide 1 từ 0:00 (phủ intro trước khi giọng đọc vào "Phần 1"); slide N từ
   mốc "Phần N". Mốc sót → nội suy tuyến tính giữa 2 mốc kề (WARNING).
4. **Ghép**: ffmpeg concat demuxer (ảnh + duration) + audio → h264 `-tune stillimage`
   `-pix_fmt yuv420p -r 10` + AAC 160k, `-t <độ dài audio thật>`.
5. **Syncmap**: sinh `<out>-syncmap.md` — bảng Slide · Start(s) · mm:ss · nguồn mốc
   (audio "Phần N" / nội suy / mốc nội dung) để CEO spot-check.

## Dependencies

pip (Python312 — đã cài 2026-07-22): `pymupdf` · `faster-whisper` · `imageio-ffmpeg`.
ffmpeg KHÔNG cần cài hệ thống — dùng `imageio_ffmpeg.get_ffmpeg_exe()`.

## Gotchas đã trả giá

| Gotcha | Xử lý (đã nằm trong script) |
|---|---|
| ffmpeg không có trên PATH | binary bundle imageio-ffmpeg |
| whisper `info.duration` ngắn hơn mp3 thật (VAD) | parse `Duration:` từ `ffmpeg -i` stderr; fallback whisper |
| concat demuxer thừa ~40s slide cuối câm | cắt `-t <audio duration>` ngay lúc encode |
| concat demuxer nhân đôi tiền tố scratch khi `--out` tương đối | ghi đường dẫn tuyệt đối vào concat.txt |
| console Windows cp1252 crash chữ Việt | tự wrap stdout UTF-8 |
| từ whisper dính dấu câu (`'ba,'`, `'hai:'`) | norm() bỏ dấu câu trước khi so |
| "phần" xuất hiện giữa câu thường | chỉ nhận N tăng đơn điệu từ mốc trước |
| dựng lại video = transcribe lại (3–5 phút mỗi lần) | marks.json cạnh audio, dò 1 lần ở 3.8 |
| marks.json của audio CŨ sau khi sinh lại audio | so `audio_bytes`, lệch → tự dò lại + WARNING |

## Định nghĩa hoàn thành (per bài)

Thư mục `Bai-NN-<slug>/` đủ 7 file (+ `audio.transcript.txt` phụ trợ): `slides.pdf` ·
`audio.mp3` · `audio.marks.json` ·
`video.mp4` · `video-syncmap.md` · `slide-script.md` · `outline.md` (kèm Sync Report ghi
số mốc tìm thấy/nội suy). Video fail → ⚠ trong Sync Report, không chặn bài (marks đã có,
dựng lại không tốn whisper).
