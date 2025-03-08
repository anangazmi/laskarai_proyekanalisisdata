import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
from babel.numbers import format_currency

sns.set(style='darkgrid')

# Konfigurasi Halaman
st.set_page_config(page_title="Dashboard Analisis Data E-Commerce", layout="wide")

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    df = pd.read_csv("all_data.csv", parse_dates=["order_purchase_timestamp", "order_delivered_customer_date"])
    df["delivery_time"] = (df["order_delivered_customer_date"] - df["order_purchase_timestamp"]).dt.days
    df["bulan"] = df["order_purchase_timestamp"].dt.to_period("M")
    return df

df = load_data()

# Sidebar Filter
st.sidebar.header("🔍 Filter Data")
min_date, max_date = df["order_purchase_timestamp"].min(), df["order_purchase_timestamp"].max()
start_date, end_date = st.sidebar.date_input("📅 Pilih Rentang Waktu:", [min_date, max_date], min_value=min_date, max_value=max_date)

# Filter Data
df_filtered = df[(df["order_purchase_timestamp"] >= str(start_date)) & (df["order_purchase_timestamp"] <= str(end_date))]

# Header Dashboard
st.title("📊 Dashboard Analisis Data E-Commerce")
st.markdown("---")

# 📌 **1. Produk Terlaris**
st.subheader("🏆 Produk Terlaris")
top_products = df_filtered["product_category_name"].value_counts().head(10)
fig_top_products = px.bar(top_products, x=top_products.index, y=top_products.values, 
                          labels={'x': 'Kategori Produk', 'y': 'Jumlah Terjual'}, 
                          title="Top 10 Produk Terlaris", color=top_products.values, 
                          color_continuous_scale="Blues")
st.plotly_chart(fig_top_products, use_container_width=True)

# 📌 **2. Metode Pembayaran**
st.subheader("💳 Metode Pembayaran Paling Populer")
payment_counts = df_filtered["payment_type"].value_counts()
fig_payment = px.pie(values=payment_counts.values, names=payment_counts.index, 
                     title="Distribusi Metode Pembayaran", 
                     color_discrete_sequence=px.colors.qualitative.Set3)
st.plotly_chart(fig_payment, use_container_width=True)

# 📌 **3. Lokasi Pesanan**
st.subheader("📍 Kota dan Negara Bagian dengan Pesanan Terbanyak")
top_cities = df_filtered["customer_city"].value_counts().head(10)
top_states = df_filtered["customer_state"].value_counts().head(10)

col1, col2 = st.columns(2)
with col1:
    fig_city = px.bar(top_cities, x=top_cities.index, y=top_cities.values, 
                      labels={'x': 'Kota', 'y': 'Jumlah Pesanan'}, 
                      title="Top 10 Kota dengan Pesanan Terbanyak", 
                      color=top_cities.values, color_continuous_scale="Purples")
    st.plotly_chart(fig_city, use_container_width=True)
with col2:
    fig_state = px.bar(top_states, x=top_states.index, y=top_states.values, 
                       labels={'x': 'Negara Bagian', 'y': 'Jumlah Pesanan'}, 
                       title="Top 10 Negara Bagian dengan Pesanan Terbanyak", 
                       color=top_states.values, color_continuous_scale="Greens")
    st.plotly_chart(fig_state, use_container_width=True)

# 📌 **4. Rata-rata Waktu Pengiriman**
st.subheader("🚚 Rata-rata Waktu Pengiriman per Kategori Produk")
delivery_time_per_category = df_filtered.groupby('product_category_name')["delivery_time"].mean().reset_index()
delivery_time_per_category = delivery_time_per_category.sort_values(by='delivery_time')
fig_delivery = px.bar(delivery_time_per_category, x='delivery_time', y='product_category_name', orientation='h', 
                      labels={'delivery_time': 'Hari', 'product_category_name': 'Kategori Produk'}, 
                      title="Waktu Pengiriman per Kategori Produk", 
                      color='delivery_time', color_continuous_scale="Oranges")
st.plotly_chart(fig_delivery, use_container_width=True)

# Filter data berdasarkan rentang waktu yang dipilih
filtered_df = df[(df["order_purchase_timestamp"] >= pd.to_datetime(start_date)) & 
                     (df["order_purchase_timestamp"] <= pd.to_datetime(end_date))]

# 📌 **5. Tren Penjualan**
# Membuat format bulan
filtered_df["bulan"] = filtered_df["order_purchase_timestamp"].dt.to_period("M").astype(str)

# Mengelompokkan data berdasarkan bulan dan menghitung total penjualan
penjualan_per_bulan = filtered_df.groupby("bulan")["price"].sum().reset_index()

# Membuat visualisasi dengan Plotly
fig_sales = px.line(penjualan_per_bulan, x="bulan", y="price", markers=True, 
                    labels={'bulan': 'Bulan', 'price': 'Total Penjualan'}, 
                    title="Tren Penjualan per Bulan")

st.plotly_chart(fig_sales, use_container_width=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.write("👨‍💻 powered by: Azmi Irfala")
