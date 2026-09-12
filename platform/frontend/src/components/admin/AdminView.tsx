import React, { useState, useEffect } from 'react';
import { UserPlus, Shield, CheckCircle, AlertCircle, X, Lock, Mail, User as UserIcon } from 'lucide-react';
import { getAdminUsers, createAdminUser } from '../../lib/api';

export const AdminView: React.FC = () => {
  const [users, setUsers] = useState<any[]>([]);
  const [showModal, setShowModal] = useState(false);

  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('district_health_officer');
  const [districtScope, setDistrictScope] = useState('535');
  const [message, setMessage] = useState<{ text: string; isError: boolean } | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    const data = await getAdminUsers();
    setUsers(data || []);
  };

  const handleCreateAccount = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);

    try {
      const res = await createAdminUser({
        full_name: fullName,
        email: email,
        password: password,
        role: role,
        district_code: districtScope ? parseInt(districtScope, 10) : undefined
      });

      if (res && res.id) {
        setMessage({ text: `Account for ${res.full_name} created successfully!`, isError: false });
        setShowModal(false);
        setFullName('');
        setEmail('');
        setPassword('');
        loadUsers();
      } else {
        setMessage({ text: 'Failed to create account. Please try again.', isError: true });
      }
    } catch (err: any) {
      setMessage({ text: err.message || 'Error provisioning account', isError: true });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Admin Header */}
      <div className="p-6 bg-slate-900 border border-slate-800 rounded-2xl flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center space-x-2">
            <Shield className="w-5 h-5 text-teal-400" />
            <span>System User Administration & Role Provisioning</span>
          </h2>
          <p className="text-sm text-slate-400 mt-1">Manage system administrators, District Health Officers (DHO), and MMU Coordinators across Karnataka districts.</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="px-4 py-2.5 bg-teal-500 text-slate-950 font-bold rounded-xl hover:bg-teal-400 transition-colors flex items-center space-x-2 shadow-lg shadow-teal-500/20"
        >
          <UserPlus className="w-4 h-4" />
          <span>Create New System Account</span>
        </button>
      </div>

      {message && (
        <div className={`p-4 rounded-xl border text-sm font-medium flex items-center justify-between ${
          message.isError ? 'bg-red-500/10 text-red-400 border-red-500/30' : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
        }`}>
          <span>{message.text}</span>
          <button onClick={() => setMessage(null)} className="text-slate-400 hover:text-white">
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* Accounts Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
        <div className="p-4 border-b border-slate-800 bg-slate-900/50">
          <h3 className="text-sm font-bold text-white uppercase tracking-wider">Provisioned System Users ({users.length})</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-950 text-xs font-semibold text-slate-400 uppercase border-b border-slate-800">
              <tr>
                <th className="py-3.5 px-4">User ID</th>
                <th className="py-3.5 px-4">Full Name</th>
                <th className="py-3.5 px-4">Email Address</th>
                <th className="py-3.5 px-4">Assigned Role</th>
                <th className="py-3.5 px-4">District Scope</th>
                <th className="py-3.5 px-4">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-medium">
              {users.map((u) => (
                <tr key={u.id} className="hover:bg-slate-800/40 transition-colors">
                  <td className="py-3.5 px-4 font-mono text-xs text-slate-400">#{u.id}</td>
                  <td className="py-3.5 px-4 font-semibold text-white">{u.full_name}</td>
                  <td className="py-3.5 px-4 text-slate-300">{u.email}</td>
                  <td className="py-3.5 px-4">
                    <span className="px-2.5 py-1 text-xs font-semibold bg-teal-500/10 text-teal-400 border border-teal-500/20 rounded-lg">
                      {u.role}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 font-mono text-xs text-slate-400">
                    {u.district_code ? `District #${u.district_code}` : 'Statewide (All Districts)'}
                  </td>
                  <td className="py-3.5 px-4">
                    <span className="px-2 py-0.5 text-xs font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 rounded-full">
                      ACTIVE
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Account Creation Centered Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-md p-4">
          <div className="relative w-full max-w-lg bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden p-6 space-y-6">
            
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <h3 className="text-lg font-bold text-white flex items-center space-x-2">
                <UserPlus className="w-5 h-5 text-teal-400" />
                <span>Create New System Account</span>
              </h3>
              <button onClick={() => setShowModal(false)} className="text-slate-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleCreateAccount} className="space-y-4 text-sm">
              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">Full Name *</label>
                <div className="relative">
                  <UserIcon className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
                  <input
                    type="text"
                    required
                    placeholder="Ms.Sinchana"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    className="w-full pl-10 pr-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-white focus:outline-none focus:border-teal-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">Email Address *</label>
                <div className="relative">
                  <Mail className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
                  <input
                    type="email"
                    required
                    placeholder="sinchana@gmail.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full pl-10 pr-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-white focus:outline-none focus:border-teal-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">Password *</label>
                <div className="relative">
                  <Lock className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
                  <input
                    type="password"
                    required
                    placeholder="••••••••"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full pl-10 pr-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-white focus:outline-none focus:border-teal-500"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">Assigned Role *</label>
                <select
                  value={role}
                  onChange={(e) => setRole(e.target.value)}
                  className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-white focus:outline-none focus:border-teal-500"
                >
                  <option value="district_health_officer">District Health Officer (DHO)</option>
                  <option value="mmu_coordinator">MMU Coordinator</option>
                  <option value="state_health_administrator">State Health Administrator</option>
                  <option value="system_administrator">System Administrator</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-400 mb-1">Assigned District Scope *</label>
                <select
                  value={districtScope}
                  onChange={(e) => setDistrictScope(e.target.value)}
                  className="w-full px-4 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-white focus:outline-none focus:border-teal-500"
                >
                  <option value="535">Davanagere (535)</option>
                  <option value="524">Bagalkote (524)</option>
                  <option value="525">Ballari (525)</option>
                  <option value="526">Belagavi (526)</option>
                  <option value="527">Bengaluru Rural (527)</option>
                  <option value="528">Bengaluru Urban (528)</option>
                  <option value="529">Bidar (529)</option>
                  <option value="530">Chamarajanagar (530)</option>
                  <option value="531">Chikkaballapura (531)</option>
                  <option value="532">Chikkamagaluru (532)</option>
                  <option value="533">Chitradurga (533)</option>
                  <option value="534">Dakshina Kannada (534)</option>
                </select>
              </div>

              <div className="flex items-center justify-end space-x-3 pt-4 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 bg-slate-800 text-slate-300 hover:text-white rounded-xl text-xs font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="px-5 py-2 bg-teal-500 text-slate-950 font-bold rounded-xl hover:bg-teal-400 transition-colors text-xs disabled:opacity-50"
                >
                  {loading ? 'Creating...' : 'Create Account'}
                </button>
              </div>
            </form>

          </div>
        </div>
      )}

    </div>
  );
};
