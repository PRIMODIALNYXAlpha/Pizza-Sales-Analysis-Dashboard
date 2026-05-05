import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("data/pizza_sales.csv")

# Fix date & time format
df['order_date'] = pd.to_datetime(df['order_date'], format='%d-%m-%Y')
df['order_time'] = pd.to_datetime(df['order_time'])

# ---------------- KPI ----------------
print("\n--- KPI ---")
print("Total Revenue:", df['total_price'].sum())
print("Total Orders:", df['order_id'].nunique())
print("Total Pizzas Sold:", df['quantity'].sum())

# ---------------- Top Pizzas ----------------
top_pizzas = df.groupby('pizza_name')['quantity'].sum() \
               .sort_values(ascending=False).head(10)

print("\nTop 10 Pizzas:\n", top_pizzas)

# ---------------- Sales by Day ----------------
df['day'] = df['order_date'].dt.day_name()

sales_day = df.groupby('day')['total_price'].sum() \
              .sort_values(ascending=False)

print("\nSales by Day:\n", sales_day)

# ---------------- Peak Hours ----------------
df['hour'] = df['order_time'].dt.hour

hourly_sales = df.groupby('hour')['quantity'].sum()

print("\nSales by Hour:\n", hourly_sales)

# ---------------- Category Analysis ----------------
category_sales = df.groupby('pizza_category')['total_price'].sum() \
                  .sort_values(ascending=False)

print("\nSales by Category:\n", category_sales)

# ---------------- Size Analysis ----------------
size_sales = df.groupby('pizza_size')['total_price'].sum() \
               .sort_values(ascending=False)

print("\nSales by Size:\n", size_sales)

# ---------------- Visualizations ----------------

# Top pizzas
sns.barplot(x=top_pizzas.values, y=top_pizzas.index)
plt.title("Top 10 Pizzas")
plt.show()

# Category sales
sns.barplot(x=category_sales.values, y=category_sales.index)
plt.title("Sales by Category")
plt.show()

# Hourly sales
hourly_sales.plot(kind='line')
plt.title("Sales by Hour")
plt.show()