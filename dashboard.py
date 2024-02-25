import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

#Fungsi - fungsi untuk menyiapkan Dataframe yang akan digunakan untuk Visualisasi Data
def  create_group_by_2011_df(df):
    filtered_2011 = df[df['yr'] == 0]
    group_by_2011 = filtered_2011.groupby('mnth')['cnt'].sum()
    return  group_by_2011
def create_group_by_2012_df(df):
    filtered_2012 = df[df['yr'] == 1]
    group_by_2012 = filtered_2012.groupby('mnth')['cnt'].sum()
    return group_by_2012
def create_yearly_users_df(df):
    yearly_users = df.groupby('yr')['cnt'].sum()
    return yearly_users
def create_group_by_weathersit_df(df):
    group_by_weathersit = df.groupby('weathersit')['cnt'].sum()
    return group_by_weathersit 
def create_group_by_hour_df(df):
    group_by_hour = df.groupby('hr')['cnt'].sum()
    return group_by_hour

#Membaca data csv yang sudah dibersihkan
cleaned_day_df = pd.read_csv("cleaned_day.csv")
cleaned_hour_df = pd.read_csv("cleaned_hour.csv")

#Mengurutkan data berdasarkan kolom dteday
datetime_columns = ["dteday"]
cleaned_day_df.sort_values(by="dteday", inplace=True)
cleaned_day_df.reset_index(inplace=True)
cleaned_hour_df.sort_values(by="dteday", inplace=True)
cleaned_hour_df.reset_index(inplace=True)

#Memastikan kolom dteday memiliki tipe data datetime
for column in datetime_columns:
    cleaned_day_df[column] = pd.to_datetime(cleaned_day_df[column])
    cleaned_hour_df[column] = pd.to_datetime(cleaned_hour_df[column])

#Memfilter data berdasarkan kolom dteday menggunakan widget date input
min_date = cleaned_day_df["dteday"].min()
max_date = cleaned_day_df["dteday"].max()
with st.sidebar:
    st.header('Bike Sharing Company :bike:')
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
main_day_df = cleaned_day_df[(cleaned_day_df["dteday"] >= str(start_date)) & 
                (cleaned_day_df["dteday"] <= str(end_date))]
main_hour_df = cleaned_hour_df[(cleaned_hour_df["dteday"] >= str(start_date)) & 
                (cleaned_hour_df["dteday"] <= str(end_date))]

#Menyiapkan dataframe untuk Visualisasi Data
group_by_2011 = create_group_by_2011_df(main_day_df)
group_by_2012 = create_group_by_2012_df(main_day_df)
yearly_users = create_yearly_users_df(main_day_df)
group_by_weathersit = create_group_by_weathersit_df(main_hour_df)
group_by_hour = create_group_by_hour_df(main_hour_df)

#Membuat Header Dashboard
st.header('Bike Sharing Dashboard :sparkles:')

#Visualisasi data pengguna sepeda pada tahun 2011
st.subheader('Distribution of Bicycle Users in 2011')
fig, ax = plt.subplots(figsize=(19, 8))
nama_bulan = {
    1: 'Januari',
    2: 'Februari',
    3: 'Maret',
    4: 'April',
    5: 'Mei',
    6: 'Juni',
    7: 'Juli',
    8: 'Agustus',
    9: 'September',
    10: 'Oktober',
    11: 'November',
    12: 'Desember'
}
group_by_2011.index = group_by_2011.index.map(nama_bulan)
ax.plot(
    group_by_2011.index,
    group_by_2011.values,
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

#Visualisasi data pengguna sepeda pada tahun 2012
st.subheader('Distribution of Bicycle Users in 2012')
fig, ax = plt.subplots(figsize=(19, 8))
group_by_2012.index = group_by_2012.index.map(nama_bulan)
ax.plot(
    group_by_2012.index,
    group_by_2012.values,
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

#Visualisasi data total pengguna sepeda pada tahun 2011 dan 2012
st.subheader('Years With The Highest Number of Bicycle Users')
tahun = {
    0: '2011',
    1: '2012'
}
yearly_users_df = yearly_users.reset_index()
yearly_users_df['yr'] = yearly_users_df['yr'].map(tahun)
col1, col2 = st.columns(2)
with col1: #Menampilkan angka total pengguna sepeda pada tahun 2011
    if '2011' in yearly_users_df['yr'].unique():
        total_2011 = yearly_users_df[yearly_users_df['yr'] == '2011']['cnt'].values[0]
        st.metric("Total of Bicycle Users in 2011", value=total_2011)
    else :
        total_2011 = 0
        st.metric("Total of Bicycle Users in 2011", value=total_2011)
with col2: #Menampilkan angka total pengguna sepeda pada tahun 2011
    if '2012' in yearly_users_df['yr'].unique():
        total_2012 = yearly_users_df[yearly_users_df['yr'] == '2012']['cnt'].values[0]
        st.metric("Total of Bicycle Users in 2012", value=total_2012)
    else :
        total_2012 = 0
        st.metric("Total of Bicycle Users in 2012", value=total_2012)
fig, ax = plt.subplots(figsize=(16, 10))
colors = ['#90CAF9' if cnt == yearly_users_df['cnt'].max() else '#D3D3D3' for cnt in yearly_users_df['cnt']]
sns.barplot(data=yearly_users_df, x='yr', y='cnt', palette = colors)
ax.tick_params(axis='y', labelsize=17)
ax.tick_params(axis='x', labelsize=17)
ax.set_xlabel('')
ax.set_ylabel('')
st.pyplot(fig)

#Visualisasi data jumlah pengguna sepeda berdasarkan kondisi cuaca
st.subheader('Distribution of Bicycle Users Based on Weathersit')
cuaca = {
    1: 'Cerah',
    2: 'Kabut/Berawan',
    3: 'Hujan Ringan',
    4: 'Hujan Lebat/Badai'
}
group_by_weathersit_df = group_by_weathersit.reset_index()
group_by_weathersit_df['weathersit'] = group_by_weathersit_df['weathersit'].map(cuaca)
fig, ax = plt.subplots(figsize=(16, 10))
sns.barplot(data=group_by_weathersit_df, x='weathersit', y='cnt', color="#90CAF9")
ax.set_yscale('log')
ax.tick_params(axis='y', labelsize=17)
ax.tick_params(axis='x', labelsize=17)
ax.set_xlabel('')
ax.set_ylabel('Jumlah Pengguna Sepeda (skala log)',fontsize = 19)
st.pyplot(fig)

#Visualisasi data jumlah pengguna sepeda berdasarkan jam dalam sehari
st.subheader('Distribution of Bicycle Users by Hours of The Day')
fig, ax = plt.subplots(figsize=(16, 10))
def terjemahkan_hour(hour):
    return f'{hour:02}:00'
group_by_hour.index = group_by_hour.index.map(terjemahkan_hour)
ax.plot(
    group_by_hour.index,
    group_by_hour.values,
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=17,rotation=90)
st.pyplot(fig)