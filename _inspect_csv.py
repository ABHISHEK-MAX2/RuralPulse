from pathlib import Path
import csv

p = Path(r"D:\IBM HACK")
print("FILES")
for f in sorted(p.iterdir()):
    kind = "DIR" if f.is_dir() else "FILE"
    size = f.stat().st_size if f.is_file() else "-"
    print(f"{kind}\t{size}\t{f.name}")

files = [
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
    "04_integrated/integrated_village_health_profile.csv",
]
for name in files:
    path = p / name
    print("\n====", name, "====")
    print("exists", path.exists(), "size", path.stat().st_size if path.exists() else 0)
    if not path.exists():
        continue
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        r = csv.reader(fh)
        header = next(r)
        print("ncols", len(header))
        print("header", header)
        row = next(r, None)
        print("sample", row[:25] if row else None)
