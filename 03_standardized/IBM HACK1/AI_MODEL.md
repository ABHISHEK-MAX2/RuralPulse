# Explainable AI & Vulnerability Index Specification

## 10-Dimensional Vulnerability Index (0–100)

| Dimension | Weight | Primary Indicators |
| :--- | :---: | :--- |
| **Healthcare Accessibility** | 20% | Distance & travel time to nearest PHC/CHC, road condition, flood risk |
| **Maternal & Child Health** | 15% | District ANC coverage gap, non-institutional delivery rate |
| **Immunization Coverage** | 15% | District under-5 full immunization deficit |
| **Nutrition & Malnutrition** | 10% | Poshan Tracker SAM & MAM case counts |
| **Infrastructure & Basic Amenities** | 10% | Unpaved road, lack of tap water / electricity / 4G telecom |
| **Demographic Burden** | 10% | Children <5 ratio, elderly ratio, literacy deficit |
| **Operational Resources** | 5% | Doctor/Nurse vacancy rates |
| **Weather & Environmental Hazards** | 5% | Heavy rainfall warnings, extreme heat, flood vulnerability |
| **Service Utilization Deficit** | 5% | OPD/IPD visits per capita |
| **Historical Vulnerability Trend** | 5% | Risk delta over previous quarters |

---

## Explainable AI (SHAP) Factor Attribution

For every village, the platform generates exact point contributions for top risk drivers:
- Example: `+12.5 pts contribution from Travel Time to PHC (45 mins)`
- Example: `+8.2 pts contribution from Malnutrition Burden (3 SAM cases registered)`
