"""Small display helpers for LearnSeek's video results."""

from __future__ import annotations

import math
from typing import Any


def short_description(video: dict[str, Any], limit: int = 220) -> str:
    """Return a compact description without changing the source metadata."""
    description = " ".join(str(video.get("description") or "").split())
    if len(description) <= limit:
        return description
    return description[: limit - 1].rsplit(" ", 1)[0] + "…"


def relevance_label(video: dict[str, Any]) -> str | None:
    """Format a real ranking percentage when a future ranker provides one."""
    relevance = video.get("relevance_percent")
    if not isinstance(relevance, (int, float)) or isinstance(relevance, bool):
        return None
    try:
        score = float(relevance)
    except (OverflowError, ValueError):
        return None
    if not math.isfinite(score):
        return None
    return f"{max(0, min(100, score)):.0f}% match"


def build_theme_stylesheet(base_styles: str, dark_styles: str, dark_mode: bool) -> str:
    """Wrap both palettes in one style element so Streamlit treats them as CSS."""
    selected_styles = base_styles + (dark_styles if dark_mode else "")
    return f"<style>\n{selected_styles}\n</style>"
