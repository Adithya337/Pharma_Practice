import pandas as pd
import numpy as np
from faker import Faker
import random
import os

# Initialize
fake = Faker('en_US')
Faker.seed(321)
random.seed(321)

# Parameters
num_regions = 12
zones = ['East', 'West', 'North', 'South', 'Central']
urban_rural = ['Urban', 'Rural']

# Generate region table
region_df = pd.DataFrame({
    "region_id": list(range(1, num_regions + 1)),
    "region_name": [f"Region_{i}" for i in range(1, num_regions + 1)],
    "state": random.sample([fake.state() for _ in range(30)], k=num_regions),  # Unique states
    "zone": random.choices(zones, k=num_regions),
    "urban_rural_flag": random.choices(urban_rural, k=num_regions)
})

# Save to CSV (optional)
output_dir = "pharma_dataset"
os.makedirs(output_dir, exist_ok=True)
region_df.to_csv(f"{output_dir}/region_lookup.csv", index=False)

print("Region Lookup Table generated with 12 U.S. regions.")
