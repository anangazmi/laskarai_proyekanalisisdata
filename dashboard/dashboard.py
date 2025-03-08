import pandas as pd
import streamlit as st
from babel.numbers import format_currency
import plotly.express as px

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe

def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "payment_value": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_id": "order_count",
        "payment_value": "revenue"
    }, inplace=True)
    
    return daily_orders_df

def create_sum_order_items_df(df):
    sum_order_items_df = df.groupby("product_id").price.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def create_bycity_df(df):
    bycity_df = df.groupby(by="customer_city").customer_id.nunique().reset_index()
    bycity_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    
    return bycity_df

def create_bystate_df(df):
    bystate_df = df.groupby(by="customer_state").customer_id.nunique().reset_index()
    bystate_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    
    return bystate_df

def create_rfm_df(df):
    rfm_df = df.groupby(by="customer_id", as_index=False).agg({
        "order_purchase_timestamp": "max",
        "order_id": "nunique",
        "payment_value": "sum"
    })
    rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
    
    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = df["order_purchase_timestamp"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
    
    return rfm_df

# Load cleaned data
all_df = pd.read_csv("all_data.csv")

# Konversi kolom datetime
datetime_columns = ["order_purchase_timestamp", "order_delivered_customer_date"]
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Filter data berdasarkan tanggal
min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data berdasarkan rentang tanggal
main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                 (all_df["order_purchase_timestamp"] <= str(end_date))]

# Menyiapkan berbagai dataframe
daily_orders_df = create_daily_orders_df(main_df)
sum_order_items_df = create_sum_order_items_df(main_df)
bycity_df = create_bycity_df(main_df)
bystate_df = create_bystate_df(main_df)
rfm_df = create_rfm_df(main_df)

# Tampilkan dashboard
st.header('E-Commerce Dashboard :sparkles:')
st.subheader('Daily Orders')

col1, col2 = st.columns(2)

with col1:
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total orders", value=total_orders)

with col2:
    total_revenue = format_currency(daily_orders_df.revenue.sum(), "BRL", locale='pt_BR') 
    st.metric("Total Revenue", value=total_revenue)

# Plot daily orders dengan Plotly
fig = px.line(daily_orders_df, x="order_purchase_timestamp", y="order_count", title="Daily Orders")
st.plotly_chart(fig)

# Product performance
st.subheader("Best & Worst Performing Product")

fig1 = px.bar(sum_order_items_df.head(5), x="price", y="product_id", title="Best Performing Product")
fig2 = px.bar(sum_order_items_df.sort_values(by="price", ascending=True).head(5), x="price", y="product_id", title="Worst Performing Product")

st.plotly_chart(fig1)
st.plotly_chart(fig2)

# Customer demographics
st.subheader("Customer Demographics")

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(bycity_df.sort_values(by="customer_count", ascending=False).head(5), y="customer_count", x="customer_city", title="Number of Customer by City")
    st.plotly_chart(fig)

with col2:
    fig = px.bar(bystate_df.sort_values(by="customer_count", ascending=False).head(5), y="customer_count", x="customer_state", title="Number of Customer by State")
    st.plotly_chart(fig)

# Best Customer Based on RFM Parameters
st.subheader("Best Customer Based on RFM Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)

with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)

with col3:
    avg_monetary = format_currency(rfm_df.monetary.mean(), "BRL", locale='pt_BR') 
    st.metric("Average Monetary", value=avg_monetary)

fig1 = px.bar(rfm_df.sort_values(by="recency", ascending=True).head(5), y="recency", x="customer_id", title="By Recency (days)")
fig2 = px.bar(rfm_df.sort_values(by="frequency", ascending=False).head(5), y="frequency", x="customer_id", title="By Frequency")
fig3 = px.bar(rfm_df.sort_values(by="monetary", ascending=False).head(5), y="monetary", x="customer_id", title="By Monetary")

st.plotly_chart(fig1)
st.plotly_chart(fig2)
st.plotly_chart(fig3)

st.caption('Copyright ©Azmi Irfala')