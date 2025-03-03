import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('/mnt/data/all_data.csv')
    return df

df = load_data()

# Sidebar menu
st.sidebar.title("E-Commerce Dashboard")
option = st.sidebar.selectbox("Pilih Analisis:", [
    "Produk Terlaris", "Metode Pembayaran", "Pesanan Berdasarkan Kota & Negara Bagian", 
    "Waktu Pengiriman per Kategori", "Tingkat Kepuasan Pelanggan", "Tren Penjualan"
])

st.title("📊 Dashboard Analisis E-Commerce")

if option == "Produk Terlaris":
    st.subheader("Top 10 Produk Terlaris")
    top_products = df['product_category_name'].value_counts().head(10)
    fig, ax = plt.subplots()
    top_products.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_ylabel("Jumlah Pesanan")
    ax.set_xlabel("Kategori Produk")
    ax.set_title("Top 10 Produk Terlaris")
    st.pyplot(fig)

elif option == "Metode Pembayaran":
    st.subheader("Distribusi Metode Pembayaran")
    payment_counts = df['payment_type'].value_counts()
    fig, ax = plt.subplots()
    payment_counts.plot(kind='bar', ax=ax, color='orange')
    ax.set_ylabel("Jumlah Transaksi")
    ax.set_xlabel("Metode Pembayaran")
    ax.set_title("Metode Pembayaran yang Paling Sering Digunakan")
    st.pyplot(fig)

elif option == "Pesanan Berdasarkan Kota & Negara Bagian":
    st.subheader("Top 10 Kota dengan Pesanan Terbanyak")
    top_cities = df['customer_city'].value_counts().head(10)
    fig, ax = plt.subplots()
    top_cities.plot(kind='bar', ax=ax, color='green')
    ax.set_ylabel("Jumlah Pesanan")
    ax.set_xlabel("Kota")
    ax.set_title("Top 10 Kota dengan Pesanan Terbanyak")
    st.pyplot(fig)
    
    st.subheader("Top 10 Negara Bagian dengan Pesanan Terbanyak")
    top_states = df['customer_state'].value_counts().head(10)
    fig, ax = plt.subplots()
    top_states.plot(kind='bar', ax=ax, color='blue')
    ax.set_ylabel("Jumlah Pesanan")
    ax.set_xlabel("Negara Bagian")
    ax.set_title("Top 10 Negara Bagian dengan Pesanan Terbanyak")
    st.pyplot(fig)

elif option == "Waktu Pengiriman per Kategori":
    st.subheader("Rata-rata Waktu Pengiriman per Kategori Produk")
    delivery_times = df.groupby('product_category_name')['delivery_days'].mean().sort_values()
    fig, ax = plt.subplots()
    delivery_times.head(10).plot(kind='bar', ax=ax, color='purple')
    ax.set_ylabel("Rata-rata Waktu Pengiriman (hari)")
    ax.set_xlabel("Kategori Produk")
    ax.set_title("Kategori Produk dengan Pengiriman Tercepat")
    st.pyplot(fig)

elif option == "Tingkat Kepuasan Pelanggan":
    st.subheader("Distribusi Rating Pelanggan")
    fig, ax = plt.subplots()
    sns.histplot(df['review_score'], bins=5, kde=True, ax=ax, color='red')
    ax.set_xlabel("Rating")
    ax.set_ylabel("Jumlah Ulasan")
    ax.set_title("Distribusi Rating Produk")
    st.pyplot(fig)

elif option == "Tren Penjualan":
    st.subheader("Tren Penjualan dari Waktu ke Waktu")
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    df['order_date'] = df['order_purchase_timestamp'].dt.date
    sales_trend = df.groupby('order_date').size()
    fig, ax = plt.subplots()
    sales_trend.plot(ax=ax, color='darkblue', linewidth=2)
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Pesanan")
    ax.set_title("Tren Penjualan Harian")
    st.pyplot(fig)

st.sidebar.info("E-Commerce Dashboard by: Azmi Irfala")
