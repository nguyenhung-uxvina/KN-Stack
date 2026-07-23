# learn-lecture — Video build (bước 3.9)

Dựng MP4 đồng bộ từ slide PDF + audio đã tải về vault. Script codified:
`D:\KN-Stack\scripts\lecture_video.py`. Proven live 2026-07-22 (Bài 1 AI Fluency,
12 slide, 12/12 mốc tìm thấy, 0 nội suy).

## Lệnh chuẩn

```bash
python D:/KN-Stack/scripts/lecture_video.py \
  --pdf   "<vault>/Bai-NN-<slug>/Bai-NN-slides.pdf" \
  --audio "<vault>/Bai-NN-<slug>/Bai-NN-audio.mp3" \
  --out   "<vault>/Bai-NN-<slug>/Bai-NN-video.mp4"
# flags phụ: --scratch <dir> · --lang vi · --model small · --syncmap <path.md>
```

Chạy `run_in_background` (transcribe ~15 phút audio ≈ 3–5 phút CPU; lần đầu tải
model whisper `small` ~460MB từ HuggingFace).

## Cơ chế

1. **Tách slide**: PyMuPDF render mỗi trang PDF → PNG 1920px (giữ tỷ lệ, 1920×1072
   với deck NLM 16:9 — số chẵn, h264 hợp lệ).
2. **Dò mốc**: faster-whisper (`small`, CPU int8, `language=vi`, word_timestamps,
   vad_filter) → quét chuỗi từ tìm `Phần N` — bắt cả số (`4`, `4.`) lẫn chữ
   (`hai`, `mười hai`); chuẩn hóa bỏ dấu + bỏ dấu câu dính (`'ba,'`→`ba`); chỉ nhận
   N tăng đơn điệu (chống nhận nhầm "phần" giữa câu).
3. **Timing**: slide 1 từ 0:00 (phủ intro trước khi giọng đọc vào "Phần 1");
   slide N từ mốc "Phần N". Mốc sót → nội suy tuyến tính giữa 2 mốc kề (WARNING).
4. **Ghép**: ffmpeg concat demuxer (ảnh + duration) + audio → h264 `-tune stillimage`
   `-pix_fmt yuv420p -r 10` + AAC 160k, `-t <độ dài audio thật>`.
5. **Syncmap**: sinh `<out>-syncmap.md` — bảng Slide · Start(s) · mm:ss · nguồn mốc
   (audio "Phần N" / nội suy) để CEO spot-check.

## Dependencies

pip (Python312 — đã cài 2026-07-22): `pymupdf` · `faster-whisper` · `imageio-ffmpeg`.
ffmpeg KHÔNG cần cài hệ thống — dùng `imageio_ffmpeg.get_ffmpeg_exe()`.

## Gotchas đã trả giá

| Gotcha | Xử lý (đã nằm trong script) |
|---|---|
| ffmpeg không có trên PATH | binary bundle imageio-ffmpeg |
| whisper `info.duration` ngắn hơn mp3 thật (VAD) | parse `Duration:` từ `ffmpeg -i` stderr; fallback whisper |
| concat demuxer thừa ~40s slide cuối câm | cắt `-t <audio duration>` ngay lúc encode |
| console Windows cp1252 crash chữ Việt | tự wrap stdout UTF-8 |
| từ whisper dính dấu câu (`'ba,'`, `'hai:'`) | norm() bỏ dấu câu trước khi so |
| "phần" xuất hiện giữa câu thường | chỉ nhận N tăng đơn điệu từ mốc trước |

## Định nghĩa hoàn thành (per bài)

Thư mục `Bai-NN-<slug>/` đủ 5 file: `slides.pdf` · `audio.mp3` · `video.mp4` ·
`outline.md` (kèm Sync Report ghi số mốc tìm thấy/nội suy) · `video-syncmap.md`.
Video fail → ⚠ trong Sync Report, không chặn bài.
