#!/bin/bash
# Cổng plugin fluency-4d — chạy TRƯỚC khi mở hoặc cập nhật PR.
#
# Gom mọi phép kiểm của plugin vào một lệnh, thoát khác 0 nếu bất kỳ cửa nào đỏ.
# Repo chưa có CI; khi nào dựng CI thì gọi đúng script này, đừng chép lại danh sách.
#
#   bash scripts/gate-fluency-4d.sh
#
# Năm cửa, cửa nào cũng bắt một lớp lỗi mà cửa khác không thấy:
#   1. pytest   — logic linter + máy trạng thái thí nghiệm + vòng đời sổ
#   2. lint     — bốn file tham chiếu khớp nhau, citation đúng thư mục dùng chung
#   3. eval     — SKILL.md còn đủ luật (regex tĩnh)
#   4. mutation — chính các anchor eval có thật sự canh cái chúng tưởng không
#   5. triển khai — junction đúng đích, VÀ copy trần resolve được citation
#
# Cửa 4 tồn tại vì cửa 3 tự nó không tự kiểm được: eval xanh không có nghĩa
# eval đang canh cái gì. Bỏ cửa 4 thì cửa 3 trôi dần thành cổng-từ-khoá.

set -uo pipefail
export NO_COLOR=1
export PYTHONIOENCODING=utf-8

cd "$(git rev-parse --show-toplevel)" || exit 2

FAIL=0
run() {
    local label="$1"; shift
    echo ""
    echo "── $label ─────────────────────────────────────────"
    if "$@"; then
        echo "   [OK] $label"
    else
        echo "   [ĐỎ] $label"
        FAIL=1
    fi
}

run "1. pytest" python -m pytest scripts/test_fluency_4d.py -q

run "2. lint tầng tham chiếu" python -c "
import sys; sys.path.insert(0, 'scripts')
import fluency_4d_lint as l
errs  = l.lint_rubric((l.REF_DIR / 'rubric-core.md').read_text(encoding='utf-8'))
errs += l.lint_playbook((l.REF_DIR / 'improvement-playbook.md').read_text(encoding='utf-8'))
# Tầng trỏ: profile đang bật phải tồn tại, không phải khuôn rỗng, không còn ô chờ điền.
errs += l.lint_active_profile((l.REF_DIR / 'active-profile.md').read_text(encoding='utf-8'))
# Mọi profile khác kiểm ở chế độ nháp — sai khung là lỗi, còn ô chờ điền thì không.
for p in sorted(l.REF_DIR.glob('profile-*.md')):
    errs += [f'{p.name}: {e}' for e in l.lint_profile(p.read_text(encoding='utf-8'), allow_draft=True)]
errs += l.validate_ledger_line(l.extract_sample_record((l.REF_DIR / 'ledger-schema.md').read_text(encoding='utf-8')))
errs += l.validate_experiments(l.parse_experiments((l.PLUGIN_ROOT / 'templates' / 'experiments.md').read_text(encoding='utf-8')))
errs += l.lint_skills()
[print('  ', e) for e in errs]
sys.exit(1 if errs else 0)
"

echo ""
echo "── 3. eval tĩnh ba skill ──────────────────────────────"
for s in fluency-4d-preflight fluency-4d-review fluency-4d-weekly; do
    line=$(bash evals/run-eval.sh "$s" 2>&1 | grep -iE "^Score:" | tail -1)
    echo "   $s: $line"
    case "$line" in
        *"(100%)") ;;
        *) FAIL=1; echo "   [ĐỎ] $s chưa đủ điểm" ;;
    esac
done

run "4. mutation eval" python scripts/fluency_4d_mutate.py

run "5. triển khai (junction + copy trần)" bash -c '
    bash setup.sh --verify 2>&1 | grep -E "plugin skill dirs" | tee /dev/stderr | grep -q "^\[OK\]\|All" || exit 1
    python - <<PY
import re, sys, shutil, tempfile
from pathlib import Path
src = Path("plugins/fluency-4d")
tmp = Path(tempfile.mkdtemp()) / "fluency-4d"
shutil.copytree(src, tmp)
rx = re.compile(r"\.\./([A-Za-z0-9._-]+)/references/([A-Za-z0-9._-]+\.md)")
bad = 0
for sk in sorted((tmp / "skills").iterdir()):
    f = sk / "SKILL.md"
    if not f.is_file():
        continue
    for d, ref in sorted(set(rx.findall(f.read_text(encoding="utf-8")))):
        if not (sk / ".." / d / "references" / ref).resolve().is_file():
            print(f"   copy tran HONG: {sk.name} -> ../{d}/references/{ref}"); bad += 1
shutil.rmtree(tmp.parent, ignore_errors=True)
sys.exit(1 if bad else 0)
PY
'

echo ""
echo "══════════════════════════════════════════════════════"
if [ $FAIL -eq 0 ]; then
    echo "CỔNG fluency-4d: XANH — mở PR được"
else
    echo "CỔNG fluency-4d: ĐỎ — đừng mở PR"
fi
exit $FAIL
