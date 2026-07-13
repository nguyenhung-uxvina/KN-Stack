#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""qtcn_figure_register.py — Sinh 'PHỤ LỤC minh họa' (figure register) từ QTCN JSON (--cad).

Đọc QTCN-<sp>.json (đã có nhánh cad_illustration cho mỗi nguyên công) → xuất bảng tổng hợp
toàn bộ hình H-A/B/C + mã bản vẽ nguồn để họa viên **nhận việc một lượt**. Có thể append
idempotent vào thân QTCN Markdown (giữa 2 marker) hoặc ghi ra file riêng.

Dùng:
    python qtcn_figure_register.py --in QTCN-<sp>.json [--append QTCN-<sp>.md] [--out <md>]

Không cần thư viện ngoài.
"""
import argparse
import json
import os
import re
import sys

START = "<!-- QTCN-FIGURE-REGISTER:START -->"
END = "<!-- QTCN-FIGURE-REGISTER:END -->"


def norm_drawings(src):
    """Rút danh sách mã bản vẽ (19.BM-01.NN.NN[.HH]) từ chuỗi nguồn (kể cả dạng rút gọn 'NN.NN')."""
    if not src:
        return [], src
    codes = []
    for m in re.finditer(r"19\.BM-01\.\d{2}\.\d{2}(?:\.HH)?", src):
        if m.group(0) not in codes:
            codes.append(m.group(0))
    # dải: 19.BM-01.NN.00–MM.00 → mở rộng NN..MM
    for m in re.finditer(r"19\.BM-01\.(\d{2})\.00\s*[–\-]\s*(\d{2})\.00", src):
        a, b = int(m.group(1)), int(m.group(2))
        for n in range(a, b + 1):
            code = "19.BM-01.%02d.00" % n
            if code not in codes:
                codes.append(code)
    for m in re.finditer(r"(?<![\d.\-])(\d{2}\.\d{2})(?![\d.])", src):
        code = "19.BM-01." + m.group(1)
        if code not in codes:
            codes.append(code)
    return codes, src


def build(doc):
    ops = [o for o in doc.get("operations", []) if o.get("cad_illustration", {}).get("required")]
    prod = doc.get("product", {})
    pname = prod.get("name", "")
    pcode = prod.get("code", "")

    L = [START, "", "---", "",
         "# PHỤ LỤC — SỔ ĐĂNG KÝ HÌNH MINH HỌA (FIGURE REGISTER)", "",
         "> Tổng hợp **%d hình** cần dựng CAD cho QTCN %s (%s). Họa viên nhận việc một lượt: "
         "mỗi dòng = 1 hình + mã bản vẽ nguồn để trích. Sau khi vẽ, thay `[ẢNH: H-<id>]` trong "
         "thân QTCN và tick cột trạng thái. Sinh tự động từ JSON — **đừng sửa tay bảng này**, "
         "chạy lại `qtcn_figure_register.py` khi QTCN đổi." % (len(ops), pcode, pname), ""]

    # --- Bảng 1: danh mục hình theo nguyên công ---
    L.append("## 1. Danh mục hình theo nguyên công")
    L.append("")
    L.append("| Mã hình | NC | Loại hình | Nội dung thể hiện | Callout bắt buộc | Nguồn bản vẽ | Đã vẽ |")
    L.append("|---------|----|-----------|-------------------|------------------|--------------|:---:|")
    for o in ops:
        c = o["cad_illustration"]
        fid = c.get("figure_id") or ("H-%s" % o["id"])
        callout = "; ".join(c.get("callouts", []))
        row = [fid, o["id"], c.get("view_type", ""), c.get("shows", ""),
               callout, c.get("source_drawing", ""), "☐"]
        L.append("| " + " | ".join(x.replace("|", "/") for x in row) + " |")
    L.append("")

    # --- Bảng 2: tổng hợp bản vẽ nguồn ---
    reg = {}          # code -> [figure ids]
    no_dwg = []       # figures without a drawing code (dựng mới / hồ sơ)
    for o in ops:
        c = o["cad_illustration"]
        fid = c.get("figure_id") or ("H-%s" % o["id"])
        codes, raw = norm_drawings(c.get("source_drawing", ""))
        if codes:
            for code in codes:
                reg.setdefault(code, []).append(fid)
        else:
            no_dwg.append((fid, raw))

    L.append("## 2. Tổng hợp bản vẽ nguồn cần trích (lấy một lượt)")
    L.append("")
    L.append("| Bản vẽ nguồn | Số hình | Các hình dùng |")
    L.append("|--------------|:------:|---------------|")
    for code in sorted(reg):
        figs = reg[code]
        L.append("| %s | %d | %s |" % (code, len(figs), ", ".join(figs)))
    L.append("")
    if no_dwg:
        L.append("**Hình dựng mới / từ hồ sơ (không trích bản vẽ chi tiết):**")
        for fid, raw in no_dwg:
            L.append("- %s — %s" % (fid, raw))
        L.append("")

    # --- Bảng 3: tiến độ theo phần ---
    by_phase = {"A": 0, "B": 0, "C": 0}
    for o in ops:
        by_phase[o.get("phase", "?")] = by_phase.get(o.get("phase", "?"), 0) + 1
    L.append("## 3. Tiến độ")
    L.append("")
    L.append("- Tổng hình: **%d** (Phần A: %d · Phần B: %d · Phần C: %d)"
             % (len(ops), by_phase.get("A", 0), by_phase.get("B", 0), by_phase.get("C", 0)))
    L.append("- Số bản vẽ nguồn phải trích: **%d** + %d hình dựng mới/hồ sơ."
             % (len(reg), len(no_dwg)))
    L.append("- Đã vẽ: 0/%d  (họa viên cập nhật)" % len(ops))
    L.append("")
    L.append(END)
    return "\n".join(L)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Sinh PHỤ LỤC hình minh họa từ QTCN JSON")
    ap.add_argument("--in", dest="infile", required=True, help="QTCN-<sp>.json (--cad)")
    ap.add_argument("--append", help="thân QTCN .md để chèn/thay phụ lục (idempotent)")
    ap.add_argument("--out", help="ghi phụ lục ra file .md riêng")
    args = ap.parse_args()

    doc = json.load(open(args.infile, encoding="utf-8"))
    section = build(doc)
    n = sum(1 for o in doc.get("operations", []) if o.get("cad_illustration", {}).get("required"))

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(section + "\n")
        sys.stdout.write("[ok] figure register -> %s (%d hình)\n" % (args.out, n))

    if args.append:
        md = open(args.append, encoding="utf-8").read()
        if START in md and END in md:
            md = re.sub(re.escape(START) + r".*?" + re.escape(END), section, md, flags=re.S)
        else:
            md = md.rstrip() + "\n\n" + section + "\n"
        with open(args.append, "w", encoding="utf-8") as f:
            f.write(md)
        sys.stdout.write("[ok] appended figure register -> %s (%d hình)\n" % (args.append, n))

    if not args.out and not args.append:
        sys.stdout.write(section + "\n")


if __name__ == "__main__":
    main()
