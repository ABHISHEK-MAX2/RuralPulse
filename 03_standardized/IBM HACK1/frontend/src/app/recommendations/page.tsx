"use client";

import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiService } from "@/lib/api";
import { useAuth } from "@/lib/AuthContext";
import { Cpu, CheckCircle, XCircle, ShieldCheck } from "lucide-react";

import { RoleGuard } from "@/components/shell/RoleGuard";

export default function RecommendationsPage() {
  const { selectedDistrict } = useAuth();
  const queryClient = useQueryClient();
  
  const [selectedStatus, setSelectedStatus] = useState<string>("PENDING_REVIEW");
  const [reviewNotes, setReviewNotes] = useState<string>("");
  const [activeRecId, setActiveRecId] = useState<number | null>(null);

  const { data: recommendations, isLoading } = useQuery({
    queryKey: ["recommendations", selectedDistrict, selectedStatus],
    queryFn: () => apiService.getRecommendations(selectedDistrict, selectedStatus),
  });

  const reviewMutation = useMutation({
    mutationFn: ({ id, status, notes }: { id: number; status: string; notes?: string }) =>
      apiService.reviewRecommendation(id, status, notes),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["recommendations"] });
      setActiveRecId(null);
      setReviewNotes("");
    },
  });

  const handleReviewAction = (id: number, status: string) => {
    reviewMutation.mutate({ id, status, notes: reviewNotes });
  };

  return (
    <RoleGuard allowedRoles={["STATE_ADMIN", "DHO"]}>
      <div className="space-y-6">
        
        {/* Header */}
        <div className="bg-dark-card p-6 rounded-2xl border border-dark-cardBorder shadow-md flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2 text-amber-400 text-xs font-bold uppercase tracking-wider mb-1">
              <Cpu className="w-4 h-4 text-amber-400" />
              <span>HUMAN-IN-THE-LOOP DECISION SUPPORT SYSTEM</span>
            </div>
            <h1 className="text-2xl font-bold text-white">Decision Support & Action Plans</h1>
            <p className="text-xs text-slate-400 mt-1">
              Data-backed intervention action plans requiring official DHO / State Administrator authorization prior to dispatch.
            </p>
          </div>

          {/* Status Filter Tabs */}
          <div className="flex items-center space-x-1.5 bg-dark-inset p-1.5 rounded-xl border border-dark-insetBorder text-xs">
            {["PENDING_REVIEW", "APPROVED", "REJECTED"].map((st) => (
              <button
                key={st}
                onClick={() => setSelectedStatus(st)}
                className={`px-3 py-1.5 rounded-lg font-bold transition ${
                  selectedStatus === st
                    ? "bg-brand-emerald text-dark-bg shadow-sm"
                    : "text-slate-400 hover:bg-dark-card hover:text-white"
                }`}
              >
                {st.replace("_", " ")}
              </button>
            ))}
          </div>
        </div>

        {/* Recommendations Cards Grid */}
        <div className="space-y-4">
          {isLoading ? (
            <div className="p-12 text-center text-slate-400 bg-dark-card rounded-2xl border border-dark-cardBorder">
              Loading AI recommendation feed...
            </div>
          ) : recommendations && recommendations.length > 0 ? (
            recommendations.map((rec) => (
              <div
                key={rec.id}
                className="bg-dark-card border border-dark-cardBorder rounded-2xl p-6 shadow-md space-y-4 transition"
              >
                <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-2 border-b border-dark-cardBorder pb-3">
                  <div className="flex items-center space-x-3">
                    <span
                      className={`px-2.5 py-1 rounded-md text-xs font-extrabold font-mono ${
                        rec.priority === "CRITICAL"
                          ? "bg-rose-950/80 text-rose-400 border border-rose-800"
                          : "bg-amber-950/80 text-amber-400 border border-amber-800"
                      }`}
                    >
                      PRIORITY: {rec.priority}
                    </span>
                    <h3 className="text-base font-bold text-white">{rec.action}</h3>
                  </div>

                  <div className="flex items-center space-x-2 text-xs">
                    <span className="text-slate-400 font-medium">Confidence Score:</span>
                    <span className="bg-emerald-950/80 text-brand-emerald font-mono font-bold px-2.5 py-0.5 rounded border border-emerald-800">
                      {(rec.confidence * 100).toFixed(0)}% AI CONFIDENCE
                    </span>
                  </div>
                </div>

                {/* Village & Rationale */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
                  <div className="bg-dark-inset p-3.5 rounded-xl border border-dark-insetBorder space-y-1">
                    <span className="text-slate-400 font-bold block">TARGET VILLAGE</span>
                    <p className="font-bold text-white text-sm">{rec.village_name || `Village #${rec.village_code}`}</p>
                    <p className="text-slate-400">LGD Code: {rec.village_code}</p>
                  </div>

                  <div className="bg-dark-inset p-3.5 rounded-xl border border-dark-insetBorder md:col-span-2 space-y-1">
                    <span className="text-slate-400 font-bold block">INTERVENTION RATIONALE</span>
                    <p className="text-slate-200 font-medium">{rec.reason}</p>
                    {rec.expected_impact && (
                      <p className="text-brand-emerald font-semibold pt-1">Impact: {rec.expected_impact}</p>
                    )}
                  </div>
                </div>

                {/* Status & Review Controls */}
                {rec.status === "PENDING_REVIEW" && (
                  <div className="pt-3 border-t border-dark-cardBorder flex flex-col md:flex-row items-end md:items-center justify-between gap-4">
                    <div className="flex-1 w-full">
                      <input
                        type="text"
                        placeholder="Officer authorization notes or modification instructions..."
                        value={activeRecId === rec.id ? reviewNotes : ""}
                        onChange={(e) => {
                          setActiveRecId(rec.id);
                          setReviewNotes(e.target.value);
                        }}
                        className="w-full text-xs px-3.5 py-2 bg-dark-inset border border-dark-insetBorder rounded-xl text-white focus:outline-none focus:border-brand-emerald"
                      />
                    </div>

                    <div className="flex items-center space-x-2 shrink-0">
                      <button
                        onClick={() => handleReviewAction(rec.id, "REJECTED")}
                        disabled={reviewMutation.isPending}
                        className="px-4 py-2 bg-rose-950/80 hover:bg-rose-900 text-rose-300 font-bold text-xs rounded-xl border border-rose-800 transition flex items-center space-x-1"
                      >
                        <XCircle className="w-4 h-4" />
                        <span>Reject</span>
                      </button>
                      
                      <button
                        onClick={() => handleReviewAction(rec.id, "APPROVED")}
                        disabled={reviewMutation.isPending}
                        className="px-5 py-2 bg-brand-emerald hover:bg-emerald-600 text-dark-bg font-extrabold text-xs rounded-xl transition shadow flex items-center space-x-1"
                      >
                        <CheckCircle className="w-4 h-4" />
                        <span>Approve & Authorize Dispatch</span>
                      </button>
                    </div>
                  </div>
                )}

                {rec.status === "APPROVED" && (
                  <div className="bg-emerald-950/60 border border-emerald-800 p-3 rounded-xl text-xs text-brand-emerald flex items-center justify-between">
                    <div className="flex items-center space-x-2 font-bold">
                      <ShieldCheck className="w-4 h-4 text-brand-emerald" />
                      <span>APPROVED & AUTHORIZED BY: {rec.approved_by || "District Health Officer"}</span>
                    </div>
                    <span className="font-mono text-emerald-400">{rec.approved_at ? new Date(rec.approved_at).toLocaleString() : "Authorized"}</span>
                  </div>
                )}

              </div>
            ))
          ) : (
            <div className="p-12 text-center text-slate-400 bg-dark-card rounded-2xl border border-dark-cardBorder">
              No recommendations found for status: <strong>{selectedStatus}</strong>.
            </div>
          )}
        </div>

      </div>
    </RoleGuard>
  );
}
