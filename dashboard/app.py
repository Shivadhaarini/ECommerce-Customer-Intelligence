
import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "ecommerce.db"
REPORTS_DIR = BASE_DIR / "reports"

st.set_page_config(
    page_title="E-Commerce Customer Intelligence",
    page_icon="📊",
    layout="wide"
)

st.title("📊 E-Commerce Customer Intelligence Dashboard")
st.caption("Sales, customers, and machine-learning insights")

@st.cache_data
def load_data():
    with sqlite3.connect(DB_PATH) as conn:
        customers = pd.read_sql_query("SELECT * FROM customers", conn)
        orders = pd.read_sql_query("SELECT * FROM orders", conn)
        products = pd.read_sql_query("SELECT * FROM products", conn)
    return customers, orders, products

customers, orders, products = load_data()

orders["order_date"] = pd.to_datetime(orders["order_date"])
delivered = orders[orders["status"] == "Delivered"].copy()

total_customers = customers["customer_id"].nunique()
total_orders = orders["order_id"].nunique()
delivered_revenue = delivered["order_amount"].sum()
average_order_value = delivered["order_amount"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Delivered Revenue", f"{delivered_revenue:,.2f}")
col4.metric("Average Delivered Order", f"{average_order_value:,.2f}")

st.divider()

st.subheader("📈 Monthly Delivered Revenue")

monthly_revenue = (
    delivered.groupby(delivered["order_date"].dt.to_period("M"))["order_amount"]
    .sum()
    .reset_index()
)

monthly_revenue["Month"] = monthly_revenue["order_date"].astype(str)

st.line_chart(
    monthly_revenue.set_index("Month")["order_amount"],
    y_label="Revenue"
)

left, right = st.columns(2)

with left:
    st.subheader("🛍️ Revenue by Product Category")
    category_revenue = (
        delivered.merge(products[["product_id", "category"]], on="product_id")
        .groupby("category")["order_amount"]
        .sum()
        .sort_values(ascending=False)
    )
    st.bar_chart(category_revenue, y_label="Revenue")

with right:
    st.subheader("🌍 Revenue by Region")
    customer_regions = customers[["customer_id", "region"]]
    region_revenue = (
        delivered.merge(customer_regions, on="customer_id")
        .groupby("region")["order_amount"]
        .sum()
        .sort_values(ascending=False)
    )
    st.bar_chart(region_revenue, y_label="Revenue")

st.divider()

st.subheader("📦 Order Status")
status_counts = orders["status"].value_counts()
st.bar_chart(status_counts, y_label="Number of Orders")

st.subheader("🔎 Explore Orders")
selected_status = st.selectbox(
    "Filter orders by status",
    ["All"] + sorted(orders["status"].unique().tolist())
)

if selected_status == "All":
    filtered_orders = orders
else:
    filtered_orders = orders[orders["status"] == selected_status]

st.dataframe(filtered_orders, use_container_width=True)

st.divider()

st.subheader("🤖 Machine Learning Reports")

report_files = {
    "RFM Customer Segments": "rfm_customer_segments.csv",
    "Customer Activity Analysis": "churn_analysis.csv",
    "Model Comparison": "model_comparison.csv"
}

for report_name, filename in report_files.items():
    report_path = REPORTS_DIR / filename
    if report_path.exists():
        st.markdown(f"**{report_name}**")
        report_df = pd.read_csv(report_path)
        st.dataframe(report_df.head(20), use_container_width=True)
    else:
        st.info(f"{report_name} report is not available yet.")

st.caption("Built with Python, Pandas, SQLite, Scikit-learn, and Streamlit")
