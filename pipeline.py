"""
pipeline.py — AttentionX processing core
Powered by the PULSE Score (Peak Urgency & Listener Signal Engine)

PULSE = 5-signal psycholinguistically grounded viral moment detector:
  P — Prosodic Energy     (RMS amplitude envelope)
  U — Urgency Velocity    (speech rate acceleration)
  L — Lexical Impact      (TF-IDF hook-word density)
  S — Sentiment Salience  (Gemini emotional intensity, 0–1)
  E — Entropy Spike       (spectral flux — tonal unpredictability)

Final: PULSE = sigmoid( w·[P, U, L, S, E] ) × 100

Built for AttentionX AI Hackathon 2026 by Aniket Shivshetti
B.Tech CSE, BMIT Solapur
"""

from __future__ import annotations
import os
import json
import math
import subprocess
import numpy as np
from pathlib import Path
from typing import Optional


# ── Constants ─────────────────────────────────────────────────────────────────

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

_SIGMOID_K = 8.0   # steepness — controls score separation


# ── Helpers ───────────────────────────────────────────────────────────────────

def _sigmoid(x: float) -> float:
    """Smooth S-curve mapping any real to (0, 1)."""
    return 1.0 / (1.0 + math.exp(-_SIGMOID_K * (x - 0.5)))


def normalize(arr: list[float]) -> list[float]:
    """Min-max normalise to [0, 1]. Handles flat arrays gracefully."""
    if not arr:
        return []
    lo, hi = min(arr), max(arr)
    if hi == lo:
        return [0.5] * len(arr)
    return [(v - lo) / (hi - lo) for v in arr]


# ── 1. Audio extraction ───────────────────────────────────────────────────────

def extract_audio(video_path: str, audio_path: str) -> float:
    """
    Extract 16 kHz mono WAV using ffmpeg subprocess.
    Returns video duration in seconds.
    Fast: a 2-hour video extracts in ~15 seconds.
    """
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", video_path],
        capture_output=True, text=True
    )
    duration = float(probe.stdout.strip() or "0")

    subprocess.run([
        "ffmpeg", "-y", "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        audio_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    return duration


# ── 2. Transcription ──────────────────────────────────────────────────────────

def transcribe_audio(audio_path: str, model_size: str = "tiny") -> dict:
    """
    Whisper transcription with word-level timestamps.
    tiny  → ~5× real-time
    base  → ~2× real-time (better accuracy)
    """
    import whisper
    model = whisper.load_model(model_size)
    return model.transcribe(
        audio_path,
        verbose=False,
        word_timestamps=True,
        task="transcribe",
        condition_on_previous_text=False,
    )


# ── 3. PULSE Signal Extraction ────────────────────────────────────────────────

def compute_prosodic_energy(audio_path: str, segments: list[dict]) -> list[float]:
    """
    P — Prosodic Energy: RMS amplitude per segment.
    Captures where the speaker is loudest / most energised.
    """
    import librosa
    y, sr = librosa.load(audio_path, sr=None)
    energies = []
    for seg in segments:
        s = int(seg["start"] * sr)
        e = int(seg["end"] * sr)
        chunk = y[s:e]
        rms = float(np.sqrt(np.mean(chunk ** 2))) if len(chunk) > 0 else 0.0
        energies.append(rms)
    return normalize(energies)


def compute_urgency_velocity(segments: list[dict]) -> list[float]:
    """
    U — Urgency Velocity: rate of change in words-per-second.
    Now also detects pauses — silence before a segment boosts urgency score,
    since speakers often pause right before delivering a key point.
    """
    def wps(seg: dict) -> float:
        dur = max(seg["end"] - seg["start"], 0.01)
        return len(seg["text"].split()) / dur

    rates = [wps(s) for s in segments]
    deltas = []
    for i, r in enumerate(rates):
        # Silence gap between previous segment and this one
        pause = 0.0
        if i > 0:
            pause = max(0.0, segments[i]["start"] - segments[i - 1]["end"])
        pause_boost = min(pause / 2.0, 1.0)  # 2s silence = max boost

        window = rates[max(0, i - 2): i + 3]
        avg = sum(window) / len(window)
        deltas.append(abs(r - avg) + pause_boost)
    return normalize(deltas)


def compute_spectral_entropy(audio_path: str, segments: list[dict]) -> list[float]:
    """
    E — Entropy Spike: spectral flux (frame-to-frame spectral change).
    High flux = emotionally charged moments (laughter, emphasis, voice breaks).
    """
    import librosa
    y, sr = librosa.load(audio_path, sr=None)
    hop = 512
    S = np.abs(librosa.stft(y, hop_length=hop))
    flux = np.sqrt(np.mean(np.diff(S, axis=1) ** 2, axis=0))
    times = librosa.frames_to_time(np.arange(len(flux)), sr=sr, hop_length=hop)

    entropies = []
    for seg in segments:
        mask = (times >= seg["start"]) & (times <= seg["end"])
        chunk = flux[mask]
        val = float(np.mean(chunk)) if len(chunk) > 0 else 0.0
        entropies.append(val)
    return normalize(entropies)


def compute_lexical_impact(segments: list[dict]) -> list[float]:
    """
    L — Lexical Impact: TF-IDF weighted hook-word density.
    Rare hook words score higher than common ones.
    """
    all_texts = [s["text"].lower() for s in segments]
    corpus_freq: dict[str, int] = {}
    for t in all_texts:
        for kw in HOOK_WORDS:
            if kw in t:
                corpus_freq[kw] = corpus_freq.get(kw, 0) + 1

    n = len(segments)
    scores = []
    for seg in segments:
        t = seg["text"].lower()
        words = t.split()
        if not words:
            scores.append(0.0)
            continue
        score = 0.0
        for kw in HOOK_WORDS:
            if kw in t:
                df = corpus_freq.get(kw, 1)
                idf = math.log(n / df + 1)
                score += idf
        scores.append(score / max(len(words), 1))
    return normalize(scores)


# ── 4. Gemini Sentiment Analysis ──────────────────────────────────────────────

def gemini_analyze(full_transcript: str, top_segments: list[dict]) -> list[dict]:
    """
    S — Sentiment Salience via Gemini 1.5 Flash.
    Returns per-segment: sentiment_score, hook_headline, why_viral, signals.
    """
    import google.generativeai as genai

    segments_text = "\n".join([
        f"[{i+1}] ({s['start']:.0f}s–{s['end']:.0f}s): {s['text'].strip()}"
        for i, s in enumerate(top_segments)
    ])

    prompt = f"""You are a world-class viral content strategist for TikTok, Instagram Reels, and YouTube Shorts.

Transcript context (first 6000 chars):
{full_transcript[:6000]}

Analyze these specific segments. Return ONLY a valid JSON array, no markdown, no explanation.

Segments:
{segments_text}

For each segment return an object with exactly:
- "index": 1-based integer
- "sentiment_score": float 0.0–1.0 (emotional intensity of this moment)
- "hook_headline": string under 10 words — punchy, makes people stop scrolling
- "why_viral": one sentence explaining the viral potential
- "signals": array of strings from: ["emotional_peak","insight_moment","story_turn","hard_truth","actionable","controversy","authority","curiosity_gap"]

Return only the JSON array."""

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    raw = response.text.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(raw)


# ── 5. PULSE Score Calculation ────────────────────────────────────────────────

def pulse_score(
    prosodic: float,
    urgency: float,
    lexical: float,
    sentiment: float,
    entropy: float,
    weights: tuple[float, float, float, float, float] = (0.25, 0.20, 0.20, 0.25, 0.10),
) -> float:
    """
    PULSE = sigmoid( weighted sum of 5 normalised signals ) × 100

    Weights (default):
      P prosodic energy    0.25
      U urgency velocity   0.20
      L lexical impact     0.20
      S sentiment salience 0.25
      E entropy spike      0.10

    Sigmoid sharpens separation — average content stays 40–60,
    genuinely viral moments push toward 90+.
    Returns 0–100 (two decimal places).
    """
    wp, wu, wl, ws, we = weights
    raw = (wp * prosodic + wu * urgency + wl * lexical
           + ws * sentiment + we * entropy)
    return round(_sigmoid(raw) * 100, 2)


# ── 6. Pre-filter Candidates ──────────────────────────────────────────────────

def get_top_candidates(
    segments: list[dict],
    prosodic: list[float],
    lexical: list[float],
    top_n: int = 20,
) -> list[int]:
    """
    Fast pre-filter before calling Gemini (no API cost).
    Uses P + L only to select the most promising segments.
    """
    raw = [0.5 * prosodic[i] + 0.5 * lexical[i] for i in range(len(segments))]
    return sorted(range(len(raw)), key=lambda i: raw[i], reverse=True)[:top_n]


# ── 7. Clip Cutting ───────────────────────────────────────────────────────────

def cut_clip(video_path: str, start: float, end: float, output_path: str):
    """
    Stream-copy clip cut — no re-encode.
    A 60-second clip cuts in ~1 second.
    """
    subprocess.run([
        "ffmpeg", "-y",
        "-ss", str(max(0, start)),
        "-to", str(end),
        "-i", video_path,
        "-c", "copy",
        "-avoid_negative_ts", "make_zero",
        output_path,
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# ── 8. Smart 9:16 Vertical Crop ───────────────────────────────────────────────

def smart_crop_vertical(input_path: str, output_path: str):
    """
    Face-tracked 9:16 crop using MediaPipe.
    Falls back to center-weighted crop if no face detected.
    """
    import cv2
    import mediapipe as mp

    face_cx_rel = 0.5
    cap = cv2.VideoCapture(input_path)
    ret, frame = cap.read()
    cap.release()

    if ret:
        with mp.solutions.face_detection.FaceDetection(
            min_detection_confidence=0.35
        ) as det:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = det.process(rgb)
            if results.detections:
                bbox = results.detections[0].location_data.relative_bounding_box
                face_cx_rel = bbox.xmin + bbox.width / 2

    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height",
         "-of", "csv=p=0", input_path],
        capture_output=True, text=True
    )
    parts = probe.stdout.strip().split(",")
    if len(parts) != 2:
        subprocess.run(["cp", input_path, output_path])
        return

    w, h = int(parts[0]), int(parts[1])
    target_w = int(h * 9 / 16)

    if target_w >= w:
        subprocess.run(["cp", input_path, output_path])
        return

    cx = int(face_cx_rel * w)
    x1 = max(0, min(cx - target_w // 2, w - target_w))

    subprocess.run([
        "ffmpeg", "-y", "-i", input_path,
        "-vf", f"crop={target_w}:{h}:{x1}:0",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "copy",
        output_path,
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# ── 9. SRT Caption Burn ───────────────────────────────────────────────────────

def _words_to_srt(word_segments: list[dict], clip_start: float) -> str:
    """Convert word-level segments to SRT subtitle format."""
    def fmt(t: float) -> str:
        t = max(0, t)
        h = int(t // 3600)
        m = int((t % 3600) // 60)
        s = int(t % 60)
        ms = int((t % 1) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    lines: list[tuple[float, float, str]] = []
    chunk: list[dict] = []
    for w in word_segments:
        chunk.append(w)
        if len(chunk) >= 3 or w.get("end", 0) - chunk[0].get("start", 0) > 1.5:
            start_t = chunk[0].get("start", 0) - clip_start
            end_t = chunk[-1].get("end", start_t + 0.5) - clip_start
            text = " ".join(c.get("text", "").strip() for c in chunk)
            if text and start_t >= 0:
                lines.append((start_t, end_t, text))
            chunk = []
    if chunk:
        start_t = chunk[0].get("start", 0) - clip_start
        end_t = chunk[-1].get("end", start_t + 0.5) - clip_start
        text = " ".join(c.get("text", "").strip() for c in chunk)
        if text and start_t >= 0:
            lines.append((start_t, end_t, text))

    srt = ""
    for i, (s, e, txt) in enumerate(lines, 1):
        srt += f"{i}\n{fmt(s)} --> {fmt(max(s + 0.1, e))}\n{txt}\n\n"
    return srt


def burn_captions(video_path: str, word_segments: list[dict],
                  clip_start: float, output_path: str):
    """
    Burn captions via ffmpeg subtitles filter.
    Uses SRT format — much faster than per-word TextClip.
    """
    import tempfile

    if not word_segments:
        subprocess.run(["cp", video_path, output_path])
        return

    srt_content = _words_to_srt(word_segments, clip_start)
    if not srt_content.strip():
        subprocess.run(["cp", video_path, output_path])
        return

    with tempfile.NamedTemporaryFile(
        suffix=".srt", mode="w", delete=False, encoding="utf-8"
    ) as f:
        f.write(srt_content)
        srt_path = f.name

    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", video_path,
            "-vf", (
                f"subtitles={srt_path}:force_style='"
                "FontName=Arial,FontSize=20,Bold=1,"
                "PrimaryColour=&H00FFFFFF,"
                "OutlineColour=&H00000000,Outline=2,"
                "Alignment=2,MarginV=40'"
            ),
            "-c:v", "libx264", "-preset", "fast", "-crf", "22",
            "-c:a", "copy",
            output_path,
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    finally:
        os.unlink(srt_path)


# ── 10. Demo Cache Helpers ────────────────────────────────────────────────────

def save_demo_cache(data: dict, path: str = "demo_cache.json"):
    """Save processed results to JSON for instant demo replay."""
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def load_demo_cache(path: str = "demo_cache.json") -> Optional[dict]:
    """Load cached demo results if available."""
    p = Path(path)
    if p.exists():
        with open(p) as f:
            return json.load(f)
    return None
