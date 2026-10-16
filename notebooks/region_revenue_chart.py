import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

orders = pd.read_csv(DATA_DIR / "orders.csv")
customers = pd.read_csv(DATA_DIR / "customers.csv")

delivered = orders[orders["status"] == "Delivered"]

region_data = delivered.merge(
    customers[["customer_id", "region"]],
    on="customer_id",
    how="left"
)

region_revenue = (
    region_data.groupby("region")["order_amount"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(9, 6))
region_revenue.plot(kind="bar")

plt.title("Delivered Revenue by Region")
plt.xlabel("Region")
plt.ylabel("Revenue")
plt.xticks(rotation=0)
plt.tight_layout()

REPORTS_DIR.mkdir(exist_ok=True)
chart_path = REPORTS_DIR / "region_revenue.png"

plt.savefig(chart_path, dpi=300)
plt.show()

print(f"Chart saved to: {chart_path}")