# -*- coding: utf-8 -*-
"""
make_golden_v0.py — Sinh golden set v0: 3 chi tiết GIẢI TÍCH (đáp án tính tay chính xác)

Chạy TRONG python của FreeCAD (Gate G3, WX-QT-EXTRACT-SENSOR-01 mục 5 — nhóm mẫu
khởi điểm khi chưa có file CAD thật đã đo tay):
    GOLDEN_OUT=<repo>/golden/step freecadcmd make_golden_v0.py

Ba ca — vật liệu quy ước Thép EH32 ρ=7,85 g/cm³ (STEP không mang nhãn vật liệu,
extractor rơi về default EH32 — chủ đích, để đáp án khớp):

1. plate-4holes  — tấm 1000×500×10, 4 lỗ Ø50 xuyên (bắt: khối lượng, diện tích, trừ lỗ)
   V = 5.000.000 − 4·π·25²·10                = 4.921.460,18 mm³ = 4921,46 cm³
   m = V×7,85/10⁶                            = 38,633 kg
   A = 2(500.000−4·π·625) + 2(1000+500)·10 + 4·π·50·10 = 1.020.575,22 mm² = 10205,75 cm²
2. box-tube      — hộp 60×40×3, L=1000 (bắt: thành mỏng, mặt trong)
   V = (60·40 − 54·34)·1000                  = 564.000 mm³ = 564,00 cm³
   m                                          = 4,427 kg
   A = 2(60+40)·1000 + 2(54+34)·1000 + 2·564 = 377.128 mm² = 3771,28 cm²
3. cylinder      — trụ Ø100×200 (bắt: mặt cong + rule đẳng chu S1-05)
   V = π·50²·200                             = 1.570.796,33 mm³ = 1570,80 cm³
   m                                          = 12,331 kg
   A = 2π·50² + 2π·50·200                    = 78.539,82 mm²  = 785,40 cm²
"""
import os, sys
import FreeCAD, Part
import Import   # Import.export giữ NHÃN chi tiết trong STEP product entity;
                # Part.export thì không (phát hiện bởi chính golden run đầu tiên:
                # name thành "Open CASCADE STEP translator" -> merge theo tên vỡ)

OUT = os.environ.get("GOLDEN_OUT")
if not OUT:
    sys.stderr.write("[!] Thiếu env GOLDEN_OUT\n"); sys.exit(2)

doc = FreeCAD.newDocument("golden")

def export(shape, label, case):
    d = os.path.join(OUT, case, "source")
    os.makedirs(d, exist_ok=True)
    obj = doc.addObject("Part::Feature", label)
    obj.Label = label
    obj.Shape = shape
    path = os.path.join(d, label + ".step")
    Import.export([obj], path)
    # In số FreeCAD tính để đối chiếu chéo với đáp án giải tích ngay lúc sinh
    print("%s: V=%.2f mm3  A=%.2f mm2  -> %s" % (label, shape.Volume, shape.Area, path))

# 1) Tấm 1000×500×10, 4 lỗ Ø50 xuyên
plate = Part.makeBox(1000, 500, 10)
for cx, cy in ((200, 150), (200, 350), (800, 150), (800, 350)):
    plate = plate.cut(Part.makeCylinder(25, 10, FreeCAD.Vector(cx, cy, 0)))
export(plate, "TamKhoetLo", "plate-4holes")

# 2) Hộp 60×40 dày 3, dài 1000 (cắt xuyên: lòng 54×34)
tube = Part.makeBox(60, 40, 1000).cut(
    Part.makeBox(54, 34, 1002, FreeCAD.Vector(3, 3, -1)))
export(tube, "HopThanhMong", "box-tube")

# 3) Trụ đặc Ø100×200
export(Part.makeCylinder(50, 200), "TruDac", "cylinder")

# 4) frame-varies — 2 thanh CÙNG TÊN GỐC, KHÁC chiều dài (mô phỏng Frame Generator):
#    regression cho bug bắt trên Tong lap.iam thật (2026-07-02): est_mass lấy instance
#    nhẹ nhất nhưng volume/bbox lấy instance đầu tiên -> S1-01 FAIL 794%.
#    Thanh 40×40, L=500 (V=800 cm³, m=6,280 kg, A=832 cm²) và L=1000 (m=12,560 kg).
#    Kỳ vọng nhóm: qty=2, varies=true, est=6,280 + volume=800 + bbox 40×40×500 (CÙNG
#    thanh ngắn), total = 18,840 kg.
d4 = os.path.join(OUT, "frame-varies", "source")
os.makedirs(d4, exist_ok=True)
b1 = doc.addObject("Part::Feature", "ThanhGoc")
b1.Label = "ThanhGoc"
b1.Shape = Part.makeBox(40, 40, 500)
b2 = doc.addObject("Part::Feature", "ThanhGoc001")   # hậu tố instance kiểu STEP/Inventor
b2.Label = "ThanhGoc001"
b2.Shape = Part.makeBox(40, 40, 1000, FreeCAD.Vector(100, 0, 0))
p4 = os.path.join(d4, "ThanhGocX2.step")
Import.export([b1, b2], p4)
print("ThanhGoc x2: V=%.2f + %.2f mm3 -> %s" % (b1.Shape.Volume, b2.Shape.Volume, p4))

print("OK: 4 case golden v0 da sinh.")
