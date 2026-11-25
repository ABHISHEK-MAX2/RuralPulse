"use client";

export const dynamic = "force-dynamic";

import React from "react";
import { useQuery } from "@tanstack/react-query";
import { apiService } from "@/lib/api";
import { useAuth } from "@/lib/AuthContext";
import { Building2 } from "lucide-react";


import { RoleGuard } from "@/components/shell/RoleGuard";

export default function FacilitiesPage() {
  const { selectedDistrict } = useAuth();

  const { data: facilities, isLoading } = useQuery({
    queryKey: ["healthFacilities", selectedDistrict],
    queryFn: () => apiService.getFacilities({ district_code: selectedDistrict }),
  });

  return (
    <RoleGuard allowedRoles={["DHO"]}>
      <div className="space-y-6">
        
        {/* Page Title Header */}
        <div className="bg-dark-card border border-dark-cardBorder p-6 rounded-2xl shadow-md space-y-1">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-emerald-950/80 rounded-lg text-brand-emerald border border-emerald-800/80">
              <Building2 className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-extrabold text-white">
                Karnataka Health Facility Master & Service Utilization Directory
              </h1>
              <p className="text-xs text-slate-400">
                Sourced from National Health Facility Registry (NIN) & Rural Health Statistics (RHS) • SQLite Database Engine
              </p>
            </div>
          </div>
        </div>

        {/* Facilities Grid */}
        {isLoading ? (
          <div className="p-12 text-center text-slate-400 bg-dark-card rounded-2xl border border-dark-cardBorder font-mono text-xs">
            Loading health facilities registry...
          </div>
        ) : facilities && facilities.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {facilities.map((fac: any, idx: number) => (
              <div
                key={fac.facility_id || idx}
                className="bg-dark-card border border-dark-cardBorder rounded-2xl p-6 shadow-lg space-y-5 flex flex-col justify-between"
              >
                {/* Card Header: Facility ID Pill & Status Badge */}
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="bg-dark-inset text-slate-400 text-[10px] font-bold font-mono px-2.5 py-1 rounded-md border border-dark-insetBorder">
                      {fac.facility_id || `KA-FAC-${fac.district_code || 524}-${idx + 1}`}
                    </span>

                    {fac.facility_status === "FUNCTIONAL" || !fac.facility_status ? (
                      <span className="bg-brand-emeraldBg text-emerald-400 text-[10px] font-bold px-3 py-1 rounded-md border border-brand-emeraldBorder tracking-wide font-mono">
                        FUNCTIONAL
                      </span>
                    ) : (
                      <span className="bg-brand-goldBg text-amber-400 text-[10px] font-bold px-3 py-1 rounded-md border border-brand-goldBorder tracking-wide font-mono">
                        {fac.facility_status}
                      </span>
                    )}
                  </div>

                  {/* Title & Type */}
                  <div className="flex items-center space-x-2">
                    <span className="bg-emerald-950/80 text-brand-emerald font-mono font-bold text-[10px] px-2 py-0.5 rounded border border-emerald-800">
                      {fac.facility_type || "PHC"}
                    </span>
                    <h2 className="text-lg font-bold text-white">{fac.facility_name}</h2>
                  </div>
                  <p className="text-xs text-slate-400 font-medium mt-1">
                    District Code: {fac.district_code} | Taluk Code: {fac.taluk_code}
                  </p>
                </div>

                {/* Inset Metric Box (3 Columns) */}
                <div className="bg-dark-inset border border-dark-insetBorder rounded-xl p-4 grid grid-cols-3 gap-2 text-center">
                  <div className="space-y-1 border-r border-dark-insetBorder pr-2">
                    <span className="text-[10px] text-slate-400 font-semibold uppercase block">Bed Capacity</span>
                    <span className="text-base font-extrabold text-white">{fac.beds || 6} Beds</span>
                  </div>

                  <div className="space-y-1 border-r border-dark-insetBorder px-2">
                    <span className="text-[10px] text-slate-400 font-semibold uppercase block">Doctors (Pos/Sanc)</span>
                    <span className="text-base font-extrabold text-white">
                      {fac.doctors_in_position ?? 2} / {fac.doctors_sanctioned ?? 2}
                    </span>
                  </div>

                  <div className="space-y-1 pl-2">
                    <span className="text-[10px] text-slate-400 font-semibold uppercase block">Nurses (Pos/Sanc)</span>
                    <span className="text-base font-extrabold text-white">
                      {fac.nurses_in_position ?? 3} / {fac.nurses_sanctioned ?? 3}
                    </span>
                  </div>
                </div>

                {/* Facility Details Footer */}
                <div className="flex items-center justify-between text-xs pt-1">
                  <span className="text-slate-400 font-medium">ANM Staff Status:</span>
                  <span className="text-brand-emerald font-extrabold font-mono">
                    {fac.anm_available ?? 2} ANM Staff Deployed
                  </span>
                </div>

              </div>
            ))}
          </div>
        ) : (
          <div className="p-12 text-center text-slate-400 bg-dark-card rounded-2xl border border-dark-cardBorder font-mono text-xs">
            No health facilities returned for selected district scope.
          </div>
        )}

      </div>
    </RoleGuard>
  );
}

