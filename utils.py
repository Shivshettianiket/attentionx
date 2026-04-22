"""
utils.py — AttentionX Shared Utilities
Lightweight helpers used across pipeline.py and app.py.

Built for AttentionX AI Hackathon 2026 by Aniket Shivshetti
B.Tech CSE, BMIT Solapur
"""

from __future__ import annotations
import math
from config import SIGMOID_K


# ── Math Helpers ──────────────────────────────────────────────────────────────

def sigmoid(x: float, k: float = SIGMOID_K) -> float:
    """
    Smooth S-curve mapping any real number to (0, 1).

    Args:
        x:  Input value (weighted sum of PULSE signals, typically 0–1).
        k:  Steepness parameter. Higher k = sharper separation.

    Returns:
        Float in (0, 1).

    Example:
        >>> sigmoid(0.5)   # midpoint → 0.5
        0.5
        >>> sigmoid(0.8)   # strong signal → ~0.92
        0.923...
    """
    return 1.0 / (1.0 + math.exp(-k * (x - 0.5)))


def normalize(arr: list[float]) -> list[float]:
    """
    Min-max normalise a list of floats to the range [0, 1].

    Handles flat arrays (all values equal) gracefully by returning 0.5
    for every element, avoiding zero-division.

    Args:
        arr: List of raw signal values.

    Returns:
        Normalised list of the same length, values in [0, 1].

    Example:
        >>> normalize([10, 20, 30])
        [0.0, 0.5, 1.0]
        >>> normalize([5, 5, 5])   # flat → neutral
        [0.5, 0.5, 0.5]
    """
    if not arr:
        return []
    lo, hi = min(arr), max(arr)
    if hi == lo:
        return [0.5] * len(arr)
    return [(v - lo) / (hi - lo) for v in arr]


# ── Time Formatting ───────────────────────────────────────────────────────────

def fmt_timestamp(seconds: float) -> str:
    """
    Format seconds into HH:MM:SS,mmm (SRT subtitle format).

    Args:
        seconds: Time in seconds (non-negative).

    Returns:
        String like '00:01:23,456'.

    Example:
        >>> fmt_timestamp(83.5)
        '00:01:23,500'
    """
    t = max(0.0, seconds)
    h   = int(t // 3600)
    m   = int((t % 3600) // 60)
    s   = int(t % 60)
    ms  = int((t % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def fmt_duration(seconds: float) -> str:
    """
    Human-readable duration string.

    Args:
        seconds: Duration in seconds.

    Returns:
        String like '1m 23s' or '45s'.

    Example:
        >>> fmt_duration(83)
        '1m 23s'
        >>> fmt_duration(45)
        '45s'
    """
    s = int(seconds)
    m, sec = divmod(s, 60)
    if m:
        return f"{m}m {sec}s"
    return f"{sec}s"


# ── Validation ────────────────────────────────────────────────────────────────

def weights_valid(weights: tuple[float, ...], tol: float = 0.01) -> bool:
    """
    Check that PULSE weights sum to approximately 1.0.

    Args:
        weights: Tuple of (wp, wu, wl, ws, we).
        tol:     Allowed deviation from 1.0 (default ±0.01).

    Returns:
        True if sum is within tolerance.

    Example:
        >>> weights_valid((0.25, 0.20, 0.20, 0.25, 0.10))
        True
        >>> weights_valid((0.5, 0.5, 0.5, 0.5, 0.5))
        False
    """
    return abs(sum(weights) - 1.0) <= tol


def clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    """
    Clamp a value between lo and hi (inclusive).

    Example:
        >>> clamp(1.5)
        1.0
        >>> clamp(-0.2)
        0.0
    """
    return max(lo, min(hi, value))
