import pandas as pd
import numpy as np
from faker import Faker
import random
import os

# Initialize
fake = Faker()
Faker.seed(456)
random.seed(456)
np.random.seed(456)

# Parameters
num_manufacturers = 70
cert_statuses = ['Certified', 'Pending', 'Revoked']

# Generate base data
manufacturer_df = pd.DataFrame({
    "manufacturer_id": range(1, num_manufacturers + 1),
    "manufacturer_name": [fake.company() for _ in range(num_manufacturers)],
    "country": [fake.country() for _ in range(num_manufacturers)],
    "founded_year": np.random.randint(1950, 2021, size=num_manufacturers),
    "certification_status": np.random.choice(cert_statuses, size=num_manufacturers)
})

# Introduce a few duplicate rows (e.g., 5)
duplicates = manufacturer_df.sample(5)
manufacturer_df = pd.concat([manufacturer_df, duplicates], ignore_index=True)

# Save to CSV (optional)
output_dir = "pharma_dataset"
os.makedirs(output_dir, exist_ok=True)
manufacturer_df.to_csv(f"{output_dir}/manufacturer.csv", index=False)

print("Manufacturer Table generated with duplicates.")
