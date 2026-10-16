import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

BASE_DIR = Path(__file__).resolve().parent.parent

customers = pd.read_csv(BASE_DIR / "data" / "customers.csv")
orders = pd.read_csv(BASE_DIR / "data" / "orders.csv")

delivered_customers = set(
    orders.loc[orders["status"] == "Delivered", "customer_id"]
)
customers["purchased"] = customers["customer_id"].isin(
    delivered_customers
).astype(int)

X = customers[["age", "region"]]
y = customers["purchased"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

def make_pipeline(classifier):
    preprocessor = ColumnTransformer([
        ("region", OneHotEncoder(handle_unknown="ignore"), ["region"]),
        ("age", "passthrough", ["age"])
    ])
    return Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", classifier)
    ])

models = {
    "Logistic Regression": LogisticRegression(
        class_weight="balanced", max_iter=1000, random_state=42
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=100, class_weight="balanced", random_state=42
    )
}

results = []

for name, classifier in models.items():
    model = make_pipeline(classifier)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    results.append({
        "Model": name,
        "Accuracy": accuracy_score(y_test, predictions),
        "Precision": precision_score(y_test, predictions, zero_division=0),
        "Recall": recall_score(y_test, predictions, zero_division=0),
        "F1 Score": f1_score(y_test, predictions, zero_division=0)
    })

results_df = pd.DataFrame(results)

output_file = BASE_DIR / "reports" / "model_comparison.csv"
results_df.to_csv(output_file, index=False)

print("Model Performance Comparison")
print("----------------------------")
print(results_df.to_string(index=False))
print("\nComparison saved to:", output_file)