"""Ingest all 30,771 Karnataka LGD Villages into SQLite krhi.db."""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd

from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.models import Village, District, DataSource
from app.services.scoring import calculate_village_risk_score

def ingest_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    csv_path = 'd:/IBM HACK/karnataka_multilayer_health_gis_dataset.csv'
    if not os.path.exists(csv_path):
        csv_path = 'd:/IBM HACK/04_integrated/integrated_village_health_profile.csv'

    print(f"Reading dataset from {csv_path}...")
    df = pd.read_csv(csv_path)

    print(f"Total rows in dataset: {len(df):,}")

    db.query(Village).delete()
    db.commit()

    villages_to_add = []
    for idx, row in df.iterrows():
        v_code = int(row.get('village_code', 0))
        v_name = str(row.get('village_name', f'Village #{v_code}'))
        d_code = int(row.get('district_code', 2901))
        d_name = str(row.get('district_name', 'Karnataka'))
        sub_code = int(row.get('sub-district_code', row.get('subdistrict_code', 0)))
        sub_name = str(row.get('sub-district_name', row.get('subdistrict_name', 'Rural Sub-District')))
        pop = int(row.get('total_population', row.get('population', 1000)))
        dist_phc = float(row.get('distance_to_phc_km', 10.0))
        time_phc = float(row.get('travel_time_minutes', row.get('travel_time_to_phc_minutes', dist_phc * 3.0)))
        road = "ALL_WEATHER" if row.get('all_weather_road_access', 1) == 1 else "SEASONAL_UNPAVED"
        flood = "HIGH" if dist_phc > 15.0 else ("MEDIUM" if dist_phc > 10.0 else "LOW")

        # Score calculation
        score_res = calculate_village_risk_score({
            "distance_to_phc_km": dist_phc,
            "travel_time_to_phc_minutes": time_phc,
            "road_accessibility": road,
            "flood_prone_indicator": flood,
            "population": pop
        })

        v = Village(
            village_code=v_code,
            village_name=v_name,
            subdistrict_code=sub_code,
            subdistrict_name=sub_name,
            district_code=d_code,
            district_name=d_name,
            population=pop,
            households=int(pop / 4.5),
            risk_score=score_res["risk_score"],
            risk_category=score_res["risk_category"],
            distance_to_phc_km=dist_phc,
            travel_time_to_phc_minutes=time_phc,
            road_accessibility=road,
            flood_prone_indicator=flood
        )
        villages_to_add.append(v)

        if len(villages_to_add) >= 5000:
            db.bulk_save_objects(villages_to_add)
            db.commit()
            villages_to_add = []
            print(f"Ingested {idx + 1:,} / {len(df):,} villages...")

    if villages_to_add:
        db.bulk_save_objects(villages_to_add)
        db.commit()

    total_in_db = db.query(Village).count()
    print(f"SUCCESSFULLY INGESTED ALL {total_in_db:,} VILLAGES INTO krhi.db SQLite Database!")

    # Ingest Data Sources info
    db.query(DataSource).delete()
    db.commit()

    layers = [
        ("LGD Administrative Master", 1, 30771),
        ("Village Demographics & Infrastructure", 2, 30771),
        ("Health Facility Master", 3, 721),
        ("Health Service Utilization", 4, 721),
        ("Health Indicators", 5, 32),
        ("Anganwadi Nutrition Data", 6, 481),
        ("Weather Hazard Real-Time", 7, 32),
        ("Village Accessibility Matrix", 8, 30771),
        ("Operational Resources", 9, 21),
        ("MMU Operations Log", 10, 11),
        ("Health Data Availability Matrix", 11, 11)
    ]
    for name, layer_num, count in layers:
        db.add(DataSource(source_name=name, layer_number=layer_num, record_count=count, status="ACTIVE"))
    db.commit()
    print("SUCCESSFULLY SEEDED DATA SOURCES MATRIX.")

if __name__ == "__main__":
    ingest_data()
