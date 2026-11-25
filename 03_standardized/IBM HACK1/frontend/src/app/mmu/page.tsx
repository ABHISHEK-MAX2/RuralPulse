"use client";

import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiService } from "@/lib/api";
import { useAuth } from "@/lib/AuthContext";
import { Truck, Send } from "lucide-react";

import { RoleGuard } from "@/components/shell/RoleGuard";

export default function MMUPage() {
  const { selectedDistrict } = useAuth();
  const queryClient = useQueryClient();

  const [showDispatchModal, setShowDispatchModal] = useState(false);
  const [targetVillageCode, setTargetVillageCode] = useState<number>(598623);
  const [mmuId, setMmuId] = useState<string>("KA-MMU-524-01");
  const [missionName, setMissionName] = useState<string>("Hanamaneri Inam Emergency Healthcare Relief");
  const [scheduledDate, setScheduledDate] = useState<string>("2026-09-15");

  const { data: fleet } = useQuery({
    queryKey: ["mmuFleet", selectedDistrict],
    queryFn: () => apiService.getMMUFleet(selectedDistrict),
  });

  const { data: missions } = useQuery({
    queryKey: ["mmuMissions", selectedDistrict],
    queryFn: () => apiService.getMMUMissions(selectedDistrict),
  });

  const dispatchMutation = useMutation({
    mutationFn: (data: any) => apiService.dispatchMMU(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["mmuMissions"] });
      setShowDispatchModal(false);
    },
  });

  const handleDispatch = (e: React.FormEvent) => {
    e.preventDefault();
    dispatchMutation.mutate({
      mmu_id: mmuId,
      village_code: targetVillageCode,
      mission_name: missionName,
      scheduled_date: scheduledDate,
      priority: "CRITICAL",
      beneficiaries_targeted: 75,
    });
  };

  return (
    <RoleGuard allowedRoles={["DHO", "MMU_COORDINATOR"]}>
      <div className="space-y-6">
        
        {/* Header */}
        <div className="bg-dark-card p-6 rounded-2xl border border-dark-cardBorder shadow-md flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2 text-brand-emerald text-xs font-bold uppercase tracking-wider mb-1">
              <Truck className="w-4 h-4 text-brand-emerald" />
              <span>MOBILE MEDICAL UNIT (MMU) FLEET OPERATIONS</span>
            </div>
            <h1 className="text-2xl font-bold text-white">MMU Mission Dispatch & Operations</h1>
            <p className="text-xs text-slate-400 mt-1">
              Plan, dispatch, and track mobile health clinic missions for remote villages with travel barriers.
            </p>
          </div>

          <button
            onClick={() => setShowDispatchModal(true)}
            className="px-5 py-2.5 bg-brand-emerald text-dark-bg font-extrabold text-xs rounded-xl shadow hover:bg-emerald-400 transition flex items-center space-x-2"
          >
            <Send className="w-4 h-4" />
            <span>Dispatch New MMU Mission</span>
          </button>
        </div>

        {/* Fleet Vehicles Status Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {fleet?.map((mmu) => (
            <div key={mmu.id} className="bg-dark-card border border-dark-cardBorder rounded-2xl p-5 shadow-sm space-y-3">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs font-bold text-slate-400">{mmu.mmu_id}</span>
                <span className="bg-emerald-950/80 text-brand-emerald text-[10px] font-bold px-2 py-0.5 rounded border border-emerald-800 font-mono">
                  {mmu.status}
                </span>
              </div>
              <h3 className="font-bold text-white text-sm">{mmu.mmu_name}</h3>
              <div className="text-xs text-slate-400 space-y-1">
                <p>Sector: <strong className="text-slate-200">{mmu.assigned_area || "Bagalkote Rural"}</strong></p>
                <p>Available: <strong className="text-slate-200">{mmu.available_from || "09:00 AM IST"}</strong></p>
              </div>
              <p className="text-[10px] text-amber-400 font-mono bg-dark-inset p-2 rounded-lg border border-dark-insetBorder">
                GPS Telemetry: {mmu.data_status}
              </p>
            </div>
          ))}
        </div>

        {/* Missions Queue Table */}
        <div className="bg-dark-card border border-dark-cardBorder rounded-2xl shadow-md p-6 space-y-4">
          <div className="flex items-center justify-between border-b border-dark-cardBorder pb-3">
            <h2 className="text-base font-bold text-white">Active & Scheduled MMU Missions</h2>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-dark-inset text-slate-300 font-bold border-b border-dark-insetBorder uppercase tracking-wider">
                <tr>
                  <th className="p-3">Mission Name</th>
                  <th className="p-3">MMU Unit</th>
                  <th className="p-3">Target Village</th>
                  <th className="p-3">Scheduled Date</th>
                  <th className="p-3">Priority</th>
                  <th className="p-3">Status</th>
                  <th className="p-3">Beneficiaries Targeted</th>
                  <th className="p-3">Dispatched By</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-dark-insetBorder font-medium text-slate-200">
                {missions?.map((m) => (
                  <tr key={m.id} className="hover:bg-dark-inset/50 transition">
                    <td className="p-3 font-bold text-white">{m.mission_name}</td>
                    <td className="p-3 font-mono font-bold text-brand-emerald">{m.mmu_id}</td>
                    <td className="p-3 font-bold text-slate-200">{m.village_name || `Village #${m.village_code}`}</td>
                    <td className="p-3 font-mono text-slate-300">{m.scheduled_date}</td>
                    <td className="p-3">
                      <span className="bg-rose-950/80 text-rose-400 text-[10px] font-bold px-2 py-0.5 rounded border border-rose-800">
                        {m.priority}
                      </span>
                    </td>
                    <td className="p-3">
                      <span className="bg-emerald-950/80 text-brand-emerald text-[10px] font-bold px-2 py-0.5 rounded border border-emerald-800">
                        {m.status}
                      </span>
                    </td>
                    <td className="p-3 font-mono text-slate-300">{m.beneficiaries_targeted} Patients</td>
                    <td className="p-3 text-slate-400">{m.assigned_by}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Dispatch Modal */}
        {showDispatchModal && (
          <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4">
            <div className="bg-dark-card border border-dark-cardBorder rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-4">
              <h2 className="text-lg font-bold text-white">Dispatch Mobile Medical Unit</h2>
              
              <form onSubmit={handleDispatch} className="space-y-3 text-xs">
                <div>
                  <label className="font-bold text-slate-300 block mb-1">Select MMU Vehicle</label>
                  <select
                    value={mmuId}
                    onChange={(e) => setMmuId(e.target.value)}
                    className="w-full p-2.5 border border-dark-insetBorder rounded-xl bg-dark-inset text-white font-semibold focus:outline-none"
                  >
                    <option value="KA-MMU-524-01">KA-MMU-524-01 (Bagalkote Sector 1)</option>
                    <option value="KA-MMU-528-01">KA-MMU-528-01 (Ballari Sector 1)</option>
                  </select>
                </div>

                <div>
                  <label className="font-bold text-slate-300 block mb-1">Target Village LGD Code</label>
                  <input
                    type="number"
                    value={targetVillageCode}
                    onChange={(e) => setTargetVillageCode(Number(e.target.value))}
                    className="w-full p-2.5 border border-dark-insetBorder rounded-xl bg-dark-inset text-white font-mono"
                    required
                  />
                </div>

                <div>
                  <label className="font-bold text-slate-300 block mb-1">Mission Title</label>
                  <input
                    type="text"
                    value={missionName}
                    onChange={(e) => setMissionName(e.target.value)}
                    className="w-full p-2.5 border border-dark-insetBorder rounded-xl bg-dark-inset text-white font-medium"
                    required
                  />
                </div>

                <div>
                  <label className="font-bold text-slate-300 block mb-1">Scheduled Deployment Date</label>
                  <input
                    type="date"
                    value={scheduledDate}
                    onChange={(e) => setScheduledDate(e.target.value)}
                    className="w-full p-2.5 border border-dark-insetBorder rounded-xl bg-dark-inset text-white font-mono"
                    required
                  />
                </div>

                <div className="pt-4 flex justify-end space-x-2">
                  <button
                    type="button"
                    onClick={() => setShowDispatchModal(false)}
                    className="px-4 py-2 border border-dark-insetBorder rounded-xl font-bold text-slate-400 hover:bg-dark-inset"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={dispatchMutation.isPending}
                    className="px-5 py-2 bg-brand-emerald text-dark-bg rounded-xl font-extrabold hover:bg-emerald-400"
                  >
                    Confirm Dispatch
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

      </div>
    </RoleGuard>
  );
}
