"""lecture_video.py — build a synchronized lecture video from slide PDF + narration audio.

Part of the learn-lecture skill (KN-Stack). Slides auto-advance at the exact moments
the Vietnamese narration announces "Phần N" (detected via faster-whisper word timestamps).

Marker detection is cached in a sidecar marks file next to the audio, so it runs ONCE
per lesson (right after the audio is downloaded, step 3.8) and every later video build
reuses it instead of re-transcribing.

Proven live 2026-07-22 (Bai-01 AI Fluency, 12 slides, 12/12 markers found, zero interpolation).

Usage:
    # step 3.8 — detect markers once, write <audio>.marks.json, no video
    python lecture_video.py --audio <audio.mp3> --slides 12 --detect-only

    # step 3.9 — build video, reusing the marks file (no whisper)
    python lecture_video.py --pdf <slides.pdf> --audio <audio.mp3> --out <video.mp4>
                            [--marks <path.json>] [--redetect] [--scratch <dir>]
                            [--lang vi] [--model small] [--syncmap <path.md>]

Dependencies (pip): pymupdf, faster-whisper, imageio-ffmpeg
"""
import argparse
import json
import os
import re
import subprocess
import sys
import unicodedata

MARKS_VERSION = 1

# Vietnamese number words for "Phần N" detection (whisper may emit digits or words)
NUMWORDS = {'mot': 1, 'hai': 2, 'ba': 3, 'bon': 4, 'tu': 4, 'nam': 5,
            'sau': 6, 'bay': 7, 'tam': 8, 'chin': 9, 'muoi': 10}


def norm(s: str) -> str:
    """Lowercase, strip Vietnamese diacritics and punctuation ('Phần' -> 'phan', 'ba,' -> 'ba')."""
    s = unicodedata.normalize('NFD', s.lower().strip())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]', '', s)


def parse_num(toks, n_max):
    """Parse a section number (digits or Vietnamese words) from tokens after 'phan'."""
    if not toks:
        return None
    m = re.match(r'^(\d{1,2})', toks[0])
    if m:
        n = int(m.group(1))
        return n if 1 <= n <= n_max else None
    if toks[0] == 'muoi' and len(toks) > 1 and toks[1] in ('mot', 'hai'):
        return 10 + NUMWORDS[toks[1]]
    if toks[0] in NUMWORDS:
        return NUMWORDS[toks[0]]
    return None


def to_seconds(v):
    """Accept 61.3, '61.3' or hand-edited 'mm:ss' / 'h:mm:ss'."""
    if isinstance(v, (int, float)):
        return float(v)
    parts = str(v).strip().split(':')
    total = 0.0
    for p in parts:
        total = total * 60 + float(p)
    return total


def mmss(s):
    return f'{int(s // 60)}:{int(s % 60):02d}'


def pdf_page_count(pdf_path):
    import fitz
    doc = fitz.open(pdf_path)
    n = doc.page_count
    doc.close()
    return n


def extract_slides(pdf_path, out_dir, width=1920):
    import fitz
    os.makedirs(out_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    paths = []
    for i, page in enumerate(doc):
        zoom = width / page.rect.width
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        p = os.path.join(out_dir, f'slide{i + 1:02d}.png')
        pix.save(p)
        paths.append(p)
    doc.close()
    return paths


def transcribe(audio_path, lang, model_name):
    from faster_whisper import WhisperModel
    model = WhisperModel(model_name, device='cpu', compute_type='int8')
    segments, info = model.transcribe(audio_path, language=lang,
                                      word_timestamps=True, vad_filter=True)
    words, lines = [], []
    for seg in segments:
        lines.append((seg.start, (seg.text or '').strip()))
        for w in (seg.words or []):
            words.append({'start': w.start, 'word': w.word})
    return words, lines, info.duration


def find_markers(words, n_slides):
    """First occurrence of each 'Phần N', N walking monotonically upward."""
    markers = {}
    expect = 1
    for i, w in enumerate(words):
        if norm(w['word']) == 'phan':
            following = [norm(x['word']) for x in words[i + 1:i + 3]]
            n = parse_num(following, n_slides)
            if n is not None and n in (expect, expect + 1) and n not in markers:
                markers[n] = w['start']
                expect = n + 1
    return markers


def default_marks_path(audio_path):
    """Sidecar lives next to the AUDIO — it describes the audio, not any one video."""
    return os.path.splitext(audio_path)[0] + '.marks.json'


def write_marks(path, audio_path, markers, n_slides, duration, lang, model):
    missing = [n for n in range(1, n_slides + 1) if n not in markers]
    data = {
        'version': MARKS_VERSION,
        'audio': os.path.basename(audio_path),
        'audio_bytes': os.path.getsize(audio_path),
        'audio_duration': round(duration, 3) if duration else None,
        'lang': lang,
        'model': model,
        'n_slides': n_slides,
        'found': sorted(markers),
        'missing': missing,
        'note': 'Mốc "Phần N" (giây) dò 1 lần từ audio. Sửa tay được: điền số giây hoặc "mm:ss". '
                'Slide thiếu mốc sẽ bị nội suy khi dựng video.',
        'marks': {str(n): round(markers[n], 3) for n in sorted(markers)},
    }
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return data


def load_marks(path, audio_path):
    """Return {slide:int -> start:float} or None if absent/stale/unusable."""
    if not os.path.exists(path):
        return None
    try:
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
    except (ValueError, OSError) as e:
        print(f'WARNING marks file unreadable ({e}) -> re-detecting')
        return None
    actual = os.path.getsize(audio_path)
    if data.get('audio_bytes') not in (None, actual):
        print(f'WARNING marks file stale (audio_bytes {data.get("audio_bytes")} != {actual}) '
              f'-> re-detecting')
        return None
    try:
        markers = {int(k): to_seconds(v) for k, v in (data.get('marks') or {}).items()}
    except (TypeError, ValueError) as e:
        print(f'WARNING marks file has bad values ({e}) -> re-detecting')
        return None
    if not markers:
        print('WARNING marks file has no markers -> re-detecting')
        return None
    return markers


def slide_timings(markers, n_slides, duration):
    """Slide 1 starts at 0 (covers any intro); missing markers are interpolated."""
    starts = [0.0]
    for n in range(2, n_slides + 1):
        starts.append(markers.get(n))
    known = [i for i, s in enumerate(starts) if s is not None]
    interpolated = []
    for i, s in enumerate(starts):
        if s is None:
            interpolated.append(i + 1)
            prev_i = max(k for k in known if k < i)
            nxt = [k for k in known if k > i]
            if nxt:
                next_i = min(nxt)
                frac = (i - prev_i) / (next_i - prev_i)
                starts[i] = starts[prev_i] + frac * (starts[next_i] - starts[prev_i])
            else:
                remain = n_slides - prev_i
                starts[i] = starts[prev_i] + (i - prev_i) * (duration - starts[prev_i]) / remain
    durs = [max(0.5, (starts[i + 1] if i + 1 < n_slides else duration) - starts[i])
            for i in range(n_slides)]
    return starts, durs, interpolated


def audio_duration(ffmpeg, audio_path):
    """Parse real duration from ffmpeg -i stderr (ffprobe is not bundled)."""
    r = subprocess.run([ffmpeg, '-i', audio_path], capture_output=True, text=True, errors='replace')
    m = re.search(r'Duration:\s*(\d+):(\d+):(\d+\.\d+)', r.stderr)
    if not m:
        return None
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def detect(args, ffmpeg, n_slides, duration):
    """Transcribe once and persist the 'Phần N' markers (+ transcript) next to the audio."""
    marks_path = args.marks or default_marks_path(args.audio)
    words, lines, wh_duration = transcribe(args.audio, args.lang, args.model)
    duration = duration or wh_duration
    markers = find_markers(words, n_slides)
    markers.setdefault(1, 0.0)  # slide 1 always covers the intro
    data = write_marks(marks_path, args.audio, markers, n_slides, duration,
                       args.lang, args.model)

    # The transcript is free here (whisper already ran) and is what you read to place
    # marks by content when the narration never announces "Phần N" (podcast format).
    tr_path = os.path.splitext(args.audio)[0] + '.transcript.txt'
    with open(tr_path, 'w', encoding='utf-8') as f:
        for start, text in lines:
            f.write(f'[{mmss(start)}] {text}\n')

    print(f'words: {len(words)}, audio duration: {duration:.1f}s')
    print(f'markers found {len(data["found"])}/{n_slides}: '
          + ', '.join(f'{n}={mmss(markers[n])}' for n in data['found']))
    if data['missing']:
        print(f'WARNING missing markers (sẽ nội suy khi dựng video): {data["missing"]}')
        print(f'  -> đọc {os.path.basename(tr_path)} tìm câu mở đầu mỗi phần, '
              f'điền mốc vào "marks" trong {os.path.basename(marks_path)}')
    print(f'marks -> {marks_path}')
    print(f'transcript -> {tr_path}')
    return markers, duration, marks_path


def build(args):
    import imageio_ffmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    if args.detect_only:
        if not (args.pdf or args.slides):
            print('ERROR: --detect-only needs --slides N (or --pdf to read the count)')
            return 1
    elif not (args.pdf and args.out):
        print('ERROR: --pdf and --out are required when building a video')
        return 1

    n_slides = args.slides or pdf_page_count(args.pdf)
    duration = audio_duration(ffmpeg, args.audio)

    if args.detect_only:
        detect(args, ffmpeg, n_slides, duration)
        return 0

    marks_path = args.marks or default_marks_path(args.audio)
    print(f'slides: {n_slides}')

    if args.timings:
        # Explicit content-anchored start times (seconds), one per slide.
        # Fallback for NLM podcast-format audio that never says "Phần N".
        starts = [to_seconds(x) for x in args.timings.split(',')]
        if len(starts) != n_slides:
            print(f'ERROR: --timings has {len(starts)} values, need {n_slides}')
            return 1
        if duration is None:
            *_, duration = transcribe(args.audio, args.lang, args.model)
        durs = [max(0.5, (starts[i + 1] if i + 1 < n_slides else duration) - starts[i])
                for i in range(n_slides)]
        interpolated = []
        mark_source = '--timings (mốc nội dung do CEO chỉ định)'
        print('markers: explicit --timings', [round(s, 1) for s in starts])
    else:
        markers = None if args.redetect else load_marks(marks_path, args.audio)
        if markers is not None:
            mark_source = f'marks file `{os.path.basename(marks_path)}` (không transcribe lại)'
            print(f'markers: reused from {marks_path} '
                  f'({len(markers)} mốc, whisper skipped)')
        else:
            markers, duration, marks_path = detect(args, ffmpeg, n_slides, duration)
            mark_source = f'whisper (dò mới, đã ghi `{os.path.basename(marks_path)}`)'
        if duration is None:
            *_, duration = transcribe(args.audio, args.lang, args.model)
        starts, durs, interpolated = slide_timings(markers, n_slides, duration)
        if interpolated:
            print(f'WARNING interpolated slides: {interpolated}')

    print(f'audio duration: {duration:.1f}s')
    scratch = args.scratch or os.path.join(os.path.dirname(args.out) or '.', '_video_build')
    os.makedirs(scratch, exist_ok=True)
    slides = extract_slides(args.pdf, os.path.join(scratch, 'slides'))
    if len(slides) != n_slides:
        print(f'ERROR: rendered {len(slides)} slides but timed {n_slides}')
        return 1

    # Absolute paths: concat demuxer resolves relative 'file' entries against the
    # concat.txt dir, which doubles the scratch prefix when --out is relative.
    concat = os.path.join(scratch, 'concat.txt')
    abs_slides = [os.path.abspath(p).replace(chr(92), '/') for p in slides]
    with open(concat, 'w', encoding='utf-8') as f:
        for p, d in zip(abs_slides, durs):
            f.write(f"file '{p}'\n")
            f.write(f'duration {d:.3f}\n')
        f.write(f"file '{abs_slides[-1]}'\n")  # concat demuxer quirk

    cmd = [ffmpeg, '-y', '-f', 'concat', '-safe', '0', '-i', concat, '-i', args.audio,
           '-c:v', 'libx264', '-tune', 'stillimage', '-pix_fmt', 'yuv420p', '-r', '10',
           '-c:a', 'aac', '-b:a', '160k', '-t', f'{duration:.3f}', args.out]
    r = subprocess.run(cmd, capture_output=True, text=True, errors='replace')
    if r.returncode != 0:
        print('FFMPEG FAIL\n', r.stderr[-3000:])
        return 1
    print(f'OK -> {args.out} ({os.path.getsize(args.out)} bytes)')

    syncmap = args.syncmap or os.path.splitext(args.out)[0] + '-syncmap.md'
    with open(syncmap, 'w', encoding='utf-8') as f:
        f.write(f'# Sync map — {os.path.basename(args.out)}\n\n'
                f'Nguồn mốc: {mark_source}\n\n'
                '| Slide | Start (s) | Start (mm:ss) | Nguồn mốc |\n|---|---|---|---|\n')
        for i, s in enumerate(starts):
            src = ('đầu audio' if i == 0
                   else 'mốc nội dung' if args.timings
                   else 'nội suy' if (i + 1) in interpolated
                   else f'audio "Phần {i + 1}"')
            f.write(f'| {i + 1} | {s:.1f} | {mmss(s)} | {src} |\n')
    print(f'syncmap -> {syncmap}')
    return 0


def main():
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ('utf-8', 'utf8'):
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--pdf', help='slide deck PDF (from NLM) — required to build a video')
    ap.add_argument('--audio', required=True, help='narration audio (mp3/m4a)')
    ap.add_argument('--out', help='output mp4 path — required to build a video')
    ap.add_argument('--detect-only', action='store_true',
                    help='only detect "Phần N" markers and write the marks file, no video '
                         '(run this right after the audio is downloaded)')
    ap.add_argument('--slides', type=int, default=None,
                    help='slide count (from slide-script.md); avoids opening the PDF in --detect-only')
    ap.add_argument('--marks', default=None,
                    help='marks JSON path (default <audio>.marks.json); reused instead of '
                         're-transcribing when it matches the audio')
    ap.add_argument('--redetect', action='store_true',
                    help='ignore an existing marks file and transcribe again')
    ap.add_argument('--scratch', default=None, help='work dir (default: <out-dir>/_video_build)')
    ap.add_argument('--lang', default='vi', help='audio language (default vi)')
    ap.add_argument('--model', default='small', help='faster-whisper model (default small)')
    ap.add_argument('--syncmap', default=None, help='sync map md path (default <out>-syncmap.md)')
    ap.add_argument('--timings', default=None,
                    help='explicit slide start times (seconds or mm:ss), comma-separated, one per '
                         'slide; overrides marker detection — use when NLM podcast audio omits callouts')
    sys.exit(build(ap.parse_args()))


if __name__ == '__main__':
    main()
