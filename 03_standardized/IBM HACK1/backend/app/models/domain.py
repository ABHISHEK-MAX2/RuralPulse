from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, nullable=False)  # STATE_ADMIN, DHO, MMU_COORDINATOR, SYS_ADMIN
    district_code = Column(Integer, nullable=True)  # Null for STATE_ADMIN / SYS_ADMIN
    taluk_code = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class LGDVillage(Base):
    __tablename__ = "lgd_villages"
    village_code = Column(Integer, primary_key=True, index=True)
    village_name = Column(String, index=True, nullable=False)
    state_code = Column(Integer, default=29)
    state_name = Column(String, default="Karnataka")
    district_code = Column(Integer, index=True, nullable=False)
    district_name = Column(String, index=True, nullable=False)
    taluk_code = Column(Integer, index=True, nullable=False)
    taluk_name = Column(String, index=True, nullable=False)
    gram_panchayat_code = Column(Integer, nullable=True)
    gram_panchayat_name = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    source = Column(String, nullable=True)
    source_url = Column(String, nullable=True)
    retrieval_date = Column(String, nullable=True)
    record_status = Column(String, default="ACTIVE")

class VillageDemographics(Base):
    __tablename__ = "village_demographics"
    village_code = Column(Integer, primary_key=True, index=True)
    population = Column(Integer, default=0)
    male_population = Column(Integer, default=0)
    female_population = Column(Integer, default=0)
    children_under_5 = Column(Integer, default=0)
    elderly_population = Column(Integer, default=0)
    households = Column(Integer, default=0)
    literacy_rate = Column(Float, default=0.0)
    drinking_water_access = Column(String, nullable=True)
    electricity_access = Column(String, nullable=True)
    road_access = Column(String, nullable=True)
    telecom_connectivity = Column(String, nullable=True)
    internet_connectivity = Column(String, nullable=True)
    source = Column(String, nullable=True)
    source_year = Column(Integer, nullable=True)
    geographic_granularity = Column(String, nullable=True)
    source_url = Column(String, nullable=True)

class HealthFacility(Base):
    __tablename__ = "health_facilities"
    facility_id = Column(String, primary_key=True, index=True)
    facility_name = Column(String, index=True, nullable=False)
    facility_type = Column(String, index=True, nullable=False)
    sub_centre_or_phc_or_chc = Column(String, nullable=True)
    district_code = Column(Integer, index=True, nullable=False)
    taluk_code = Column(Integer, index=True, nullable=False)
    village_code = Column(Integer, index=True, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    beds = Column(Integer, default=0)
    doctors_sanctioned = Column(Integer, default=0)
    doctors_in_position = Column(Integer, default=0)
    nurses_sanctioned = Column(Integer, default=0)
    nurses_in_position = Column(Integer, default=0)
    anm_available = Column(Integer, default=0)
    facility_status = Column(String, default="FUNCTIONAL")
    source = Column(String, nullable=True)
    source_date = Column(String, nullable=True)
    source_url = Column(String, nullable=True)

class HealthServiceUtilization(Base):
    __tablename__ = "health_service_utilization"
    id = Column(Integer, primary_key=True, autoincrement=True)
    facility_id = Column(String, index=True, nullable=False)
    village_code = Column(Integer, index=True, nullable=True)
    district_code = Column(Integer, index=True, nullable=False)
    taluk_code = Column(Integer, index=True, nullable=False)
    reporting_period = Column(String, nullable=False)
    opd = Column(Integer, default=0)
    ipd = Column(Integer, default=0)
    anc_visits = Column(Integer, default=0)
    pnc_visits = Column(Integer, default=0)
    institutional_deliveries = Column(Integer, default=0)
    immunization_sessions = Column(Integer, default=0)
    children_immunized = Column(Integer, default=0)
    high_risk_pregnancies = Column(Integer, default=0)
    referrals = Column(Integer, default=0)
    outreach_sessions = Column(Integer, default=0)
    source = Column(String, nullable=True)
    source_date = Column(String, nullable=True)
    source_url = Column(String, nullable=True)
    geographic_granularity = Column(String, nullable=True)

class HealthIndicators(Base):
    __tablename__ = "health_indicators"
    id = Column(Integer, primary_key=True, autoincrement=True)
    geographic_level = Column(String, nullable=False)
    geographic_code = Column(Integer, index=True, nullable=False)
    geographic_name = Column(String, index=True, nullable=False)
    district_code = Column(Integer, index=True, nullable=False)
    reporting_period = Column(String, nullable=False)
    immunization_coverage = Column(Float, default=0.0)
    anc_coverage = Column(Float, default=0.0)
    institutional_delivery = Column(Float, default=0.0)
    maternal_health_indicators = Column(Text, nullable=True)  # JSON String
    child_health_indicators = Column(Text, nullable=True)     # JSON String
    nutrition_indicators = Column(Text, nullable=True)        # JSON String
    mortality_indicators = Column(Text, nullable=True)        # JSON String
    disease_indicators = Column(Text, nullable=True)          # JSON String
    source = Column(String, nullable=True)
    source_year = Column(Integer, nullable=True)
    source_url = Column(String, nullable=True)

class AnganwadiNutrition(Base):
    __tablename__ = "anganwadi_nutrition"
    anganwadi_id = Column(String, primary_key=True, index=True)
    anganwadi_name = Column(String, nullable=False)
    village_code = Column(Integer, index=True, nullable=False)
    district_code = Column(Integer, index=True, nullable=False)
    taluk_code = Column(Integer, index=True, nullable=False)
    children_registered = Column(Integer, default=0)
    children_screened = Column(Integer, default=0)
    sam_cases = Column(Integer, default=0)
    mam_cases = Column(Integer, default=0)
    malnutrition_cases = Column(Integer, default=0)
    nutrition_services = Column(String, nullable=True)
    medicine_availability = Column(String, nullable=True)
    drinking_water = Column(String, nullable=True)
    toilet_availability = Column(String, nullable=True)
    worker_available = Column(String, nullable=True)
    helper_available = Column(String, nullable=True)
    doctor_visit = Column(String, nullable=True)
    last_inspection_date = Column(String, nullable=True)
    source = Column(String, nullable=True)
    source_date = Column(String, nullable=True)
    source_url = Column(String, nullable=True)

class WeatherHazard(Base):
    __tablename__ = "weather_hazards"
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(String, nullable=False)
    district_code = Column(Integer, index=True, nullable=False)
    district_name = Column(String, nullable=False)
    taluk_code = Column(Integer, index=True, nullable=False)
    taluk_name = Column(String, nullable=False)
    weather_station_id = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    rainfall = Column(Float, default=0.0)
    temperature = Column(Float, default=0.0)
    humidity = Column(Float, default=0.0)
    wind_speed = Column(Float, default=0.0)
    weather_warning = Column(String, default="NONE")
    heavy_rainfall_warning = Column(String, default="NO")
    forecast_rainfall = Column(Float, default=0.0)
    forecast_date = Column(String, nullable=True)
    source = Column(String, nullable=True)
    source_url = Column(String, nullable=True)
    retrieval_timestamp = Column(String, nullable=True)

class VillageAccessibility(Base):
    __tablename__ = "village_accessibility"
    village_code = Column(Integer, primary_key=True, index=True)
    nearest_phc_id = Column(String, nullable=True)
    nearest_chc_id = Column(String, nullable=True)
    distance_to_phc_km = Column(Float, default=0.0)
    travel_time_to_phc_minutes = Column(Float, default=0.0)
    distance_to_chc_km = Column(Float, default=0.0)
    travel_time_to_chc_minutes = Column(Float, default=0.0)
    road_type = Column(String, nullable=True)
    road_accessibility = Column(String, default="ALL_WEATHER")
    flood_prone_indicator = Column(String, default="LOW")
    elevation = Column(Float, default=0.0)
    river_crossing_risk = Column(String, default="NONE")
    source = Column(String, nullable=True)
    calculation_method = Column(String, nullable=True)
    calculation_date = Column(String, nullable=True)

class OperationalResources(Base):
    __tablename__ = "operational_resources"
    id = Column(Integer, primary_key=True, autoincrement=True)
    facility_id = Column(String, index=True, nullable=False)
    village_code = Column(Integer, index=True, nullable=True)
    timestamp = Column(String, nullable=False)
    vaccine_name = Column(String, nullable=True)
    vaccine_stock = Column(String, nullable=True)
    vaccine_stock_days = Column(String, nullable=True)
    ifa_stock = Column(String, nullable=True)
    ifa_stock_days = Column(String, nullable=True)
    essential_medicine_stock = Column(String, nullable=True)
    medicine_stock_days = Column(String, nullable=True)
    doctor_available = Column(String, nullable=True)
    nurse_available = Column(String, nullable=True)
    anm_available = Column(String, nullable=True)
    source = Column(String, nullable=True)
    data_status = Column(String, nullable=True)

class MMUOperation(Base):
    __tablename__ = "mmu_operations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    mmu_id = Column(String, index=True, nullable=False)
    mmu_name = Column(String, nullable=False)
    district_code = Column(Integer, index=True, nullable=False)
    taluk_code = Column(Integer, index=True, nullable=False)
    current_latitude = Column(String, nullable=True)
    current_longitude = Column(String, nullable=True)
    timestamp = Column(String, nullable=False)
    status = Column(String, default="AVAILABLE")
    vehicle_status = Column(String, default="OPERATIONAL")
    assigned_area = Column(String, nullable=True)
    current_mission = Column(String, nullable=True)
    available_from = Column(String, nullable=True)
    patients_served = Column(String, nullable=True)
    last_service_date = Column(String, nullable=True)
    source = Column(String, nullable=True)
    data_status = Column(String, nullable=True)

class DataAvailabilityMatrix(Base):
    __tablename__ = "data_availability_matrix"
    id = Column(Integer, primary_key=True, autoincrement=True)
    dataset = Column(String, nullable=False)
    field = Column(String, nullable=False)
    source_organization = Column(String, nullable=True)
    source_name = Column(String, nullable=True)
    source_url = Column(String, nullable=True)
    geographic_granularity = Column(String, nullable=True)
    temporal_granularity = Column(String, nullable=True)
    update_frequency = Column(String, nullable=True)
    historical_coverage = Column(String, nullable=True)
    real_time_available = Column(String, nullable=True)
    publicly_accessible = Column(String, nullable=True)
    api_available = Column(String, nullable=True)
    download_available = Column(String, nullable=True)
    license = Column(String, nullable=True)
    data_quality_notes = Column(Text, nullable=True)
    missingness = Column(String, nullable=True)
    access_requirements = Column(Text, nullable=True)

class VulnerabilityScore(Base):
    __tablename__ = "vulnerability_scores"
    village_code = Column(Integer, primary_key=True, index=True)
    score = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)  # CRITICAL, HIGH, MEDIUM, LOW
    predicted_score_7d = Column(Float, nullable=True)
    healthcare_access_subscore = Column(Float, default=0.0)
    maternal_child_subscore = Column(Float, default=0.0)
    immunization_subscore = Column(Float, default=0.0)
    nutrition_subscore = Column(Float, default=0.0)
    infra_subscore = Column(Float, default=0.0)
    demographic_subscore = Column(Float, default=0.0)
    resource_subscore = Column(Float, default=0.0)
    environmental_subscore = Column(Float, default=0.0)
    utilization_subscore = Column(Float, default=0.0)
    trend_subscore = Column(Float, default=0.0)
    shap_json = Column(Text, nullable=True)
    top_contributing_factors_json = Column(Text, nullable=True)
    calculated_at = Column(DateTime, default=datetime.utcnow)

class AIRecommendation(Base):
    __tablename__ = "ai_recommendations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    village_code = Column(Integer, index=True, nullable=False)
    action = Column(String, nullable=False)
    reason = Column(Text, nullable=False)
    priority = Column(String, default="HIGH")  # CRITICAL, HIGH, MEDIUM, LOW
    expected_impact = Column(Text, nullable=True)
    required_resources = Column(Text, nullable=True)
    suggested_deadline = Column(String, nullable=True)
    confidence = Column(Float, default=0.85)
    supporting_indicators_json = Column(Text, nullable=True)
    status = Column(String, default="PENDING_REVIEW")  # PENDING_REVIEW, APPROVED, REJECTED, MODIFIED, DISPATCHED, COMPLETED
    approved_by = Column(String, nullable=True)
    approved_at = Column(DateTime, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class MMUMission(Base):
    __tablename__ = "mmu_missions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    mmu_id = Column(String, index=True, nullable=False)
    village_code = Column(Integer, index=True, nullable=False)
    mission_name = Column(String, nullable=False)
    scheduled_date = Column(String, nullable=False)
    status = Column(String, default="ASSIGNED")  # ASSIGNED, EN_ROUTE, ON_SITE, COMPLETED, CANCELLED
    priority = Column(String, default="HIGH")
    beneficiaries_targeted = Column(Integer, default=50)
    beneficiaries_served = Column(Integer, default=0)
    clinical_notes = Column(Text, nullable=True)
    assigned_by = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    village_code = Column(Integer, index=True, nullable=True)
    district_code = Column(Integer, index=True, nullable=False)
    alert_type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String, default="HIGH")  # CRITICAL, HIGH, MEDIUM, LOW
    status = Column(String, default="OPEN")  # OPEN, ACKNOWLEDGED, ASSIGNED, RESOLVED, ESCALATED
    assigned_to = Column(String, nullable=True)
    recommended_action = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    acknowledged_at = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String, nullable=False)
    user_role = Column(String, nullable=False)
    action = Column(String, nullable=False)
    resource = Column(String, nullable=False)
    details_json = Column(Text, nullable=True)
    prev_hash = Column(String, nullable=True)
    log_hash = Column(String, nullable=False)
