import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Pizza Sales Dashboard", layout="wide")

st.title("🍕 Pizza Sales Interactive Dashboard")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data/pizza_sales.csv")

df['order_date'] = pd.to_datetime(df['order_date'], format='%d-%m-%Y')
df['order_time'] = pd.to_datetime(df['order_time'])
df['hour'] = df['order_time'].dt.hour
df['day'] = df['order_date'].dt.day_name()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🔍 Filters")

category = st.sidebar.multiselect(
    "Select Category",
    options=df['pizza_category'].unique(),
    default=df['pizza_category'].unique()
)

size = st.sidebar.multiselect(
    "Select Size",
    options=df['pizza_size'].unique(),
    default=df['pizza_size'].unique()
)

# Filter data
filtered_df = df[
    (df['pizza_category'].isin(category)) &
    (df['pizza_size'].isin(size))
]

# ---------------- KPIs ----------------
total_revenue = filtered_df['total_price'].sum()
total_orders = filtered_df['order_id'].nunique()
total_quantity = filtered_df['quantity'].sum()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Revenue", f"${total_revenue:,.2f}")
col2.metric("📦 Orders", total_orders)
col3.metric("🍕 Quantity", total_quantity)

st.markdown("---")

# ---------------- TOP PIZZAS ----------------
st.subheader("🔝 Top 10 Pizzas")

top_pizzas = filtered_df.groupby('pizza_name')['quantity'].sum().nlargest(10)

fig1 = px.bar(
    x=top_pizzas.values,
    y=top_pizzas.index,
    orientation='h',
    labels={'x': 'Quantity', 'y': 'Pizza'},
    title="Top Selling Pizzas"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- SALES OVER TIME ----------------
st.subheader("📅 Sales Over Time")

daily_sales = filtered_df.groupby('order_date')['total_price'].sum().reset_index()

fig2 = px.line(
    daily_sales,
    x='order_date',
    y='total_price',
    title="Daily Revenue Trend"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- HOURLY SALES ----------------
st.subheader("⏰ Sales by Hour")

hourly_sales = filtered_df.groupby('hour')['quantity'].sum().reset_index()

fig3 = px.line(
    hourly_sales,
    x='hour',
    y='quantity',
    markers=True,
    title="Peak Hours"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- CATEGORY ----------------
st.subheader("🍕 Category Distribution")

category_sales = filtered_df.groupby('pizza_category')['total_price'].sum().reset_index()

fig4 = px.pie(
    category_sales,
    names='pizza_category',
    values='total_price',
    title="Revenue by Category"
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------- SIZE ----------------
st.subheader("📏 Size Distribution")

size_sales = filtered_df.groupby('pizza_size')['total_price'].sum().reset_index()

fig5 = px.bar(
    size_sales,
    x='pizza_size',
    y='total_price',
    title="Revenue by Size"
)

st.plotly_chart(fig5, use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.write("🚀 Built by Tarun SR | Interactive Data Dashboard")