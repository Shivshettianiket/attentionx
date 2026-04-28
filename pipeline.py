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

