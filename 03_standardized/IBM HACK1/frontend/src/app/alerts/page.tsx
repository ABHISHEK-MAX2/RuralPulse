"use client";

export const dynamic = "force-dynamic";

import React from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiService } from "@/lib/api";
import { useAuth } from "@/lib/AuthContext";
import { AlertTriangle } from "lucide-react";

import { RoleGuard } from "@/components/shell/RoleGuard";

export default function AlertsPage() {
  const { selectedDistrict } = useAuth();
  const queryClient = useQueryClient();

  const { data: alerts, isLoading } = useQuery({
    queryKey: ["alerts", selectedDistrict],
    queryFn: () => apiService.getAlerts(selectedDistrict),
  });

  const actionMutation = useMutation({
    mutationFn: ({ id, action, assignedTo }: { id: number; action: string; assignedTo?: string }) =>
      apiService.actionAlert(id, action, assignedTo),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["alerts"] });
    },
  });

  return (
    <RoleGuard allowedRoles={["DHO", "MMU_COORDINATOR"]}>
      <div className="space-y-6">
        
        {/* Header */}
        <div className="bg-dark-card p-6 rounded-2xl border border-dark-cardBorder shadow-md flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2 text-rose-400 text-xs font-bold uppercase tracking-wider mb-1">
              <AlertTriangle className="w-4 h-4 text-rose-400" />
              <span>INTELLIGENT HEALTH & HAZARD ALERT ENGINE</span>
            </div>
            <h1 className="text-2xl font-bold text-white">Health Threat & Hazard Alerts</h1>
            <p className="text-xs text-slate-400 mt-1">
              Real-time automated alerts for vulnerability spikes, weather hazards, disease clusters, and stockout threats.
            </p>
          </div>
        </div>

        {/* Alerts Feed */}
        <div className="space-y-4">
          {isLoading ? (
            <div className="p-12 text-center text-slate-400 bg-dark-card rounded-2xl border border-dark-cardBorder">
              Loading real-time alert engine feed...
            </div>
          ) : alerts && alerts.length > 0 ? (
            alerts.map((alert) => (
              <div
                key={alert.id}
                className={`bg-dark-card border rounded-2xl p-6 shadow-md space-y-3 transition ${
                  alert.severity === "CRITICAL" ? "border-rose-900 bg-rose-950/20" : "border-dark-cardBorder"
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-center space-x-3">
                    <span
                      className={`px-2.5 py-1 rounded-md text-xs font-extrabold font-mono ${
                        alert.severity === "CRITICAL"
                          ? "bg-rose-950/80 text-rose-400 border border-rose-800 animate-pulse"
                          : "bg-amber-950/80 text-amber-400 border border-amber-800"
                      }`}
                    >
                      {alert.severity} SEVERITY
                    </span>
                    <h3 className="text-base font-bold text-white">{alert.title}</h3>
                  </div>

                  <span className="bg-dark-inset text-slate-300 text-xs font-mono font-semibold px-2.5 py-1 rounded-md border border-dark-insetBorder uppercase">
                    STATUS: {alert.status}
                  </span>
                </div>

                <p className="text-xs text-slate-300 font-medium">{alert.description}</p>

                {alert.recommended_action && (
                  <div className="bg-dark-inset border border-dark-insetBorder p-3 rounded-xl text-xs space-y-1">
                    <span className="text-slate-400 font-bold block">RECOMMENDED ACTION</span>
                    <p className="text-white font-semibold">{alert.recommended_action}</p>
                  </div>
                )}

                {/* Alert Actions */}
                <div className="pt-2 border-t border-dark-cardBorder flex items-center justify-between text-xs">
                  <span className="text-slate-500 font-mono">
                    Triggered: {new Date(alert.created_at).toLocaleString()}
                  </span>

                  {alert.status === "OPEN" && (
                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => actionMutation.mutate({ id: alert.id, action: "ACKNOWLEDGE" })}
                        className="px-3 py-1.5 bg-dark-inset hover:bg-dark-sidebar text-slate-200 font-bold rounded-lg border border-dark-insetBorder transition"
                      >
                        Acknowledge
                      </button>
                      <button
                        onClick={() => actionMutation.mutate({ id: alert.id, action: "RESOLVE" })}
                        className="px-3 py-1.5 bg-brand-emerald hover:bg-emerald-600 text-dark-bg font-extrabold rounded-lg shadow transition"
                      >
                        Mark Resolved
                      </button>
                    </div>
                  )}
                </div>
              </div>
            ))
          ) : (
            <div className="p-12 text-center text-slate-400 bg-dark-card rounded-2xl border border-dark-cardBorder">
              No active alerts recorded.
            </div>
          )}
        </div>

      </div>
    </RoleGuard>
  );
}
