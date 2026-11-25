"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/AuthContext";
import { apiService } from "@/lib/api";
import { Activity, Shield, UserCheck, ArrowRight, Lock, Mail } from "lucide-react";
import { UserRole } from "@/lib/types";

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuth();
  
  const [email, setEmail] = useState("state_admin@karnataka.gov.in");
  const [password, setPassword] = useState("admin123");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const data = await apiService.login(email, password);
      login(data.access_token, {
        id: 1,
        email: email,
        full_name: data.user_name,
        role: data.role as UserRole,
        district_code: data.district_code,
      });
      const defaultRoutes: Record<string, string> = {
        STATE_ADMIN: "/dashboard",
        DHO: "/dashboard",
        MMU_COORDINATOR: "/mmu",
        SYS_ADMIN: "/admin",
      };
      router.push(defaultRoutes[data.role] || "/dashboard");
    } catch (err: any) {
      console.error(err);
      setError("Invalid login credentials. Please verify official government email.");
    } finally {
      setLoading(false);
    }
  };

  const handleQuickLogin = async (roleEmail: string, rolePass: string) => {
    setEmail(roleEmail);
    setPassword(rolePass);
    setLoading(true);
    setError("");

    try {
      const data = await apiService.login(roleEmail, rolePass);
      login(data.access_token, {
        id: 1,
        email: roleEmail,
        full_name: data.user_name,
        role: data.role as UserRole,
        district_code: data.district_code,
      });
      const defaultRoutes: Record<string, string> = {
        STATE_ADMIN: "/dashboard",
        DHO: "/dashboard",
        MMU_COORDINATOR: "/mmu",
        SYS_ADMIN: "/admin",
      };
      router.push(defaultRoutes[data.role] || "/dashboard");
    } catch (err: any) {
      console.error(err);
      setError("Invalid login credentials. Please verify official government email.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col justify-between p-6 relative overflow-hidden">
      
      {/* Background Glow */}
      <div className="absolute -top-40 -left-40 w-96 h-96 bg-cyan-600/20 rounded-full blur-3xl" />
      <div className="absolute -bottom-40 -right-40 w-96 h-96 bg-gov-blue/30 rounded-full blur-3xl" />

      {/* Top Bar */}
      <div className="max-w-6xl mx-auto w-full flex items-center justify-between z-10">
        <div className="flex items-center space-x-3">
          <div className="bg-gov-gold p-2 rounded-lg text-gov-navy font-bold">
            <Activity className="w-6 h-6 stroke-[2.5]" />
          </div>
          <div>
            <span className="font-extrabold text-lg text-white tracking-wide uppercase flex items-center space-x-1.5">
              <span>Govt of Karnataka • </span><span className="text-emerald-400">Rural</span><span>Pulse</span>
            </span>
            <p className="text-xs text-slate-400">Department of Health & Family Welfare</p>
          </div>
        </div>
      </div>

      {/* Login Card */}
      <div className="max-w-md mx-auto w-full bg-slate-900/90 border border-slate-800 p-8 rounded-2xl shadow-2xl backdrop-blur-md z-10 space-y-6">
        
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-black text-white"><span className="text-emerald-400">Rural</span>Pulse</h1>
          <p className="text-xs text-slate-400">Karnataka Rural Healthcare Intelligence & Decision Support System</p>
        </div>

        {error && (
          <div className="bg-rose-950/80 border border-rose-800 text-rose-300 text-xs p-3 rounded-lg text-center font-medium">
            {error}
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-4">
          <div className="space-y-1">
            <label className="text-xs font-semibold text-slate-300">Official Government Email</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full pl-9 pr-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-sm text-white focus:outline-none focus:border-cyan-500"
                placeholder="officer@karnataka.gov.in"
              />
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-xs font-semibold text-slate-300">Security Password</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full pl-9 pr-4 py-2 bg-slate-800 border border-slate-700 rounded-lg text-sm text-white focus:outline-none focus:border-cyan-500"
                placeholder="••••••••"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 bg-gov-blue hover:bg-cyan-600 text-white text-sm font-bold rounded-lg shadow-md transition flex items-center justify-center space-x-2"
          >
            {loading ? "Authenticating..." : "Access Official Portal"}
            <ArrowRight className="w-4 h-4" />
          </button>
        </form>

        {/* Demo Persona Quick-Select */}
        <div className="pt-4 border-t border-slate-800 space-y-2">
          <p className="text-[11px] text-slate-400 font-semibold uppercase tracking-wider text-center">
            Demo Persona Quick Access
          </p>
          
          <div className="grid grid-cols-2 gap-2 text-xs">
            <button
              onClick={() => handleQuickLogin("sinchana_admin@karnataka.gov.in", "admin123")}
              className="p-2 bg-slate-800/80 hover:bg-slate-800 border border-slate-700 rounded-lg text-left transition text-slate-200"
            >
              <span className="font-bold text-cyan-400 block">Sinchana Admin</span>
              <span className="text-[10px] text-slate-400">State Health Director</span>
            </button>

            <button
              onClick={() => handleQuickLogin("dho_bagalkote@karnataka.gov.in", "dho123")}
              className="p-2 bg-slate-800/80 hover:bg-slate-800 border border-slate-700 rounded-lg text-left transition text-slate-200"
            >
              <span className="font-bold text-amber-400 block">DHO Bagalkote</span>
              <span className="text-[10px] text-slate-400">Dr. Patil</span>
            </button>

            <button
              onClick={() => handleQuickLogin("mmu_coord_bagalkote@karnataka.gov.in", "mmu123")}
              className="p-2 bg-slate-800/80 hover:bg-slate-800 border border-slate-700 rounded-lg text-left transition text-slate-200"
            >
              <span className="font-bold text-emerald-400 block">MMU Coordinator</span>
              <span className="text-[10px] text-slate-400">Suresh Kumar</span>
            </button>

            <button
              onClick={() => handleQuickLogin("sysadmin@karnataka.gov.in", "sys123")}
              className="p-2 bg-slate-800/80 hover:bg-slate-800 border border-slate-700 rounded-lg text-left transition text-slate-200"
            >
              <span className="font-bold text-purple-400 block">System Admin</span>
              <span className="text-[10px] text-slate-400">Sys Admin</span>
            </button>
          </div>
        </div>

      </div>

      {/* Footer */}
      <div className="max-w-6xl mx-auto w-full text-center text-xs text-slate-500 z-10">
        Strictly for authorized Karnataka public health officers. National Health Mission (NHM) Karnataka.
      </div>
    </div>
  );
}
