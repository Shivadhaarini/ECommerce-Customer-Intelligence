import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

orders = pd.read_csv(DATA_DIR / "orders.csv")
products = pd.read_csv(DATA_DIR / "products.csv")

delivered = orders[orders["status"] == "Delivered"]

category_data = delivered.merge(
    products[["product_id", "category"]],
    on="product_id",
    how="left"
)

category_revenue = (
    category_data.groupby("category")["order_amount"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))
category_revenue.plot(kind="bar")

plt.title("Delivered Revenue by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Revenue")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()

REPORTS_DIR.mkdir(exist_ok=True)
chart_path = REPORTS_DIR / "category_revenue.png"

plt.savefig(chart_path, dpi=300)
plt.show()

print(f"Chart saved to: {chart_path}")