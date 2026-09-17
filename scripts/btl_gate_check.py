#!/usr/bin/env python3
"""Cổng máy cho /book-to-learn.

Dùng: python scripts/btl_gate_check.py <LEARN-dir> <L0|L1|L2|L3|L4|L5|L7> [tuỳ chọn]

Exit 0 = đạt (và ghi dấu vào _pipeline_state.md, trừ khi --no-stamp),
1 = trượt (in từng dòng FAIL), 2 = dùng sai.

Lý do tồn tại: chỗ nào hệ thống chỉ NÓI phải làm mà không có gì BẮT BUỘC,
chỗ đó thủng. Orchestrator không được đánh dấu một pha xong nếu script chưa exit 0.
"""
import argparse
import json
import re
import sys
import unicodedata
from datetime import date, datetime
from pathlib import Path

PHASES = ("L0", "L1", "L2", "L3", "L4", "L5", "L7")  # Note: L6 is intentionally skipped

STATE_KEYS = ("slug", "framework_ung_vien", "quick", "notebook_goc", "notebook_mo_rong", "started")
BRIEF_KEYS = ("van_de_that", "du_doan_1", "du_doan_2", "du_doan_3", "dreyfus_truoc",
              "target", "noi_ap_dung", "tieu_chi_thanh_cong")


# ---------------------------------------------------------------- đọc tệp

def read(path) -> str:
    # utf-8-sig: strip a UTF-8 BOM if present (PowerShell Out-File default on
    # this host writes one) — plain utf-8 would leave "﻿---" as the first
    # bytes and parse_frontmatter would silently return {} for the whole file.
    return Path(path).read_text(encoding="utf-8-sig")


def parse_frontmatter(text: str) -> dict:
    m = re.match(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
            value = value[1:-1]
        elif value.startswith("[") and value.endswith("]"):
            value = [x.strip().strip("'\"") for x in value[1:-1].split(",") if x.strip()]
        elif value.lower() in ("true", "false"):
            value = value.lower() == "true"
        out[key] = value
    return out


def sections(text: str) -> dict:
    out, current, buf = {}, None, []
    for line in text.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m or re.match(r"^#\s", line):
            if current is not None:
                out[current] = "\n".join(buf).strip()
            current, buf = (m.group(1) if m else None), []
            continue
        if current is not None:
            buf.append(line)
    if current is not None:
        out[current] = "\n".join(buf).strip()
    return out


def section_starting(text: str, prefix: str) -> str:
    for heading, content in sections(text).items():
        if heading.startswith(prefix):
            return content
    return ""


def table_rows(text: str) -> list:
    rows, last_was_row = [], False
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            last_was_row = False
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if any(cells) and all(re.fullmatch(r":?-{3,}:?", c) for c in cells if c):
            if last_was_row and rows:
                rows.pop()  # dòng ngay trên vạch phân cách là tiêu đề
            last_was_row = False
            continue
        rows.append(cells)
        last_was_row = True
    return rows


def slugify(name: str) -> str:
    s = name.replace("đ", "d").replace("Đ", "D")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()


def words(text: str) -> int:
    return len([t for t in re.split(r"\s+", text) if t])


def is_int(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def parse_day(value):
    try:
        return date.fromisoformat(str(value).strip())
    except ValueError:
        return None


# ---------------------------------------------------------------- ngữ cảnh

class Ctx:
    def __init__(self, learn_dir, vault, books_root, skills_root, meta_dir,
                 nlm_list=None, nlm_content_dir=None):
        self.learn_dir = Path(learn_dir)
        self.vault = Path(vault)
        self.books_root = Path(books_root)
        self.skills_root = Path(skills_root)
        self.meta_dir = Path(meta_dir)
        self.nlm_list = Path(nlm_list) if nlm_list else None
        self.nlm_content_dir = Path(nlm_content_dir) if nlm_content_dir else None

    @classmethod
    def from_args(cls, a):
        learn = Path(a.learn_dir).resolve()
        vault = Path(a.vault).resolve() if a.vault else learn.parents[1]
        return cls(
            learn, vault,
            a.books_root or vault / "3_Resources" / "Books",
            a.skills_root or Path.home() / ".claude" / "skills",
            a.meta_dir or vault / "2_Areas" / "CEO-Self" / "Learning-Meta",
            a.nlm_list, a.nlm_content_dir,
        )

    @property
    def state_path(self) -> Path:
        return self.learn_dir / "_pipeline_state.md"

    @property
    def state(self) -> dict:
        return parse_frontmatter(read(self.state_path)) if self.state_path.exists() else {}

    @property
    def slug(self) -> str:
        return str(self.state.get("slug", "")).strip()

    @property
    def frameworks(self) -> list:
        fws = self.state.get("framework_ung_vien", [])
        return fws if isinstance(fws, list) else []


def gate_passed(ctx: Ctx, phase: str) -> bool:
    if not ctx.state_path.exists():
        return False
    return re.search(rf"^- {phase}: PASS ", read(ctx.state_path), re.M) is not None


def stamp(ctx: Ctx, phase: str, now: datetime) -> None:
    text = read(ctx.state_path)
    line = f"- {phase}: PASS {now:%Y-%m-%dT%H:%M}"
    pattern = rf"^- {phase}: PASS .*$"
    if re.search(pattern, text, re.M):
        text = re.sub(pattern, line, text, flags=re.M)
    else:
        if "## Gates" not in text:
            text = text.rstrip("\n") + "\n\n## Gates\n"
        text = text.rstrip("\n") + "\n" + line + "\n"
    ctx.state_path.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------- các cổng

# Nhãn "trần" và nhãn bọc động từ đệm (chọn/lấy/theo/phương án/PA/option) đều
# coi là chưa ghi bằng chữ — nhưng "Chọn A vì <lý do>" thì phần còn lại sau
# nhãn không khớp hết (fullmatch), nên vẫn PASS.
_FILLER = r"(?:chọn|chon|lấy|theo|phương\s+án|phuong\s+an|PA|option)"
LABEL_ONLY = re.compile(
    rf"\s*[-*]?\s*(?:[^:]*:\s*)?(?:{_FILLER}\s+)?\(?[A-Z]\)?\s*\.?\s*",
    re.IGNORECASE,
)


def check_L0(ctx: Ctx) -> list:
    p = ctx.learn_dir / "_Project_Brief.md"
    if not p.exists():
        return ["L0: thiếu _Project_Brief.md"]
    text = read(p)
    fm = parse_frontmatter(text)
    errs = []
    if not str(fm.get("van_de_that", "")).strip():
        errs.append("L0: van_de_that rỗng — cần một vấn đề/quyết định thật của Workshop X")
    if any(not str(fm.get(f"du_doan_{i}", "")).strip() for i in (1, 2, 3)) or "du_doan_4" in fm:
        errs.append("L0: cần đúng 3 dự đoán (du_doan_1..du_doan_3)")
    if str(fm.get("dreyfus_truoc", "")).strip() not in {"1", "2", "3", "4", "5"}:
        errs.append("L0: dreyfus_truoc phải là số 1–5")
    target = str(fm.get("target", "")).strip()
    if target:
        if not (ctx.vault / "1_Projects" / target).is_dir():
            errs.append(f"L0: dự án đích không tồn tại: 1_Projects/{target}")
    elif not str(fm.get("noi_ap_dung", "")).strip():
        errs.append("L0: không có target thì noi_ap_dung phải khác rỗng")
    for line in sections(text).get("Quyết định", "").splitlines():
        if line.strip() and LABEL_ONLY.fullmatch(line):
            errs.append(f"L0: quyết định phải ghi bằng chữ, không bằng nhãn: '{line.strip()}'")
    return errs


ARG_SUBST = re.compile(r"\$[0-9](?![0-9])")
LEVEL = re.compile(r"L([1-9]|1[0-2])")


def check_L1(ctx: Ctx) -> list:
    errs = []
    skill_dir = ctx.skills_root / ctx.slug
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [f"L1: thiếu {skill_md}"]
    if not list((skill_dir / "chapters").glob("*.md")):
        errs.append("L1: skill không có chương nào trong chapters/")
    for i, line in enumerate(read(skill_md).splitlines(), 1):
        if ARG_SUBST.search(line):
            errs.append(f"L1: SKILL.md dòng {i} có '$<số>' — Claude Code sẽ thay bằng tham số: {line.strip()[:80]}")
    lever = ctx.books_root / ctx.slug / "Leverage_Map.md"
    if not lever.exists():
        errs.append("L1: thiếu Leverage_Map.md")
    else:
        rows = table_rows(read(lever))
        if not rows:
            errs.append("L1: Leverage_Map.md không có dòng framework nào")
        for r in rows:
            if len(r) < 2 or not LEVEL.fullmatch(r[1]):
                errs.append(f"L1: framework '{r[0]}' thiếu mức đòn bẩy L1–L12")
    kit = ctx.books_root / ctx.slug / "Learning_Kit.md"
    if not kit.exists() or not read(kit).strip():
        errs.append("L1: thiếu hoặc rỗng Learning_Kit.md")
    return errs


def check_L2(ctx: Ctx) -> list:
    src = ctx.books_root / ctx.slug / "_source"
    files = sorted(p for p in src.glob("*") if p.is_file()) if src.is_dir() else []
    if not files:
        return ["L2: _source/ trống — chưa tách chương"]
    if not ctx.nlm_list or not ctx.nlm_list.exists():
        return ["L2: cần --nlm-list (JSON của `nlm source list <notebook> -j`) — không tin kết quả in ra của `source add`"]
    try:
        items = json.loads(read(ctx.nlm_list))
    except json.JSONDecodeError as e:
        return [f"L2: {ctx.nlm_list} không phải JSON hợp lệ — {e}"]

    # Detect duplicate titles
    title_counts = {}
    for i in items:
        title = i.get("title")
        title_counts[title] = title_counts.get(title, 0) + 1
    duplicates = [t for t, count in title_counts.items() if count > 1]
    if duplicates:
        return [f"L2: nhiều nguồn cùng tên '{dup}' — xoá bản trùng trước khi kiểm" for dup in duplicates]

    by_title = {i.get("title"): i for i in items}
    errs = []
    ready = [i for i in items if i.get("status") == 2]
    if len(ready) != len(files):
        errs.append(f"L2: {len(ready)} nguồn sẵn sàng ≠ {len(files)} tệp chương")
    for f in files:
        item = by_title.get(f.name)
        if not item:
            errs.append(f"L2: không thấy nguồn '{f.name}' trên notebook")
            continue
        if item.get("status") != 2:
            errs.append(f"L2: nguồn '{f.name}' chưa sẵn sàng (status={item.get('status')})")
            continue
        cpath = ctx.nlm_content_dir / f"{item['id']}.json" if ctx.nlm_content_dir else None
        if not cpath or not cpath.exists():
            errs.append(f"L2: thiếu nội dung đã tải cho '{f.name}' (nlm source content {item['id']} -j)")
            continue
        try:
            got = json.loads(read(cpath)).get("char_count", 0)
        except json.JSONDecodeError as e:
            errs.append(f"L2: {cpath.name} không phải JSON hợp lệ — {e}")
            continue
        need = len(read(f)) * 0.5
        if got < need:
            errs.append(f"L2: nguồn '{f.name}' chỉ {got} ký tự < 50% tệp gốc ({len(read(f))}) — nghi trang chặn bot")
    return errs


CLAIM_LABELS = {"SUPPORTED", "CONTESTED", "CẦN-CHUYỂN-VN"}
EMPTY_CELL = {"", "-", "—", "✅", "✓"}
FEYNMAN_KEYS = ("framework", "tac_gia")
MIN_ANSWER_WORDS = 40

# Constants for L5 and L7
CARD_KEYS = ("framework", "gia_thuyet", "chi_so", "baseline", "nguong", "nguoi_chiu_trach_nhiem",
             "ngay_bat_dau", "ngay_ket_thuc", "du_doan", "don_vi_framework", "don_vi_thi_nghiem",
             "muc_tin_cay_du_lieu", "ceo_duyet")
MAX_RUN_DAYS = 16
AAR_HEADINGS = ("Định xảy ra gì", "Thực tế ra sao", "Vì sao khác", "Lần sau làm gì")
AAR_KEYS = ("quyet_dinh",)
DECISIONS = {"keep", "adapt", "drop"}
PERKINS = {"tacit", "aware", "strategic", "reflective"}
CYCLE_KEYS = {
    "slug": str, "opened": str, "closed": str, "target": (str, type(None)),
    "dreyfus_before": int, "dreyfus_after": int, "leverage_reached": str, "perkins": str,
    "applied": bool, "decision": str, "prediction_hits": int, "prediction_total": int,
    "days_to_competence": int, "techniques": dict, "illusion_gap": (int, float),
    "book_type": str, "failure_points": list, "next_book_hint": str,
}


def check_L3(ctx: Ctx) -> list:
    p = ctx.books_root / ctx.slug / "Claims.md"
    if not p.exists():
        return ["L3: thiếu Claims.md"]
    rows = table_rows(read(p))
    if not rows:
        return ["L3: Claims.md không có luận điểm nào"]
    errs = []
    for r in rows:
        if len(r) < 5:
            errs.append(f"L3: dòng thiếu cột (cần #, Luận điểm, Nhãn, Nguồn, Vị trí): {r}")
            continue
        num, claim, label, source, where = r[:5]
        if label not in CLAIM_LABELS:
            errs.append(f"L3: luận điểm {num} có nhãn '{label}' — chỉ nhận {sorted(CLAIM_LABELS)}")
        if source in EMPTY_CELL or where in EMPTY_CELL:
            errs.append(f"L3: luận điểm {num} thiếu nguồn hoặc vị trí (dấu ✅ không phải trích dẫn)")
    return errs


def check_L4(ctx: Ctx) -> list:
    if not ctx.frameworks:
        return ["L4: framework_ung_vien trong _pipeline_state.md đang rỗng — CEO chọn sau L1"]
    errs = []
    for fw in ctx.frameworks:
        name = f"feynman-{slugify(fw)}.md"
        p = ctx.learn_dir / "learn" / name
        if not p.exists():
            errs.append(f"L4: thiếu learn/{name} cho framework '{fw}'")
            continue
        text = read(p)
        fm = parse_frontmatter(text)
        # Check all FEYNMAN_KEYS are present and not blank
        for key in FEYNMAN_KEYS:
            if not str(fm.get(key, "")).strip():
                errs.append(f"L4: {name} thiếu hoặc trống {key}:")
        # Check framework value matches candidate (case-insensitive)
        if str(fm.get("framework", "")).strip().casefold() != fw.strip().casefold():
            errs.append(f"L4: {name} framework: '{fm.get('framework', '')}' ≠ ứng viên '{fw}'")
        # Check tac_gia == "CEO"
        if str(fm.get("tac_gia", "")).strip() != "CEO":
            errs.append(f"L4: {name} phải có tac_gia: CEO — AI không được điền câu trả lời Feynman")
        for q in ("Q1", "Q2", "Q3"):
            answer = "\n".join(l for l in section_starting(text, q).splitlines()
                               if not l.lstrip().startswith(">"))
            if words(answer) < MIN_ANSWER_WORDS:
                errs.append(f"L4: {name} {q} chỉ {words(answer)} từ < {MIN_ANSWER_WORDS}")
        rubric = table_rows(section_starting(text, "Rubric"))
        if not rubric:
            errs.append(f"L4: {name} thiếu bảng Rubric tự chấm")
        for r in rubric:
            if r[-1] not in {"1", "2", "3", "4", "5"}:
                errs.append(f"L4: {name} rubric '{r[0]}' có mức '{r[-1]}' — cần 1–5")
    return errs


def check_L5(ctx: Ctx) -> list:
    errs = []
    if not gate_passed(ctx, "L4"):
        errs.append("L5: cổng Feynman L4 chưa qua")
    if not ctx.state.get("quick") and not gate_passed(ctx, "L3"):
        errs.append("L5: L3 (Claims) chưa qua — hoặc đặt quick: true và chấp nhận nhãn CHƯA KIỂM")
    p = ctx.learn_dir / "Experiment_Card.md"
    if not p.exists():
        return errs + ["L5: thiếu Experiment_Card.md"]
    fm = parse_frontmatter(read(p))
    for k in CARD_KEYS:
        if not str(fm.get(k, "")).strip():
            errs.append(f"L5: thẻ thiếu ô {k}")
    fw_card = str(fm.get("framework", "")).strip()
    if fw_card and not any(fw_card.casefold() == fw.casefold() for fw in ctx.frameworks):
        errs.append(f"L5: framework '{fm.get('framework')}' không nằm trong framework_ung_vien")
    if str(fm.get("baseline", "")).strip() and not re.fullmatch(r"-?\d+(?:[.,]\d+)?", str(fm["baseline"]).strip()):
        errs.append(f"L5: baseline phải là con số, đang là '{fm['baseline']}'")
    start, end = parse_day(fm.get("ngay_bat_dau", "")), parse_day(fm.get("ngay_ket_thuc", ""))
    if not start or not end:
        errs.append("L5: ngay_bat_dau/ngay_ket_thuc phải là ngày ISO YYYY-MM-DD")
    elif not 0 <= (end - start).days <= MAX_RUN_DAYS:
        errs.append(f"L5: thời lượng {(end - start).days} ngày — phải trong 0–{MAX_RUN_DAYS}")
    uf, ut = str(fm.get("don_vi_framework", "")).strip(), str(fm.get("don_vi_thi_nghiem", "")).strip()
    if uf and ut and uf.casefold() != ut.casefold():
        errs.append(f"L5: đơn vị phân tích lệch — framework '{uf}' ≠ thí nghiệm '{ut}'")
    trust = str(fm.get("muc_tin_cay_du_lieu", "")).strip()
    if trust and not re.match(r"L[1-5]\b", trust):
        errs.append("L5: muc_tin_cay_du_lieu phải bắt đầu bằng L1–L5")
    if str(fm.get("ceo_duyet", "")).strip() and not parse_day(fm.get("ceo_duyet")):
        errs.append("L5: ceo_duyet phải là ngày ISO")
    return errs


def check_L7(ctx: Ctx) -> list:
    errs = []
    aar = ctx.learn_dir / "AAR.md"
    if not aar.exists():
        errs.append("L7: thiếu AAR.md")
    else:
        text = read(aar)
        if parse_frontmatter(text).get("quyet_dinh") not in DECISIONS:
            errs.append(f"L7: quyet_dinh phải thuộc {sorted(DECISIONS)}")
        secs = sections(text)
        for h in AAR_HEADINGS:
            if not secs.get(h, "").strip():
                errs.append(f"L7: AAR thiếu hoặc rỗng mục '{h}'")
    ledger = ctx.meta_dir / "cycles.jsonl"
    rows = []
    if ledger.exists():
        for lineno, line in enumerate(read(ledger).splitlines(), 1):
            if line.strip():
                try:
                    obj = json.loads(line)
                    if obj.get("slug") == ctx.slug:
                        rows.append(obj)
                except json.JSONDecodeError as e:
                    errs.append(f"L7: cycles.jsonl dòng {lineno} không phải JSON hợp lệ — {e}")
    if not rows:
        return errs + [f"L7: cycles.jsonl chưa có dòng cho slug '{ctx.slug}'"]
    row = rows[-1]
    for k, typ in CYCLE_KEYS.items():
        if k not in row:
            errs.append(f"L7: dòng meta thiếu '{k}'")
            continue
        v = row[k]
        ok = is_int(v) if typ is int else (isinstance(v, typ) and not (isinstance(v, bool) and typ != bool))
        if not ok:
            errs.append(f"L7: '{k}' sai kiểu: {v!r}")
    if row.get("decision") not in DECISIONS:
        errs.append("L7: decision phải là keep/adapt/drop")
    if row.get("perkins") not in PERKINS:
        errs.append(f"L7: perkins phải thuộc {sorted(PERKINS)}")
    if not LEVEL.fullmatch(str(row.get("leverage_reached", ""))):
        errs.append("L7: leverage_reached phải là L1–L12")
    for k in ("dreyfus_before", "dreyfus_after"):
        if is_int(row.get(k)) and not 1 <= row[k] <= 5:
            errs.append(f"L7: {k} phải 1–5")
    if row.get("applied") is True and not gate_passed(ctx, "L5"):
        errs.append("L7: applied=true nhưng thẻ thí nghiệm L5 chưa qua cổng — ghi applied=false")
    return errs


CHECKS = {"L0": check_L0, "L1": check_L1, "L2": check_L2, "L3": check_L3, "L4": check_L4,
          "L5": check_L5, "L7": check_L7}


# ---------------------------------------------------------------- CLI

def parse_args(argv):
    ap = argparse.ArgumentParser(prog="btl_gate_check")
    ap.add_argument("learn_dir")
    ap.add_argument("phase")
    ap.add_argument("--vault")
    ap.add_argument("--books-root")
    ap.add_argument("--skills-root")
    ap.add_argument("--meta-dir")
    ap.add_argument("--nlm-list", help="tệp JSON từ `nlm source list <notebook> -j`")
    ap.add_argument("--nlm-content-dir", help="thư mục chứa <source_id>.json từ `nlm source content <id> -j`")
    ap.add_argument("--no-stamp", action="store_true")
    return ap.parse_args(argv)


def main(argv=None) -> int:
    a = parse_args(sys.argv[1:] if argv is None else argv)
    if a.phase not in CHECKS:
        print(f"Pha không hợp lệ: {a.phase}. Dùng một trong: {', '.join(sorted(CHECKS))}")
        return 2
    ctx = Ctx.from_args(a)
    if not ctx.slug:
        print(f"Thiếu {ctx.state_path} hoặc thiếu trường slug")
        return 2
    errs = CHECKS[a.phase](ctx)
    for e in errs:
        print("FAIL " + e)
    if errs:
        return 1
    print(f"PASS {a.phase}")
    if not a.no_stamp:
        stamp(ctx, a.phase, datetime.now())
    return 0


if __name__ == "__main__":
    sys.exit(main())
