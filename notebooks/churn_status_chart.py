import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

input_file = BASE_DIR / "reports" / "churn_analysis.csv"
output_file = BASE_DIR / "reports" / "churn_status_chart.png"

df = pd.read_csv(input_file)

status_counts = df["churn_status"].value_counts()

plt.figure(figsize=(9, 6))
status_counts.plot(kind="bar")

plt.title("E-Commerce Customer Activity Status")
plt.xlabel("Customer Status")
plt.ylabel("Number of Customers")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()

plt.savefig(output_file, dpi=300)
plt.show()

print("Churn status chart saved to:", output_file)
print("\nCustomer status counts:")
print(status_counts)