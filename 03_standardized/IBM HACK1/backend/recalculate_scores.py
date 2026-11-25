import os
import json
import csv
from app.database import SessionLocal
from app.models.domain import (
    LGDVillage, VulnerabilityScore, AIRecommendation, Alert
)
from app.services.scoring_engine import VulnerabilityScoringEngine
from app.services.recommendation_engine import RecommendationEngine

def run_rescore():
    print("--- Re-calculating Vulnerability Scores & SHAP Attributions for all 30,771 Villages ---")
    db = SessionLocal()
    try:
        db.query(VulnerabilityScore).delete()
        db.query(AIRecommendation).delete()
        db.query(Alert).delete()
        db.commit()
        print("[OK] Cleared legacy vulnerability scores, recommendations, and alerts.")

        base_dir = os.path.dirname(os.path.abspath(__file__))
        datasets_dir = os.path.abspath(os.path.join(base_dir, "..", "DATASETS"))
        print(f"[INFO] Loading datasets from: {datasets_dir}")

        def parse_float(val, default=0.0):
            try:
                return float(val) if val is not None and str(val).strip() != "" else default
            except (ValueError, TypeError):
                return default

        def parse_int(val, default=0):
            try:
                return int(float(val)) if val is not None and str(val).strip() != "" else default
            except (ValueError, TypeError):
                return default

        demo_dict = {}
        demo_path = os.path.join(datasets_dir, "02_karnataka_village_demographics_infrastructure.csv")
        if os.path.exists(demo_path):
            with open(demo_path, mode="r", encoding="utf-8-sig") as f:
                for row in csv.DictReader(f):
                    v_code = parse_int(row.get("village_code"))
                    if v_code: demo_dict[v_code] = row
            print(f"[OK] Indexed {len(demo_dict)} demographics records.")

        acc_dict = {}
        acc_path = os.path.join(datasets_dir, "08_karnataka_village_health_accessibility.csv")
        if os.path.exists(acc_path):
            with open(acc_path, mode="r", encoding="utf-8-sig") as f:
                for row in csv.DictReader(f):
                    v_code = parse_int(row.get("village_code"))
                    if v_code: acc_dict[v_code] = row
            print(f"[OK] Indexed {len(acc_dict)} accessibility records.")

        ind_dict = {}
        ind_path = os.path.join(datasets_dir, "05_karnataka_health_indicators.csv")
        if os.path.exists(ind_path):
            with open(ind_path, mode="r", encoding="utf-8-sig") as f:
                for row in csv.DictReader(f):
                    d_code = parse_int(row.get("district_code"))
                    if d_code: ind_dict[d_code] = row
            print(f"[OK] Indexed {len(ind_dict)} district indicators records.")

        ang_dict = {}
        ang_path = os.path.join(datasets_dir, "06_karnataka_anganwadi_nutrition.csv")
        if os.path.exists(ang_path):
            with open(ang_path, mode="r", encoding="utf-8-sig") as f:
                for row in csv.DictReader(f):
                    v_code = parse_int(row.get("village_code"))
                    if v_code: ang_dict[v_code] = row
            print(f"[OK] Indexed {len(ang_dict)} anganwadi records.")

        wx_dict = {}
        wx_path = os.path.join(datasets_dir, "07_karnataka_weather_hazard_realtime.csv")
        if os.path.exists(wx_path):
            with open(wx_path, mode="r", encoding="utf-8-sig") as f:
                for row in csv.DictReader(f):
                    d_code = parse_int(row.get("district_code"))
                    if d_code: wx_dict[d_code] = row
            print(f"[OK] Indexed {len(wx_dict)} weather records.")

        util_dict = {}
        util_path = os.path.join(datasets_dir, "04_karnataka_health_service_utilization.csv")
        if os.path.exists(util_path):
            with open(util_path, mode="r", encoding="utf-8-sig") as f:
                for row in csv.DictReader(f):
                    fac_id = row.get("facility_id")
                    if fac_id: util_dict[fac_id] = row
            print(f"[OK] Indexed {len(util_dict)} facility utilization records.")

        villages = db.query(LGDVillage).all()
        print(f"[INFO] Computing calibrated scores for {len(villages)} villages...")

        score_objects = []
        recommendations_to_create = []
        alerts_to_create = []

        for v in villages:
            v_code = v.village_code
            d_code = v.district_code

            d_row = demo_dict.get(v_code, {})
            ac_row = acc_dict.get(v_code, {})
            ind_row = ind_dict.get(d_code, {})
            ang_row = ang_dict.get(v_code, {})
            wx_row = wx_dict.get(d_code, {})
            u_row = util_dict.get(f"KA-PHC-{d_code}01", {})

            score, risk_lvl, subscores, top_factors, pred_7d = VulnerabilityScoringEngine.compute_village_vulnerability(
                demographics=d_row,
                accessibility=ac_row,
                district_indicators=ind_row,
                anganwadi=ang_row,
                weather=wx_row,
                facility_utilization=u_row
            )

            score_objects.append(VulnerabilityScore(
                village_code=v_code,
                score=score,
                risk_level=risk_lvl,
                predicted_score_7d=pred_7d,
                healthcare_access_subscore=subscores["healthcare_access"],
                maternal_child_subscore=subscores["maternal_child_health"],
                immunization_subscore=subscores["immunization_coverage"],
                nutrition_subscore=subscores["nutrition_malnutrition"],
                infra_subscore=subscores["infrastructure"],
                demographic_subscore=subscores["demographics"],
                resource_subscore=subscores["operational_resources"],
                environmental_subscore=subscores["weather_environmental"],
                utilization_subscore=subscores["service_utilization"],
                trend_subscore=subscores["historical_trend"],
                shap_json=json.dumps(subscores),
                top_contributing_factors_json=json.dumps(top_factors)
            ))

            if score >= 50.0:
                recs = RecommendationEngine.generate_recommendations_for_village(
                    village_code=v_code,
                    village_name=v.village_name,
                    vulnerability_score=score,
                    risk_level=risk_lvl,
                    subscores=subscores,
                    top_factors=top_factors,
                    accessibility=ac_row,
                    anganwadi=ang_row
                )
                for r in recs:
                    recommendations_to_create.append(AIRecommendation(
                        village_code=r["village_code"],
                        action=r["action"],
                        reason=r["reason"],
                        priority=r["priority"],
                        expected_impact=r["expected_impact"],
                        required_resources=r["required_resources"],
                        suggested_deadline=r["suggested_deadline"],
                        confidence=r["confidence"],
                        supporting_indicators_json=json.dumps(r["supporting_indicators"]),
                        status="PENDING_REVIEW"
                    ))

            if score >= 65.0 or "HIGH" in str(ac_row.get("flood_prone_indicator", "")).upper():
                alerts_to_create.append(Alert(
                    village_code=v_code,
                    district_code=d_code,
                    alert_type="HIGH_VULNERABILITY_SPIKE" if score >= 65.0 else "FLOOD_HAZARD_ALERT",
                    title=f"High Risk Alert: {v.village_name} ({v.taluk_name})",
                    description=f"Village {v.village_name} scored {score}/100 ({risk_lvl}). Primary driver: Travel time to PHC ({ac_row.get('travel_time_to_phc_minutes', 30)} min) and severe care accessibility deficit.",
                    severity="CRITICAL" if score >= 80.0 else "HIGH",
                    status="OPEN",
                    recommended_action="Deploy MMU and initiate emergency maternal/child health screening."
                ))

        db.bulk_save_objects(score_objects)
        db.commit()
        print(f"[OK] Re-saved {len(score_objects)} vulnerability scores.")

        if recommendations_to_create:
            db.bulk_save_objects(recommendations_to_create[:300])
            db.commit()
            print(f"[OK] Re-generated {len(recommendations_to_create[:300])} AI recommendations.")

        if alerts_to_create:
            db.bulk_save_objects(alerts_to_create[:120])
            db.commit()
            print(f"[OK] Re-generated {len(alerts_to_create[:120])} system alerts.")

    finally:
        db.close()

if __name__ == "__main__":
    run_rescore()
