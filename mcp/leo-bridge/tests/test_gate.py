from leo_bridge import gate


def test_generic_bearing_is_thuong():
    r = gate.classify("Tìm bạc đạn SKF 6205 chịu tải hướng kính 2 kN, trục Ø25")
    assert r.verdict == "THUONG"
    assert r.hits == []
    assert r.redacted is None


def test_uuv_context_is_mat_with_redaction():
    r = gate.classify("Chọn bạc lót cho GIÁ TRƯỢT UUV, tải 3 kN")
    assert r.verdict == "MAT"
    terms = {h.term.lower() for h in r.hits}
    assert "uuv" in terms
    assert "giá trượt" in terms
    assert "UUV" not in r.redacted
    assert "[REDACTED]" in r.redacted
    assert "3 kN" in r.redacted  # thông số kỹ thuật giữ nguyên


def test_product_code_and_english_terms_hit():
    r = gate.classify("bracket for V-SMASH-127 towed radar target winch")
    assert r.verdict == "MAT"
    cats = {h.category for h in r.hits}
    assert "product_code" in cats


def test_drawing_pattern_hits():
    r = gate.classify("theo bản vẽ TN-03-02-000 revision B")
    assert r.verdict == "MAT"


def test_load_denylist_missing_key_fails():
    import pytest
    with pytest.raises(ValueError):
        gate._validate_denylist({"product_codes": []})


def test_drawing_hit_term_is_matched_text():
    r = gate.classify("theo bản vẽ TN-03-02-000")
    assert any(h.term == "TN-03-02-000" and h.category == "drawing_pattern" for h in r.hits)


def test_lowercase_generic_codename_words_are_thuong():
    r = gate.classify("the sentinel value returns a verdict on the bastion of quality")
    assert r.verdict == "THUONG"


def test_overlapping_hits_redact_merged():
    r = gate.classify("bạc cho VN-XUONG-UUV chịu 2 kN")
    assert r.verdict == "MAT"
    assert "UUV" not in r.redacted
    assert "2 kN" in r.redacted
