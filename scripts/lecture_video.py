"""lecture_video.py — build a synchronized lecture video from slide PDF + narration audio.

Part of the learn-lecture skill (KN-Stack). Slides auto-advance at the exact moments
the Vietnamese narration announces "Phần N" (detected via faster-whisper word timestamps).

Proven live 2026-07-22 (Bai-01 AI Fluency, 12 slides, 12/12 markers found, zero interpolation).

Usage:
    python lecture_video.py --pdf <slides.pdf> --audio <audio.mp3> --out <video.mp4>
                            [--scratch <dir>] [--lang vi] [--model small] [--syncmap <path.md>]

Dependencies (pip): pymupdf, faster-whisper, imageio-ffmpeg
"""
import argparse
import json
import os
import re
import subprocess
import sys
import unicodedata

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
    words = []
    for seg in segments:
        for w in (seg.words or []):
            words.append({'start': w.start, 'word': w.word})
    return words, info.duration


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


def build(args):
    import imageio_ffmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    scratch = args.scratch or os.path.join(os.path.dirname(args.out) or '.', '_video_build')
    os.makedirs(scratch, exist_ok=True)

    slides = extract_slides(args.pdf, os.path.join(scratch, 'slides'))
    n_slides = len(slides)
    print(f'slides: {n_slides}')

    words, wh_duration = transcribe(args.audio, args.lang, args.model)
    # real mp3 duration beats whisper's (VAD can under-report); fall back to whisper's
    duration = audio_duration(ffmpeg, args.audio) or wh_duration
    print(f'audio duration: {duration:.1f}s, words: {len(words)}')

    markers = find_markers(words, n_slides)
    print('markers:', {k: round(v, 1) for k, v in sorted(markers.items())})
    starts, durs, interpolated = slide_timings(markers, n_slides, duration)
    if interpolated:
        print(f'WARNING interpolated slides: {interpolated}')

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
        sys.exit(1)
    print(f'OK -> {args.out} ({os.path.getsize(args.out)} bytes)')

    syncmap = args.syncmap or os.path.splitext(args.out)[0] + '-syncmap.md'
    with open(syncmap, 'w', encoding='utf-8') as f:
        f.write(f'# Sync map — {os.path.basename(args.out)}\n\n'
                '| Slide | Start (s) | Start (mm:ss) | Nguồn mốc |\n|---|---|---|---|\n')
        for i, s in enumerate(starts):
            src = ('đầu audio' if i == 0
                   else 'nội suy' if (i + 1) in interpolated
                   else f'audio "Phần {i + 1}"')
            f.write(f'| {i + 1} | {s:.1f} | {int(s // 60)}:{int(s % 60):02d} | {src} |\n')
    print(f'syncmap -> {syncmap}')
    return 0


def main():
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ('utf-8', 'utf8'):
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--pdf', required=True, help='slide deck PDF (from NLM)')
    ap.add_argument('--audio', required=True, help='narration audio (mp3/m4a)')
    ap.add_argument('--out', required=True, help='output mp4 path')
    ap.add_argument('--scratch', default=None, help='work dir (default: <out-dir>/_video_build)')
    ap.add_argument('--lang', default='vi', help='audio language (default vi)')
    ap.add_argument('--model', default='small', help='faster-whisper model (default small)')
    ap.add_argument('--syncmap', default=None, help='sync map md path (default <out>-syncmap.md)')
    sys.exit(build(ap.parse_args()))


if __name__ == '__main__':
    main()
