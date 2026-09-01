#!/usr/bin/env python3
"""
cad_fab_pipeline.py — one-command drawing-folder → fabrication bundle.

Codifies the proven manual workflow (GIÁ TRƯỢT UUV / Khung cơ sở) so any
drawing group runs the SAME deterministic pipeline without redoing it by hand:

  1. ingest  — read every DWG/DXF (via helix-cad-ingest/ingest.py; DWG→ODA)
  2. aggregate — roll up per-part extracts → MASTER_BOM + CRITICAL_DIMS
  3. pdf      — dump the PDF text per page + auto-extract the parts-list rows
               (lines carrying material + thickness + SL) for AI/CEO decode
  4. report   — PIPELINE_REPORT.md: counts, materials, flags, AI next-steps

The JUDGMENT tail (decode garbled Vietnamese names, map codes, resolve
conflicts, fill the TCVN Quy trình công nghệ, run nest, emit DOCX) stays with
AI + CEO — this script does the mechanical ~80% identically every time.

  python cad_fab_pipeline.py "<drawing_folder>" --classification MẬT \
         --out "<folder>/ingested" [--prefer dwg]

All file output is UTF-8. Run with PYTHONUTF8=1 on Windows.
"""
import argparse
import glob
import os
import re
import subprocess
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
INGEST = os.path.join(HERE, "..", "helix-cad-ingest", "ingest.py")
AGGREGATE = os.path.join(HERE, "..", "helix-cad-ingest", "aggregate.py")
WORKBOOK = os.path.join(HERE, "..", "helix-cad-workbook", "fab_workbook.py")
DEFAULT_MASTER = r"D:\Workshop_X\3_Resources\Master-Data\WX-MASTER-DATA.xlsx"


def run(cmd):
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    print("  $", " ".join(os.path.basename(c) if c.endswith(".py") else c for c in cmd))
    return subprocess.run(cmd, env=env, capture_output=True, text=True, encoding="utf-8")


def step_ingest(folder, out, classification, prefer):
    r = run([sys.executable, INGEST, folder, "--out", out,
             "--classification", classification, "--prefer", prefer])
    print(r.stdout.strip()[-1500:] or r.stderr.strip()[-800:])
    n = len(glob.glob(os.path.join(out, "*.cad_extract.json")))
    return n


def step_aggregate(out):
    r = run([sys.executable, AGGREGATE, out])
    print(r.stdout.strip() or r.stderr.strip()[-800:])
    return r.stdout.strip()


def step_pdf(folder, out):
    """Dump PDF text + auto-extract parts-list rows (material+thickness+SL)."""
    pdfs = glob.glob(os.path.join(folder, "*.pdf")) + glob.glob(os.path.join(folder, "*.PDF"))
    if not pdfs:
        print("  [pdf] no PDF in folder — skip (machine-truth only)")
        return [], None
    try:
        import fitz
    except ImportError:
        print("  [pdf] PyMuPDF not installed (pip install pymupdf) — skip")
        return [], pdfs[0]
    pdf = pdfs[0]
    doc = fitz.open(pdf)
    raw_lines = []
    rows = []
    for pi, pg in enumerate(doc):
        t = pg.get_text("text")
        raw_lines.append(f"\n===== PAGE {pi+1} ({pg.rect.width:.0f}x{pg.rect.height:.0f}) =====")
        raw_lines.append(t)
        for ln in t.splitlines():
            if re.search(r"\bSL\s*\d", ln):   # parts-list nomenclature row
                mat = ("NHÔM 5083" if "5083" in ln else
                       "THÉP SS400" if "SS400" in ln else
                       "THÉP C45" if ("C45" in ln or "S45C" in ln) else "?")
                thk = (re.search(r"(\d+)\s*mm", ln) or [None, "?"])[1]
                sl = (re.search(r"SL\s*(\d+)", ln) or [None, "?"])[1]
                rows.append({"page": pi + 1, "raw_name": ln.strip(),
                             "material": mat, "thickness_mm": thk, "qty": sl})
    with open(os.path.join(out, "PDF_RAW.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(raw_lines))
    import csv
    with open(os.path.join(out, "PDF_PARTSLIST.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["page", "raw_name", "material", "thickness_mm", "qty"])
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"  [pdf] {pdf} — {doc.page_count} pages; {len(rows)} parts-list rows "
          f"-> PDF_PARTSLIST.csv (raw_name garbled → AI decode)")
    return rows, pdf


def step_report(folder, out, n_extracts, agg_summary, pl_rows, pdf):
    # materials from aggregate stdout
    mats = re.search(r"materials=\{([^}]*)\}", agg_summary or "")
    stale = re.search(r"stale-code parts=(\d+)", agg_summary or "")
    pl_mat = defaultdict(int)
    for r in pl_rows:
        if str(r["qty"]).isdigit():
            pl_mat[(r["material"], r["thickness_mm"])] += int(r["qty"])
    lines = [
        f"# PIPELINE REPORT — {os.path.basename(folder)}\n",
        f"> cad_fab_pipeline · nguồn: {os.path.basename(folder)}\n",
        "## Đã chạy (deterministic)",
        f"- ingest: **{n_extracts}** bản vẽ → cad_extract.json/.md",
        f"- aggregate: {agg_summary or '(xem MASTER_BOM.md)'}",
        f"- PDF parts-list (authoritative): **{len(pl_rows)}** dòng "
        f"({'có' if pdf else 'không'} PDF) → PDF_PARTSLIST.csv + PDF_RAW.txt",
    ]
    if pl_mat:
        lines.append("\n## Gom vật liệu × dày từ bảng kê PDF (cho nest/mua):")
        for (m, t), q in sorted(pl_mat.items()):
            lines.append(f"- {m} — {t}mm: {q} phôi")
    lines += [
        "\n## ⏭️ Bước AI/CEO finalize (judgment — không tự động hóa)",
        "1. **Giải mã tên chi tiết** trong PDF_PARTSLIST.csv (font lỗi /ToUnicode → AI dịch; số/VL/SL đã trích).",
        "2. **Đối chiếu** PDF parts-list (chuẩn) ↔ MASTER_BOM (DWG): khóa mã + SL, gắn cờ xung đột (C45 tiện riêng, vượt khổ tấm, VL/SL...).",
        "3. **Nest**: tạo parts.csv (mã,material,thickness_mm,bbox_w,bbox_h,qty) → "
        "`python ../helix-cad-nest/nest_estimate.py --parts parts.csv --out nest`.",
        "4. **Quy trình công nghệ (TCVN)**: forge-fabrication F0 + template 11 mục → QUY_TRINH_CONG_NGHE.md → "
        "`python md_to_docx.py QUY_TRINH_CONG_NGHE.md`.",
        "5. **Kiểm CHECKLIST** trong {PROJECT}_FAB-DB.xlsx — ô đỏ THIẾU phải xử lý trước handoff "
        "(gate param_sufficiency của helix-cad-validate sẽ chặn).",
        "6. **CEO chốt** cờ §11 + classification, ký phát hành.",
    ]
    p = os.path.join(out, "PIPELINE_REPORT.md")
    with open(p, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return p


def step_workbook(out, project, master):
    """Sinh {PROJECT}_FAB-DB.xlsx (helix-cad-workbook). Skip có hướng dẫn nếu thiếu master —
    KHÔNG bịa đơn giá (fail-safe)."""
    if not os.path.isfile(WORKBOOK):
        print(f"  [workbook] không thấy fab_workbook.py ({WORKBOOK}) — skip")
        return None
    if not master or not os.path.isfile(master):
        print(f"  [workbook] KHÔNG thấy master data: {master}")
        print(f"  → tạo seed: python \"{WORKBOOK}\" --init-master \"{master}\" (kỹ sư duyệt giá trước khi dùng)")
        return None
    r = run([sys.executable, WORKBOOK, out, "--master", master, "--project", project])
    print(r.stdout.strip()[-600:] or r.stderr.strip()[-600:])
    return os.path.join(out, "..", f"{project}_FAB-DB.xlsx")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--classification", default="MẬT")
    ap.add_argument("--out", default=None)
    ap.add_argument("--prefer", choices=["dwg", "dxf"], default="dwg")
    ap.add_argument("--master", default=DEFAULT_MASTER, help="WX-MASTER-DATA.xlsx (đơn giá/hao hụt/định mức)")
    ap.add_argument("--project", default=None, help="mã dự án cho tên FAB-DB.xlsx (mặc định tên folder)")
    ap.add_argument("--no-workbook", action="store_true")
    a = ap.parse_args()
    folder = a.folder
    out = a.out or os.path.join(folder, "ingested")
    os.makedirs(out, exist_ok=True)
    print(f"=== CAD→FAB PIPELINE === {folder}\nclassification: {a.classification} · out: {out}\n")
    print("[1/5] ingest (DWG/DXF → cad_extract)")
    n = step_ingest(folder, out, a.classification, a.prefer)
    print("\n[2/5] aggregate (→ MASTER_BOM + CRITICAL_DIMS)")
    agg = step_aggregate(out)
    print("\n[3/5] PDF parts-list extract")
    pl, pdf = step_pdf(folder, out)
    print("\n[4/5] report")
    rp = step_report(folder, out, n, agg, pl, pdf)
    wbk = None
    if not a.no_workbook:
        print("\n[5/5] workbook (→ {PROJECT}_FAB-DB.xlsx: PARTS/BOM/DINH_MUC/DU_TOAN/QC_DIMS/CHECKLIST)")
        wbk = step_workbook(out, a.project or os.path.basename(os.path.abspath(folder)), a.master)
    print(f"\n✅ DONE → {out}\n   PIPELINE_REPORT.md · MASTER_BOM.* · CRITICAL_DIMS.md · "
          f"PDF_PARTSLIST.csv · PDF_RAW.txt · {n} cad_extract" + (" · FAB-DB.xlsx" if wbk else ""))
    print("   Next: AI/CEO finalize (xem PIPELINE_REPORT.md §⏭️).")


if __name__ == "__main__":
    main()
