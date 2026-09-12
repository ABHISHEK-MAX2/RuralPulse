import pandas as pd
import numpy as np
import os

np.random.seed(42)

input_file = "karnataka_lgd_codes.csv"
print(f"Loading Layer 1 (Real LGD Geography) from {input_file}...")
df_l1 = pd.read_csv(input_file, low_memory=False)

n = len(df_l1)
print(f"Total Villages: {n:,}")

coastal_ghats_districts = ['Dakshina Kannada', 'Udupi', 'Uttara Kannada', 'Kodagu', 'Chikkamagaluru', 'Shivamogga']
dry_north_districts = ['Vijayapura', 'Yadgir', 'Raichur', 'Koppal', 'Ballari', 'Kalaburagi', 'Gadag', 'Bagalkote']

# ==========================================
# LAYER 1: Geography & LGD Administrative Hierarchy
# ==========================================
file_l1 = "karnataka_layer1_geography_lgd.csv"
df_l1.to_csv(file_l1, index=False)
print(f"Saved Layer 1 CSV: '{file_l1}' ({df_l1.shape[1]} columns)")


# ==========================================
# LAYER 2: Demographics & Infrastructure
# ==========================================
file_l2 = "karnataka_layer2_demographics_infrastructure.csv"

populations = np.random.lognormal(mean=7.0, sigma=0.6, size=n).astype(int)
populations = np.clip(populations, 150, 12500)
households = (populations / np.random.uniform(4.0, 4.8, size=n)).astype(int)

literacy_base = np.where(df_l1['district_name'].isin(['Dakshina Kannada', 'Udupi', 'Bengaluru Urban']), 88.0, 72.0)
literacy_rates = np.round(np.clip(literacy_base + np.random.normal(0, 5, n), 52.0, 97.5), 1)

road_access_prob = np.where(df_l1['district_name'].isin(coastal_ghats_districts), 0.82, 0.91)
road_access_labels = np.where(np.random.binomial(1, road_access_prob, n) == 1, 'Yes', 'No')

water_sources = ['Piped Tap Water', 'Borewell with Pump', 'Covered Well', 'Open Well/Tank']
drinking_water = np.random.choice(water_sources, size=n, p=[0.55, 0.30, 0.10, 0.05])

electricity_pct = np.round(np.clip(np.random.normal(96.5, 3.5, n), 80.0, 100.0), 1)
pucca_housing_pct = np.round(np.clip(np.random.normal(78.0, 9.0, n), 45.0, 98.5), 1)

df_l2 = pd.DataFrame({
    'village_code': df_l1['village_code'],
    'total_population': populations,
    'total_households': households,
    'literacy_rate_pct': literacy_rates,
    'all_weather_road_access': road_access_labels,
    'drinking_water_source': drinking_water,
    'electrified_households_pct': electricity_pct,
    'pucca_housing_pct': pucca_housing_pct
})
df_l2.to_csv(file_l2, index=False)
print(f"Saved Layer 2 CSV: '{file_l2}' ({df_l2.shape[1]} columns)")


# ==========================================
# LAYER 3: Health & Nutrition Indicators
# ==========================================
file_l3 = "karnataka_layer3_health_indicators.csv"

phc_names = df_l1['sub-district_name'].astype(str) + " Primary Health Centre"

distance_base = np.where(df_l1['district_name'].isin(coastal_ghats_districts), 6.5, 3.5)
distance_phc = np.round(np.clip(distance_base + np.random.exponential(scale=2.5, size=n), 0.5, 24.0), 1)

immunization_pct = np.round(np.clip(np.random.normal(86.0, 7.0, n), 55.0, 99.5), 1)
anc_pct = np.round(np.clip(np.random.normal(82.0, 8.5, n), 50.0, 99.0), 1)
high_risk_preg = np.random.poisson(lam=np.maximum(1, populations * 0.004)).astype(int)
malnutrition_pct = np.round(np.clip(np.random.normal(16.5, 5.0, n), 4.0, 38.0), 1)
institutional_delivery_pct = np.round(np.clip(np.random.normal(92.0, 4.5, n), 70.0, 100.0), 1)

df_l3 = pd.DataFrame({
    'village_code': df_l1['village_code'],
    'assigned_phc': phc_names,
    'distance_to_phc_km': distance_phc,
    'full_immunization_rate_pct': immunization_pct,
    'anc_4_visits_pct': anc_pct,
    'high_risk_pregnancies_count': high_risk_preg,
    'child_malnutrition_rate_pct': malnutrition_pct,
    'institutional_deliveries_pct': institutional_delivery_pct
})
df_l3.to_csv(file_l3, index=False)
print(f"Saved Layer 3 CSV: '{file_l3}' ({df_l3.shape[1]} columns)")


# ==========================================
# LAYER 4: Weather & Climate Hazard
# ==========================================
file_l4 = "karnataka_layer4_weather_hazards.csv"

rainfall_mm = np.zeros(n)
temp_max_c = np.zeros(n)
temp_min_c = np.zeros(n)
flood_risk = []
drought_risk = []

flood_categories = ['Low', 'Moderate', 'High', 'Severe']
drought_categories = ['Low', 'Moderate', 'High']

for i in range(n):
    dname = df_l1['district_name'].iloc[i]
    if dname in coastal_ghats_districts:
        rainfall_mm[i] = np.random.normal(3400, 450)
        temp_max_c[i] = np.random.normal(31.5, 1.5)
        temp_min_c[i] = np.random.normal(22.0, 1.2)
        f_p = [0.30, 0.40, 0.20, 0.10]
        d_p = [0.70, 0.25, 0.05]
    elif dname in dry_north_districts:
        rainfall_mm[i] = np.random.normal(680, 120)
        temp_max_c[i] = np.random.normal(38.5, 2.0)
        temp_min_c[i] = np.random.normal(24.5, 1.5)
        f_p = [0.75, 0.20, 0.04, 0.01]
        d_p = [0.20, 0.45, 0.35]
    else:
        rainfall_mm[i] = np.random.normal(1100, 200)
        temp_max_c[i] = np.random.normal(33.0, 1.8)
        temp_min_c[i] = np.random.normal(20.5, 1.4)
        f_p = [0.60, 0.30, 0.08, 0.02]
        d_p = [0.50, 0.35, 0.15]
    
    flood_risk.append(np.random.choice(flood_categories, p=f_p))
    drought_risk.append(np.random.choice(drought_categories, p=d_p))

rainfall_mm = np.round(np.clip(rainfall_mm, 450, 5200), 1)
temp_max_c = np.round(temp_max_c, 1)
temp_min_c = np.round(temp_min_c, 1)

weather_alerts = ['Green (Normal)', 'Yellow (Watch)', 'Orange (Alert)', 'Red (Warning)']
weather_alert = np.random.choice(weather_alerts, size=n, p=[0.75, 0.15, 0.08, 0.02])

df_l4 = pd.DataFrame({
    'village_code': df_l1['village_code'],
    'annual_rainfall_mm': rainfall_mm,
    'temp_max_celsius': temp_max_c,
    'temp_min_celsius': temp_min_c,
    'flood_risk_level': flood_risk,
    'drought_risk_level': drought_risk,
    'weather_alert_level': weather_alert
})
df_l4.to_csv(file_l4, index=False)
print(f"Saved Layer 4 CSV: '{file_l4}' ({df_l4.shape[1]} columns)")


# ==========================================
# LAYER 5: Operational & Logistics Demo Data
# ==========================================
file_l5 = "karnataka_layer5_operational_logistics.csv"

vaccine_stock = np.random.randint(20, 850, size=n)
ifa_stock = np.random.randint(100, 3500, size=n)

doctor_statuses = ['Present', 'On Field Duty', 'On Leave', 'Post Vacant']
doctor_attendance = np.random.choice(doctor_statuses, size=n, p=[0.72, 0.15, 0.08, 0.05])

mmu_statuses = ['Active & On Route', 'Scheduled', 'Under Maintenance', 'Not Assigned']
mmu_availability = np.random.choice(mmu_statuses, size=n, p=[0.35, 0.35, 0.10, 0.20])

subcenter_statuses = ['Functional', 'Upgrading', 'Staff Shortage', 'Building Repair']
subcenter_status = np.random.choice(subcenter_statuses, size=n, p=[0.82, 0.08, 0.06, 0.04])

# Generate realistic recent visit dates (2026-08-01 to 2026-09-10)
random_days = np.random.randint(1, 40, size=n)
last_mmu_dates = [(pd.Timestamp('2026-09-12') - pd.Timedelta(days=int(d))).strftime('%Y-%m-%d') for d in random_days]

df_l5 = pd.DataFrame({
    'village_code': df_l1['village_code'],
    'vaccine_stock_doses': vaccine_stock,
    'ifa_tablet_stock_count': ifa_stock,
    'doctor_attendance_status': doctor_attendance,
    'mmu_availability': mmu_availability,
    'last_mmu_visit_date': last_mmu_dates,
    'subcenter_status': subcenter_status,
    'data_provenance': 'Synthetic Demo Operational Data'
})
df_l5.to_csv(file_l5, index=False)
print(f"Saved Layer 5 CSV: '{file_l5}' ({df_l5.shape[1]} columns)")

print("\n================ SUCCESS ================")
print("All 5 Layer CSV datasets created successfully!")
