from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import BaseModel


class GateResult(BaseModel):
    score: int
    markdownlint_issues: int
    broken_links: int
    vale_alerts: int
    notes: list[str]


def _read_text(path: Path) -> str | None:
    if not path.exists():
        return None
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return None


def _loads_json(text: str | None) -> Any:
    if not text:
        return None
    try:
        import json
        return json.loads(text)
    except Exception:
        return None


def _count_markdownlint(path: Path) -> int:
    raw = _loads_json(_read_text(path))
    if isinstance(raw, dict):
        return sum(len(v) for v in raw.values() if isinstance(v, list))
    return 0


def _count_vale(path: Path) -> int:
    raw = _loads_json(_read_text(path))
    if isinstance(raw, dict):
        return sum(len(v) for v in raw.values() if isinstance(v, list))
    return 0


def _count_lychee(path: Path) -> int:
    raw = _loads_json(_read_text(path))
    if raw is None:
        return 0

    if isinstance(raw, dict):
        if isinstance(raw.get("errors"), list):
            return len(raw["errors"])
        links = raw.get("links")
        if isinstance(links, list):
            broken = 0
            for x in links:
                if not isinstance(x, dict):
                    continue
                ok = x.get("ok")
                status = str(x.get("status", ""))
                if ok is False or status.startswith(("4", "5")):
                    broken += 1
            return broken
        return 0

    if isinstance(raw, list):
        broken = 0
        for x in raw:
            if not isinstance(x, dict):
                continue
            ok = x.get("ok")
            status = str(x.get("status", ""))
            if ok is False or status.startswith(("4", "5")):
                broken += 1
        return broken

    return 0


def compute_score(reports_dir: Path) -> GateResult:
    reports_dir = Path(reports_dir)

    md = reports_dir / "markdownlint.json"
    ly = reports_dir / "lychee.json"
    va = reports_dir / "vale.json"

    markdownlint_issues = _count_markdownlint(md)
    broken_links = _count_lychee(ly)
    vale_alerts = _count_vale(va)

    notes: list[str] = []
    score = 100

    # Penalties
    score -= min(30, markdownlint_issues * 2)
    score -= min(40, broken_links * 10)
    score -= min(30, vale_alerts * 2)
    score = max(0, min(100, score))

    if not md.exists():
        notes.append("markdownlint report missing (reports/markdownlint.json).")
    if not ly.exists():
        notes.append("lychee report missing (reports/lychee.json).")
    if not va.exists():
        notes.append("vale report missing (reports/vale.json).")

    return GateResult(
        score=score,
        markdownlint_issues=markdownlint_issues,
        broken_links=broken_links,
        vale_alerts=vale_alerts,
        notes=notes,
    )
