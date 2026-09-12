import os
import shutil

base_dir = r"d:\IBM HACK"
std_dir = os.path.join(base_dir, "03_standardized")
datasets_dir1 = os.path.join(base_dir, "datasets")
datasets_dir2 = os.path.join(base_dir, "platform", "backend", "datasets")

os.makedirs(datasets_dir1, exist_ok=True)
os.makedirs(datasets_dir2, exist_ok=True)

files_to_copy = [
    "01_lgd_karnataka_administrative_master.csv",
    "02_karnataka_village_demographics_infrastructure.csv",
    "03_karnataka_health_facility_master.csv",
    "04_karnataka_health_service_utilization.csv",
    "05_karnataka_health_indicators.csv",
    "06_karnataka_anganwadi_nutrition.csv",
    "07_karnataka_weather_hazard_realtime.csv",
    "08_karnataka_village_health_accessibility.csv",
    "09_karnataka_health_operational_resources.csv",
    "10_karnataka_mmu_operations.csv",
    "11_karnataka_health_data_availability_matrix.csv"
]

print("Copying complete 11 datasets from 03_standardized/ into datasets/ directories...")

for fn in files_to_copy:
    src = os.path.join(std_dir, fn)
    if not os.path.exists(src):
        src = os.path.join(base_dir, fn)
        
    if os.path.exists(src):
        dst1 = os.path.join(datasets_dir1, fn)
        dst2 = os.path.join(datasets_dir2, fn)
        shutil.copy2(src, dst1)
        shutil.copy2(src, dst2)
        print(f"  [OK] Copied {fn}")
    else:
        print(f"  [WARNING] File not found: {src}")

print("\nDatasets directory setup complete!")
