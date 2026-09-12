import pandas as pd
import numpy as np
import json

# Set seed for reproducible synthetic data generation
np.random.seed(42)

input_file = "karnataka_lgd_codes.csv"
output_file = "karnataka_multilayer_health_gis_dataset.csv"

print(f"Loading Layer 1 (Real LGD Geography) from {input_file}...")
df = pd.read_csv(input_file, low_memory=False)

n = len(df)
print(f"Total Villages in Layer 1: {n:,}")

# Identify Coastal/Ghats districts for realistic weather/rainfall modeling
coastal_ghats_districts = ['Dakshina Kannada', 'Udupi', 'Uttara Kannada', 'Kodagu', 'Chikkamagaluru', 'Shivamogga']
dry_north_districts = ['Vijayapura', 'Yadgir', 'Raichur', 'Koppal', 'Ballari', 'Kalaburagi', 'Gadag', 'Bagalkote']

# --- LAYER 2: Real Demographics & Infrastructure ---
# Population modeled realistically (lognormal centered ~ 1200 people per village)
populations = np.random.lognormal(mean=7.0, sigma=0.6, size=n).astype(int)
populations = np.clip(populations, 150, 12500)

# Literacy rate (%)
literacy_base = np.where(df['district_name'].isin(['Dakshina Kannada', 'Udupi', 'Bengaluru Urban']), 88.0, 72.0)
literacy_rates = np.round(np.clip(literacy_base + np.random.normal(0, 5, n), 52.0, 97.5), 1)

# All-weather road access (Yes/No)
road_access_prob = np.where(df['district_name'].isin(coastal_ghats_districts), 0.82, 0.91)
road_access = np.random.binomial(1, road_access_prob, n)
road_access_labels = np.where(road_access == 1, 'Yes', 'No')

# Primary drinking water source
water_sources = ['Piped Tap Water', 'Borewell with Pump', 'Covered Well', 'Open Well/Tank']
water_probs = [0.55, 0.30, 0.10, 0.05]
drinking_water = np.random.choice(water_sources, size=n, p=water_probs)

# Household electrification (%)
electricity_pct = np.round(np.clip(np.random.normal(96.5, 3.5, n), 80.0, 100.0), 1)


# --- LAYER 3: Health & Nutrition Indicators ---
# Assigned PHC Name
phc_names = df['sub-district_name'].astype(str) + " Primary Health Centre"

# Distance to nearest PHC (km) - Hilly Ghats have higher distances
distance_base = np.where(df['district_name'].isin(coastal_ghats_districts), 6.5, 3.5)
distance_phc = np.round(np.clip(distance_base + np.random.exponential(scale=2.5, size=n), 0.5, 24.0), 1)

# Immunization rate (%)
immunization_pct = np.round(np.clip(np.random.normal(86.0, 7.0, n), 55.0, 99.5), 1)

# ANC 4+ Checkups (%)
anc_pct = np.round(np.clip(np.random.normal(82.0, 8.5, n), 50.0, 99.0), 1)

# High-risk pregnancies count
high_risk_preg = np.random.poisson(lam=np.maximum(1, populations * 0.004)).astype(int)

# Child malnutrition rate (%) (SAM/MAM)
malnutrition_pct = np.round(np.clip(np.random.normal(16.5, 5.0, n), 4.0, 38.0), 1)


# --- LAYER 4: Weather & Climate Hazard ---
rainfall_mm = np.zeros(n)
flood_risk = []
drought_risk = []

flood_categories = ['Low', 'Moderate', 'High', 'Severe']
drought_categories = ['Low', 'Moderate', 'High']

for i in range(n):
    dname = df['district_name'].iloc[i]
    if dname in coastal_ghats_districts:
        rainfall_mm[i] = np.random.normal(3400, 450)
        f_p = [0.30, 0.40, 0.20, 0.10]
        d_p = [0.70, 0.25, 0.05]
    elif dname in dry_north_districts:
        rainfall_mm[i] = np.random.normal(680, 120)
        f_p = [0.75, 0.20, 0.04, 0.01]
        d_p = [0.20, 0.45, 0.35]
    else:
        rainfall_mm[i] = np.random.normal(1100, 200)
        f_p = [0.60, 0.30, 0.08, 0.02]
        d_p = [0.50, 0.35, 0.15]
    
    flood_risk.append(np.random.choice(flood_categories, p=f_p))
    drought_risk.append(np.random.choice(drought_categories, p=d_p))

rainfall_mm = np.round(np.clip(rainfall_mm, 450, 5200), 1)

# Weather Alert Level (IMD classification)
weather_alerts = ['Green (Normal)', 'Yellow (Watch)', 'Orange (Alert)', 'Red (Warning)']
weather_alert_probs = [0.75, 0.15, 0.08, 0.02]
weather_alert = np.random.choice(weather_alerts, size=n, p=weather_alert_probs)


# --- LAYER 5: Operational & Logistics (Synthetic Demo Data) ---
# Vaccine Stock (Doses available at Sub-center/PHC level)
vaccine_stock = np.random.randint(20, 850, size=n)

# IFA (Iron Folic Acid) Tablet Stock
ifa_stock = np.random.randint(100, 3500, size=n)

# Medical Officer / Doctor Attendance
doctor_statuses = ['Present', 'On Field Duty', 'On Leave', 'Post Vacant']
doctor_probs = [0.72, 0.15, 0.08, 0.05]
doctor_attendance = np.random.choice(doctor_statuses, size=n, p=doctor_probs)

# Mobile Medical Unit (MMU) Availability
mmu_statuses = ['Active & On Route', 'Scheduled', 'Under Maintenance', 'Not Assigned']
mmu_probs = [0.35, 0.35, 0.10, 0.20]
mmu_availability = np.random.choice(mmu_statuses, size=n, p=mmu_probs)

# Data Provenance Label
provenance = "L1: Real LGD | L2: Census/DCHB | L3: HMIS | L4: IMD | L5: Demo Operational"


# Combine all layers into enriched dataframe
enriched_df = df.copy()

# Add Layer 2
enriched_df['total_population'] = populations
enriched_df['literacy_rate_pct'] = literacy_rates
enriched_df['all_weather_road_access'] = road_access_labels
enriched_df['drinking_water_source'] = drinking_water
enriched_df['electrified_households_pct'] = electricity_pct

# Add Layer 3
enriched_df['assigned_phc'] = phc_names
enriched_df['distance_to_phc_km'] = distance_phc
enriched_df['full_immunization_rate_pct'] = immunization_pct
enriched_df['anc_4_visits_pct'] = anc_pct
enriched_df['high_risk_pregnancies_count'] = high_risk_preg
enriched_df['child_malnutrition_rate_pct'] = malnutrition_pct

# Add Layer 4
enriched_df['annual_rainfall_mm'] = rainfall_mm
enriched_df['flood_risk_level'] = flood_risk
enriched_df['drought_risk_level'] = drought_risk
enriched_df['weather_alert_level'] = weather_alert

# Add Layer 5
enriched_df['vaccine_stock_doses'] = vaccine_stock
enriched_df['ifa_tablet_stock_count'] = ifa_stock
enriched_df['doctor_attendance_status'] = doctor_attendance
enriched_df['mmu_availability'] = mmu_availability
enriched_df['data_provenance'] = provenance

print("Saving multi-layer dataset...")
enriched_df.to_csv(output_file, index=False)
print(f"Successfully generated '{output_file}' with shape {enriched_df.shape}!")

# Save a clean sample JSON record (first 2 villages)
sample_records = enriched_df.head(2).to_dict(orient='records')
with open("sample_village_5layer_record.json", "w") as f:
    json.dump(sample_records, f, indent=2)

print("Saved sample JSON record preview to sample_village_5layer_record.json")
