"use client";

import React from "react";
import { Utensils } from "lucide-react";

export default function NutritionPage() {
  return (
    <div className="space-y-6">
      <div className="bg-dark-card p-6 rounded-2xl border border-dark-cardBorder shadow-md flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-amber-400 text-xs font-bold uppercase tracking-wider mb-1">
            <Utensils className="w-4 h-4 text-amber-400" />
            <span>POSHAN TRACKER & ANGANWADI NUTRITION MONITORING</span>
          </div>
          <h1 className="text-2xl font-bold text-white">Anganwadi & Malnutrition Surveillance</h1>
          <p className="text-xs text-slate-400 mt-1">
            Severe Acute Malnutrition (SAM), Moderate Acute Malnutrition (MAM), and Take Home Ration (THR) monitoring across 480 Anganwadi centres.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-dark-card p-6 rounded-2xl border border-dark-cardBorder shadow-md space-y-2">
          <span className="text-xs font-bold text-slate-400 uppercase">Screened Children</span>
          <div className="text-3xl font-black font-mono text-white">33,240</div>
          <p className="text-xs text-slate-400">Anganwadi Registered Children</p>
        </div>

        <div className="bg-dark-card p-6 rounded-2xl border border-rose-950/80 shadow-md space-y-2">
          <span className="text-xs font-bold text-rose-400 uppercase">Severe Malnutrition (SAM)</span>
          <div className="text-3xl font-black font-mono text-rose-400">46 Cases</div>
          <p className="text-xs text-rose-300 font-medium">Require Emergency Therapeutic Food & PHC Visit</p>
        </div>

        <div className="bg-dark-card p-6 rounded-2xl border border-amber-950/80 shadow-md space-y-2">
          <span className="text-xs font-bold text-amber-400 uppercase">Moderate Malnutrition (MAM)</span>
          <div className="text-3xl font-black font-mono text-amber-400">182 Cases</div>
          <p className="text-xs text-amber-300 font-medium">Receiving Daily THR & Growth Monitoring</p>
        </div>
      </div>
    </div>
  );
}
