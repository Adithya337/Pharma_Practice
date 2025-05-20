import pandas as pd
import numpy as np
import random
from faker import Faker
import os

# Initialize
fake = Faker()
Faker.seed(789)
random.seed(789)
np.random.seed(789)

# Load existing region IDs
region_df = pd.read_csv("pharma_dataset/region_lookup.csv")
region_ids = region_df["region_id"].tolist()

# Parameters
records_per_region = 5000
total_pharmacies = 150
total_drugs = 200

# Output path
output_dir = "pharma_dataset/sales_by_region"
os.makedirs(output_dir, exist_ok=True)

# Certification flag
promo_flags = [True, False]

# Function to create data for one region
def generate_sales_data(region_id):
    sales_data = []
    for i in range(records_per_region):
        pharmacy_id = random.randint(1, total_pharmacies)
        drug_id = random.randint(1, total_drugs)
        quantity = random.randint(1, 20)
        sale_date = fake.date_between(start_date='-2y', end_date='today')
        amount = round(random.uniform(5.0, 500.0), 2)
        promo_flag = random.choice(promo_flags)

        sales_data.append([
            f"T_{region_id}_{i+1}",
            pharmacy_id,
            drug_id,
            quantity,
            sale_date,
            amount,
            promo_flag
        ])

    df = pd.DataFrame(sales_data, columns=[
        "transaction_id", "pharmacy_id", "drug_id",
        "quantity_sold", "sale_date", "total_amount", "promotion_applied_flag"
    ])

    # Inject ~2% nulls in random columns
    for col in ['quantity_sold', 'total_amount']:
        null_indices = df.sample(frac=0.02).index
        df.loc[null_indices, col] = None

    # Inject ~1% corrupted rows (missing drug_id or total_amount)
    corrupt_indices = df.sample(frac=0.01).index
    for idx in corrupt_indices:
        if random.random() < 0.5:
            df.at[idx, 'drug_id'] = np.nan
        else:
            df.at[idx, 'total_amount'] = np.nan

    # Save file
    df.to_csv(f"{output_dir}/sales_region_{region_id}.csv", index=False)
    print(f"✅ sales_region_{region_id}.csv generated with {len(df)} records")

# Generate CSV for each region
for rid in region_ids:
    generate_sales_data(rid)
