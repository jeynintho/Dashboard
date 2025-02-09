import streamlit as st

st.markdown(
        """
        <h1 style="text-align: center; font-size: 30px; color: black;">Dataset characteristics</h1>
        """, unsafe_allow_html=True
    )
st.write('<hr>', unsafe_allow_html=True)
st.write(
    """
    Baik hour.csv maupun day.csv memiliki kolom berikut, kecuali hr yang tidak tersedia di day.csv
- instant : indeks rekaman
- dteday : tanggal
- season : musim (1:springer, 2:summer, 3:fall, 4:winter)
- yr : tahun (0: 2011, 1:2012)
- mnth : bulan (1 hingga 12)
- hr : jam (0 hingga 23)
- holiday : hari cuaca libur atau tidak (diekstrak dari http://dchr.dc.gov/page/holiday-schedule)
- weekday : hari dalam seminggu
- workingday : jika hari bukan akhir pekan atau hari libur adalah 1, jika tidak adalah 0.
+ weathersit :
    1. Cerah, Sedikit awan, Berawan sebagian, Berawan sebagian
    2. Kabut + Berawan, Kabut + Awan pecah, Kabut + Sedikit awan, Kabut
    3. Salju Ringan, Hujan Ringan + Badai Petir + Awan Bertebaran, Hujan Ringan + Awan Bertebaran
    4. Hujan Lebat + Es + Badai Petir + Kabut, Salju + Kabut
- temp : Suhu normal dalam Celcius. Nilai dibagi menjadi 41 (maks)
- atemp : Suhu perasaan normal dalam Celcius. Nilai dibagi menjadi 50 (maks)
- hum : Kelembaban normal. Nilai dibagi menjadi 100 (maks)
- windspeed : Kecepatan angin normal. Nilai dibagi menjadi 67 (maks)
- casual : jumlah pengguna kasual
- registered : jumlah pengguna terdaftar
- cnt : jumlah total sepeda sewaan termasuk kasual dan terdaftar
    """
) 