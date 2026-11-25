"use client";

export const dynamic = "force-dynamic";

import React, { useState } from "react";
import nextDynamic from "next/dynamic";
import { useQuery } from "@tanstack/react-query";
import { apiService } from "@/lib/api";
import { useAuth } from "@/lib/AuthContext";
import { VillageProfileDrawer } from "@/components/village/VillageProfileDrawer";
import { Map, Filter, Layers, CheckCircle2, ShieldAlert } from "lucide-react";

const MapComponent = nextDynamic(() => import("@/components/map/MapComponent"), {
  ssr: false,
  loading: () => (
    <div className="w-full h-[650px] bg-dark-card rounded-2xl flex items-center justify-center text-slate-400">
      <div className="text-center space-y-3">
        <div className="animate-spin w-8 h-8 border-4 border-brand-emerald border-t-transparent rounded-full mx-auto" />
        <p className="text-xs font-mono text-slate-300">Loading Karnataka Map Intelligence Engine...</p>
      </div>
    </div>
  ),
});

import { RoleGuard } from "@/components/shell/RoleGuard";

export default function MapPage() {
  const { selectedDistrict } = useAuth();
  const [selectedVillageCode, setSelectedVillageCode] = useState<number | null>(null);
  const [riskFilter, setRiskFilter] = useState<string>("ALL");
  const [activeLayerId, setActiveLayerId] = useState<string>("vulnerability");

  const indicatorLayers = [
    { id: "vulnerability", name: "01. Overall Vulnerability Index (0–100)", dataset: "LGD Master + Scoring Engine", color: "text-rose-400" },
    { id: "accessibility", name: "02. Healthcare Travel Accessibility (Min to PHC)", dataset: "GIS Accessibility Matrix", color: "text-amber-400" },
    { id: "maternal", name: "03. Maternal ANC & Delivery Care Deficit", dataset: "HMIS & NFHS-5 Indicators", color: "text-cyan-400" },
    { id: "immunization", name: "04. Immunization Coverage Deficit", dataset: "HMIS Child Health Records", color: "text-blue-400" },
    { id: "nutrition", name: "05. Malnutrition Surveillance (SAM/MAM)", dataset: "Poshan Tracker Anganwadi", color: "text-purple-400" },
    { id: "infrastructure", name: "06. Infrastructure & Unpaved Road Access", dataset: "Census 2011 Infrastructure", color: "text-emerald-400" },
    { id: "demographics", name: "07. Demographic Vulnerability Ratio", dataset: "Census Demographics", color: "text-indigo-400" },
    { id: "facilities", name: "08. Health Facility Master (CHCs & PHCs)", dataset: "National Facility Registry (NIN)", color: "text-teal-400" },
    { id: "mmu", name: "09. MMU Fleet GPS Telemetry", dataset: "108 GPS Fleet Operations", color: "text-lime-400" },
    { id: "weather", name: "10. IMD Weather & Rainfall Flood Alert", dataset: "India Meteorological Dept", color: "text-orange-400" },
    { id: "logistics", name: "11. Drug & Vaccine Stock Availability", dataset: "DVDMS Logistics System", color: "text-pink-400" },
  ];

  const { data: villages } = useQuery({
    queryKey: ["mapVillages", selectedDistrict, riskFilter],
    queryFn: () =>
      apiService.getVillages({
        district_code: selectedDistrict,
        risk_level: riskFilter === "ALL" ? undefined : riskFilter,
        limit: 500,
      }),
  });

  const activeLayerObj = indicatorLayers.find(l => l.id === activeLayerId) || indicatorLayers[0];

  return (
    <RoleGuard allowedRoles={["STATE_ADMIN", "DHO", "MMU_COORDINATOR"]}>
      <div className="space-y-6">
        
        {/* Page Header */}
        <div className="bg-dark-card p-6 rounded-2xl border border-dark-cardBorder shadow-md flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2 text-brand-emerald text-xs font-bold uppercase tracking-wider mb-1">
              <Map className="w-4 h-4" />
              <span>GIS MAP INTELLIGENCE & GEOSPATIAL HEATMAP</span>
            </div>
            <h1 className="text-2xl font-bold text-white">Karnataka Rural Health Vulnerability Map</h1>
            <p className="text-xs text-slate-400 mt-1">
              Spatial distribution across all 11 health indicator layers, 30,771 LGD villages, PHC health facilities, travel accessibility, and flood risk.
            </p>
          </div>

          {/* Risk Level Filter Toolbar */}
          <div className="flex items-center space-x-2 bg-dark-inset p-1.5 rounded-xl border border-dark-insetBorder text-xs shrink-0">
            <Filter className="w-3.5 h-3.5 text-slate-400 ml-1" />
            <span className="font-semibold text-slate-300">Risk Filter:</span>
            {["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"].map((level) => (
              <button
                key={level}
                onClick={() => setRiskFilter(level)}
                className={`px-3 py-1 rounded-lg font-bold transition ${
                  riskFilter === level
                    ? "bg-brand-emerald text-dark-bg shadow-sm"
                    : "text-slate-400 hover:bg-dark-card hover:text-white"
                }`}
              >
                {level}
              </button>
            ))}
          </div>
        </div>

        {/* 11 Health Indicator GIS Layers Selector Panel */}
        <div className="bg-dark-card p-5 rounded-2xl border border-dark-cardBorder shadow-md space-y-3">
          <div className="flex items-center justify-between border-b border-dark-cardBorder pb-2.5">
            <div className="flex items-center space-x-2 text-xs font-bold text-white uppercase tracking-wider">
              <Layers className="w-4 h-4 text-brand-emerald" />
              <span>11 Health Indicator GIS Layer Toggles</span>
            </div>
            <div className="text-[11px] font-mono text-slate-400">
              Active GIS Layer: <span className="font-bold text-brand-emerald">{activeLayerObj.name}</span> ({activeLayerObj.dataset})
            </div>
          </div>

          {/* Indicator Layer Buttons Grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-2">
            {indicatorLayers.map((layer) => {
              const isActive = activeLayerId === layer.id;
              return (
                <button
                  key={layer.id}
                  onClick={() => setActiveLayerId(layer.id)}
                  className={`p-2.5 rounded-xl text-left text-xs transition border flex flex-col justify-between space-y-1 ${
                    isActive
                      ? "bg-emerald-950/80 border-brand-emerald text-white font-bold shadow-md"
                      : "bg-dark-inset/60 border-dark-insetBorder text-slate-400 hover:bg-dark-inset hover:text-slate-200"
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className={`text-[10px] font-mono font-bold ${layer.color}`}>{layer.id.toUpperCase()}</span>
                    {isActive && <CheckCircle2 className="w-3.5 h-3.5 text-brand-emerald" />}
                  </div>
                  <span className="text-[11px] leading-tight font-semibold line-clamp-2">{layer.name}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Active Layer Details Banner */}
        <div className="bg-dark-inset p-4 rounded-xl border border-dark-insetBorder flex items-center justify-between text-xs text-slate-300">
          <div className="flex items-center space-x-3">
            <ShieldAlert className="w-4 h-4 text-brand-emerald" />
            <span>
              Rendering spatial points for <strong className="text-white">{activeLayerObj.name}</strong> from dataset <strong className="text-brand-emerald font-mono">{activeLayerObj.dataset}</strong>.
            </span>
          </div>
          <span className="font-mono text-[11px] text-slate-400">
            Showing {villages?.length || 0} spatial locations
          </span>
        </div>

        {/* Map Container */}
        <div className="bg-dark-card p-3 rounded-2xl border border-dark-cardBorder shadow-lg relative">
          <MapComponent
            villages={villages || []}
            activeLayerId={activeLayerId}
            onSelectVillage={(code) => setSelectedVillageCode(code)}
          />
        </div>

        {/* Village Profile Drawer */}
        <VillageProfileDrawer
          villageCode={selectedVillageCode}
          onClose={() => setSelectedVillageCode(null)}
        />

      </div>
    </RoleGuard>
  );
}
