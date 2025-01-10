import streamlit as st
import pandas as pd

# Load the CSV files
file_ahp = "AHP Crypto.csv"
file_topsis = "TOPSIS Crypto.csv"
file_saw = "SAW Crypto.csv"
file_average = "AVERAGE Crypto.csv"

# Function to load CSV file
def load_csv(file_path):
    return pd.read_csv(file_path)

# Streamlit App
st.title("Visualisasi Data AHP, TOPSIS, SAW, dan AVERAGE")

# File 1: AHP Pembobotan
st.header("1. AHP Pembobotan")
bobot_df = load_csv(file_ahp)

if not bobot_df.empty:
    st.write("### Data Bobot")
    st.dataframe(bobot_df)

# File 2: TOPSIS
st.header("2. Perhitungan TOPSIS")
topsis_df = load_csv(file_topsis)

if not topsis_df.empty:
    st.write("### Data TOPSIS")
    st.dataframe(topsis_df)

    # Alternatif nilai tertinggi dan terendah
    highest_alternative = topsis_df.iloc[topsis_df.iloc[:, 1].idxmax()]
    lowest_alternative = topsis_df.iloc[topsis_df.iloc[:, 1].idxmin()]

    st.write(f"### Alternatif dengan Nilai Tertinggi:")
    st.write(highest_alternative)

    st.write(f"### Alternatif dengan Nilai Terendah:")
    st.write(lowest_alternative)

# File 3: SAW
st.header("3. Peringkat SAW")
saw_df = load_csv(file_saw)

if not saw_df.empty:
    st.write("### Data Peringkat")
    st.dataframe(saw_df)

    # Visualisasi Diagram Batang
    st.write("### Diagram Batang Peringkat")
    st.bar_chart(saw_df.set_index(saw_df.columns[0]))

# File 4: AVERAGE
st.header("4. Peringkat Berdasarkan AVERAGE")
average_df = load_csv(file_average)

if not average_df.empty:
    st.write("### Data AVERAGE")
    st.dataframe(average_df)

    # Dropdown untuk memilih kriteria
    selected_kriteria = st.selectbox("Pilih Kriteria untuk Penilaian:", average_df.columns[1:])

    if selected_kriteria:
        # Mengambil bobot dari file AHP Pembobotan
        if selected_kriteria in bobot_df[bobot_df.columns[0]].values:
            bobot_kriteria = bobot_df.loc[bobot_df[bobot_df.columns[0]] == selected_kriteria, bobot_df.columns[1]].values[0]
        else:
            bobot_kriteria = 1  # Default jika tidak ada bobot yang ditemukan

        # Menghitung nilai akhir dengan pembobotan
        average_df["Nilai Akhir"] = average_df[selected_kriteria] * bobot_kriteria
        sorted_average_df = average_df.sort_values(by="Nilai Akhir", ascending=False)

        st.write(f"### Peringkat Alternatif Berdasarkan: {selected_kriteria}")
        st.dataframe(sorted_average_df[[average_df.columns[0], "Nilai Akhir"]])

        # Visualisasi diagram batang
        st.write("### Diagram Batang Peringkat Berdasarkan Kriteria")
        st.bar_chart(sorted_average_df.set_index(average_df.columns[0])["Nilai Akhir"])
