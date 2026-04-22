# 🤝 Contributing to AttentionX

Thanks for your interest in contributing! AttentionX is an open project built for the AI Hackathon 2026. All contributions are welcome — bug fixes, new signals, UI improvements, or documentation.

---

## 🚀 Getting Started

```bash
git clone https://github.com/Shivshettianiket/attentionx
cd attentionx
pip install -r requirements.txt
python -m streamlit run app.py
```

Make sure `ffmpeg` is installed and on your PATH before running.

---

## 📁 Codebase Overview

| File | Purpose |
|------|---------|
| `app.py` | Streamlit UI — upload, process, display results |
| `pipeline.py` | PULSE engine — signal computation, clip export |
| `config.py` | All constants — weights, hook words, model settings |
| `utils.py` | Shared math helpers — sigmoid, normalize, formatting |

---

## 🛠 How to Contribute

### 1. Fork & Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make your changes
- Follow the existing code style (type hints, docstrings)
- Add constants to `config.py` rather than hardcoding values
- Add shared helpers to `utils.py`

### 3. Test locally
```bash
python -m streamlit run app.py
```

### 4. Commit with a clear message
```bash
git commit -m "feat: add pause detection signal to PULSE"
```

### 5. Open a Pull Request
Describe what you changed and why. Link any relevant issues.

---

## 💡 Ideas for Contribution

- **New PULSE signals** — pause detection, pitch variance, audience laughter
- **Export formats** — JSON export, CSV score tables, SRT-only download
- **Multi-language support** — Whisper supports 90+ languages
- **Better hook words** — domain-specific lists (fitness, finance, tech)
- **UI improvements** — mobile layout, dark mode, better charts
- **Performance** — batch Gemini calls, parallel clip cutting

---

## 📋 Commit Message Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

| Prefix | Use for |
|--------|---------|
| `feat:` | New feature or signal |
| `fix:` | Bug fix |
| `docs:` | Documentation only |
| `refactor:` | Code restructure, no behaviour change |
| `perf:` | Performance improvement |
| `style:` | Formatting, no logic change |
| `chore:` | Dependency updates, config |

---

## 🐛 Reporting Bugs

Open a GitHub Issue with:
- Steps to reproduce
- Expected vs actual behaviour
- Python version, OS, ffmpeg version

---

## 📄 License

By contributing, you agree your changes will be licensed under the MIT License.

---

Built with ⚡ by Aniket Shivshetti — BMIT Solapur
