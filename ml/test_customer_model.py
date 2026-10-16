import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

model_path = BASE_DIR / "ml" / "customer_purchase_model.pkl"

model = joblib.load(model_path)

# Test with sample customer details
sample_customers = pd.DataFrame({
    "age": [22, 35, 45, 28],
    "region": ["South", "North", "East", "West"]
})

predictions = model.predict(sample_customers)

print("Saved Model Testing")
print("-------------------")

for i, prediction in enumerate(predictions):
    result = (
        "Delivered Purchase"
        if prediction == 1
        else "No Delivered Purchase"
    )
    print(
        f"Customer {i + 1}: "
        f"Age={sample_customers.iloc[i]['age']}, "
        f"Region={sample_customers.iloc[i]['region']}, "
        f"Prediction={result}"
    )