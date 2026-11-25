"use client";

import React from "react";
import { Package, Lock } from "lucide-react";

export default function ResourcesPage() {
  return (
    <div className="space-y-6">
      <div className="bg-dark-card p-6 rounded-2xl border border-dark-cardBorder shadow-md flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-brand-emerald text-xs font-bold uppercase tracking-wider mb-1">
            <Package className="w-4 h-4 text-brand-emerald" />
            <span>DVDMS / e-AUSHADHI DRUG LOGISTICS INTEGRATION</span>
          </div>
          <h1 className="text-2xl font-bold text-white">Operational Resources & Stock Status</h1>
          <p className="text-xs text-slate-400 mt-1">
            Vaccine stock days, essential medicines, IFA syrup, and biometric staff attendance tracking.
          </p>
        </div>
      </div>

      <div className="bg-amber-950/40 border border-amber-800 p-6 rounded-2xl shadow-md space-y-3">
        <div className="flex items-center space-x-2 text-amber-400 font-bold text-sm">
          <Lock className="w-5 h-5 text-amber-400" />
          <span>DATA INTEGRITY NOTICE: PROTECTED GOVERNMENT SYSTEM</span>
        </div>
        <p className="text-xs text-amber-200 font-medium leading-relaxed">
          Official real-time inventory from the Karnataka Drugs and Logistics Warehouse System (DVDMS / e-Aushadhi) requires authorized OAuth2 client certificate authentication.
        </p>
        <p className="text-xs text-slate-300 font-mono bg-dark-inset p-3 rounded-xl border border-dark-insetBorder">
          Status: NOT PUBLICLY AVAILABLE — REQUIRES AUTHORIZED GOVERNMENT SYSTEM ACCESS
        </p>
      </div>
    </div>
  );
}
