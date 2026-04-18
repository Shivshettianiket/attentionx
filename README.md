# ⚡ AttentionX — Automated Viral Clip Engine

> Turn a 2-hour lecture into 5 viral Reels in minutes.
> Powered by the **PULSE Score** — *Peak Urgency & Listener Signal Engine*.

Built for the **AttentionX AI Hackathon 2026** by **Aniket Shivshetti**, B.Tech CSE, BMIT Solapur.

---

## 🎬 Demo Video

[▶ Watch Live Demo — AttentionX in action](YOUR_GOOGLE_DRIVE_LINK_HERE)

> Replace the link above with your Google Drive screen recording link before submission.

---

## 🧠 The PULSE Score

PULSE is a **psycholinguistically grounded** viral moment detector.
Unlike simple averages, PULSE uses a **sigmoid non-linearity** to sharpen score separation —
average content scores 40–60, genuinely viral moments push toward **85–100**.

```
raw   = wp·P + wu·U + wl·L + ws·S + we·E
PULSE = σ(raw, k=8) × 100
```

| Signal | Full Name | Source | What it captures |
|--------|-----------|--------|-----------------|
| **P** | Prosodic Energy | Librosa RMS | Speaker loudness / energy level |
| **U** | Urgency Velocity | Whisper timestamps | Speech *rate acceleration* — people speak faster when excited |
| **L** | Lexical Impact | TF-IDF hook-word scan | Rare trigger phrases score higher than common ones |
| **S** | Sentiment Salience | Gemini 1.5 Flash | Emotional intensity of the moment (0–1) |
| **E** | Entropy Spike | Librosa spectral flux | Tonal unpredictability — laughter, emphasis, voice breaks |

All five signals are **independently normalised to [0, 1]** before weighting.
All weights are **tunable live via UI sliders** during demo.

---

## ✨ Features

- 🎙️ **Whisper ASR** with word-level timestamps (tiny/base model selectable)
- 📊 **5-signal PULSE scoring** — prosodic, urgency, lexical, sentiment, entropy
- 🤖 **Gemini 1.5 Flash** — hook headlines, sentiment scores, viral signal tags
- ✂️ **ffmpeg stream-copy clip cutting** — clips in ~1 second, no re-encode
- 📱 **MediaPipe face-tracked 9:16 crop** — Reels/TikTok ready
- 💬 **SRT-based caption burn** — fast, ffmpeg-native
- ⬇️ **Direct clip download** from the web UI
- 💾 **Demo cache mode** — pre-compute results, replay instantly for judges
- 🎚️ **Live weight tuning** — adjust all 5 PULSE signals from the sidebar
- 📊 **PULSE breakdown table** — every signal per clip, judge-friendly

---

## 🚀 Run Locally

```bash
git clone https://github.com/aniketshivshetti/attentionx
cd attentionx
pip install -r requirements.txt
streamlit run app.py
```

Then open `http://localhost:8501`.

**Requirements:**
- Google Gemini API key (free at [aistudio.google.com](https://aistudio.google.com))
- FFmpeg installed:
  - Linux: `sudo apt install ffmpeg`
  - Mac: `brew install ffmpeg`
  - Windows: [ffmpeg.org/download.html](https://ffmpeg.org/download.html)

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit + Custom CSS (Syne + JetBrains Mono fonts) |
| Transcription | OpenAI Whisper (tiny/base) |
| Audio Analysis | Librosa (RMS + STFT spectral flux) |
| AI Analysis | Google Gemini 1.5 Flash |
| Video Processing | ffmpeg (subprocess, stream-copy — no MoviePy re-encode) |
| Face Detection | MediaPipe |
| Scoring | Custom PULSE sigmoid formula |
| Language | Python 3.10+ |

---

## 📁 Project Structure

```
attentionx/
├── app.py                  # Streamlit UI — all frontend logic
├── pipeline.py             # All processing functions (clean separation)
├── requirements.txt
├── README.md
├── demo_cache.json         # Auto-generated after first run (instant demo replay)
└── .streamlit/
    └── config.toml         # Upload size + theme settings
```

---

## 🏗 Architecture

```
Video Upload
     ↓
🎵 Extract Audio → 16kHz mono WAV (ffmpeg subprocess, ~15s for 2hr video)
     ↓
🤖 Transcribe (Whisper tiny/base) → timestamped segments + word timestamps
     ↓
📊 Compute 5 PULSE Signals:
  P: Librosa RMS per segment
  U: Speech rate delta per segment
  L: TF-IDF hook-word density
  E: Librosa spectral flux
     ↓
🔍 Pre-filter Top 20 candidates (P + L, no API cost)
     ↓
✨ Gemini 1.5 Flash → S (sentiment) + hook headlines + viral tags
     ↓
🧮 PULSE = σ(wp·P + wu·U + wl·L + ws·S + we·E) × 100
     ↓
Sort → Top N clips
     ↓
✂️ ffmpeg stream-copy clip cutting (~1s per clip)
     ↓ (optional)
📱 MediaPipe face crop → 9:16
     ↓ (optional)
💬 ffmpeg subtitles burn → SRT captions
     ↓
⬇️ Download-ready clips + Demo cache saved ✅
```

---

## 🏆 Judging Criteria Alignment

| Criteria | Weight | AttentionX approach |
|----------|--------|---------------------|
| **User Experience** | 25% | Light purple/blue premium UI, live PULSE dashboard, tunable sliders, one-click demo, step-by-step processing stages with ETAs |
| **Impact** | 20% | Turns 60min lecture → 5 viral clips. Applicable to 10M+ educators/creators |
| **Innovation** | 20% | PULSE Score — named, explainable, sigmoid-sharpened, 5-signal psycholinguistic formula. TF-IDF hook weighting + spectral flux novel for this problem |
| **Technical Execution** | 20% | Clean 2-file architecture, ffmpeg subprocess (no re-encode), SRT caption burn, demo cache, error handling |
| **Presentation** | 15% | Recorded demo in README, demo mode for judges, PULSE explainer built into UI |

---

## ⚡ Quick Judge Setup (30 seconds)

```bash
# Clone and install
git clone https://github.com/YOUR_USERNAME/attentionx
cd attentionx
pip install -r requirements.txt

# Run
streamlit run app.py

# No video? Use Demo Mode!
# Click "See it in action → Try demo" in the UI (no API key needed)
```

---

## 👨‍💻 Built By

**Aniket Shivshetti** — 2nd year B.Tech CSE, BMIT College, Solapur
Built solo for the AttentionX AI Hackathon 2026.

LinkedIn: [linkedin.com/in/aniket-shivshetti](https://linkedin.com/in/aniket-shivshetti)