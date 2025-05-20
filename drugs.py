import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime
import os

# Initialize
fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

# Parameters
num_records = 200
manufacturer_ids = list(range(1, 71))
drug_types = ['Tablet', 'Capsule', 'Syrup', 'Injection', 'Cream']

# Generate unique drug names, then create duplicates
base_names = [f"Drug_{i}" for i in range(150)]  # 150 unique
extra_names = random.choices(base_names, k=50)  # 50 duplicates
drug_names = base_names + extra_names
random.shuffle(drug_names)

# Create initial DataFrame
drug_df = pd.DataFrame({
    "drug_id": range(1, num_records + 1),
    "drug_name": drug_names[:num_records],
    "drug_type": random.choices(drug_types, k=num_records),
    "manufacturer_id": np.random.choice(manufacturer_ids, size=num_records),
    "approval_date": [fake.date_between(start_date='-5y', end_date='today') for _ in range(num_records)],
    "price": np.round(np.random.uniform(5, 500, size=num_records), 2),
    "prescription_required": np.random.choice([True, False], size=num_records)
})

# Introduce null values in 5% of records for some columns
for col in ['drug_type', 'approval_date', 'price']:
    null_indices = drug_df.sample(frac=0.05).index
    drug_df.loc[null_indices, col] = None

# Add a few completely duplicate rows (realistic dirty data)
duplicates = drug_df.sample(5)
drug_df = pd.concat([drug_df, duplicates], ignore_index=True)

# Save to CSV (optional)
output_dir = "pharma_dataset"
os.makedirs(output_dir, exist_ok=True)
drug_df.to_csv(f"{output_dir}/drug_master.csv", index=False)

print("Drug Master Table generated with 200+ rows (including nulls and duplicates).")
