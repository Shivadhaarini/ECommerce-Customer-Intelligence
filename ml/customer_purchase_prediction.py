import joblib
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

BASE_DIR = Path(__file__).resolve().parent.parent

customers = pd.read_csv(BASE_DIR / "data" / "customers.csv")
orders = pd.read_csv(BASE_DIR / "data" / "orders.csv")

# Create a target: whether a customer placed any delivered order
delivered_customers = set(
    orders.loc[orders["status"] == "Delivered", "customer_id"]
)

customers["purchased"] = customers["customer_id"].isin(
    delivered_customers
).astype(int)

# Use only customer information as model inputs
X = customers[["age", "region"]]
y = customers["purchased"]

preprocessor = ColumnTransformer(
    transformers=[
        ("region", OneHotEncoder(handle_unknown="ignore"), ["region"]),
        ("age", "passthrough", ["age"])
    ]
)

model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    ))
])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model.fit(X_train, y_train)
joblib.dump(model, BASE_DIR / "ml" / "customer_purchase_model.pkl")
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)


report_dir = BASE_DIR / "reports"
report_dir.mkdir(exist_ok=True)

report_text = classification_report(
    y_test,
    predictions,
    labels=[0, 1],
    target_names=["No Delivered Purchase", "Delivered Purchase"],
    zero_division=0
)

report_file = report_dir / "purchase_prediction_report.txt"

with open(report_file, "w", encoding="utf-8") as file:
    file.write("Customer Purchase Prediction Model\n")
    file.write("----------------------------------\n")
    file.write(f"Training customers: {len(X_train)}\n")
    file.write(f"Testing customers: {len(X_test)}\n")
    file.write(f"Accuracy: {accuracy:.2%}\n\n")
    file.write("Classification Report:\n")
    file.write(report_text)

print("Evaluation report saved to:", report_file)
print("\nAccuracy:", f"{accuracy:.2%}")
print(report_text)
