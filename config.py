"""
config.py — AttentionX Configuration
All tunable constants for the PULSE Score engine.

Built for AttentionX AI Hackathon 2026 by Aniket Shivshetti
B.Tech CSE, BMIT Solapur
"""

# ── PULSE Sigmoid ─────────────────────────────────────────────────────────────

SIGMOID_K: float = 8.0
"""
Steepness of the sigmoid curve.
Higher → more separation between average and viral moments.
Default 8.0 keeps mid-range content at 40–60 and viral peaks at 85–100.
"""


# ── PULSE Default Weights ─────────────────────────────────────────────────────

DEFAULT_WEIGHTS: tuple[float, float, float, float, float] = (0.25, 0.20, 0.20, 0.25, 0.10)
"""
Default signal weights: (P, U, L, S, E)
  P · Prosodic Energy    — 0.25
  U · Urgency Velocity   — 0.20
  L · Lexical Impact     — 0.20
  S · Sentiment Salience — 0.25
  E · Entropy Spike      — 0.10
Sum = 1.0  ✓
"""


# ── Whisper ───────────────────────────────────────────────────────────────────

WHISPER_DEFAULT_MODEL: str = "tiny"
"""
Default Whisper model size.
  tiny  → ~5× real-time, lower accuracy
  base  → ~2× real-time, better accuracy
"""


# ── Audio Extraction ──────────────────────────────────────────────────────────

AUDIO_SAMPLE_RATE: int = 16_000
"""Target sample rate for extracted WAV (Hz). Whisper expects 16 kHz."""

AUDIO_CHANNELS: int = 1
"""Mono audio for Whisper and librosa processing."""


# ── Candidate Pre-filter ──────────────────────────────────────────────────────

TOP_CANDIDATE_COUNT: int = 20
"""
Max segments passed to Gemini for sentiment analysis.
Keeps API cost low while covering the best moments.
"""


# ── Clip Export ───────────────────────────────────────────────────────────────

DEFAULT_CLIP_PAD_SECONDS: int = 2
"""Seconds of padding added before/after each detected segment."""

FFMPEG_VIDEO_CODEC: str = "libx264"
FFMPEG_PRESET: str = "fast"
FFMPEG_CRF: int = 23


# ── Caption Style ─────────────────────────────────────────────────────────────

CAPTION_FONT: str = "Arial"
CAPTION_FONT_SIZE: int = 20
CAPTION_BOLD: bool = True
CAPTION_PRIMARY_COLOR: str = "&H00FFFFFF"   # White text
CAPTION_OUTLINE_COLOR: str = "&H00000000"   # Black outline
CAPTION_OUTLINE_WIDTH: int = 2
CAPTION_ALIGNMENT: int = 2                  # Bottom-center
CAPTION_MARGIN_V: int = 40
CAPTION_WORDS_PER_CHUNK: int = 3
CAPTION_MAX_CHUNK_DURATION: float = 1.5     # seconds


# ── Demo Cache ────────────────────────────────────────────────────────────────

DEMO_CACHE_PATH: str = "demo_cache.json"


# ── Hook Words (Lexical Impact signal) ───────────────────────────────────────

HOOK_WORDS: list[str] = [
    # Contrast / negation
    "never", "always", "wrong", "mistake", "actually", "truth", "lie",
    "nobody", "everyone", "no one", "stop", "start", "fail", "succeed",
    # Intensity / urgency
    "critical", "urgent", "important", "key", "secret", "hidden",
    "powerful", "fundamental", "real", "only", "biggest", "worst", "best",
    # Curiosity triggers
    "why", "reason", "this is", "the problem", "missing", "nobody tells",
    "most people", "you need", "remember", "challenge", "hard truth",
    "the truth is", "simple", "one thing", "step", "the way",
]


# ── Gemini ────────────────────────────────────────────────────────────────────

GEMINI_MODEL: str = "gemini-1.5-flash"
GEMINI_TRANSCRIPT_CONTEXT_CHARS: int = 6_000
"""Max characters of transcript context sent to Gemini to stay within token limits."""

VIRAL_SIGNALS: list[str] = [
    "emotional_peak",
    "insight_moment",
    "story_turn",
    "hard_truth",
    "actionable",
    "controversy",
    "authority",
    "curiosity_gap",
]
