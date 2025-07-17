# 📈 CoinDCX Crypto RSI Signal App

This is a Streamlit web app that displays **RSI-based BUY/SELL signals** for selected crypto pairs on the **CoinDCX exchange**. The app fetches real-time candlestick data and uses the Relative Strength Index (RSI) indicator to generate trading signals.

🔗 **Live App:**  
👉 [https://coindcx-crypto-v1.streamlit.app/](https://coindcx-crypto-v1.streamlit.app/)

---

## 📊 Features

- Fetches 5-minute interval OHLCV data from CoinDCX public API
- Calculates 14-period RSI using `ta` (technical analysis library)
- Classifies signals:
  - RSI ≤ 30 → **BUY**
  - RSI ≥ 70 → **SELL**
  - Otherwise → **NEUTRAL**
- Displays signal table only when triggered manually via **"Run" button**
- Mobile-friendly interface (thanks to Streamlit)

---

## ⚙️ Technologies Used

- `Python`
- `Streamlit`
- `Pandas`
- `Requests`
- `ta` (Technical Analysis)
- `NumPy`

---
