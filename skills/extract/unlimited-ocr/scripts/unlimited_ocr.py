"""
Unlimited-OCR runner — PDF / images -> per-page Markdown via baidu/Unlimited-OCR.

Backends:
  space   Hugging Face Space baidu/Unlimited-OCR (ZeroGPU). Works on a laptop with
          no NVIDIA GPU. SENDS EVERY PAGE TO HUGGING FACE — public/unclassified only.
  server  An SGLang server already running the model (OpenAI-compatible API), e.g.
          started by D:/GitHub/Unlimited-OCR/infer.py or `python -m sglang.launch_server`
          on a CUDA machine. Stays on your network.
  windows Windows.Media.Ocr (built into Windows 10/11) via scripts/winocr.ps1. NOT the
          Unlimited-OCR model: plain text lines, no tables/layout, but local, no quota,
          nothing leaves the machine. Use it to finish a run the Space quota stopped —
          finished pages are kept, so only the missing ones are OCR'd.

Output (in --out):
  pages/page_NNNN.md      one file per page, raw model output (resume skips non-empty ones)
  <stem>.md               all pages joined, <|det|> markers stripped, <!-- page N --> anchors
  _report.json            per-page timing, chars, U+FFFD count, text-layer similarity

Usage:
  python unlimited_ocr.py book.pdf --out D:/tmp/ocr_book --pages 1-20
  python unlimited_ocr.py book.pdf --out D:/tmp/ocr_book            # all pages, resumable
  python unlimited_ocr.py scans/ --out D:/tmp/ocr_scans             # directory of images
  python unlimited_ocr.py book.pdf --backend server --server http://10.0.0.5:10000
  python unlimited_ocr.py book.pdf --out D:/tmp/ocr_book --backend windows   # local, resumes
"""

import argparse
import base64
import difflib
import json
import os
import re
import sys
import time
from collections import Counter
from concurrent.futures import CancelledError, ThreadPoolExecutor, as_completed

SPACE_ID = "baidu/Unlimited-OCR"
PROMPT = "document parsing."
IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff")
QUOTA_PATTERNS = ("quota", "exceeded", "ZeroGPU", "rate limit", "429")

DET_RE = re.compile(r"<\|det\|>([^<\s]+)(?:\s*\[[^\]]*\])?\s*<\|/det\|>(.*)", re.DOTALL)


class QuotaExhausted(RuntimeError):
    pass


def parse_pages(spec: str, n: int) -> list[int]:
    """'1-5,9,12-' -> 1-based page numbers within [1, n]."""
    if not spec:
        return list(range(1, n + 1))
    out = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            a = int(a) if a else 1
            b = int(b) if b else n
            out.update(range(a, b + 1))
        elif part:
            out.add(int(part))
    return sorted(p for p in out if 1 <= p <= n)


def remove_det(raw: str) -> str:
    """Strip <|det|>type [bbox]<|/det|> markers (upstream README post-processing)."""
    if "<|det|>" not in raw:
        return raw.strip()
    blocks, cur = [], None
    for line in raw.splitlines():
        line = line.rstrip()
        if not line:
            continue
        m = DET_RE.match(line)
        if m:
            category, content = m.group(1).strip(), m.group(2).strip()
            if category == "image":
                continue
            if cur is not None:
                blocks.append(cur)
            cur = [content] if content else []
            continue
        if cur is None:
            cur = []
        cur.append(line)
    if cur is not None:
        blocks.append(cur)
    return "\n\n".join("\n".join(b) for b in blocks).strip()


def words(s: str) -> list[str]:
    return re.findall(r"\w+", s.lower())


def similarity(ocr: str, layer: str) -> tuple[float | None, float | None]:
    """(order-sensitive ratio, order-free recall of text-layer words in OCR).

    Low ratio with high recall = reading order differs (often the TEXT LAYER is the one
    scrambled, e.g. two-column TOC). Low recall = OCR dropped or misread content.
    """
    wa, wb = words(ocr), words(layer)
    if len(wb) < 20:  # text layer too thin to be a meaningful reference
        return None, None
    ratio = difflib.SequenceMatcher(None, wa, wb, autojunk=False).ratio()
    pool = Counter(wa)
    hit = sum(min(c, pool[w]) for w, c in Counter(wb).items())
    return round(ratio, 3), round(hit / len(wb), 3)


def collect_jobs(src: str, pages_spec: str, dpi: int, img_dir: str):
    """Return list of (page_no, image_path, text_layer_or_None)."""
    if os.path.isdir(src):
        files = sorted(f for f in os.listdir(src) if f.lower().endswith(IMAGE_EXTS))
        sel = parse_pages(pages_spec, len(files))
        return [(i, os.path.join(src, files[i - 1]), None) for i in sel]
    if src.lower().endswith(IMAGE_EXTS):
        return [(1, src, None)]

    import fitz  # PyMuPDF

    doc = fitz.open(src)
    sel = parse_pages(pages_spec, doc.page_count)
    os.makedirs(img_dir, exist_ok=True)
    jobs = []
    for p in sel:
        page = doc[p - 1]
        path = os.path.join(img_dir, f"page_{p:04d}.png")
        if not os.path.exists(path):
            page.get_pixmap(dpi=dpi).save(path)
        jobs.append((p, path, page.get_text()))
    doc.close()
    return jobs


class SpaceBackend:
    def __init__(self, mode: str):
        from gradio_client import Client

        token = os.environ.get("HF_TOKEN") or None
        self.client = Client(SPACE_ID, token=token, verbose=False)
        self.mode = mode

    def ocr(self, image_path: str) -> str:
        from gradio_client import handle_file

        try:
            r = self.client.predict(handle_file(image_path), self.mode, PROMPT, api_name="/run_ocr")
        except Exception as e:  # gradio raises AppError with the Space's message
            msg = str(e)
            if any(k.lower() in msg.lower() for k in QUOTA_PATTERNS):
                raise QuotaExhausted(msg) from e
            raise
        if isinstance(r, dict):
            return r.get("text", "")
        return str(r)


class ServerBackend:
    def __init__(self, url: str, mode: str):
        import requests

        self.session = requests.Session()
        self.session.trust_env = False
        self.url = url.rstrip("/")
        self.mode = mode
        self.processor = None
        try:
            from sglang.srt.sampling.custom_logit_processor import (
                DeepseekOCRNoRepeatNGramLogitProcessor,
            )
            self.processor = DeepseekOCRNoRepeatNGramLogitProcessor.to_str()
        except ImportError:
            print("  ! sglang not importable here — sending without no-repeat-ngram processor "
                  "(higher risk of repetition loops)", file=sys.stderr)

    def ocr(self, image_path: str) -> str:
        ext = os.path.splitext(image_path)[1].lower()
        mime = "image/jpeg" if ext in (".jpg", ".jpeg") else f"image/{ext.lstrip('.')}"
        with open(image_path, "rb") as f:
            data = base64.b64encode(f.read()).decode("ascii")
        payload = {
            "model": "Unlimited-OCR",
            "messages": [{"role": "user", "content": [
                {"type": "text", "text": PROMPT},
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{data}"}},
            ]}],
            "temperature": 0,
            "skip_special_tokens": False,
            "images_config": {"image_mode": self.mode},
            "stream": False,
        }
        if self.processor:
            payload["custom_logit_processor"] = self.processor
            payload["custom_params"] = {"ngram_size": 35, "window_size": 128}
        r = self.session.post(f"{self.url}/v1/chat/completions", json=payload, timeout=1200)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]


class WindowsBackend:
    """Windows.Media.Ocr through PowerShell 5.1 — one short-lived process per page."""

    def __init__(self, lang: str):
        import shutil

        if sys.platform != "win32":
            sys.exit("--backend windows needs Windows (Windows.Media.Ocr)")
        self.ps = shutil.which("powershell") or shutil.which("powershell.exe")
        if not self.ps:
            sys.exit("--backend windows: powershell.exe not found on PATH")
        self.script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "winocr.ps1")
        self.lang = lang

    def ocr(self, image_path: str) -> str:
        import subprocess
        import tempfile

        fd, tmp = tempfile.mkstemp(suffix=".txt")
        os.close(fd)
        try:
            cmd = [self.ps, "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
                   "-File", self.script, "-Image", os.path.abspath(image_path), "-Out", tmp]
            if self.lang:
                cmd += ["-Lang", self.lang]
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if r.returncode != 0:
                raise RuntimeError(f"winocr.ps1 exit {r.returncode}: {(r.stderr or r.stdout).strip()[:300]}")
            with open(tmp, encoding="utf-8") as f:
                return f.read()
        finally:
            os.remove(tmp)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", help="PDF file, image file, or directory of images")
    ap.add_argument("--out", required=True, help="output directory")
    ap.add_argument("--pages", default="", help="e.g. 1-20,35,90- (1-based; default all)")
    ap.add_argument("--backend", choices=("space", "server", "windows"), default="space")
    ap.add_argument("--server", default="http://127.0.0.1:10000", help="SGLang URL for --backend server")
    ap.add_argument("--lang", default="", help="--backend windows: OCR language tag, e.g. en-US "
                                               "(default: user-profile languages)")
    ap.add_argument("--mode", choices=("gundam", "base"), default="gundam")
    ap.add_argument("--dpi", type=int, default=200, help="PDF render DPI (upstream uses 300)")
    ap.add_argument("--concurrency", type=int, default=1)
    ap.add_argument("--retries", type=int, default=3)
    ap.add_argument("--force", action="store_true", help="re-OCR pages that already have output")
    args = ap.parse_args()

    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")

    out = os.path.abspath(args.out)
    pages_dir = os.path.join(out, "pages")
    os.makedirs(pages_dir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(os.path.normpath(args.src)))[0]

    jobs = collect_jobs(args.src, args.pages, args.dpi, os.path.join(out, "_img"))
    print(f"{len(jobs)} page(s) selected, backend={args.backend}, mode={args.mode}, dpi={args.dpi}")

    if args.backend == "space":
        backend = SpaceBackend(args.mode)
    elif args.backend == "server":
        backend = ServerBackend(args.server, args.mode)
    else:
        backend = WindowsBackend(args.lang)

    report_path = os.path.join(out, "_report.json")
    report = {}
    if os.path.exists(report_path):
        with open(report_path, encoding="utf-8") as f:
            report = json.load(f)

    def run_one(job):
        p, img, layer = job
        md_path = os.path.join(pages_dir, f"page_{p:04d}.md")
        if not args.force and os.path.exists(md_path) and os.path.getsize(md_path) > 0:
            return p, None
        last = None
        for attempt in range(args.retries):
            t0 = time.time()
            try:
                text = backend.ocr(img)
                break
            except QuotaExhausted:
                raise
            except Exception as e:
                last = e
                time.sleep(5 * (attempt + 1))
        else:
            return p, {"error": str(last)[:300]}
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(text)
        ratio, recall = similarity(remove_det(text), layer) if layer else (None, None)
        return p, {
            "seconds": round(time.time() - t0, 1),
            "chars": len(text),
            "fffd": text.count("\ufffd"),
            "layer_order_ratio": ratio,
            "layer_word_recall": recall,
        }

    quota_hit = None
    done = skipped = failed = 0
    with ThreadPoolExecutor(max_workers=max(1, args.concurrency)) as ex:
        futs = {ex.submit(run_one, j): j[0] for j in jobs}
        for fut in as_completed(futs):
            try:
                p, info = fut.result()
            except QuotaExhausted as e:
                quota_hit = str(e)[:300]
                for f in futs:
                    f.cancel()
                continue
            except CancelledError:
                continue
            if info is None:
                skipped += 1
                continue
            report[str(p)] = info
            if "error" in info:
                failed += 1
                print(f"  p{p:>4}: FAILED {info['error']}")
            else:
                done += 1
                print(f"  p{p:>4}: {info['seconds']:>5}s {info['chars']:>6} chars"
                      f" fffd={info['fffd']} order={info['layer_order_ratio']}"
                      f" recall={info['layer_word_recall']}")
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=1, sort_keys=True)

    # Rebuild the joined file from every page present on disk (not only this run).
    files = sorted(f for f in os.listdir(pages_dir) if f.endswith(".md"))
    parts = []
    for name in files:
        n = int(name[5:9])
        with open(os.path.join(pages_dir, name), encoding="utf-8") as f:
            parts.append(f"<!-- page {n} -->\n\n{remove_det(f.read())}\n")
    joined = os.path.join(out, f"{stem}.md")
    with open(joined, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))

    print(f"\nOCR'd {done}, skipped (already done) {skipped}, failed {failed}; "
          f"{len(files)} page file(s) on disk -> {joined}")
    if quota_hit:
        print(f"\n!! STOPPED: Space GPU quota exhausted: {quota_hit}\n"
              f"   Re-run the same command later (or set HF_TOKEN) — finished pages are kept.\n"
              f"   Or finish locally now: same command with --backend windows (plain text, no tables).")
        sys.exit(4)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
