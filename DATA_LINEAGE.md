# Karnataka Rural Healthcare Data Lineage & Pipeline Architecture

## Lineage Map
```
[Official Government Sources]
   ├── LGD Portal (MoPR) ---------------> 01_raw/raw_lgd_karnataka_2026.csv
   │                                           │
   │                                           v
   │                                     03_standardized/01_lgd_karnataka_administrative_master.csv (L1 Master)
   │                                           │
   ├── Census 2011 / DCHB -------------> 03_standardized/02_karnataka_village_demographics_infrastructure.csv (L2)
   ├── NIN Facility Registry -----------> 03_standardized/03_karnataka_health_facility_master.csv (L3)
   ├── HMIS MoHFW ---------------------> 03_standardized/04_karnataka_health_service_utilization.csv (L4)
   ├── NFHS-5 Survey ------------------> 03_standardized/05_karnataka_health_indicators.csv (L5 District Level)
   ├── Poshan Tracker -----------------> 03_standardized/06_karnataka_anganwadi_nutrition.csv (L6)
   ├── IMD & KSNDMC -------------------> 03_standardized/07_karnataka_weather_hazard_realtime.csv (L7)
   │
   ├── [GIS Computation Engine] --------> 03_standardized/08_karnataka_village_health_accessibility.csv (L8 Derived)
   │
   └── [Protected Systems DVDMS/108] --> 03_standardized/09 & 10 (Schema Audit: NOT PUBLICLY AVAILABLE)
                                               │
                                               v
                                         04_integrated/integrated_village_health_profile.csv
```

## Data Provenance Classifications
1. **REAL_SOURCE_DATA**: Directly ingested from government portals (LGD, Census 2011, NIN, HMIS, NFHS-5, Poshan Tracker, IMD).
2. **DERIVED_DATA**: Computed via transparent algorithms (e.g., Haversine distance matrix from village coordinates to nearest PHC).
3. **NOT_PUBLICLY_AVAILABLE**: Fields requiring internal government authentication (DVDMS drug logistics, 108 MMU real-time GPS telemetry). Never fabricated.
