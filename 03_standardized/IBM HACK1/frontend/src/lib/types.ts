export type UserRole = "STATE_ADMIN" | "DHO" | "MMU_COORDINATOR" | "SYS_ADMIN";

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: UserRole;
  district_code?: number;
  taluk_code?: number;
}

export interface ExecutiveKPIs {
  total_villages: number;
  critical_villages: number;
  high_risk_villages: number;
  medium_risk_villages: number;
  low_risk_villages: number;
  active_mmus: number;
  pending_deployments: number;
  open_alerts: number;
  avg_vulnerability_score: number;
}

export interface DistrictSummary {
  district_code: number;
  district_name: string;
  total_villages: number;
  high_risk_villages: number;
  medium_risk_villages: number;
  low_risk_villages: number;
  avg_vulnerability_score: number;
}

export interface TalukSummary {
  taluk_code: number;
  taluk_name: string;
  district_code: number;
  total_villages: number;
  high_risk_villages: number;
  avg_vulnerability_score: number;
}

export interface VillageListItem {
  village_code: number;
  village_name: string;
  district_code: number;
  district_name: string;
  taluk_code: number;
  taluk_name: string;
  population: number;
  vulnerability_score: number;
  risk_level: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";
  latitude?: number;
  longitude?: number;
}

export interface SHAPFactor {
  factor_name: string;
  impact_points: number;
  explanation: string;
}

export interface VillageProfile {
  village_code: number;
  village_name: string;
  district_code: number;
  district_name: string;
  taluk_code: number;
  taluk_name: string;
  gram_panchayat_name?: string;
  latitude?: number;
  longitude?: number;
  population: number;
  children_under_5: number;
  elderly_population: number;
  literacy_rate: number;
  road_access: string;
  drinking_water_access: string;
  electricity_access: string;
  telecom_connectivity: string;
  vulnerability_score: number;
  risk_level: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";
  predicted_score_7d: number;
  subscores: Record<string, number>;
  top_contributing_factors: SHAPFactor[];
  nearest_phc_name: string;
  distance_to_phc_km: number;
  travel_time_to_phc_minutes: number;
  flood_prone_indicator: string;
  provenance_classification: string;
}

export interface AIRecommendation {
  id: number;
  village_code: number;
  village_name?: string;
  district_code?: number;
  action: string;
  reason: string;
  priority: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";
  expected_impact?: string;
  required_resources?: string;
  suggested_deadline?: string;
  confidence: number;
  status: "PENDING_REVIEW" | "APPROVED" | "REJECTED" | "MODIFIED" | "DISPATCHED" | "COMPLETED";
  approved_by?: string;
  approved_at?: string;
  rejection_reason?: string;
}

export interface MMUOperation {
  id: number;
  mmu_id: string;
  mmu_name: string;
  district_code: number;
  taluk_code: number;
  status: string;
  assigned_area?: string;
  available_from?: string;
  data_status: string;
}

export interface MMUMission {
  id: number;
  mmu_id: string;
  village_code: number;
  village_name?: string;
  mission_name: string;
  scheduled_date: string;
  status: string;
  priority: string;
  beneficiaries_targeted: number;
  beneficiaries_served: number;
  clinical_notes?: string;
  assigned_by: string;
  created_at: string;
  completed_at?: string;
}

export interface Alert {
  id: number;
  village_code?: number;
  village_name?: string;
  district_code: number;
  district_name?: string;
  alert_type: string;
  title: string;
  description: string;
  severity: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";
  status: "OPEN" | "ACKNOWLEDGED" | "ASSIGNED" | "RESOLVED" | "ESCALATED";
  assigned_to?: string;
  recommended_action?: string;
  created_at: string;
}

export interface DataAvailabilityItem {
  id: number;
  dataset: string;
  field: string;
  source_organization?: string;
  source_name?: string;
  geographic_granularity?: string;
  temporal_granularity?: string;
  publicly_accessible?: string;
  missingness?: string;
  access_requirements?: string;
}

export interface AuditLogItem {
  id: number;
  timestamp: string;
  user_id: string;
  user_role: string;
  action: string;
  resource: string;
  details: string;
  prev_hash: string;
  log_hash: string;
}
