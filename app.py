# convert date & time
df['order_date'] = pd.to_datetime(df['order_date'])
df['order_time'] = pd.to_datetime(df['order_time']).dt.time

# create revenue column
df['revenue'] = df['quantity'] * df['price']