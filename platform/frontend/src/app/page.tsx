'use client';

import React, { useState } from 'react';
import { Shield, Activity, Map, Database, UserCheck, Heart } from 'lucide-react';
import { ExecutiveDashboard } from '../components/dashboard/ExecutiveDashboard';
import { AdminView } from '../components/admin/AdminView';
import { MapIntelligence } from '../components/map/MapIntelligence';
import { DataGrid } from '../components/datasources/DataGrid';

export default function Home() {
  const [activeView, setActiveView] = useState<'dashboard' | 'map' | 'datasources' | 'admin'>('dashboard');

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans antialiased selection:bg-teal-500 selection:text-slate-950">
      
      {/* Navigation Header */}
      <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          
          {/* Logo & Platform Name */}
          <div className="flex items-center space-x-3">
            <div className="p-2.5 bg-teal-500/10 border border-teal-500/30 rounded-xl text-teal-400">
              <Heart className="w-6 h-6 fill-teal-500/20" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h1 className="text-lg font-bold text-white tracking-tight">Karnataka Rural Healthcare Intelligence</h1>
                <span className="px-2 py-0.5 text-[10px] font-bold font-mono bg-teal-500/20 text-teal-400 border border-teal-500/30 rounded-full">
                  LGD 2026
                </span>
              </div>
              <p className="text-xs text-slate-400">AI-Powered Decision Support & MMU Fleet Routing • Govt of Karnataka</p>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="flex items-center space-x-2 bg-slate-950/60 p-1.5 border border-slate-800 rounded-xl text-xs font-semibold">
            <button
              onClick={() => setActiveView('dashboard')}
              className={`px-4 py-2 rounded-lg flex items-center space-x-2 transition-all ${
                activeView === 'dashboard' ? 'bg-teal-500 text-slate-950 font-bold shadow-md shadow-teal-500/20' : 'text-slate-400 hover:text-white'
              }`}
            >
              <Activity className="w-4 h-4" />
              <span>Executive Dashboard</span>
            </button>
            <button
              onClick={() => setActiveView('map')}
              className={`px-4 py-2 rounded-lg flex items-center space-x-2 transition-all ${
                activeView === 'map' ? 'bg-teal-500 text-slate-950 font-bold shadow-md shadow-teal-500/20' : 'text-slate-400 hover:text-white'
              }`}
            >
              <Map className="w-4 h-4" />
              <span>Geospatial Map</span>
            </button>
            <button
              onClick={() => setActiveView('datasources')}
              className={`px-4 py-2 rounded-lg flex items-center space-x-2 transition-all ${
                activeView === 'datasources' ? 'bg-teal-500 text-slate-950 font-bold shadow-md shadow-teal-500/20' : 'text-slate-400 hover:text-white'
              }`}
            >
              <Database className="w-4 h-4" />
              <span>11-Layer Data Grid</span>
            </button>
            <button
              onClick={() => setActiveView('admin')}
              className={`px-4 py-2 rounded-lg flex items-center space-x-2 transition-all ${
                activeView === 'admin' ? 'bg-teal-500 text-slate-950 font-bold shadow-md shadow-teal-500/20' : 'text-slate-400 hover:text-white'
              }`}
            >
              <UserCheck className="w-4 h-4" />
              <span>User Administration</span>
            </button>
          </nav>

          {/* User Profile Badge */}
          <div className="flex items-center space-x-3 text-xs">
            <div className="text-right">
              <div className="font-semibold text-white">Ms. Sinchana Urs</div>
              <div className="text-teal-400 font-mono text-[11px]">System Administrator</div>
            </div>
            <div className="w-9 h-9 bg-teal-500/20 border border-teal-500/40 rounded-full flex items-center justify-center text-teal-400 font-bold">
              SU
            </div>
          </div>

        </div>
      </header>

      {/* Main Content Area */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {activeView === 'dashboard' && <ExecutiveDashboard />}
        {activeView === 'admin' && <AdminView />}
        {activeView === 'map' && <MapIntelligence />}
        {activeView === 'datasources' && <DataGrid />}
      </main>

    </div>
  );
}
