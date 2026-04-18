"""
app.py — AttentionX Viral Clip Engine
Powered by PULSE Score (Peak Urgency & Listener Signal Engine)

Built for AttentionX AI Hackathon 2026 by Aniket Shivshetti
B.Tech CSE, BMIT Solapur
"""

import streamlit as st
import os
import json
import tempfile
import time
from pathlib import Path

st.set_page_config(
    page_title="AttentionX — Viral Clip Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

<style>
/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background-color: #f0f4ff !important;
}
.main .block-container {
    background: #f0f4ff;
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1200px;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #1e0a4a 0%, #2d1472 50%, #1a0a3a 100%) !important;
    border-right: none !important;
}
section[data-testid="stSidebar"] * { color: #c4b5fd !important; }
section[data-testid="stSidebar"] .stSlider > div > div > div { background: #7c3aed !important; }
section[data-testid="stSidebar"] .stSlider [data-testid="stTickBar"] { color: #7c3aed !important; }
section[data-testid="stSidebar"] label { color: #a78bfa !important; font-size: 0.82rem !important; }
section[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(139,92,246,0.4) !important;
    color: #e9d5ff !important;
    border-radius: 10px !important;
}
section[data-testid="stSidebar"] input[type="password"] {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(139,92,246,0.4) !important;
    color: #e9d5ff !important;
    border-radius: 10px !important;
}
section[data-testid="stSidebar"] .stToggle > div { border-color: #7c3aed !important; }

/* ── Hero Header ── */
.ax-hero {
    background: linear-gradient(135deg, #2e0a6e 0%, #4c1d95 40%, #1e3a8a 100%);
    border-radius: 24px;
    padding: 40px 44px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.ax-hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(125,211,252,0.18) 0%, transparent 70%);
    border-radius: 50%;
}
.ax-hero::after {
    content: '';
    position: absolute;
    bottom: -80px; left: 30%;
    width: 400px; height: 200px;
    background: radial-gradient(ellipse, rgba(167,139,250,0.12) 0%, transparent 70%);
}
.ax-wordmark {
    font-family: 'Syne', sans-serif;
    font-size: 3.8rem;
    font-weight: 800;
    letter-spacing: 0.02em;
    line-height: 1;
    color: #ffffff;
    margin-bottom: 0;
}
.ax-accent { color: #7dd3fc; }
.ax-tagline {
    font-size: 0.85rem;
    font-weight: 400;
    color: rgba(196,181,253,0.8);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 6px;
    font-family: 'JetBrains Mono', monospace;
}
.pulse-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(125,211,252,0.3);
    border-radius: 100px;
    padding: 7px 18px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: rgba(255,255,255,0.7);
    margin-top: 20px;
}
.pulse-pill span { color: #7dd3fc; font-weight: 500; }

/* ── Section Label ── */
.ax-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #7c3aed;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* ── Upload Zone ── */
[data-testid="stFileUploadDropzone"] {
    background: white !important;
    border: 2px dashed #c4b5fd !important;
    border-radius: 16px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 24px rgba(124,58,237,0.06) !important;
}
[data-testid="stFileUploadDropzone"]:hover {
    border-color: #7c3aed !important;
    box-shadow: 0 4px 32px rgba(124,58,237,0.12) !important;
}
[data-testid="stFileUploadDropzone"] * { color: #7c3aed !important; }

/* ── Cards ── */
.info-card {
    background: white;
    border-radius: 18px;
    padding: 24px;
    box-shadow: 0 4px 24px rgba(79,70,229,0.07);
    border: 1px solid rgba(196,181,253,0.3);
    height: 100%;
}
.how-step {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid #f3f0ff;
}
.how-step:last-child { border-bottom: none; }
.step-num {
    width: 30px; height: 30px;
    background: linear-gradient(135deg, #7c3aed, #3b82f6);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.72rem;
    font-weight: 700;
    color: white;
    font-family: 'JetBrains Mono', monospace;
    flex-shrink: 0;
}
.step-text { font-size: 0.85rem; color: #4c1d95; font-weight: 500; }

/* ── CTA Button ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7c3aed 0%, #3b82f6 100%) !important;
    color: white !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.85rem 2rem !important;
    letter-spacing: 0.01em !important;
    box-shadow: 0 8px 28px rgba(124,58,237,0.35) !important;
    transition: all 0.2s ease !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 36px rgba(124,58,237,0.45) !important;
}
.stButton > button[kind="secondary"] {
    background: white !important;
    color: #7c3aed !important;
    border: 1.5px solid #c4b5fd !important;
    border-radius: 12px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    transition: all 0.15s !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: #7c3aed !important;
    box-shadow: 0 4px 16px rgba(124,58,237,0.12) !important;
}

/* ── Stat Strip ── */
.stat-strip {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
    margin-bottom: 28px;
}
.stat-cell {
    background: white;
    border-radius: 14px;
    padding: 16px 12px;
    text-align: center;
    box-shadow: 0 2px 16px rgba(79,70,229,0.06);
    border: 1px solid rgba(196,181,253,0.25);
}
.stat-num {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #7c3aed, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}
.stat-lbl {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    color: #a78bfa;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 4px;
}

/* ── Clip Card ── */
.clip-card {
    background: white;
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 6px 32px rgba(79,70,229,0.09);
    border: 1px solid rgba(196,181,253,0.35);
    position: relative;
    overflow: hidden;
}
.clip-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #7c3aed, #3b82f6, #7dd3fc);
}
.clip-rank {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.14em;
    color: #a78bfa;
    text-transform: uppercase;
}
.clip-score {
    font-family: 'Syne', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #7c3aed, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}
.clip-score-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    color: #c4b5fd;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
.clip-hook {
    font-size: 1.15rem;
    font-weight: 700;
    color: #1e0a4a;
    line-height: 1.4;
    border-left: 3px solid #7c3aed;
    padding-left: 14px;
    margin: 14px 0 10px;
}
.clip-why {
    font-size: 0.83rem;
    font-weight: 400;
    color: #6d28d9;
    line-height: 1.6;
    margin-bottom: 14px;
    background: #f5f3ff;
    padding: 10px 14px;
    border-radius: 10px;
}
.signal-tag {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    background: #ede9fe;
    border: 1px solid #c4b5fd;
    color: #6d28d9;
    border-radius: 6px;
    padding: 3px 8px;
    margin-right: 5px;
    margin-bottom: 4px;
    letter-spacing: 0.04em;
}
.time-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #7c3aed;
    background: #ede9fe;
    border-radius: 6px;
    padding: 3px 10px;
    display: inline-block;
    margin-top: 4px;
}

/* ── PULSE Bars ── */
.pulse-bar-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 7px;
}
.pulse-bar-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    color: #7c3aed;
    width: 14px;
    font-weight: 600;
}
.pulse-bar-track {
    flex: 1;
    height: 5px;
    background: #ede9fe;
    border-radius: 3px;
    overflow: hidden;
}
.pulse-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #7c3aed, #3b82f6);
    border-radius: 3px;
}
.pulse-bar-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    color: #a78bfa;
    width: 28px;
    text-align: right;
}

/* ── Processing Stages ── */
.stage-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid #f3f0ff;
}
.stage-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.stage-dot.done    { background: #7c3aed; }
.stage-dot.active  { background: #3b82f6; animation: pulse-dot 1.2s ease infinite; }
.stage-dot.pending { background: #e9d5ff; }
@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.4; transform: scale(0.6); }
}
.stage-name { font-size: 0.85rem; color: #c4b5fd; }
.stage-name.done   { color: #7c3aed; font-weight: 500; }
.stage-name.active { color: #1e0a4a; font-weight: 600; }
.stage-eta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    color: #c4b5fd;
    margin-left: auto;
}
.stage-eta.active { color: #7c3aed; font-weight: 600; }

/* ── Progress bar ── */
.stProgress > div > div {
    background: linear-gradient(90deg, #7c3aed, #3b82f6) !important;
    border-radius: 8px !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: white !important;
    border: 1.5px solid #c4b5fd !important;
    color: #7c3aed !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    transition: all 0.15s !important;
}
.stDownloadButton > button:hover {
    border-color: #7c3aed !important;
    box-shadow: 0 4px 16px rgba(124,58,237,0.15) !important;
}

/* ── Expander ── */
div[data-testid="stExpander"] {
    background: white;
    border: 1px solid rgba(196,181,253,0.35) !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 12px rgba(79,70,229,0.05) !important;
}
div[data-testid="stExpander"] summary { color: #4c1d95 !important; font-weight: 600 !important; }

/* ── Alert ── */
.stAlert {
    background: #f5f3ff !important;
    border: 1px solid #c4b5fd !important;
    border-radius: 12px !important;
    color: #4c1d95 !important;
}

/* ── Dataframe ── */
.stDataFrame { border-radius: 14px !important; overflow: hidden !important; box-shadow: 0 2px 16px rgba(79,70,229,0.07) !important; }

/* ── Typography overrides ── */
h1, h2, h3 { color: #1e0a4a !important; font-family: 'Syne', sans-serif !important; }
p, label, .stMarkdown { color: #4c1d95 !important; }
.stCaption { color: #a78bfa !important; }

/* ── Divider ── */
hr { border-color: rgba(196,181,253,0.3) !important; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 1.2rem 0 0.5rem;">
        <div style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;
                    color:#ffffff;letter-spacing:0.04em;">
            ⚡ Attention<span style="color:#7dd3fc;">X</span>
        </div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.58rem;
                    color:rgba(167,139,250,0.6);text-transform:uppercase;
                    letter-spacing:0.12em;margin-top:3px;">Viral Clip Engine v2</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown('<div class="ax-label">🎚️ &nbsp;PULSE Score Weights</div>', unsafe_allow_html=True)
    st.caption("Tune what 'viral' means for your content type")

    wp = st.slider("🔊 P · Prosodic Energy",    0.05, 0.50, 0.25, 0.05, key="wp")
    wu = st.slider("⚡ U · Urgency Velocity",   0.05, 0.40, 0.20, 0.05, key="wu")
    wl = st.slider("📝 L · Lexical Impact",     0.05, 0.40, 0.20, 0.05, key="wl")
    ws = st.slider("💜 S · Sentiment Salience", 0.05, 0.50, 0.25, 0.05, key="ws")
    we = st.slider("🌊 E · Entropy Spike",      0.00, 0.30, 0.10, 0.05, key="we")

    total = round(wp + wu + wl + ws + we, 2)
    color = "#7dd3fc" if abs(total - 1.0) < 0.01 else "#f87171"
    st.markdown(
        f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.75rem;'
        f'color:{color};padding:6px 10px;background:rgba(255,255,255,0.06);'
        f'border-radius:8px;border:1px solid rgba(255,255,255,0.1);">'
        f'Σ = {total} {"✓ balanced" if abs(total - 1.0) < 0.01 else "⚠ best at 1.0"}</div>',
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown('<div class="ax-label">⚙️ &nbsp;Output Settings</div>', unsafe_allow_html=True)
    top_n        = st.slider("🎬 Clips to generate", 1, 6, 3)
    clip_pad     = st.slider("⏱ Clip padding (s)",  0, 5, 2)
    model_size   = st.selectbox("🤖 Whisper model", ["tiny", "base"], index=0,
                                help="tiny = fastest · base = better accuracy")
    vertical_on  = st.toggle("📱 Smart crop 9:16 (Reels/TikTok)", value=False)
    captions_on  = st.toggle("💬 Burn captions into clips", value=False)

    st.divider()
    st.markdown('<div class="ax-label">🔑 &nbsp;API Key</div>', unsafe_allow_html=True)
    gemini_key = st.text_input(
        "Google Gemini API Key", type="password",
        placeholder="AIza...",
        help="Free at aistudio.google.com",
    )
    if gemini_key:
        st.markdown("""
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;
                    color:#86efac;padding:5px 10px;background:rgba(134,239,172,0.1);
                    border-radius:8px;border:1px solid rgba(134,239,172,0.25);">
            ✓ API key set
        </div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown("""
    <div style="background:rgba(255,255,255,0.05);border:1px solid rgba(167,139,250,0.2);
                border-radius:12px;padding:14px;">
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;
                    color:rgba(167,139,250,0.5);line-height:2.2;text-transform:uppercase;
                    letter-spacing:0.08em;">
            🔊 P · Prosodic Energy<br>
            ⚡ U · Urgency Velocity<br>
            📝 L · Lexical Impact<br>
            💜 S · Sentiment Salience<br>
            🌊 E · Entropy Spike
        </div>
        <div style="margin-top:10px;font-family:'JetBrains Mono',monospace;
                    font-size:0.65rem;color:#7dd3fc;text-align:center;
                    background:rgba(125,211,252,0.08);border-radius:8px;padding:6px;">
            PULSE = σ(P+U+L+S+E) × 100
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Hero Header ───────────────────────────────────────────────────────────────
col_head, col_pill = st.columns([3, 1])
with col_head:
    st.markdown("""
    <div class="ax-hero">
        <div style="display:flex;align-items:center;gap:14px;margin-bottom:4px;">
            <span style="font-size:2.8rem;">⚡</span>
            <div class="ax-wordmark">Attention<span class="ax-accent">X</span></div>
        </div>
        <div class="ax-tagline">Peak Urgency &amp; Listener Signal Engine</div>
        <div class="pulse-pill">
            PULSE &nbsp;·&nbsp; <span>σ(P+U+L+S+E) × 100</span>
        </div>
        <div style="position:absolute;top:20px;right:28px;font-size:3rem;opacity:0.12;">🎯</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def pulse_bars(p, u, l, s, e):
    signals = [("P", p), ("U", u), ("L", l), ("S", s), ("E", e)]
    html = ""
    for label, val in signals:
        pct = int(val * 100)
        html += f"""
        <div class="pulse-bar-row">
            <span class="pulse-bar-label">{label}</span>
            <div class="pulse-bar-track">
                <div class="pulse-bar-fill" style="width:{pct}%"></div>
            </div>
            <span class="pulse-bar-val">{pct}</span>
        </div>"""
    return html


def render_clip_card(rank, item):
    seg = item["seg"]
    signals_html = "".join(
        f'<span class="signal-tag">✦ {s}</span>'
        for s in item.get("signals", [])
    )
    score_int = int(item["score"])
    score_dec = f"{item['score']:.2f}".split(".")[1]

    st.markdown(f"""
    <div class="clip-card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;">
            <div>
                <div class="clip-rank">🎬 CLIP #{rank + 1}</div>
                <div><span class="time-badge">🕐 {seg['start']:.0f}s – {seg['end']:.0f}s</span></div>
            </div>
            <div style="text-align:right;">
                <div class="clip-score">{score_int}<span style="font-size:1.6rem;">.{score_dec}</span></div>
                <div class="clip-score-label">PULSE Score</div>
            </div>
        </div>
        <div class="clip-hook">"{item['headline']}"</div>
        <div class="clip-why">💡 {item['why']}</div>
        <div style="margin-bottom:14px;">{signals_html}</div>
        <div class="ax-label" style="margin-bottom:8px;">📊 Signal Breakdown</div>
        {pulse_bars(item['prosodic'], item['urgency'],
                    item['lexical'], item['sentiment'], item['entropy'])}
    </div>
    """, unsafe_allow_html=True)


def try_load_demo():
    from pipeline import load_demo_cache
    return load_demo_cache("demo_cache.json")


# ── Upload Section ────────────────────────────────────────────────────────────
col_upload, col_info = st.columns([3, 2])

with col_upload:
    st.markdown('<div class="ax-label">📁 &nbsp;Upload Video</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Drop your long-form video here",
        type=["mp4", "mov", "avi", "mkv", "webm"],
        label_visibility="collapsed",
        help="Up to 500 MB · MP4, MOV, AVI, MKV, WebM"
    )
    st.caption("🎙 Supports lectures, podcasts, workshops · up to 500 MB")

with col_info:
    st.markdown("""
    <div class="info-card">
        <div class="ax-label">✨ &nbsp;How it works</div>
        <div class="how-step">
            <div class="step-num">01</div>
            <div class="step-text">📤 Upload your video</div>
        </div>
        <div class="how-step">
            <div class="step-num">02</div>
            <div class="step-text">📊 PULSE scores every moment</div>
        </div>
        <div class="how-step">
            <div class="step-num">03</div>
            <div class="step-text">🤖 Gemini writes hook headlines</div>
        </div>
        <div class="how-step">
            <div class="step-num">04</div>
            <div class="step-text">⬇️ Download Reels-ready clips</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

demo_col, _ = st.columns([2, 4])
with demo_col:
    demo_clicked = st.button("🎮 See it in action → Try demo",
                             type="secondary", use_container_width=True)

if not gemini_key and uploaded:
    st.warning("⚠️ Add your Gemini API key in the sidebar for hook headlines. "
               "Get one free at [aistudio.google.com](https://aistudio.google.com)")

st.divider()


# ── Processing Stages ─────────────────────────────────────────────────────────
STAGES = [
    ("🎵 Extracting audio track",        "~10s"),
    ("🤖 Transcribing with Whisper AI",  "~30–90s"),
    ("📊 Computing PULSE signals",       "~15s"),
    ("🔍 Pre-filtering top candidates",  "~2s"),
    ("✨ Gemini · hooks & sentiment",    "~10s"),
    ("🧮 Scoring with PULSE formula",    "~1s"),
    ("✂️ Cutting & exporting clips",     "~5–30s"),
]


def render_stages(current: int):
    html = '<div style="background:white;border-radius:16px;padding:16px 20px;' \
           'box-shadow:0 4px 24px rgba(79,70,229,0.08);' \
           'border:1px solid rgba(196,181,253,0.3);margin:1rem 0;">'
    for i, (name, eta) in enumerate(STAGES):
        state = "done" if i < current else ("active" if i == current else "pending")
        html += f"""
        <div class="stage-row">
            <div class="stage-dot {state}"></div>
            <span class="stage-name {state}">{name}</span>
            <span class="stage-eta {'active' if state == 'active' else ''}">{eta}</span>
        </div>"""
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


# ── Main CTA ──────────────────────────────────────────────────────────────────
run_button = st.button("⚡ Find My Viral Moments", type="primary",
                       use_container_width=True,
                       disabled=not bool(uploaded))

demo_data = None
if demo_clicked:
    demo_data = try_load_demo()
    if demo_data is None:
        st.info("📂 No demo cache found. Process a video once and it will be saved "
                "automatically for instant demo replay.")

should_process = run_button and uploaded

if should_process or demo_data:

    from pipeline import (
        extract_audio, transcribe_audio,
        compute_prosodic_energy, compute_urgency_velocity,
        compute_spectral_entropy, compute_lexical_impact,
        get_top_candidates, gemini_analyze, pulse_score,
        cut_clip, smart_crop_vertical, burn_captions,
        save_demo_cache, load_demo_cache,
    )
    import google.generativeai as genai_mod
    if gemini_key:
        genai_mod.configure(api_key=gemini_key)

    if demo_data:
        st.success("⚡ Demo loaded instantly from cache")
        final_clips = demo_data["clips"]
        video_duration = demo_data.get("duration", 0)
        transcript_text = demo_data.get("transcript", "")
        render_full_results = True
        clip_files_map = {}
    else:
        render_full_results = False

    if should_process:
        render_full_results = False
        with tempfile.TemporaryDirectory() as tmpdir:
            video_path = os.path.join(tmpdir, "input.mp4")
            audio_path = os.path.join(tmpdir, "audio.wav")

            with open(video_path, "wb") as f:
                f.write(uploaded.read())

            st.video(video_path)
            progress  = st.progress(0)
            stage_box = st.empty()
            status    = st.empty()

            with stage_box.container():
                render_stages(0)
            status.caption("🎵 Extracting audio...")
            try:
                video_duration = extract_audio(video_path, audio_path)
                progress.progress(10)
            except Exception as err:
                st.error(f"❌ Audio extraction failed: {err}")
                st.stop()

            with stage_box.container():
                render_stages(1)
            status.caption(f"🤖 Transcribing with Whisper ({model_size})...")
            try:
                result   = transcribe_audio(audio_path, model_size)
                segments = result["segments"]
                progress.progress(35)
            except Exception as err:
                st.error(f"❌ Transcription failed: {err}")
                st.stop()

            with stage_box.container():
                render_stages(2)
            status.caption("📊 Computing PULSE signal vectors...")
            try:
                prosodic = compute_prosodic_energy(audio_path, segments)
                urgency  = compute_urgency_velocity(segments)
                entropy  = compute_spectral_entropy(audio_path, segments)
                lexical  = compute_lexical_impact(segments)
                progress.progress(55)
            except Exception as err:
                st.error(f"❌ Signal computation failed: {err}")
                st.stop()

            with stage_box.container():
                render_stages(3)
            status.caption("🔍 Selecting top candidates...")
            top_idx  = get_top_candidates(segments, prosodic, lexical,
                                          top_n=min(20, len(segments)))
            top_segs = [segments[i] for i in top_idx]
            progress.progress(60)

            with stage_box.container():
                render_stages(4)
            gem_map: dict = {}
            if gemini_key:
                status.caption("✨ Gemini writing hooks and scoring sentiment...")
                try:
                    gem_results = gemini_analyze(result["text"][:8000], top_segs)
                    gem_map = {r["index"] - 1: r for r in gem_results}
                except Exception as err:
                    st.warning(f"⚠️ Gemini skipped (fallback active): {err}")
            progress.progress(72)

            with stage_box.container():
                render_stages(5)
            status.caption("🧮 Applying PULSE formula...")
            weights = (wp, wu, wl, ws, we)
            scored = []
            for li, seg in enumerate(top_segs):
                oi  = top_idx[li]
                gem = gem_map.get(li, {})
                s   = gem.get("sentiment_score", 0.5)
                sc  = pulse_score(prosodic[oi], urgency[oi], lexical[oi],
                                  s, entropy[oi], weights)
                scored.append({
                    "seg":       seg,
                    "score":     sc,
                    "prosodic":  prosodic[oi],
                    "urgency":   urgency[oi],
                    "lexical":   lexical[oi],
                    "sentiment": s,
                    "entropy":   entropy[oi],
                    "headline":  gem.get("hook_headline", "This moment stops the scroll"),
                    "why":       gem.get("why_viral", "Strong audio energy with emotional language"),
                    "signals":   gem.get("signals", ["emotional_peak"]),
                })

            scored.sort(key=lambda x: x["score"], reverse=True)
            final_clips = scored[:top_n]
            progress.progress(80)

            with stage_box.container():
                render_stages(6)
            status.caption("✂️ Cutting and exporting clips...")

            clip_files_map: dict[int, bytes] = {}
            for rank, item in enumerate(final_clips):
                seg   = item["seg"]
                start = max(0, seg["start"] - clip_pad)
                end   = min(video_duration, seg["end"] + clip_pad)

                raw_p     = os.path.join(tmpdir, f"raw_{rank}.mp4")
                crop_p    = os.path.join(tmpdir, f"crop_{rank}.mp4")
                caption_p = os.path.join(tmpdir, f"final_{rank}.mp4")

                cut_clip(video_path, start, end, raw_p)
                work = raw_p

                if vertical_on and os.path.exists(raw_p):
                    try:
                        smart_crop_vertical(raw_p, crop_p)
                        work = crop_p
                    except Exception:
                        pass

                if captions_on and os.path.exists(work):
                    word_segs = [
                        {"text": w["word"], "start": w["start"], "end": w["end"]}
                        for s in segments
                        if s["start"] >= seg["start"] - clip_pad
                        and s["end"]   <= seg["end"]   + clip_pad
                        for w in s.get("words", [])
                        if w.get("start") is not None
                    ]
                    try:
                        burn_captions(work, word_segs, start, caption_p)
                        work = caption_p
                    except Exception:
                        pass

                if os.path.exists(work):
                    with open(work, "rb") as f:
                        clip_files_map[rank] = f.read()

                progress.progress(80 + int(18 * (rank + 1) / max(top_n, 1)))

            cache_payload = {
                "duration":   video_duration,
                "transcript": result.get("text", ""),
                "clips": [
                    {k: v for k, v in c.items() if k != "seg"}
                    | {"seg": {"start": c["seg"]["start"], "end": c["seg"]["end"],
                               "text": c["seg"]["text"]}}
                    for c in final_clips
                ],
            }
            try:
                save_demo_cache(cache_payload)
            except Exception:
                pass

            progress.progress(100)
            stage_box.empty()
            status.empty()
            render_full_results = True
            transcript_text = result.get("text", "")

    # ── Results ───────────────────────────────────────────────────────────────
    if render_full_results:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;
                    color:#1e0a4a;margin-bottom:4px;">
            🎉 Your Viral Clips
        </div>
        <div style="font-size:0.82rem;color:#a78bfa;margin-bottom:20px;">
            Ranked by PULSE score · highest viral potential first
        </div>
        """, unsafe_allow_html=True)

        n_clips   = len(final_clips)
        total_dur = sum(c["seg"]["end"] - c["seg"]["start"] for c in final_clips)
        avg_score = sum(c["score"] for c in final_clips) / max(n_clips, 1)
        top_score = max(c["score"] for c in final_clips)
        dur_min   = int(video_duration // 60) if video_duration else "?"

        st.markdown(f"""
        <div class="stat-strip">
            <div class="stat-cell">
                <div style="font-size:1.5rem;margin-bottom:4px;">🎬</div>
                <div class="stat-num">{n_clips}</div>
                <div class="stat-lbl">Clips Generated</div>
            </div>
            <div class="stat-cell">
                <div style="font-size:1.5rem;margin-bottom:4px;">⏱</div>
                <div class="stat-num">{dur_min}</div>
                <div class="stat-lbl">Min Processed</div>
            </div>
            <div class="stat-cell">
                <div style="font-size:1.5rem;margin-bottom:4px;">📐</div>
                <div class="stat-num">{int(total_dur)}s</div>
                <div class="stat-lbl">Total Duration</div>
            </div>
            <div class="stat-cell">
                <div style="font-size:1.5rem;margin-bottom:4px;">📊</div>
                <div class="stat-num">{avg_score:.1f}</div>
                <div class="stat-lbl">Avg PULSE</div>
            </div>
            <div class="stat-cell">
                <div style="font-size:1.5rem;margin-bottom:4px;">🏆</div>
                <div class="stat-num">{top_score:.1f}</div>
                <div class="stat-lbl">Peak PULSE</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        for rank, item in enumerate(final_clips):
            col_vid, col_info = st.columns([1, 1])

            with col_vid:
                if not demo_data and rank in clip_files_map:
                    st.video(clip_files_map[rank])
                    st.download_button(
                        f"⬇️ Download Clip #{rank + 1}",
                        clip_files_map[rank],
                        file_name=f"attentionx_clip_{rank + 1}.mp4",
                        mime="video/mp4",
                        use_container_width=True,
                    )
                else:
                    seg = item["seg"]
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#f5f3ff,#eff6ff);
                                border:2px dashed #c4b5fd;border-radius:16px;
                                padding:3rem 1rem;text-align:center;">
                        <div style="font-size:2.5rem;margin-bottom:8px;">🎬</div>
                        <div style="font-family:'JetBrains Mono',monospace;
                                    font-size:0.62rem;color:#a78bfa;
                                    text-transform:uppercase;letter-spacing:0.1em;
                                    margin-bottom:8px;">Demo Preview</div>
                        <div style="font-family:'Syne',sans-serif;
                                    font-size:1.8rem;font-weight:700;
                                    background:linear-gradient(135deg,#7c3aed,#3b82f6);
                                    -webkit-background-clip:text;
                                    -webkit-text-fill-color:transparent;
                                    background-clip:text;">
                            {seg['start']:.0f}s — {seg['end']:.0f}s
                        </div>
                        <div style="font-size:0.78rem;color:#a78bfa;margin-top:6px;">
                            Upload your video to get the actual clip
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            with col_info:
                render_clip_card(rank, item)

            st.markdown("<br>", unsafe_allow_html=True)

        # Score table
        st.markdown('<div class="ax-label">📊 &nbsp;PULSE Score Breakdown</div>',
                    unsafe_allow_html=True)
        import pandas as pd
        df = pd.DataFrame([{
            "Rank":        f"#{r + 1}",
            "Time":        f"{c['seg']['start']:.0f}s–{c['seg']['end']:.0f}s",
            "PULSE":       f"{c['score']:.2f}",
            "P·Prosodic":  f"{c['prosodic']:.3f}",
            "U·Urgency":   f"{c['urgency']:.3f}",
            "L·Lexical":   f"{c['lexical']:.3f}",
            "S·Sentiment": f"{c['sentiment']:.3f}",
            "E·Entropy":   f"{c['entropy']:.3f}",
            "Hook":        c['headline'],
        } for r, c in enumerate(final_clips)])
        st.dataframe(df, use_container_width=True, hide_index=True)

        if transcript_text:
            with st.expander("📝 Full Transcript"):
                st.text(transcript_text)

        with st.expander("🧠 What is the PULSE Score?"):
            st.markdown("""
            **PULSE** — *Peak Urgency & Listener Signal Engine* — detects viral moments
            using five psycholinguistically grounded signals:

            | Signal | Measures | Source |
            |--------|----------|--------|
            | **P · Prosodic Energy** | RMS amplitude — where the speaker is loudest | Librosa audio |
            | **U · Urgency Velocity** | Speech rate *acceleration* | Whisper timestamps |
            | **L · Lexical Impact** | TF-IDF weighted hook-word density | Transcript |
            | **S · Sentiment Salience** | Emotional intensity (0–1) | Gemini 1.5 Flash |
            | **E · Entropy Spike** | Spectral flux — tonal unpredictability | Librosa STFT |

            ```
            raw   = wp·P + wu·U + wl·L + ws·S + we·E
            PULSE = σ(raw, k=8) × 100
            ```

            The **sigmoid** sharpens separation — average content stays 40–60,
            genuinely viral moments push toward **85–100**.
            """)

elif not uploaded and not demo_clicked:
    st.markdown("""
    <div style="text-align:center;padding:5rem 2rem;">
        <div style="font-size:5rem;margin-bottom:16px;">⚡</div>
        <div style="font-family:'Syne',sans-serif;font-size:3.5rem;font-weight:800;
                    background:linear-gradient(135deg,#7c3aed,#3b82f6,#7dd3fc);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                    background-clip:text;line-height:1.1;margin-bottom:16px;">
            Drop a video.<br>Get viral clips.
        </div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;
                    color:#c4b5fd;text-transform:uppercase;letter-spacing:0.14em;">
            PULSE · 5-signal psycholinguistic scoring · Gemini-powered hooks
        </div>
        <div style="display:flex;justify-content:center;gap:20px;margin-top:32px;flex-wrap:wrap;">
            <div style="background:white;border:1px solid #e9d5ff;border-radius:14px;
                        padding:14px 22px;box-shadow:0 4px 20px rgba(124,58,237,0.08);">
                <span style="font-size:1.4rem;">🎙️</span>
                <div style="font-size:0.78rem;color:#7c3aed;font-weight:600;margin-top:4px;">Whisper ASR</div>
            </div>
            <div style="background:white;border:1px solid #e9d5ff;border-radius:14px;
                        padding:14px 22px;box-shadow:0 4px 20px rgba(124,58,237,0.08);">
                <span style="font-size:1.4rem;">📊</span>
                <div style="font-size:0.78rem;color:#7c3aed;font-weight:600;margin-top:4px;">PULSE Scoring</div>
            </div>
            <div style="background:white;border:1px solid #e9d5ff;border-radius:14px;
                        padding:14px 22px;box-shadow:0 4px 20px rgba(124,58,237,0.08);">
                <span style="font-size:1.4rem;">🤖</span>
                <div style="font-size:0.78rem;color:#7c3aed;font-weight:600;margin-top:4px;">Gemini AI</div>
            </div>
            <div style="background:white;border:1px solid #e9d5ff;border-radius:14px;
                        padding:14px 22px;box-shadow:0 4px 20px rgba(124,58,237,0.08);">
                <span style="font-size:1.4rem;">📱</span>
                <div style="font-size:0.78nm;color:#7c3aed;font-weight:600;margin-top:4px;">Reels-Ready</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)