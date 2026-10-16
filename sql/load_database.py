
import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = BASE_DIR / "data" / "ecommerce.db"

customers = pd.read_csv(DATA_DIR / "customers.csv")
orders = pd.read_csv(DATA_DIR / "orders.csv")
products = pd.read_csv(DATA_DIR / "products.csv")

customers["signup_date"] = pd.to_datetime(
    customers["signup_date"]
).dt.strftime("%Y-%m-%d")

orders["order_date"] = pd.to_datetime(
    orders["order_date"]
).dt.strftime("%Y-%m-%d")

with sqlite3.connect(DB_PATH) as connection:
    customers.to_sql(
        "customers", connection, if_exists="replace", index=False
    )
    orders.to_sql(
        "orders", connection, if_exists="replace", index=False
    )
    products.to_sql(
        "products", connection, if_exists="replace", index=False
    )

print("Database created successfully!")
print(f"Database location: {DB_PATH}")
print(f"Customers loaded: {len(customers)}")
print(f"Orders loaded: {len(orders)}")
print(f"Products loaded: {len(products)}")
