import sqlite3
import random
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "karnataka_health.db")

# Dictionary of bounding boxes for each Karnataka district code
DISTRICT_BOUNDS = {
    524: {"name": "Bagalkote", "lat": (15.80, 16.45), "lon": (75.20, 76.20)},
    528: {"name": "Ballari", "lat": (14.90, 15.65), "lon": (76.50, 77.20)},
    527: {"name": "Belagavi", "lat": (15.30, 16.60), "lon": (74.05, 75.30)},
    526: {"name": "Bengaluru Rural", "lat": (12.90, 13.50), "lon": (77.30, 77.90)},
    631: {"name": "Bengaluru South", "lat": (12.40, 12.95), "lon": (77.05, 77.65)},
    525: {"name": "Bengaluru Urban", "lat": (12.80, 13.15), "lon": (77.45, 77.80)},
    529: {"name": "Bidar", "lat": (17.50, 18.40), "lon": (76.80, 77.60)},
    531: {"name": "Chamarajanagar", "lat": (11.65, 12.35), "lon": (76.40, 77.40)},
    630: {"name": "Chikkaballapura", "lat": (13.30, 13.95), "lon": (77.50, 78.20)},
    532: {"name": "Chikkamagaluru", "lat": (13.10, 13.95), "lon": (75.10, 76.20)},
    533: {"name": "Chitradurga", "lat": (13.70, 14.55), "lon": (76.00, 76.90)},
    534: {"name": "Dakshina Kannada", "lat": (12.50, 13.20), "lon": (74.70, 75.60)},
    535: {"name": "Davanagere", "lat": (14.05, 14.70), "lon": (75.70, 76.45)},
    536: {"name": "Dharwad", "lat": (15.10, 15.65), "lon": (74.80, 75.40)},
    537: {"name": "Gadag", "lat": (14.90, 15.80), "lon": (75.40, 76.05)},
    539: {"name": "Hassan", "lat": (12.50, 13.40), "lon": (75.50, 76.40)},
    540: {"name": "Haveri", "lat": (14.30, 15.05), "lon": (75.10, 75.85)},
    538: {"name": "Kalaburagi", "lat": (16.80, 17.75), "lon": (76.40, 77.50)},
    541: {"name": "Kodagu", "lat": (11.90, 12.60), "lon": (75.40, 76.10)},
    542: {"name": "Kolar", "lat": (12.90, 13.45), "lon": (77.90, 78.55)},
    543: {"name": "Koppal", "lat": (15.10, 15.75), "lon": (75.80, 76.55)},
    544: {"name": "Mandya", "lat": (12.30, 12.75), "lon": (76.50, 77.10)},
    545: {"name": "Mysuru", "lat": (11.90, 12.60), "lon": (75.90, 77.00)},
    546: {"name": "Raichur", "lat": (15.80, 16.60), "lon": (76.30, 77.60)},
    547: {"name": "Shivamogga", "lat": (13.60, 14.45), "lon": (74.80, 75.85)},
    548: {"name": "Tumakuru", "lat": (13.00, 14.20), "lon": (76.40, 77.40)},
    549: {"name": "Udupi", "lat": (13.10, 13.90), "lon": (74.60, 75.25)},
    550: {"name": "Uttara Kannada", "lat": (13.90, 15.40), "lon": (74.10, 75.10)},
    738: {"name": "Vijayanagara", "lat": (14.70, 15.35), "lon": (75.80, 76.60)},
    530: {"name": "Vijayapura", "lat": (16.30, 17.30), "lon": (75.30, 76.40)},
    635: {"name": "Yadgir", "lat": (16.20, 16.95), "lon": (76.50, 77.45)},
}

# Fallback bounding box for entire Karnataka state
KARNATAKA_FALLBACK = {"lat": (11.6, 18.4), "lon": (74.0, 78.5)}

def get_coords(district_code, seed_val):
    bounds = DISTRICT_BOUNDS.get(district_code, KARNATAKA_FALLBACK)
    min_lat, max_lat = bounds["lat"]
    min_lon, max_lon = bounds["lon"]
    
    # Deterministic pseudo-random placement based on seed_val
    rng = random.Random(seed_val)
    lat = round(rng.uniform(min_lat, max_lat), 6)
    lon = round(rng.uniform(min_lon, max_lon), 6)
    return lat, lon

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("Updating LGD Villages GIS coordinates...")
    villages = cursor.execute("SELECT village_code, district_code FROM lgd_villages").fetchall()
    village_updates = []
    for v_code, d_code in villages:
        lat, lon = get_coords(d_code, v_code)
        village_updates.append((lat, lon, v_code))
    
    cursor.executemany("UPDATE lgd_villages SET latitude = ?, longitude = ? WHERE village_code = ?", village_updates)
    print(f"Updated {len(village_updates)} villages.")
    
    print("Updating Health Facilities GIS coordinates...")
    facilities = cursor.execute("SELECT facility_id, district_code, village_code FROM health_facilities").fetchall()
    facility_updates = []
    for f_id, d_code, v_code in facilities:
        seed_val = v_code if v_code else hash(f_id)
        lat, lon = get_coords(d_code, seed_val)
        facility_updates.append((lat, lon, f_id))
        
    cursor.executemany("UPDATE health_facilities SET latitude = ?, longitude = ? WHERE facility_id = ?", facility_updates)
    print(f"Updated {len(facility_updates)} facilities.")
    
    print("Updating Weather Hazards GIS coordinates...")
    hazards = cursor.execute("SELECT id, district_code, taluk_code FROM weather_hazards").fetchall()
    hazard_updates = []
    for h_id, d_code, t_code in hazards:
        lat, lon = get_coords(d_code, h_id * 1000 + t_code)
        hazard_updates.append((lat, lon, h_id))
        
    cursor.executemany("UPDATE weather_hazards SET latitude = ?, longitude = ? WHERE id = ?", hazard_updates)
    print(f"Updated {len(hazard_updates)} weather hazards.")

    conn.commit()
    conn.close()
    print("Successfully updated GIS coordinates for all 31 districts!")

if __name__ == "__main__":
    main()
