# ⚡ AttentionX — Automated Viral Clip Engine

> Turn a 2-hour lecture into 5 viral Reels in minutes.
> Powered by the **PULSE Score** — *Peak Urgency & Listener Signal Engine*.

Built for the **AttentionX AI Hackathon 2026** by **Aniket Shivshetti**, B.Tech CSE, BMIT Solapur.

---

## 🎬 Demo Video

[▶ Watch Live Demo — AttentionX in action](https://youtu.be/areibZ1ncGk?feature=shared)

---

## 👨‍💻 Developer

- 🔗 GitHub: [Shivshettianiket](https://github.com/Shivshettianiket)
- 💼 LinkedIn: [aniketshivshetti](https://www.linkedin.com/in/aniketshivshetti/)

---

## 🧠 The PULSE Score

PULSE is a **psycholinguistically grounded** viral moment detector.

```
PULSE = σ(wp·P + wu·U + wl·L + ws·S + we·E) × 100
```

| Signal | Meaning |
|--------|---------|
| **P** | Prosodic Energy (voice intensity) |
| **U** | Urgency Velocity (speech speed change) |
| **L** | Lexical Impact (hook words) |
| **S** | Sentiment Salience (emotional intensity) |
| **E** | Entropy Spike (audio unpredictability) |

---

## ✨ Features

- 🎙️ Whisper AI transcription (tiny / base model)
- 🤖 Gemini AI viral hook headline generation
- 📊 5-signal PULSE scoring engine
- ✂️ Instant clip cutting via ffmpeg (no re-encode)
- 📱 Face-tracked 9:16 vertical crop (Reels / TikTok ready)
- 💬 Auto-burn captions (SRT-based, styled)
- 🎚️ Live PULSE weight tuning sliders
- 📊 Per-clip signal breakdown for full explainability
- 🎮 Demo cache for instant replay without re-processing

---

## 🏗 Architecture

```
Video → ffmpeg Audio → Whisper ASR → PULSE Signals (P·U·L·E) → Gemini (S) → Ranking → Clip Export
```

---

## 🚀 Run Locally

### Prerequisites
- Python 3.9+
- ffmpeg installed and on PATH (`brew install ffmpeg` / `apt install ffmpeg`)
- A free [Google Gemini API key](https://aistudio.google.com)

### Setup

```bash
git clone https://github.com/Shivshettianiket/attentionx
cd attentionx
pip install -r requirements.txt
python -m streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📁 Project Structure

```
attentionx/
├── app.py              # Streamlit UI — upload, process, display results
├── pipeline.py         # PULSE engine — all signal computation & clip export
├── config.py           # Constants — hook words, weights, sigmoid params
├── utils.py            # Shared helpers — sigmoid, normalize
├── requirements.txt    # Pinned dependencies
├── .gitignore          # Excludes cache, temp files, API keys
└── README.md           # You are here
```

---

## ⚡ Quick Demo (for judges)

1. Upload any long-form video (lecture, podcast, interview)
2. Add your Gemini API key in the sidebar
3. Click **"Find My Viral Moments"**
4. Watch PULSE detect the highest-potential moments in real time
5. Download Reels-ready clips instantly

---

## 🏆 Why This Wins

- 🚀 **Fast** — optimised ffmpeg pipeline, Whisper tiny runs ~5× real-time
- 🧠 **Explainable AI** — every PULSE score shows its 5 signal breakdown
- 🎯 **Real-world use case** — creators, educators, marketers all benefit
- 🎥 **Demo-ready UI** — polished Streamlit interface built for judges
- ⚡ **Clean execution** — modular, well-documented codebase

---

## 📄 License

MIT © 2026 Aniket Shivshetti
