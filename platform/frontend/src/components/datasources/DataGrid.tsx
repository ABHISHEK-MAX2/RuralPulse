import React from 'react';
import { Database, Table, CheckCircle2, Shield, FileSpreadsheet, Server } from 'lucide-react';
import { MOCK_DATA_AVAILABILITY } from '../../lib/mockData';

export const DataGrid: React.FC = () => {
  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="p-6 bg-slate-900 border border-slate-800 rounded-2xl flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center space-x-4">
          <div className="p-3 bg-teal-500/10 border border-teal-500/30 rounded-xl text-teal-400">
            <Database className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-white flex items-center space-x-2">
              <span>11-Layer Health Domain Datasets (LGD 2026 Standardized)</span>
              <span className="px-2.5 py-0.5 text-xs font-mono bg-teal-500/20 text-teal-400 border border-teal-500/30 rounded-full">
                30,771 Villages
              </span>
            </h2>
            <p className="text-sm text-slate-400 mt-1">
              Multi-source health domain matrix connecting demographics, PHC transit, ANC checkup gaps, monsoon flood hazards, and MMU logs.
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-3 text-xs font-mono">
          <div className="px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-slate-300 flex items-center space-x-2">
            <Server className="w-4 h-4 text-emerald-400" />
            <span>SQLite krhi.db Status: ONLINE</span>
          </div>
        </div>
      </div>

      {/* Grid of 11 Layers */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {MOCK_DATA_AVAILABILITY.map((layer) => (
          <div
            key={layer.id}
            className="p-5 bg-slate-900 border border-slate-800 hover:border-teal-500/40 rounded-2xl transition-all space-y-4 shadow-lg group"
          >
            <div className="flex items-center justify-between">
              <span className="px-2.5 py-1 text-xs font-mono font-bold bg-teal-500/10 text-teal-400 border border-teal-500/20 rounded-lg">
                {layer.code}
              </span>
              <span className="flex items-center space-x-1 text-xs font-semibold text-emerald-400 bg-emerald-500/10 px-2.5 py-1 border border-emerald-500/20 rounded-lg">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>{layer.status}</span>
              </span>
            </div>

            <div>
              <h3 className="text-base font-bold text-white group-hover:text-teal-300 transition-colors">
                {layer.name}
              </h3>
              <p className="text-xs text-slate-400 mt-1">
                Standardized for all 31 districts of Karnataka under Local Government Directory (LGD) 2026.
              </p>
            </div>

            <div className="pt-3 border-t border-slate-800 flex items-center justify-between text-xs font-mono">
              <span className="text-slate-400">Total Ingested Records</span>
              <span className="font-bold text-white">{layer.records.toLocaleString()}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Sample Dataset Data Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
        <div className="p-4 border-b border-slate-800 bg-slate-900/50 flex items-center justify-between">
          <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
            <FileSpreadsheet className="w-4 h-4 text-teal-400" />
            <span>Layer 08 & Layer 01 Integrated Master Matrix Sample</span>
          </h3>
          <span className="text-xs text-slate-400 font-mono">LGD 2026 Census Schema</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-950 text-xs font-semibold text-slate-400 uppercase border-b border-slate-800">
              <tr>
                <th className="py-3.5 px-4">LGD Code</th>
                <th className="py-3.5 px-4">Village Name</th>
                <th className="py-3.5 px-4">Taluk</th>
                <th className="py-3.5 px-4">District</th>
                <th className="py-3.5 px-4">PHC Transit Dist</th>
                <th className="py-3.5 px-4">Monsoon Road Risk</th>
                <th className="py-3.5 px-4">ANC Gap (%)</th>
                <th className="py-3.5 px-4">Flood Level</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-medium">
              <tr className="hover:bg-slate-800/40 transition-colors">
                <td className="py-3.5 px-4 font-mono text-xs text-slate-400">607535</td>
                <td className="py-3.5 px-4 font-semibold text-white">Honnalli Rural</td>
                <td className="py-3.5 px-4">Honnalli</td>
                <td className="py-3.5 px-4">Davanagere</td>
                <td className="py-3.5 px-4 font-mono text-amber-400">18.5 km</td>
                <td className="py-3.5 px-4 font-mono text-red-400">SEASONAL_UNPAVED</td>
                <td className="py-3.5 px-4 font-mono text-red-400">32.4%</td>
                <td className="py-3.5 px-4 font-mono text-red-400">HIGH</td>
              </tr>
              <tr className="hover:bg-slate-800/40 transition-colors">
                <td className="py-3.5 px-4 font-mono text-xs text-slate-400">607536</td>
                <td className="py-3.5 px-4 font-semibold text-white">Nyamathi East</td>
                <td className="py-3.5 px-4">Honnalli</td>
                <td className="py-3.5 px-4">Davanagere</td>
                <td className="py-3.5 px-4 font-mono text-amber-400">14.2 km</td>
                <td className="py-3.5 px-4 font-mono text-amber-400">UNPAVED</td>
                <td className="py-3.5 px-4 font-mono text-amber-400">27.8%</td>
                <td className="py-3.5 px-4 font-mono text-amber-400">MEDIUM</td>
              </tr>
              <tr className="hover:bg-slate-800/40 transition-colors">
                <td className="py-3.5 px-4 font-mono text-xs text-slate-400">607537</td>
                <td className="py-3.5 px-4 font-semibold text-white">Harihara North</td>
                <td className="py-3.5 px-4">Harihara</td>
                <td className="py-3.5 px-4">Davanagere</td>
                <td className="py-3.5 px-4 font-mono text-emerald-400">11.0 km</td>
                <td className="py-3.5 px-4 font-mono text-emerald-400">ALL_WEATHER</td>
                <td className="py-3.5 px-4 font-mono text-amber-400">19.5%</td>
                <td className="py-3.5 px-4 font-mono text-emerald-400">LOW</td>
              </tr>
              <tr className="hover:bg-slate-800/40 transition-colors">
                <td className="py-3.5 px-4 font-mono text-xs text-slate-400">607538</td>
                <td className="py-3.5 px-4 font-semibold text-white">Channagiri South</td>
                <td className="py-3.5 px-4">Channagiri</td>
                <td className="py-3.5 px-4">Davanagere</td>
                <td className="py-3.5 px-4 font-mono text-emerald-400">7.5 km</td>
                <td className="py-3.5 px-4 font-mono text-emerald-400">ALL_WEATHER</td>
                <td className="py-3.5 px-4 font-mono text-emerald-400">14.2%</td>
                <td className="py-3.5 px-4 font-mono text-emerald-400">LOW</td>
              </tr>
              <tr className="hover:bg-slate-800/40 transition-colors">
                <td className="py-3.5 px-4 font-mono text-xs text-slate-400">607539</td>
                <td className="py-3.5 px-4 font-semibold text-white">Jagalur West</td>
                <td className="py-3.5 px-4">Jagalur</td>
                <td className="py-3.5 px-4">Davanagere</td>
                <td className="py-3.5 px-4 font-mono text-emerald-400">4.0 km</td>
                <td className="py-3.5 px-4 font-mono text-emerald-400">ALL_WEATHER</td>
                <td className="py-3.5 px-4 font-mono text-emerald-400">8.1%</td>
                <td className="py-3.5 px-4 font-mono text-emerald-400">LOW</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
