"use client";

import React from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/AuthContext";
import { UserRole } from "@/lib/types";
import { UserCheck, Globe, LogOut } from "lucide-react";

export const AppHeader: React.FC = () => {
  const { user, role, logout } = useAuth();
  const router = useRouter();

  const roleLabels: Record<UserRole, string> = {
    STATE_ADMIN: "State Health Director",
    DHO: "District Health Officer (DHO)",
    MMU_COORDINATOR: "MMU Fleet Coordinator",
    SYS_ADMIN: "System Administrator",
  };

  return (
    <header className="bg-dark-bg text-white border-b border-dark-cardBorder sticky top-0 z-40 px-6 py-3 shadow-md w-full">
      <div className="w-full flex items-center justify-between">
        
        {/* Left Side: KA Emblem, Title, Demo Badge, Subtitle */}
        <div className="flex items-center space-x-3">
          {/* Green Circle KA Avatar */}
          <div className="w-9 h-9 rounded-full bg-brand-emerald text-dark-bg font-extrabold flex items-center justify-center text-sm shadow">
            KA
          </div>

          <div>
            <div className="flex items-center space-x-2">
              <h1 className="font-black text-xl text-white tracking-tight flex items-center">
                <span className="text-brand-emerald">Rural</span><span>Pulse</span>
              </h1>
              <span className="text-xs text-slate-400 font-medium pl-1 hidden md:inline">| Healthcare Spatial Intelligence</span>
            </div>
            <p className="text-[11px] text-slate-400 font-medium">
              Government of Karnataka — Department of Health & Family Welfare
            </p>
          </div>
        </div>

        {/* Right Side: Logged-in User Profile & Logout Button */}
        <div className="flex items-center space-x-3">
          
          {/* Authenticated User Badge */}
          <div className="flex items-center space-x-2 bg-dark-card px-3.5 py-1.5 rounded-full border border-dark-cardBorder text-xs">
            <UserCheck className="w-3.5 h-3.5 text-brand-emerald" />
            <span className="text-slate-400 text-[11px]">Authenticated Persona:</span>
            <span className="font-bold text-white">
              {user?.full_name || roleLabels[role] || "State Health Director"}
            </span>
          </div>

          {/* Language Indicator */}
          <div className="hidden sm:flex items-center space-x-1.5 bg-dark-card px-3 py-1.5 rounded-full border border-dark-cardBorder text-xs text-slate-300 font-medium">
            <Globe className="w-3.5 h-3.5 text-slate-400" />
            <span>English</span>
          </div>

          {/* Logout Button */}
          <button
            onClick={() => {
              logout();
              router.push("/");
            }}
            className="flex items-center space-x-1.5 bg-rose-950/80 hover:bg-rose-900 text-rose-300 px-3 py-1.5 rounded-full border border-rose-800 text-xs font-bold transition cursor-pointer"
          >
            <LogOut className="w-3.5 h-3.5 text-rose-400" />
            <span>Log Out</span>
          </button>

        </div>

      </div>
    </header>
  );
};
