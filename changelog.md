# 📋 Changelog

All notable changes to AttentionX are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [2.0.0] — 2026-04-22

### Added
- **PULSE Score engine** — 5-signal psycholinguistic viral moment detector
  - P · Prosodic Energy (RMS amplitude via librosa)
  - U · Urgency Velocity (speech rate acceleration via Whisper timestamps)
  - L · Lexical Impact (TF-IDF hook-word density)
  - S · Sentiment Salience (Gemini 1.5 Flash emotional intensity)
  - E · Entropy Spike (spectral flux via librosa STFT)
- **Gemini AI integration** — hook headline generation + viral signal classification
- **Smart 9:16 vertical crop** — face-tracked via MediaPipe, falls back to center
- **SRT caption burning** — word-level timestamps from Whisper, styled via ffmpeg
- **Demo cache system** — `demo_cache.json` for instant replay without re-processing
- **Live PULSE weight sliders** — tune what "viral" means per content type
- **Per-clip signal breakdown** — full explainability for each detected moment
- **`config.py`** — all constants centralised (hook words, weights, model settings)
- **`utils.py`** — shared helpers (sigmoid, normalize, timestamp formatting, validation)
- **`.gitignore`** — excludes cache, media, secrets, venv
- **`CONTRIBUTING.md`** — contribution guide with commit conventions
- **`CHANGELOG.md`** — this file

### Changed
- Refactored `_sigmoid()` and `normalize()` from `pipeline.py` → `utils.py`
- Extracted all constants from `pipeline.py` → `config.py`
- Cleaned `README.md` — removed accidentally merged `requirements.txt` content
- Pinned all dependency versions in `requirements.txt`

### Architecture
```
Video → ffmpeg Audio → Whisper ASR → PULSE Signals (P·U·L·E) → Gemini (S) → Ranking → Clip Export
```

---

## [1.0.0] — 2026-04-15

### Added
- Initial AttentionX prototype for AI Hackathon 2026
- Whisper transcription pipeline
- Basic RMS energy detection
- ffmpeg clip cutting
- Streamlit UI (v1)

---

Built with ⚡ by Aniket Shivshetti — B.Tech CSE, BMIT Solapur
