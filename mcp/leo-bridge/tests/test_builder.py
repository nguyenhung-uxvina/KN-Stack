import pytest

from leo_bridge import builder


def test_mode_a_fills_fields_and_assumptions():
    p = builder.build_prompt(
        "A",
        {
            "FUNCTION": "đỡ trục quay Ø25, tải hướng kính",
            "ENVELOPE": "OD ≤ 52 mm, rộng ≤ 15 mm, lỗ Ø25 H7",
            "SPEC": "tải 2 kN, 3000 rpm, nhiệt ≤ 80°C",
            "SOURCE": "kho vendor 120M",
        },
        assumptions=["tải tĩnh", "bôi trơn mỡ"],
    )
    assert "[FUNCTION] đỡ trục quay Ø25, tải hướng kính" in p
    assert "[Phân loại: THƯỜNG]" in p
    assert "[GIẢ ĐỊNH] tải tĩnh · bôi trơn mỡ" in p
    # 5 nguyên tắc: search-before-generate giữ nguyên từ template [ASK]
    assert "tái dùng" in p or "thiết kế mới" in p


def test_missing_required_field_raises_with_names():
    with pytest.raises(builder.BuildError) as e:
        builder.build_prompt("C", {"GOAL": "tính FoS"})
    assert "KNOWNS" in str(e.value)
    assert "UNKNOWN" in str(e.value)


def test_invalid_mode_raises():
    with pytest.raises(builder.BuildError):
        builder.build_prompt("Z", {})


def test_lowercase_param_keys_accepted():
    p = builder.build_prompt(
        "B",
        {"question": "dung sai H7/g6 trục Ø25?", "context": "thép C45"},
    )
    assert "[QUESTION] dung sai H7/g6" in p


def test_mode_f_requirements_continuation_consumed():
    p = builder.build_prompt(
        "F",
        {
            "PART": "bạc lót trục Ø40",
            "REQUIREMENTS": "tải 500 N; nhiệt 60°C; ưu tiên cost",
            "PROCESS": "tiện CNC",
        },
    )
    assert "[REQUIREMENTS] tải 500 N" in p
    assert "Ưu tiên: [cost" not in p
    assert "3–5 vật liệu" in p or "Trade-off" in p


def test_ask_block_not_swallowed():
    p = builder.build_prompt(
        "A",
        {
            "FUNCTION": "đỡ trục quay Ø25, tải hướng kính",
            "ENVELOPE": "OD ≤ 52 mm, rộng ≤ 15 mm, lỗ Ø25 H7",
            "SPEC": "tải 2 kN, 3000 rpm, nhiệt ≤ 80°C",
            "SOURCE": "kho vendor 120M",
        },
    )
    assert "Liệt kê 5 part ứng viên" in p
