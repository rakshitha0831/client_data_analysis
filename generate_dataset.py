import pandas as pd
import numpy as np
import random

# Reproducibility
np.random.seed(42)

# Define parameters
num_clients = 300
regions = ["UK", "Germany", "France", "Spain", "Italy", "Netherlands"]
industries = ["Retail", "Tech", "Finance", "Healthcare", "Education", "Manufacturing"]

# Generate synthetic data
data = {
    "client_id": range(1001, 1001 + num_clients),
    "region": [random.choice(regions) for _ in range(num_clients)],
    "industry": [random.choice(industries) for _ in range(num_clients)],
    "sessions": np.random.randint(10, 200, num_clients),
    "avg_session_time": np.round(np.random.uniform(1.0, 8.0, num_clients), 2),
    "conversion_rate": np.round(np.random.uniform(0.05, 0.9, num_clients), 2),
    "revenue": np.round(np.random.uniform(5000, 80000, num_clients), 2),
    "customer_tenure_months": np.random.randint(1, 60, num_clients),
    "support_tickets": np.random.randint(0, 15, num_clients),
    "satisfaction_score": np.random.randint(1, 10, num_clients),
    "marketing_spend": np.round(np.random.uniform(500, 10000, num_clients), 2),
    "product_adoption_rate": np.round(np.random.uniform(0.2, 1.0, num_clients), 2)
}

# Derived metric: engagement score
data["engagement_score"] = np.round(
    (0.4 * (data["sessions"] / np.max(data["sessions"])) +
     0.3 * data["conversion_rate"] +
     0.3 * data["avg_session_time"] / np.max(data["avg_session_time"])), 2
)

# Churn logic: higher for low engagement, satisfaction, or high tickets
data["churn"] = [
    1 if (e < 0.35 or s < 5 or t > 10) else 0
    for e, s, t in zip(data["engagement_score"], data["satisfaction_score"], data["support_tickets"])
]

df = pd.DataFrame(data)

# Save dataset
df.to_csv("client_data.csv", index=False)

print("✅ Dataset created successfully: client_data.csv")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
print(df.head())
