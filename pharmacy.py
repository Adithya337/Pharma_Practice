import pandas as pd
import numpy as np
from faker import Faker
import random
import os

# Initialize
fake = Faker()
Faker.seed(123)
np.random.seed(123)
random.seed(123)

# Parameters
num_pharmacies = 150
region_ids = list(range(1, 12))  # 11 regions

# Generate base pharmacy data
pharmacy_df = pd.DataFrame({
    "pharmacy_id": range(1, num_pharmacies + 1),
    "pharmacy_name": [f"Pharma_{i}" for i in range(1, num_pharmacies + 1)],
    "region_id": np.random.choice(region_ids, size=num_pharmacies),
    "open_date": [fake.date_between(start_date='-10y', end_date='-1y') for _ in range(num_pharmacies)],
    "total_employees": np.random.randint(5, 100, size=num_pharmacies)
})

# Introduce null values (~5%) in open_date and total_employees
for col in ['open_date', 'total_employees']:
    null_indices = pharmacy_df.sample(frac=0.05).index
    pharmacy_df.loc[null_indices, col] = None

# Add a few completely duplicate rows
duplicates = pharmacy_df.sample(5)
pharmacy_df = pd.concat([pharmacy_df, duplicates], ignore_index=True)

# Save to CSV (optional)
output_dir = "pharma_dataset"
os.makedirs(output_dir, exist_ok=True)
pharmacy_df.to_csv(f"{output_dir}/pharmacy_branch.csv", index=False)

print("Pharmacy Branch Table generated with nulls and duplicates.")
