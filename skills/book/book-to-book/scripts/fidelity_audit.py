# -*- coding: utf-8 -*-
"""CỔNG NGUYÊN BẢN — đo thật tỷ lệ nguyên bản của sách phái sinh, rồi phán quyết.

Vì sao tồn tại
--------------
Lần chạy Cross 5e (2026-09-07) ra một cuốn 18 chương/159k từ rồi mới đo được:
**trích nguyên văn 9.606 từ = 16,07% toàn bộ sách gốc.** Con số ấy quyết định
cuốn sách dùng được ở đâu — và nó chỉ xuất hiện ở cuối, sau khi mọi chữ đã viết
xong. Tệ hơn: "nội bộ" lúc đó vẫn là *giả định của đường ống*, chưa ai quyết.

Script này đảo ngược thứ tự đó. Mức nguyên bản được **khai trước** (P0, có chữ
ký), rồi đo **bằng máy** ở P7. Model không được tự chấm; đây là nơi duy nhất ra
phán quyết.

Nguyên tắc nền: *prompt không cưỡng chế được prompt.* Một SKILL.md có thể tuyên
bố luật, chỉ mã chạy thật mới thi hành được nó.

Đo cái gì
---------
1. **Trích có thật không** — mọi chuỗi trong ngoặc kép phải tìm thấy trong kho
   ngữ liệu gốc. Một trích không thấy = trích bịa = TRƯỢT ở mọi mức.
2. **Nguyên văn KHÔNG ngoặc** — quét n-gram: đoạn ≥ `--min-run` từ trùng khít
   kho gốc mà nằm ngoài mọi cặp ngoặc. Đây là vùng mù của cổng trích dẫn cũ, và
   là dạng nguy hiểm hơn (không ghi nguồn).
3. **Hai tỷ lệ**, hai câu hỏi khác nhau:
   - `bao phủ` = từ nguyên văn / **từ sách gốc** → "tôi tái tạo bao nhiêu phần
     của người ta" (câu hỏi bản quyền).
   - `mật độ`  = từ nguyên văn / **từ sách mình** → "bao nhiêu phần sách này
     không phải của tôi" (câu hỏi đóng góp).
4. **Câu quy kết trần** — câu "Cross cho rằng X" không có trích neo, không có số
   trang. Không tự phán đúng/sai; chỉ bảo đảm không câu nào lọt khỏi tầm mắt.
5. **Dấu bản nội bộ** trên từng tệp giao ra.

Chạy
----
    python fidelity_audit.py <output_dir> --level F2 [--min-run 10] [--book "glob"]

Mã thoát: 0 = ĐẠT · 1 = KHÔNG ĐẠT (vượt trần / trích bịa / thiếu dấu) ·
          2 = KHÔNG ĐO ĐƯỢC (thiếu khai báo, thiếu kho gốc, không thấy bản thảo).
Mã 2 KHÔNG phải là "sạch". Orchestrator KHÔNG được trình CEO checkpoint khi != 0.
"""
from __future__ import annotations

import argparse
import glob as globlib
import hashlib
import io
import json
import os
import re
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from source_ingest import norm  # noqa: E402  (dùng CHUNG một hàm chuẩn hoá)

# Trần theo mức nguyên bản. Hiệu chỉnh trên số đo thật của lần chạy Cross 5e:
# bao phủ 16,07% · mật độ 6,0% → cuốn đó là F3 xét bao phủ, F2 xét mật độ.
LEVELS = {
    'F1': dict(ten='Lược thuật', bao_phu=2.0, mat_do=3.0),
    'F2': dict(ten='Diễn giải ứng dụng', bao_phu=8.0, mat_do=10.0),
    'F3': dict(ten='Trung thành theo chương', bao_phu=20.0, mat_do=25.0),
    'F4': dict(ten='Sát nguyên bản', bao_phu=None, mat_do=None),
}

STAMP = re.compile(r'ban noi bo', re.IGNORECASE)
# Đường dẫn tệp trong ngoặc nháy KHÔNG phải trích dẫn. Bỏ lọc này thì mỗi dòng
# `_source/sections/muc06_intro.txt` trong tệp thăm dò lại bị báo là một trích bịa —
# dương tính giả, và dương tính giả làm người đọc mất lòng tin vào cả bảng kết quả.
LA_DUONG_DAN = re.compile(r'[/\][^\s]*\.[A-Za-z0-9]{1,5}\s*$|\.(?:md|txt|py|json|pdf|epub|csv|html?)\s*$')
MIN_BYTES = 400


def bo_dau(s):
    """Bỏ dấu tiếng Việt để so khớp lời khai. Bắt đúng dấu là thứ dễ trượt mà
    không nói lên điều gì — "muc nguyen ban" và "mức nguyên bản" là một lời khai."""
    s = unicodedata.normalize('NFD', s).replace('đ', 'd').replace('Đ', 'D')
    return ''.join(c for c in s if not unicodedata.combining(c))

# --- câu quy kết nguồn (vùng mù của cổng trích dẫn) -------------------------
VERB = (r'(?:nói|viết|ghi|ghi nhận|cho rằng|khẳng định|nêu|chỉ ra|lập luận|kết luận|'
        r'đề xuất|gọi|đặt tên|nhấn mạnh|thừa nhận|bác|phản đối|dẫn|trích|mô tả|'
        r'định nghĩa|phân biệt|khuyến nghị|yêu cầu|cảnh báo|quy định|xếp|liệt kê|tính)')
HAS_QUOTE = re.compile(r'[`“"][^`“”"]{20,}[”"`]')
HAS_PAGE = re.compile(r'tr\.\s*\d+|trang\s*\d+|p\.\s*\d+')


class KhongDoDuoc(Exception):
    """Thiếu đầu vào để đo. Khác hẳn 'đo xong và sạch' — đừng bao giờ lẫn hai cái."""


def bam(path):
    return hashlib.sha256(io.open(path, 'rb').read()).hexdigest()[:16]


# --------------------------------------------------- chống báo cáo CŨ (--verify)

GATE_RE = re.compile(r'```json b2b-gate\n(.*?)\n```', re.S)


def verify(outdir, level, pattern=None):
    """Xác nhận báo cáo P7 còn ĐÚNG VỚI bản thảo hiện tại. Dùng làm điều kiện vào P7.5/P8.

    Dạng hỏng thật hay gặp nhất không phải "chưa đo" mà là **đã đo rồi sửa tiếp**:
    P7 chạy xong, P6 sửa thêm vài chương, báo cáo cũ vẫn nằm đó với dấu ✅. Một báo
    cáo mang nhãn sai tệ hơn không có báo cáo — không có thì biết là mình chưa đo;
    có nhãn sai thì TIN là đã đo. Nên ở đây so băm từng tệp, không so ngày sửa.
    """
    p = os.path.join(outdir, 'Phase7-Fidelity-Report.md')
    if not os.path.isfile(p):
        print('KHÔNG CÓ BÁO CÁO — chưa chạy cổng nguyên bản lần nào. '
              'Chạy: python fidelity_audit.py "%s" --level %s' % (outdir, level))
        return 2
    m = GATE_RE.search(io.open(p, encoding='utf-8').read())
    if not m:
        print('BÁO CÁO KHÔNG CÓ KHỐI ẤN — nhiều khả năng đã bị sửa tay. Chạy lại cổng.')
        return 1
    g = json.loads(m.group(1))
    _, chuong = doc_ban_thao(outdir, pattern)
    hien = {}
    for _, _, path in chuong:
        hien[os.path.relpath(path, outdir).replace('\\', '/')] = bam(path)
    cu = g.get('ban_thao', {})
    doi = [k for k in hien if k in cu and cu[k] != hien[k]]
    moi = [k for k in hien if k not in cu]
    mat = [k for k in cu if k not in hien]
    if g.get('level') != level:
        print('BÁO CÁO Ở MỨC %s, ĐANG HỎI MỨC %s.' % (g.get('level'), level))
        return 1
    if doi or moi or mat:
        print('BÁO CÁO CŨ — bản thảo đã đổi sau khi đo:')
        for k in doi[:20]:
            print('  đã sửa : %s' % k)
        for k in moi[:20]:
            print('  mới thêm: %s (chưa hề được đo)' % k)
        for k in mat[:20]:
            print('  biến mất: %s' % k)
        print('Chạy lại cổng trước khi sang P7.5/P8. Con số cũ không nói gì về bản mới.')
        return 1
    if g.get('phan_quyet') != 'DAT':
        print('BÁO CÁO CÒN ĐÚNG VỚI BẢN THẢO, NHƯNG PHÁN QUYẾT LÀ KHÔNG ĐẠT.')
        return 1
    print('✅ Báo cáo P7 còn đúng với bản thảo hiện tại (%d tệp, mức %s, ký %s).'
          % (len(hien), g.get('level'), g.get('ceo_ky')))
    return 0


# ------------------------------------------------------------- khai báo P0

def doc_khai_bao(outdir, level):
    """Đọc `_scope_decision.md`. Đây là chỗ biến 'nội bộ' từ giả định thành quyết định.

    Lần chạy Cross kết thúc với phạm vi phát hành vẫn treo, vì không bước nào
    *bắt* phải chốt. Ở đây không có khai báo thì không có phép đo.
    """
    p = os.path.join(outdir, '_scope_decision.md')
    if not os.path.isfile(p) or os.path.getsize(p) < MIN_BYTES:
        raise KhongDoDuoc(
            'thiếu (hoặc rỗng) %s. Mức nguyên bản và phạm vi phát hành phải được '
            'CEO chốt ở P0 TRƯỚC khi viết chữ nào — chạy /book-to-book P0.' % p)
    raw = io.open(p, encoding='utf-8').read()
    # Đọc bản BỎ DẤU: CEO gõ tay thì "mức nguyên bản" hay "muc nguyen ban" đều
    # là cùng một lời khai. Bắt đúng dấu là thứ dễ trượt mà không nói lên điều gì.
    t = bo_dau(raw)

    m = re.search(r'muc nguyen ban\s*[:=]\s*(F[1-4])', t, re.IGNORECASE)
    if not m:
        raise KhongDoDuoc('%s không khai "mức nguyên bản: F1|F2|F3|F4".' % p)
    khai = m.group(1).upper()
    if khai != level:
        raise KhongDoDuoc(
            'khai báo P0 là %s nhưng lệnh audit chạy ở %s. Hai con số lệch nhau thì '
            'phép đo vô nghĩa — sửa khai báo (và nói rõ vì sao đổi) hoặc sửa lệnh.'
            % (khai, level))

    if not re.search(r'pham vi phat hanh\s*[:=][^\n]*noi bo', t, re.IGNORECASE):
        raise KhongDoDuoc(
            '%s không khai "phạm vi phát hành: NỘI BỘ". /book-to-book chỉ sinh bản '
            'nội bộ; muốn phát hành ra ngoài thì đó là một quyết định khác, đo lại '
            'ở trần khác, không phải một cờ dòng lệnh.' % p)

    ky = re.search(r'\bky\b[^\n]{0,30}?(\d{4}-\d{2}-\d{2})', t)
    if not ky:
        raise KhongDoDuoc('%s chưa có dòng "CEO ký ngày: YYYY-MM-DD".' % p)

    if khai in ('F3', 'F4') and not re.search(
            r'khong tai len|khoa phat tan', t, re.IGNORECASE):
        raise KhongDoDuoc(
            'mức %s tái tạo phần lớn tác phẩm gốc. Khai báo phải mang dòng khoá phát '
            'tán ("khoá phát tán: máy CEO + vault, KHÔNG TẢI LÊN dịch vụ ngoài") — '
            'vì P8 nạp NotebookLM là gửi bản dịch cho bên thứ ba.' % khai)
    return dict(level=khai, ky=ky.group(1), text=t)


# ------------------------------------------------------------ kho ngữ liệu

def doc_kho(outdir):
    sdir = os.path.join(outdir, '_source')
    paths = sorted(globlib.glob(os.path.join(sdir, '*.corpus.txt')))
    if not paths:
        raise KhongDoDuoc(
            'không có kho ngữ liệu gốc trong %s. Chạy source_ingest.py trước. '
            '(Không có kho thì mọi phép đo trả 0 — và 0 ở đây đọc y hệt "sạch". '
            'Đó là âm tính giả im lặng, nên dừng hẳn thay vì báo số.)' % sdir)
    kho = []
    for p in paths:
        label = os.path.basename(p)[:-len('.corpus.txt')]
        corpus = io.open(p, encoding='utf-8').read()
        pm, meta = [], {}
        pmp = os.path.join(sdir, label + '.pagemap.json')
        mp = os.path.join(sdir, label + '.meta.json')
        if os.path.isfile(pmp):
            pm = json.loads(io.open(pmp, encoding='utf-8').read())
        if os.path.isfile(mp):
            meta = json.loads(io.open(mp, encoding='utf-8').read())
        kho.append(dict(label=label, corpus=corpus, pagemap=pm,
                        words=meta.get('words') or len(corpus.split()), meta=meta))
    return kho


def trang_cua(pagemap, off):
    best = None
    for start, page in pagemap:
        if start <= off:
            best = page
        else:
            break
    return best


# --------------------------------------------------------------- bản thảo

ORDER = [
    ('book.md', 'book.md'),
    ('Phase7-Book/book.md', 'Phase7-Book/book.md'),
    ('Phase6-Revised/Ch*.md', 'Phase6-Revised/'),
    ('Phase4-Chapters/Ch*.md', 'Phase4-Chapters/'),
    ('Phase4-Drafts/Ch*.md', 'Phase4-Drafts/'),
]


def doc_ban_thao(outdir, pattern=None):
    """Trả (nhãn_bộ, [(nhãn_chương, text, đường_dẫn)]).

    Lỗi đã gặp: cổng lọc tên tệp `endswith("_Exploration.md")` nên khi chạy trên
    thư mục bản thảo nó trả "0 không thấy" một cách RỖNG — đọc y hệt như sạch.
    Nên ở đây: không thấy tệp nào là lỗi mã 2, không bao giờ là kết quả 0.
    """
    pats = [(pattern, pattern)] if pattern else ORDER
    for pat, nhan in pats:
        hits = [p for p in sorted(globlib.glob(os.path.join(outdir, pat)))
                if os.path.isfile(p) and os.path.getsize(p) >= MIN_BYTES]
        if not hits:
            continue
        chuong = []
        if len(hits) == 1 and os.path.basename(hits[0]).lower().startswith('book'):
            text = io.open(hits[0], encoding='utf-8', errors='replace').read()
            chuong = tach_chuong(text, hits[0])
        else:
            for p in hits:
                chuong.append((os.path.basename(p)[:-3],
                               io.open(p, encoding='utf-8', errors='replace').read(), p))
        return nhan, chuong
    raise KhongDoDuoc(
        'không thấy bản thảo nào trong %s (đã thử: %s). Không có bản thảo thì không '
        'có gì để đo — đừng đọc đây là "0 vi phạm".'
        % (outdir, ', '.join(p for p, _ in pats)))


# Tiêu đề khối SAU SÁCH. Chúng kết thúc chương cuối và thành hàng riêng của mình.
SAU_SACH = re.compile(
    r'(?m)^#{1,2}\s+(?:Phụ\s*lục|Phu\s*luc|Appendix|Appendices|Tài\s*liệu\s*tham\s*khảo'
    r'|References|Bibliography|Index|Chỉ\s*mục|Lời\s*bạt|Afterword|Về\s*tác\s*giả)\b[^\n]*$'
)

# Khối ngắn hơn ngần này là DÒNG PHÂN CÁCH ("# Phụ lục" đứng một mình), không phải
# một khối nội dung. Gộp về khối sau, vì chấm nó như một khối riêng sẽ báo
# "thiếu dấu BẢN NỘI BỘ" trên một cuốn đã đóng dấu đủ — đúng lớp dương tính giả
# mà chú thích bên dưới đã kể.
TU_TOI_THIEU_KHOI = 60


def tach_chuong(text, path):
    """Cắt book.md đã hợp nhất theo tiêu đề chương. Không thấy tiêu đề thì trả cả cuốn.

    🔴 Chương cuối KHÔNG kéo đến hết tệp. Lỗi đo được (performance-by-design-v2,
    2026-09-23): chương cuối nuốt trọn ba phụ lục — bảng báo "Chương 17 = 19.930 từ"
    trong khi chương ấy thật sự có **4.963**, phần còn lại là 16.364 từ phụ lục.
    Dấu hiệu lộ ra: đoạn "nguyên văn ngoài ngoặc" mà bảng gán cho Chương 17 là chuỗi
    số `1 0 1 8 2 2 3 5 5 0` — nội dung của Phụ lục B (bảng tra), không phải của
    chương. Hậu quả không dừng ở một dòng sai: một phiên sau đó đọc con số 19.930,
    tin rằng "chương đậm chất Xưởng nhất nuôi được 20k từ", và suýt dựng cả kế hoạch
    một cuốn sách trên đó.

    Sai theo hướng AN TOÀN GIẢ: mẫu số phình ra nên mật độ chương cuối trông thấp
    hơn thật.
    """
    idx = [(m.start(), m.group(0).strip(), 'chuong')
    # Tiêu đề chương phải BẮT ĐẦU bằng "Chương"/"Chapter", không chỉ CHỨA chữ ấy.
    # Lỗi đo được (book.md inside-the-box, 2026-09-14): regex cũ cắt cả tiểu mục
    # "## Kết luận của chương" và "## Ăng-ten trong tuyết — ca kỹ thuật trung tâm
    # của chương" thành hai "chương" giả — và hai chương giả ấy dĩ nhiên không
    # mang dấu BẢN NỘI BỘ, nên cổng báo TRƯỢT trên một cuốn đã đóng dấu đủ.
    # Dương tính giả ở cổng đắt hơn nó trông: nó làm người đọc mất lòng tin vào
    # cả bảng, kể cả những dòng đúng. Đây là lần thứ TƯ trong dự án này.
    for m in re.finditer(r'(?m)^#{1,2}\s+(?:Chương|Chapter)\b[^\n]*$', text)]
    if not idx:
        return [(os.path.basename(path)[:-3], text, path)]

    # Khối sau sách chỉ tính khi nó nằm SAU chương cuối — "Phụ lục" nhắc giữa thân
    # sách không được cắt chương làm đôi.
    sau_chuong_cuoi = idx[-1][0]
    moc = idx + [(m.start(), m.group(0).strip(), 'sau')
                 for m in SAU_SACH.finditer(text) if m.start() > sau_chuong_cuoi]
    moc.sort(key=lambda x: x[0])

    tho = []
    for i, (pos, tieu_de, loai) in enumerate(moc):
        end = moc[i + 1][0] if i + 1 < len(moc) else len(text)
        nhan = re.sub(r'^#+\s*', '', tieu_de)[:48]
        if loai == 'sau':
            nhan = '[sau sách] ' + nhan
        tho.append([nhan, text[pos:end]])

    # Gộp dòng phân cách về khối liền sau. Không bỏ đi: bỏ thì tổng số từ hụt,
    # mà mọi tỷ lệ đều chia cho tổng ấy.
    out, treo = [], ''
    for nhan, doan in tho:
        if len(norm(doan).split()) < TU_TOI_THIEU_KHOI:
            treo += doan
            continue
        out.append((nhan, treo + doan, path))
        treo = ''
    if treo:
        if out:
            nhan, doan, p = out[-1]
            out[-1] = (nhan, doan + treo, p)
        else:
            out.append((os.path.basename(path)[:-3], treo, path))
    return out


# ---------------------------------------------------------- trích dẫn

def rut_trich(text):
    """Tách chuỗi trong ngoặc theo CẶP đồng bộ.

    Bug đã vá: regex một-lớp bắt nhầm phần chữ NẰM GIỮA hai trích dẫn (dấu đóng
    của trích A ghép với dấu mở của trích B). Kiểm bằng đột biến bốn nhánh:
    trích thật · trích bịa · trích lược thật · trích nửa thật nửa bịa.
    """
    out = []
    bt = chr(96)
    for i, seg in enumerate(text.split(bt)):
        if i % 2 == 1:
            out.append(seg)
    stripped = re.sub(bt + '[^' + bt + ']*' + bt, '', text)
    for i, seg in enumerate(stripped.split(chr(34))):
        if i % 2 == 1:
            out.append(seg)
    out += re.findall('“([^“”]{1,600})”', text)
    return out


def ty_le_viet(s):
    return len(re.findall(r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]',
                          s.lower())) / max(len(s), 1)


CT_TOAN = re.compile(r'[=≈≤≥/·×^√∑∫±]|\b\d+[,.]\d+\b')


def la_cong_thuc(q: str) -> bool:
    """Chuỗi này là CÔNG THỨC, không phải trích dẫn?

    🔴 Vì sao cần. Cổng này từng ra phán quyết **KHÔNG ĐẠT — 9 trích không đối chiếu được** cho
    `usv-thiet-ke-he-thong` (2026-10-01), và **7/9 là công thức**, không phải trích:
        Lp/Bpx = 2,00 · 3,06 · 4,09 · 5,50 · 7,00
        K_T/J_T² = T_P/[ρD²v²(1−W_T)²]
        PC_w = c_L·[ C_r·α·√W·√x + (C_p + C_s·√α)·t^1,5·l ] + W_s*·t²·l·c_W
    Chúng **không thể** khớp kho vì `norm()` nghiền mọi con số và ký hiệu — đó là thiết kế, không
    phải lỗi. Đếm chúng như trích bịa làm cổng báo sai bản chất: một cuốn sách kỹ thuật in công
    thức thì **luôn** trượt, và phán quyết «bịa hoặc sửa chữ» chĩa vào chỗ không có lỗi.

    Tiêu chí đo trên chính 9 ca ấy: **dưới 3 từ chữ cái dài ≥3** *và* có ít nhất một toán tử. Nó
    tách đúng 7 công thức khỏi 2 trích thật (`"I caution you to provide reinforced…"` và
    `"For production operations Figure 11.9 can be used"`), không cần điều chỉnh tay.
    """
    tu = [w for w in re.findall(r'[A-Za-zÀ-ỹ]{3,}', q)]
    return len(tu) < 3 and bool(CT_TOAN.search(q))


def kiem_trich(kho, q):
    """Kiểm một trích trên nhiều nguồn. Trả (trạng thái, trang, nhãn nguồn, số từ khớp).

    Xử dấu lược: NLM/người viết lược giữa câu bằng "..." nên khớp nguyên chuỗi
    luôn trượt. Cắt theo dấu lược rồi kiểm TỪNG MẢNH; mảnh nào không thấy thì đó
    là nửa bịa. Không xử thì báo "18 câu sai" trong khi 16/18 là thật.

    🔴 Lượt tra PHỤ (thêm 2026-10-01): lớp chữ PDF làm hỏng khoảng trắng theo HAI kiểu —
    **tách một từ thành hai** (`electroly tes`, `dead rise`) và **giãn từng chữ cái**
    (`r p r o d u c t i o n o p e r a t i o n s`, đúng ca P&B tr.548). Cả hai làm phép so chuỗi
    trượt trên câu **có in trong sách**.
    `quote_locate.py` đã được vá cho đúng lớp lỗi này (`dee8b59`), **nhưng tệp này cài phép tra
    RIÊNG** nên bản vá không bao giờ tới đây — và đây mới là cổng ra **phán quyết**. Hai gate, hai
    cách tra, một cái được vá. Nay cả hai bỏ hết khoảng trắng rồi so lại khi lượt chính trượt.
    """
    frags = [f for f in re.split(r'[.]{3}|…', q) if len(norm(f)) >= 25] or [q]
    tot = ('NOT-FOUND', None, None, 0)
    rank = {'FOUND': 3, 'FOUND-ELIDED': 3, 'FOUND-PARTIAL': 2, 'NOT-FOUND': 1}
    for src in kho:
        offs, miss, khop_tu = [], 0, 0
        for f in frags:
            nf = norm(f)
            o = src['corpus'].find(nf)
            if o < 0:
                # luot phu: bo HET khoang trang hai ben (xem docstring)
                if 'liet' not in src:
                    src['liet'] = src['corpus'].replace(' ', '')
                if len(nf.replace(' ', '')) >= 20 and nf.replace(' ', '') in src['liet']:
                    o = 0 if not offs else offs[-1]
                    khop_tu += len(nf.split())
                    offs.append(o)
                    continue
                w = nf.split()
                head = ' '.join(w[:max(6, int(len(w) * 0.6))])
                o = src['corpus'].find(head) if len(head) >= 25 else -1
                if o < 0:
                    miss += 1
                    continue
                khop_tu += len(head.split())
            else:
                khop_tu += len(nf.split())
            offs.append(o)
        if not offs:
            continue
        st = 'FOUND-PARTIAL' if miss else ('FOUND' if len(frags) == 1 else 'FOUND-ELIDED')
        cand = (st, trang_cua(src['pagemap'], min(offs)), src['label'], khop_tu)
        if rank[st] > rank[tot[0]]:
            tot = cand
        if rank[st] == 3:
            break
    return tot


# ------------------------------------------- nguyên văn KHÔNG ngoặc (n-gram)

def tap_ngram(corpus, n):
    w = corpus.split()
    return {' '.join(w[i:i + n]) for i in range(len(w) - n + 1)}


def quet_ngoai_ngoac(text, ngram_theo_nguon, n):
    """Bỏ mọi phần trong ngoặc rồi quét n-gram trùng khít kho gốc.

    Đây là vùng mù của cổng trích dẫn: chép nguyên đoạn mà KHÔNG đóng ngoặc thì
    cổng cũ không bao giờ nhìn thấy, dù đó mới là dạng nặng hơn (không ghi nguồn).

    Trả [(nhãn nguồn, đoạn)] — phải quy về ĐÚNG nguồn, vì tỷ lệ bao phủ tính
    riêng cho từng cuốn (xem `audit`).
    """
    bt = chr(96)
    t = re.sub(bt + '[^' + bt + ']*' + bt, ' ', text)
    t = re.sub(chr(34) + '[^' + chr(34) + ']*' + chr(34), ' ', t)
    t = re.sub('“[^”]*”', ' ', t)
    w = norm(t).split()
    hit = [None] * max(len(w) - n + 1, 0)
    for i in range(len(hit)):
        g = ' '.join(w[i:i + n])
        for nhan, tap in ngram_theo_nguon.items():
            if g in tap:
                hit[i] = nhan
                break
    runs, i = [], 0
    while i < len(hit):
        if hit[i] is None:
            i += 1
            continue
        j = i
        while j + 1 < len(hit) and hit[j + 1] == hit[i]:
            j += 1
        runs.append((hit[i], ' '.join(w[i:j + n])))
        i = j + 1
    return runs


# ------------------------------------------------------------- câu trần

def quet_cau_tran(text, nguon_nhan):
    """Trả (danh sách câu trần, số dòng bảng đã bỏ qua).

    Dòng bảng Markdown bị BỎ QUA: một dòng như `| bản gốc | bản này | ghi chú |`
    khớp regex quy kết (chủ ngữ "bản gốc" + động từ "ghi") nhưng nó là **dữ liệu**,
    không phải một câu khẳng định về nguồn. Đo được trên book.md inside-the-box
    2026-09-14: bảng thuật ngữ sinh 1 dương tính giả.

    Nhưng bỏ qua IM LẶNG thì vi phạm chính luật rút ra ở P6 — *mọi cổng phải in ra
    thứ nó KHÔNG nhìn thấy, cùng chỗ với kết quả nó nhìn thấy*. Nên hàm này **đếm
    và trả về** số dòng đã bỏ, để báo cáo in ra.
    """
    subj = '(?:' + '|'.join(re.escape(x) for x in nguon_nhan) + ')'
    claim = re.compile(subj + r'[^.\n]{0,60}?\s' + VERB + r'\b', re.IGNORECASE)
    lines = text.split('\n')
    tran, bo_bang = [], 0
    for ln, raw in enumerate(lines, start=1):
        if raw.lstrip().startswith('|'):
            if claim.search(raw):
                bo_bang += 1
            continue
        for s in re.split(r'(?<=[.!?:])\s+', raw):
            s = s.strip()
            if not s or not claim.search(s):
                continue
            # Cua so neo +-4 dong, KHONG phai +-2. Ly do do duoc (Ch04 inside-the-box,
            # 2026-09-14): cau dan "...Zuckerberg noi:" roi DONG TRONG roi khoi trich
            # `> *"..."*` nam cach 3 dong -> cua so +-2 bao 4 cau tran trong khi ca 4 deu
            # CO neo. Duong tinh gia lam nguoi doc mat long tin vao ca bang. Noi THEM nua
            # thi cam bien bat dau nhan nham mot trich dan KHONG lien quan lam neo.
            lo, hi = max(0, ln - 5), min(len(lines), ln + 4)
            cua_so = '\n'.join(lines[lo:hi])
            if not HAS_QUOTE.search(cua_so) and not HAS_PAGE.search(cua_so):
                tran.append((ln, s[:180]))
    return tran, bo_bang


# ----------------------------------------------------------------- chạy

def audit(outdir, level, min_run, pattern, nguon_nhan):
    khai = doc_khai_bao(outdir, level)
    kho = doc_kho(outdir)
    bo, chuong = doc_ban_thao(outdir, pattern)

    tu_goc = sum(s['words'] for s in kho)
    # Tập n-gram RIÊNG cho từng nguồn. Gộp chung vào một tập thì không quy được
    # đoạn nguyên văn về đúng cuốn nào — và tỷ lệ bao phủ bắt buộc phải tính
    # riêng từng cuốn (xem chỗ tính `bao_phu_theo` bên dưới).
    ngram_theo_nguon = {s['label']: tap_ngram(s['corpus'], min_run) for s in kho}
    tu_theo_nguon = {s['label']: 0 for s in kho}

    # Nguồn ngoại ngữ thì câu tiếng Việt trong ngoặc là lời của người viết, không
    # phải trích — bỏ qua để khỏi báo "NOT-FOUND" hàng loạt (dương tính giả).
    nguon_ngoai_ngu = ty_le_viet(kho[0]['corpus'][:20000]) < 0.02

    hang, bia, thieu_dau, cau_tran = [], [], [], []
    bo_bang_tong = 0
    tong_tu = 0
    for nhan, text, path in chuong:
        tu = len(norm(text).split())
        tong_tu += tu
        if not STAMP.search(bo_dau(text)):
            thieu_dau.append((nhan, path))

        tu_trich, seen = 0, set()
        for cand in rut_trich(text):
            q = cand.strip()
            if not (25 <= len(q) <= 600) or LA_DUONG_DAN.search(q):
                continue
            if nguon_ngoai_ngu and ty_le_viet(q) > 0.02:
                continue
            if la_cong_thuc(q):
                continue          # công thức, không phải trích — xem la_cong_thuc()
            k = norm(q)[:80]
            if len(k) < 25 or k in seen:
                continue
            seen.add(k)
            st, trang, src, khop = kiem_trich(kho, q)
            if st == 'NOT-FOUND':
                bia.append((nhan, q[:120]))
            else:
                tu_trich += khop
                tu_theo_nguon[src] = tu_theo_nguon.get(src, 0) + khop
                if st == 'FOUND-PARTIAL':
                    bia.append((nhan, '[NỬA BỊA] ' + q[:110]))

        runs = quet_ngoai_ngoac(text, ngram_theo_nguon, min_run)
        tu_ngoai = 0
        for src_nhan, doan in runs:
            n_tu = len(doan.split())
            tu_ngoai += n_tu
            tu_theo_nguon[src_nhan] = tu_theo_nguon.get(src_nhan, 0) + n_tu
        _ct, _bo = quet_cau_tran(text, nguon_nhan)
        bo_bang_tong += _bo
        cau_tran += [(nhan, ln, s) for ln, s in _ct]
        hang.append(dict(nhan=nhan, tu=tu, trich=tu_trich, ngoai=tu_ngoai,
                         runs=runs[:3], path=path))

    tu_nguyen_van = sum(h['trich'] + h['ngoai'] for h in hang)

    # 🔴 CÙNG NGÔN NGỮ HAY KHÁC NGÔN NGỮ — quyết định phép đo có nghĩa hay không.
    # Phát hiện khi chạy thật (chương mẫu inside-the-box, 2026-09-14): một chương
    # DỊCH TRỌN VẸN 10.811 từ tiếng Anh sang 10.193 từ tiếng Việt chỉ đo được 99 từ
    # nguyên văn → mật độ 1,0%, cổng báo ĐẠT. Con số ấy đúng nhưng bị đọc sai: nó đo
    # NGÂN SÁCH TRÍCH, không đo mức độ phái sinh. Vùng mù này KHÔNG chỉ có ở F4 như
    # bản đầu tiên của script giả định — nó có ở MỌI mức khi hai bên khác ngôn ngữ.
    viet_sach = ty_le_viet(' '.join(norm(t) for _, t, _ in chuong)[:40000])
    khac_ngon_ngu = nguon_ngoai_ngu and viet_sach > 0.02

    # 🔴 BAO PHỦ TÍNH RIÊNG TỪNG NGUỒN, rồi lấy CUỐN BỊ TÁI TẠO NHIỀU NHẤT.
    # Cộng dồn mẫu số của mọi nguồn là một âm tính giả trông rất hợp lý: nạp
    # thêm một cuốn nền (việc PHẢI làm để khỏi báo oan trích dẫn hợp lệ) sẽ pha
    # loãng mẫu số và kéo tỷ lệ xuống. Đo thật trên cuốn cross-design-methods:
    # gộp mẫu số ra 3,90%, tính riêng ra 16,02% — mà 16,07% mới là số đo tay.
    # Câu hỏi bản quyền luôn là "tôi tái tạo bao nhiêu phần CỦA MỘT TÁC PHẨM",
    # không bao giờ là "bao nhiêu phần của cả cái thư viện tôi đã đọc".
    bao_phu_theo = {s['label']: 100.0 * tu_theo_nguon.get(s['label'], 0) / max(s['words'], 1)
                    for s in kho}
    bao_phu = max(bao_phu_theo.values()) if bao_phu_theo else 0.0
    nguon_rang_buoc = max(bao_phu_theo, key=bao_phu_theo.get) if bao_phu_theo else '-'
    mat_do = 100.0 * tu_nguyen_van / max(tong_tu, 1)
    tran = LEVELS[level]

    # ---------------------------------------------------------- phán quyết
    loi = []
    if bia:
        loi.append('%d trích không đối chiếu được với kho gốc (bịa hoặc sửa chữ)' % len(bia))
    if thieu_dau:
        loi.append('%d tệp thiếu dấu "BẢN NỘI BỘ"' % len(thieu_dau))
    if tran['bao_phu'] is not None:
        if bao_phu > tran['bao_phu']:
            loi.append('bao phủ %.2f%% trên "%s" > trần %s %.1f%%'
                       % (bao_phu, nguon_rang_buoc, level, tran['bao_phu']))
        if mat_do > tran['mat_do']:
            loi.append('mật độ %.2f%% > trần %s %.1f%%' % (mat_do, level, tran['mat_do']))

    bao_cao = ket_xuat(outdir, khai, kho, bo, hang, tu_goc, tong_tu, tu_nguyen_van,
                       bao_phu, mat_do, level, tran, bia, thieu_dau, cau_tran,
                       min_run, loi, bao_phu_theo, tu_theo_nguon, nguon_rang_buoc,
                       khac_ngon_ngu, bo_bang_tong)
    print(bao_cao)
    return 1 if loi else 0


def ket_xuat(outdir, khai, kho, bo, hang, tu_goc, tong_tu, tu_nv, bao_phu, mat_do,
             level, tran, bia, thieu_dau, cau_tran, min_run, loi,
             bao_phu_theo, tu_theo_nguon, nguon_rang_buoc, khac_ngon_ngu=False,
             bo_bang_tong=0):
    L = []
    a = L.append
    a('=' * 78)
    a('CỔNG NGUYÊN BẢN — %s  (%s)' % (level, tran['ten']))
    a('=' * 78)
    a('  khai báo P0  : %s · CEO ký %s · phạm vi NỘI BỘ' % (khai['level'], khai['ky']))
    a('  kho gốc      : %s (%d từ)' % (', '.join(s['label'] for s in kho), tu_goc))
    a('  bản thảo đo  : %s — %d chương, %d từ' % (bo, len(hang), tong_tu))
    a('  ngưỡng chuỗi : %d từ liên tiếp tính là nguyên văn' % min_run)
    a('')
    a('  TỪ NGUYÊN VĂN: %d   (trích có ngoặc %d + ngoài ngoặc %d)'
      % (tu_nv, sum(h['trich'] for h in hang), sum(h['ngoai'] for h in hang)))
    if tran['bao_phu'] is None:
        a('  bao phủ / mật độ: %.2f%% / %.2f%%' % (bao_phu, mat_do))
        a('')
        a('  🔴 Ở F4 HAI SỐ TRÊN KHÔNG CÓ NGHĨA. Bản dịch sát nguyên bản tái tạo ~100%')
        a('     tác phẩm gốc theo thiết kế, nhưng nó là tiếng Việt nên không khớp chuỗi')
        a('     với bản gốc tiếng Anh — cảm biến trả số thấp và số thấp ấy là MÙ, không')
        a('     phải sạch. F4 được cai trị bằng KHAI BÁO + KHOÁ PHÁT TÁN, không bằng số.')
    else:
        a('  bao phủ (cuốn bị tái tạo nhiều nhất: "%s"): %.2f%%   trần %s = %.1f%%   %s'
          % (nguon_rang_buoc, bao_phu, level, tran['bao_phu'],
             'ĐẠT' if bao_phu <= tran['bao_phu'] else 'VƯỢT'))
        a('  mật độ  (trên sách mình): %.2f%%   trần %s = %.1f%%   %s'
          % (mat_do, level, tran['mat_do'], 'ĐẠT' if mat_do <= tran['mat_do'] else 'VƯỢT'))
    a('')
    if khac_ngon_ngu:
        a('  🔴 KHÁC NGÔN NGỮ — HAI SỐ TRÊN CHỈ ĐO NGÂN SÁCH TRÍCH, KHÔNG ĐO MỨC PHÁI SINH.')
        a('     Bản thảo là tiếng Việt, kho gốc là ngoại ngữ, nên phép so chuỗi chỉ nhìn thấy')
        a('     những đoạn còn để nguyên văn. Một chương DỊCH TRỌN một chương gốc vẫn ra vài')
        a('     phần trăm — và vài phần trăm ấy là MÙ, không phải sạch.')
        a('     Ở cặp khác ngôn ngữ, thứ cai trị mức phái sinh là **bảng ánh xạ chương ở P3**')
        a('     cộng lời khai P0, y như cách F4 được cai trị. Đọc con số dưới đây đúng một')
        a('     nghĩa: "tôi đã tiêu bao nhiêu phần ngân sách trích được phép".')
        a('')
    if len(kho) > 1:
        a('| nguồn | từ gốc | từ bị tái tạo | bao phủ |')
        a('|---|---:|---:|---:|')
        for s_ in kho:
            a('| %s | %d | %d | %.2f%% |'
              % (s_['label'], s_['words'], tu_theo_nguon.get(s_['label'], 0),
                 bao_phu_theo.get(s_['label'], 0.0)))
        a('')
        a('Bao phủ tính RIÊNG từng cuốn rồi lấy cuốn cao nhất. Cộng gộp mẫu số của mọi')
        a('nguồn sẽ pha loãng tỷ lệ: nạp thêm một cuốn nền — việc phải làm để khỏi báo oan')
        a('trích dẫn hợp lệ — tự nó kéo con số xuống mà không có chữ nào được sửa.')
        a('')
    a('| chương | từ | trích | ngoài ngoặc | mật độ chương |')
    a('|---|---:|---:|---:|---:|')
    for h in sorted(hang, key=lambda x: -(x['trich'] + x['ngoai'])):
        md = 100.0 * (h['trich'] + h['ngoai']) / max(h['tu'], 1)
        a('| %s | %d | %d | %d | %.1f%% |'
          % (h['nhan'].replace('|', '/')[:46], h['tu'], h['trich'], h['ngoai'], md))
    a('')
    if bia:
        a('## 🔴 Trích KHÔNG đối chiếu được (%d)' % len(bia))
        for nhan, q in bia[:25]:
            a('- **%s** — %s' % (nhan, q.replace('|', '/')))
        if len(bia) > 25:
            a('- … còn %d ca nữa' % (len(bia) - 25))
        a('')
    nv_ngoai = [(h['nhan'], '[%s] %s' % (src, r)) for h in hang for src, r in h['runs']]
    if nv_ngoai:
        a('## ⚠️ Đoạn nguyên văn NGOÀI ngoặc (mẫu, tối đa 3/chương)')
        a('Chép đúng chữ mà không đóng ngoặc: cổng trích dẫn cũ mù hoàn toàn với dạng này.')
        for nhan, r in nv_ngoai[:20]:
            a('- **%s** — %s…' % (nhan, r[:140]))
        a('')
    if thieu_dau:
        a('## 🔴 Thiếu dấu "BẢN NỘI BỘ" (%d tệp)' % len(thieu_dau))
        for nhan, p in thieu_dau[:20]:
            a('- %s (%s)' % (nhan, p))
        a('')
    a('## Câu quy kết nguồn không có neo (%d)' % len(cau_tran))
    if bo_bang_tong:
        a('')
        a('> ⚠️ **Đã BỎ QUA %d dòng bảng Markdown** khớp mẫu quy kết. Dòng bảng là dữ liệu,'
          % bo_bang_tong)
        a('> không phải câu khẳng định về nguồn. Khai ra đây vì bỏ qua im lặng cũng là một')
        a('> vùng mù — nếu một bảng thật sự chứa khẳng định về nguồn, cổng này sẽ không thấy.')
    a('Script KHÔNG phán đúng/sai câu nào — việc đó cần người đọc. Nó chỉ bảo đảm')
    a('không câu nào lọt khỏi tầm mắt. Đây đúng là chỗ một chương từng gán cho tác giả')
    a('một thang điểm ông không hề nêu, rồi dựng chuẩn toàn Xưởng lên tiền đề sai ấy.')
    a('')
    for nhan, ln, s in cau_tran[:30]:
        a('- **%s** dòng %d — %s' % (nhan, ln, s.replace('|', '/')))
    if len(cau_tran) > 30:
        a('- … còn %d câu nữa' % (len(cau_tran) - 30))
    a('')
    a('## 🕳️ CỔNG NÀY KHÔNG NHÌN THẤY GÌ')
    a('Lỗi sẽ di cư sang đúng những chỗ dưới đây — đã xảy ra rồi, không phải giả định:')
    a('')
    a('1. **Cắt câu làm đảo nghĩa.** Bỏ mệnh đề sau dấu phẩy đảo được nghĩa mà không sai')
    a('   một chữ nào; bản dịch đúng từng chữ của một câu đã bị cắt vẫn là bản dịch đúng.')
    a('2. **Chép CẤU TRÚC.** Đi đúng thứ tự lập luận và thứ tự chương của bản gốc là sự')
    a('   thật về tác phẩm phái sinh mà không phép so chuỗi nào bắt được.')
    a('3. **Số liệu tự khai.** "hai trăm tám mươi ba trang cách nhau" giữa tr.273 và')
    a('   tr.456 — thật là 183, lặp 2 lần. Không lượt soát nào của đường ống làm phép trừ.')
    a('4. **Diễn giải sát mà không ngoặc, dưới %d từ liên tiếp.** Hạ `--min-run` thì bắt' % min_run)
    a('   thêm nhưng nhiễu tăng; số hiện tại là đánh đổi, không phải chân lý.')
    a('5. **Mức phái sinh khi khác ngôn ngữ.** Phép so chuỗi mù với bản dịch. Bảng ánh xạ')
    a('   chương ở P3 là thứ DUY NHẤT ghi lại việc ta đã bám cấu trúc của ai tới đâu.')
    a('6. **Neo lệch trang.** Số trang in ở đây suy từ running header; trang mở chương')
    a('   thường không có header nên được nội suy. Kiểm tay vài mốc trước khi trích dẫn.')
    a('')
    a('## _gate — khối ấn để `--verify` đối chiếu về sau')
    a('')
    a('Băm từng tệp bản thảo tại lúc đo. `--verify` so lại băm này, không so ngày sửa —')
    a('sửa xong rồi `touch` ngược thì ngày nói dối, băm thì không.')
    a('')
    a('```json b2b-gate')
    a(json.dumps(dict(
        level=level,
        phan_quyet='KHONG_DAT' if loi else 'DAT',
        ceo_ky=khai['ky'],
        bao_phu=round(bao_phu, 3),
        nguon_rang_buoc=nguon_rang_buoc,
        bao_phu_theo_nguon={k: round(v, 3) for k, v in bao_phu_theo.items()},
        mat_do=round(mat_do, 3),
        tu_goc=tu_goc,
        tu_sach=tong_tu,
        tu_nguyen_van=tu_nv,
        min_run=min_run,
        khac_ngon_ngu=khac_ngon_ngu,
        nguon={s['label']: (s['meta'].get('sha256') or '')[:16] for s in kho},
        ban_thao={k: v for k, v in sorted(
            {os.path.relpath(h['path'], outdir).replace('\\', '/'): bam(h['path'])
             for h in hang}.items())},
    ), ensure_ascii=False, indent=1))
    a('```')
    a('')
    a('=' * 78)
    if loi:
        a('PHÁN QUYẾT: ❌ KHÔNG ĐẠT — ' + ' · '.join(loi))
        a('CẤM trình CEO checkpoint P7. Hạ lượng trích, ghi nguồn, hoặc khai lại mức')
        a('nguyên bản ở P0 (và nói rõ vì sao đổi) rồi chạy lại.')
    else:
        a('PHÁN QUYẾT: ✅ ĐẠT mức %s — trong trần, không trích bịa, đủ dấu nội bộ.' % level)
        a('Vẫn đọc mục "CỔNG NÀY KHÔNG NHÌN THẤY GÌ" trước khi ký.')
    a('=' * 78)
    out = '\n'.join(L)
    try:
        io.open(os.path.join(outdir, 'Phase7-Fidelity-Report.md'), 'w',
                encoding='utf-8', newline='\n').write(out + '\n')
    except OSError as e:
        out += '\n!! không ghi được Phase7-Fidelity-Report.md: %r' % (e,)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description='Cổng nguyên bản cho /book-to-book')
    ap.add_argument('outdir', help='thư mục Data Bus của cuốn sách')
    ap.add_argument('--level', required=True, choices=sorted(LEVELS),
                    help='mức nguyên bản đã khai ở P0')
    ap.add_argument('--min-run', type=int, default=10,
                    help='số từ liên tiếp tối thiểu tính là nguyên văn (mặc định 10)')
    ap.add_argument('--book', default=None, help='glob bản thảo (mặc định: dò theo thứ tự pha)')
    ap.add_argument('--nguon', default='',
                    help='tên tác giả/nguồn, phân cách dấu phẩy, để quét câu quy kết')
    ap.add_argument('--verify', action='store_true',
                    help='không đo lại; chỉ xác nhận báo cáo P7 còn đúng với bản thảo '
                         'hiện tại (điều kiện vào P7.5/P8)')
    a = ap.parse_args(argv)

    nhan = [x.strip() for x in a.nguon.split(',') if x.strip()]
    if not nhan:
        nhan = ['tác giả', 'nguyên tác', 'sách gốc']
    try:
        if a.verify:
            return verify(a.outdir, a.level, a.book)
        return audit(a.outdir, a.level, a.min_run, a.book, nhan)
    except KhongDoDuoc as e:
        print('=' * 78)
        print('KHÔNG ĐO ĐƯỢC — %s' % e)
        print('=' * 78)
        print('Mã thoát 2 KHÔNG phải "sạch". Không có phép đo nào đã chạy.')
        return 2


if __name__ == '__main__':
    sys.exit(main())
