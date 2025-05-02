import streamlit as st
import pandas as pd

st.title("SPK Penerimaan Beasiswa - Metode SAW")

# Upload data
uploaded_file = st.file_uploader("", type="csv")

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.subheader("Data Asli")
    st.dataframe(data)

    # Bobot dan kriteria
    bobot = {'Nilai': 0.3, 'Umur': 0.1, 'Penghasilan_Ayah': 0.2, 'Penghasilan_Ibu': 0.2, 'Saudara': 0.2}
    kriteria = {'Nilai': 'benefit', 'Umur': 'cost', 'Penghasilan_Ayah': 'cost', 'Penghasilan_Ibu': 'cost', 'Saudara': 'benefit'}

    # Normalisasi
    normalisasi = pd.DataFrame()
    for kolom in bobot:
        if kriteria[kolom] == 'benefit':
            normalisasi[kolom] = data[kolom] / data[kolom].max()
        else:
            normalisasi[kolom] = data[kolom].min() / data[kolom]
    for kolom in bobot:
        normalisasi[kolom] *= bobot[kolom]

    data['Skor_Akhir'] = normalisasi.sum(axis=1)
    data['Ranking'] = data['Skor_Akhir'].rank(ascending=False).astype(int)

    st.subheader("Hasil Ranking")
    st.dataframe(data.sort_values(by='Ranking')[['Nama', 'Skor_Akhir', 'Ranking']])

else:
    st.info("Silakan upload file CSV terlebih dahulu.")