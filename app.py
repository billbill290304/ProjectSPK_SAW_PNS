import streamlit as st
import pandas as pd

# Atur lebar halaman
st.set_page_config(page_title="SPK Beasiswa - SAW", layout="wide")

# Judul Aplikasi
st.title("SPK Penerimaan Beasiswa - Metode SAW")

# Input Nama
nama_input = st.text_input("✏️ Masukkan Nama Lengkap Anda dengan format Aa Bb")

# Upload File
st.markdown("### 📤 Upload File CSV")
uploaded_file = st.file_uploader("Pilih file CSV dengan kolom: Nama, Nilai, Umur, Penghasilan_Ayah, Penghasilan_Ibu, Saudara", type="csv")

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.success("✅ File berhasil diunggah!")

    col1, col2 = st.columns(2)

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

    with col1:
        st.markdown("### 📊 Data Asli")
        # Hapus kolom Skor_Akhir dan Ranking hanya dari tampilan
        data_tanpa_skor = data.drop(columns=['Skor_Akhir', 'Ranking'])
        st.dataframe(data_tanpa_skor.style.set_properties(**{'background-color': '#F9F9F9', 'color': 'black'}))

    with col2:
        st.markdown("### 🏆 Hasil Perhitungan dan Ranking")
        hasil = data.sort_values(by='Ranking')[['Nama', 'Skor_Akhir', 'Ranking']].reset_index(drop=True)
        st.dataframe(hasil.style.background_gradient(cmap='YlGn'))

    # Cek apakah nama ada dalam top 25
    if nama_input:
        hasil_nama = hasil[hasil['Nama'].str.lower() == nama_input.strip().lower()]
        if not hasil_nama.empty:
            peringkat = hasil_nama['Ranking'].values[0]
            if peringkat <= 25:
                st.success(f"🎉 Selamat, {nama_input}! Anda termasuk dalam 25 penerima beasiswa.")
                st.toast("Horee, Anda beruntung", icon="🎉")
            else:
                st.warning(f"😥 Maaf, {nama_input} belum termasuk dalam 25 penerima beasiswa.")
                st.toast("Yaah, Maaf kamu belum beruntung", icon="😥")
        else:
            st.error(f"❌ Nama '{nama_input}' tidak ditemukan dalam data.")
            st.toast("Mau cari siapa??", icon="❌")
else:
    st.info("📎 Silakan upload file CSV terlebih dahulu / 📥 [Download file contoh CSV di sini](https://drive.google.com/file/d/1U5TpqaNXFVI_oTgb6PGvSdOPKB6CBXuw/view?usp=sharing)")
