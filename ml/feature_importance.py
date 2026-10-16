import pandas as pd
import matplotlib.pyplot as plt
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

model_path = BASE_DIR / "ml" / "customer_purchase_model.pkl"
output_path = BASE_DIR / "reports" / "feature_importance.png"

model = joblib.load(model_path)

preprocessor = model.named_steps["preprocessor"]
classifier = model.named_steps["classifier"]

feature_names = preprocessor.get_feature_names_out()
importance_values = classifier.feature_importances_

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importance_values
}).sort_values("Importance", ascending=False)

print("Feature Importance")
print("------------------")
print(importance_df.to_string(index=False))

plt.figure(figsize=(9, 6))
plt.barh(
    importance_df["Feature"],
    importance_df["Importance"]
)
plt.title("Customer Purchase Model - Feature Importance")
plt.xlabel("Importance Score")
plt.ylabel("Feature")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(output_path, dpi=300)
plt.show()

print("\nChart saved to:", output_path)