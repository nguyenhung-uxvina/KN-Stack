#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Authoritative parts master for GIÁ TRƯỢT UUV, compiled from the PDF BOM sheets
(groups 1/3/4) + the two laser-nesting sheets. This is the corrected source of
truth that overrides the stale title-block codes found in the DXF/PDF detail
sheets. Emits PARTS_MASTER.md, FAB_ROUTING.md, PARTS_MASTER.csv.

  python authoritative_bom.py --out <dir>
"""
import io, os, csv, argparse
from collections import defaultdict

# code, name, qty(total/product), material, stock(thickness or Ø), process, parent_assembly, note/flag
P = [
 # ---- GT.00.01.00 KHUNG CƠ SỞ (assembly, 60kg) ----
 ("GT.00.01.00","Khung cơ sở","1","-","-","WELD-ASSY","GT.00.00.00",""),
 ("GT.00.01.01","Tấm cơ sở","1","Nhôm 5083","6mm","LASER+BEND","GT.00.01.00","4250±3 ×310"),
 ("GT.00.01.02","Gối đỡ đuôi xi lanh","1","Thép C45","Ø/khối","TURN/MILL","GT.00.01.00","Ø25H7,Ø25h7"),
 ("GT.00.01.03","Tai gá giá phụ","1","Thép SS400","10mm","LASER+BEND","GT.00.01.00","172×150×80"),
 ("GT.00.01.04","Trục quay giá phụ","1","Thép C45","Ø30","TURN","GT.00.01.00","Ø30h7 ×186"),
 ("GT.00.01.05","Cữ chặn vị trí ban đầu","1","Nhôm 5083","10mm","LASER+BEND+WELD","GT.00.01.00","CT1+CT2"),
 ("GT.00.01.06","Thanh chống","2","Thép SS400","ốngØ42×3 + 10mm","WELD","GT.00.01.00","L1015; ⚠tai đầu xung đột VL/SL"),
 ("GT.00.01.07","Tai gá thanh chống","2","Nhôm 5083","10mm","LASER","GT.00.01.00","85×70"),
 ("GT.00.01.08","Con lăn cơ sở","1","-","-","WELD-ASSY","GT.00.01.00","5 chi tiết con"),
 ("GT.00.01.08a","Tấm đế con lăn cơ sở","1","Thép SS400","10mm","LASER","GT.00.01.08","270×140"),
 ("GT.00.01.08b","Tai gá con lăn cơ sở","2","Thép SS400","10mm","LASER","GT.00.01.08","Ø? ; nesting SL02"),
 ("GT.00.01.08c","Trục con lăn cơ sở","1","Thép SS400","Ø30","TURN","GT.00.01.08","Ø30h7,Ø55 L167"),
 ("GT.00.01.08d","Con lăn cơ sở (ống)","1","Nhựa Teflon","Ø78","TURN","GT.00.01.08","Ø40H7 nội"),
 ("GT.00.01.08e","Bạc đồng con lăn cơ sở","1","Đồng đỏ","Ø50","TURN","GT.00.01.08","Ø30F7/Ø40m6"),
 ("GT.00.01.09","Tai bắt khung cơ sở","8","Nhôm 5083","6mm","LASER+BEND","GT.00.01.00","115×50"),
 ("GT.00.01.10","Gân tăng cứng cơ sở","5","Nhôm 5083","6mm","LASER","GT.00.01.00","296×40"),

 # ---- GT.00.03.00 GIÁ PHỤ (assembly) ----
 ("GT.00.03.00","Giá phụ","1","-","-","WELD-ASSY","GT.00.00.00",""),
 ("GT.00.03.01","Chốt đầu xi lanh","1","Thép C45","Ø40","TURN","GT.00.03.00","Ø28h7 L186"),
 ("GT.00.03.02","Bạc lót trục đầu xi lanh","1","INOX 304","Ø56","TURN","GT.00.03.00","Ø40h7"),
 ("GT.00.03.03","Ống bao đầu giá phụ","1","Thép C45","Ø50","TURN","GT.00.03.00","Ø50h7,Ø30.6 M8"),
 ("GT.00.03.04","Giá phụ (tấm+tai gá)","1","Thép SS400","5mm/10mm","LASER+WELD","GT.00.03.00","1270; tai gá SL2 10mm"),
 ("GT.00.03.05","Ống bao đuôi giá phụ","1","Thép SS400","Ø44","TURN","GT.00.03.00","Ø30.6 M8; ⚠sheet ghi nhầm .04"),
 ("STD-VM8-3","Vú mỡ M8","2","mua","-","PURCHASE","GT.00.03.00",""),

 # ---- GT.00.04.00 GIÁ CHÍNH (assembly, 60kg) ----
 ("GT.00.04.00","Giá chính","1","-","-","WELD-ASSY","GT.00.00.00",""),
 ("GT.00.04.01","Khung giá chính","1","Nhôm 5083","6mm prof 400×105","LASER+BEND+WELD","GT.00.04.00","5125±2; 83kg"),
 ("GT.00.04.01a","Gân tăng cứng giá chính 1","2","Nhôm 5083","6mm","LASER","GT.00.04.01","107.5"),
 ("GT.00.04.01b","Gân tăng cứng giá chính 2","2","Nhôm 5083","6mm","LASER","GT.00.04.01","107.5×95"),
 ("GT.00.04.01c","Gân tăng cứng giá chính 3","8","Nhôm 5083","6mm","LASER","GT.00.04.01","386×95"),
 ("GT.00.04.01d","Tai khóa vị trí đầu","1","Nhôm 5083","10mm","LASER","GT.00.04.01","80×60.5"),
 ("GT.00.04.01e","Ray dẫn hướng con lăn CT1","1","Thép SS400","6mm","LASER+WELD","GT.00.04.01","108×1200"),
 ("GT.00.04.01f","Ray dẫn hướng con lăn CT2","1","Thép SS400","6mm","LASER+WELD","GT.00.04.01","50×1200"),
 ("GT.00.04.01g","Ray dẫn hướng con lăn CT3","1","Thép SS400","6mm","LASER+WELD","GT.00.04.01","350×1200 nhiều lỗ"),
 ("GT.00.04.01h","Tai gá đầu giá chính","2","Nhôm 5083","10mm?","LASER/MILL","GT.00.04.01","Ø40H7 R28"),
 ("GT.00.04.01i","Bạc lót tai gá đầu giá","2","Đồng đỏ","Ø50","TURN","GT.00.04.01","Ø40h7/Ø30.6"),
 ("GT.00.04.02","Trục quay đầu giá chính","1","Thép C45","Ø30","TURN","GT.00.04.00","Ø30h7 L267; ⚠sheet=GT.00.01.02"),
 ("GT.00.04.03","Giá đỡ rulo","1","Nhôm 5083","6mm","LASER+BEND","GT.00.04.00","390×210×160; ⚠sheet=.01.03"),
 ("GT.00.04.04","Puly dẫn cáp","1","-","-","WELD-ASSY","GT.00.04.00","4.6kg; ⚠sheet=.01.04"),
 ("GT.00.04.04a","Tấm đế puly dẫn cáp","1","Nhôm 5083","6mm","LASER","GT.00.04.04","120×130"),
 ("GT.00.04.04b","Tấm gá puly dẫn cáp","2","Nhôm 5083","6mm","LASER","GT.00.04.04","375.5"),
 ("GT.00.04.04c","Bạc puly dẫn cáp","1","Đồng đỏ","Ø30","TURN","GT.00.04.04","Ø20.6"),
 ("GT.00.04.04d","Puly dẫn cáp (ròng rọc)","1","Nhựa Teflon","Ø64","TURN","GT.00.04.04","Ø30H7"),
 ("GT.00.04.04e","Trục giữ dây","1","Thép C45","Ø20","TURN","GT.00.04.04","Ø10 L65"),
 ("GT.00.04.04f","Trục puly dẫn cáp","1","Thép C45","Ø34","TURN","GT.00.04.04","Ø20h7 L65"),
 ("GT.00.04.05","Cữ chặn con trượt","4","Thép SS400","khối","MILL","GT.00.04.00","55×42 4×M8; ⚠sheet=.01.05"),
 ("GT.00.04.06","Ray trượt HGH30 CA","2","mua","L4670","PURCHASE+CUT","GT.00.04.00","⚠sheet=.01.06"),
 ("GT.00.04.07","Khung hộp 50x100x5","2","Nhôm 5083","hộp 50×100×5","WELD","GT.00.04.00","L4600; ⚠sheet=.01.07"),
 ("GT.00.04.07a","Tấm bịt đầu","5","Nhôm 5083","6mm","LASER+BEND","GT.00.04.07","123×100"),
 ("GT.00.04.08","Khung trượt","6","-","-","WELD-ASSY","GT.00.04.00","5kg; ⚠sheet=.01.08"),
 ("GT.00.04.08a","Giá đỡ thanh trượt","18","Nhôm 5083","6mm","LASER","GT.00.04.08","147×257 (3×6)"),
 ("GT.00.04.08b","Hộp nhôm 30×30×1300","12","Nhôm 5083","hộp 30×30","PURCHASE+CUT","GT.00.04.08","2/assy ×6"),
 ("GT.00.04.08c","Tấm mặt trượt (Teflon)","12","Nhựa Teflon","10mm","LASER","GT.00.04.08","410-pitch; 2/assy"),
 ("GT.00.04.08d","Tấm mặt trượt (cao su)","24","Cao su","2-3mm","CUT","GT.00.04.08","2+2/assy"),
 ("GT.00.04.09","Vành đón mũi","1","-","-","WELD-ASSY","GT.00.04.00","44kg; ⚠sheet=.01.09"),
 ("GT.00.04.09a","Bàn trượt","1","Nhôm 5083","? (cụm lỗ)","LASER+MILL","GT.00.04.09","600×? nhiều lỗ ren"),
 ("GT.00.04.09b","Vành đón mũi CT1","1","Nhôm 5083","10mm","LASER+BEND","GT.00.04.09",""),
 ("GT.00.04.09c","Vành đón mũi CT2","2","Nhôm 5083","10mm","LASER","GT.00.04.09",""),
 ("GT.00.04.09d","Vành đón mũi CT3","1","Nhôm 5083","10mm","LASER","GT.00.04.09","220×325"),
 ("GT.00.04.09e","Vành đón mũi CT4","1","Nhôm 5083","10mm","LASER+BEND","GT.00.04.09",""),
 ("GT.00.04.09f","Miệng luồn dây 1","1","Nhôm 5083","6mm","LASER","GT.00.04.09","134×70"),
 ("GT.00.04.09g","Miệng luồn dây 2","2","Nhôm 5083","6mm","LASER","GT.00.04.09","237×90"),
 ("GT.00.04.09h","Miệng luồn dây 4","1","Nhôm 5083","6mm","LASER","GT.00.04.09","190×103"),
 ("GT.00.04.09i","Miệng luồn dây 5","1","Nhôm 5083","6mm","LASER","GT.00.04.09","92×65"),
 ("GT.00.04.09j","Ống lồng ngắn","2","Nhôm 5083","ốngØ15/Ø11","TURN/CUT","GT.00.04.09","L51"),
 ("GT.00.04.09k","Ống lồng dài","2","Nhôm 5083","ốngØ15/Ø11","TURN/CUT","GT.00.04.09","L78"),
 ("STD-HGH30-10","Con trượt HGH 30 CA","4","mua","-","PURCHASE","GT.00.04.00",""),
]

COLS = ["code","name","qty","material","stock","process","parent","note"]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default=".")
    a = ap.parse_args(); out = a.out; os.makedirs(out, exist_ok=True)
    rows = [dict(zip(COLS, r)) for r in P]

    # CSV
    with io.open(os.path.join(out,"PARTS_MASTER.csv"),"w",encoding="utf-8",newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS); w.writeheader()
        for r in rows: w.writerow(r)

    # PARTS_MASTER.md
    M = ["# PARTS MASTER (authoritative) — GIÁ TRƯỢT UUV","",
         "> Nguồn chân lý: BOM 3 PDF (nhóm 1/3/4) + 2 tờ sắp hình laser. Mã đã **sửa** theo tờ BOM; cột note đánh dấu mã khung tên sai trên tờ chi tiết.","",
         "| Mã đúng | Tên | SL | Vật liệu | Phôi/dày | Công nghệ | Thuộc cụm | Ghi chú |",
         "|---|---|--:|---|---|---|---|---|"]
    for r in rows:
        M.append(f"| {r['code']} | {r['name']} | {r['qty']} | {r['material']} | {r['stock']} | {r['process']} | {r['parent']} | {r['note']} |")
    with io.open(os.path.join(out,"PARTS_MASTER.md"),"w",encoding="utf-8") as f:
        f.write("\n".join(M))

    # FAB_ROUTING.md — group by process + material/thickness for nesting
    leaf = [r for r in rows if r["process"] not in ("WELD-ASSY",)]
    by_proc = defaultdict(list)
    for r in leaf: by_proc[r["process"].split("+")[0].split("/")[0]].append(r)
    R = ["# FAB ROUTING — GIÁ TRƯỢT UUV","",
         "Cut-list & routing theo trạm. SL = tổng/sản phẩm (đã nhân cụm con).",""]
    # laser nesting by material+thickness
    laser = [r for r in leaf if "LASER" in r["process"]]
    nest = defaultdict(list)
    for r in laser: nest[(r["material"], r["stock"])].append(r)
    R.append("## TRẠM LASER + CHẤN (nhóm theo vật liệu × bề dày → sắp hình)")
    for (mat,th),items in sorted(nest.items()):
        tot = sum(int(i["qty"]) for i in items if i["qty"].isdigit())
        R.append(f"\n### {mat} — {th}  ({len(items)} loại, {tot} tấm)")
        for i in items: R.append(f"- [{i['qty']}×] {i['name']} ({i['code']}) {i['note']}")
    # turning
    turn = [r for r in leaf if r["process"].startswith("TURN") or "MILL" in r["process"]]
    R.append("\n## TRẠM TIỆN / PHAY")
    for i in turn: R.append(f"- [{i['qty']}×] {i['name']} ({i['code']}) — {i['material']} {i['stock']} {i['note']}")
    # purchase
    buy = [r for r in leaf if "PURCHASE" in r["process"]]
    R.append("\n## MUA NGOÀI / CẮT PHÔI")
    for i in buy: R.append(f"- [{i['qty']}×] {i['name']} ({i['code']}) — {i['material']} {i['stock']}")
    # weld assemblies
    R.append("\n## TRẠM HÀN (cụm lắp)")
    for r in rows:
        if r["process"]=="WELD-ASSY" or "WELD" in r["process"]:
            R.append(f"- {r['name']} ({r['code']}) ×{r['qty']} ⟶ thuộc {r['parent']}")
    with io.open(os.path.join(out,"FAB_ROUTING.md"),"w",encoding="utf-8") as f:
        f.write("\n".join(R))

    # rollups
    mat = defaultdict(int)
    for r in leaf:
        if r["qty"].isdigit(): mat[r["material"]] += int(r["qty"])
    print("parts(rows)=",len(rows)," leaf=",len(leaf))
    print("material totals (pieces):", dict(mat))
    print("laser nesting groups:", {f"{m} {t}":len(v) for (m,t),v in nest.items()})
    print("wrote PARTS_MASTER.md/.csv + FAB_ROUTING.md ->", out)

if __name__ == "__main__":
    main()
