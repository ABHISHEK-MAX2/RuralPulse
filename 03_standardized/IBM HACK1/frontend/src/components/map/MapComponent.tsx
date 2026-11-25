"use client";

import React, { useEffect, useState } from "react";
import { VulnerabilityBadge } from "../village/VulnerabilityBadge";

interface VillagePoint {
  village_code: number;
  village_name: string;
  district_name: string;
  taluk_name: string;
  latitude?: number;
  longitude?: number;
  vulnerability_score: number;
  risk_level: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";
}

interface Props {
  villages: VillagePoint[];
  activeLayerId?: string;
  onSelectVillage: (villageCode: number) => void;
}

export const MapComponent: React.FC<Props> = ({ villages, activeLayerId = "vulnerability", onSelectVillage }) => {
  const [mounted, setMounted] = useState(false);
  const [LeafletMap, setLeafletMap] = useState<any>(null);

  useEffect(() => {
    setMounted(true);
    // Dynamically load leaflet components only on client-side
    Promise.all([
      import("react-leaflet"),
      import("leaflet")
    ]).then(([ReactLeaflet, L]) => {
      // Fix default icon path
      delete (L.Icon.Default.prototype as any)._getIconUrl;
      L.Icon.Default.mergeOptions({
        iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
        iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
        shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
      });

      setLeafletMap({
        MapContainer: ReactLeaflet.MapContainer,
        TileLayer: ReactLeaflet.TileLayer,
        Circle: ReactLeaflet.Circle,
        Popup: ReactLeaflet.Popup,
      });
    });
  }, []);

  if (!mounted || !LeafletMap) {
    return (
      <div className="w-full h-[600px] bg-dark-card rounded-2xl flex items-center justify-center text-slate-400">
        <div className="text-center space-y-3">
          <div className="animate-spin w-8 h-8 border-4 border-brand-emerald border-t-transparent rounded-full mx-auto" />
          <p className="text-xs font-mono text-slate-300">Initializing GIS Map Engine...</p>
        </div>
      </div>
    );
  }

  const { MapContainer, TileLayer, Circle, Popup } = LeafletMap;

  const validVillages = villages.filter(v => v.latitude && v.longitude);
  const avgLat = validVillages.length > 0
    ? validVillages.reduce((acc, curr) => acc + (curr.latitude || 0), 0) / validVillages.length
    : 15.317;
  const avgLng = validVillages.length > 0
    ? validVillages.reduce((acc, curr) => acc + (curr.longitude || 0), 0) / validVillages.length
    : 75.714;

  const center: [number, number] = [avgLat, avgLng];

  // Helper for Layer-specific styling, distinct colors, and highlighting for all 11 GIS layers
  const getLayerStyle = (v: VillagePoint) => {
    const score = v.vulnerability_score;

    switch (activeLayerId) {
      case "accessibility":
        // 02. Travel Accessibility
        return {
          color: score > 50 ? "#f59e0b" : "#0284c7",
          radius: score > 50 ? 1400 : 700,
          label: "02. Healthcare Travel Accessibility",
          detail: score > 50 ? "High Travel Time Barrier (>35 min to PHC)" : "Normal PHC Travel Distance"
        };
      case "maternal":
        // 03. Maternal ANC & Delivery Care
        return {
          color: score > 50 ? "#06b6d4" : "#0891b2",
          radius: score > 50 ? 1300 : 700,
          label: "03. Maternal ANC & Delivery Care Deficit",
          detail: score > 50 ? "High 1st Trimester ANC Deficit Risk" : "Stable Maternal Care Access"
        };
      case "immunization":
        // 04. Immunization Coverage Deficit
        return {
          color: score > 50 ? "#2563eb" : "#3b82f6",
          radius: score > 50 ? 1300 : 700,
          label: "04. Immunization Coverage Deficit",
          detail: score > 50 ? "Under-5 Vaccination Dropout Cluster" : "Target Immunization Level"
        };
      case "nutrition":
        // 05. Malnutrition Surveillance (SAM/MAM)
        return {
          color: score > 50 ? "#a855f7" : "#c026d3",
          radius: score > 50 ? 1500 : 800,
          label: "05. Malnutrition Surveillance (SAM/MAM)",
          detail: score > 50 ? "Active Anganwadi SAM/MAM Alert Zone" : "Routine Anganwadi Nutrition"
        };
      case "infrastructure":
        // 06. Infrastructure & Unpaved Road Access
        return {
          color: score > 50 ? "#059669" : "#10b981",
          radius: score > 50 ? 1350 : 650,
          label: "06. Infrastructure & Unpaved Road Access",
          detail: score > 50 ? "Unpaved Kutcha Road Access Barrier" : "Paved Road Connectivity"
        };
      case "demographics":
        // 07. Demographic Vulnerability Ratio
        return {
          color: score > 50 ? "#4f46e5" : "#6366f1",
          radius: score > 50 ? 1300 : 700,
          label: "07. Demographic Vulnerability Ratio",
          detail: score > 50 ? "High Under-5 & Elderly Dependency Ratio" : "Normal Demographic Ratio"
        };
      case "facilities":
        // 08. Health Facility Master
        return {
          color: "#0d9488",
          radius: score > 50 ? 1100 : 600,
          label: "08. Health Facility Master (CHCs & PHCs)",
          detail: "PHC/CHC Facility Catchment Territory"
        };
      case "mmu":
        // 09. MMU Fleet GPS Telemetry
        return {
          color: "#84cc16",
          radius: 1000,
          label: "09. MMU Fleet GPS Telemetry",
          detail: "Mobile Clinic Telemetry Coverage Zone"
        };
      case "weather":
        // 10. IMD Weather & Rainfall Flood Alert
        return {
          color: score > 50 ? "#ea580c" : "#f97316",
          radius: score > 50 ? 1600 : 800,
          label: "10. IMD Weather & Rainfall Flood Alert",
          detail: score > 50 ? "Heavy Rainfall & Active Flood Risk Alert" : "Normal Climate Status"
        };
      case "logistics":
        // 11. Drug & Vaccine Stock Availability
        return {
          color: score > 50 ? "#db2777" : "#e11d48",
          radius: score > 50 ? 1200 : 600,
          label: "11. Drug & Vaccine Stock Availability",
          detail: score > 50 ? "Essential Drug & Vaccine Stockout Warning" : "Adequate Supply Inventory"
        };
      default:
        // 01. Overall Vulnerability Index (0-100)
        return {
          color: score >= 70 ? "#ef4444" : score >= 50 ? "#f97316" : score >= 30 ? "#f59e0b" : "#10b981",
          radius: score > 60 ? 1200 : 600,
          label: "01. Overall Vulnerability Index",
          detail: `Overall Score: ${score}/100 (${v.risk_level} Risk)`
        };
    }
  };

  return (
    <div className="w-full h-full min-h-[600px] rounded-xl overflow-hidden border border-dark-cardBorder shadow-inner relative z-0">
      <MapContainer
        center={center}
        zoom={9}
        scrollWheelZoom={true}
        style={{ width: "100%", height: "100%", minHeight: "600px" }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {villages.map((v) => {
          if (!v.latitude || !v.longitude) return null;
          const layerStyle = getLayerStyle(v);

          return (
            <React.Fragment key={v.village_code}>
              <Circle
                center={[v.latitude, v.longitude]}
                radius={layerStyle.radius}
                pathOptions={{
                  color: layerStyle.color,
                  fillColor: layerStyle.color,
                  fillOpacity: 0.55,
                  weight: 2,
                }}
              >
                <Popup>
                  <div className="p-1 space-y-2 min-w-[210px]">
                    <div className="font-bold text-sm text-slate-900">{v.village_name}</div>
                    <div className="text-[11px] text-slate-600 font-medium">
                      Taluk: <strong>{v.taluk_name}</strong> | District: <strong>{v.district_name}</strong>
                    </div>

                    <div className="p-2 bg-slate-100 rounded-lg text-xs space-y-1 font-mono">
                      <div className="text-[10px] text-slate-500 font-bold uppercase">{layerStyle.label}</div>
                      <div className="text-[11px] font-semibold text-slate-800">{layerStyle.detail}</div>
                      <div className="flex items-center justify-between font-bold pt-1 border-t border-slate-200">
                        <span>Vulnerability Score:</span>
                        <span>{v.vulnerability_score}/100</span>
                      </div>
                    </div>

                    <div className="pt-1">
                      <VulnerabilityBadge score={v.vulnerability_score} riskLevel={v.risk_level} size="sm" />
                    </div>

                    <button
                      onClick={() => onSelectVillage(v.village_code)}
                      className="w-full mt-2 bg-dark-card text-white text-xs py-1.5 px-3 rounded font-semibold hover:bg-slate-800 transition shadow"
                    >
                      Inspect Full Profile →
                    </button>
                  </div>
                </Popup>
              </Circle>
            </React.Fragment>
          );
        })}
      </MapContainer>
    </div>
  );
};

export default MapComponent;
