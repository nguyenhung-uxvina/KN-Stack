"""Hàm thuần (không cần AutoCAD) — làm sạch chữ, dựng chữ kích thước, đọc khung tên, nhãn SL/TL/VL.

Dùng chung cho đường COM (server.py) và đường đọc DXF ngoại tuyến (dxf_scan.py).
"""
import re
import unicodedata

BS = "\\"

# --- MText ---------------------------------------------------------------
_UNI = re.compile(r"\\U\+([0-9A-Fa-f]{4})")
_STACK = re.compile(r"\\S([^;^#/]*)[\^#/]([^;]*);")
_ARG_CODES = re.compile(r"\\[fFHhCcTtQqWwAap][^;]*;")
_TOGGLES = re.compile(r"\\[LlOoKkNnXx]")
_PERCENT = {"%%c": "Ø", "%%C": "Ø", "%%d": "°", "%%D": "°", "%%p": "±", "%%P": "±"}


def clean_mtext(s: str, para_sep: str = " ") -> str:
    """Bỏ mã định dạng MText/TEXT, giữ chữ. `\\P` (xuống dòng) → para_sep."""
    if not s:
        return ""
    s = s.replace(BS + BS, "\x00")                                # chừa '\\' literal
    s = _UNI.sub(lambda m: chr(int(m.group(1), 16)), s)
    s = _STACK.sub(lambda m: f"{m.group(1)}/{m.group(2)}", s)
    s = _ARG_CODES.sub("", s)
    s = _TOGGLES.sub("", s)
    s = s.replace(BS + "P", "\n").replace(BS + "~", " ")
    for k, v in _PERCENT.items():
        s = s.replace(k, v)
    s = re.sub(r"%%[uUoO]", "", s)
    s = s.replace("{", "").replace("}", "").replace("\x00", BS)
    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in s.split("\n")]
    return para_sep.join(ln for ln in lines if ln)


# --- Kích thước ----------------------------------------------------------
def format_measurement(value: float, precision: int = 2, decimal_sep: str = ".",
                       suppress_trailing_zeros: bool = True) -> str:
    txt = f"{value:.{max(0, precision)}f}"
    if suppress_trailing_zeros and "." in txt:
        txt = txt.rstrip("0").rstrip(".")
    return txt.replace(".", decimal_sep)


def render_dim_text(override: str, measurement: float, **fmt) -> str:
    """Chữ hiển thị thật của kích thước: override rỗng hoặc '<>' ⇒ số đo; có '<>' ⇒ chèn số đo vào."""
    meas = format_measurement(measurement, **fmt)
    ov = clean_mtext(override or "")
    if not ov:
        return meas
    return ov.replace("<>", meas)


# --- Nhãn chi tiết con: "SL 02; TL 1/2; VL NHÔM 5083" ---------------------
_SL = re.compile(r"\bSL\s*0*(\d+)\s*(?:;\s*TL\s*([\d.,:/ ]+?))?\s*(?:;\s*VL\s*(.+))?$", re.I)


def parse_sl_label(text: str):
    """Trả {'qty', 'scale', 'material'} hoặc None nếu không phải nhãn SL."""
    m = _SL.search(clean_mtext(text))
    if not m:
        return None
    return {"qty": int(m.group(1)), "scale": (m.group(2) or "").strip() or None,
            "material": (m.group(3) or "").strip() or None}


# --- Khung tên ----------------------------------------------------------
# Ô của block «KHUNG TÊN BẢN VẼ LẮP» (TCVN) trong toạ độ cục bộ của block (đã chia tỉ lệ chèn).
# Hiệu chỉnh trên một bộ hồ sơ thật 42 tờ (2026-11). Khung tên khác ⇒ truyền `cells` riêng.
TITLE_CELLS_TCVN = {
    "name":     (195, 250, 110, 125),
    "material": (195, 250, 88, 105),
    "code":     (250, 300, 124, 135),
    "mass":     (268, 285, 105, 120),
    "scale":    (285, 305, 105, 120),
    "sheet":    (250, 280, 95, 105),
    "sheets":   (280, 305, 95, 105),
}
TITLE_BLOCK_HINTS = ("KHUNG TÊN", "KHUNG TEN", "TITLE")


def is_title_block(name: str) -> bool:
    up = (name or "").upper()
    return any(h in up for h in TITLE_BLOCK_HINTS)


def title_fields(texts, origin, scale: float = 1.0, cells=None) -> dict:
    """texts: iterable (x, y, chữ đã sạch) trong toạ độ bản vẽ; origin: điểm chèn khung tên."""
    cells = cells or TITLE_CELLS_TCVN
    out = {k: "" for k in cells}
    ox, oy = origin[0], origin[1]
    s = scale or 1.0
    for x, y, t in texts:
        if not t:
            continue
        lx, ly = (x - ox) / s, (y - oy) / s
        for key, (x0, x1, y0, y1) in cells.items():
            if x0 <= lx < x1 and y0 <= ly < y1:
                out[key] = (out[key] + " " + t).strip() if out[key] else t
                break
    return out


TITLE_REGION = (100, 320, 80, 145)   # toàn vùng khung tên (toạ độ cục bộ) — chữ trong đây không phải nội dung hình


def in_title_region(x, y, origin, scale: float = 1.0) -> bool:
    s = scale or 1.0
    lx, ly = (x - origin[0]) / s, (y - origin[1]) / s
    x0, x1, y0, y1 = TITLE_REGION
    return x0 <= lx <= x1 and y0 <= ly <= y1


def _ascii_tokens(s: str) -> set:
    s = unicodedata.normalize("NFD", s.replace("đ", "d").replace("Đ", "D"))
    s = "".join(ch for ch in s if not unicodedata.combining(ch)).lower()
    return {t for t in re.findall(r"[a-z0-9]+", s) if len(t) >= 2}


def name_matches_file(file_stem: str, title_name: str) -> bool:
    """Tên tệp (không dấu) có chung ≥1 từ với tên trong khung tên? Tên trống ⇒ True (không kết luận).
    False ⇒ nghi khung tên chép từ tờ khác (mã + tên đều chép nên luật 'cùng mã khác tên' bỏ sót)."""
    if not title_name.strip():
        return True
    stem = re.sub(r"^\s*\d+(?:\.\d+)*\.?\s*", "", file_stem)
    return bool(_ascii_tokens(stem) & _ascii_tokens(title_name))


def is_balloon(text: str) -> bool:
    """Số vị trí (bóng số) trên tờ lắp: 1–2 chữ số đứng riêng."""
    return bool(re.fullmatch(r"\d{1,2}", clean_mtext(text)))
