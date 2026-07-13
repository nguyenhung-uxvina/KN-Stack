#!/usr/bin/env python3
"""qtcn_to_json.py — Chuyển một QTCN Markdown (bản tổng thể / chi tiết) sang JSON kiểm tra quy trình.

Hiện thực cờ `--json` của skill `qtcn` (COD: Offload — bóc tách xác định bằng code).
Đọc file QTCN.md có cấu trúc chuẩn (# PHẦN A/B/C, ## NGUYÊN CÔNG <id>, ### I/II/III) và
xuất JSON theo schema references §E, gồm phần cốt lõi `checkpoints[]` — **tự động khai thác
mọi tiêu chí định lượng** (lực siết, dung sai, Δ đường chéo, khoảng cách, điện áp, góc, IP)
từ mục I. Yêu cầu kỹ thuật để dùng cho verify/inspection/audit về sau.

Dùng:
    python qtcn_to_json.py --in QTCN-<sp>.md [--out <dir>] [--name <slug>] [--scope full|B] [--cad]

Không cần thư viện ngoài. Exit: 0 ok | 2 lỗi đầu vào.
"""
import argparse
import json
import os
import re
import sys


def read(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def first_int(s):
    m = re.search(r"\d+", s or "")
    return int(m.group()) if m else None


# --- checkpoint miner: rút tiêu chí định lượng từ text YCKT -------------------
def _param_of(text):
    t = text.lower()
    for kw, name in (
        ("thẳng đứng", "Độ thẳng đứng"),
        ("đường chéo", "Sai lệch đường chéo (vuông góc)"),
        ("chéo", "Sai lệch đường chéo (vuông góc)"),
        ("mô-men", "Mô-men siết"),
        ("siết", "Mô-men siết"),
        ("điện áp", "Điện áp ắc quy"),
        ("ắc quy", "Điện áp ắc quy"),
        ("tâm", "Khoảng cách tâm"),
        ("chân", "Chiều cao chân mối hàn"),
        ("phẳng", "Độ phẳng"),
        ("cóc", "Khoảng cách cóc kẹp cáp"),
        ("võng", "Độ võng dây chằng"),
        ("khoảng cách", "Khoảng cách"),
    ):
        if kw in t:
            return name
    return "Thông số kỹ thuật"


def mine_checkpoints(steps):
    """steps: list of {step, text} -> list of checkpoint dicts (deduped)."""
    out, seen = [], set()

    def add(param, nominal, tol, unit, phrase, step):
        key = (param, nominal, tol, unit)
        if key in seen:
            return
        seen.add(key)
        cp = {"param": param, "nominal": nominal, "unit": unit,
              "method": None, "criterion": phrase.strip(), "source_step": step, "auto": True}
        if tol is not None:
            cp["tol"] = tol
        out.append(cp)

    for s in steps:
        text, step = s["text"], s["step"]
        # 1) mô-men siết: 45 ÷ 55 Nm
        for m in re.finditer(r"(\d+(?:[.,]\d+)?)\s*[÷\-–]\s*(\d+(?:[.,]\d+)?)\s*Nm", text):
            add("Mô-men siết", "%s–%s" % (m.group(1), m.group(2)), None, "Nm", m.group(0), step)
        # 2) điện áp: 12 ÷ 12,8 V
        for m in re.finditer(r"(\d+(?:[.,]\d+)?)\s*[÷\-–]\s*(\d+(?:[.,]\d+)?)\s*V\b", text):
            add("Điện áp ắc quy", "%s–%s" % (m.group(1), m.group(2)), None, "V", m.group(0), step)
        # 3) danh nghĩa ± dung sai: 1530 ± 10 mm
        for m in re.finditer(r"(\d+(?:[.,]\d+)?)\s*±\s*(\d+(?:[.,]\d+)?)\s*mm", text):
            add(_param_of(text), m.group(1), "±%s" % m.group(2), "mm", m.group(0), step)
        # 4) ± dung sai đứng riêng: ±1 mm
        for m in re.finditer(r"(?<![\d])±\s*(\d+(?:[.,]\d+)?)\s*mm", text):
            add(_param_of(text), "0", "±%s" % m.group(1), "mm", m.group(0), step)
        # 5) Δ đường chéo: Δ ≤ 5 mm
        for m in re.finditer(r"Δ\s*[≤=]?\s*(\d+(?:[.,]\d+)?)\s*mm", text):
            add("Sai lệch đường chéo (vuông góc)", "≤ %s" % m.group(1), None, "mm", m.group(0), step)
        # 6) ≤/≥ giá trị + đơn vị (không phải Nm → không gán nhãn mô-men)
        for m in re.finditer(r"([≤≥])\s*(\d+(?:[.,]\d+)?)\s*(mm|°|V|kg|m|mm/m)\b", text):
            p = _param_of(text)
            if p == "Mô-men siết":
                p = "Khoảng cách" if m.group(3) == "mm" else "Thông số kỹ thuật"
            add(p, "%s %s" % (m.group(1), m.group(2)), None, m.group(3), m.group(0), step)
        # 7) khoảng cách dải: 50 ÷ 80 mm / 200 ÷ 250 mm (đơn vị mm ⇒ khoảng cách, không phải mô-men)
        for m in re.finditer(r"(\d+)\s*[÷\-–]\s*(\d+)\s*mm", text):
            add("Khoảng cách", "%s–%s" % (m.group(1), m.group(2)), None, "mm", m.group(0), step)
        # 8) IP rating
        for m in re.finditer(r"IP\s?(\d{2})", text):
            add("Cấp bảo vệ chống nước", "IP%s" % m.group(1), None, None, m.group(0), step)
        # 9) góc: 0,5°
        for m in re.finditer(r"(\d+(?:[.,]\d+)?)\s*°", text):
            add(_param_of(text), m.group(1), None, "°", m.group(0), step)
    return out


def detect_core_rule(steps):
    for s in steps:
        t = s["text"]
        if re.search(r"ch[ưu]a\s+si[ếe]t|gá\s*l[ỏo]ng|tuy[ệe]t\s*đối", t, re.IGNORECASE):
            return t.strip()
    return None


# --- section III: materials + equipment --------------------------------------
_QTY_UNITS = r"cái|bộ|viên|cuộn|mét|m|chiếc|sợi|tấm|đoạn|tuýp|tuyp|lá|thanh|kg|gói|hộp|lít"


def _split_items(txt):
    """Tách item theo ';' hoặc ',' nhưng KHÔNG tách bên trong dấu ngoặc ()."""
    parts, buf, depth = [], "", 0
    for ch in txt:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        if depth == 0 and ch in ";,":
            parts.append(buf)
            buf = ""
        else:
            buf += ch
    if buf.strip():
        parts.append(buf)
    return [p for p in (x.strip(" .") for x in parts) if p]


def _parse_item(txt):
    txt = txt.strip(" .")
    m = re.match(r"(.+?):\s*(\d+.*)$", txt)            # "Tên: 06 bộ"
    if m:
        return {"name": m.group(1).strip(), "qty": m.group(2).strip()}
    m = re.search(r"\s(\d+\s*(?:%s)\b.*)$" % _QTY_UNITS, txt, re.IGNORECASE)  # "Tên 06 bộ"
    if m:
        return {"name": txt[:m.start()].strip(), "qty": m.group(1).strip()}
    return {"name": txt, "qty": None}


def parse_iv(lines):
    """Mục IV. Minh họa → cad_illustration (references §E)."""
    d = {}
    for ln in lines:
        m = re.match(r"[-*]\s*\*\*(.+?):\*\*\s*(.+)$", ln.strip())
        if m:
            d[m.group(1).strip().lower()] = m.group(2).strip()
    callout = d.get("callout bắt buộc", "")
    return {
        "required": True,
        "figure_id": d.get("mã hình"),
        "view_type": d.get("loại hình"),
        "shows": d.get("thể hiện"),
        "callouts": [c.strip() for c in re.split(r";\s*", callout) if c.strip()],
        "source_drawing": d.get("nguồn"),
    }


def parse_iii(lines):
    materials, equipment, mode = [], [], "equipment"
    head = " ".join(lines[:1]).lower()
    if "nguyên" in head or "vật liệu" in head:
        mode = "materials"
    for ln in lines[1:]:
        s = ln.strip()
        if not s:
            continue
        mh = re.match(r"[*\-]+\s*\*\*(.+?):?\*\*\s*(.*)$", s)
        if mh:
            label = mh.group(1).lower()
            rest = mh.group(2).strip()
            mode = "materials" if ("vật liệu" in label or "nguyên" in label) else "equipment"
            for it in _split_items(rest):             # inline: "**Thiết bị:** a 02 cái; b (x,y) 01 cái"
                (materials if mode == "materials" else equipment).append(_parse_item(it))
            continue
        mnum = re.match(r"\d+\.\s+(.+)$", s)           # numbered: "1. Thước cuộn: 01 cái"
        if mnum:
            (materials if mode == "materials" else equipment).append(_parse_item(mnum.group(1)))
    return materials, equipment


# --- main parse --------------------------------------------------------------
def parse_qtcn(text):
    lines = text.split("\n")
    doc = {"product": {}, "standards": [], "general_specs": {}, "bom": [],
           "operations": [], "safety": []}

    # header meta: > **Key:** value
    for ln in lines[:40]:
        m = re.match(r">\s*\*\*(.+?):\*\*\s*(.+)$", ln)
        if m:
            k, v = m.group(1).strip().lower(), m.group(2).strip()
            if "ký hiệu sản phẩm" in k or k == "ký hiệu":
                doc["product"]["code"] = v
            elif "tên gọi" in k:
                doc["product"]["name"] = v
    # title lines
    titles = [l[2:].strip() for l in lines[:6] if l.startswith("# ")]
    if titles:
        doc["product"].setdefault("name", titles[-1])
        doc["product"]["title"] = " — ".join(titles)

    # walk sections & operations
    principal, standards, bom = {}, [], []
    section = None
    phase = None
    op = None
    sub = None            # I/II/III
    sub_lines = []

    def flush_sub():
        nonlocal sub, sub_lines, op
        if op is None or sub is None:
            sub, sub_lines = None, []
            return
        if sub == "I":
            steps, cur = [], None
            for ln in sub_lines:
                s = ln.strip()
                if not s:
                    continue
                m = re.match(r"(\d+)\.\s+(.+)$", s)
                if m:                                  # bước đánh số mới
                    cur = {"step": len(steps) + 1, "text": m.group(2).strip()}
                    steps.append(cur)
                elif cur is not None:                  # gạch đầu dòng con / dòng gãy → gộp vào bước
                    cur["text"] += " " + re.sub(r"^[-*•]\s*", "", s)
            op["tech_requirements"] = steps
            op["core_rule"] = detect_core_rule(steps)
            op["checkpoints"] = mine_checkpoints(steps)
        elif sub == "II":
            blob = " ".join(l.strip() for l in sub_lines)

            def field(pat):
                m = re.search(pat, blob)
                return m.group(1).strip(" .") if m else None
            op["labor"] = {
                "grade": field(r"\*\*Bậc thợ:?\*\*\s*([^·*\n]+)"),
                "time_min": first_int(field(r"\*\*Định mức[^*]*?:?\*\*\s*([^·*\n]+)") or ""),
                "location": field(r"\*\*Nơi thực hiện:?\*\*\s*([^·*\n]+)"),
            }
        elif sub == "III":
            mats, equip = parse_iii(sub_lines)
            op["materials"], op["equipment"] = mats, equip
        elif sub == "IV":
            op["cad_illustration"] = parse_iv(sub_lines)
        sub, sub_lines = None, []

    def flush_op():
        nonlocal op
        if op is not None:
            # vt_refs from name + steps
            blob = op["name"] + " " + " ".join(s["text"] for s in op.get("tech_requirements", []))
            op["vt_refs"] = sorted(set(re.findall(r"VT\d+", blob)),
                                   key=lambda x: int(x[2:]))
            op.setdefault("cad_illustration", {"required": False})
            doc["operations"].append(op)
        op = None

    i = 0
    while i < len(lines):
        ln = lines[i]
        # phase marker
        mp = re.match(r"#\s+PHẦN\s+([ABC])", ln)
        if mp:
            flush_sub(); flush_op(); phase = mp.group(1); section = None
            i += 1; continue
        # numbered section (## 2. ...)
        ms = re.match(r"##\s+(\d+)\.\s+(.+)$", ln)
        if ms:
            flush_sub(); flush_op(); section = ms.group(2).strip().lower()
            i += 1; continue
        # operation header
        mo = re.match(r"##\s+NGUYÊN CÔNG\s+([A-C]?\d+)\s*:\s*(.+)$", ln)
        if mo:
            flush_sub(); flush_op()
            op = {"id": mo.group(1), "phase": phase or mo.group(1)[0],
                  "name": mo.group(2).strip()}
            section = None
            i += 1; continue
        # sub-section I/II/III
        msub = re.match(r"###\s+([IVX]+)\.", ln)
        if msub and op is not None:
            flush_sub(); sub = {"I": "I", "II": "II", "III": "III"}.get(msub.group(1), msub.group(1))
            i += 1; continue
        if sub is not None:
            sub_lines.append(ln)
        # collect section-level data
        if section:
            if "viện dẫn" in section:
                mb = re.match(r"[-*]\s+(.+)$", ln.strip())
                if mb:
                    standards.append(mb.group(1).strip())
            if "thông số" in section and "|" in ln and "---" not in ln:
                cells = [c.strip() for c in ln.strip().strip("|").split("|")]
                if len(cells) >= 2 and cells[0].lower() not in ("thông số", ""):
                    principal[cells[0]] = cells[1]
            if ("bảng kê" in section or "bom" in section) and "|" in ln and "---" not in ln:
                cells = [c.strip() for c in ln.strip().strip("|").split("|")]
                if len(cells) >= 5 and cells[0].lower() not in ("pos", ""):
                    bom.append({"pos": cells[0], "drawing_no": cells[1],
                                "name": cells[2], "qty": cells[3], "material": cells[4]})
        i += 1
    flush_sub(); flush_op()

    doc["product"]["principal_particulars"] = principal
    doc["standards"] = standards
    doc["bom"] = bom

    # general_specs mined from whole text + operations
    gs = {}
    mt = re.search(r"±IT14/2", text)
    if mt:
        gs["default_tolerance"] = "±IT14/2"
    if re.search(r"IP\s?67", text):
        gs["ip_rating"] = "IP67"
    mv = re.search(r"(\d+(?:[.,]\d+)?)\s*[÷\-–]\s*(\d+(?:[.,]\d+)?)\s*V\b", text)
    if mv:
        gs["battery_voltage"] = "%s–%s V" % (mv.group(1), mv.group(2))
    # bolt → mô-men: đọc thẳng từ text thô (mỗi cặp M..×.. đạt a÷b Nm nằm trên 1 dòng)
    torque = {}
    for m in re.finditer(r"M(\d+)[×x]\d+[^\n]*?(\d+)\s*[÷\-–]\s*(\d+)\s*Nm", text):
        torque["M%s" % m.group(1)] = "%s–%s Nm" % (m.group(2), m.group(3))
    if torque:
        gs["torque"] = torque
    doc["general_specs"] = gs
    return doc


def main():
    try:  # legacy Windows consoles are cp1252; QTCN paths/text are Vietnamese
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="QTCN Markdown -> JSON kiểm tra quy trình")
    ap.add_argument("--in", dest="infile", required=True)
    ap.add_argument("--out", default=".")
    ap.add_argument("--name")
    ap.add_argument("--scope", choices=["full", "B"], default="full")
    ap.add_argument("--cad", action="store_true")
    args = ap.parse_args()

    if not os.path.isfile(args.infile):
        sys.stderr.write("[!] Không tìm thấy file: %s\n" % args.infile)
        sys.exit(2)

    doc = parse_qtcn(read(args.infile))
    doc["scope"] = args.scope
    doc["cad_included"] = bool(args.cad)
    if not args.cad:  # tôn trọng cờ: không --cad thì không xuất spec minh họa
        for o in doc["operations"]:
            o["cad_illustration"] = {"required": False}
    if args.scope == "B":
        doc["operations"] = [o for o in doc["operations"] if o.get("phase") in ("B", "C")]
    doc["process_summary"] = [
        {"seq": idx + 1, "id": o["id"], "name": o["name"],
         "grade": o.get("labor", {}).get("grade"),
         "time_min": o.get("labor", {}).get("time_min")}
        for idx, o in enumerate(doc["operations"])
    ]
    total = sum((o.get("labor", {}).get("time_min") or 0) for o in doc["operations"])
    n_cp = sum(len(o.get("checkpoints", [])) for o in doc["operations"])
    doc["totals"] = {"operations": len(doc["operations"]),
                     "time_min": total, "checkpoints": n_cp}

    name = args.name or re.sub(r"\.md$", "", os.path.basename(args.infile))
    os.makedirs(args.out, exist_ok=True)
    out_path = os.path.join(args.out, name + ".json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    sys.stdout.write(
        "[ok] scope=%s -> %s | %d operations, %d checkpoints, total %d min\n"
        % (args.scope, out_path, len(doc["operations"]), n_cp, total))


if __name__ == "__main__":
    main()
