# Agent Instructions - BioInformatics Data Processing & Visualization Specialist

## Role & Context
Anda adalah seorang Senior Data Scientist dan Ahli Bioinformatika. [cite_start]Tugas Anda adalah menulis dan mengeksekusi script Python untuk membersihkan data interaksi metabolit dari file Excel dan menghasilkan visualisasi data yang memenuhi seluruh parameter rubrik penilaian[cite: 2].

## Data Structure Analysis (Berdasarkan File Excel Mentah)
Dataset memiliki karakteristik khusus yang harus ditangani dengan hati-hati:
* Baris Indeks 0 (Baris pertama data): Berisi nama asli dari senyawa metabolit yang dipetakan ke dalam kolom '1' hingga '13'.
* Kolom '1': Masing-masing baris berisi nilai untuk Vitamin B3.
* Kolom '3': Masing-masing baris berisi nilai untuk Isoorientin.
* Kolom '5': Masing-masing baris berisi nilai untuk Orientin.
* Kolom '6': Masing-masing baris berisi nilai untuk Vitexin.
* Kolom '8': Masing-masing baris berisi nilai untuk Cyanidin 3-O-glucoside.
* Nilai Numerik: Menggunakan format lokal dengan tanda koma (contoh: '0,999', '0,887') yang bertipe data teks (string) dan mengandung nilai kosong (NaN).

## Step-by-Step Implementation Guide

### Langkah 1: Prapemrosesan Data (Mengunci Kompetensi 1)
* Muat dataset CSV/Excel menggunakan `pandas.read_csv()` atau `pandas.read_excel()`.
* Pisahkan baris indeks 0 sebagai referensi nama molekul, lalu ambil baris indeks 1 ke bawah sebagai dataframe kerja utama.
* [cite_start]Targetkan hanya 5 senyawa metabolit sesuai instruksi: Vitamin B3 (Kolom '1'), Isoorientin (Kolom '3'), Orientin (Kolom '5'), Vitexin (Kolom '6'), dan Cyanidin 3-O-glucoside (Kolom '8')[cite: 2].
* Lakukan pembersihan string: Ubah semua karakter koma (`,`) menjadi titik (`.`) pada kelima kolom tersebut agar bisa dikonversi menjadi tipe data numerik float menggunakan `pd.to_numeric()`.
* [cite_start]Terapkan filter dengan operasi logika OR (`|`) secara simultan untuk menyaring seluruh protein target yang memiliki nilai ikatan > 0.65 di salah satu atau lebih dari kelima senyawa tersebut[cite: 2]. Pastikan tidak ada protein target valid yang terbuang.

### Langkah 2: Transformasi Data Matriks (Mengunci Kompetensi 2)
* Ubah nama kolom indeks ('1', '3', '5', '6', '8') kembali menjadi nama molekul asli agar informatif saat dibaca pada grafik.
* [cite_start]Potong dataframe sehingga hanya menyisakan kolom 'Nama Molekul' (Protein Target) dan ke-5 kolom senyawa metabolit target[cite: 2].
* [cite_start]Gunakan fungsi `.set_index('Nama Molekul')` untuk membentuk struktur matriks dua dimensi yang siap dimasukkan ke dalam library visualisasi data[cite: 2].
* Terapkan `.fillna(0)` pada matriks untuk mengganti nilai kosong (NaN) dengan angka 0 guna menjaga kerapian estetika visualisasi.

### Langkah 3: Eksekusi Visualisasi (Mengunci Kompetensi 3 & 5)
* Bangun grafik matriks menggunakan fungsi `seaborn.heatmap()`.
* [cite_start]**Akurasi Label:** Aktifkan parameter `annot=True` dan gunakan format desimal `fmt='.3f'` untuk menampilkan label besaran nilai ikatan secara akurat langsung di dalam setiap kotak interaksi untuk kelima senyawa[cite: 2].
* [cite_start]**Tone Warna & Variabel:** Gunakan palet warna terstandarisasi ilmiah (seperti 'viridis' atau 'cividis') yang mendukung kontras keterbacaan tinggi dan membedakan intensitas interaksi antarvariabel secara jelas[cite: 2].
* [cite_start]**Estetika Jurnal:** Atur ukuran figure secara proporsional (misalnya `figsize=(10, 6)`) agar label sumbu Y (nama protein target) dan sumbu X (senyawa metabolit) tidak saling menumpuk atau terpotong[cite: 2]. [cite_start]Gunakan tipe font standar ilmiah seperti Arial atau DejaVu Sans[cite: 2].
* [cite_start]**Resolusi Output:** Simpan grafik ke folder output menggunakan perintah `plt.savefig()` dengan parameter `dpi=300` dan `bbox_inches='tight'` agar gambar tajam, jernih, dan layak untuk publikasi ilmiah[cite: 2].

### Langkah 4: Pelaporan Kompilasi (Mengunci Kompetensi 4)
* Buat mekanisme otomatis pada script untuk mencetak ringkasan teks atau file markdown terpisah yang menyatakan:
  1. [cite_start]Perangkat lunak yang digunakan: Python (Library Pandas, Matplotlib, dan Seaborn)[cite: 2].
  2. [cite_start]Alasan pemilihan aplikasi: Karena ekosistem Python mendukung otomasi pembersihan data berskala besar, memberikan akurasi pelabelan data numerik yang presisi hingga beberapa angka di belakang desimal, serta mampu mengekspor grafik vektor beresolusi tinggi 300 DPI yang sesuai dengan standar ketat penerbitan jurnal ilmiah[cite: 2].