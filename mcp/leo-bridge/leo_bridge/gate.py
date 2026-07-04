"""Computational Sensor — gate MẬT cho leo-bridge. Deterministic, KHÔNG LLM, hard block."""
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

DENYLIST_PATH = Path(__file__).parent / "denylist.yaml"
REQUIRED_KEYS = ("product_codes", "codenames", "defense_terms", "drawing_patterns")


@dataclass
class Hit:
    term: str
    category: str


@dataclass
class ClassifyResult:
    verdict: str  # "THUONG" | "MAT"
    hits: list = field(default_factory=list)
    redacted: str | None = None


def _validate_denylist(data: dict) -> dict:
    missing = [k for k in REQUIRED_KEYS if k not in data]
    if missing:
        raise ValueError(f"denylist.yaml thiếu mục {missing}")
    return data


def load_denylist(path=DENYLIST_PATH) -> dict:
    return _validate_denylist(yaml.safe_load(Path(path).read_text(encoding="utf-8")))


def _term_regex(term: str, case_sensitive: bool) -> re.Pattern:
    flags = 0 if case_sensitive else re.IGNORECASE
    return re.compile(rf"(?<!\w){re.escape(term)}(?!\w)", flags)


def classify(text: str, denylist: dict | None = None) -> ClassifyResult:
    dl = denylist if denylist is not None else load_denylist()
    spans: list[tuple[int, int]] = []
    hits: dict[tuple[str, str], Hit] = {}

    def scan(terms, category, case_sensitive=False):
        for term in terms or []:
            for m in _term_regex(term, case_sensitive).finditer(text):
                spans.append((m.start(), m.end()))
                hits.setdefault((term, category), Hit(term, category))

    scan(dl["product_codes"], "product_code")
    scan(dl["codenames"], "codename", case_sensitive=True)
    scan(dl["defense_terms"], "defense_term")
    for pat in dl["drawing_patterns"]:
        for m in re.finditer(pat, text):
            spans.append((m.start(), m.end()))
            hits.setdefault((m.group(0), "drawing_pattern"), Hit(m.group(0), "drawing_pattern"))

    if not hits:
        return ClassifyResult("THUONG")
    return ClassifyResult("MAT", list(hits.values()), _redact(text, spans))


def _redact(text: str, spans: list[tuple[int, int]]) -> str:
    merged: list[list[int]] = []
    for s, e in sorted(spans):
        if merged and s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    out, prev = [], 0
    for s, e in merged:
        out.append(text[prev:s])
        out.append("[REDACTED]")
        prev = e
    out.append(text[prev:])
    return "".join(out)
