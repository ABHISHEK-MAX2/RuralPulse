export interface VillageData {
  village_code: number;
  village_name: string;
  subdistrict_code: number;
  subdistrict_name: string;
  district_code: number;
  district_name: string;
  population: number;
  risk_score: number;
  risk_category: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  distance_to_phc_km: number;
  travel_time_to_phc_minutes: number;
  road_accessibility: string;
  flood_prone_indicator: string;
  latitude?: number;
  longitude?: number;
}

export const MOCK_VILLAGES: VillageData[] = [
  { village_code: 607535, village_name: 'Honnalli Rural', subdistrict_code: 5501, subdistrict_name: 'Honnalli', district_code: 535, district_name: 'Davanagere', population: 4250, risk_score: 84.5, risk_category: 'CRITICAL', distance_to_phc_km: 18.5, travel_time_to_phc_minutes: 55.0, road_accessibility: 'SEASONAL_UNPAVED', flood_prone_indicator: 'HIGH', latitude: 14.44, longitude: 75.64 },
  { village_code: 607536, village_name: 'Nyamathi East', subdistrict_code: 5501, subdistrict_name: 'Honnalli', district_code: 535, district_name: 'Davanagere', population: 3100, risk_score: 76.2, risk_category: 'CRITICAL', distance_to_phc_km: 14.2, travel_time_to_phc_minutes: 42.0, road_accessibility: 'UNPAVED', flood_prone_indicator: 'MEDIUM', latitude: 14.25, longitude: 75.58 },
  { village_code: 607537, village_name: 'Harihara North', subdistrict_code: 5502, subdistrict_name: 'Harihara', district_code: 535, district_name: 'Davanagere', population: 5800, risk_score: 68.4, risk_category: 'HIGH', distance_to_phc_km: 11.0, travel_time_to_phc_minutes: 30.0, road_accessibility: 'ALL_WEATHER', flood_prone_indicator: 'LOW', latitude: 14.51, longitude: 75.80 },
  { village_code: 607538, village_name: 'Channagiri South', subdistrict_code: 5503, subdistrict_name: 'Channagiri', district_code: 535, district_name: 'Davanagere', population: 2900, risk_score: 52.1, risk_category: 'MEDIUM', distance_to_phc_km: 7.5, travel_time_to_phc_minutes: 20.0, road_accessibility: 'ALL_WEATHER', flood_prone_indicator: 'LOW', latitude: 14.02, longitude: 75.92 },
  { village_code: 607539, village_name: 'Jagalur West', subdistrict_code: 5504, subdistrict_name: 'Jagalur', district_code: 535, district_name: 'Davanagere', population: 1850, risk_score: 35.0, risk_category: 'LOW', distance_to_phc_km: 4.0, travel_time_to_phc_minutes: 12.0, road_accessibility: 'ALL_WEATHER', flood_prone_indicator: 'LOW', latitude: 14.52, longitude: 76.34 }
].sort((a, b) => b.risk_score - a.risk_score);

export const MOCK_DATA_AVAILABILITY = [
  { id: 1, name: 'LGD Administrative Master', code: 'LAYER_01', records: 30771, status: 'AVAILABLE' },
  { id: 2, name: 'Village Demographics & Infra', code: 'LAYER_02', records: 30771, status: 'AVAILABLE' },
  { id: 3, name: 'Health Facility Master', code: 'LAYER_03', records: 721, status: 'AVAILABLE' },
  { id: 4, name: 'Health Service Utilization', code: 'LAYER_04', records: 721, status: 'AVAILABLE' },
  { id: 5, name: 'Health Indicators', code: 'LAYER_05', records: 32, status: 'AVAILABLE' },
  { id: 6, name: 'Anganwadi Nutrition Data', code: 'LAYER_06', records: 481, status: 'AVAILABLE' },
  { id: 7, name: 'Weather Hazard Real-Time', code: 'LAYER_07', records: 32, status: 'AVAILABLE' },
  { id: 8, name: 'Village Accessibility Matrix', code: 'LAYER_08', records: 30771, status: 'AVAILABLE' },
  { id: 9, name: 'Operational Resources', code: 'LAYER_09', records: 21, status: 'AVAILABLE' },
  { id: 10, name: 'MMU Operations Log', code: 'LAYER_10', records: 11, status: 'AVAILABLE' },
  { id: 11, name: 'Health Data Availability Matrix', code: 'LAYER_11', records: 11, status: 'AVAILABLE' }
];
