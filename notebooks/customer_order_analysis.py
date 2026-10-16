import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

customers = pd.read_csv(DATA_DIR / "customers.csv")
orders = pd.read_csv(DATA_DIR / "orders.csv")

customer_orders = (
    orders.groupby("customer_id")
    .agg(
        total_orders=("order_id", "count"),
        total_order_value=("order_amount", "sum")
    )
    .reset_index()
)

customer_analysis = customers.merge(
    customer_orders,
    on="customer_id",
    how="left"
)

customer_analysis["total_orders"] = (
    customer_analysis["total_orders"].fillna(0).astype(int)
)
customer_analysis["total_order_value"] = (
    customer_analysis["total_order_value"].fillna(0).round(2)
)

print("\n===== CUSTOMER ORDER ANALYSIS =====")
print(f"Total customers: {len(customer_analysis)}")
print(f"Customers who ordered: {(customer_analysis['total_orders'] > 0).sum()}")
print(f"Customers with no orders: {(customer_analysis['total_orders'] == 0).sum()}")

print("\n===== TOP 10 CUSTOMERS BY ORDER COUNT =====")
print(
    customer_analysis.sort_values(
        "total_orders", ascending=False
    )[["customer_id", "region", "total_orders", "total_order_value"]]
    .head(10).to_string(index=False)
)

print("\n===== CUSTOMER ORDER FREQUENCY =====")
print(customer_analysis["total_orders"].value_counts().sort_index().to_string())

REPORTS_DIR.mkdir(exist_ok=True)
output_path = REPORTS_DIR / "customer_order_analysis.csv"

customer_analysis.to_csv(output_path, index=False)

print(f"\nCustomer analysis saved to: {output_path}")