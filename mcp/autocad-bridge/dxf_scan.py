"""Đọc DXF ngoại tuyến (ezdxf) — không cần mở AutoCAD, không ghi tệp. Dùng cho quét cả bộ hồ sơ."""
import csv
import logging
import re
from collections import Counter, defaultdict
from pathlib import Path

import ezdxf

from acad_text import (clean_mtext, in_title_region, is_balloon, is_title_block, name_matches_file,
                       parse_sl_label, render_dim_text, title_fields)

logging.getLogger("ezdxf").setLevel(logging.WARNING)

def _in_title(tb, x, y):
    return tb is not None and in_title_region(x, y, (tb.dxf.insert.x, tb.dxf.insert.y), tb.dxf.xscale)


def _texts(space):
    for e in space.query("TEXT MTEXT"):
        raw = e.text if e.dxftype() == "MTEXT" else e.dxf.text
        yield e.dxf.insert.x, e.dxf.insert.y, clean_mtext(raw)


def _title_block(msp):
    return next((i for i in msp.query("INSERT") if is_title_block(i.dxf.name)), None)


def _dim_rendered(doc, dim):
    """Chữ in trên giấy = chữ trong block hình học của kích thước; dự phòng = dựng lại từ override."""
    m = dim.get_measurement()
    blk = doc.blocks.get(dim.dxf.geometry) if dim.dxf.hasattr("geometry") else None
    if blk is not None:
        shown = " ".join(clean_mtext(x.text if x.dxftype() == "MTEXT" else x.dxf.text) for x in blk.query("TEXT MTEXT"))
        if shown.strip():
            return shown.strip(), m
    if isinstance(m, (int, float)):
        return render_dim_text(dim.dxf.get("text", ""), m), m
    return "", m


def _title(msp, texts):
    tb = _title_block(msp)
    if tb is None:
        return None, {}
    origin = (tb.dxf.insert.x, tb.dxf.insert.y)
    return tb, title_fields(texts, origin, tb.dxf.xscale or 1.0)


def file_index(name: str) -> str:
    """'4.1.2  khung do' → '4.1.2'; '4.cum do-tong lap' → '4'."""
    m = re.match(r"^\s*(\d+(?:\.\d+)*)", name)
    return m.group(1) if m else ""


def dxf_summary(path: str, max_holes_per_size: int = 50) -> dict:
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()
    texts = list(_texts(msp))
    tb, title = _title(msp, texts)
    labels, notes, balloons, other = [], [], [], []
    for x, y, t in texts:
        if not t or _in_title(tb, x, y):
            continue
        sl = parse_sl_label(t)
        if sl:
            labels.append({**sl, "at": [round(x, 1), round(y, 1)]})
        elif is_balloon(t):
            balloons.append(int(t))
        elif len(t) > 60:
            notes.append(t)
        else:
            other.append({"text": t, "at": [round(x, 1), round(y, 1)]})
    dims = []
    for d in msp.query("DIMENSION"):
        shown, m = _dim_rendered(doc, d)
        dims.append({"shown": shown, "geometry": round(m, 3) if isinstance(m, (int, float)) else None,
                     "at": [round(v, 1) for v in d.dxf.get("text_midpoint", d.dxf.defpoint)][:2]})
    holes = defaultdict(list)
    for c in msp.query("CIRCLE"):
        holes[round(2 * c.dxf.radius, 2)].append([round(c.dxf.center.x, 2), round(c.dxf.center.y, 2)])
    return {
        "file": Path(path).name, "index": file_index(Path(path).stem),
        "units": doc.header.get("$INSUNITS"), "title": title,
        "title_block": tb.dxf.name if tb is not None else None,
        "part_labels": labels, "balloons": sorted(set(balloons)), "notes": notes, "texts": other,
        "dimensions": dims,
        "holes": {f"Ø{k:g}": {"count": len(v), "centers": sorted(v)[:max_holes_per_size]} for k, v in sorted(holes.items())},
        "entity_counts": dict(Counter(e.dxftype() for e in msp)),
        "layers": dict(Counter(e.dxf.layer for e in msp)),
    }


def _index_key(idx: str):
    return [int(p) for p in idx.split(".")] if idx else [9999]


def scan_folder(folder: str, pattern: str = "*.dxf", csv_out: str = "") -> dict:
    """Quét mọi DXF: khung tên + nhãn SL/VL + bóng số. Trả bảng; ghi CSV nếu csv_out."""
    rows, errors = [], []
    for p in sorted(Path(folder).glob(pattern), key=lambda p: (_index_key(file_index(p.stem)), p.name)):
        try:
            doc = ezdxf.readfile(p)
        except Exception as e:  # noqa: BLE001 — một tệp hỏng không được chặn cả bộ
            errors.append({"file": p.name, "error": str(e)})
            continue
        msp = doc.modelspace()
        texts = list(_texts(msp))
        tb, title = _title(msp, texts)
        drawing = [(x, y, t) for x, y, t in texts if not _in_title(tb, x, y)]
        labels = [lb for lb in (parse_sl_label(t) for _, _, t in drawing) if lb]
        assembly = "tong lap" in p.stem.lower() or "tổng lắp" in p.stem.lower()
        if tb is None:
            warn = "không thấy khung tên trong modelspace"
        elif not any(title.values()):
            warn = "khung tên rỗng — chữ nằm trong block ẩn danh, công cụ chưa đọc được: đọc tay trên bản vẽ"
        elif not assembly and not name_matches_file(p.stem, title.get("name", "")):
            warn = "tên tệp ≠ tên khung tên — nghi khung tên chép từ tờ khác"
        else:
            warn = ""
        rows.append({
            "file": p.name, "index": file_index(p.stem), "assembly": assembly,
            **{k: title.get(k, "") for k in ("code", "name", "material", "mass", "scale", "sheet", "sheets")},
            "part_labels": "; ".join(f"SL{lb['qty']} {lb['material'] or '?'}" for lb in labels),
            "balloons": ",".join(str(b) for b in sorted({int(t) for _, _, t in drawing if is_balloon(t)})) if assembly else "",
            "warn": warn,
        })
    # nhiều tờ của cùng một chi tiết dùng chung mã là hợp lệ ⇒ chỉ báo khi cùng mã mà KHÁC tên
    names_by_code = defaultdict(set)
    for r in rows:
        if r["code"] and not r["assembly"]:
            names_by_code[r["code"]].add(r["name"])
    dup_codes = {c for c, names in names_by_code.items() if len(names) > 1}
    # cùng mã + cùng «tờ/số tờ» ở hai tệp ⇒ tệp trùng hoặc đánh số tờ sai
    files_by_sheet = defaultdict(list)
    for r in rows:
        if r["code"] and r["sheet"]:
            files_by_sheet[(r["code"], f'{r["sheet"]}/{r["sheets"]}')].append(r["file"])
    dup_sheets = [{"code": c, "sheet": s, "files": f} for (c, s), f in sorted(files_by_sheet.items()) if len(f) > 1]
    dup_sheet_files = {f for d in dup_sheets for f in d["files"]}

    def _add(r, msg):
        r["warn"] = (r["warn"] + "; " if r["warn"] else "") + msg

    for r in rows:
        if r["code"] in dup_codes and not r["assembly"]:
            _add(r, "mã trùng tờ khác")
        if r["file"] in dup_sheet_files:
            _add(r, "trùng số tờ với tệp khác")
    if csv_out and rows:
        with open(csv_out, "w", newline="", encoding="utf-8-sig") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    return {"folder": folder, "files": len(rows), "rows": rows, "errors": errors,
            "duplicate_codes": sorted(dup_codes), "duplicate_sheets": dup_sheets, "csv": csv_out or None}
