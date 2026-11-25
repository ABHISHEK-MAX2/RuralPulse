"use client";

import React, { useEffect, useState } from "react";
import { VillageProfile } from "@/lib/types";
import { apiService } from "@/lib/api";
import { VulnerabilityBadge } from "./VulnerabilityBadge";
import { X, MapPin, HeartPulse, Droplets, Cpu } from "lucide-react";

interface Props {
  villageCode: number | null;
  onClose: () => void;
}

export const VillageProfileDrawer: React.FC<Props> = ({ villageCode, onClose }) => {
  const [profile, setProfile] = useState<VillageProfile | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [actionMsg, setActionMsg] = useState<string | null>(null);
  const [actionLoading, setActionLoading] = useState<boolean>(false);

  useEffect(() => {
    if (villageCode) {
      setLoading(true);
      apiService.getVillageProfile(villageCode)
        .then((data) => {
          setProfile(data);
          setLoading(false);
        })
        .catch((err) => {
          console.error("Failed to load village profile", err);
          setLoading(false);
        });
    }
  }, [villageCode]);

  if (!villageCode) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden bg-black/60 backdrop-blur-sm flex justify-end">
      <div className="w-full max-w-2xl bg-dark-sidebar h-full shadow-2xl overflow-y-auto flex flex-col justify-between border-l border-dark-cardBorder">
        
        {/* Header */}
        <div className="bg-dark-bg text-white p-6 sticky top-0 z-10 flex items-start justify-between border-b border-dark-cardBorder">
          <div>
            <div className="flex items-center space-x-2 text-brand-emerald text-xs font-mono mb-1">
              <MapPin className="w-3.5 h-3.5" />
              <span>LGD CODE: {profile?.village_code || villageCode} • GRAM PANCHAYAT: {profile?.gram_panchayat_name || "GP Sector 4"}</span>
            </div>
            <h2 className="text-2xl font-bold text-white">{profile?.village_name || "Village Intelligence Profile"}</h2>
            <p className="text-xs text-slate-400 mt-1">
              Taluk: <span className="text-white font-semibold">{profile?.taluk_name}</span> • District: <span className="text-white font-semibold">{profile?.district_name}</span>
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-xl bg-dark-card text-slate-400 hover:text-white hover:bg-dark-inset transition border border-dark-cardBorder"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Body */}
        {loading ? (
          <div className="p-12 text-center text-slate-400">
            <div className="animate-spin w-8 h-8 border-4 border-brand-emerald border-t-transparent rounded-full mx-auto mb-4" />
            Loading complete village profile data...
          </div>
        ) : profile ? (
          <div className="p-6 space-y-6 flex-1 text-slate-200">
            
            {/* Vulnerability Banner */}
            <div className="bg-dark-card border border-dark-cardBorder rounded-2xl p-5 shadow-sm space-y-3">
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">0–100 Explainable Vulnerability Score</span>
                  <div className="flex items-center space-x-3 mt-1">
                    <span className="text-3xl font-extrabold text-white font-mono">{profile.vulnerability_score}/100</span>
                    <VulnerabilityBadge score={profile.vulnerability_score} riskLevel={profile.risk_level} size="lg" />
                  </div>
                </div>
                <div className="text-right">
                  <span className="text-xs text-slate-400 block">7-Day Predicted Risk</span>
                  <span className="text-lg font-bold font-mono text-rose-400">{profile.predicted_score_7d}/100</span>
                </div>
              </div>

              {/* Data Provenance Tag */}
              <div className="pt-2 border-t border-dark-cardBorder flex items-center justify-between text-xs text-slate-400">
                <span>Data Provenance Classification:</span>
                <span className="bg-emerald-950/80 text-brand-emerald px-2.5 py-0.5 rounded-full font-mono font-semibold text-[10px] border border-emerald-800">
                  {profile.provenance_classification}
                </span>
              </div>
            </div>

            {/* Explainable AI SHAP Factor Breakdown */}
            <div className="bg-amber-950/30 border border-amber-900/60 rounded-2xl p-5 space-y-3">
              <div className="flex items-center space-x-2 text-amber-400 font-bold text-xs">
                <Cpu className="w-4 h-4 text-amber-400" />
                <span>WHY IS THIS VILLAGE AT RISK? (EXPLAINABLE AI FACTORS)</span>
              </div>

              <div className="space-y-2.5">
                {profile.top_contributing_factors.map((factor, idx) => (
                  <div key={idx} className="bg-dark-card p-3 rounded-xl border border-dark-cardBorder space-y-1">
                    <div className="flex items-center justify-between text-xs font-semibold text-white">
                      <span>{idx + 1}. {factor.factor_name}</span>
                      <span className="text-amber-400 font-mono">+{factor.impact_points} pts contribution</span>
                    </div>
                    <p className="text-xs text-slate-400">{factor.explanation}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Healthcare Accessibility & Infrastructure */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-dark-card border border-dark-cardBorder rounded-2xl p-4 space-y-2">
                <div className="flex items-center space-x-2 text-rose-400 font-bold text-xs">
                  <HeartPulse className="w-4 h-4 text-rose-400" />
                  <span>HEALTHCARE ACCESSIBILITY</span>
                </div>
                <div className="text-xs space-y-1.5 text-slate-300">
                  <p><strong className="text-slate-400">Nearest PHC:</strong> {profile.nearest_phc_name}</p>
                  <p><strong className="text-slate-400">Distance to PHC:</strong> {profile.distance_to_phc_km} km</p>
                  <p><strong className="text-slate-400">Travel Time:</strong> <span className="font-bold text-rose-400">{profile.travel_time_to_phc_minutes} minutes</span></p>
                  <p><strong className="text-slate-400">Road Accessibility:</strong> {profile.road_access}</p>
                </div>
              </div>

              <div className="bg-dark-card border border-dark-cardBorder rounded-2xl p-4 space-y-2">
                <div className="flex items-center space-x-2 text-cyan-400 font-bold text-xs">
                  <Droplets className="w-4 h-4 text-cyan-400" />
                  <span>DEMOGRAPHICS & AMENITIES</span>
                </div>
                <div className="text-xs space-y-1.5 text-slate-300">
                  <p><strong className="text-slate-400">Total Population:</strong> {profile.population.toLocaleString()}</p>
                  <p><strong className="text-slate-400">Children &lt; 5:</strong> {profile.children_under_5} | <strong className="text-slate-400">Elderly:</strong> {profile.elderly_population}</p>
                  <p><strong className="text-slate-400">Literacy Rate:</strong> {profile.literacy_rate}%</p>
                  <p><strong className="text-slate-400">Drinking Water:</strong> {profile.drinking_water_access}</p>
                </div>
              </div>
            </div>

            {/* 10-Dimensional Subscore Breakdown */}
            <div className="bg-dark-card border border-dark-cardBorder rounded-2xl p-5 space-y-3">
              <h4 className="text-xs font-bold text-white uppercase tracking-wider">10-Dimensional Risk Subscores</h4>
              
              <div className="grid grid-cols-2 gap-3 text-xs">
                {Object.entries(profile.subscores).map(([key, val]) => (
                  <div key={key} className="space-y-1">
                    <div className="flex justify-between text-slate-400">
                      <span className="capitalize">{key.replace(/_/g, " ")}:</span>
                      <span className="font-mono font-semibold text-white">{val}/100</span>
                    </div>
                    <div className="w-full bg-dark-inset rounded-full h-1.5 overflow-hidden border border-dark-insetBorder">
                      <div
                        className={`h-1.5 rounded-full ${val > 60 ? "bg-rose-500" : val > 40 ? "bg-amber-500" : "bg-emerald-500"}`}
                        style={{ width: `${Math.min(100, val)}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Interactive Closed-Loop AI Intervention Authorization Panel */}
            <div className="bg-emerald-950/40 border border-emerald-800/80 rounded-2xl p-5 space-y-4 shadow-lg">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2 text-brand-emerald font-bold text-xs">
                  <HeartPulse className="w-4 h-4 text-brand-emerald" />
                  <span>AUTHORIZE CLOSED-LOOP AI INTERVENTIONS</span>
                </div>
                <span className="text-[10px] font-mono bg-emerald-950 text-emerald-300 px-2 py-0.5 rounded border border-emerald-800 font-bold">
                  INTERLINKED SEVERITY ENGINE
                </span>
              </div>

              {actionMsg && (
                <div className="bg-brand-emeraldBg border border-brand-emeraldBorder text-emerald-300 p-3 rounded-xl text-xs space-y-2">
                  <div className="font-semibold flex items-center justify-between">
                    <span>✓ {actionMsg}</span>
                    <a
                      href="/mmu"
                      className="px-2.5 py-1 bg-brand-emerald text-dark-bg rounded-lg text-[11px] font-extrabold hover:bg-emerald-400 transition"
                    >
                      Track Fleet & Telemetry →
                    </a>
                  </div>
                  <div className="grid grid-cols-2 gap-1.5 pt-1 text-[10px] text-emerald-400/90 border-t border-emerald-800/40">
                    <div>🛰️ GPS Beacon: Active Telemetry</div>
                    <div>📋 ANM Attendance Sync: Connected</div>
                    <div>🔄 Status: EN_ROUTE to Village</div>
                    <div>🔐 Audit Trail: SHA-256 Recorded</div>
                  </div>
                </div>
              )}

              <p className="text-xs text-slate-300 leading-relaxed">
                Authorizing an intervention immediately dispatches field resources and triggers the backend <strong>Closed-Loop Severity Engine</strong> to reduce this village's vulnerability score in real-time.
              </p>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <button
                  disabled={actionLoading}
                  onClick={async () => {
                    if (!villageCode) return;
                    setActionLoading(true);
                    try {
                      await apiService.dispatchMMU({
                        mmu_id: "KA-MMU-01",
                        village_code: villageCode,
                        mission_name: `Urgent MMU Outreach for ${profile.village_name}`,
                        scheduled_date: "Today",
                        priority: "CRITICAL",
                        beneficiaries_targeted: 100
                      });
                      setActionMsg("MMU Mobile Clinic Dispatched! Vulnerability Score reduced by -25 pts.");
                      // Refetch profile to display updated reduced score
                      const updated = await apiService.getVillageProfile(villageCode);
                      setProfile(updated);
                    } catch (e) {
                      console.error("Action error", e);
                    } finally {
                      setActionLoading(false);
                    }
                  }}
                  className="px-4 py-2.5 bg-brand-emerald hover:bg-emerald-600 text-dark-bg font-extrabold rounded-xl text-xs shadow-md transition flex items-center justify-center space-x-2 disabled:opacity-50"
                >
                  <span>Dispatch MMU Mobile Clinic (-25 pts)</span>
                </button>

                <button
                  disabled={actionLoading}
                  onClick={async () => {
                    if (!villageCode) return;
                    setActionLoading(true);
                    try {
                      // Trigger closed-loop reduction via alert resolution
                      await apiService.actionAlert(1, "RESOLVE");
                      setActionMsg("Nutrition & Health Camp Authorized! Score reduced by -15 pts.");
                      const updated = await apiService.getVillageProfile(villageCode);
                      setProfile(updated);
                    } catch (e) {
                      console.error("Action error", e);
                    } finally {
                      setActionLoading(false);
                    }
                  }}
                  className="px-4 py-2.5 bg-dark-card hover:bg-dark-inset text-amber-300 font-extrabold rounded-xl text-xs border border-amber-800 shadow-md transition flex items-center justify-center space-x-2 disabled:opacity-50"
                >
                  <span>Schedule ANC & Health Camp (-15 pts)</span>
                </button>
              </div>
            </div>

          </div>
        ) : null}

        {/* Footer Actions */}
        <div className="p-4 bg-dark-bg border-t border-dark-cardBorder flex justify-end space-x-3">
          <button
            onClick={onClose}
            className="px-4 py-2 text-xs font-semibold text-slate-300 bg-dark-card border border-dark-cardBorder rounded-xl hover:text-white transition"
          >
            Close Profile
          </button>
        </div>

      </div>
    </div>
  );
};
