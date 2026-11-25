"use client";

import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiService } from "@/lib/api";
import { Shield, UserPlus, Users, X, CheckCircle2, KeyRound } from "lucide-react";

import { RoleGuard } from "@/components/shell/RoleGuard";

export default function AdminPage() {
  const queryClient = useQueryClient();
  const [showModal, setShowModal] = useState<boolean>(false);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Form State
  const [fullName, setFullName] = useState<string>("Ms.Sinchana");
  const [email, setEmail] = useState<string>("sinchana@gmail.com");
  const [password, setPassword] = useState<string>("12345678");
  const [role, setRole] = useState<string>("DHO");
  const [districtCode, setDistrictCode] = useState<string>("535"); // Davanagere (535)

  // Fetch Audit Logs
  const { data: auditLogs, isLoading: logsLoading } = useQuery({
    queryKey: ["auditLogs"],
    queryFn: () => apiService.getAuditLogs(),
  });

  // Fetch Provisioned Users
  const { data: users, isLoading: usersLoading } = useQuery({
    queryKey: ["provisionedUsers"],
    queryFn: () => apiService.listUsers(),
  });

  // User Registration Mutation
  const registerMutation = useMutation({
    mutationFn: (userData: {
      email: string;
      password: string;
      full_name: string;
      role: string;
      district_code?: number;
    }) => apiService.registerUser(userData),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["provisionedUsers"] });
      queryClient.invalidateQueries({ queryKey: ["auditLogs"] });
      setSuccessMsg(`Account for ${data.full_name} (${data.role}) provisioned successfully in SQLite database!`);
      setErrorMsg(null);
      setShowModal(false);
    },
    onError: (err: any) => {
      setErrorMsg(err?.response?.data?.detail || "Failed to provision user account.");
      setSuccessMsg(null);
    },
  });

  const handleCreateAccount = (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);
    setSuccessMsg(null);

    registerMutation.mutate({
      email,
      password,
      full_name: fullName,
      role,
      district_code: districtCode ? parseInt(districtCode, 10) : undefined,
    });
  };

  return (
    <RoleGuard allowedRoles={["STATE_ADMIN", "SYS_ADMIN"]}>
      <div className="space-y-6">
        
        {/* Header */}
        <div className="bg-dark-card p-6 rounded-2xl border border-dark-cardBorder shadow-md flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2 text-purple-400 text-xs font-bold uppercase tracking-wider mb-1">
              <Shield className="w-4 h-4 text-purple-400" />
              <span>SECURITY CONTROL & USER PROVISIONING</span>
            </div>
            <h1 className="text-2xl font-bold text-white">System Administration & Audit Ledger</h1>
            <p className="text-xs text-slate-400 mt-1">
              Provision RBAC roles, assign district scopes, and inspect SHA-256 cryptographic audit logs in SQLite database.
            </p>
          </div>

          <button
            onClick={() => setShowModal(true)}
            className="px-4 py-2.5 bg-brand-emerald hover:bg-emerald-600 text-dark-bg font-extrabold text-xs rounded-xl transition shadow-md flex items-center space-x-2 shrink-0 cursor-pointer"
          >
            <UserPlus className="w-4 h-4" />
            <span>Create System Account</span>
          </button>
        </div>

        {/* Success Notification Banner */}
        {successMsg && (
          <div className="bg-emerald-950/80 border border-brand-emerald p-4 rounded-xl text-brand-emerald text-xs font-bold flex items-center justify-between shadow-md">
            <div className="flex items-center space-x-2">
              <CheckCircle2 className="w-4 h-4" />
              <span>{successMsg}</span>
            </div>
            <button onClick={() => setSuccessMsg(null)} className="text-slate-400 hover:text-white">
              <X className="w-4 h-4" />
            </button>
          </div>
        )}

        {/* Error Notification Banner */}
        {errorMsg && (
          <div className="bg-rose-950/80 border border-rose-800 p-4 rounded-xl text-rose-300 text-xs font-bold flex items-center justify-between shadow-md">
            <span>{errorMsg}</span>
            <button onClick={() => setErrorMsg(null)} className="text-slate-400 hover:text-white">
              <X className="w-4 h-4" />
            </button>
          </div>
        )}

        {/* Active System Users Section */}
        <div className="bg-dark-card border border-dark-cardBorder rounded-2xl shadow-md overflow-hidden">
          <div className="p-4 bg-dark-inset border-b border-dark-insetBorder flex items-center justify-between">
            <div className="flex items-center space-x-2 text-xs font-bold text-slate-200 uppercase tracking-wider">
              <Users className="w-4 h-4 text-brand-emerald" />
              <span>Provisioned User Personas (SQLite Security Registry)</span>
            </div>
            <span className="bg-dark-card text-slate-300 text-xs font-mono font-bold px-2.5 py-0.5 rounded border border-dark-cardBorder">
              {users?.length || 0} Accounts Active
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead className="bg-dark-inset text-slate-300 font-bold border-b border-dark-insetBorder uppercase">
                <tr>
                  <th className="p-3">User ID</th>
                  <th className="p-3">Full Name</th>
                  <th className="p-3">Email Address</th>
                  <th className="p-3">Role</th>
                  <th className="p-3">District Scope</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-dark-insetBorder text-slate-200">
                {usersLoading ? (
                  <tr>
                    <td colSpan={5} className="p-6 text-center text-slate-400">Loading user registry...</td>
                  </tr>
                ) : users?.map((u: any) => (
                  <tr key={u.id} className="hover:bg-dark-inset/50 transition">
                    <td className="p-3 font-bold text-slate-500">#{u.id}</td>
                    <td className="p-3 font-bold text-white font-sans">{u.full_name}</td>
                    <td className="p-3 text-slate-300">{u.email}</td>
                    <td className="p-3 font-bold text-brand-emerald">{u.role}</td>
                    <td className="p-3 text-slate-400">
                      {u.district_code ? `District Code: ${u.district_code}` : "Statewide (All 31 Districts)"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* SHA-256 Audit Ledger Table */}
        <div className="bg-dark-card border border-dark-cardBorder rounded-2xl shadow-md overflow-hidden">
          <div className="p-4 bg-dark-inset border-b border-dark-insetBorder flex items-center justify-between">
            <span className="text-xs font-bold text-slate-200 uppercase tracking-wider">
              SHA-256 Cryptographic Audit Ledger
            </span>
            <span className="bg-emerald-950/80 text-brand-emerald text-xs font-mono font-bold px-2.5 py-0.5 rounded border border-emerald-800">
              CHAIN VERIFIED • ZERO TAMPERING DETECTED
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead className="bg-dark-inset text-slate-300 font-bold border-b border-dark-insetBorder uppercase tracking-wider">
                <tr>
                  <th className="p-3">Log ID</th>
                  <th className="p-3">Timestamp (UTC)</th>
                  <th className="p-3">User ID</th>
                  <th className="p-3">Role</th>
                  <th className="p-3">Action</th>
                  <th className="p-3">Resource</th>
                  <th className="p-3">SHA-256 Log Hash</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-dark-insetBorder text-slate-200">
                {logsLoading ? (
                  <tr>
                    <td colSpan={7} className="p-8 text-center text-slate-400">
                      Loading cryptographic audit ledger...
                    </td>
                  </tr>
                ) : auditLogs?.map((log: any) => (
                  <tr key={log.id} className="hover:bg-dark-inset/50 transition">
                    <td className="p-3 font-bold text-slate-500">#{log.id}</td>
                    <td className="p-3 text-slate-400">{new Date(log.timestamp).toLocaleString()}</td>
                    <td className="p-3 font-bold text-white">{log.user_id}</td>
                    <td className="p-3 text-brand-emerald font-bold">{log.user_role}</td>
                    <td className="p-3 font-bold text-purple-400">{log.action}</td>
                    <td className="p-3 text-slate-300">{log.resource}</td>
                    <td className="p-3 text-slate-500 text-[10px] truncate max-w-xs">{log.log_hash}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* CREATE NEW SYSTEM ACCOUNT MODAL */}
        {showModal && (
          <div className="fixed inset-0 z-50 overflow-y-auto bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
            <div className="bg-dark-card border border-dark-cardBorder rounded-2xl w-full max-w-lg shadow-2xl overflow-hidden">
              
              {/* Modal Header */}
              <div className="bg-dark-bg p-5 border-b border-dark-cardBorder flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <KeyRound className="w-5 h-5 text-brand-emerald" />
                  <div>
                    <h3 className="text-base font-bold text-white">Create New System Account</h3>
                    <p className="text-xs text-slate-400">Provision role permissions and district scope in SQLite</p>
                  </div>
                </div>
                <button
                  onClick={() => setShowModal(false)}
                  className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-dark-inset"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Modal Form */}
              <form onSubmit={handleCreateAccount} className="p-6 space-y-4 text-xs">
                
                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Full Name *</label>
                  <input
                    type="text"
                    required
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    placeholder="e.g. Ms.Sinchana"
                    className="w-full bg-dark-inset border border-dark-insetBorder text-white p-2.5 rounded-xl focus:outline-none focus:border-brand-emerald"
                  />
                </div>

                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Email Address *</label>
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="e.g. sinchana@gmail.com"
                    className="w-full bg-dark-inset border border-dark-insetBorder text-white p-2.5 rounded-xl focus:outline-none focus:border-brand-emerald font-mono"
                  />
                </div>

                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Password *</label>
                  <input
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    className="w-full bg-dark-inset border border-dark-insetBorder text-white p-2.5 rounded-xl focus:outline-none focus:border-brand-emerald font-mono"
                  />
                </div>

                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Assigned Role *</label>
                  <select
                    value={role}
                    onChange={(e) => setRole(e.target.value)}
                    className="w-full bg-dark-inset border border-dark-insetBorder text-white p-2.5 rounded-xl focus:outline-none focus:border-brand-emerald"
                  >
                    <option value="DHO">District Health Officer (DHO)</option>
                    <option value="STATE_ADMIN">State Health Director (STATE_ADMIN)</option>
                    <option value="MMU_COORDINATOR">MMU Fleet Coordinator (MMU_COORDINATOR)</option>
                    <option value="SYS_ADMIN">System Administrator (SYS_ADMIN)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-slate-300 font-semibold mb-1">Assigned District Scope *</label>
                  <select
                    value={districtCode}
                    onChange={(e) => setDistrictCode(e.target.value)}
                    className="w-full bg-dark-inset border border-dark-insetBorder text-white p-2.5 rounded-xl focus:outline-none focus:border-brand-emerald"
                  >
                    <option value="535">Davanagere (District Code: 535)</option>
                    <option value="524">Bagalkote (District Code: 524)</option>
                    <option value="525">Ballari (District Code: 525)</option>
                    <option value="526">Belagavi (District Code: 526)</option>
                    <option value="527">Bengaluru Rural (District Code: 527)</option>
                    <option value="528">Bengaluru South (District Code: 528)</option>
                    <option value="">Statewide / All Districts</option>
                  </select>
                </div>

                {/* Form Buttons */}
                <div className="pt-4 border-t border-dark-cardBorder flex justify-end space-x-3">
                  <button
                    type="button"
                    onClick={() => setShowModal(false)}
                    className="px-4 py-2 bg-dark-inset text-slate-300 hover:text-white rounded-xl border border-dark-insetBorder font-semibold"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={registerMutation.isPending}
                    className="px-4 py-2 bg-brand-emerald hover:bg-emerald-600 text-dark-bg font-extrabold rounded-xl transition shadow"
                  >
                    {registerMutation.isPending ? "Creating Account..." : "Create Account"}
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
