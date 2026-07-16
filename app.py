import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import io
import warnings

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="BioInformatics Data Pipeline & Visualization",
    page_icon="🧬",
    layout="wide"
)

warnings.filterwarnings('ignore', category=UserWarning)

# ============================================================
# KONFIGURASI MAPPING KOLOM (Sesuai AGENT.MD)
# Kolom bernomor di Excel -> Nama Metabolit Asli
# ============================================================
COLUMN_METABOLITE_MAP = {
    1: 'Vitamin B3',
    3: 'Isoorientin',
    5: 'Orientin',
    6: 'Vitexin',
    8: 'Cyanidin 3-O-glucoside',
}

# Kolom protein target sesuai instruksi AGENT.MD
PROTEIN_COL = 'Nama Molekul'

# Threshold
THRESHOLD = 0.65


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
    # --- Pisahkan baris indeks 0 (sub-header) dan ambil data kerja ---
    df_work = df_raw.iloc[1:].copy().reset_index(drop=True)
    
    # --- Identifikasi kolom target (handle int atau str) ---
    target_cols = {}
    for col_num, metabolite_name in COLUMN_METABOLITE_MAP.items():
        # Kolom bisa dibaca sebagai int (1) atau str ('1')
        if col_num in df_work.columns:
            target_cols[col_num] = metabolite_name
        elif str(col_num) in df_work.columns:
            target_cols[str(col_num)] = metabolite_name
    
    if not target_cols:
        return None, None, "Kolom metabolit (1, 3, 5, 6, 8) tidak ditemukan di file Excel."
    
    # --- Pembersihan string: koma -> titik, lalu konversi ke float ---
    for col_key in target_cols.keys():
        df_work[col_key] = (
            df_work[col_key]
            .astype(str)
            .str.replace(',', '.', regex=False)
            .str.strip()
        )
        df_work[col_key] = pd.to_numeric(df_work[col_key], errors='coerce')
    
    # --- Filter OR: protein yang punya nilai > threshold di SALAH SATU kolom ---
    filter_mask = pd.Series(False, index=df_work.index)
    for col_key in target_cols.keys():
        filter_mask = filter_mask | (df_work[col_key] > threshold)
    
    df_filtered = df_work[filter_mask].copy()
    
    if len(df_filtered) == 0:
        return None, None, f"Tidak ada protein target yang memiliki nilai ikatan > {threshold}."
    
    # --- Rename kolom ke nama metabolit asli ---
    df_filtered = df_filtered.rename(columns=target_cols)
    
    # --- Potong: hanya kolom Protein Target + 5 kolom metabolit ---
    protein_col_actual = PROTEIN_COL
    if protein_col_actual not in df_filtered.columns:
        # Fallback: cari kolom yang mengandung kata 'molekul' atau 'protein'
        for c in df_filtered.columns:
            if 'molekul' in str(c).lower() or 'nama' in str(c).lower():
                protein_col_actual = c
                break
    
    metabolite_names = list(target_cols.values())
    keep_cols = [protein_col_actual] + metabolite_names
    df_matrix = df_filtered[keep_cols].copy()
    
    # --- Set index ke Protein Target ---
    df_matrix = df_matrix.set_index(protein_col_actual)
    
    # --- fillna(0) untuk estetika visualisasi ---
    df_matrix = df_matrix.fillna(0)
    
    return df_matrix, protein_col_actual, None


def create_heatmap(matrix_df):
    """
    Langkah 3: Eksekusi Visualisasi (Kompetensi 3 & 5).
    
    - seaborn.heatmap() dengan annot=True, fmt='.3f'
    - Palet viridis (color-blind friendly)
    - Ukuran figure proporsional
    - Font Arial/DejaVu Sans
    - Resolusi 300 DPI
    """
    num_targets = len(matrix_df.index)
    num_metabolites = len(matrix_df.columns)
    
    # Ukuran figure proporsional agar label tidak menumpuk
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
        cbar_kws={
            'label': 'Binding Threshold Score',
            'shrink': 0.8
        },
        ax=ax,
        annot_kws={'size': 9, 'weight': 'bold'}
    )
    
    ax.set_title(
        'Metabolite – Target Protein Interaction Heatmap',
        fontsize=15, pad=20, fontweight='bold'
    )
    ax.set_xlabel('Senyawa Metabolit', fontsize=12, fontweight='bold', labelpad=12)
    ax.set_ylabel('Protein Target', fontsize=12, fontweight='bold', labelpad=12)
    
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha='right', fontsize=10)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=9)
    
    plt.tight_layout()
    return fig


def generate_report_text():
    """Langkah 4: Pelaporan Kompilasi (Kompetensi 4)."""
    return (
        "# Laporan Visualisasi Data Bioinformatika\n\n"
        "## Perangkat Lunak yang Digunakan\n"
        "Python menggunakan Library **Pandas**, **Matplotlib**, dan **Seaborn**.\n\n"
        "## Alasan Pemilihan Aplikasi\n"
        "Karena ekosistem Python mendukung otomasi pembersihan data berskala besar, "
        "memberikan akurasi pelabelan data numerik yang presisi hingga beberapa angka "
        "di belakang desimal, serta mampu mengekspor grafik vektor beresolusi tinggi "
        "300 DPI yang sesuai dengan standar ketat penerbitan jurnal ilmiah.\n"
    )


def main():
    # === HEADER ===
    st.title("🧬 BioInformatics Data Pipeline & Visualization")
    st.markdown(
        "Aplikasi web untuk mengolah data interaksi **metabolit tanaman** dengan **protein target** "
        "hasil prediksi SwissTargetPrediction, dan menghasilkan visualisasi **Annotated Heatmap** "
        "siap publikasi jurnal ilmiah."
    )
    st.markdown("---")
    
    # === SIDEBAR ===
    with st.sidebar:
        st.header("⚙️ Pengaturan")
        threshold = st.number_input(
            "Batas Nilai Ikatan (Threshold)",
            min_value=0.0, max_value=1.0, value=0.65, step=0.01,
            help="Hanya protein yang punya nilai ikatan **di atas** angka ini (pada minimal 1 dari 5 senyawa) yang akan ditampilkan."
        )
        st.markdown("---")
        st.markdown("##### 📋 Mapping Kolom Excel → Metabolit")
        for col_num, name in COLUMN_METABOLITE_MAP.items():
            st.markdown(f"- Kolom `{col_num}` → **{name}**")
    
    # === FILE UPLOADER ===
    uploaded_file = st.file_uploader(
        "📂 Unggah file dataset Excel (.xlsx)",
        type=["xlsx"],
        help="File Excel dari SwissTargetPrediction."
    )
    
    if uploaded_file is not None:
        try:
            with st.spinner("Membaca dan memproses data..."):
                setup_style()
                df_raw = pd.read_excel(uploaded_file)
            
            # --- TAMPILKAN DATA MENTAH ---
            st.subheader("📊 Data Mentah (5 Baris Pertama)")
            st.dataframe(df_raw.head(), use_container_width=True)
            
            # --- LANGKAH 1 & 2: PRAPEMROSESAN + TRANSFORMASI ---
            matrix_df, protein_col, error_msg = process_data(df_raw, threshold)
            
            if matrix_df is None:
                st.error(f"❌ {error_msg}")
                return
            
            st.success(
                f"✅ Data berhasil diproses! "
                f"Protein target lolos filtrasi: **{len(matrix_df)}** | "
                f"Senyawa metabolit: **{len(matrix_df.columns)}**"
            )
            
            # --- TAMPILKAN MATRIKS ---
            st.subheader("📐 Matriks Interaksi (Pivot Table)")
            st.dataframe(
                matrix_df.style.format("{:.3f}").background_gradient(cmap='viridis'),
                use_container_width=True
            )
            
            # --- LANGKAH 3: VISUALISASI HEATMAP ---
            st.subheader("🗺️ Visualisasi Annotated Heatmap")
            fig = create_heatmap(matrix_df)
            st.pyplot(fig)
            
            # --- DOWNLOAD VISUALISASI ---
            st.markdown("### 📥 Download Visualisasi (Resolusi 300 DPI)")
            col1, col2, col3 = st.columns(3)
            
            buf_png = io.BytesIO()
            fig.savefig(buf_png, format="png", dpi=300, bbox_inches='tight')
            col1.download_button("⬇️ Download PNG", buf_png.getvalue(), "visualisasi_interaksi.png", "image/png")
            
            buf_pdf = io.BytesIO()
            fig.savefig(buf_pdf, format="pdf", dpi=300, bbox_inches='tight')
            col2.download_button("⬇️ Download PDF", buf_pdf.getvalue(), "visualisasi_interaksi.pdf", "application/pdf")
            
            buf_svg = io.BytesIO()
            fig.savefig(buf_svg, format="svg", dpi=300, bbox_inches='tight')
            col3.download_button("⬇️ Download SVG", buf_svg.getvalue(), "visualisasi_interaksi.svg", "image/svg+xml")
            
            # --- LANGKAH 4: PENCATATAN DAN PELAPORAN ---
            st.markdown("---")
            st.subheader("📝 Laporan Analisis Data")
            
            # === RINGKASAN STATISTIK ===
            total_raw = len(df_raw) - 1  # minus 1 karena baris sub-header
            total_filtered = len(matrix_df)
            total_metabolites = len(matrix_df.columns)
            
            st.markdown("#### 📌 Ringkasan Umum")
            col_s1, col_s2, col_s3, col_s4 = st.columns(4)
            col_s1.metric("Total Data Mentah", f"{total_raw} baris")
            col_s2.metric("Protein Lolos Filter", f"{total_filtered} protein")
            col_s3.metric("Senyawa Metabolit", f"{total_metabolites} senyawa")
            col_s4.metric("Threshold", f"> {threshold}")
            
            st.markdown(
                f"Dari **{total_raw}** baris data mentah, setelah dilakukan penyaringan dengan "
                f"nilai ambang batas (threshold) **> {threshold}** menggunakan operasi logika OR "
                f"pada 5 senyawa metabolit target, diperoleh **{total_filtered}** protein target "
                f"yang memenuhi kriteria untuk divisualisasikan."
            )
            
            # === ANALISIS PER METABOLIT ===
            st.markdown("#### 🔬 Analisis Per Senyawa Metabolit")
            
            for met_col in matrix_df.columns:
                met_data = matrix_df[met_col]
                met_nonzero = met_data[met_data > 0]
                
                if len(met_nonzero) > 0:
                    best_protein = met_nonzero.idxmax()
                    best_score = met_nonzero.max()
                    avg_score = met_nonzero.mean()
                    count_interact = len(met_nonzero)
                    
                    with st.expander(f"🧪 {met_col} — {count_interact} interaksi terdeteksi"):
                        st.markdown(
                            f"- **Jumlah protein yang berinteraksi:** {count_interact}\n"
                            f"- **Rata-rata nilai ikatan:** {avg_score:.3f}\n"
                            f"- **Nilai ikatan tertinggi:** {best_score:.3f} → *{best_protein}*\n"
                            f"- **Nilai ikatan terendah:** {met_nonzero.min():.3f} → *{met_nonzero.idxmin()}*"
                        )
                else:
                    with st.expander(f"🧪 {met_col} — Tidak ada interaksi"):
                        st.markdown("Tidak ada protein target yang memiliki nilai ikatan > threshold untuk senyawa ini.")
            
            # === TOP PROTEIN TARGET ===
            st.markdown("#### 🏆 Protein Target dengan Interaksi Terkuat")
            
            # Hitung skor rata-rata per protein (hanya dari kolom yang > 0)
            protein_avg = matrix_df.replace(0, float('nan')).mean(axis=1).sort_values(ascending=False)
            top_n = min(5, len(protein_avg))
            
            for rank, (protein_name, avg_val) in enumerate(protein_avg.head(top_n).items(), 1):
                st.markdown(f"**{rank}.** {protein_name} — rata-rata skor: **{avg_val:.3f}**")
            
            # === LAPORAN STANDAR PUBLIKASI ===
            st.markdown("---")
            st.markdown("#### 📄 Keterangan Perangkat Lunak (Standar Publikasi)")
            st.info(
                "**Perangkat lunak yang digunakan:** Python menggunakan Library Pandas, Matplotlib, dan Seaborn.\n\n"
                "**Alasan pemilihan aplikasi:** Karena ekosistem Python mendukung otomasi pembersihan data "
                "berskala besar, memberikan akurasi pelabelan data numerik yang presisi hingga beberapa "
                "angka di belakang desimal, serta mampu mengekspor grafik vektor beresolusi tinggi 300 DPI "
                "yang sesuai dengan standar ketat penerbitan jurnal ilmiah."
            )
            
            # === GENERATE FULL DOWNLOADABLE REPORT ===
            report_lines = []
            report_lines.append("# Laporan Analisis Data Bioinformatika\n")
            report_lines.append("## 1. Ringkasan Umum\n")
            report_lines.append(f"- **Total data mentah:** {total_raw} baris\n")
            report_lines.append(f"- **Threshold yang digunakan:** > {threshold}\n")
            report_lines.append(f"- **Protein target lolos filtrasi:** {total_filtered}\n")
            report_lines.append(f"- **Jumlah senyawa metabolit:** {total_metabolites}\n")
            report_lines.append(f"\nDari {total_raw} baris data mentah, setelah dilakukan penyaringan dengan "
                                f"nilai ambang batas (threshold) > {threshold} menggunakan operasi logika OR "
                                f"pada 5 senyawa metabolit target, diperoleh {total_filtered} protein target "
                                f"yang memenuhi kriteria.\n")
            
            report_lines.append("\n## 2. Analisis Per Senyawa Metabolit\n")
            for met_col in matrix_df.columns:
                met_data = matrix_df[met_col]
                met_nonzero = met_data[met_data > 0]
                report_lines.append(f"\n### {met_col}\n")
                if len(met_nonzero) > 0:
                    report_lines.append(f"- Jumlah protein yang berinteraksi: {len(met_nonzero)}\n")
                    report_lines.append(f"- Rata-rata nilai ikatan: {met_nonzero.mean():.3f}\n")
                    report_lines.append(f"- Nilai ikatan tertinggi: {met_nonzero.max():.3f} ({met_nonzero.idxmax()})\n")
                    report_lines.append(f"- Nilai ikatan terendah: {met_nonzero.min():.3f} ({met_nonzero.idxmin()})\n")
                else:
                    report_lines.append("- Tidak ada interaksi yang terdeteksi di atas threshold.\n")
            
            report_lines.append("\n## 3. Protein Target dengan Interaksi Terkuat\n")
            for rank, (protein_name, avg_val) in enumerate(protein_avg.head(top_n).items(), 1):
                report_lines.append(f"{rank}. **{protein_name}** — rata-rata skor: {avg_val:.3f}\n")
            
            report_lines.append("\n## 4. Perangkat Lunak yang Digunakan\n")
            report_lines.append("Python menggunakan Library **Pandas**, **Matplotlib**, dan **Seaborn**.\n\n")
            report_lines.append("## 5. Alasan Pemilihan Aplikasi\n")
            report_lines.append(
                "Karena ekosistem Python mendukung otomasi pembersihan data berskala besar, "
                "memberikan akurasi pelabelan data numerik yang presisi hingga beberapa angka "
                "di belakang desimal, serta mampu mengekspor grafik vektor beresolusi tinggi "
                "300 DPI yang sesuai dengan standar ketat penerbitan jurnal ilmiah.\n"
            )
            
            full_report = "".join(report_lines)
            st.download_button(
                "📄 Download Laporan Lengkap (Markdown)",
                full_report, "laporan_analisis.md", "text/markdown"
            )
            
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan saat memproses file: {e}")
            st.exception(e)


if __name__ == '__main__':
    main()
