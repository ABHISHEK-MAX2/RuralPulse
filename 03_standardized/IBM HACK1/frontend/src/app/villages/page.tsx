"use client";

import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { apiService } from "@/lib/api";
import { useAuth } from "@/lib/AuthContext";
import { VulnerabilityBadge } from "@/components/village/VulnerabilityBadge";
import { VillageProfileDrawer } from "@/components/village/VillageProfileDrawer";
import { Search, Home, ChevronLeft, ChevronRight, Eye } from "lucide-react";

export default function VillagesPage() {
  const { selectedDistrict } = useAuth();
  const [search, setSearch] = useState("");
  const [riskLevel, setRiskLevel] = useState<string>("");
  const [page, setPage] = useState(0);
  const [selectedVillageCode, setSelectedVillageCode] = useState<number | null>(null);

  const limit = 25;

  const { data: villages, isLoading } = useQuery({
    queryKey: ["villagesList", selectedDistrict, search, riskLevel, page],
    queryFn: () =>
      apiService.getVillages({
        district_code: selectedDistrict,
        risk_level: riskLevel || undefined,
        search: search || undefined,
        limit,
        offset: page * limit,
      }),
  });

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="bg-dark-card p-6 rounded-2xl border border-dark-cardBorder shadow-md flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-brand-emerald text-xs font-bold uppercase tracking-wider mb-1">
            <Home className="w-4 h-4" />
            <span>LGD ADMINISTRATIVE MASTER DIRECTORY</span>
          </div>
          <h1 className="text-2xl font-bold text-white">Karnataka Rural Village Directory</h1>
          <p className="text-xs text-slate-400 mt-1">
            Searchable index of 30,773 villages with official LGD codes, demographics, travel times, and vulnerability scores.
          </p>
        </div>

        {/* Search & Filter Controls */}
        <div className="flex flex-wrap items-center gap-3 w-full md:w-auto">
          
          {/* Search Box */}
          <div className="relative flex-1 md:w-64">
            <Search className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" />
            <input
              type="text"
              value={search}
              onChange={(e) => { setSearch(e.target.value); setPage(0); }}
              placeholder="Search village name..."
              className="w-full pl-9 pr-4 py-2 text-xs bg-dark-inset border border-dark-insetBorder rounded-xl text-white focus:outline-none focus:border-brand-emerald"
            />
          </div>

          {/* Risk Level Filter */}
          <select
            value={riskLevel}
            onChange={(e) => { setRiskLevel(e.target.value); setPage(0); }}
            className="text-xs bg-dark-inset border border-dark-insetBorder rounded-xl px-3 py-2 text-slate-200 font-semibold focus:outline-none"
          >
            <option value="" className="bg-dark-sidebar">All Risk Levels</option>
            <option value="CRITICAL" className="bg-dark-sidebar">Critical Risk (80+)</option>
            <option value="HIGH" className="bg-dark-sidebar">High Risk (60-79)</option>
            <option value="MEDIUM" className="bg-dark-sidebar">Medium Risk (40-59)</option>
            <option value="LOW" className="bg-dark-sidebar">Low Risk (0-39)</option>
          </select>

        </div>
      </div>

      {/* Villages Table */}
      <div className="bg-dark-card border border-dark-cardBorder rounded-2xl shadow-md overflow-hidden">
        
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-dark-inset text-slate-300 font-bold border-b border-dark-insetBorder uppercase tracking-wider">
              <tr>
                <th className="p-3.5">LGD Code</th>
                <th className="p-3.5">Village Name</th>
                <th className="p-3.5">Taluk</th>
                <th className="p-3.5">District</th>
                <th className="p-3.5">Population</th>
                <th className="p-3.5">Vulnerability Score</th>
                <th className="p-3.5 text-right">Inspect Profile</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-dark-insetBorder font-medium text-slate-200">
              {isLoading ? (
                <tr>
                  <td colSpan={7} className="p-8 text-center text-slate-400 font-mono">
                    Loading LGD village database...
                  </td>
                </tr>
              ) : villages && villages.length > 0 ? (
                villages.map((v) => (
                  <tr key={v.village_code} className="hover:bg-dark-inset/50 transition">
                    <td className="p-3.5 font-mono text-slate-400 font-semibold">{v.village_code}</td>
                    <td className="p-3.5 font-bold text-white text-sm">{v.village_name}</td>
                    <td className="p-3.5 text-slate-300">{v.taluk_name}</td>
                    <td className="p-3.5 text-slate-300">{v.district_name}</td>
                    <td className="p-3.5 font-mono">{v.population.toLocaleString()}</td>
                    <td className="p-3.5">
                      <VulnerabilityBadge score={v.vulnerability_score} riskLevel={v.risk_level} size="sm" />
                    </td>
                    <td className="p-3.5 text-right">
                      <button
                        onClick={() => setSelectedVillageCode(v.village_code)}
                        className="px-3 py-1.5 bg-dark-inset hover:bg-brand-emerald hover:text-dark-bg text-slate-200 font-bold rounded-lg transition inline-flex items-center space-x-1 border border-dark-insetBorder"
                      >
                        <Eye className="w-3.5 h-3.5" />
                        <span>Profile</span>
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={7} className="p-8 text-center text-slate-400">
                    No matching villages found for the selected filters.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination Footer */}
        <div className="bg-dark-inset p-4 border-t border-dark-insetBorder flex items-center justify-between text-xs">
          <span className="text-slate-400 font-medium">
            Showing Page {page + 1} (25 villages per page)
          </span>
          
          <div className="flex items-center space-x-2">
            <button
              disabled={page === 0}
              onClick={() => setPage((p) => Math.max(0, p - 1))}
              className="p-1.5 rounded-lg border border-dark-insetBorder bg-dark-card hover:bg-dark-sidebar disabled:opacity-50 transition font-bold text-slate-200"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <button
              disabled={!villages || villages.length < limit}
              onClick={() => setPage((p) => p + 1)}
              className="p-1.5 rounded-lg border border-dark-insetBorder bg-dark-card hover:bg-dark-sidebar disabled:opacity-50 transition font-bold text-slate-200"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>

      </div>

      {/* Village Profile Drawer Modal */}
      <VillageProfileDrawer
        villageCode={selectedVillageCode}
        onClose={() => setSelectedVillageCode(null)}
      />

    </div>
  );
}
