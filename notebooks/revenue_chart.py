import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

orders = pd.read_csv(DATA_DIR / "orders.csv")
orders["order_date"] = pd.to_datetime(orders["order_date"])

delivered = orders[orders["status"] == "Delivered"].copy()

monthly_revenue = (
    delivered.groupby(delivered["order_date"].dt.to_period("M"))["order_amount"]
    .sum()
)

monthly_revenue.index = monthly_revenue.index.astype(str)

plt.figure(figsize=(10, 6))
monthly_revenue.plot(kind="bar")

plt.title("Monthly Delivered Revenue - 2026")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()

REPORTS_DIR.mkdir(exist_ok=True)
chart_path = REPORTS_DIR / "monthly_revenue.png"

plt.savefig(chart_path, dpi=300)
plt.show()

print(f"Chart saved to: {chart_path}")