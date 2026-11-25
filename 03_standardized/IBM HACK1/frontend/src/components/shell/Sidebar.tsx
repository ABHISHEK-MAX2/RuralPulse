"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard, Map, Building2, Truck,
  AlertTriangle, BarChart3, Database, Shield, Cpu
} from "lucide-react";
import { useAuth } from "@/lib/AuthContext";
import { UserRole } from "@/lib/types";

export const Sidebar: React.FC = () => {
  const pathname = usePathname();
  const { role } = useAuth();

  const roleNavItems: Record<UserRole, Array<{ name: string; href: string; icon: any }>> = {
    STATE_ADMIN: [
      { name: "Executive Dashboard", href: "/dashboard", icon: LayoutDashboard },
      { name: "Map Intelligence", href: "/map", icon: Map },
      { name: "Decision Support & Action Plans", href: "/recommendations", icon: Cpu },
      { name: "Analytics & Reports", href: "/reports", icon: BarChart3 },
      { name: "User Provisioning & Audit", href: "/admin", icon: Shield },
    ],
    DHO: [
      { name: "Executive Dashboard", href: "/dashboard", icon: LayoutDashboard },
      { name: "Map Intelligence", href: "/map", icon: Map },
      { name: "Health Facilities", href: "/facilities", icon: Building2 },
      { name: "Decision Support & Action Plans", href: "/recommendations", icon: Cpu },
      { name: "MMU Dispatch", href: "/mmu", icon: Truck },
      { name: "Alert Manager", href: "/alerts", icon: AlertTriangle },
      { name: "DHO Reports", href: "/reports", icon: BarChart3 },
    ],
    MMU_COORDINATOR: [
      { name: "MMU Fleet Operations", href: "/mmu", icon: Truck },
      { name: "Map Intelligence", href: "/map", icon: Map },
      { name: "Alert Manager", href: "/alerts", icon: AlertTriangle },
    ],
    SYS_ADMIN: [
      { name: "Data Governance Matrix", href: "/data-sources", icon: Database },
      { name: "System Admin & Audit", href: "/admin", icon: Shield },
      { name: "Audit & Provenance Reports", href: "/reports", icon: BarChart3 },
    ],
  };

  const navItems = roleNavItems[role] || roleNavItems.STATE_ADMIN;

  return (
    <aside className="w-64 bg-dark-sidebar text-slate-300 min-h-[calc(100vh-4rem)] border-r border-dark-cardBorder flex flex-col justify-between p-4 shrink-0">
      
      {/* Navigation Items */}
      <div className="space-y-1">
        <div className="px-3 py-2 text-[10px] font-bold text-slate-500 uppercase tracking-widest">
          {role === "SYS_ADMIN" ? "SYSTEM GOVERNANCE" :
           role === "MMU_COORDINATOR" ? "FLEET & EMERGENCY NAVIGATION" :
           role === "DHO" ? "DISTRICT HEALTH OPERATIONS" :
           "STATE HEALTH DIRECTORATE"}
        </div>

        {navItems.map((item) => {
          const isActive = pathname === item.href || pathname?.startsWith(item.href + "/");
          const Icon = item.icon;

          return (
            <Link
              key={item.name}
              href={item.href}
              className={`flex items-center space-x-3 px-3.5 py-2.5 rounded-xl text-xs font-medium transition ${
                isActive
                  ? "bg-emerald-950/70 text-brand-emerald border border-emerald-800/80 font-bold shadow-sm"
                  : "text-slate-400 hover:bg-dark-card hover:text-white"
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? "text-brand-emerald" : "text-slate-400"}`} />
              <span>{item.name}</span>
            </Link>
          );
        })}
      </div>

      {/* Bottom Session Role Context Card */}
      <div className="space-y-3 pt-4">
        <div className="bg-dark-card border border-dark-cardBorder rounded-xl p-4 space-y-2 relative">
          <span className="text-[10px] text-slate-500 font-semibold block uppercase tracking-wider">
            Session Role Context
          </span>
          <h4 className="text-xs font-bold text-white">
            {role === "SYS_ADMIN" ? "System Administrator" :
             role === "STATE_ADMIN" ? "State Health Director" :
             role === "MMU_COORDINATOR" ? "MMU Fleet Coordinator" :
             "District Health Officer (DHO)"}
          </h4>
          
          <div className="pt-1">
            <span className="bg-emerald-950/80 text-brand-emerald text-[10px] font-bold px-2 py-0.5 rounded-full border border-emerald-800 font-mono">
              {role === "STATE_ADMIN" || role === "SYS_ADMIN" ? "State Level (All 31 Districts)" : "Bagalkote District"}
            </span>
          </div>

          <p className="text-[10px] text-slate-500 font-mono pt-1">
            Primary Key: <span className="text-slate-400">village_code</span> (LGD Master)
          </p>
        </div>

        {/* Floating Avatar Circle 'N' */}
        <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-700 text-white font-bold text-xs flex items-center justify-center shadow">
          {role ? role.charAt(0) : "N"}
        </div>
      </div>

    </aside>
  );
};
