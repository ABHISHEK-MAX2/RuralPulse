import React, { useState } from 'react';
import { Map, Layers, Filter, Eye, ShieldAlert, AlertTriangle, Activity, CheckCircle } from 'lucide-react';
import { MOCK_VILLAGES } from '../../lib/mockData';

export const MapIntelligence: React.FC = () => {
  const [selectedFilter, setSelectedFilter] = useState<string>('ALL');
  const [activeVillage, setActiveVillage] = useState<any | null>(MOCK_VILLAGES[0]);

  const filteredVillages = MOCK_VILLAGES.filter(v => 
    selectedFilter === 'ALL' || v.risk_category === selectedFilter
  );

  return (
    <div className="space-y-6">
      
      {/* Map Control Bar */}
      <div className="p-4 bg-slate-900 border border-slate-800 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 bg-teal-500/10 border border-teal-500/30 rounded-xl text-teal-400">
            <Map className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-white uppercase tracking-wider">Geospatial Map Intelligence & Risk Layers</h3>
            <p className="text-xs text-slate-400">30,771 villages mapped across 31 Karnataka districts with 11-layer GIS overlays.</p>
          </div>
        </div>

        {/* Risk Filter Badges */}
        <div className="flex items-center space-x-2">
          <Filter className="w-4 h-4 text-slate-400 mr-1" />
          <span className="text-xs text-slate-400 font-medium mr-2">Filter Risk Pins:</span>
          {['ALL', 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'].map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedFilter(cat)}
              className={`px-3 py-1.5 text-xs font-semibold rounded-xl border transition-all ${
                selectedFilter === cat
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

      {/* Map Main Grid View */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Visual Map Simulator View */}
        <div className="lg:col-span-2 relative bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden h-[540px] flex flex-col">
          
          {/* Simulated Map Canvas Header */}
          <div className="p-3 bg-slate-950/80 border-b border-slate-800 flex items-center justify-between text-xs text-slate-400 font-mono">
            <span className="flex items-center space-x-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span>MapLibre GL GIS Layer: Karnataka State (LGD 2026)</span>
            </span>
            <span>Zoom Level: 10.5 | Center: 14.44° N, 75.64° E</span>
          </div>

          {/* Map Simulation Container */}
          <div className="relative flex-1 bg-[radial-gradient(#1e293b_1px,transparent_1px)] [background-size:16px_16px] bg-slate-950 p-6 flex flex-col justify-between">
            
            {/* Overlay Map Pins */}
            <div className="absolute inset-0 p-8 grid grid-cols-3 gap-8 items-center justify-center">
              {filteredVillages.map((v) => (
                <button
                  key={v.village_code}
                  onClick={() => setActiveVillage(v)}
                  className={`relative group p-4 rounded-2xl border backdrop-blur-md text-left transition-all hover:scale-105 shadow-xl ${
                    v.risk_category === 'CRITICAL' ? 'bg-red-500/10 border-red-500/40 hover:border-red-500' :
                    v.risk_category === 'HIGH' ? 'bg-amber-500/10 border-amber-500/40 hover:border-amber-500' :
                    v.risk_category === 'MEDIUM' ? 'bg-blue-500/10 border-blue-500/40 hover:border-blue-500' :
                    'bg-emerald-500/10 border-emerald-500/40 hover:border-emerald-500'
                  } ${activeVillage?.village_code === v.village_code ? 'ring-2 ring-teal-400 ring-offset-2 ring-offset-slate-950' : ''}`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-bold text-white text-sm">{v.village_name}</span>
                    <span className={`w-3 h-3 rounded-full ${
                      v.risk_category === 'CRITICAL' ? 'bg-red-500 shadow-lg shadow-red-500/50' :
                      v.risk_category === 'HIGH' ? 'bg-amber-500 shadow-lg shadow-amber-500/50' :
                      v.risk_category === 'MEDIUM' ? 'bg-blue-500 shadow-lg shadow-blue-500/50' :
                      'bg-emerald-500 shadow-lg shadow-emerald-500/50'
                    }`}></span>
                  </div>
                  <div className="text-xs text-slate-400 font-mono">LGD #{v.village_code}</div>
                  <div className="text-xs font-semibold text-slate-300 mt-1">{v.distance_to_phc_km} km to PHC</div>
                </button>
              ))}
            </div>

            {/* Map Legend Footer */}
            <div className="relative z-10 p-3 bg-slate-900/90 border border-slate-800 rounded-xl flex items-center justify-around text-xs font-semibold">
              <span className="flex items-center space-x-2 text-red-400">
                <span className="w-3 h-3 rounded-full bg-red-500"></span>
                <span>🔴 CRITICAL (≥ 75.0)</span>
              </span>
              <span className="flex items-center space-x-2 text-amber-400">
                <span className="w-3 h-3 rounded-full bg-amber-500"></span>
                <span>🟡 HIGH (60.0-74.9)</span>
              </span>
              <span className="flex items-center space-x-2 text-blue-400">
                <span className="w-3 h-3 rounded-full bg-blue-500"></span>
                <span>🔵 MEDIUM (40.0-59.9)</span>
              </span>
              <span className="flex items-center space-x-2 text-emerald-400">
                <span className="w-3 h-3 rounded-full bg-emerald-500"></span>
                <span>🟢 LOW (&lt; 40.0)</span>
              </span>
            </div>

          </div>

        </div>

        {/* Selected Village Info Panel */}
        {activeVillage && (
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-5 h-[540px] flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between border-b border-slate-800 pb-4">
                <div>
                  <span className="text-xs font-mono text-teal-400 font-medium">SELECTED MAP PIN</span>
                  <h4 className="text-lg font-bold text-white mt-0.5">{activeVillage.village_name}</h4>
                  <p className="text-xs text-slate-400">{activeVillage.subdistrict_name} Taluk, {activeVillage.district_name}</p>
                </div>
                <span className={`px-2.5 py-1 text-xs font-bold rounded-full ${
                  activeVillage.risk_category === 'CRITICAL' ? 'bg-red-500/20 text-red-400 border border-red-500/30' :
                  activeVillage.risk_category === 'HIGH' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' :
                  activeVillage.risk_category === 'MEDIUM' ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30' :
                  'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                }`}>
                  {activeVillage.risk_category} ({activeVillage.risk_score})
                </span>
              </div>

              <div className="space-y-3 mt-4 text-xs">
                <div className="p-3 bg-slate-950/60 border border-slate-800 rounded-xl flex justify-between">
                  <span className="text-slate-400">LGD Village Code</span>
                  <span className="font-mono text-white">{activeVillage.village_code}</span>
                </div>
                <div className="p-3 bg-slate-950/60 border border-slate-800 rounded-xl flex justify-between">
                  <span className="text-slate-400">PHC Distance</span>
                  <span className="font-mono text-white">{activeVillage.distance_to_phc_km} km ({activeVillage.travel_time_to_phc_minutes}m)</span>
                </div>
                <div className="p-3 bg-slate-950/60 border border-slate-800 rounded-xl flex justify-between">
                  <span className="text-slate-400">Road Transport Access</span>
                  <span className="font-mono text-white">{activeVillage.road_accessibility}</span>
                </div>
                <div className="p-3 bg-slate-950/60 border border-slate-800 rounded-xl flex justify-between">
                  <span className="text-slate-400">Flood Hazard Level</span>
                  <span className="font-mono text-white">{activeVillage.flood_prone_indicator}</span>
                </div>
                <div className="p-3 bg-slate-950/60 border border-slate-800 rounded-xl flex justify-between">
                  <span className="text-slate-400">Total Population</span>
                  <span className="font-mono text-white">{activeVillage.population?.toLocaleString()}</span>
                </div>
              </div>
            </div>

            <div className="p-4 bg-teal-500/10 border border-teal-500/20 rounded-xl text-xs space-y-2 text-slate-300">
              <span className="font-bold text-teal-400 uppercase tracking-wider block">Recommended Action</span>
              <p>Mobile Medical Unit (MMU) priority dispatch recommended for ANC checkup camp and cold-chain vaccine replenishment.</p>
            </div>
          </div>
        )}

      </div>

    </div>
  );
};
