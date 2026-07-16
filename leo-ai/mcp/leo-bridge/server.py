"""leo-bridge MCP server — cầu nối bán tự động Workshop X ↔ getleo.ai.

100% local: không network call. Transport = clipboard (API stub chờ Leo cấp access).
Doctrine: gate MẬT hard-block (2 lần) · propose-only · mọi số Leo = UNVERIFIED tới khi CEO verify.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from mcp.server.fastmcp import FastMCP

from leo_bridge import builder, gate, parsers, router, templates
from leo_bridge.ledger import Ledger
from leo_bridge.transports import get_transport

LEDGER_DIR = Path(os.environ.get("LEO_BRIDGE_LEDGER_DIR", str(Path(__file__).parent / "ledger")))

mcp = FastMCP("leo-bridge")
_ledger = Ledger(LEDGER_DIR)


@mcp.tool()
def leo_classify(task_text: str) -> dict:
    """Gate MẬT (bước 1, bắt buộc): phân loại THUONG/MAT bằng denylist deterministic.
    MAT → trả bản redacted để CEO viết lại prompt trừu tượng hóa (chức năng + thông số generic,
    KHÔNG tên khí tài). Hard block — không có override gửi nguyên bản."""
    r = gate.classify(task_text)
    return {
        "verdict": r.verdict,
        "hits": [{"term": h.term, "category": h.category} for h in r.hits],
        "redacted": r.redacted,
        "next": "THUONG → leo_prompt_build. MAT → trừu tượng hóa rồi classify lại.",
    }


@mcp.tool()
def leo_prompt_build(mode: str, params: dict, assumptions: list[str] | None = None) -> dict:
    """Sinh prompt Leo theo mode A/B/C/D/E1/E2/E3/F từ template leo-assist (source of truth).
    Ép 5 nguyên tắc: load case định lượng, interface thật, process, cite bắt buộc,
    search-before-generate. Thiếu tham số bắt buộc → lỗi liệt kê rõ."""
    scan_text = " ".join(str(v) for v in params.values())
    if assumptions:
        scan_text += " " + " ".join(str(a) for a in assumptions)
    c = gate.classify(scan_text)
    classification = "THƯỜNG" if c.verdict == "THUONG" else "MẬT→generic/COTS only"
    prompt = builder.build_prompt(mode, params, classification, assumptions)
    return {
        "prompt": prompt,
        "gate_verdict": c.verdict,
        "gate_hits": [h.term for h in c.hits],
        "warning": None if c.verdict == "THUONG" else
            "Params chứa context MẬT — leo_send SẼ CHẶN. Trừu tượng hóa trước.",
    }


# Map mode → nhóm intent trên UI chat thống nhất của app.getleo.ai
# (xác nhận theo screenshot CEO 2026-07-05: 1 khung chat, 4 nhóm gợi ý)
UI_INTENT = {
    "A": "Part search",
    "B": "Learn (lý thuyết/tiêu chuẩn) hoặc Develop (how-to/best-practice)",
    "C": "Calculate (có thể yêu cầu Leo vẽ plot)",
    "D": "Develop (DFM/design practices)",
    "E1": "chat thường — yêu cầu 9-point engineering summary",
    "E2": "chat thường — yêu cầu datasheet/BOM-text",
    "E3": "Part search (kèm yêu cầu kéo mfg-data)",
    "F": "Calculate (so vật liệu định lượng) hoặc Learn",
}


@mcp.tool()
def leo_send(prompt: str, mode: str, note: str = "") -> dict:
    """Gate lần 2 (defense-in-depth, hard block) → copy prompt vào clipboard →
    tạo exchange_id + ghi ledger. CEO dán vào app.getleo.ai (1 khung chat thống nhất)."""
    if mode.upper() not in builder.REQUIRED_FIELDS:
        return {
            "status": "ERROR",
            "reason": f"Mode không hợp lệ: {mode}. Hợp lệ: A/B/C/D/E1/E2/E3/F",
        }
    r = gate.classify(prompt)
    if r.verdict == "MAT":
        return {
            "status": "BLOCKED",
            "reason": "Prompt chứa context MẬT — TUYỆT ĐỐI không gửi lên Leo cloud (spec §2, doctrine leo-assist).",
            "hits": [h.term for h in r.hits],
            "redacted_suggestion": r.redacted,
            "action": "Thay tên khí tài/mã dự án bằng chức năng + thông số generic rồi leo_send lại.",
        }
    ex_id = _ledger.new_id()
    transport = get_transport()
    instructions = transport.send(prompt)
    intent = UI_INTENT[mode.upper()]
    instructions += f" Gợi ý UI: prompt này thuộc nhóm '{intent}' — dán vào khung chat chung, dòng [MODE] đầu prompt sẽ giúp Leo route đúng."
    _ledger.append(ex_id, "created", status="SENT", mode=mode.upper(), note=note,
                   transport=transport.name, classification="THUONG", prompt=prompt)
    return {"status": "SENT", "exchange_id": ex_id, "instructions": instructions}


@mcp.tool()
def leo_ingest(exchange_id: str) -> dict:
    """Đọc kết quả Leo từ clipboard → parse theo mode → verify checklist
    (mọi số/part = UNVERIFIED) → đề xuất đích. PROPOSE-ONLY: không ghi gì."""
    ex = _ledger.get(exchange_id)
    raw = get_transport().receive()
    parsed, checklist = parsers.parse_result(ex["mode"], raw)
    routes = router.propose_routes(ex["mode"], parsed)
    _ledger.append(exchange_id, "ingested", status="INGESTED",
                   raw=raw, parsed=parsed, checklist=checklist)
    return {
        "exchange_id": exchange_id,
        "parsed": parsed,
        "verify_checklist": checklist,
        "proposed_routes": routes,
        "note": "Propose-only. CEO mở nguồn verify từng mục → leo_route(verified_items=[...], confirm=true).",
    }


@mcp.tool()
def leo_route(exchange_id: str, target_type: str, target_path: str,
              confirm: bool = False, verified_items: list[int] | None = None) -> dict:
    """Ghi kết quả đã duyệt vào đích (parts_master_csv STAGING / journal_md / calc_md).
    confirm=true = CEO đã ra lệnh rõ. verified_items = index checklist CEO ĐÃ mở nguồn xác minh.
    Mục UNVERIFIED bị CHẶN vào parts_master_csv."""
    ex = _ledger.get(exchange_id)
    if ex.get("status") not in ("INGESTED", "ROUTED"):
        return {
            "status": "BLOCKED",
            "reason": f"Exchange {exchange_id} đang ở status {ex.get('status')} — chưa có kết quả ingest. Gọi leo_ingest trước.",
        }
    checklist = ex.get("checklist", [])
    if verified_items:
        for i in verified_items:
            if 0 <= i < len(checklist):
                checklist[i]["status"] = "VERIFIED"
        _ledger.append(exchange_id, "verified", checklist=checklist)
        ex["checklist"] = checklist
    written = router.write_route(ex, target_type, target_path, confirm=confirm)
    _ledger.append(exchange_id, "routed", status="ROUTED",
                   target_type=target_type, target_path=written)
    return {"status": "ROUTED", "written": written}


@mcp.tool()
def leo_ledger(action: str = "list", exchange_id: str = "", status: str = "") -> dict:
    """Traceability. action=list (lọc status tùy chọn) | show (cần exchange_id) | pending
    (SENT chưa ingest + INGESTED chưa route)."""
    if action == "show":
        return _ledger.get(exchange_id)
    if action == "pending":
        rows = _ledger.list("SENT") + _ledger.list("INGESTED")
        return {"rows": [
            {k: r.get(k) for k in ("exchange_id", "status", "mode", "ts", "note")} for r in rows
        ]}
    rows = _ledger.list(status or None)
    return {"rows": [
        {k: r.get(k) for k in ("exchange_id", "status", "mode", "ts", "note")} for r in rows
    ]}


def _selftest() -> None:
    t = templates.load_templates()
    assert set(t) == {"A", "B", "C", "D", "E1", "E2", "E3", "F"}, f"templates: {sorted(t)}"
    assert gate.classify("bạc đạn SKF 6205 chịu 2 kN").verdict == "THUONG"
    assert gate.classify("bạc lót cho UUV").verdict == "MAT"
    # "_" là separator, không phải word char — slug snake_case không được lọt gate
    assert gate.classify("goi Xuong_UUV_CoKhi").verdict == "MAT"
    assert gate.classify("he fire_control_v2").verdict == "MAT"
    # ...nhưng term dính liền trong từ khác vẫn không match oan
    assert gate.classify("UUVN co so").verdict == "THUONG"
    p = builder.build_prompt("B", {"QUESTION": "dung sai H7/g6 cho trục Ø25?",
                                   "CONTEXT": "thép C45, lắp trượt"})
    assert "[QUESTION] dung sai H7/g6" in p
    print("selftest OK — 8 templates, gate + builder hoạt động. Tools: leo_classify, "
          "leo_prompt_build, leo_send, leo_ingest, leo_route, leo_ledger")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if "--selftest" in sys.argv:
        _selftest()
    else:
        mcp.run()
