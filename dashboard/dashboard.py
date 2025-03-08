import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from babel.numbers import format_currency

# Konfigurasi Streamlit
st.set_page_config(page_title="Dashboard Analisis Data E-Commerce", layout="wide")

# **Pastikan path dataset benar**
DATA_DIR = "../data/"  # Semua dataset CSV ada di folder `data`
DASHBOARD_DIR = "./"  # `dashboard.py` dan `all_data.csv` ada di folder `dashboard/`

DATASETS = {
    "orders": "orders_dataset.csv",
    "order_items": "order_items_dataset.csv",
    "order_payments": "order_payments_dataset.csv",
    "order_reviews": "order_reviews_dataset.csv",
    "customers": "customers_dataset.csv",
    "geolocation": "geolocation_dataset.csv",
    "sellers": "sellers_dataset.csv",
    "products": "products_dataset.csv",
    "category_translation": "product_category_name_translation.csv"
}

# **Fungsi untuk memuat semua dataset**
@st.cache_data
def load_data():
    data = {}
    for key, filename in DATASETS.items():
        file_path = os.path.join(DATA_DIR, filename)
        if not os.path.exists(file_path):
            st.error(f"❌ File {file_path} tidak ditemukan! Harap letakkan file di direktori yang benar.")
            return None
        data[key] = pd.read_csv(file_path)
    
    # **Load all_data.csv dari folder `dashboard/`**
    all_data_path = os.path.join(DASHBOARD_DIR, "all_data.csv")
    if os.path.exists(all_data_path):
        data["all_data"] = pd.read_csv(all_data_path)
    else:
        st.error(f"❌ File {all_data_path} tidak ditemukan! Harap letakkan file di direktori yang benar.")
        return None

    return data

# **Load semua dataset**
data = load_data()
if data is None:
    st.stop()  # Hentikan Streamlit jika file tidak ditemukan

# **Gabungkan Data**
orders = data["orders"]
order_items = data["order_items"]
order_payments = data["order_payments"]
order_reviews = data["order_reviews"]
customers = data["customers"]
geolocation = data["geolocation"]
sellers = data["sellers"]
products = data["products"]
category_translation = data["category_translation"]
all_data = data["all_data"]

# **Konversi tipe data**
orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])
orders["order_delivered_customer_date"] = pd.to_datetime(orders["order_delivered_customer_date"])
orders["bulan"] = orders["order_purchase_timestamp"].dt.to_period("M").astype(str)

# **Gabungkan data order dengan pelanggan**
df = orders.merge(customers, on="customer_id", how="left")
df = df.merge(order_items, on="order_id", how="left")
df = df.merge(products, on="product_id", how="left")
df = df.merge(order_payments, on="order_id", how="left")

# **Menghitung waktu pengiriman dalam hari**
df["delivery_time"] = (df["order_delivered_customer_date"] - df["order_purchase_timestamp"]).dt.days

# **Sidebar - Filter Waktu**
st.sidebar.header("📅 Filter Data")
min_date, max_date = df["order_purchase_timestamp"].min(), df["order_purchase_timestamp"].max()
start_date, end_date = st.sidebar.date_input("Pilih Rentang Waktu:", [min_date, max_date], min_value=min_date, max_value=max_date)

# **Filter Data berdasarkan tanggal**
filtered_df = df[(df["order_purchase_timestamp"] >= pd.to_datetime(start_date)) & 
                 (df["order_purchase_timestamp"] <= pd.to_datetime(end_date))]

# **Dashboard Header**
st.title("📊 Dashboard Analisis Data E-Commerce")
st.markdown("---")

### **1. Analisis Produk Terlaris**
st.subheader("🏆 Produk Terlaris")
top_products = filtered_df["product_category_name"].value_counts().head(10)
fig_top_products = px.bar(top_products, x=top_products.index, y=top_products.values, 
                          labels={'x': 'Kategori Produk', 'y': 'Jumlah Terjual'}, 
                          title="Top 10 Produk Terlaris", color=top_products.values, 
                          color_continuous_scale="Blues")
st.plotly_chart(fig_top_products, use_container_width=True)

### **2. Metode Pembayaran**
st.subheader("💳 Metode Pembayaran yang Paling Banyak Digunakan")
payment_counts = filtered_df["payment_type"].value_counts()
fig_payment = px.pie(values=payment_counts.values, names=payment_counts.index, 
                     title="Distribusi Metode Pembayaran", color_discrete_sequence=px.colors.qualitative.Set3)
st.plotly_chart(fig_payment, use_container_width=True)

### **3. Kota & Negara Bagian dengan Pesanan Terbanyak**
st.subheader("📍 Kota dan Negara Bagian dengan Pesanan Terbanyak")
top_cities = filtered_df["customer_city"].value_counts().head(10)
top_states = filtered_df["customer_state"].value_counts().head(10)

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

### **4. Tren Penjualan**
st.subheader("📈 Tren Penjualan")
filtered_df["bulan"] = filtered_df["order_purchase_timestamp"].dt.to_period("M").astype(str)
penjualan_per_bulan = filtered_df.groupby("bulan")["price"].sum().reset_index()
fig_sales = px.line(penjualan_per_bulan, x="bulan", y="price", markers=True, 
                    labels={'bulan': 'Bulan', 'price': 'Total Penjualan'}, 
                    title="Tren Penjualan per Bulan")
st.plotly_chart(fig_sales, use_container_width=True)

### **Footer**
st.sidebar.markdown("---")
st.sidebar.write("👨‍💻 Powered by: Azmi Irfala | A163YAF089@devacademy.id")
