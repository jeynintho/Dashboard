import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


day_df = pd.read_csv("data/cleaned_day.csv")
hour_df = pd.read_csv("data/cleaned_hour.csv")

data = pd.read_csv("day.csv")
data2 = pd.read_csv("hour.csv")

st.set_page_config(
    page_title='Dashboard',
)

st.markdown(
    """
    <style>        
        /* Memperkecil ukuran input */
        div[data-baseweb="input"] {
            max-width: 180px;
            
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
        """
        <h1 style="text-align: center; font-size: 35px; color: black;">Bike Sharing Dashboard</h1>
        """, unsafe_allow_html=True
    )
st.write('<hr>', unsafe_allow_html=True) #hr Garis Pemisah

def create_monthly_count_df(df):
    df["mnth"] = pd.Categorical(df["mnth"], categories=[
        'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], ordered=True)

    monthly_count = df.groupby(by=["mnth","yr"], observed=False).agg({
        "cnt": "sum"
    }).reset_index()

    return monthly_count

def create_sum_byhour_df(df):
    sum_byhour_df = df.groupby("hr").cnt.sum().sort_values(ascending=False).reset_index()
    
    return sum_byhour_df

def create_sum_byseason_df(df):
    sum_byseason_df = df.groupby("season").cnt.sum().sort_values(ascending=False).reset_index()
    
    return sum_byseason_df

def create_weather_counts_sorted_df(df):
    # Mapping angka menjadi label kondisi cuaca
    CUACA = {
        1: 'Cerah, Sedikit Berawan, Seagian Berawan ',
        2: 'Kabut + Berawan, Kabut + awan Pecah, Kabut + Sedikit Berawan ',
        3: 'Saju Ringan, Hujan Ringan + Badai Petir + Awan Bertebaran ',
        4: 'Hujan Lebat + Es + Badai Petir + Kabut, Salju + Kabut '
    }

    # Mengganti nilai angka weathersit dengan label kondisi cuaca
    df['CUACA'] = df['weathersit'].map(CUACA)

    # Menghitung total jumlah penyewaan sepeda untuk setiap kondisi cuaca
    weather_counts = df.groupby('CUACA')['cnt'].sum().reset_index().rename(columns={'cnt': 'JUMLAH'})

    # Mengurutkan DataFrame berdasarkan jumlah penyewaan sepeda
    weather_counts_sorted = weather_counts.sort_values(by='JUMLAH', ascending=False)
    
    return weather_counts_sorted

def create_size_registeredcasual(df):
    # Data
    sizes = [df['casual'].sum(), df['registered'].sum()]

    return sizes

# =====================================================================

datetime_columns = ["dteday"]
day_df.sort_values(by="instant", inplace=True)
day_df.reset_index(inplace=True)

for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

# Input tanggal terpisah

st.subheader('Grafik Jumlah Pelanggan Pada Tahun 2011 Sampai 2012')

start_date = st.date_input("Tanggal Mulai", min_value=min_date, max_value=max_date, value=min_date)
end_date = st.date_input("Tanggal Selesai", min_value=min_date, max_value=max_date, value=max_date)


main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]
main_df2 = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                (hour_df["dteday"] <= str(end_date))]

monthly_count = create_monthly_count_df(main_df)
sum_byhour_df = create_sum_byhour_df(main_df2)
sum_byseason_df = create_sum_byseason_df(main_df)
weather_counts_sorted = create_weather_counts_sorted_df(main_df)
sizes = create_size_registeredcasual(main_df)

# Membuat plot dengan ukuran gambar yang ditentukan
fig, ax = plt.subplots(figsize=(45, 20))

# Mendefinisikan warna untuk setiap tahun
colors = {2011: 'blue', 2012: 'black'}

sns.lineplot(
    data=monthly_count,
    x="mnth",
    y="cnt",
    hue="yr",
    palette=colors,  # Menggunakan warna yang ditentukan sebelumnya
    marker="o",
    markersize=15
    )

ax.set_title("Grafik Jumlah Pelanggan Pada Tahun 2011 Sampai 2012", fontsize=50)
ax.set_xlabel('Bulan', fontsize=50)
ax.set_ylabel('Jumlah Pelanggan', fontsize=50)
legend = ax.legend(title="Tahun", loc="upper right", fontsize=50)
legend.get_title().set_fontsize('35')  # Adjust font size as needed
plt.tight_layout()
ax.tick_params(axis='x', labelrotation=45, labelsize=45)
ax.tick_params(axis='y', labelsize=45)

st.pyplot(fig)

#Expander Grafik
with st.expander("Penjelasan Grafik Jumlah Pelanggan Pada Tahun 2011 Sampai 2012") :
    st.write('Dilihat dari grafik total pengguna sepeda pada tahun 2011. pada bulan januari memiliki pengguna dengan jumlah lebih 100.000 dengan setiap bulan nya meningkat drastis sampai di bulan september dengan jumlah pengguna mencapai lebih dari 200.000, lalu mengalami penurunan pada bulan bulan selanjutnya hingga pada bulan desember mencapai kurang lebih 125.000 pengguna dan pada awal tahun di 2012 di bulan januari kurang dari 50.000 pengguna. lalu di bulan selanjutnya mengalami kenaikan pada bulan Juni hingga lebih dari 125.000 pengguna dan mengalami penurunan kembali di bulan Juli, Agustus, September, November dan pada bulan December mencapai Kurang lebih dari 75.000 pengguna.') 
    
st.write('<hr>', unsafe_allow_html=True) #hr Garis Pemisah

# ===========================================================

# Mengubah Angka Menjadi Nama
season_names = ['Semi', 'Dingin', 'Panas', 'Gugur']

# Mengubah nilai season menjadi nama musim
season_mapping = {1: 'Semi', 2: 'Dingin', 3: 'Panas', 4: 'Gugur'}
data['season'] = data['season'].map(season_mapping)
# Menghitung Total Penyewaan Per Musim
total_by_season = data.groupby('season')['cnt'].sum().sort_values()
# Menghitung jumlah penyewa sepeda berdasarkan workingday dan season
summary = data.groupby(['season', 'workingday'])['cnt'].sum().unstack()
# Menghitung total penyewa berdasarkan jenis dan musim
total_season = data.groupby('season')[['registered', 'casual']].sum()

# =================================================================


########### GRAFIK BAR PENYEWAAN SEPEDA PER MUSIM ############


# Membuat bar plot dengan sumbu Y yang lebih jelas
plt.figure(figsize=(8, 5))
bars = plt.bar(season_names, total_by_season, color=['#e3384a', '#cdc0c1', '#cdc0c1', '#e3384a'])

data_penyewaan = pd.DataFrame({
    'MUSIM' : season_names,
    'JUMLAH' : total_by_season.values
})

st.header('Grafik Pengguna Sepeda Per Musim Pada 2011 dan 2012')
st.dataframe(data_penyewaan)
# Menambahkan label angka di atas setiap batang
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:,}', ha='center', va='bottom', fontsize=10)
plt.title('Total Pengguna Per Musim Pada 2011 Dan 2012', fontsize=14)
plt.xlabel('MUSIM', fontsize=12)
plt.ylabel('Total Pengguna', fontsize=12)
plt.xticks(fontsize=10, rotation=30)  # Rotasi label sumbu X
plt.yticks(range(0, int(max(total_by_season)) + 100000, 100000), 
           [f'{x:,}' for x in range(0, int(max(total_by_season)) + 100000, 100000)], fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

st.pyplot(plt)

#Expander Grafik
with st.expander("Penjelasan Penyewaan Sepeda Setiap Musim") :
    st.write('Dilihat dari grafik total pengguna per Musim, Terlihat Bahwa Pengguna Tertinggi Terjadi Pada Musim Gugur Dengan Jumlah 1.061.129 Pengguna. dan Pengguna Terendah Terjadi Pada Musim Semi Dengan Jumlah 471.348 Pengguna') 
    
st.write('<hr>', unsafe_allow_html=True) #hr Garis Pemisah


########### Grafik Pengguna Terdaftar dan Non-Terdaftar Berdasarkan Musim ############


# Mengganti nama kolom pada DataFrame
total_season.rename(columns={"registered": "Registered", "casual": "Casual"}, inplace=True)
# Menampilkan tabel total penyewa
st.header("Grafik Pengguna Registered dan Casual Berdasarkan Musim")
st.dataframe(total_season)
# Membuat grafik batang
plt.figure(figsize=(10, 6))
bar_width = 0.4
index = range(len(total_season))
bars1 = plt.bar(index, total_season['Registered'], bar_width, label='Registered', color='blue')
bars2 = plt.bar([i + bar_width for i in index], total_season['Casual'], bar_width, label='Casual', color='orange')
# Menambahkan nilai di atas chart
for bar in bars1:
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50, str(int(bar.get_height())), ha='center', va='bottom', color='black')
for bar in bars2:
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50, str(int(bar.get_height())), ha='center', va='bottom', color='black')
plt.xlabel('Musim')
plt.ylabel('Jumlah Pengguna')
plt.title('Total Pengguna Yang Registered Dan Casual Per Musim')
plt.xticks([i + bar_width / 2 for i in index], total_season.index)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend()
st.pyplot(plt)

#Expander Grafik
with st.expander("Penjelasan Pengguna Sepeda Yang Registered Dan Casual Setiap Musim") :
    st.write('Dilihat dari grafik diatas,jumlah pengguna sepeda yang Registered per musim dengan jumlah terbanyak berada di musim panas dengan total jumlah 835.038 dan yang paling sedikit di musim semi dengan jumlah 410.726. Adapun jumlah pengguna yang Casual tertinggi berada dimusim semi yaitu dengan jumlah total 226.091 dan terendah di musim semi dengan jumlah 60.622.  ') 
    
st.write('<hr>', unsafe_allow_html=True) #hr Garis Pemisah


########### Grafik Penyewa Sepeda Weekday Dan Weekend ############


# Mengubah nama kolom
summary.columns = ['Weekend', 'Weekday']
# Menampilkan data summary di Streamlit
st.header("Grafik Penyewa Sepeda Weekday Dan Weekend Per Musim")
st.dataframe(summary)

# Membuat grafik
fig, ax = plt.subplots(figsize=(11, 8))
summary.plot(kind='bar', ax=ax)
ax.set_title('Jumlah Pengguna Sepeda Berdasarkan WeekDay Dan Weekend')
ax.set_xlabel('Musim')  
ax.set_ylabel('Jumlah Pengguna')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(fontsize=10, rotation=0)  # Rotasi label sumbu X
ax.legend(['Weekend', 'Weekday'])

# Tambahkan label angka pada bar chart
for container in ax.containers:
    ax.bar_label(container, fmt='%d', fontsize=10, padding=3)
# Menampilkan grafik di Streamlit
st.pyplot(fig)

 #Expander Grafik
with st.expander("Penjelasan Jumlah Pengguna Sepeda Berdasarkan WeekDay Dan Weekend") :
    st.write('Dilihat dari grafik diatas,jumlah pengguna tertingi di hari weekday berada di musim panas yaitu dengan total 749.073 dan yang terendah berada di musim semi dengan total 333.665, Adapun di hari weekend jumlah pengguna tertinggi berada di musim panas dengan jumlah 312.056 dan yang paling terendah berada di musim semi dengan total 137.683. ') 
    
st.write('<hr>', unsafe_allow_html=True) #hr Garis Pemisah


############## Grafik Pengguna Berdasarkan Cuaca #############

st.subheader("Grafik Jumlah Pengguna Berdasarkan Cuaca ")

st.dataframe(weather_counts_sorted)

# Membuat bar plot
fig, ax = plt.subplots(figsize=(15, 10))
sns.barplot(data=weather_counts_sorted, x='JUMLAH', y='CUACA')
ax.set_xlabel('Jumlah Pengguna Sepeda', fontsize=30)
ax.set_ylabel(None)
ax.set_title('Jumlah Pengguna Berdasarkan Cuaca', fontsize=35)
ax.tick_params(axis='x', labelsize=25)
ax.tick_params(axis='y', labelsize=25)
plt.grid(axis='x', linestyle='--', alpha=0.9)

# Menyesuaikan tampilan sumbu X agar tidak menggunakan skala eksponensial
ax.set_xlim(0, 2800000)  # Set batas hingga 2.400.000
ax.set_xticks(range(0, 2800001, 500000))  # Buat ticks di 0, 600rb, 1.2jt, 1.8jt, 2.4jt
ax.ticklabel_format(style='plain', axis='x')  # Pastikan format angka biasa, bukan eksponensial


# Menambahkan label angka di tengah batang
for bar in ax.containers:
    ax.bar_label(bar, fmt="%.0f", padding=3, fontsize=25, color="black")

st.pyplot(fig)

 #Expander Grafik
with st.expander("Penjelasan Jumlah Pengguna Berdasarkan Cuaca") :
    st.write('Dilihat dari grafik diatas,jumlah pengguna sepeda tertingi berada di saat cuaca sedang Cerah, Sedikit Berawan, Sebagian Berawan dan tidak ada pengguna yang menyewa di saat cuaca sedang Hujan Lebat + Es + Badai Petir + Kabut, Salju + Kabut  ') 
    
st.write('<hr>', unsafe_allow_html=True) #hr Garis Pemisah

# ========= Grafik Korelasi Temperatur ============

# Nama bulan
month_names = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]

data['dteday'] = pd.to_datetime(data['dteday'])  # Konversi kolom tanggal

data['year'] = data['dteday'].dt.year  # Ambil tahun dari tanggal
data['month'] = data['dteday'].dt.month  # Ambil bulan dari tanggal

# Denormalisasi suhu
data['temp_actual'] = data['temp'] * 41  # Mengonversi suhu ke skala sebenarnya

# Filter data untuk tahun 2011
df_2011 = data[data['year'] == 2011]
df_2012 = data[data['year'] == 2012]
avg_temp_2011 = df_2011.groupby('month')['temp_actual'].mean()
avg_temp_2012 = df_2012.groupby('month')['temp_actual'].mean()

# Streamlit UI
st.subheader("Grafik Rata-rata Suhu pada 2011 dan 2012")

# Gabungkan data untuk tahun 2011 dan 2012
comparison_df = pd.DataFrame({
    "Bulan": month_names,  # Menggunakan nama bulan
    "2011": avg_temp_2011.values, 
    "2012": avg_temp_2012.values
})

# Menampilkan tabel
st.dataframe(comparison_df)


# Plot rata-rata suhu per bulan
fig, ax = plt.subplots()
ax.plot(avg_temp_2011.index, avg_temp_2011.values, marker='o', linestyle='-', color='blue', label="2011")
ax.plot(avg_temp_2012.index, avg_temp_2012.values, marker='o', linestyle='-', color='red', label="2012")
ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-rata Suhu (°C)")
ax.set_title("Rata-rata Suhu per Bulan pada 2011 dan 2012")
legend = ax.legend(title="Tahun", loc="upper right", fontsize=8)
legend.get_title()
ax.set_xticks(range(1, 13))
ax.set_xticklabels(month_names)
st.pyplot(fig)

 #Expander Grafik
with st.expander("Penjelasan Rata-rata Suhu Pada Tahun 2011 dan 2012") :
    st.write('Dilihat dari grafik diatas, Bahwa Suhu Tertinggi Terjadi Pada Juli Dengan Rata Rata 30 Derajat Celcius pada tahun 2011 Sedangkan Pada tahun 2012 Rata rata nya adalah 31 Derajat Celcius. Dan Suhu Terendah terjadi Pada Bulan Januari dengan rata-rata adalah 8 Derajat Celcius Pada Tahun 2011 Sedangkan Pada tahun 2012 rata rata nya adalah 11 Derajat Celcius')
st.write('<hr>', unsafe_allow_html=True) #hr Garis Pemisah

########### Grafik Rata rata Kecepatan Angin Pada tahun 2011 dan 2012 #############

data['dteday'] = pd.to_datetime(data['dteday'])  # Konversi kolom tanggal

data['year'] = data['dteday'].dt.year  # Ambil tahun dari tanggal
data['month'] = data['dteday'].dt.month  # Ambil bulan dari tanggal

# Denormalisasi windspeed
data['windspeed_actual'] = data['windspeed'] * 67  # Mengonversi windspeed ke skala sebenarnya

# Filter data untuk tahun 2011 dan 2012
df_2011 = data[data['year'] == 2011]
df_2012 = data[data['year'] == 2012]
avg_windspeed_2011 = df_2011.groupby('month')['windspeed_actual'].mean()
avg_windspeed_2012 = df_2012.groupby('month')['windspeed_actual'].mean()

# Nama bulan
month_names = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]

# Streamlit UI
st.subheader("Grafik Analisis Rata-rata Windspeed pada 2011 dan 2012 berdasarkan Bulan")

# Gabungkan data untuk tahun 2011 dan 2012
comparison_df = pd.DataFrame({
    "Bulan": month_names,  # Menggunakan nama bulan
    "2011": avg_windspeed_2011.values, 
    "2012": avg_windspeed_2012.values
})

# Menampilkan tabel
st.dataframe(comparison_df)

# Plot rata-rata windspeed per bulan
fig, ax = plt.subplots()
ax.plot(avg_windspeed_2011.index, avg_windspeed_2011.values, marker='o', linestyle='-', color='brown', label="2011")
ax.plot(avg_windspeed_2012.index, avg_windspeed_2012.values, marker='o', linestyle='-', color='orange', label="2012")
ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-rata Windspeed (km/h)")
ax.set_title("Rata-rata Windspeed per Bulan pada 2011 dan 2012")
ax.set_xticks(range(1, 13))
ax.set_xticklabels(month_names)
ax.legend()

st.pyplot(fig)

# Expander Grafik
with st.expander("Penjelasan Rata-rata Kecepatan Angin Pada Tahun 2011 dan 2012") :
    st.write('Dilihat dari grafik diatas, bahwa Kecepatan Angin Tertinggi Pada tahun 2011 dan 2012 terjadi pada Bulan April Dengan Rata-rata 16 Kilometer / jam pada tahun 2011 dan 15 Kilometer / jam pada tahun 2012. dan Kecepatan Angin Terendah Pada Tahun 2011 Terjadi Pada Bulan September Yaitu 10 kilometer / jam. sedangkan pada tahun 2012 terjadi pada bulan agustus dengan rata rata 10 kilometer / jam')
st.write('<hr>', unsafe_allow_html=True) #hr Garis Pemisah