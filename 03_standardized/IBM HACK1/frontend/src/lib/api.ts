import axios from "axios";
import {
  ExecutiveKPIs, DistrictSummary, TalukSummary, VillageListItem,
  VillageProfile, AIRecommendation, MMUOperation, MMUMission, Alert,
  DataAvailabilityItem, AuditLogItem
} from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8008/api/v1";

export const api = axios.create({
  baseURL: API_BASE,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

export const apiService = {
  // Auth
  login: async (email: string, password: string) => {
    const res = await api.post("/auth/login", { email, password });
    return res.data;
  },
  getMe: async () => {
    const res = await api.get("/auth/me");
    return res.data;
  },
  registerUser: async (userData: {
    email: string;
    password: string;
    full_name: string;
    role: string;
    district_code?: number;
  }) => {
    const res = await api.post("/auth/register", userData);
    return res.data;
  },
  listUsers: async () => {
    const res = await api.get("/auth/users");
    return res.data;
  },

  // Geography & Villages
  getDistricts: async (): Promise<DistrictSummary[]> => {
    const res = await api.get("/geography/districts");
    return res.data;
  },
  getTaluks: async (districtCode?: number): Promise<TalukSummary[]> => {
    const res = await api.get("/geography/taluks", { params: { district_code: districtCode } });
    return res.data;
  },
  getVillages: async (params?: {
    district_code?: number;
    taluk_code?: number;
    risk_level?: string;
    search?: string;
    min_score?: number;
    limit?: number;
    offset?: number;
  }): Promise<VillageListItem[]> => {
    const res = await api.get("/geography/villages", { params });
    return res.data;
  },
  getVillageProfile: async (villageCode: number): Promise<VillageProfile> => {
    const res = await api.get(`/geography/villages/${villageCode}`);
    return res.data;
  },

  // Health Facilities
  getFacilities: async (params?: { district_code?: number; taluk_code?: number; facility_type?: string }): Promise<any[]> => {
    const res = await api.get("/facilities", { params });
    return res.data;
  },

  // Vulnerability Intelligence & KPIs
  getKPIs: async (districtCode?: number): Promise<ExecutiveKPIs> => {
    const res = await api.get("/vulnerability/kpis", { params: { district_code: districtCode } });
    return res.data;
  },
  getGeoJSON: async (districtCode?: number) => {
    const res = await api.get("/vulnerability/geojson", { params: { district_code: districtCode } });
    return res.data;
  },

  // Recommendations
  getRecommendations: async (districtCode?: number, status?: string): Promise<AIRecommendation[]> => {
    const res = await api.get("/recommendations", { params: { district_code: districtCode, status } });
    return res.data;
  },
  reviewRecommendation: async (id: number, status: string, notes?: string) => {
    const res = await api.post(`/recommendations/${id}/review`, { status, notes });
    return res.data;
  },

  // MMU Fleet & Missions
  getMMUFleet: async (districtCode?: number): Promise<MMUOperation[]> => {
    const res = await api.get("/mmus", { params: { district_code: districtCode } });
    return res.data;
  },
  getMMUMissions: async (districtCode?: number): Promise<MMUMission[]> => {
    const res = await api.get("/mmus/missions", { params: { district_code: districtCode } });
    return res.data;
  },
  dispatchMMU: async (data: {
    mmu_id: string;
    village_code: number;
    mission_name: string;
    scheduled_date: string;
    priority?: string;
    beneficiaries_targeted?: number;
  }) => {
    const res = await api.post("/mmus/dispatch", data);
    return res.data;
  },

  // Intelligent Alerts
  getAlerts: async (districtCode?: number, status?: string, severity?: string): Promise<Alert[]> => {
    const res = await api.get("/alerts", { params: { district_code: districtCode, status, severity } });
    return res.data;
  },
  actionAlert: async (id: number, action: string, assignedTo?: string) => {
    const res = await api.post(`/alerts/${id}/action`, { action, assigned_to: assignedTo });
    return res.data;
  },

  // Reports
  generateReport: async (reportType: string, districtCode: number, format: string = "PDF") => {
    const res = await api.post("/reports/generate", { report_type: reportType, district_code: districtCode, format });
    return res.data;
  },

  // Data Sources & Quality Matrix
  getDataSources: async (): Promise<DataAvailabilityItem[]> => {
    const res = await api.get("/data-sources");
    return res.data;
  },
  triggerIngest: async (id: number) => {
    const res = await api.post(`/data-sources/${id}/trigger-ingest`);
    return res.data;
  },

  // Audit Logs
  getAuditLogs: async (): Promise<AuditLogItem[]> => {
    const res = await api.get("/audit/logs");
    return res.data;
  }
};
