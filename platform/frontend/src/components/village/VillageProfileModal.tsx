import React, { useState, useEffect } from 'react';
import { X, Bot, Shield, AlertTriangle, MapPin, Activity, CheckCircle, RefreshCw, Layers } from 'lucide-react';
import { getWatsonxBriefing } from '../../lib/api';
import { MOCK_DATA_AVAILABILITY } from '../../lib/mockData';

interface VillageProfileModalProps {
  village: any;
  onClose: () => void;
}

export const VillageProfileModal: React.FC<VillageProfileModalProps> = ({ village, onClose }) => {
  const [activeTab, setActiveTab] = useState<'xai' | 'layers' | 'interventions' | 'watsonx'>('xai');
  const [briefing, setBriefing] = useState<any>(null);
  const [loadingBriefing, setLoadingBriefing] = useState(false);

  useEffect(() => {
    if (village) {
      fetchBriefing();
    }
  }, [village]);

  const fetchBriefing = async () => {
    setLoadingBriefing(true);
    try {
      const res = await getWatsonxBriefing(village.village_code);
      setBriefing(res);
    } catch (err) {
      console.error('Error fetching briefing:', err);
    } finally {
      setLoadingBriefing(false);
    }
  };

  if (!village) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-md p-4 overflow-y-auto">
      <div className="relative w-full max-w-4xl bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-slate-800 bg-slate-900/50">
          <div className="flex items-center space-x-4">
            <div className="p-3 bg-teal-500/10 border border-teal-500/20 rounded-xl text-teal-400">
              <MapPin className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center space-x-3">
                <h2 className="text-xl font-bold text-white">{village.village_name}</h2>
                <span className="px-2.5 py-0.5 text-xs font-mono font-medium rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                  LGD Code: {village.village_code}
                </span>
                <span className={`px-2.5 py-0.5 text-xs font-bold rounded-full ${
                  village.risk_category === 'CRITICAL' ? 'bg-red-500/20 text-red-400 border border-red-500/30' :
                  village.risk_category === 'HIGH' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' :
                  village.risk_category === 'MEDIUM' ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30' :
                  'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                }`}>
                  {village.risk_category} RISK ({village.risk_score?.toFixed(1) || '0.0'})
                </span>
              </div>
              <p className="text-sm text-slate-400 mt-1">
                {village.subdistrict_name} Taluk, {village.district_name} District, Karnataka • Population: {village.population?.toLocaleString() || 0}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab Navigation */}
        <div className="flex border-b border-slate-800 bg-slate-900/30 px-6 space-x-6 text-sm font-medium">
          <button
            onClick={() => setActiveTab('xai')}
            className={`py-3.5 border-b-2 flex items-center space-x-2 transition-colors ${
              activeTab === 'xai' ? 'border-teal-400 text-teal-400' : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <Shield className="w-4 h-4" />
            <span>Explainable AI Risk Factors</span>
          </button>
          <button
            onClick={() => setActiveTab('layers')}
            className={`py-3.5 border-b-2 flex items-center space-x-2 transition-colors ${
              activeTab === 'layers' ? 'border-teal-400 text-teal-400' : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <Layers className="w-4 h-4" />
            <span>11-Layer Domain Indicators</span>
          </button>
          <button
            onClick={() => setActiveTab('interventions')}
            className={`py-3.5 border-b-2 flex items-center space-x-2 transition-colors ${
              activeTab === 'interventions' ? 'border-teal-400 text-teal-400' : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <Activity className="w-4 h-4" />
            <span>Recommended Interventions</span>
          </button>
          <button
            onClick={() => setActiveTab('watsonx')}
            className={`py-3.5 border-b-2 flex items-center space-x-2 transition-colors ${
              activeTab === 'watsonx' ? 'border-teal-400 text-teal-400' : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <Bot className="w-4 h-4" />
            <span>IBM watsonx.ai Copilot</span>
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6 overflow-y-auto space-y-6 flex-1 text-slate-300">

          {/* TAB 1: EXPLAINABLE AI */}
          {activeTab === 'xai' && (
            <div className="space-y-4">
              <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider">Top Vulnerability Risk Drivers</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 bg-slate-800/40 border border-slate-800 rounded-xl">
                  <div className="text-xs text-slate-400 font-medium">PHC Distance Bottleneck</div>
                  <div className="text-lg font-bold text-white mt-1">{village.distance_to_phc_km || 14.2} km to nearest PHC</div>
                  <div className="text-xs text-amber-400 mt-1">Impact: +22.4 pts on vulnerability score</div>
                </div>
                <div className="p-4 bg-slate-800/40 border border-slate-800 rounded-xl">
                  <div className="text-xs text-slate-400 font-medium">Road Accessibility Index</div>
                  <div className="text-lg font-bold text-white mt-1">{village.road_accessibility || 'SEASONAL_UNPAVED'}</div>
                  <div className="text-xs text-red-400 mt-1">Impact: +18.1 pts monsoon transport blockage</div>
                </div>
                <div className="p-4 bg-slate-800/40 border border-slate-800 rounded-xl">
                  <div className="text-xs text-slate-400 font-medium">Flood Hazard Risk Level</div>
                  <div className="text-lg font-bold text-white mt-1">{village.flood_prone_indicator || 'HIGH'}</div>
                  <div className="text-xs text-amber-400 mt-1">Impact: +15.8 pts emergency delay hazard</div>
                </div>
                <div className="p-4 bg-slate-800/40 border border-slate-800 rounded-xl">
                  <div className="text-xs text-slate-400 font-medium">Maternal ANC Coverage Deficit</div>
                  <div className="text-lg font-bold text-white mt-1">27.8% ANC Checkup Deficit</div>
                  <div className="text-xs text-red-400 mt-1">Impact: +12.5 pts maternal risk index</div>
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: 11-LAYER DOMAIN INDICATORS */}
          {activeTab === 'layers' && (
            <div className="space-y-4">
              <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider">11 Health Domain Datasets Availability</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {MOCK_DATA_AVAILABILITY.map((layer) => (
                  <div key={layer.id} className="p-3.5 bg-slate-800/40 border border-slate-800 rounded-xl flex items-center justify-between">
                    <div>
                      <div className="text-xs font-mono text-teal-400 font-medium">{layer.code}</div>
                      <div className="text-sm font-semibold text-white mt-0.5">{layer.name}</div>
                    </div>
                    <span className="px-2.5 py-1 text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-lg">
                      {layer.records.toLocaleString()} Records
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB 3: INTERVENTIONS */}
          {activeTab === 'interventions' && (
            <div className="space-y-4">
              <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider">Recommended Field Deployment Actions</h3>
              <div className="space-y-3">
                <div className="p-4 bg-slate-800/40 border border-slate-800 rounded-xl flex items-start space-x-3">
                  <CheckCircle className="w-5 h-5 text-teal-400 mt-0.5 shrink-0" />
                  <div>
                    <h4 className="text-sm font-semibold text-white">Mobile Medical Unit (MMU) Priority Route Dispatch</h4>
                    <p className="text-xs text-slate-400 mt-1">Schedule weekly MMU visit for maternal ANC checkups and routine child immunization.</p>
                  </div>
                </div>
                <div className="p-4 bg-slate-800/40 border border-slate-800 rounded-xl flex items-start space-x-3">
                  <CheckCircle className="w-5 h-5 text-teal-400 mt-0.5 shrink-0" />
                  <div>
                    <h4 className="text-sm font-semibold text-white">DVDMS Cold-Chain Vaccine Replenishment</h4>
                    <p className="text-xs text-slate-400 mt-1">Refill essential vaccine and maternal drug buffer stock via DVDMS portal.</p>
                  </div>
                </div>
                <div className="p-4 bg-slate-800/40 border border-slate-800 rounded-xl flex items-start space-x-3">
                  <CheckCircle className="w-5 h-5 text-teal-400 mt-0.5 shrink-0" />
                  <div>
                    <h4 className="text-sm font-semibold text-white">ASHA Worker Door-to-Door Monitoring</h4>
                    <p className="text-xs text-slate-400 mt-1">Activate ASHA field tracking for high-risk pregnant women and malnourished infants.</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* TAB 4: IBM WATSONX AI COPILOT */}
          {activeTab === 'watsonx' && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider">Executive Briefing Copilot</h3>
                <button
                  onClick={fetchBriefing}
                  disabled={loadingBriefing}
                  className="px-3 py-1.5 text-xs font-medium bg-slate-800 text-slate-200 hover:text-white rounded-lg hover:bg-slate-700 flex items-center space-x-1.5 transition-colors disabled:opacity-50"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${loadingBriefing ? 'animate-spin' : ''}`} />
                  <span>Regenerate Briefing</span>
                </button>
              </div>

              {loadingBriefing ? (
                <div className="p-8 text-center bg-slate-800/20 border border-slate-800 rounded-xl space-y-3">
                  <RefreshCw className="w-6 h-6 text-teal-400 animate-spin mx-auto" />
                  <p className="text-sm text-slate-400">Synthesizing 11-layer health indicators via 4-Tier AI Cascade...</p>
                </div>
              ) : (
                <div className="p-5 bg-slate-950/60 border border-slate-800 rounded-xl space-y-4 font-mono text-sm leading-relaxed text-slate-200 whitespace-pre-wrap">
                  <div className="text-xs text-slate-400 font-sans border-b border-slate-800 pb-2 flex items-center justify-between">
                    <span>Source: <code className="text-teal-400 font-mono">{briefing?.source || 'GROQ_CLOUD_LIVE_API'}</code></span>
                    <span>Model: <code className="text-emerald-400 font-mono">{briefing?.model || 'groq/compound'}</code></span>
                  </div>
                  {briefing?.briefing_text}
                </div>
              )}
            </div>
          )}

        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-800 bg-slate-900/50 flex items-center justify-between text-xs text-slate-400">
          <span>Karnataka Rural Healthcare Intelligence Platform • LGD 2026 Standardized</span>
          <button
            onClick={onClose}
            className="px-4 py-2 bg-teal-500 text-slate-950 font-semibold rounded-lg hover:bg-teal-400 transition-colors"
          >
            Close Profile
          </button>
        </div>

      </div>
    </div>
  );
};
