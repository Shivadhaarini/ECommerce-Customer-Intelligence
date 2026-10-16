import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

file_path = BASE_DIR / "reports" / "rfm_customer_segments.csv"
output_path = BASE_DIR / "reports" / "rfm_segment_chart.png"

df = pd.read_csv(file_path)

segment_counts = df["Segment"].value_counts().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
segment_counts.plot(kind="bar")

plt.title("E-Commerce Customer Segmentation (RFM Analysis)")
plt.xlabel("Customer Segment")
plt.ylabel("Number of Customers")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()

plt.savefig(output_path, dpi=300)
plt.show()

print("Customer segmentation chart saved to:", output_path)
print("\nSegment counts:")
print(segment_counts)