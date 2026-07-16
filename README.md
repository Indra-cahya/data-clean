# BioInformatics Data Pipeline & Visualization

Aplikasi web untuk mengolah data interaksi metabolit tanaman dengan protein target hasil prediksi dari platform SwissTargetPrediction.

## Fitur
- 📊 Upload file dataset Excel (.xlsx)
- 🔬 Filter otomatis berdasarkan threshold (> 0.65)
- 🗺️ Visualisasi Annotated Heatmap standar publikasi ilmiah
- 📥 Download hasil dalam format PNG, PDF, SVG (300 DPI)
- 📝 Laporan analisis data otomatis

## Tech Stack
- Python 3.10+
- Pandas & Openpyxl (Data Processing)
- Matplotlib & Seaborn (Visualization)
- Streamlit (Web Interface)

## Cara Menjalankan Lokal
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy
Aplikasi ini siap di-deploy ke [Streamlit Community Cloud](https://share.streamlit.io).
