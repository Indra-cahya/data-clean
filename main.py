import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import glob
import warnings

# Mengabaikan warning font
warnings.filterwarnings('ignore', category=UserWarning)

# ============================================================
# KONFIGURASI (Sesuai AGENT.MD)
# ============================================================
DATA_DIR = 'data'
OUTPUT_DIR = 'output'
THRESHOLD = 0.65

# Mapping kolom bernomor di Excel -> Nama Metabolit Asli
COLUMN_METABOLITE_MAP = {
    1: 'Vitamin B3',
    3: 'Isoorientin',
    5: 'Orientin',
    6: 'Vitexin',
    8: 'Cyanidin 3-O-glucoside',
}

# Kolom protein target
PROTEIN_COL = 'Nama Molekul'


def setup_style():
    """Mengonfigurasi style matplotlib/seaborn untuk plot standar ilmiah."""
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'DejaVu Sans'],
        'font.size': 10,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
    })
    sns.set_theme(style="white")


def find_excel_file(data_dir):
    """Mencari file Excel pertama di dalam direktori data."""
    files = glob.glob(os.path.join(data_dir, '*.xlsx'))
    if not files:
        raise FileNotFoundError(f"Tidak ada file Excel (.xlsx) ditemukan di direktori '{data_dir}'.")
    return files[0]


def process_data(df_raw, threshold):
    """
    Langkah 1 & 2: Prapemrosesan dan Transformasi Data.
    
    Sesuai AGENT.MD:
    - Pisahkan baris indeks 0 (sub-header metabolit), gunakan baris 1+ sebagai data kerja.
    - Targetkan hanya 5 kolom metabolit: '1', '3', '5', '6', '8'.
    - Bersihkan koma -> titik, konversi ke float.
    - Filter OR: pertahankan protein yang memiliki nilai > threshold di salah satu kolom.
    - Rename kolom ke nama metabolit asli.
    - Set index ke 'Nama Molekul'.
    - fillna(0).
    """
    # Pisahkan baris indeks 0 (sub-header) dan ambil data kerja (baris 1 ke bawah)
    df_work = df_raw.iloc[1:].copy().reset_index(drop=True)
    
    # Identifikasi kolom target (handle int atau str)
    target_cols = {}
    for col_num, metabolite_name in COLUMN_METABOLITE_MAP.items():
        if col_num in df_work.columns:
            target_cols[col_num] = metabolite_name
        elif str(col_num) in df_work.columns:
            target_cols[str(col_num)] = metabolite_name
    
    if not target_cols:
        raise ValueError("Kolom metabolit (1, 3, 5, 6, 8) tidak ditemukan di file Excel.")
    
    # Pembersihan string: koma -> titik, lalu konversi ke float
    for col_key in target_cols.keys():
        df_work[col_key] = (
            df_work[col_key]
            .astype(str)
            .str.replace(',', '.', regex=False)
            .str.strip()
        )
        df_work[col_key] = pd.to_numeric(df_work[col_key], errors='coerce')
    
    # Filter OR: protein yang punya nilai > threshold di SALAH SATU kolom
    filter_mask = pd.Series(False, index=df_work.index)
    for col_key in target_cols.keys():
        filter_mask = filter_mask | (df_work[col_key] > threshold)
    
    df_filtered = df_work[filter_mask].copy()
    
    if len(df_filtered) == 0:
        print(f"[!] Tidak ada protein target yang memiliki nilai ikatan > {threshold}.")
        return None
    
    print(f"[*] Protein target yang lolos filter OR (threshold > {threshold}): {len(df_filtered)}")
    
    # Rename kolom ke nama metabolit asli
    df_filtered = df_filtered.rename(columns=target_cols)
    
    # Potong: hanya kolom Protein Target + 5 kolom metabolit
    protein_col_actual = PROTEIN_COL
    if protein_col_actual not in df_filtered.columns:
        for c in df_filtered.columns:
            if 'molekul' in str(c).lower() or 'nama' in str(c).lower():
                protein_col_actual = c
                break
    
    metabolite_names = list(target_cols.values())
    keep_cols = [protein_col_actual] + metabolite_names
    df_matrix = df_filtered[keep_cols].copy()
    
    # Set index ke Protein Target
    df_matrix = df_matrix.set_index(protein_col_actual)
    
    # fillna(0) untuk estetika visualisasi
    df_matrix = df_matrix.fillna(0)
    
    return df_matrix


def main():
    try:
        # === SETUP ===
        os.makedirs(DATA_DIR, exist_ok=True)
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        setup_style()
        
        # Mencari file Excel
        excel_path = find_excel_file(DATA_DIR)
        print(f"[*] Membaca file: {excel_path}")
        
        # === LANGKAH 1: DATA LOADING ===
        df_raw = pd.read_excel(excel_path)
        print("\n--- Informasi Dataset Mentah ---")
        print(f"Kolom tersedia: {df_raw.columns.tolist()}")
        print(f"Jumlah baris: {len(df_raw)}")
        print("5 Baris pertama:")
        print(df_raw.head())
        
        # === LANGKAH 1 & 2: PRAPEMROSESAN + TRANSFORMASI ===
        matrix_df = process_data(df_raw, THRESHOLD)
        
        if matrix_df is None:
            return
        
        print(f"\n[*] Matriks berhasil dibuat: {matrix_df.shape[0]} protein x {matrix_df.shape[1]} metabolit")
        print(matrix_df.head())
        
        # === LANGKAH 3: VISUALISASI (Kompetensi 3 & 5) ===
        num_targets = len(matrix_df.index)
        num_metabolites = len(matrix_df.columns)
        
        fig_width = max(10, num_metabolites * 2.2)
        fig_height = max(6, num_targets * 0.45 + 2)
        
        fig, ax = plt.subplots(figsize=(fig_width, fig_height))
        
        sns.heatmap(
            matrix_df,
            annot=True,
            fmt=".3f",
            cmap="viridis",
            linewidths=0.6,
            linecolor='#e0e0e0',
            cbar_kws={'label': 'Binding Threshold Score', 'shrink': 0.8},
            ax=ax,
            annot_kws={'size': 9, 'weight': 'bold'}
        )
        
        ax.set_title('Metabolite – Target Protein Interaction Heatmap', fontsize=15, pad=20, fontweight='bold')
        ax.set_xlabel('Senyawa Metabolit', fontsize=12, fontweight='bold', labelpad=12)
        ax.set_ylabel('Protein Target', fontsize=12, fontweight='bold', labelpad=12)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha='right', fontsize=10)
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=9)
        plt.tight_layout()
        
        # === EKSPOR VISUALISASI ===
        print("\n[*] Menyimpan hasil visualisasi...")
        
        png_path = os.path.join(OUTPUT_DIR, 'visualisasi_interaksi.png')
        pdf_path = os.path.join(OUTPUT_DIR, 'visualisasi_interaksi.pdf')
        svg_path = os.path.join(OUTPUT_DIR, 'visualisasi_interaksi.svg')
        
        fig.savefig(png_path, dpi=300, bbox_inches='tight')
        fig.savefig(pdf_path, dpi=300, bbox_inches='tight')
        fig.savefig(svg_path, dpi=300, bbox_inches='tight')
        
        print(f"[*] Sukses! Visualisasi berhasil disimpan di:")
        print(f"    - {png_path}")
        print(f"    - {pdf_path}")
        print(f"    - {svg_path}")
        
        # === LANGKAH 4: PENCATATAN DAN PELAPORAN (Kompetensi 4) ===
        print("\n=== LAPORAN PENCATATAN (STANDAR PUBLIKASI) ===")
        report_console = (
            "Perangkat lunak yang digunakan: Python (Library Pandas, Matplotlib, dan Seaborn).\n"
            "Alasan pemilihan aplikasi: Karena ekosistem Python mendukung otomasi pembersihan data "
            "berskala besar, memberikan akurasi pelabelan data numerik yang presisi hingga beberapa "
            "angka di belakang desimal, serta mampu mengekspor grafik vektor beresolusi tinggi "
            "300 DPI yang sesuai dengan standar ketat penerbitan jurnal ilmiah."
        )
        print(report_console)
        print("================================================\n")
        
        # Simpan laporan ke file markdown
        laporan_path = os.path.join(OUTPUT_DIR, 'laporan.md')
        with open(laporan_path, 'w', encoding='utf-8') as f:
            f.write("# Laporan Visualisasi Data Bioinformatika\n\n")
            f.write("## Perangkat Lunak yang Digunakan\n")
            f.write("Python menggunakan Library **Pandas**, **Matplotlib**, dan **Seaborn**.\n\n")
            f.write("## Alasan Pemilihan Aplikasi\n")
            f.write("Karena ekosistem Python mendukung otomasi pembersihan data berskala besar, ")
            f.write("memberikan akurasi pelabelan data numerik yang presisi hingga beberapa angka ")
            f.write("di belakang desimal, serta mampu mengekspor grafik vektor beresolusi tinggi ")
            f.write("300 DPI yang sesuai dengan standar ketat penerbitan jurnal ilmiah.\n")
        print(f"[*] Laporan teks disimpan di: {laporan_path}")

    except FileNotFoundError as e:
        print(f"\n[!] Error: {e}")
        print("Silakan masukkan file dataset .xlsx Anda ke dalam folder 'data/' dan jalankan ulang script.")
    except Exception as e:
        print(f"\n[!] Terjadi kesalahan yang tidak terduga: {e}")


if __name__ == '__main__':
    main()
