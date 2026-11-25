"use client";

export const dynamic = "force-dynamic";

import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiService } from "@/lib/api";
import { Database, RefreshCw, CheckCircle2, ShieldAlert, Filter, Info } from "lucide-react";

import { RoleGuard } from "@/components/shell/RoleGuard";

export default function DataSourcesPage() {
  const queryClient = useQueryClient();
  const [filterType, setFilterType] = useState<string>("ALL");
  const [ingestBanner, setIngestBanner] = useState<any>(null);

  const { data: sources, isLoading } = useQuery({
    queryKey: ["dataSources"],
    queryFn: () => apiService.getDataSources(),
  });

  const ingestMutation = useMutation({
    mutationFn: (id: number) => apiService.triggerIngest(id),
    onSuccess: (data: any) => {
      queryClient.invalidateQueries({ queryKey: ["dataSources"] });
      setIngestBanner(data);
    },
  });

  const filteredSources = sources?.filter((s) => {
    if (filterType === "PUBLIC") return s.publicly_accessible === "YES";
    if (filterType === "PROTECTED") return s.publicly_accessible !== "YES";
    return true;
  });

  return (
    <RoleGuard allowedRoles={["SYS_ADMIN"]}>
      <div className="space-y-6">
        
        {/* Header */}
        <div className="bg-dark-card p-6 rounded-2xl border border-dark-cardBorder shadow-md flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2 text-brand-emerald text-xs font-bold uppercase tracking-wider mb-1">
              <Database className="w-4 h-4" />
              <span>DATA PROVENANCE & INTEGRITY MATRIX</span>
            </div>
            <h1 className="text-2xl font-bold text-white">Data Governance Matrix & Availability Audit</h1>
            <p className="text-xs text-slate-400 mt-1">
              Authoritative lineage, granularity, missingness %, and public vs protected access controls for all 11 health datasets.
            </p>
          </div>

          {/* Access Filter Toolbar */}
          <div className="flex items-center space-x-2 bg-dark-inset p-1.5 rounded-xl border border-dark-insetBorder text-xs shrink-0">
            <Filter className="w-3.5 h-3.5 text-slate-400 ml-1" />
            <span className="font-semibold text-slate-300">Access Filter:</span>
            {["ALL", "PUBLIC", "PROTECTED"].map((type) => (
              <button
                key={type}
                onClick={() => setFilterType(type)}
                className={`px-3 py-1 rounded-lg font-bold transition ${
                  filterType === type
                    ? "bg-brand-emerald text-dark-bg shadow-sm"
                    : "text-slate-400 hover:bg-dark-card hover:text-white"
                }`}
              >
                {type === "PUBLIC" ? "Public Open Data" : type === "PROTECTED" ? "Protected Data" : "All Datasets"}
              </button>
            ))}
          </div>
        </div>

        {/* Live Ingestion Success Feedback Banner */}
        {ingestBanner && (
          <div className="bg-emerald-950/80 border border-brand-emerald p-4 rounded-2xl text-xs text-white shadow-lg space-y-1 animate-pulse">
            <div className="flex items-center justify-between font-bold">
              <div className="flex items-center space-x-2 text-brand-emerald">
                <CheckCircle2 className="w-4 h-4 text-brand-emerald" />
                <span className="uppercase tracking-wider">PIPELINE INGESTION COMPLETED</span>
              </div>
              <span className="font-mono text-slate-400 text-[11px]">{ingestBanner.ingestion_timestamp}</span>
            </div>
            <p className="text-slate-200 font-medium">
              {ingestBanner.message}
            </p>
          </div>
        )}

        {/* Governance Info Card */}
        <div className="bg-dark-inset p-4 rounded-xl border border-dark-insetBorder flex items-center justify-between text-xs text-slate-300">
          <div className="flex items-center space-x-3">
            <Info className="w-4 h-4 text-brand-emerald shrink-0" />
            <span>
              All 11 datasets adhere to strict <strong>National Data Sharing and Accessibility Policy (NDSAP)</strong> rules. Public open datasets are retrieved from data.gov.in. Operational telemetry is restricted to authorized System Administrators.
            </span>
          </div>
          <span className="font-mono text-[11px] text-slate-400 shrink-0 ml-3">
            Total Tracked Datasets: {sources?.length || 11}
          </span>
        </div>

        {/* Data Availability Matrix Table */}
        <div className="bg-dark-card border border-dark-cardBorder rounded-2xl shadow-md overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-dark-inset text-slate-300 font-bold border-b border-dark-insetBorder uppercase tracking-wider">
                <tr>
                  <th className="p-3.5">Dataset Domain</th>
                  <th className="p-3.5">Source Organization</th>
                  <th className="p-3.5">Granularity</th>
                  <th className="p-3.5">Public Accessibility</th>
                  <th className="p-3.5">Missingness %</th>
                  <th className="p-3.5">Access Requirements & Governance</th>
                  <th className="p-3.5 text-right">Pipeline Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-dark-insetBorder font-medium text-slate-200">
                {isLoading ? (
                  <tr>
                    <td colSpan={7} className="p-8 text-center text-slate-400 font-mono">
                      Loading dataset availability matrix...
                    </td>
                  </tr>
                ) : filteredSources && filteredSources.length > 0 ? (
                  filteredSources.map((s) => (
                    <tr key={s.id} className="hover:bg-dark-inset/50 transition">
                      <td className="p-3.5">
                        <span className="font-bold text-white block">{s.dataset}</span>
                        <span className="text-[11px] text-slate-400 font-mono">{s.field}</span>
                      </td>
                      <td className="p-3.5 text-slate-300 font-semibold">{s.source_organization}</td>
                      <td className="p-3.5 font-mono text-slate-400">{s.geographic_granularity}</td>
                      <td className="p-3.5">
                        {s.publicly_accessible === "YES" ? (
                          <span className="bg-emerald-950/80 text-brand-emerald text-[10px] font-bold px-2.5 py-0.5 rounded border border-emerald-800 font-mono">
                            PUBLIC OPEN DATA
                          </span>
                        ) : (
                          <span className="bg-rose-950/80 text-rose-400 text-[10px] font-bold px-2.5 py-0.5 rounded border border-rose-800 font-mono">
                            PROTECTED ACCESS
                          </span>
                        )}
                      </td>
                      <td className="p-3.5 font-mono font-bold">{s.missingness}</td>
                      <td className="p-3.5 text-slate-400 max-w-xs text-[11px]">{s.access_requirements}</td>
                      <td className="p-3.5 text-right">
                        <button
                          onClick={() => ingestMutation.mutate(s.id)}
                          disabled={ingestMutation.isPending}
                          className="px-3.5 py-1.5 bg-dark-inset hover:bg-brand-emerald hover:text-dark-bg text-slate-200 font-bold rounded-lg border border-dark-insetBorder transition inline-flex items-center space-x-1.5 cursor-pointer disabled:opacity-50"
                        >
                          <RefreshCw className={`w-3.5 h-3.5 ${ingestMutation.isPending ? "animate-spin" : ""}`} />
                          <span>{ingestMutation.isPending ? "Ingesting..." : "Re-Ingest"}</span>
                        </button>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={7} className="p-8 text-center text-slate-400 font-mono">
                      No datasets matching selected access filter.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </RoleGuard>
  );
}
