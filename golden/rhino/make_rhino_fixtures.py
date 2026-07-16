# -*- coding: utf-8 -*-
"""Sinh fixture .3dm cho golden/rhino/ — good (đúng quy ước HU) và bad (cài lỗi)."""
import os, sys
import rhino3dm as r

OUT = r"d:\KN-Stack\golden\rhino"
os.makedirs(OUT, exist_ok=True)

# ---------- fixture GOOD: mm, tol 0.01, layer đúng, solid kín, đủ UserText ----------
m = r.File3dm()
m.Settings.ModelUnitSystem = r.UnitSystem.Millimeters
m.Settings.ModelAbsoluteTolerance = 0.01

lay = r.Layer(); lay.Name = "VO_NGOAI"
i_vo = m.Layers.Add(lay)
lay2 = r.Layer(); lay2.Name = "BOONG"
i_boong = m.Layers.Add(lay2)

def add_sphere(cx, cy, cz, rad, layer_idx, mat=None, plate=None, name=None):
    b = r.Sphere(r.Point3d(cx, cy, cz), rad).ToBrep()
    a = r.ObjectAttributes()
    a.LayerIndex = layer_idx
    if name: a.Name = name
    if mat: a.SetUserString("material", mat)
    if plate: a.SetUserString("plate_mm", plate)
    m.Objects.AddBrep(b, a)

add_sphere(0, 0, 0, 500, i_vo, mat="5083", plate="5", name="VoMuiTrai")
add_sphere(2000, 0, 0, 500, i_boong, mat="5083", plate="4", name="BoongChinh")
ok = m.Write(os.path.join(OUT, "fixture-good.3dm"), 7)
print("good ->", ok)

# ---------- fixture BAD: đơn vị MÉT, tol lỏng, surface hở, thiếu UserText, layer Default ----------
mb = r.File3dm()
mb.Settings.ModelUnitSystem = r.UnitSystem.Meters          # HU-02 FAIL
mb.Settings.ModelAbsoluteTolerance = 0.5                    # HU-02 FAIL (tol lỏng)

# solid kín nhưng THIẾU UserText + nằm layer Default (index 0 mặc định? tự thêm)
lay0 = r.Layer(); lay0.Name = "Default"
i0 = mb.Layers.Add(lay0)
b1 = r.Sphere(r.Point3d(0, 0, 0), 0.5).ToBrep()
a1 = r.ObjectAttributes(); a1.LayerIndex = i0; a1.Name = "VoThieuThongTin"
mb.Objects.AddBrep(b1, a1)                                  # HU-04 FAIL, HU-03 WARNING

# mặt HỞ: extrusion không nắp
try:
    pl = r.Polyline([r.Point3d(0,0,0), r.Point3d(1,0,0), r.Point3d(1,0.5,0),
                     r.Point3d(0,0.5,0), r.Point3d(0,0,0)])
    crv = pl.ToPolylineCurve()
    ext = r.Extrusion.Create(crv, 0.3, False)               # cap=False -> hở, HU-01 FAIL
    a2 = r.ObjectAttributes(); a2.LayerIndex = i0; a2.Name = "MatHo"
    a2.SetUserString("material", "5083")
    mb.Objects.Add(ext, a2)
    print("extrusion added, IsSolid attr:", getattr(ext, "IsSolid", "N/A"))
except Exception as e:
    print("ext err:", e)

ok = mb.Write(os.path.join(OUT, "fixture-bad.3dm"), 7)
print("bad ->", ok)

# đọc lại kiểm nhanh
chk = r.File3dm.Read(os.path.join(OUT, "fixture-good.3dm"))
print("re-read good: objs =", len(chk.Objects), "units =", chk.Settings.ModelUnitSystem)
for o in chk.Objects:
    g = o.Geometry
    print("  ", o.Attributes.Name, type(g).__name__,
          "IsSolid" , getattr(g, "IsSolid", "?"),
          "| mat:", o.Attributes.GetUserString("material"),
          "| layer idx:", o.Attributes.LayerIndex)
