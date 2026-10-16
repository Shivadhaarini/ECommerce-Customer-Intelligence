import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

input_file = BASE_DIR / "reports" / "model_comparison.csv"
output_file = BASE_DIR / "reports" / "model_comparison_chart.png"

df = pd.read_csv(input_file)

metrics = ["Accuracy", "Precision", "Recall", "F1 Score"]
df = df.set_index("Model")

ax = df[metrics].plot(kind="bar", figsize=(10, 6))

plt.title("Machine Learning Model Performance Comparison")
plt.xlabel("Model")
plt.ylabel("Score")
plt.ylim(0, 1)
plt.xticks(rotation=0)
plt.legend(title="Metrics")
plt.tight_layout()

plt.savefig(output_file, dpi=300)
plt.show()

print("Model comparison chart saved to:", output_file)