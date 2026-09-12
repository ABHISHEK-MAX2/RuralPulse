import pandas as pd
import json

input_file = "list-of-states-districts-sub-districts-and-villages-along-with-their-lgd-codes-as-of-2-july-2026.csv"
output_file = "karnataka_lgd_codes.csv"

print(f"Loading full dataset from {input_file}...")
df = pd.read_csv(input_file, low_memory=False)

total_rows = len(df)
total_states = df['state_name'].nunique()
total_districts = df['district_code'].nunique()
total_subdistricts = df['sub-district_code'].nunique()
total_villages = df['village_code'].nunique()

print("\n================ FULL DATASET SUMMARY ================")
print(f"Total Records (Villages): {total_rows:,}")
print(f"Total States & Union Territories: {total_states}")
print(f"Total Unique Districts: {total_districts:,}")
print(f"Total Unique Sub-Districts: {total_subdistricts:,}")
print(f"Total Unique Villages (Codes): {total_villages:,}")
print("Columns:", list(df.columns))

# Filter for Karnataka
kar_mask = df['state_name'].astype(str).str.strip().str.upper() == 'KARNATAKA'
kar_df = df[kar_mask].copy()

# Save Karnataka dataset
kar_df.to_csv(output_file, index=False)
print(f"\nSaved Karnataka dataset to '{output_file}' with {len(kar_df):,} rows.")

# Karnataka Statistics
state_code = kar_df['state_code'].iloc[0] if not kar_df.empty else "N/A"
num_districts = kar_df['district_name'].nunique()
num_subdistricts = kar_df['sub-district_name'].nunique()
num_villages = len(kar_df)

print("\n================ KARNATAKA STATE SUMMARY ================")
print(f"State Name: Karnataka")
print(f"State LGD Code: {state_code}")
print(f"Total Districts: {num_districts}")
print(f"Total Sub-Districts (Taluks): {num_subdistricts}")
print(f"Total Villages: {num_villages:,}")

print("\n================ DISTRICT-WISE BREAKDOWN (KARNATAKA) ================")
dist_summary = kar_df.groupby(['district_code', 'district_name']).agg(
    sub_districts=('sub-district_name', 'nunique'),
    villages=('village_code', 'count')
).reset_index().sort_values('district_name')

print(dist_summary.to_string(index=False))

# Data quality check for Karnataka
print("\n================ DATA QUALITY CHECK (KARNATAKA) ================")
print("Null values per column:")
print(kar_df.isnull().sum())
print("\nDuplicate rows check:", kar_df.duplicated().sum())

# Save summary metrics to json for easy artifact formatting if needed
metrics = {
    "total_records_all_india": total_rows,
    "total_states": total_states,
    "karnataka": {
        "state_code": int(state_code),
        "total_districts": num_districts,
        "total_subdistricts": num_subdistricts,
        "total_villages": num_villages,
        "district_breakdown": dist_summary.to_dict(orient="records")
    }
}

with open("karnataka_summary.json", "w") as f:
    json.dump(metrics, f, indent=2)
