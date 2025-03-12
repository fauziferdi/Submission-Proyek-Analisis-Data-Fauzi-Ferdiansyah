import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style="dark")


# Fungsi data penyewaan per musim
def create_seasonal_rentals_df(df_day):
    seasonal_rentals_df = df_day.groupby("season")["cnt"].sum().reset_index()
    seasonal_rentals_df.rename(columns={"cnt": "total_rentals"}, inplace=True)
    return seasonal_rentals_df


# Fungsi data penyewaan per bulan
def create_monthly_rentals_df(df_day):
    monthly_rentals_df = df_day.groupby("mnth")["cnt"].sum().reset_index()
    monthly_rentals_df.rename(
        columns={"cnt": "total_rentals", "mnth": "month"}, inplace=True
    )
    return monthly_rentals_df


# Fungsi penyewaan per periode waktu
def create_period_rentals_df(df_hour):
    def time_period(hour):
        if 6 <= hour <= 10:
            return "Pagi"
        elif 11 <= hour <= 17:
            return "Sore"
        else:
            return "Malam"

    df_hour["period"] = df_hour["hr"].apply(time_period)
    period_rentals_df = (
        df_hour.groupby("period")["cnt"].sum().sort_values(ascending=True).reset_index()
    )
    period_rentals_df.rename(columns={"cnt": "total_rentals"}, inplace=True)
    return period_rentals_df


# Load data
hour_df = pd.read_csv("dashboard/hour_final.csv")
day_df = pd.read_csv("dashboard/day_final.csv")

day_df["dteday"] = pd.to_datetime(day_df["dteday"]).dt.date
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"]).dt.date

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    st.header("Filter Rentang Waktu")
    start_date, end_date = st.date_input(
        "Pilih Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date],
    )

day_df_filtered = day_df[
    (day_df["dteday"] >= start_date) & (day_df["dteday"] <= end_date)
]
hour_df_filtered = hour_df[
    (hour_df["dteday"] >= start_date) & (hour_df["dteday"] <= end_date)
]

seasonal_rentals_df = create_seasonal_rentals_df(day_df_filtered)
monthly_rentals_df = create_monthly_rentals_df(day_df_filtered)
period_rentals_df = create_period_rentals_df(hour_df_filtered)

st.title("Bike Rental Analysis Dashboard")

# Menampilkan Informasi Jumlah Total Penyewa
total_renters = int(day_df_filtered["cnt"].sum())
st.metric("Total Peminjam Sepeda", value=total_renters)


# Visualisasi 1
st.header("Total Bike Rentals by Season")

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x="season", y="total_rentals", data=seasonal_rentals_df, ax=ax)
ax.set_title("Total Bike Rentals by Season")
ax.set_xlabel("Season")
ax.set_ylabel("Total Rentals")
st.pyplot(fig)

st.write("Grafik di atas menunjukkan total jumlah penyewaan sepeda untuk setiap musim.")

# Visualisasi 2
st.header("Total Bike Rentals by Month")

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="month", y="total_rentals", data=monthly_rentals_df, ax=ax)
ax.set_title("Total Bike Rentals by Month")
ax.set_xlabel("Month")
ax.set_ylabel("Total Rentals")
st.pyplot(fig)

st.write("Grafik di atas menunjukkan total jumlah penyewaan sepeda untuk setiap bulan.")

# Visualisasi 3
st.header("Total Bike Rentals by Period")

fig, ax = plt.subplots(figsize=(8, 5))
sns.lineplot(x="period", y="total_rentals", data=period_rentals_df, ax=ax, marker="o")
ax.set_title("Total Bike Rentals by Period")
ax.set_xlabel("Period")
ax.set_ylabel("Total Rentals")
st.pyplot(fig)

st.write(
    "Grafik di atas menunjukkan perbedaan jumlah penyewaan sepeda di berbagai waktu"
)
