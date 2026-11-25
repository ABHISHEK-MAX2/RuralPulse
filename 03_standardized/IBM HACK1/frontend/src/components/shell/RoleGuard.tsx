"use client";

import React from "react";
import { useAuth } from "@/lib/AuthContext";
import { UserRole } from "@/lib/types";
import { ShieldAlert, ArrowLeft } from "lucide-react";
import Link from "next/link";

interface RoleGuardProps {
  allowedRoles: UserRole[];
  children: React.ReactNode;
}

const defaultRoutes: Record<UserRole, string> = {
  STATE_ADMIN: "/dashboard",
  DHO: "/dashboard",
  MMU_COORDINATOR: "/mmu",
  SYS_ADMIN: "/admin",
};

const roleLabels: Record<UserRole, string> = {
  STATE_ADMIN: "State Health Director",
  DHO: "District Health Officer (DHO)",
  MMU_COORDINATOR: "MMU Fleet Coordinator",
  SYS_ADMIN: "System Administrator",
};

export const RoleGuard: React.FC<RoleGuardProps> = ({ allowedRoles, children }) => {
  const { role } = useAuth();

  if (!role || !allowedRoles.includes(role)) {
    const homeRoute = defaultRoutes[role] || "/dashboard";
    return (
      <div className="min-h-[60vh] flex items-center justify-center p-6">
        <div className="bg-dark-card border border-rose-950/80 rounded-2xl p-8 max-w-lg w-full text-center space-y-4 shadow-2xl">
          <div className="w-12 h-12 rounded-full bg-rose-950/80 border border-rose-800 text-rose-400 flex items-center justify-center mx-auto">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <h2 className="text-xl font-bold text-white">Access Restricted by RBAC Policy</h2>
          <p className="text-xs text-slate-300">
            Your authenticated persona <strong className="text-rose-400 font-mono">[{roleLabels[role] || role}]</strong> is strictly scoped to specific operational workflows.
          </p>
          <div className="bg-dark-inset p-3.5 rounded-xl border border-dark-insetBorder text-left text-xs space-y-1.5 font-mono text-slate-400">
            <span className="text-slate-300 font-bold uppercase block">Authorized Capabilities for Your Role:</span>
            {role === "STATE_ADMIN" && <p>• Statewide Executive Dashboard, 11-Layer Map, Decision Support & Action Plans, Reports, User Provisioning</p>}
            {role === "DHO" && <p>• District Dashboard, 11-Layer Map, Facilities, Decision Support & Action Plans, MMU Dispatch, Hazard Alerts, DHO Reports</p>}
            {role === "MMU_COORDINATOR" && <p>• MMU Fleet Operations & Dispatch, Map Intelligence, Medical Hazard Alerts</p>}
            {role === "SYS_ADMIN" && <p>• Data Governance Matrix, System Admin & Cryptographic Audit Ledger, Audit Reports</p>}
          </div>

          <div className="pt-2">
            <Link
              href={homeRoute}
              className="inline-flex items-center space-x-2 px-5 py-2.5 bg-brand-emerald hover:bg-emerald-400 text-dark-bg font-extrabold text-xs rounded-xl shadow transition cursor-pointer"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Return to Authorized Dashboard</span>
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return <>{children}</>;
};
