import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

customers = pd.read_csv(DATA_DIR / "customers.csv")
orders = pd.read_csv(DATA_DIR / "orders.csv")
products = pd.read_csv(DATA_DIR / "products.csv")

orders["order_date"] = pd.to_datetime(orders["order_date"])

delivered = orders[orders["status"] == "Delivered"].copy()

print("\n===== E-COMMERCE CUSTOMER ANALYSIS =====")
print(f"Total customers: {len(customers)}")
print(f"Total orders: {len(orders)}")
print(f"Delivered orders: {len(delivered)}")
print(f"Customers without orders: {len(set(customers['customer_id']) - set(orders['customer_id']))}")

print("\n===== MONTHLY DELIVERED REVENUE =====")
monthly_revenue = (
    delivered.groupby(delivered["order_date"].dt.to_period("M"))["order_amount"]
    .sum()
    .round(2)
)
print(monthly_revenue)

print("\n===== REVENUE BY CATEGORY =====")
category_revenue = delivered.merge(
    products[["product_id", "category"]],
    on="product_id",
    how="left"
).groupby("category")["order_amount"].sum().sort_values(ascending=False).round(2)

print(category_revenue)

print("\n===== REVENUE BY REGION =====")
region_revenue = delivered.merge(
    customers[["customer_id", "region"]],
    on="customer_id",
    how="left"
).groupby("region")["order_amount"].sum().sort_values(ascending=False).round(2)

print(region_revenue)

REPORTS_DIR.mkdir(exist_ok=True)

report_path = REPORTS_DIR / "customer_analysis.txt"

with report_path.open("w", encoding="utf-8") as file:
    file.write("E-COMMERCE CUSTOMER ANALYSIS\n\n")
    file.write(f"Total customers: {len(customers)}\n")
    file.write(f"Total orders: {len(orders)}\n")
    file.write(f"Delivered orders: {len(delivered)}\n\n")
    file.write("MONTHLY DELIVERED REVENUE\n")
    file.write(monthly_revenue.to_string())
    file.write("\n\nREVENUE BY CATEGORY\n")
    file.write(category_revenue.to_string())
    file.write("\n\nREVENUE BY REGION\n")
    file.write(region_revenue.to_string())

print(f"\nAnalysis report saved to: {report_path}")