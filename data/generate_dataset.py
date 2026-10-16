import csv
import random
from datetime import date, timedelta

random.seed(42)

NUM_CUSTOMERS = 1000
NUM_ORDERS = 5000
NUM_PRODUCTS = 50

regions = ["North", "South", "East", "West"]
categories = [
    "Electronics",
    "Fashion",
    "Home & Kitchen",
    "Beauty",
    "Sports"
]

customers = []

for i in range(1, NUM_CUSTOMERS + 1):
    customers.append({
        "customer_id": f"C{i:04d}",
        "name": f"Customer {i}",
        "age": random.randint(18, 60),
        "region": random.choice(regions),
        "signup_date": (
            date(2025, 1, 1)
            + timedelta(days=random.randint(0, 365))
        ).isoformat()
    })

products = []

for i in range(1, NUM_PRODUCTS + 1):
    products.append({
        "product_id": f"P{i:03d}",
        "product_name": f"Product {i}",
        "category": random.choice(categories),
        "unit_price": round(random.uniform(200, 5000), 2)
    })

orders = []

start_date = date(2026, 1, 1)

for i in range(1, NUM_ORDERS + 1):
    customer = random.choice(customers)
    product = random.choice(products)

    order_date = start_date + timedelta(
        days=random.randint(0, 272)
    )

    quantity = random.randint(1, 4)

    orders.append({
        "order_id": f"O{i:05d}",
        "customer_id": customer["customer_id"],
        "product_id": product["product_id"],
        "order_date": order_date.isoformat(),
        "quantity": quantity,
        "unit_price": product["unit_price"],
        "order_amount": round(quantity * product["unit_price"], 2),
        "status": random.choices(
            ["Delivered", "Cancelled", "Returned"],
            weights=[85, 10, 5]
        )[0]
    })


def write_csv(filename, rows):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


write_csv("customers.csv", customers)
write_csv("products.csv", products)
write_csv("orders.csv", orders)

print(f"Created {len(customers)} customers.")
print(f"Created {len(products)} products.")
print(f"Created {len(orders)} orders.")