#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_pipeline.py — MỘT LỆNH chạy cả chuỗi trích xuất từ thư mục _QTCN_export

Thay chuỗi 5–7 lệnh tay (bom_xlsx → freecadcmd → validate → cross → merge) bằng:

    python cad-pipeline/scripts/extract/run_pipeline.py --dir "D:\\...\\_QTCN_export\\Tong lap"
        [--name <slug>] [--seed2d <seed-2d-đã-validate.json>] [--release] [--force]

Chuỗi (dừng ngay tại gate đầu tiên chặn, báo rõ gate nào + cách sửa):
  1. Tìm đầu vào trong --dir:  *.step  và  *_BOM.csv|*.xlsx
  2. BOM  → qtcn-seed-bom.json   (bom_xlsx_to_seed.py — QTY/Material/Mass Inventor)
  3. STEP → qtcn-seed-step.json  (freecadcmd + freecad_extract.py — hình học thật)
  4. Gate G1 từng seed (validate_qtcn_seed.py) — FAIL → DỪNG (trừ --force)
  5. Kiểm chéo 2 nguồn S2 (--release: bắt buộc, đúng chính sách phát hành lô)
  6. Merge → qtcn-seed-final.json (+ --seed2d nếu có bản vẽ 2D: dung sai/drawing_no)
  7. Validate seed cuối + tóm tắt: file nào, verdict nào, lệnh kế tiếp

Exit: 0 xong (có thể kèm WARNING — xem danh sách G2) · 2 bị gate chặn · 3 thiếu đầu vào/môi trường.
Cần: python + freecadcmd (env FREECADCMD nếu khác đường dẫn mặc định).
"""
import argparse, glob, json, os, subprocess, sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
FREECADCMD = os.environ.get("FREECADCMD", r"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe")

def run(cmd, env=None, tag=""):
    print("\n=== %s ===" % tag)
    sys.stdout.flush()          # tránh output cha/con đảo thứ tự trên console Windows
    p = subprocess.run(cmd, env=env)
    return p.returncode

def verdict_of(seed_path):
    rep = os.path.splitext(seed_path)[0] + ".validation.json"
    try:
        with open(rep, encoding="utf-8-sig") as f:
            return json.load(f).get("verdict", "?")
    except Exception:
        return "?"

def main():
    ap = argparse.ArgumentParser(description="Pipeline 1 lệnh: _QTCN_export -> seed validated")
    ap.add_argument("--dir", required=True, help="thư mục _QTCN_export/<assembly>")
    ap.add_argument("--name", default=None, help="slug sản phẩm (mặc định = tên thư mục)")
    ap.add_argument("--seed2d", default=None, help="seed 2D (DXF/bản vẽ) ĐÃ validate — ghép dung sai/drawing_no")
    ap.add_argument("--release", action="store_true", help="chế độ phát hành lô: kiểm chéo 2 nguồn BẮT BUỘC")
    ap.add_argument("--force", action="store_true", help="đi tiếp qua gate FAIL (ghi đè có chủ đích — KHÔNG dùng cho phát hành)")
    a = ap.parse_args()

    d = os.path.abspath(a.dir)
    if not os.path.isdir(d):
        sys.stderr.write("[!] Không thấy thư mục: %s\n" % d); sys.exit(3)
    name = a.name or os.path.basename(d.rstrip("\\/")).replace(" ", "-").lower()
    py = sys.executable

    # --- 1. Tìm đầu vào ---
    steps = sorted(glob.glob(os.path.join(d, "*.step"))) + sorted(glob.glob(os.path.join(d, "*.stp")))
    boms = [p for p in sorted(glob.glob(os.path.join(d, "*_BOM.csv")) + glob.glob(os.path.join(d, "*.xlsx")))
            if "giao-viec" not in os.path.basename(p).lower()]
    print("Đầu vào (%s):" % d)
    print("  STEP: %s" % (os.path.basename(steps[0]) if steps else "KHÔNG CÓ"))
    print("  BOM : %s" % (os.path.basename(boms[0]) if boms else "KHÔNG CÓ"))
    if not steps and not boms:
        sys.stderr.write("[!] Không có cả STEP lẫn BOM — chạy rule iLogic Export_QTCN_Package trước.\n")
        sys.exit(3)

    seeds = {}   # nhãn -> đường dẫn seed

    # --- 2. BOM -> seed ---
    if boms:
        out = os.path.join(d, "qtcn-seed-bom.json")
        code = run([py, os.path.join(HERE, "bom_xlsx_to_seed.py"), "--bom", boms[0],
                    "--out", d, "--name", "qtcn-seed-bom", "--product-name", name],
                   tag="BOM → seed (nguồn vàng QTY/Material/Mass)")
        if code == 0:
            seeds["bom"] = out
        else:
            print("[!] BOM → seed lỗi (exit %d) — đi tiếp bằng nguồn còn lại nếu có." % code)

    # --- 3. STEP -> seed ---
    if steps:
        if not os.path.exists(FREECADCMD):
            sys.stderr.write("[!] Không thấy freecadcmd (%s) — đặt env FREECADCMD.\n" % FREECADCMD)
            if not seeds:
                sys.exit(3)
        else:
            env = dict(os.environ, FC_FILE=steps[0], FC_OUT=d, FC_NAME="qtcn-seed-step")
            code = run([FREECADCMD, os.path.join(HERE, "freecad_extract.py")], env=env,
                       tag="STEP → seed (hình học thật qua FreeCAD)")
            out = os.path.join(d, "qtcn-seed-step.json")
            if code == 0 and os.path.exists(out):
                seeds["step"] = out
            else:
                print("[!] STEP → seed lỗi (exit %d)." % code)

    if not seeds:
        sys.stderr.write("[!] Không sinh được seed nào.\n"); sys.exit(3)

    # --- 4. Gate G1 từng seed ---
    blocked = []
    for label, path in seeds.items():
        code = run([py, os.path.join(HERE, "validate_qtcn_seed.py"), "--seed", path],
                   tag="Gate G1 — validate seed %s" % label)
        if code == 2:
            blocked.append(label)
    if blocked and not a.force:
        print("\n████ GATE G1 CHẶN (seed: %s) — pipeline DỪNG." % ", ".join(blocked))
        print("     Sửa lỗi theo *.validation.json (thường: gán vật liệu trong CAD — xem giao-viec.csv),")
        print("     hoặc ghi đè CÓ CHỦ ĐÍCH: thêm --force (không dùng cho phát hành).")
        sys.exit(2)

    # --- 5. Kiểm chéo 2 nguồn (S2) ---
    cross_ok = None
    if "bom" in seeds and "step" in seeds:
        args = [py, os.path.join(HERE, "validate_qtcn_seed.py"),
                "--cross", seeds["bom"], seeds["step"],
                "--report", os.path.join(d, "cross-bom-step.validation.json")]
        if a.release:
            args += ["--seed", seeds["bom"], "--release"]
        code = run(args, tag="Kiểm chéo 2 nguồn độc lập (S2: BOM × STEP)")
        cross_ok = (code != 2)
        if code == 2 and not a.force:
            print("\n████ KIỂM CHÉO FAIL — hai nguồn lệch nhau vượt ngưỡng. Pipeline DỪNG (xem report).")
            sys.exit(2)
    elif a.release:
        print("\n████ --release yêu cầu ĐỦ 2 nguồn (BOM + STEP) để kiểm chéo — hiện chỉ có: %s. DỪNG."
              % ", ".join(seeds))
        sys.exit(2)

    # --- 6. Merge -> seed cuối ---
    final = None
    s2d = a.seed2d or seeds.get("bom")
    s3d = seeds.get("step")
    if s2d and s3d and s2d != s3d:
        final = os.path.join(d, "qtcn-seed-final.json")
        margs = [py, os.path.join(HERE, "merge_qtcn_seeds.py"),
                 "--seed2d", s2d, "--seed3d", s3d, "--out", final]
        if a.force:
            margs.append("--force")
        code = run(margs, tag="Merge → seed cuối (drawing_no/vật liệu/QTY + hình học)")
        if code != 0:
            print("\n████ MERGE bị chặn/lỗi (exit %d)." % code)
            sys.exit(2)
        run([py, os.path.join(HERE, "validate_qtcn_seed.py"), "--seed", final],
            tag="Validate seed cuối")
    else:
        final = s3d or s2d
        print("\n(Chỉ một nguồn khả dụng — seed cuối = %s, không merge.)" % os.path.basename(final))

    # --- 7. Tóm tắt ---
    print("\n" + "=" * 62)
    print("PIPELINE XONG — %s" % name)
    for label, path in seeds.items():
        print("  seed %-5s: %-28s verdict=%s" % (label, os.path.basename(path), verdict_of(path)))
    if cross_ok is not None:
        print("  kiểm chéo : %s" % ("ĐẠT (xem WARNING nếu có)" if cross_ok else "FAIL (--force đã ghi đè)"))
    print("  SEED CUỐI : %s  verdict=%s" % (os.path.basename(final), verdict_of(final)))
    print("  Bước kế   : /qtcn --seed \"%s\"  (hoặc product-dossier)" % final)
    sys.exit(0)

if __name__ == "__main__":
    main()
