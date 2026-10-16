import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

customers = pd.read_csv(BASE_DIR / "data" / "customers.csv")
orders = pd.read_csv(BASE_DIR / "data" / "orders.csv")

orders["order_date"] = pd.to_datetime(orders["order_date"])

# Use delivered orders for RFM analysis
delivered = orders[orders["status"] == "Delivered"].copy()

# Set the analysis date to one day after the latest order date
snapshot_date = orders["order_date"].max() + pd.Timedelta(days=1)

# Calculate Recency, Frequency, and Monetary value
rfm = delivered.groupby("customer_id").agg(
    Recency=("order_date", lambda dates: (snapshot_date - dates.max()).days),
    Frequency=("order_id", "nunique"),
    Monetary=("order_amount", "sum")
).reset_index()

# Assign scores from 1 to 5
rfm["R_Score"] = np.ceil(
    rfm["Recency"].rank(pct=True, ascending=False) * 5
).clip(1, 5).astype(int)

rfm["F_Score"] = np.ceil(
    rfm["Frequency"].rank(pct=True) * 5
).clip(1, 5).astype(int)

rfm["M_Score"] = np.ceil(
    rfm["Monetary"].rank(pct=True) * 5
).clip(1, 5).astype(int)

# Create customer segments
def assign_segment(row):
    if row["R_Score"] >= 4 and row["F_Score"] >= 4 and row["M_Score"] >= 4:
        return "Champions"
    elif row["F_Score"] >= 4 and row["M_Score"] >= 3:
        return "Loyal Customers"
    elif row["R_Score"] >= 4 and row["F_Score"] >= 2:
        return "Potential Loyalists"
    elif row["R_Score"] <= 2 and row["F_Score"] >= 3:
        return "At Risk"
    else:
        return "Others"

rfm["Segment"] = rfm.apply(assign_segment, axis=1)

# Add customer details
rfm = rfm.merge(customers, on="customer_id", how="left")

# Save results
output_file = BASE_DIR / "reports" / "rfm_customer_segments.csv"
rfm.to_csv(output_file, index=False)

print("RFM analysis completed successfully!")
print("Customers analysed:", len(rfm))
print("\nCustomer segment counts:")
print(rfm["Segment"].value_counts())
print("\nTop 10 customers by monetary value:")
print(
    rfm.sort_values("Monetary", ascending=False)[
        ["customer_id", "name", "region", "Recency",
         "Frequency", "Monetary", "Segment"]
    ].head(10).to_string(index=False)
)
print("\nResults saved to:", output_file)