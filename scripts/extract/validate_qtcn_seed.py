#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_qtcn_seed.py — Bộ sensor + gate cho qtcn-seed/v1 (WX-QT-EXTRACT-SENSOR-01)

Hiện thực 4 lớp sensor + Gate G1/G3 của tài liệu docs/WX-QT-EXTRACT-SENSOR-01.md,
chạy trên JSON qtcn-seed/v1 — KHÔNG phụ thuộc phần mềm CAD nguồn (một schema —
nhiều adapter — một bộ sensor). Seed FAIL không được đóng dấu validated; pipeline
5 đầu ra (qtcn / product-dossier / định mức / dự toán / nghiệm thu) từ chối nhận.

CÁC CHẾ ĐỘ (mã rule theo đúng tài liệu):
    --seed a.json [--seed b.json ...]   S1-01…S1-08 + S4-03 (bất biến vật lý, mỗi seed)
    --cross inv.json fc.json            S2-01…S2-03 (kiểm chéo 2 nguồn độc lập, khớp tên mờ)
    --history history.jsonl             S3-01 (sanity theo lịch sử; cần --seed)
    --update-history                    ghi seed đã PASS vào history.jsonl (nuôi S3)
    --determinism a.json b.json         S4-01 (2 lần chạy cùng nguồn phải trùng số)
    --diff old.json new.json            S4-02 (diff giữa revision — báo cáo cho người duyệt)
    --golden <dir>                      Gate G3 (mỗi case: expected-seed.json + actual-seed.json)
    --materials materials.json          danh mục vật liệu duyệt (mặc định: bảng nội bộ dưới)

Xuất <seed>.validation.json (= biểu mẫu WX-QT-EXTRACT-F01). Mã thoát:
    0 PASS · 1 chỉ WARNING (kèm danh sách kiểm mẫu G2) · 2 có FAIL (G1 chặn) · 3 lỗi dùng

LƯU Ý HIỆN THỰC (khác biệt có chủ đích so với chữ nghĩa tài liệu, đều ghi trong report):
  - Trường THIẾU (vd seed 2D chưa có est_mass_kg) → WARNING "thiếu trường", không FAIL:
    seed 2D hợp lệ theo thiết kế (mass đến từ merge với seed 3D/BOM). Trường CÓ mà sai → FAIL.
  - S1-05 dùng bất đẳng thức đẳng chu A ≥ (36π·V²)^(1/3) (cận dưới ĐÚNG cho mọi solid;
    công thức hình hộp trong dự thảo gốc FAIL oan chi tiết tròn) — xem chú thích (*) trong doc.
  - S2-01/02: khi một đường phải GIẢ ĐỊNH khối lượng riêng (density_assumed) thì lệch đo
    sai số của ρ đoán, không phải lỗi trích → nới thành WARNING >10% thay vì FAIL >0,5%.
"""
import argparse, difflib, json, math, os, re, sys, unicodedata

VERSION = "0.1.0"

for _s in (sys.stdout, sys.stderr):   # console Windows cp1252 -> in tiếng Việt không vỡ
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ---------------- Danh mục vật liệu duyệt (S1-02) — ρ theo g/cm³ ----------------
# MỘT NGUỒN: schemas/materials.json (đọc lúc import; mọi script dùng chung qua
# DEFAULT_MATERIALS của module này). Danh sách nội tuyến dưới chỉ là FALLBACK khi
# file không tồn tại (chạy script lẻ ngoài repo). Ghi đè per-run: --materials <json>.
_FALLBACK_MATERIALS = [
    {"names": ["5083", "al5083", "a5083"], "density_g_cm3": 2.66},
    {"names": ["5086"], "density_g_cm3": 2.66},
    {"names": ["6061"], "density_g_cm3": 2.70},
    {"names": ["6082"], "density_g_cm3": 2.70},
    {"names": ["nhom", "aluminum", "aluminium", "alumin"], "density_g_cm3": 2.70},
    {"names": ["eh32", "ct3", "ct4", "ss400", "q235", "thep", "steel", "carbon"], "density_g_cm3": 7.85},
    {"names": ["sus", "inox", "stainless", "304", "316"], "density_g_cm3": 7.93},
    {"names": ["composite", "frp", "grp", "soi thuy tinh", "glass"], "density_g_cm3": 1.70},
    {"names": ["go", "wood", "thong", "pine"], "density_g_cm3": 0.55},
    {"names": ["dong", "brass", "bronze", "copper"], "density_g_cm3": 8.50},
]

MATERIALS_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                               "..", "..", "schemas", "materials.json"))

def _load_catalog():
    try:
        with open(MATERIALS_PATH, encoding="utf-8-sig") as f:
            data = json.load(f)
        # nhận cả 2 dạng: {"materials": [...]} (chuẩn) hoặc list trần (file --materials cũ)
        return data["materials"] if isinstance(data, dict) else data
    except Exception:
        return _FALLBACK_MATERIALS

DEFAULT_MATERIALS = _load_catalog()

# Trường volatile — bỏ qua khi so determinism / golden (đường dẫn, timestamp, version)
VOLATILE_KEYS = {"file", "bom_file", "extracted_at", "extract_timestamp", "timestamp",
                 "freecad_version", "extractor_version", "header_row", "operator",
                 "sha256", "source_sha256", "_note"}

def strip_accents(s):
    s = (s or "").replace("đ", "d").replace("Đ", "D")   # đ không decompose qua NFD
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")

def norm(s):
    return re.sub(r"\s+", " ", strip_accents(str(s or "")).lower()).strip()

def load(path):
    with open(path, encoding="utf-8-sig") as f:   # -sig: chịu BOM từ Excel/PowerShell
        return json.load(f)

def require_validated(seed_path, force=False, out=sys.stderr):
    """Cưỡng chế Gate G1 tại script TIÊU THỤ seed (merge/qtcn/5 đầu ra).

    Trả True nếu seed được phép dùng: tồn tại <stem>.validation.json với
    verdict != FAIL và không cũ hơn seed. force=True chỉ hạ FAIL-chặn xuống
    cảnh báo (dùng khi CEO quyết định ghi đè có chủ đích).
    """
    rep_path = os.path.splitext(seed_path)[0] + ".validation.json"
    problem = None
    if not os.path.exists(rep_path):
        problem = ("chưa qua validator — chạy:\n"
                   "    python scripts/extract/validate_qtcn_seed.py --seed \"%s\"" % seed_path)
    else:
        try:
            with open(rep_path, encoding="utf-8-sig") as f:
                rep = json.load(f)
            if rep.get("verdict") == "FAIL":
                problem = "validation verdict = FAIL (Gate G1) — sửa lỗi rồi validate lại"
            elif os.path.getmtime(rep_path) < os.path.getmtime(seed_path):
                problem = "seed MỚI HƠN validation report — seed đã đổi sau khi validate, chạy lại validator"
        except Exception as e:
            problem = "không đọc được validation report: %s" % e
    if problem is None:
        return True
    tag = "[GATE-OVERRIDE]" if force else "[GATE G1]"
    out.write("%s %s: %s\n" % (tag, os.path.basename(seed_path), problem))
    return force

def material_entry(mat, catalog):
    t = norm(mat)
    if not t:
        return None
    for e in catalog:
        if any(n in t for n in e["names"]):
            return e
    return None

# ---------------------------- Báo cáo (biểu mẫu F01) ----------------------------
class Report:
    def __init__(self):
        self.entries = []
    def add(self, rule, level, where, msg, measured=None):
        self.entries.append({"rule": rule, "level": level, "where": where,
                             "msg": msg, "measured": measured})
    def count(self, level):
        return sum(1 for e in self.entries if e["level"] == level)
    def verdict(self):
        if self.count("FAIL"):
            return "FAIL"
        return "WARNING" if self.count("WARNING") else "PASS"
    def dump(self, path, extra=None):
        out = {"form": "WX-QT-EXTRACT-F01", "validator_version": VERSION,
               "verdict": self.verdict(),
               "counts": {lv: self.count(lv) for lv in ("FAIL", "WARNING", "INFO", "PASS")},
               "rules": self.entries}
        if extra:
            out.update(extra)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        return out

# ------------------------- Trích trường từ 1 dòng BOM seed ----------------------
def _qty_of(p):
    """qty trực tiếp; seed gộp (qtcn-seed-merged/v1) chỉ có qty_3d/qty_2d."""
    if p.get("qty") is not None:
        return p["qty"]
    if p.get("qty_3d") is not None:
        return p["qty_3d"]
    m = re.search(r"\d+", str(p.get("qty_2d") or ""))   # qty_2d có thể là "4 cái"
    return int(m.group(0)) if m else None

def fields(p):
    s = p.get("specs") or {}
    bb = s.get("bbox_mm") or {}
    return {
        "name": p.get("name") or p.get("drawing_no") or p.get("vt"),
        "qty": _qty_of(p),
        "material": p.get("material") or p.get("material_3d") or p.get("material_2d"),
        "mass": s.get("est_mass_kg"), "total_mass": s.get("total_mass_kg"),
        "vol_cm3": s.get("volume_cm3"), "area_cm2": s.get("area_cm2"),
        "bbox": [bb.get("x"), bb.get("y"), bb.get("z")] if bb else None,
        "rho": s.get("density_g_cm3"), "assumed": bool(s.get("density_assumed")),
        "src": s.get("material_source"),
    }

def bad_num(v):
    return isinstance(v, (int, float)) and (math.isnan(v) or math.isinf(v) or v <= 0)

# ================= SCHEMA — kiểm cấu trúc (mục 2.1) trước khi chạy sensor =======
SCHEMA_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                            "..", "..", "schemas", "qtcn-seed.schema.json"))

def run_schema(seed, rpt, label):
    """Guides thi hành bằng máy: dữ liệu lệch cấu trúc không tồn tại được.
    Dùng jsonschema (draft 2020-12) nếu có; fallback kiểm tối thiểu không phụ thuộc."""
    kind = seed.get("schema")
    if kind == "qtcn-seed-merged/v1":
        rpt.add("SCHEMA", "INFO", label, "seed gộp (merged/v1) — structural check hình thức chỉ áp cho qtcn-seed/v1")
        return
    if kind != "qtcn-seed/v1":
        rpt.add("SCHEMA", "FAIL", label, "trường schema = %r (phải là 'qtcn-seed/v1')" % (kind,))
        return
    try:
        import jsonschema
        with open(SCHEMA_PATH, encoding="utf-8-sig") as f:
            sch = json.load(f)
        errs = sorted(jsonschema.Draft202012Validator(sch).iter_errors(seed),
                      key=lambda e: list(e.absolute_path))
        for e in errs[:30]:
            where = "/".join(str(x) for x in e.absolute_path) or "(gốc)"
            rpt.add("SCHEMA", "FAIL", "%s/%s" % (label, where), e.message)
        if len(errs) > 30:
            rpt.add("SCHEMA", "FAIL", label, "… và %d lỗi cấu trúc nữa" % (len(errs) - 30))
        return
    except ImportError:
        rpt.add("SCHEMA", "INFO", label, "thiếu jsonschema (pip install jsonschema) — dùng kiểm tối thiểu")
    except FileNotFoundError:
        rpt.add("SCHEMA", "WARNING", label, "không thấy %s — dùng kiểm tối thiểu" % SCHEMA_PATH)
    # --- fallback tối thiểu, không phụ thuộc thư viện ---
    allowed = {"schema", "engine", "freecad_version", "product", "source", "bom",
               "consumables", "relationships", "flags", "validation", "_note"}
    for k in seed:
        if k not in allowed:
            rpt.add("SCHEMA", "FAIL", label, "trường lạ cấp gốc: %r (additionalProperties=false)" % k)
    if not isinstance(seed.get("bom"), list) or not seed["bom"]:
        rpt.add("SCHEMA", "FAIL", label, "bom phải là mảng ≥ 1 phần tử")
        return
    for i, p in enumerate(seed["bom"]):
        for req in ("vt", "name", "qty", "material", "specs"):
            if req not in p:
                rpt.add("SCHEMA", "FAIL", "%s/bom[%d]" % (label, i), "thiếu khóa bắt buộc %r" % req)

# =========================== LỚP S1 — bất biến vật lý ===========================
def run_s1(seed, catalog, rpt, label):
    bom = seed.get("bom") or []
    if not bom:
        rpt.add("S1-07", "FAIL", label, "seed không có dòng BOM nào")
        return
    env = ((seed.get("product") or {}).get("principal_particulars") or {}).get("envelope_mm")
    env_dims = sorted([env["L"], env["W"], env["H"]]) if env else None
    total_declared = (seed.get("product") or {}).get("total_mass_kg")
    sum_mass, n_mass = 0.0, 0

    for p in bom:
        f = fields(p)
        w = "%s/%s" % (label, f["name"])

        # --- S1-07: hữu hạn, dương; qty ≥ 1 (trường THIẾU -> WARNING, có mà sai -> FAIL)
        for key in ("mass", "vol_cm3", "area_cm2"):
            v = f[key]
            if v is None:
                rpt.add("S1-07", "WARNING", w, "thiếu trường %s (bổ sung qua merge/BOM)" % key)
            elif bad_num(v):
                rpt.add("S1-07", "FAIL", w, "%s = %r (phải là số dương hữu hạn)" % (key, v))
        if f["qty"] is None or (isinstance(f["qty"], (int, float)) and f["qty"] < 1):
            rpt.add("S1-07", "FAIL", w, "qty = %r (phải ≥ 1)" % (f["qty"],))

        # --- S1-02: vật liệu thuộc danh mục duyệt
        mat = f["material"]
        ent = material_entry(mat, catalog)
        if not mat or str(mat).startswith("["):
            rpt.add("S1-02", "FAIL", w, "thiếu vật liệu (%r)" % (mat,))
        elif ent is None:
            rpt.add("S1-02", "FAIL", w, "vật liệu %r NGOÀI danh mục duyệt" % mat)
        elif f["assumed"] or f["src"] in ("name_rule", "default"):
            rpt.add("S1-02", "WARNING", w,
                    "vật liệu/ρ suy đoán (source=%s) — đưa vào kiểm mẫu G2" % (f["src"] or "assumed"))

        # ρ dùng cho S1-01/08: ưu tiên ρ ghi trong seed, đối chiếu danh mục (lệch >2% -> WARNING)
        rho = f["rho"] or (ent["density_g_cm3"] if ent else None)
        if f["rho"] and ent and abs(f["rho"] - ent["density_g_cm3"]) / ent["density_g_cm3"] > 0.02:
            rpt.add("S1-02", "WARNING", w, "ρ trong seed (%.3g) lệch danh mục (%.3g g/cm³)"
                    % (f["rho"], ent["density_g_cm3"]))

        # --- S1-01 + S1-08: mass ≈ V×ρ; lệch đúng hệ số 10/1000/10⁶ -> nghi nhầm đơn vị
        if f["mass"] and f["vol_cm3"] and rho and not bad_num(f["mass"]) and not bad_num(f["vol_cm3"]):
            m_ref = f["vol_cm3"] * rho / 1000.0          # kg
            rel = abs(f["mass"] - m_ref) / f["mass"]
            if rel > 0.02:
                unit_bug = None
                for k in (10.0, 100.0, 1000.0, 1e6, 0.1, 0.01, 0.001, 1e-6):
                    if m_ref > 0 and abs(f["mass"] * k - m_ref) / m_ref <= 0.05:
                        unit_bug = k; break
                if unit_bug:
                    rpt.add("S1-08", "FAIL", w, "nghi NHẦM ĐƠN VỊ hệ số %g: mass=%.4g kg nhưng V×ρ=%.4g kg"
                            % (unit_bug, f["mass"], m_ref), {"factor": unit_bug})
                else:
                    rpt.add("S1-01", "FAIL", w, "mass=%.4g kg lệch V×ρ=%.4g kg (%.1f%% > 2%%)"
                            % (f["mass"], m_ref, rel * 100), {"rel_pct": round(rel * 100, 2)})

        # --- S1-05: đẳng chu — A ≥ (36π·V²)^(1/3) (đơn vị cm nhất quán)
        if f["area_cm2"] and f["vol_cm3"] and not bad_num(f["area_cm2"]) and not bad_num(f["vol_cm3"]):
            a_min = (36.0 * math.pi * f["vol_cm3"] ** 2) ** (1.0 / 3.0)
            if f["area_cm2"] < a_min * 0.99:
                rpt.add("S1-05", "FAIL", w, "area=%.4g cm² < cận cầu %.4g cm² — thể tích/diện tích mâu thuẫn"
                        % (f["area_cm2"], a_min))

        # --- S1-06: V ≤ thể tích bao hình
        if f["vol_cm3"] and f["bbox"] and all(f["bbox"]):
            vbox = f["bbox"][0] * f["bbox"][1] * f["bbox"][2] / 1000.0    # mm³ -> cm³
            if f["vol_cm3"] > vbox * 1.005:
                rpt.add("S1-06", "FAIL", w, "volume=%.4g cm³ > bao hình %.4g cm³" % (f["vol_cm3"], vbox))

        # --- S1-03: bao chi tiết ⊆ bao assembly + 1 mm (so theo chiều đã sắp — part có thể xoay)
        if env_dims and f["bbox"] and all(f["bbox"]):
            pd = sorted(f["bbox"])
            for i in range(3):
                if pd[i] > env_dims[i] + 1.0:
                    rpt.add("S1-03", "FAIL", w, "bbox part %.1f mm vượt bao assembly %.1f mm (+1 mm)"
                            % (pd[i], env_dims[i]))
                    break

        m_line = f["total_mass"] if f["total_mass"] is not None else (
            f["mass"] * f["qty"] if (f["mass"] and isinstance(f["qty"], (int, float))) else None)
        if m_line:
            sum_mass += m_line; n_mass += 1

    # --- S1-04: Σ mass chi tiết ≈ mass assembly (chỉ khi seed khai total và đủ mass)
    if total_declared and n_mass == len(bom):
        rel = abs(sum_mass - total_declared) / total_declared
        if rel > 0.03:
            rpt.add("S1-04", "FAIL", label, "Σ mass part = %.3f kg lệch total_mass_kg = %.3f kg (%.1f%% > 3%%)"
                    % (sum_mass, total_declared, rel * 100))

    # --- S4-03: chống thiếu sót — số thực thể nguồn vs Σ qty seed
    src = seed.get("source") or {}
    solid_n = src.get("solid_parts")
    if isinstance(solid_n, (int, float)):
        qty_sum = sum(p.get("qty") or 0 for p in bom)
        if qty_sum != solid_n:
            rpt.add("S4-03", "WARNING", label, "Σ qty seed = %s ≠ số solid nguồn = %s — rà lỗi THIẾU SÓT"
                    % (qty_sum, solid_n))

    # --- Truy vết (mục 2.1): thiếu hash/version/operator -> INFO (adapter mới bắt buộc ghi)
    for k in ("sha256", "extracted_at", "operator"):
        if k not in src:
            rpt.add("TRACE", "INFO", label, "source.%s chưa có (seed từ adapter đời trước)" % k)

# ==================== LỚP S2 — kiểm chéo 2 nguồn độc lập =======================
def match_parts(a_bom, b_bom):
    """Khớp tên chuẩn hóa; fallback mờ (cùng token đầu + ratio ≥ 0.75)."""
    A = {norm(fields(p)["name"]): p for p in a_bom}
    B = {norm(fields(p)["name"]): p for p in b_bom}
    pairs, used_b = [], set()
    for ka, pa in A.items():
        if ka in B:
            pairs.append((pa, B[ka])); used_b.add(ka); continue
        best, best_r = None, 0.0
        for kb in B:
            if kb in used_b or not ka or not kb or ka.split()[0] != kb.split()[0]:
                continue
            r = difflib.SequenceMatcher(None, ka, kb).ratio()
            if r > best_r:
                best, best_r = kb, r
        if best and best_r >= 0.75:
            pairs.append((pa, B[best])); used_b.add(best)
    only_a = [fields(p)["name"] for k, p in A.items()
              if all(p is not pa for pa, _ in pairs)]
    only_b = [fields(p)["name"] for k, p in B.items() if k not in used_b]
    return pairs, only_a, only_b

def run_s2(seed_a, seed_b, rpt, la, lb):
    pairs, only_a, only_b = match_parts(seed_a.get("bom") or [], seed_b.get("bom") or [])
    rpt.add("S2", "INFO", "%s×%s" % (la, lb), "khớp %d cặp; chỉ-%s: %d; chỉ-%s: %d"
            % (len(pairs), la, len(only_a), lb, len(only_b)))
    for name in only_a + only_b:
        rpt.add("S2-MATCH", "WARNING", name, "chỉ có ở MỘT nguồn — đầu mối lỗi thiếu sót (rà G2)")
    for pa, pb in pairs:
        fa, fb = fields(pa), fields(pb)
        w = "%s↔%s" % (fa["name"], fb["name"])
        assumed = fa["assumed"] or fb["assumed"]
        # S2-01: khối lượng đơn chiếc
        if fa["mass"] and fb["mass"]:
            rel = abs(fa["mass"] - fb["mass"]) / max(fa["mass"], fb["mass"])
            if assumed:      # một đường đoán ρ -> lệch đo sai số ρ, không phải lỗi trích
                if rel > 0.10:
                    rpt.add("S2-01", "WARNING", w, "mass lệch %.1f%% (ρ giả định — nới ngưỡng 10%%): %.4g vs %.4g kg"
                            % (rel * 100, fa["mass"], fb["mass"]))
            elif rel > 0.005:
                rpt.add("S2-01", "FAIL", w, "mass lệch %.2f%% > 0,5%%: %.4g vs %.4g kg"
                        % (rel * 100, fa["mass"], fb["mass"]))
        # S2-02: thể tích
        if fa["vol_cm3"] and fb["vol_cm3"]:
            rel = abs(fa["vol_cm3"] - fb["vol_cm3"]) / max(fa["vol_cm3"], fb["vol_cm3"])
            if rel > 0.005:
                rpt.add("S2-02", "FAIL", w, "volume lệch %.2f%% > 0,5%%" % (rel * 100))
        # S2-03: bao hình
        if fa["bbox"] and fb["bbox"] and all(fa["bbox"]) and all(fb["bbox"]):
            da, db = sorted(fa["bbox"]), sorted(fb["bbox"])
            worst = max(abs(x - y) for x, y in zip(da, db))
            if worst > 0.2:
                rpt.add("S2-03", "FAIL", w, "bbox lệch %.2f mm > 0,2 mm" % worst)
        # QTY (BOM Inventor là chuẩn; STEP hay lệch 1-instance)
        if fa["qty"] and fb["qty"] and fa["qty"] != fb["qty"]:
            rpt.add("S2-QTY", "WARNING", w, "QTY lệch: %s vs %s (lấy BOM làm chuẩn)" % (fa["qty"], fb["qty"]))

# ==================== LỚP S3 — sanity theo lịch sử =============================
def run_s3(seeds, hist_path, rpt, update):
    hist = {}
    if os.path.exists(hist_path):
        with open(hist_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    e = json.loads(line)
                    hist.setdefault(e["key"], []).append(float(e["mass_kg"]))
                except Exception:
                    continue
    def median(xs):
        xs = sorted(xs); n = len(xs)
        return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2.0
    new_lines = []
    for label, seed in seeds:
        for p in seed.get("bom") or []:
            f = fields(p)
            if not f["mass"]:
                continue
            key = norm(f["name"])
            xs = hist.get(key, [])
            if xs:
                med = median(xs)
                rel = abs(f["mass"] - med) / med if med else 0
                lv = "WARNING" if len(xs) >= 20 else "INFO"   # <20 mẫu: chưa đủ hiệu lực (mục 3.3)
                if rel > 0.30:
                    rpt.add("S3-01", lv, "%s/%s" % (label, f["name"]),
                            "mass %.4g kg lệch %.0f%% so median lịch sử %.4g kg (n=%d)"
                            % (f["mass"], rel * 100, med, len(xs)))
            new_lines.append({"key": key, "mass_kg": f["mass"], "material": f["material"],
                              "product": (seed.get("product") or {}).get("name")})
    if update:
        if rpt.count("FAIL"):
            rpt.add("S3", "INFO", hist_path, "KHÔNG ghi history: lô có FAIL (chỉ nuôi S3 bằng dữ liệu đã qua gate)")
        else:
            with open(hist_path, "a", encoding="utf-8") as f:
                for e in new_lines:
                    f.write(json.dumps(e, ensure_ascii=False) + "\n")
            rpt.add("S3", "INFO", hist_path, "đã ghi %d dòng vào history" % len(new_lines))

# ============ LỚP S4 — determinism / diff  +  Gate G3 golden set ===============
def deep_diff(a, b, path=""):
    """So 2 cấu trúc JSON, bỏ trường volatile; trả list mô tả khác biệt."""
    diffs = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k in VOLATILE_KEYS:
                continue
            if k not in a or k not in b:
                diffs.append("%s.%s: chỉ có ở %s" % (path, k, "B" if k not in a else "A"))
            else:
                diffs += deep_diff(a[k], b[k], "%s.%s" % (path, k))
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            diffs.append("%s: độ dài %d vs %d" % (path, len(a), len(b)))
        for i, (x, y) in enumerate(zip(a, b)):
            diffs += deep_diff(x, y, "%s[%d]" % (path, i))
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if a != b:
            diffs.append("%s: %r vs %r" % (path, a, b))
    elif a != b:
        diffs.append("%s: %r vs %r" % (path, a, b))
    return diffs

def run_determinism(a, b, rpt):
    diffs = deep_diff(a, b)
    if diffs:
        rpt.add("S4-01", "FAIL", "determinism", "2 lần chạy KHÁC nhau (%d chỗ) — script không tất định"
                % len(diffs), {"diffs": diffs[:50]})
    else:
        rpt.add("S4-01", "PASS", "determinism", "2 lần chạy trùng khớp (đã bỏ trường volatile)")

def run_diff(old, new, rpt):
    """S4-02 — diff giữa 2 revision; người duyệt đối chiếu với ECN/ghi chú revision."""
    pairs, only_old, only_new = match_parts(old.get("bom") or [], new.get("bom") or [])
    for n in only_old:
        rpt.add("S4-02", "WARNING", n, "part BIẾN MẤT ở revision mới")
    for n in only_new:
        rpt.add("S4-02", "WARNING", n, "part MỚI xuất hiện ở revision mới")
    for po, pn in pairs:
        fo, fn = fields(po), fields(pn)
        if fo["mass"] and fn["mass"]:
            rel = abs(fn["mass"] - fo["mass"]) / fo["mass"]
            if rel > 0.01:
                rpt.add("S4-02", "WARNING", fn["name"], "mass đổi %.1f%%: %.4g → %.4g kg — khớp với ECN không?"
                        % (rel * 100, fo["mass"], fn["mass"]))
        if fo["qty"] != fn["qty"]:
            rpt.add("S4-02", "WARNING", fn["name"], "QTY đổi: %s → %s" % (fo["qty"], fn["qty"]))
    if not any(e["rule"] == "S4-02" for e in rpt.entries):
        rpt.add("S4-02", "PASS", "diff", "không có thay đổi vượt ngưỡng giữa 2 revision")

def golden_compare(exp, act, path=""):
    """So expected/actual trong tolerance: số ±0,5% (kích thước ±0,1 mm), chuỗi khớp tuyệt đối."""
    diffs = []
    if isinstance(exp, dict) and isinstance(act, dict):
        for k in sorted(exp):
            if k in VOLATILE_KEYS or k == "source":
                continue
            if k not in act:
                diffs.append("%s.%s: thiếu ở actual" % (path, k))
            else:
                diffs += golden_compare(exp[k], act[k], "%s.%s" % (path, k))
    elif isinstance(exp, list) and isinstance(act, list):
        if len(exp) != len(act):
            diffs.append("%s: %d phần tử vs %d" % (path, len(exp), len(act)))
        for i, (x, y) in enumerate(zip(exp, act)):
            diffs += golden_compare(x, y, "%s[%d]" % (path, i))
    elif isinstance(exp, (int, float)) and isinstance(act, (int, float)):
        tol = 0.1 if path.endswith("_mm") or "bbox" in path else abs(exp) * 0.005
        if abs(exp - act) > max(tol, 1e-9):
            diffs.append("%s: expected %r vs actual %r" % (path, exp, act))
    elif exp != act:
        diffs.append("%s: expected %r vs actual %r" % (path, exp, act))
    return diffs

def run_golden(root, rpt):
    cases = []
    for dirpath, _dirs, files in os.walk(root):
        if "expected-seed.json" in files:
            cases.append(dirpath)
    if not cases:
        rpt.add("G3", "FAIL", root, "không tìm thấy case nào (cần expected-seed.json trong mỗi case)")
        return
    for c in sorted(cases):
        exp_p = os.path.join(c, "expected-seed.json")
        act_p = os.path.join(c, "actual-seed.json")
        name = os.path.relpath(c, root)
        if not os.path.exists(act_p):
            rpt.add("G3", "FAIL", name, "thiếu actual-seed.json (chạy adapter trên source/ rồi copy vào case)")
            continue
        diffs = golden_compare(load(exp_p), load(act_p))
        if diffs:
            rpt.add("G3", "FAIL", name, "lệch đáp án %d chỗ" % len(diffs), {"diffs": diffs[:30]})
        else:
            rpt.add("G3", "PASS", name, "khớp đáp án trong dung sai")
    n_fail = sum(1 for e in rpt.entries if e["rule"] == "G3" and e["level"] == "FAIL")
    rpt.add("G3", "INFO", root, "golden set: %d/%d case đạt — %s"
            % (len(cases) - n_fail, len(cases),
               "ĐƯỢC phát hành" if n_fail == 0 else "CẤM phát hành phiên bản extractor này"))

# ==================================== CLI ======================================
def main():
    ap = argparse.ArgumentParser(description="Sensor + gate cho qtcn-seed/v1 (WX-QT-EXTRACT-SENSOR-01)")
    ap.add_argument("--seed", action="append", default=[], help="seed cần kiểm S1 (lặp lại được)")
    ap.add_argument("--cross", nargs=2, metavar=("A", "B"), help="kiểm chéo 2 seed từ 2 nguồn độc lập (S2)")
    ap.add_argument("--history", default=None, help="history.jsonl cho S3")
    ap.add_argument("--update-history", action="store_true")
    ap.add_argument("--determinism", nargs=2, metavar=("A", "B"), help="2 seed từ 2 lần chạy cùng nguồn (S4-01)")
    ap.add_argument("--diff", nargs=2, metavar=("OLD", "NEW"), help="diff giữa 2 revision (S4-02)")
    ap.add_argument("--golden", default=None, help="thư mục golden set (Gate G3)")
    ap.add_argument("--materials", default=None, help="JSON danh mục vật liệu duyệt")
    ap.add_argument("--report", default=None, help="đường dẫn report (mặc định <seed>.validation.json)")
    ap.add_argument("--release", action="store_true",
                    help="chế độ phát hành lô: BẮT BUỘC kiểm chéo 2 nguồn (--cross) và đủ trường truy vết")
    a = ap.parse_args()

    if not (a.seed or a.cross or a.determinism or a.diff or a.golden):
        ap.print_help(); sys.exit(3)
    catalog = DEFAULT_MATERIALS
    if a.materials:
        catalog = load(a.materials)

    rpt = Report()
    seeds = []
    try:
        for p in a.seed:
            seeds.append((os.path.splitext(os.path.basename(p))[0], load(p)))
        for label, seed in seeds:
            run_schema(seed, rpt, label)
            run_s1(seed, catalog, rpt, label)
        if a.cross:
            sa, sb = load(a.cross[0]), load(a.cross[1])
            run_s2(sa, sb, rpt, os.path.basename(a.cross[0]), os.path.basename(a.cross[1]))
        if a.history and seeds:
            run_s3(seeds, a.history, rpt, a.update_history)
        if a.determinism:
            run_determinism(load(a.determinism[0]), load(a.determinism[1]), rpt)
        if a.diff:
            run_diff(load(a.diff[0]), load(a.diff[1]), rpt)
        if a.golden:
            run_golden(a.golden, rpt)
        # --- chế độ phát hành: bất biến "tự chấm mình" không đủ — bắt buộc 2 đường độc lập
        if a.release:
            if not a.cross:
                rpt.add("RELEASE", "FAIL", "release",
                        "phát hành lô BẮT BUỘC kiểm chéo 2 nguồn độc lập (--cross BOM×STEP) — "
                        "S1 trên seed đơn có rule tự-chấm-mình (mass và V×ρ cùng một script tính)")
            for e in rpt.entries:            # truy vết thiếu: INFO -> WARNING khi phát hành
                if e["rule"] == "TRACE" and e["level"] == "INFO":
                    e["level"] = "WARNING"
                    e["msg"] += " — bắt buộc bổ sung trước phát hành"
    except FileNotFoundError as e:
        sys.stderr.write("[!] Không thấy file: %s\n" % e); sys.exit(3)
    except json.JSONDecodeError as e:
        sys.stderr.write("[!] JSON hỏng: %s\n" % e); sys.exit(3)

    # ----- report (biểu mẫu F01) + in tóm tắt -----
    first = a.seed[0] if a.seed else (a.cross or a.determinism or a.diff or [a.golden])[0]
    rep_path = a.report or (os.path.splitext(first)[0] + ".validation.json")
    inputs = {"seeds": a.seed, "cross": a.cross, "determinism": a.determinism,
              "diff": a.diff, "golden": a.golden}
    out = rpt.dump(rep_path, {"inputs": {k: v for k, v in inputs.items() if v},
                              "validated": rpt.verdict() != "FAIL"})
    print("Wrote %s" % rep_path)
    print("VERDICT: %s  (FAIL=%d WARNING=%d INFO=%d)"
          % (out["verdict"], rpt.count("FAIL"), rpt.count("WARNING"), rpt.count("INFO")))
    for e in rpt.entries:
        if e["level"] in ("FAIL", "WARNING"):
            print("  [%s] %s @ %s — %s" % (e["level"], e["rule"], e["where"], e["msg"]))
    if out["verdict"] == "WARNING":
        print("  → Gate G2: đo tay 3–5 giá trị, ưu tiên các dòng WARNING ở trên + chi tiết giá trị lớn nhất.")
    if out["verdict"] == "FAIL":
        print("  → Gate G1 CHẶN: seed không validated, pipeline 5 đầu ra từ chối nhận.")
    sys.exit({"PASS": 0, "WARNING": 1, "FAIL": 2}[out["verdict"]])

if __name__ == "__main__":
    main()
