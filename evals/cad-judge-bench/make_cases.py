"""Build the helix-cad-judge benchmark: 10 cases (2 good, 8 seeded faults) of one plate, each in its own folder with
only spec.md, model.py, model_views.png, geometry_contract.json. Answer key + gate results go to <out>/jb_key/
(never inside a case folder). Case folder numbers are shuffled so the name carries no hint.

Usage: python evals/cad-judge-bench/make_cases.py <out_dir>     (out_dir OUTSIDE the repo, e.g. a scratchpad)
Then run one fresh judge agent per case with the prompt in skills/helix/helix-cad-judge/SKILL.md Step 3, and
score with score_bench.py <out_dir>. Needs build123d."""
import hashlib
import json
import os
import random
import subprocess
import sys
import textwrap

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GATES = os.path.join(REPO, "skills", "helix", "helix-cad-gates")
ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else sys.exit(__doc__)
CASES = os.path.join(ROOT, "jb_cases")
KEY = os.path.join(ROOT, "jb_key")

SPEC = textwrap.dedent("""\
    # Spec — TẤM GÁ JB-01 (đã duyệt)
    Đơn vị mm. Quy ước trục: X dọc tấm, Y ngang, Z chiều dày; gốc tại góc min. Phương pháp chiếu: góc thứ nhất.
    Vật liệu AL6061.

    1. Tấm chữ nhật 120 × 60 × 10.
    2. Lỗ thông Ø10, tâm cách đầu +X 30, ở giữa chiều ngang (y = 30), thông suốt theo Z.
    3. Hai lỗ thông Ø6 ở nửa −X, tâm x = 20, y = 15 và y = 45.
    4. Hốc chữ nhật lõm vào mặt +Z, 30 × 20, sâu 4, tâm tại x = 60, y = 30; đáy hốc kín (không thông xuống mặt −Z).
    5. Vát 1 × 45° các cạnh ngoài của mặt +Z. Mặt −Z không vát.
    6. Không có feature nào khác.
""")

QUESTIONS = [
    {"id": "Q1", "q": "Lỗ LỚN NHẤT trên tấm có tiết diện tròn (không vuông, không đa giác)?", "spec_line": SPEC.splitlines()[5], "severity": "block"},
    {"id": "Q2", "q": "Lỗ lớn nhất thông suốt từ mặt +Z xuống mặt −Z?", "spec_line": SPEC.splitlines()[5], "severity": "block"},
    {"id": "Q3", "q": "Có đúng hai lỗ nhỏ, cả hai nằm ở nửa −X của tấm?", "spec_line": SPEC.splitlines()[6], "severity": "block"},
    {"id": "Q4", "q": "Có một hốc chữ nhật LÕM vào mặt +Z (không phải khối nhô lên)?", "spec_line": SPEC.splitlines()[7], "severity": "block"},
    {"id": "Q5", "q": "Hốc chữ nhật có đáy kín (không thông xuống mặt −Z)?", "spec_line": SPEC.splitlines()[7], "severity": "block"},
    {"id": "Q6", "q": "Vát nằm ở các cạnh ngoài của mặt +Z, và mặt −Z không có vát?", "spec_line": SPEC.splitlines()[8], "severity": "comment"},
    {"id": "Q7", "q": "Mô hình KHÔNG có feature nào ngoài các mục 1–5 của spec?", "spec_line": SPEC.splitlines()[9], "severity": "comment"},
    {"id": "Q8", "q": "Lỗ lớn nhất nằm ở nửa +X của tấm?", "spec_line": SPEC.splitlines()[5], "severity": "block"},
]

HEAD = '''from build123d import Axis, Box, Cylinder, Location, chamfer, export_step

PARAMS = {"L": 120.0, "W": 60.0, "H": 10.0, "D_BIG": 10.0, "X_BIG_FROM_END": 30.0, "D_SMALL": 6.0,
          "X_SMALL": 20.0, "Y_SMALL": 15.0, "POCKET_L": 30.0, "POCKET_W": 20.0, "POCKET_D": 4.0, "CH": 1.0}


def at(shape, x, y, z):
    return shape.moved(Location((x, y, z)))


def build(p):
    L, W, H = p["L"], p["W"], p["H"]
    plate = at(Box(L, W, H), L / 2, W / 2, H / 2)
'''
TAIL = '''

if __name__ == "__main__":
    export_step(build(PARAMS), "model.step")
'''
CH_TOP = '    plate = chamfer(plate.edges().group_by(Axis.Z)[-1], p["CH"])\n'
CH_BOT = '    plate = chamfer(plate.edges().group_by(Axis.Z)[0], p["CH"])\n'
POCKET = '    plate = plate - at(Box(p["POCKET_L"], p["POCKET_W"], 2 * p["POCKET_D"]), L / 2, W / 2, H)\n'
POCKET_THRU = '    plate = plate - at(Box(p["POCKET_L"], p["POCKET_W"], 2 * H), L / 2, W / 2, H / 2)\n'
BOSS = '    plate = plate + at(Box(p["POCKET_L"], p["POCKET_W"], p["POCKET_D"]), L / 2, W / 2, H + p["POCKET_D"] / 2)\n'
BIG = '    plate = plate - at(Cylinder(p["D_BIG"] / 2, 2 * H), L - p["X_BIG_FROM_END"], W / 2, H / 2)\n'
BIG_SQ = '    plate = plate - at(Box(p["D_BIG"], p["D_BIG"], 2 * H), L - p["X_BIG_FROM_END"], W / 2, H / 2)\n'
BIG_BLIND = '    plate = plate - at(Cylinder(p["D_BIG"] / 2, 12.0), L - p["X_BIG_FROM_END"], W / 2, H)\n'
BIG_MIRROR = '    plate = plate - at(Cylinder(p["D_BIG"] / 2, 2 * H), p["X_BIG_FROM_END"], W / 2, H / 2)\n'
SMALL = ('    for y in (p["Y_SMALL"], W - p["Y_SMALL"]):\n'
         '        plate = plate - at(Cylinder(p["D_SMALL"] / 2, 2 * H), p["X_SMALL"], y, H / 2)\n')
SMALL_ONE = '    plate = plate - at(Cylinder(p["D_SMALL"] / 2, 2 * H), p["X_SMALL"], p["Y_SMALL"], H / 2)\n'
SMALL_MIRROR = ('    for y in (p["Y_SMALL"], W - p["Y_SMALL"]):\n'
                '        plate = plate - at(Cylinder(p["D_SMALL"] / 2, 2 * H), L - p["X_SMALL"], y, H / 2)\n')
NOTCH = '    plate = plate - at(Box(8.0, 8.0, 2 * H), L - 4.0, 4.0, H / 2)\n'
RET = '    return plate\n'

GOOD2 = HEAD + CH_TOP + BIG + SMALL + POCKET + RET   # same part, different feature order
Y = "yes"
CASE_DEFS = {
    "good_1": (HEAD + CH_TOP + POCKET + BIG + SMALL + RET, dict(Q1=Y, Q2=Y, Q3=Y, Q4=Y, Q5=Y, Q6=Y, Q7=Y, Q8=Y), "pass"),
    "good_2": (GOOD2, dict(Q1=Y, Q2=Y, Q3=Y, Q4=Y, Q5=Y, Q6=Y, Q7=Y, Q8=Y), "pass"),
    "A_square_hole": (HEAD + CH_TOP + POCKET + BIG_SQ + SMALL + RET, dict(Q1="no", Q2=Y, Q3=Y, Q4=Y, Q5=Y, Q6=Y, Q7=None, Q8=Y), "block"),
    "B_blind_hole": (HEAD + CH_TOP + POCKET + BIG_BLIND + SMALL + RET, dict(Q1=Y, Q2="no", Q3=Y, Q4=Y, Q5=Y, Q6=Y, Q7=Y, Q8=Y), "block"),
    "C_one_small_hole": (HEAD + CH_TOP + POCKET + BIG + SMALL_ONE + RET, dict(Q1=Y, Q2=Y, Q3="no", Q4=Y, Q5=Y, Q6=Y, Q7=Y, Q8=Y), "block"),
    "D_boss_not_pocket": (HEAD + CH_TOP + BOSS + BIG + SMALL + RET, dict(Q1=Y, Q2=Y, Q3=Y, Q4="no", Q5=None, Q6=Y, Q7=None, Q8=Y), "block"),
    "E_pocket_through": (HEAD + CH_TOP + POCKET_THRU + BIG + SMALL + RET, dict(Q1=Y, Q2=Y, Q3=Y, Q4=Y, Q5="no", Q6=Y, Q7=Y, Q8=Y), "block"),
    "F_chamfer_bottom": (HEAD + CH_BOT + POCKET + BIG + SMALL + RET, dict(Q1=Y, Q2=Y, Q3=Y, Q4=Y, Q5=Y, Q6="no", Q7=Y, Q8=Y), "comment-only"),
    "G_extra_notch": (HEAD + CH_TOP + POCKET + BIG + SMALL + NOTCH + RET, dict(Q1=Y, Q2=Y, Q3=Y, Q4=Y, Q5=Y, Q6=None, Q7="no", Q8=Y), "comment-only"),
    "H_mirrored": (HEAD + CH_TOP + POCKET + BIG_MIRROR + SMALL_MIRROR + RET, dict(Q1=Y, Q2=Y, Q3="no", Q4=Y, Q5=Y, Q6=Y, Q7=Y, Q8="no"), "block"),
}

CONTRACT = {
    "part_id": "JB-01", "classification": "KHÔNG-NHẠY-CẢM", "projection_method": "first-angle",
    "axis_convention": "X dọc tấm, Y ngang, Z chiều dày; gốc tại góc min",
    "bbox": [120, 60, 10], "bbox_tol": 0.5,
    "probes": [{"why": "lỗ lớn, giữa chiều dày phía trên", "pt": [90, 30, 8], "inside": False},
               {"why": "thân đặc nửa -X", "pt": [35, 30, 5], "inside": True}],
    "cyl_features": [{"what": "big_d10", "dia": 10, "min_faces": 1, "max_faces": 1},
                     {"what": "small_d6", "dia": 6, "min_faces": 2, "max_faces": 2}],
    "param_probes": [{"why": "lỗ lớn cách đầu +X 30", "pt": ["L-X_BIG_FROM_END", "W/2", "H-2"], "inside": False}],
    "f4_params": ["L", "W", "X_BIG_FROM_END"],
    "judge_questions": QUESTIONS,
    "material": "AL6061",
}


def main():
    os.makedirs(CASES, exist_ok=True)
    os.makedirs(KEY, exist_ok=True)
    names = list(CASE_DEFS)
    random.Random(20261105).shuffle(names)
    key = {}
    for i, name in enumerate(names, 1):
        code, truth, expect = CASE_DEFS[name]
        d = os.path.join(CASES, f"case_{i:02d}")
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "spec.md"), "w", encoding="utf-8").write(SPEC)
        open(os.path.join(d, "model.py"), "w", encoding="utf-8").write(code + TAIL)
        cpath = os.path.join(d, "geometry_contract.json")
        json.dump(CONTRACT, open(cpath, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        sha = hashlib.sha256(open(cpath, "rb").read()).hexdigest()
        env = dict(os.environ, PYTHONUTF8="1")
        subprocess.run([sys.executable, os.path.join(GATES, "cad_runner.py"), "run", "--model", "model.py"],
                       cwd=d, env=env, check=True, capture_output=True)
        subprocess.run([sys.executable, os.path.join(GATES, "render_views.py"), "--step", "model.step",
                        "--out", "model_views.png", "--title", "JB-01"], cwd=d, env=env, check=True,
                       capture_output=True)
        gout = os.path.join(KEY, f"case_{i:02d}_gates")
        r = subprocess.run([sys.executable, os.path.join(GATES, "geom_gates.py"), "--step", "model.step",
                            "--contract", "geometry_contract.json", "--model", "model.py", "--approved-hash", sha,
                            "--out", gout, "--quiet"], cwd=d, env=env, capture_output=True, text=True)
        g = json.load(open(gout + ".json", encoding="utf-8"))
        os.remove(os.path.join(d, "model.step"))
        key[f"case_{i:02d}"] = {"name": name, "truth": truth, "expect": expect, "sha": sha,
                                "gates_verdict": g["verdict"],
                                "gates_fail": [c["rule_id"] for c in g["checks"] if c["status"] == "FAIL"]}
        print(f"case_{i:02d} {name:<20} gates={g['verdict']:<5} {key[f'case_{i:02d}']['gates_fail']}")
    json.dump(key, open(os.path.join(KEY, "key.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
