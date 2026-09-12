import React, { useState, useEffect } from 'react';
import { Search, Filter, ShieldAlert, AlertTriangle, Activity, CheckCircle, Eye, MapPin } from 'lucide-react';
import { getVillages } from '../../lib/api';
import { VillageProfileModal } from '../village/VillageProfileModal';

export const ExecutiveDashboard: React.FC = () => {
  const [villages, setVillages] = useState<any[]>([]);
  const [selectedRiskCategory, setSelectedRiskCategory] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedVillage, setSelectedVillage] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchVillages();
  }, [selectedRiskCategory]);

  const fetchVillages = async () => {
    setLoading(true);
    try {
      const res = await getVillages(100, selectedRiskCategory);
      setVillages(res?.items || []);
    } catch (err) {
      console.error('Error fetching villages:', err);
    } finally {
      setLoading(false);
    }
  };

  const filteredVillages = villages.filter(v => 
    v.village_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    v.subdistrict_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    v.district_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    String(v.village_code).includes(searchQuery)
  );

  return (
    <div className="space-y-6">
      
      {/* Top Priority Metrics Header */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="p-5 bg-slate-900 border border-slate-800 rounded-2xl flex items-center justify-between">
          <div>
            <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Critical Risk Villages</div>
            <div className="text-2xl font-bold text-red-400 mt-1">2 Villages</div>
            <div className="text-xs text-slate-400 mt-1">Score ≥ 75.0 (Immediate MMU Dispatch)</div>
          </div>
          <div className="p-3 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400">
            <ShieldAlert className="w-6 h-6" />
          </div>
        </div>

        <div className="p-5 bg-slate-900 border border-slate-800 rounded-2xl flex items-center justify-between">
          <div>
            <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">High Risk Villages</div>
            <div className="text-2xl font-bold text-amber-400 mt-1">1 Village</div>
            <div className="text-xs text-slate-400 mt-1">Score 60.0 - 74.9</div>
          </div>
          <div className="p-3 bg-amber-500/10 border border-amber-500/20 rounded-xl text-amber-400">
            <AlertTriangle className="w-6 h-6" />
          </div>
        </div>

        <div className="p-5 bg-slate-900 border border-slate-800 rounded-2xl flex items-center justify-between">
          <div>
            <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Medium Risk Villages</div>
            <div className="text-2xl font-bold text-blue-400 mt-1">1 Village</div>
            <div className="text-xs text-slate-400 mt-1">Score 40.0 - 59.9</div>
          </div>
          <div className="p-3 bg-blue-500/10 border border-blue-500/20 rounded-xl text-blue-400">
            <Activity className="w-6 h-6" />
          </div>
        </div>

        <div className="p-5 bg-slate-900 border border-slate-800 rounded-2xl flex items-center justify-between">
          <div>
            <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Low Risk Villages</div>
            <div className="text-2xl font-bold text-emerald-400 mt-1">1 Village</div>
            <div className="text-xs text-slate-400 mt-1">Score &lt; 40.0</div>
          </div>
          <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-400">
            <CheckCircle className="w-6 h-6" />
          </div>
        </div>
      </div>

      {/* Control Bar & Risk Category Filter Badges */}
      <div className="p-4 bg-slate-900 border border-slate-800 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        
        {/* Search */}
        <div className="relative flex-1 max-w-md">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
          <input
            type="text"
            placeholder="Search village name, LGD code, taluk, or district..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-slate-950 border border-slate-800 rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:border-teal-500 transition-colors"
          />
        </div>

        {/* Risk Category Badges Filter */}
        <div className="flex items-center space-x-2">
          <Filter className="w-4 h-4 text-slate-400 mr-1" />
          <span className="text-xs text-slate-400 font-medium mr-2">Filter Risk:</span>

          {['ALL', 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'].map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedRiskCategory(cat)}
              className={`px-3 py-1.5 text-xs font-semibold rounded-xl border transition-all ${
                selectedRiskCategory === cat
                  ? cat === 'CRITICAL' ? 'bg-red-500/20 text-red-400 border-red-500/50' :
                    cat === 'HIGH' ? 'bg-amber-500/20 text-amber-400 border-amber-500/50' :
                    cat === 'MEDIUM' ? 'bg-blue-500/20 text-blue-400 border-blue-500/50' :
                    cat === 'LOW' ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/50' :
                    'bg-teal-500/20 text-teal-400 border-teal-500/50'
                  : 'bg-slate-950 text-slate-400 border-slate-800 hover:text-white'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Villages Priority Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
        <div className="p-4 border-b border-slate-800 bg-slate-900/50 flex items-center justify-between">
          <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
            <MapPin className="w-4 h-4 text-teal-400" />
            <span>Priority Village Vulnerability Ranking (LGD 2026)</span>
          </h3>
          <span className="text-xs text-slate-400 font-mono">Showing {filteredVillages.length} Villages</span>
        </div>

        {loading ? (
          <div className="p-12 text-center text-slate-400 text-sm">Loading priority village vulnerability matrix...</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-300">
              <thead className="bg-slate-950 text-xs font-semibold text-slate-400 uppercase border-b border-slate-800">
                <tr>
                  <th className="py-3.5 px-4">LGD Code</th>
                  <th className="py-3.5 px-4">Village Name</th>
                  <th className="py-3.5 px-4">Taluk & District</th>
                  <th className="py-3.5 px-4">Population</th>
                  <th className="py-3.5 px-4">PHC Distance</th>
                  <th className="py-3.5 px-4">Road Access</th>
                  <th className="py-3.5 px-4">Risk Category</th>
                  <th className="py-3.5 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-medium">
                {filteredVillages.map((v) => (
                  <tr key={v.village_code} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-3.5 px-4 font-mono text-xs text-slate-400">{v.village_code}</td>
                    <td className="py-3.5 px-4 font-semibold text-white">{v.village_name}</td>
                    <td className="py-3.5 px-4 text-slate-400">{v.subdistrict_name}, {v.district_name}</td>
                    <td className="py-3.5 px-4 font-mono">{v.population?.toLocaleString() || 0}</td>
                    <td className="py-3.5 px-4 font-mono">{v.distance_to_phc_km || 0} km ({v.travel_time_to_phc_minutes || 0}m)</td>
                    <td className="py-3.5 px-4 text-xs font-mono">{v.road_accessibility || 'ALL_WEATHER'}</td>
                    <td className="py-3.5 px-4">
                      <span className={`px-2.5 py-1 text-xs font-bold rounded-full border ${
                        v.risk_category === 'CRITICAL' ? 'bg-red-500/20 text-red-400 border-red-500/30' :
                        v.risk_category === 'HIGH' ? 'bg-amber-500/20 text-amber-400 border-amber-500/30' :
                        v.risk_category === 'MEDIUM' ? 'bg-blue-500/20 text-blue-400 border-blue-500/30' :
                        'bg-emerald-500/20 text-emerald-400 border-emerald-500/30'
                      }`}>
                        {v.risk_category} ({v.risk_score?.toFixed(1) || '0.0'})
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-right">
                      <button
                        onClick={() => setSelectedVillage(v)}
                        className="px-3 py-1.5 bg-teal-500/10 text-teal-400 hover:bg-teal-500/20 border border-teal-500/30 rounded-lg text-xs font-semibold transition-colors flex items-center space-x-1 ml-auto"
                      >
                        <Eye className="w-3.5 h-3.5" />
                        <span>View XAI Profile</span>
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Village Intelligence Modal */}
      {selectedVillage && (
        <VillageProfileModal
          village={selectedVillage}
          onClose={() => setSelectedVillage(null)}
        />
      )}

    </div>
  );
};
