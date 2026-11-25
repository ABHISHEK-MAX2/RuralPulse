from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# Token & Auth
class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    user_name: str
    district_code: Optional[int] = None

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None
    district_code: Optional[int] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class CreateUserRequest(BaseModel):
    email: str
    password: str
    full_name: str
    role: str
    district_code: Optional[int] = None
    taluk_code: Optional[int] = None

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    district_code: Optional[int] = None
    taluk_code: Optional[int] = None

# District / Taluk Summary
class DistrictSummary(BaseModel):
    district_code: int
    district_name: str
    total_villages: int
    high_risk_villages: int
    medium_risk_villages: int
    low_risk_villages: int
    avg_vulnerability_score: float

class TalukSummary(BaseModel):
    taluk_code: int
    taluk_name: str
    district_code: int
    total_villages: int
    high_risk_villages: int
    avg_vulnerability_score: float

# Village Profile & List
class VillageListItem(BaseModel):
    village_code: int
    village_name: str
    district_code: int
    district_name: str
    taluk_code: int
    taluk_name: str
    population: int
    vulnerability_score: float
    risk_level: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class VillageProfileResponse(BaseModel):
    village_code: int
    village_name: str
    district_code: int
    district_name: str
    taluk_code: int
    taluk_name: str
    gram_panchayat_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    population: int
    children_under_5: int
    elderly_population: int
    literacy_rate: float
    road_access: Optional[str] = None
    drinking_water_access: Optional[str] = None
    electricity_access: Optional[str] = None
    telecom_connectivity: Optional[str] = None
    vulnerability_score: float
    risk_level: str
    predicted_score_7d: Optional[float] = None
    subscores: Dict[str, float]
    top_contributing_factors: List[Dict[str, Any]]
    nearest_phc_name: Optional[str] = None
    distance_to_phc_km: Optional[float] = None
    travel_time_to_phc_minutes: Optional[float] = None
    flood_prone_indicator: Optional[str] = None
    provenance_classification: str = "REAL_SOURCE_DATA"

# Vulnerability & SHAP
class VulnerabilityDetail(BaseModel):
    village_code: int
    score: float
    risk_level: str
    predicted_score_7d: Optional[float] = None
    subscores: Dict[str, float]
    shap_factors: List[Dict[str, Any]]

# AI Recommendation & Approval
class RecommendationResponse(BaseModel):
    id: int
    village_code: int
    village_name: Optional[str] = None
    district_code: Optional[int] = None
    action: str
    reason: str
    priority: str
    expected_impact: Optional[str] = None
    required_resources: Optional[str] = None
    suggested_deadline: Optional[str] = None
    confidence: float
    status: str
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None

class RecommendationReviewRequest(BaseModel):
    status: str  # APPROVED, REJECTED, MODIFIED
    notes: Optional[str] = None

# MMU Operations & Missions
class MMUResponse(BaseModel):
    id: int
    mmu_id: str
    mmu_name: str
    district_code: int
    taluk_code: int
    status: str
    assigned_area: Optional[str] = None
    available_from: Optional[str] = None
    data_status: str

class MMUMissionCreateRequest(BaseModel):
    mmu_id: str
    village_code: int
    mission_name: str
    scheduled_date: str
    priority: str = "HIGH"
    beneficiaries_targeted: int = 50

class MMUMissionResponse(BaseModel):
    id: int
    mmu_id: str
    village_code: int
    village_name: Optional[str] = None
    mission_name: str
    scheduled_date: str
    status: str
    priority: str
    beneficiaries_targeted: int
    beneficiaries_served: int
    clinical_notes: Optional[str] = None
    assigned_by: str
    created_at: datetime
    completed_at: Optional[datetime] = None

# Alert
class AlertResponse(BaseModel):
    id: int
    village_code: Optional[int] = None
    village_name: Optional[str] = None
    district_code: int
    district_name: Optional[str] = None
    alert_type: str
    title: str
    description: str
    severity: str
    status: str
    assigned_to: Optional[str] = None
    recommended_action: Optional[str] = None
    created_at: datetime

class AlertActionRequest(BaseModel):
    action: str  # ACKNOWLEDGE, ASSIGN, RESOLVE, ESCALATE
    assigned_to: Optional[str] = None

# Data Quality & Ingestion
class DataAvailabilityItem(BaseModel):
    id: int
    dataset: str
    field: str
    source_organization: Optional[str] = None
    source_name: Optional[str] = None
    geographic_granularity: Optional[str] = None
    temporal_granularity: Optional[str] = None
    publicly_accessible: Optional[str] = None
    missingness: Optional[str] = None
    access_requirements: Optional[str] = None

# System KPIs & Overview
class ExecutiveKPIs(BaseModel):
    total_villages: int
    high_risk_villages: int
    medium_risk_villages: int
    low_risk_villages: int
    critical_villages: int
    active_mmus: int
    pending_deployments: int
    open_alerts: int
    avg_vulnerability_score: float
