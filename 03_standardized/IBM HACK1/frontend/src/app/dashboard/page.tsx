"use client";

export const dynamic = "force-dynamic";

import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { apiService } from "@/lib/api";
import { useAuth } from "@/lib/AuthContext";
import { VulnerabilityBadge } from "@/components/village/VulnerabilityBadge";
import { VillageProfileDrawer } from "@/components/village/VillageProfileDrawer";
import {
  Activity, ShieldAlert, Truck, Home, AlertTriangle, Cpu, TrendingUp,
  MapPin, ChevronRight, FileSpreadsheet, Layers
} from "lucide-react";
import Link from "next/link";

import { RoleGuard } from "@/components/shell/RoleGuard";

export default function DashboardPage() {
  const { role, selectedDistrict } = useAuth();
  const [selectedVillageCode, setSelectedVillageCode] = useState<number | null>(null);

  // Fetch KPIs
  const { data: kpis, isLoading: kpisLoading } = useQuery({
    queryKey: ["kpis", selectedDistrict],
    queryFn: () => apiService.getKPIs(selectedDistrict),
  });

  // Fetch District Rankings
  const { data: districts } = useQuery({
    queryKey: ["districts"],
    queryFn: () => apiService.getDistricts(),
  });

  // Fetch Top High-Risk Villages
  const { data: highRiskVillages } = useQuery({
    queryKey: ["highRiskVillages", selectedDistrict],
    queryFn: () => apiService.getVillages({ district_code: selectedDistrict, limit: 10 }),
  });

  return (
    <RoleGuard allowedRoles={["STATE_ADMIN", "DHO"]}>
      <div className="space-y-6">
        
        {/* Top Banner */}
        <div className="bg-dark-card text-white p-6 rounded-2xl shadow-lg border border-dark-cardBorder flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2 text-brand-emerald text-xs font-mono mb-1">
              <Layers className="w-3.5 h-3.5" />
              <span>EXECUTIVE DECISION SUPPORT PANEL • ROLE: {role.replace(/_/g, " ")}</span>
            </div>
            <h1 className="text-2xl font-bold text-white">
              {selectedDistrict ? "District Health Executive Overview (Bagalkote)" : "Karnataka State Health Intelligence Dashboard"}
            </h1>
            <p className="text-xs text-slate-400 mt-1">
              Monitored across 30,773 LGD mapped villages, 720 health facilities, and 480 Poshan Tracker Anganwadi sectors.
            </p>
          </div>

          <div className="flex items-center space-x-3">
            <Link
              href="/map"
              className="px-4 py-2 bg-emerald-950/80 border border-brand-emeraldBorder text-brand-emerald hover:bg-emerald-900 text-xs font-bold rounded-xl transition flex items-center space-x-1.5 shadow"
            >
              <MapPin className="w-4 h-4" />
              <span>Open Map Intelligence</span>
            </Link>
            <Link
              href="/reports"
              className="px-4 py-2 bg-dark-inset text-slate-300 border border-dark-insetBorder hover:text-white text-xs font-bold rounded-xl transition flex items-center space-x-1.5"
            >
              <FileSpreadsheet className="w-4 h-4" />
              <span>Generate DHO Report</span>
            </Link>
          </div>
        </div>

        {/* Top-Level KPI Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          
          <div className="bg-dark-card p-5 rounded-2xl border border-dark-cardBorder shadow-sm space-y-2">
            <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase">
              <span>Villages Monitored</span>
              <Home className="w-4 h-4 text-slate-500" />
            </div>
            <div className="text-2xl font-black font-mono text-white">
              {kpisLoading ? "..." : kpis?.total_villages.toLocaleString()}
            </div>
            <p className="text-[11px] text-slate-400">100% LGD Code Synchronized</p>
          </div>

          <div className="bg-dark-card p-5 rounded-2xl border border-rose-950/80 shadow-sm space-y-2">
            <div className="flex items-center justify-between text-rose-400 text-xs font-semibold uppercase">
              <span>High & Critical Risk</span>
              <ShieldAlert className="w-4 h-4 text-rose-400" />
            </div>
            <div className="text-2xl font-black font-mono text-rose-400">
              {kpisLoading ? "..." : (kpis?.high_risk_villages || 0) + (kpis?.critical_villages || 0)}
            </div>
            <p className="text-[11px] text-rose-300 font-medium">Require Health Intervention</p>
          </div>

          <div className="bg-dark-card p-5 rounded-2xl border border-emerald-950/80 shadow-sm space-y-2">
            <div className="flex items-center justify-between text-brand-emerald text-xs font-semibold uppercase">
              <span>Active MMU Fleet</span>
              <Truck className="w-4 h-4 text-brand-emerald" />
            </div>
            <div className="text-2xl font-black font-mono text-brand-emerald">
              {kpisLoading ? "..." : kpis?.active_mmus} MMUs
            </div>
            <p className="text-[11px] text-emerald-400 font-medium">GPS Fleet Operations Ready</p>
          </div>

          <div className="bg-dark-card p-5 rounded-2xl border border-amber-950/80 shadow-sm space-y-2">
            <div className="flex items-center justify-between text-amber-400 text-xs font-semibold uppercase">
              <span>Pending Decision Support Plans</span>
              <Cpu className="w-4 h-4 text-amber-400" />
            </div>
            <div className="text-2xl font-black font-mono text-amber-400">
              {kpisLoading ? "..." : kpis?.pending_deployments}
            </div>
            <p className="text-[11px] text-amber-300 font-medium">Human-in-the-Loop Review Needed</p>
          </div>

        </div>

        {/* Main Grid: District Risk Rankings & Top Vulnerable Villages */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* District Risk Ranking Table (Left 2 Columns) */}
          <div className="lg:col-span-2 bg-dark-card border border-dark-cardBorder rounded-2xl p-6 shadow-md space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-base font-bold text-white">District Healthcare Risk Rankings</h2>
                <p className="text-xs text-slate-400">Ranked by average 0–100 explainable vulnerability index score</p>
              </div>
              <Link href="/map" className="text-xs font-bold text-brand-emerald hover:underline flex items-center space-x-1">
                <span>Open Map Intelligence</span>
                <ChevronRight className="w-3.5 h-3.5" />
              </Link>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-dark-inset text-slate-300 font-bold border-b border-dark-insetBorder uppercase">
                  <tr>
                    <th className="p-3">Rank</th>
                    <th className="p-3">District Name</th>
                    <th className="p-3">Total Villages</th>
                    <th className="p-3">High Risk Villages</th>
                    <th className="p-3">Avg Vulnerability Score</th>
                    <th className="p-3 text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-dark-insetBorder font-medium text-slate-200">
                  {districts?.slice(0, 8).map((d, idx) => (
                    <tr key={d.district_code} className="hover:bg-dark-inset/50 transition">
                      <td className="p-3 font-mono font-bold text-slate-500">#{idx + 1}</td>
                      <td className="p-3 font-bold text-white">{d.district_name}</td>
                      <td className="p-3 font-mono text-slate-300">{d.total_villages.toLocaleString()}</td>
                      <td className="p-3 font-mono font-bold text-rose-400">{d.high_risk_villages}</td>
                      <td className="p-3">
                        <div className="flex items-center space-x-2">
                          <span className="font-mono font-bold text-white">{d.avg_vulnerability_score}/100</span>
                          <div className="w-20 bg-dark-inset rounded-full h-1.5 overflow-hidden border border-dark-insetBorder">
                            <div
                              className={`h-1.5 rounded-full ${d.avg_vulnerability_score > 60 ? "bg-rose-500" : "bg-amber-500"}`}
                              style={{ width: `${Math.min(100, d.avg_vulnerability_score)}%` }}
                            />
                          </div>
                        </div>
                      </td>
                      <td className="p-3 text-right">
                        <Link
                          href={`/map?district_code=${d.district_code}`}
                          className="text-brand-emerald font-bold hover:underline"
                        >
                          Inspect District →
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Priority Village Register (Right Column) */}
          <div className="bg-dark-card border border-dark-cardBorder rounded-2xl p-6 shadow-md space-y-4">
            <div className="flex items-center justify-between border-b border-dark-cardBorder pb-3">
              <div>
                <h2 className="text-base font-bold text-white">Priority Vulnerable Villages</h2>
                <p className="text-xs text-slate-400">Highest risk villages requiring immediate intervention</p>
              </div>
            </div>

            <div className="space-y-3">
              {highRiskVillages?.map((v) => (
                <div
                  key={v.village_code}
                  onClick={() => setSelectedVillageCode(v.village_code)}
                  className="p-3 rounded-xl border border-dark-cardBorder hover:border-brand-emerald transition cursor-pointer bg-dark-inset/50 space-y-2"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-sm text-white">{v.village_name}</span>
                    <VulnerabilityBadge score={v.vulnerability_score} riskLevel={v.risk_level} size="sm" />
                  </div>
                  
                  <div className="flex items-center justify-between text-xs text-slate-400">
                    <span>Taluk: <strong className="text-slate-200">{v.taluk_name}</strong></span>
                    <span>Pop: <strong className="text-slate-200">{v.population.toLocaleString()}</strong></span>
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>

        {/* Village Profile Drawer Modal */}
        <VillageProfileDrawer
          villageCode={selectedVillageCode}
          onClose={() => setSelectedVillageCode(null)}
        />

      </div>
    </RoleGuard>
  );
}
