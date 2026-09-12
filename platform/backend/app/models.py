from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Text, DateTime, JSON
from sqlalchemy.orm import relationship

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="district_health_officer")
    district_code = Column(Integer, nullable=True)
    locale = Column(String, default="en_IN")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    is_deleted = Column(Boolean, default=False)


class District(Base):
    __tablename__ = "districts"

    id = Column(Integer, primary_key=True, index=True)
    district_code = Column(Integer, unique=True, index=True, nullable=False)
    district_name = Column(String, nullable=False)
    state_code = Column(Integer, default=29)
    state_name = Column(String, default="Karnataka")
    total_villages = Column(Integer, default=0)
    total_population = Column(Integer, default=0)


class Taluk(Base):
    __tablename__ = "taluks"

    id = Column(Integer, primary_key=True, index=True)
    subdistrict_code = Column(Integer, unique=True, index=True, nullable=False)
    subdistrict_name = Column(String, nullable=False)
    district_code = Column(Integer, ForeignKey("districts.district_code"), nullable=False)


class Village(Base):
    __tablename__ = "villages"

    id = Column(Integer, primary_key=True, index=True)
    village_code = Column(Integer, unique=True, index=True, nullable=False)
    village_name = Column(String, nullable=False)
    subdistrict_code = Column(Integer, nullable=False)
    subdistrict_name = Column(String, nullable=False)
    district_code = Column(Integer, nullable=False)
    district_name = Column(String, nullable=False)
    population = Column(Integer, default=0)
    households = Column(Integer, default=0)
    risk_score = Column(Float, default=0.0)
    risk_category = Column(String, default="LOW")
    distance_to_phc_km = Column(Float, default=0.0)
    travel_time_to_phc_minutes = Column(Float, default=0.0)
    road_accessibility = Column(String, default="ALL_WEATHER")
    flood_prone_indicator = Column(String, default="LOW")
    water_quality_index = Column(Float, default=80.0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)


class Facility(Base):
    __tablename__ = "facilities"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(String, unique=True, index=True, nullable=False)
    facility_name = Column(String, nullable=False)
    facility_type = Column(String, nullable=False)
    district_code = Column(Integer, nullable=False)
    district_name = Column(String, nullable=False)
    taluk_name = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    bed_capacity = Column(Integer, default=10)
    doctor_count = Column(Integer, default=2)
    nurse_count = Column(Integer, default=5)
    operational_status = Column(String, default="OPERATIONAL")


class Anganwadi(Base):
    __tablename__ = "anganwadis"

    id = Column(Integer, primary_key=True, index=True)
    center_code = Column(String, unique=True, index=True, nullable=False)
    center_name = Column(String, nullable=False)
    village_code = Column(Integer, nullable=False)
    children_enrolled = Column(Integer, default=0)
    severely_malnourished_count = Column(Integer, default=0)


class WeatherHazard(Base):
    __tablename__ = "weather_hazards"

    id = Column(Integer, primary_key=True, index=True)
    district_code = Column(Integer, nullable=False)
    rainfall_mm = Column(Float, default=0.0)
    flood_alert_level = Column(String, default="GREEN")
    recorded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class OperationalResource(Base):
    __tablename__ = "operational_resources"

    id = Column(Integer, primary_key=True, index=True)
    district_code = Column(Integer, nullable=False)
    mmu_available = Column(Integer, default=1)
    mmu_active = Column(Integer, default=1)
    ambulance_count = Column(Integer, default=2)


class MMU(Base):
    __tablename__ = "mmus"

    id = Column(Integer, primary_key=True, index=True)
    mmu_code = Column(String, unique=True, index=True, nullable=False)
    vehicle_registration = Column(String, nullable=False)
    district_code = Column(Integer, nullable=False)
    district_name = Column(String, nullable=False)
    current_assigned_village_code = Column(Integer, nullable=True)
    status = Column(String, default="AVAILABLE")
    last_camp_date = Column(DateTime, nullable=True)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    alert_level = Column(String, default="WARNING")
    district_code = Column(Integer, nullable=True)
    village_code = Column(Integer, nullable=True)
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, nullable=True)
    user_role = Column(String, nullable=True)
    action = Column(String, nullable=False)
    resource = Column(String, nullable=False)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DataSource(Base):
    __tablename__ = "data_sources"

    id = Column(Integer, primary_key=True, index=True)
    source_name = Column(String, nullable=False)
    layer_number = Column(Integer, nullable=False)
    record_count = Column(Integer, default=0)
    status = Column(String, default="ACTIVE")
    last_synced = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class IngestionRun(Base):
    __tablename__ = "ingestion_runs"

    id = Column(Integer, primary_key=True, index=True)
    source_name = Column(String, nullable=False)
    records_ingested = Column(Integer, default=0)
    status = Column(String, default="SUCCESS")
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DataQualityIssue(Base):
    __tablename__ = "data_quality_issues"

    id = Column(Integer, primary_key=True, index=True)
    table_name = Column(String, nullable=False)
    issue_description = Column(String, nullable=False)
    severity = Column(String, default="LOW")
    detected_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class ModelConfig(Base):
    __tablename__ = "model_configs"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, nullable=False)
    version = Column(String, default="v1.0")
    parameters = Column(JSON, nullable=True)


class FieldObservation(Base):
    __tablename__ = "field_observations"

    id = Column(Integer, primary_key=True, index=True)
    village_code = Column(Integer, nullable=False)
    observer_name = Column(String, nullable=False)
    notes = Column(Text, nullable=False)
    observed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class RiskSnapshot(Base):
    __tablename__ = "risk_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    village_code = Column(Integer, nullable=False)
    risk_score = Column(Float, nullable=False)
    risk_category = Column(String, nullable=False)
    snapshot_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DistrictHealthIndicator(Base):
    __tablename__ = "district_health_indicators"

    id = Column(Integer, primary_key=True, index=True)
    district_code = Column(Integer, nullable=False)
    mmr = Column(Float, default=85.0)
    imr = Column(Float, default=20.0)
    anc_coverage_pct = Column(Float, default=78.5)


class ServiceUtilization(Base):
    __tablename__ = "service_utilization"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(String, nullable=False)
    outpatient_count = Column(Integer, default=0)
    inpatient_count = Column(Integer, default=0)
    month_year = Column(String, nullable=False)


class Mission(Base):
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True, index=True)
    mission_code = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    assigned_mmu_code = Column(String, nullable=True)
    target_village_code = Column(Integer, nullable=False)
    status = Column(String, default="SCHEDULED")
    scheduled_date = Column(DateTime, nullable=False)


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    village_code = Column(Integer, nullable=False)
    intervention_type = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(String, default="HIGH")
    status = Column(String, default="PENDING")
