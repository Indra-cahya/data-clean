# Product Requirements Document (PRD) - BioInformatics Data Pipeline & Visualization
## Target: Nilai Maksimal (100/100) sesuai Rubrik UKAS

## 1. Project Overview
Projek ini bertujuan untuk membangun sebuah data pipeline otomatis berbasis Python untuk mengolah data interaksi metabolit tanaman dengan protein target hasil prediksi dari platform SwissTargetPrediction. Sistem ini harus memenuhi seluruh area kompetensi ujian, mulai dari ketepatan filtrasi data hingga penyajian visualisasi standar publikasi ilmiah yang informatif dan memiliki resolusi tinggi.

## 2. Kriteria Keberhasilan Berdasarkan Rubrik Penilaian

### 2.1. Penetapan Masalah (Bobot: 20 Poin)
* Sistem harus mampu menyaring dan menetapkan **seluruh** protein target yang berinteraksi dengan 5 senyawa metabolit spesifik:
  1. Isoorientin
  2. Orientin
  3. Cyanidin 3-O-glucoside
  4. Vitexin
  5. Vitamin B3
* Batang ambang batas (threshold) nilai ikatan yang lolos seleksi harus ditentukan secara ketat, yaitu **> 0.65**. Tidak boleh ada data yang tertinggal atau salah saring.

### 2.2. Penyelesaian Masalah (Bobot: 20 Poin)
* Sistem harus menghasilkan bentuk visualisasi data yang mampu menampilkan interaksi antara **seluruh** protein target yang telah lolos filtrasi dengan ke-5 senyawa metabolit tersebut secara lengkap tanpa ada yang terpotong atau tereliminasi secara tidak sengaja.

### 2.3. Komunikasi Efektif (Bobot: 20 Poin)
* Visualisasi data wajib membubuhkan **label besaran nilai ikatan secara akurat** langsung pada visualisasi untuk ke-5 senyawa metabolit (bukan hanya sebagian senyawa). Angka koordinat interaksi harus terlihat jelas.

### 2.4. Pencatatan dan Pelaporan (Bobot: 10 Poin)
* Sistem atau dokumentasi luaran harus menuliskan secara eksplisit nama aplikasi/library yang digunakan untuk menyusun visualisasi data beserta penjelasan singkat mengenai alasan pemilihan aplikasi tersebut untuk kebutuhan publikasi ilmiah.

### 2.5. Sikap Profesional (Bobot: 30 Poin)
Visualisasi akhir wajib memenuhi 5 indikator profesionalitas berikut secara mutlak:
1. **Kesesuaian Template:** Menggunakan bentuk visualisasi yang relevan untuk interaksi dua variabel (direkomendasikan berbentuk Matriks/Annotated Heatmap).
2. **Keterbacaan Tone Warna:** Skema warna yang digunakan harus mendukung keterbacaan teks dan kontras informasi.
3. **Pembeda Antarvariabel:** Warna yang digunakan harus secara jelas membantu membedakan posisi antarvariabel (Metabolit vs Protein Target).
4. **Estetika Ilustrasi:** Tampilan visual tidak kaku, tidak hambar, rapi, dan memiliki tata letak yang seimbang.
5. **Resolusi Tinggi:** Output gambar akhir tidak boleh buram atau pecah (minimal 300 DPI).

## 3. Tech Stack & Environment
* Bahasa Pemrograman: Python 3.10+
* Library Utama: Pandas, Openpyxl (Ekstraksi Data), Matplotlib, Seaborn (Visualisasi Data)