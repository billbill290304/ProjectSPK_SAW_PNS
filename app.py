import streamlit as st
import pandas as pd

# Atur lebar halaman
st.set_page_config(page_title="SPK Beasiswa - SAW", layout="wide")

# Judul Aplikasi
st.title("SPK Penerimaan Beasiswa - Metode SAW")
# st.markdown(
#     "<h2 style='text-align: center; color: #6C63FF;'>🌟 SPK Penerimaan Beasiswa - Metode SAW 🌟</h2>",
#     unsafe_allow_html=True,
# )

# Upload File
st.markdown("### 📤 Upload File CSV")
uploaded_file = st.file_uploader("Pilih file CSV dengan kolom: Nama, Nilai, Umur, Penghasilan_Ayah, Penghasilan_Ibu, Saudara", type="csv")

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.success("✅ File berhasil diunggah!")

    # Tampilkan Data Asli
    st.markdown("### 📊 Data Asli")
    st.dataframe(data.style.set_properties(**{'background-color': '#F9F9F9', 'color': 'black'}))

    # Bobot dan Kriteria
    bobot = {'Nilai': 0.3, 'Umur': 0.1, 'Penghasilan_Ayah': 0.2, 'Penghasilan_Ibu': 0.2, 'Saudara': 0.2}
    kriteria = {'Nilai': 'benefit', 'Umur': 'cost', 'Penghasilan_Ayah': 'cost', 'Penghasilan_Ibu': 'cost', 'Saudara': 'benefit'}

    # Normalisasi Data
    normalisasi = pd.DataFrame()
    for kolom in bobot:
        if kriteria[kolom] == 'benefit':
            normalisasi[kolom] = data[kolom] / data[kolom].max()
        else:
            normalisasi[kolom] = data[kolom].min() / data[kolom]
    for kolom in bobot:
        normalisasi[kolom] *= bobot[kolom]

    # Hitung Skor dan Ranking
    data['Skor_Akhir'] = normalisasi.sum(axis=1)
    data['Ranking'] = data['Skor_Akhir'].rank(ascending=False).astype(int)

    # Tampilkan Hasil
    st.markdown("### 🏆 Hasil Perhitungan dan Ranking")
    hasil = data.sort_values(by='Ranking')[['Nama', 'Skor_Akhir', 'Ranking']].reset_index(drop=True)

    # Tambahkan Progress Bar untuk Skor
    for i, row in hasil.iterrows():
        st.markdown(f"**{row['Ranking']}. {row['Nama']}**")
        st.progress(min(row['Skor_Akhir'], 1.0))

    st.dataframe(hasil.style.background_gradient(cmap='YlGn'))
else:
    st.info("📎 Silakan upload file CSV terlebih dahulu.")