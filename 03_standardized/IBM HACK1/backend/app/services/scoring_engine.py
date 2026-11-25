import json
import math
from typing import Dict, Any, Tuple, List

def safe_float(val, default=0.0) -> float:
    try:
        return float(val) if val is not None and str(val).strip() != "" else default
    except (ValueError, TypeError):
        return default

def safe_int(val, default=0) -> int:
    try:
        return int(float(val)) if val is not None and str(val).strip() != "" else default
    except (ValueError, TypeError):
        return default

class VulnerabilityScoringEngine:
    """
    0-100 Explainable Vulnerability Index Engine for Karnataka Villages.
    Combines 10 weighted public health and infrastructural dimensions.
    """
    
    @staticmethod
    def compute_village_vulnerability(
        demographics: Dict[str, Any],
        accessibility: Dict[str, Any],
        district_indicators: Dict[str, Any],
        anganwadi: Dict[str, Any],
        weather: Dict[str, Any],
        facility_utilization: Dict[str, Any]
    ) -> Tuple[float, str, Dict[str, float], List[Dict[str, Any]], float]:
        """
        Calculates vulnerability score, risk level, subscores, top SHAP factors, and 7-day predicted risk.
        """
        
        # 1. Healthcare Accessibility Subscore (Weight: 22%)
        travel_time_phc = safe_float(accessibility.get("travel_time_to_phc_minutes"), 15.0)
        distance_phc = safe_float(accessibility.get("distance_to_phc_km"), 5.0)
        road_type = str(accessibility.get("road_type", "")).upper()
        flood_risk = str(accessibility.get("flood_prone_indicator", "")).upper()
        
        access_score = min(100.0, (travel_time_phc / 35.0) * 65.0 + (distance_phc / 10.0) * 25.0)
        if "UNPAVED" in road_type or "GRAVEL" in road_type:
            access_score += 20.0
        if "HIGH" in flood_risk or "YES" in flood_risk:
            access_score += 15.0
        access_score = min(100.0, access_score)

        # 2. Maternal & Child Health Subscore (Weight: 16%)
        anc_coverage = safe_float(district_indicators.get("anc_coverage"), 80.0)
        inst_delivery = safe_float(district_indicators.get("institutional_delivery"), 90.0)
        maternal_score = max(0.0, (100.0 - anc_coverage) * 2.2 + (100.0 - inst_delivery) * 1.5)
        maternal_score = min(100.0, maternal_score)

        # 3. Immunization Coverage Subscore (Weight: 16%)
        imm_coverage = safe_float(district_indicators.get("immunization_coverage"), 85.0)
        imm_score = max(0.0, (100.0 - imm_coverage) * 2.5)
        imm_score = min(100.0, imm_score)

        # 4. Nutrition & Malnutrition Subscore (Weight: 12%)
        screened = safe_int(anganwadi.get("children_screened"), 50)
        sam_cases = safe_int(anganwadi.get("sam_cases"), 0)
        mam_cases = safe_int(anganwadi.get("mam_cases"), 0)
        if screened > 0:
            sam_rate = (sam_cases / screened) * 100.0
            mam_rate = (mam_cases / screened) * 100.0
        else:
            sam_rate, mam_rate = 0.0, 0.0
        nutrition_score = min(100.0, sam_rate * 35.0 + mam_rate * 15.0 + (25.0 if sam_cases > 0 else 0.0) + (10.0 if mam_cases > 0 else 0.0))

        # 5. Infrastructure & Basic Amenities Subscore (Weight: 12%)
        road_acc = str(demographics.get("road_access", "")).upper()
        drinking_water = str(demographics.get("drinking_water_access", "")).upper()
        telecom = str(demographics.get("telecom_connectivity", "")).upper()
        infra_score = 0.0
        if "UNPAVED" in road_acc or "GRAVEL" in road_acc or "DIRT" in road_acc:
            infra_score += 40.0
        if "TAP" not in drinking_water and "PIPED" not in drinking_water:
            infra_score += 30.0
        if "POOR" in telecom or "NO" in telecom or "EDGE" in telecom:
            infra_score += 30.0
        infra_score = min(100.0, infra_score)

        # 6. Demographic Vulnerability Subscore (Weight: 10%)
        pop = safe_int(demographics.get("population"), 1000)
        u5 = safe_int(demographics.get("children_under_5"), 80)
        elderly = safe_int(demographics.get("elderly_population"), 80)
        literacy = safe_float(demographics.get("literacy_rate"), 70.0)
        
        u5_pct = (u5 / pop * 100.0) if pop > 0 else 8.0
        elderly_pct = (elderly / pop * 100.0) if pop > 0 else 8.0
        demo_score = min(100.0, (u5_pct / 12.0) * 35.0 + (elderly_pct / 12.0) * 35.0 + max(0.0, 100.0 - literacy) * 0.5)

        # 7. Operational Resource Availability Subscore (Weight: 4%)
        resource_score = 30.0

        # 8. Weather & Environmental Hazard Subscore (Weight: 4%)
        rainfall = safe_float(weather.get("rainfall"), 0.0)
        warning = str(weather.get("heavy_rainfall_warning", "")).upper()
        env_score = min(100.0, (rainfall / 40.0) * 50.0 + (45.0 if "YES" in warning or "HIGH" in warning else 0.0))

        # 9. Service Utilization Deficit Subscore (Weight: 2%)
        opd = safe_int(facility_utilization.get("opd"), 1000)
        util_score = max(0.0, 100.0 - (opd / 2000.0 * 100.0))
        util_score = min(100.0, util_score)

        # 10. Historical Vulnerability Trend Subscore (Weight: 2%)
        trend_score = 25.0

        # Raw Weighted Total Score
        raw_score = (
            access_score * 0.22 +
            maternal_score * 0.16 +
            imm_score * 0.16 +
            nutrition_score * 0.12 +
            infra_score * 0.12 +
            demo_score * 0.10 +
            resource_score * 0.04 +
            env_score * 0.04 +
            util_score * 0.02 +
            trend_score * 0.02
        )
        
        # Compound risk multiplier for multi-vulnerability co-occurrence
        compound_triggers = 0
        if access_score >= 45.0: compound_triggers += 1
        if nutrition_score >= 25.0 or sam_cases > 0: compound_triggers += 1
        if infra_score >= 40.0: compound_triggers += 1
        if maternal_score >= 30.0: compound_triggers += 1
        if "HIGH" in flood_risk or "YES" in warning: compound_triggers += 1

        multiplier = 1.0 + (compound_triggers * 0.15)
        total_score = round(min(96.0, max(0.0, raw_score * multiplier)), 1)

        # Risk Classification Tiers
        if total_score >= 70.0:
            risk_level = "CRITICAL"
        elif total_score >= 50.0:
            risk_level = "HIGH"
        elif total_score >= 30.0:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        # 7-day Predictive Forecast Risk
        weather_increase = 3.5 if "YES" in warning else 0.5
        predicted_score_7d = round(min(100.0, total_score + weather_increase), 1)

        subscores = {
            "healthcare_access": round(access_score, 1),
            "maternal_child_health": round(maternal_score, 1),
            "immunization_coverage": round(imm_score, 1),
            "nutrition_malnutrition": round(nutrition_score, 1),
            "infrastructure": round(infra_score, 1),
            "demographics": round(demo_score, 1),
            "operational_resources": round(resource_score, 1),
            "weather_environmental": round(env_score, 1),
            "service_utilization": round(util_score, 1),
            "historical_trend": round(trend_score, 1)
        }

        # SHAP-like Contributing Factors Breakdown
        factor_candidates = [
            ("Travel Time to PHC", access_score * 0.20, f"{travel_time_phc:.0f} mins travel to nearest PHC ({distance_phc:.1f} km)"),
            ("Immunization Gap", imm_score * 0.15, f"{imm_coverage:.1f}% under-5 full immunization coverage in district"),
            ("Maternal Care Deficit", maternal_score * 0.15, f"{anc_coverage:.1f}% 1st trimester ANC coverage"),
            ("Malnutrition Incidence", nutrition_score * 0.10, f"{sam_cases} SAM cases & {mam_cases} MAM cases registered"),
            ("Infrastructure Deficit", infra_score * 0.10, f"Road condition: {road_type if road_type else 'Rural access road'}"),
            ("Demographic Burden", demo_score * 0.10, f"{u5} children under 5 & {elderly} elderly residents"),
            ("Weather & Flood Risk", env_score * 0.05, f"Rainfall: {rainfall:.1f}mm | Heavy rain alert: {warning}")
        ]
        
        factor_candidates.sort(key=lambda x: x[1], reverse=True)
        top_factors = [
            {
                "factor_name": name,
                "impact_points": round(pts, 1),
                "explanation": expl
            }
            for name, pts, expl in factor_candidates[:5]
        ]

        return total_score, risk_level, subscores, top_factors, predicted_score_7d
