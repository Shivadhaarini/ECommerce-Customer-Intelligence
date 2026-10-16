import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

customers = pd.read_csv(BASE_DIR / "data" / "customers.csv")
orders = pd.read_csv(BASE_DIR / "data" / "orders.csv")

orders["order_date"] = pd.to_datetime(orders["order_date"])

# Use delivered orders to identify customer activity
delivered = orders[orders["status"] == "Delivered"].copy()

snapshot_date = orders["order_date"].max() + pd.Timedelta(days=1)

last_order = delivered.groupby("customer_id")["order_date"].max()

analysis = customers[["customer_id", "name", "region"]].copy()
analysis["last_delivered_order"] = analysis["customer_id"].map(last_order)

analysis["days_since_last_order"] = (
    snapshot_date - analysis["last_delivered_order"]
).dt.days

# Customers without a delivered order are flagged separately
analysis["churn_status"] = analysis["days_since_last_order"].apply(
    lambda days: (
        "No Delivered Orders"
        if pd.isna(days)
        else "At Risk"
        if days >= 60
        else "Active"
    )
)

output_file = BASE_DIR / "reports" / "churn_analysis.csv"
analysis.to_csv(output_file, index=False)

print("Customer activity analysis completed!")
print("\nCustomer status counts:")
print(analysis["churn_status"].value_counts())

print("\nSample results:")
print(analysis.head(10).to_string(index=False))

print("\nResults saved to:", output_file)