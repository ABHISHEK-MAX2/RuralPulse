import os
import csv
import json
from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app.models.domain import (
    User, LGDVillage, VillageDemographics, HealthFacility,
    HealthServiceUtilization, HealthIndicators, AnganwadiNutrition,
    WeatherHazard, VillageAccessibility, OperationalResources,
    MMUOperation, DataAvailabilityMatrix, VulnerabilityScore,
    AIRecommendation, MMUMission, Alert, AuditLog
)
from app.services.scoring_engine import VulnerabilityScoringEngine
from app.services.recommendation_engine import RecommendationEngine
from app.services.audit_service import AuditLogger
from app.services.auth_service import get_password_hash
from app.config import settings

def seed_database():
    print("--- Starting Database Seeding & Ingestion Pipeline ---")
    
    # 1. Create tables
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    
    try:
        # Check if database is already seeded
        if db.query(LGDVillage).count() > 0:
            print("[INFO] Database already contains seeded data. Skipping re-seeding.")
            return

        # 2. Seed Default User Personas
        users = [
            User(
                email="state_admin@karnataka.gov.in",
                hashed_password=get_password_hash("admin123"),
                full_name="Dr. R. K. Swamy (State Health Director)",
                role="STATE_ADMIN",
                district_code=None
            ),
            User(
                email="dho_bagalkote@karnataka.gov.in",
                hashed_password=get_password_hash("dho123"),
                full_name="Dr. Vijaykumar Patil (DHO Bagalkote)",
                role="DHO",
                district_code=524
            ),
            User(
                email="mmu_coord_bagalkote@karnataka.gov.in",
                hashed_password=get_password_hash("mmu123"),
                full_name="Suresh Kumar (MMU Fleet Coordinator Bagalkote)",
                role="MMU_COORDINATOR",
                district_code=524,
                taluk_code=5446
            ),
            User(
                email="sysadmin@karnataka.gov.in",
                hashed_password=get_password_hash("sys123"),
                full_name="System Administrator (e-Health Portal)",
                role="SYS_ADMIN",
                district_code=None
            )
        ]
        db.add_all(users)
        db.commit()
        print("[OK] Seeded default user personas (State Admin, DHO, MMU Coordinator, Sys Admin)")

        datasets_dir = settings.DATASETS_DIR
        print(f"[INFO] Reading datasets from: {datasets_dir}")

        # Helper function for safe float conversion
        def parse_float(val, default=0.0):
            try:
                return float(val) if val and str(val).strip() != "" else default
            except (ValueError, TypeError):
                return default

        # Helper function for safe int conversion
        def parse_int(val, default=0):
            try:
                return int(float(val)) if val and str(val).strip() != "" else default
            except (ValueError, TypeError):
                return default

        # 3. Load 01 LGD Administrative Master
        lgd_path = os.path.join(datasets_dir, "01_lgd_karnataka_administrative_master.csv")
        lgd_records = []
        if os.path.exists(lgd_path):
            with open(lgd_path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    lgd_records.append(LGDVillage(
                        village_code=parse_int(row.get("village_code")),
                        village_name=row.get("village_name", "").strip(),
                        state_code=parse_int(row.get("state_code", 29)),
                        state_name=row.get("state_name", "Karnataka").strip(),
                        district_code=parse_int(row.get("district_code")),
                        district_name=row.get("district_name", "").strip(),
                        taluk_code=parse_int(row.get("taluk_code")),
                        taluk_name=row.get("taluk_name", "").strip(),
                        gram_panchayat_code=parse_int(row.get("gram_panchayat_code")),
                        gram_panchayat_name=row.get("gram_panchayat_name", "").strip(),
                        latitude=parse_float(row.get("latitude")),
                        longitude=parse_float(row.get("longitude")),
                        source=row.get("source"),
                        source_url=row.get("source_url"),
                        retrieval_date=row.get("retrieval_date"),
                        record_status=row.get("record_status", "ACTIVE")
                    ))
            db.bulk_save_objects(lgd_records)
            db.commit()
            print(f"[OK] Ingested {len(lgd_records)} LGD administrative village records.")

        # 4. Load 02 Demographics & Infrastructure
        demo_path = os.path.join(datasets_dir, "02_karnataka_village_demographics_infrastructure.csv")
        demo_dict = {}
        if os.path.exists(demo_path):
            with open(demo_path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                demo_objects = []
                for row in reader:
                    v_code = parse_int(row.get("village_code"))
                    d_obj = VillageDemographics(
                        village_code=v_code,
                        population=parse_int(row.get("population")),
                        male_population=parse_int(row.get("male_population")),
                        female_population=parse_int(row.get("female_population")),
                        children_under_5=parse_int(row.get("children_under_5")),
                        elderly_population=parse_int(row.get("elderly_population")),
                        households=parse_int(row.get("households")),
                        literacy_rate=parse_float(row.get("literacy_rate")),
                        drinking_water_access=row.get("drinking_water_access"),
                        electricity_access=row.get("electricity_access"),
                        road_access=row.get("road_access"),
                        telecom_connectivity=row.get("telecom_connectivity"),
                        internet_connectivity=row.get("internet_connectivity"),
                        source=row.get("source"),
                        source_year=parse_int(row.get("source_year")),
                        geographic_granularity=row.get("geographic_granularity"),
                        source_url=row.get("source_url")
                    )
                    demo_objects.append(d_obj)
                    demo_dict[v_code] = row
            db.bulk_save_objects(demo_objects)
            db.commit()
            print(f"[OK] Ingested {len(demo_objects)} demographic & infrastructure records.")

        # 5. Load 03 Health Facility Master
        fac_path = os.path.join(datasets_dir, "03_karnataka_health_facility_master.csv")
        if os.path.exists(fac_path):
            with open(fac_path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                fac_objects = [
                    HealthFacility(
                        facility_id=row.get("facility_id"),
                        facility_name=row.get("facility_name"),
                        facility_type=row.get("facility_type"),
                        sub_centre_or_phc_or_chc=row.get("sub_centre_or_phc_or_chc"),
                        district_code=parse_int(row.get("district_code")),
                        taluk_code=parse_int(row.get("taluk_code")),
                        village_code=parse_int(row.get("village_code")),
                        latitude=parse_float(row.get("latitude")),
                        longitude=parse_float(row.get("longitude")),
                        beds=parse_int(row.get("beds")),
                        doctors_sanctioned=parse_int(row.get("doctors_sanctioned")),
                        doctors_in_position=parse_int(row.get("doctors_in_position")),
                        nurses_sanctioned=parse_int(row.get("nurses_sanctioned")),
                        nurses_in_position=parse_int(row.get("nurses_in_position")),
                        anm_available=parse_int(row.get("anm_available")),
                        facility_status=row.get("facility_status", "FUNCTIONAL"),
                        source=row.get("source"),
                        source_date=row.get("source_date"),
                        source_url=row.get("source_url")
                    )
                    for row in reader
                ]
            db.bulk_save_objects(fac_objects)
            db.commit()
            print(f"[OK] Ingested {len(fac_objects)} health facility records.")

        # 6. Load 04 Health Service Utilization
        util_path = os.path.join(datasets_dir, "04_karnataka_health_service_utilization.csv")
        util_dict = {}
        if os.path.exists(util_path):
            with open(util_path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                util_objects = []
                for row in reader:
                    f_id = row.get("facility_id")
                    u_obj = HealthServiceUtilization(
                        facility_id=f_id,
                        village_code=parse_int(row.get("village_code")),
                        district_code=parse_int(row.get("district_code")),
                        taluk_code=parse_int(row.get("taluk_code")),
                        reporting_period=row.get("reporting_period"),
                        opd=parse_int(row.get("opd")),
                        ipd=parse_int(row.get("ipd")),
                        anc_visits=parse_int(row.get("anc_visits")),
                        pnc_visits=parse_int(row.get("pnc_visits")),
                        institutional_deliveries=parse_int(row.get("institutional_deliveries")),
                        immunization_sessions=parse_int(row.get("immunization_sessions")),
                        children_immunized=parse_int(row.get("children_immunized")),
                        high_risk_pregnancies=parse_int(row.get("high_risk_pregnancies")),
                        referrals=parse_int(row.get("referrals")),
                        outreach_sessions=parse_int(row.get("outreach_sessions")),
                        source=row.get("source"),
                        source_date=row.get("source_date"),
                        source_url=row.get("source_url"),
                        geographic_granularity=row.get("geographic_granularity")
                    )
                    util_objects.append(u_obj)
                    util_dict[f_id] = row
            db.bulk_save_objects(util_objects)
            db.commit()
            print(f"[OK] Ingested {len(util_objects)} health service utilization records.")

        # 7. Load 05 Health Indicators
        ind_path = os.path.join(datasets_dir, "05_karnataka_health_indicators.csv")
        ind_dict = {}
        if os.path.exists(ind_path):
            with open(ind_path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                ind_objects = []
                for row in reader:
                    d_code = parse_int(row.get("district_code"))
                    i_obj = HealthIndicators(
                        geographic_level=row.get("geographic_level"),
                        geographic_code=parse_int(row.get("geographic_code")),
                        geographic_name=row.get("geographic_name"),
                        district_code=d_code,
                        reporting_period=row.get("reporting_period"),
                        immunization_coverage=parse_float(row.get("immunization_coverage")),
                        anc_coverage=parse_float(row.get("anc_coverage")),
                        institutional_delivery=parse_float(row.get("institutional_delivery")),
                        maternal_health_indicators=row.get("maternal_health_indicators"),
                        child_health_indicators=row.get("child_health_indicators"),
                        nutrition_indicators=row.get("nutrition_indicators"),
                        mortality_indicators=row.get("mortality_indicators"),
                        disease_indicators=row.get("disease_indicators"),
                        source=row.get("source"),
                        source_year=parse_int(row.get("source_year")),
                        source_url=row.get("source_url")
                    )
                    ind_objects.append(i_obj)
                    ind_dict[d_code] = row
            db.bulk_save_objects(ind_objects)
            db.commit()
            print(f"[OK] Ingested {len(ind_objects)} district health indicator records.")

        # 8. Load 06 Anganwadi Nutrition
        ang_path = os.path.join(datasets_dir, "06_karnataka_anganwadi_nutrition.csv")
        ang_dict = {}
        if os.path.exists(ang_path):
            with open(ang_path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                ang_objects = []
                for row in reader:
                    v_code = parse_int(row.get("village_code"))
                    a_obj = AnganwadiNutrition(
                        anganwadi_id=row.get("anganwadi_id"),
                        anganwadi_name=row.get("anganwadi_name"),
                        village_code=v_code,
                        district_code=parse_int(row.get("district_code")),
                        taluk_code=parse_int(row.get("taluk_code")),
                        children_registered=parse_int(row.get("children_registered")),
                        children_screened=parse_int(row.get("children_screened")),
                        sam_cases=parse_int(row.get("sam_cases")),
                        mam_cases=parse_int(row.get("mam_cases")),
                        malnutrition_cases=parse_int(row.get("malnutrition_cases")),
                        nutrition_services=row.get("nutrition_services"),
                        medicine_availability=row.get("medicine_availability"),
                        drinking_water=row.get("drinking_water"),
                        toilet_availability=row.get("toilet_availability"),
                        worker_available=row.get("worker_available"),
                        helper_available=row.get("helper_available"),
                        doctor_visit=row.get("doctor_visit"),
                        last_inspection_date=row.get("last_inspection_date"),
                        source=row.get("source"),
                        source_date=row.get("source_date"),
                        source_url=row.get("source_url")
                    )
                    ang_objects.append(a_obj)
                    ang_dict[v_code] = row
            db.bulk_save_objects(ang_objects)
            db.commit()
            print(f"[OK] Ingested {len(ang_objects)} Anganwadi nutrition records.")

        # 9. Load 07 Weather Hazard
        wx_path = os.path.join(datasets_dir, "07_karnataka_weather_hazard_realtime.csv")
        wx_dict = {}
        if os.path.exists(wx_path):
            with open(wx_path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                wx_objects = []
                for row in reader:
                    d_code = parse_int(row.get("district_code"))
                    w_obj = WeatherHazard(
                        timestamp=row.get("timestamp"),
                        district_code=d_code,
                        district_name=row.get("district_name"),
                        taluk_code=parse_int(row.get("taluk_code")),
                        taluk_name=row.get("taluk_name"),
                        weather_station_id=row.get("weather_station_id"),
                        latitude=parse_float(row.get("latitude")),
                        longitude=parse_float(row.get("longitude")),
                        rainfall=parse_float(row.get("rainfall")),
                        temperature=parse_float(row.get("temperature")),
                        humidity=parse_float(row.get("humidity")),
                        wind_speed=parse_float(row.get("wind_speed")),
                        weather_warning=row.get("weather_warning"),
                        heavy_rainfall_warning=row.get("heavy_rainfall_warning"),
                        forecast_rainfall=parse_float(row.get("forecast_rainfall")),
                        forecast_date=row.get("forecast_date"),
                        source=row.get("source"),
                        source_url=row.get("source_url"),
                        retrieval_timestamp=row.get("retrieval_timestamp")
                    )
                    wx_objects.append(w_obj)
                    wx_dict[d_code] = row
            db.bulk_save_objects(wx_objects)
            db.commit()
            print(f"[OK] Ingested {len(wx_objects)} weather hazard records.")

        # 10. Load 08 Geospatial Accessibility
        acc_path = os.path.join(datasets_dir, "08_karnataka_village_health_accessibility.csv")
        acc_dict = {}
        if os.path.exists(acc_path):
            with open(acc_path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                acc_objects = []
                for row in reader:
                    v_code = parse_int(row.get("village_code"))
                    ac_obj = VillageAccessibility(
                        village_code=v_code,
                        nearest_phc_id=row.get("nearest_phc_id"),
                        nearest_chc_id=row.get("nearest_chc_id"),
                        distance_to_phc_km=parse_float(row.get("distance_to_phc_km")),
                        travel_time_to_phc_minutes=parse_float(row.get("travel_time_to_phc_minutes")),
                        distance_to_chc_km=parse_float(row.get("distance_to_chc_km")),
                        travel_time_to_chc_minutes=parse_float(row.get("travel_time_to_chc_minutes")),
                        road_type=row.get("road_type"),
                        road_accessibility=row.get("road_accessibility"),
                        flood_prone_indicator=row.get("flood_prone_indicator"),
                        elevation=parse_float(row.get("elevation")),
                        river_crossing_risk=row.get("river_crossing_risk"),
                        source=row.get("source"),
                        calculation_method=row.get("calculation_method"),
                        calculation_date=row.get("calculation_date")
                    )
                    acc_objects.append(ac_obj)
                    acc_dict[v_code] = row
            db.bulk_save_objects(acc_objects)
            db.commit()
            print(f"[OK] Ingested {len(acc_objects)} GIS accessibility records.")

        # 11. Load 09 Operational Resources & 10 MMU Operations (Protected datasets)
        res_path = os.path.join(datasets_dir, "09_karnataka_health_operational_resources.csv")
        if os.path.exists(res_path):
            with open(res_path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                res_objects = [
                    OperationalResources(
                        facility_id=row.get("facility_id"),
                        village_code=parse_int(row.get("village_code")),
                        timestamp=row.get("timestamp"),
                        vaccine_name=row.get("vaccine_name"),
                        vaccine_stock=row.get("vaccine_stock"),
                        vaccine_stock_days=row.get("vaccine_stock_days"),
                        ifa_stock=row.get("ifa_stock"),
                        ifa_stock_days=row.get("ifa_stock_days"),
                        essential_medicine_stock=row.get("essential_medicine_stock"),
                        medicine_stock_days=row.get("medicine_stock_days"),
                        doctor_available=row.get("doctor_available"),
                        nurse_available=row.get("nurse_available"),
                        anm_available=row.get("anm_available"),
                        source=row.get("source"),
                        data_status=row.get("data_status")
                    )
                    for row in reader
                ]
            db.bulk_save_objects(res_objects)
            db.commit()
            print(f"[OK] Ingested {len(res_objects)} operational resource records (Protected status).")

        mmu_path = os.path.join(datasets_dir, "10_karnataka_mmu_operations.csv")
        if os.path.exists(mmu_path):
            with open(mmu_path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                mmu_objects = [
                    MMUOperation(
                        mmu_id=row.get("mmu_id"),
                        mmu_name=row.get("mmu_name"),
                        district_code=parse_int(row.get("district_code")),
                        taluk_code=parse_int(row.get("taluk_code")),
                        current_latitude=row.get("current_latitude"),
                        current_longitude=row.get("current_longitude"),
                        timestamp=row.get("timestamp"),
                        status="AVAILABLE" if "AVAILABLE" in str(row.get("status")) else "ASSIGNED",
                        vehicle_status="OPERATIONAL",
                        assigned_area=row.get("assigned_area"),
                        current_mission=row.get("current_mission"),
                        available_from=row.get("available_from"),
                        patients_served=row.get("patients_served"),
                        last_service_date=row.get("last_service_date"),
                        source=row.get("source"),
                        data_status=row.get("data_status")
                    )
                    for row in reader
                ]
            db.bulk_save_objects(mmu_objects)
            db.commit()
            print(f"[OK] Ingested {len(mmu_objects)} MMU operational fleet records.")

        # 12. Load 11 Data Availability Matrix
        matrix_path = os.path.join(datasets_dir, "11_karnataka_health_data_availability_matrix.csv")
        if os.path.exists(matrix_path):
            with open(matrix_path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                matrix_objects = [
                    DataAvailabilityMatrix(
                        dataset=row.get("dataset"),
                        field=row.get("field"),
                        source_organization=row.get("source_organization"),
                        source_name=row.get("source_name"),
                        source_url=row.get("source_url"),
                        geographic_granularity=row.get("geographic_granularity"),
                        temporal_granularity=row.get("temporal_granularity"),
                        update_frequency=row.get("update_frequency"),
                        historical_coverage=row.get("historical_coverage"),
                        real_time_available=row.get("real_time_available"),
                        publicly_accessible=row.get("publicly_accessible"),
                        api_available=row.get("api_available"),
                        download_available=row.get("download_available"),
                        license=row.get("license"),
                        data_quality_notes=row.get("data_quality_notes"),
                        missingness=row.get("missingness"),
                        access_requirements=row.get("access_requirements")
                    )
                    for row in reader
                ]
            db.bulk_save_objects(matrix_objects)
            db.commit()
            print(f"[OK] Ingested {len(matrix_objects)} data availability matrix records.")

        # 13. Run AI Vulnerability Scoring Core for all Villages
        print("\n--- Running AI Vulnerability Scoring & SHAP Explainer Core ---")
        villages = db.query(LGDVillage).all()
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

            # Generate AI Recommendations for High/Critical Risk Villages
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

            # Generate System Alerts for Critical Villages or Flood Risks
            if score >= 65.0 or "HIGH" in str(ac_row.get("flood_prone_indicator", "")).upper():
                alerts_to_create.append(Alert(
                    village_code=v_code,
                    district_code=d_code,
                    alert_type="HIGH_VULNERABILITY_SPIKE" if score >= 75.0 else "FLOOD_HAZARD_ALERT",
                    title=f"High Risk Alert: {v.village_name} ({v.taluk_name})",
                    description=f"Village {v.village_name} scored {score}/100 ({risk_lvl}). Primary driver: Travel time to PHC ({ac_row.get('travel_time_to_phc_minutes', 30)} min) and severe care accessibility deficit.",
                    severity="CRITICAL" if score >= 80.0 else "HIGH",
                    status="OPEN",
                    recommended_action="Deploy MMU and initiate emergency maternal/child health screening."
                ))

        db.bulk_save_objects(score_objects)
        db.commit()
        print(f"[OK] Computed vulnerability scores & SHAP factor breakdowns for {len(score_objects)} villages.")

        if recommendations_to_create:
            db.bulk_save_objects(recommendations_to_create[:250])  # Save initial top recommendations
            db.commit()
            print(f"[OK] Generated {len(recommendations_to_create[:250])} actionable AI recommendations for health administrators.")

        if alerts_to_create:
            db.bulk_save_objects(alerts_to_create[:100])
            db.commit()
            print(f"[OK] Generated {len(alerts_to_create[:100])} critical health & hazard alerts.")

        # Seed initial MMU Missions
        initial_missions = [
            MMUMission(
                mmu_id="KA-MMU-524-01",
                village_code=598623,
                mission_name="Hanamaneri Inam Vulnerability Relief & Screening Mission",
                scheduled_date="2026-09-14",
                status="ASSIGNED",
                priority="CRITICAL",
                beneficiaries_targeted=85,
                assigned_by="Dr. Vijaykumar Patil (DHO Bagalkote)"
            ),
            MMUMission(
                mmu_id="KA-MMU-524-01",
                village_code=598625,
                mission_name="Karadigudd S.A. Maternal & Pediatric Health Outreach",
                scheduled_date="2026-09-16",
                status="ASSIGNED",
                priority="HIGH",
                beneficiaries_targeted=60,
                assigned_by="Dr. Vijaykumar Patil (DHO Bagalkote)"
            )
        ]
        db.bulk_save_objects(initial_missions)
        db.commit()
        print("[OK] Created initial MMU mission assignments.")

        # Initial Audit Log entry
        AuditLogger.log_action(
            db=db,
            user_id="SYSTEM",
            user_role="SYS_ADMIN",
            action="DATABASE_INIT_AND_INGESTION",
            resource="LGD_MASTER_DATASETS",
            details={"status": "SUCCESS", "total_villages": len(lgd_records)}
        )
        print("[OK] Created genesis tamper-resistant audit log entry.")

        print("\n=== DATASET SEEDING & INGESTION COMPLETE ===")

    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
