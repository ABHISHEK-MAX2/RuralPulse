"use client";

import React, { useState } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { apiService } from "@/lib/api";
import { useAuth } from "@/lib/AuthContext";
import { FileText, Download, FileSpreadsheet } from "lucide-react";

import { RoleGuard } from "@/components/shell/RoleGuard";

export default function ReportsPage() {
  const { selectedDistrict } = useAuth();
  const [reportType, setReportType] = useState<string>("DISTRICT_HEALTH_REPORT");
  const [format, setFormat] = useState<string>("PDF");
  const [districtCode, setDistrictCode] = useState<number>(selectedDistrict || 524);
  const [generatedReport, setGeneratedReport] = useState<any>(null);

  // Fetch all 31 Karnataka districts dynamically
  const { data: districts } = useQuery({
    queryKey: ["districts"],
    queryFn: () => apiService.getDistricts(),
  });

  const reportMutation = useMutation({
    mutationFn: () => apiService.generateReport(reportType, districtCode, format),
    onSuccess: (data) => {
      setGeneratedReport(data);
    },
  });

  const handleGenerate = (e: React.FormEvent) => {
    e.preventDefault();
    reportMutation.mutate();
  };

  const handleDownload = () => {
    if (!generatedReport || !generatedReport.content_text) return;
    
    let fileExt = "pdf";
    let mimeType = "application/pdf";
    
    if (format === "CSV") {
      fileExt = "csv";
      mimeType = "text/csv;charset=utf-8;";
    } else if (format === "EXCEL") {
      fileExt = "csv"; // Excel-compatible CSV format
      mimeType = "text/csv;charset=utf-8;";
    } else {
      fileExt = "txt";
      mimeType = "text/plain;charset=utf-8;";
    }

    const filename = `${generatedReport.report_id}.${fileExt}`;
    const blob = new Blob([generatedReport.content_text], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <RoleGuard allowedRoles={["STATE_ADMIN", "DHO", "SYS_ADMIN"]}>
      <div className="space-y-6">
        
        {/* Header */}
        <div className="bg-dark-card p-6 rounded-2xl border border-dark-cardBorder shadow-md flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2 text-brand-emerald text-xs font-bold uppercase tracking-wider mb-1">
              <FileText className="w-4 h-4" />
              <span>EXECUTIVE GOVERNMENT REPORTING ENGINE</span>
            </div>
            <h1 className="text-2xl font-bold text-white">Official Health Administration Reports</h1>
            <p className="text-xs text-slate-400 mt-1">
              Generate official PDF/Excel reports formatted for District Health Officers, State Directorate, and NHM review.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Report Configuration Form (Left Column) */}
          <div className="bg-dark-card border border-dark-cardBorder rounded-2xl p-6 shadow-md space-y-4">
            <h2 className="text-base font-bold text-white border-b border-dark-cardBorder pb-3">Report Configuration</h2>
            
            <form onSubmit={handleGenerate} className="space-y-4 text-xs">
              <div>
                <label className="font-bold text-slate-300 block mb-1">Select Report Type</label>
                <select
                  value={reportType}
                  onChange={(e) => setReportType(e.target.value)}
                  className="w-full p-2.5 border border-dark-insetBorder rounded-xl bg-dark-inset font-semibold text-white focus:outline-none focus:border-brand-emerald"
                >
                  <option value="DISTRICT_HEALTH_REPORT" className="bg-dark-sidebar">District Health Officer (DHO) Executive Summary</option>
                  <option value="HIGH_RISK_REGISTER" className="bg-dark-sidebar">High-Risk Village Action Register</option>
                  <option value="MMU_MISSION_LOG" className="bg-dark-sidebar">Mobile Medical Unit Fleet Mission Log</option>
                  <option value="DATA_PROVENANCE_MATRIX" className="bg-dark-sidebar">Data Provenance & Availability Audit Report</option>
                </select>
              </div>

              <div>
                <label className="font-bold text-slate-300 block mb-1">Target District (31 Karnataka Districts)</label>
                <select
                  value={districtCode}
                  onChange={(e) => setDistrictCode(Number(e.target.value))}
                  className="w-full p-2.5 border border-dark-insetBorder rounded-xl bg-dark-inset font-semibold text-white focus:outline-none"
                >
                  {districts && districts.length > 0 ? (
                    districts.map((d: any) => (
                      <option key={d.district_code} value={d.district_code} className="bg-dark-sidebar">
                        {d.district_name} (District {d.district_code})
                      </option>
                    ))
                  ) : (
                    <>
                      <option value="524" className="bg-dark-sidebar">Bagalkote (District 524)</option>
                      <option value="528" className="bg-dark-sidebar">Ballari (District 528)</option>
                      <option value="527" className="bg-dark-sidebar">Belagavi (District 527)</option>
                      <option value="526" className="bg-dark-sidebar">Bengaluru Rural (District 526)</option>
                      <option value="535" className="bg-dark-sidebar">Davanagere (District 535)</option>
                    </>
                  )}
                </select>
              </div>

              <div>
                <label className="font-bold text-slate-300 block mb-1">Output Format</label>
                <div className="grid grid-cols-3 gap-2">
                  {["PDF", "EXCEL", "CSV"].map((fmt) => (
                    <button
                      key={fmt}
                      type="button"
                      onClick={() => setFormat(fmt)}
                      className={`py-2 rounded-xl font-bold text-center border transition ${
                        format === fmt
                          ? "bg-brand-emerald text-dark-bg border-brand-emerald"
                          : "bg-dark-inset text-slate-300 border-dark-insetBorder hover:bg-dark-sidebar"
                      }`}
                    >
                      {fmt}
                    </button>
                  ))}
                </div>
              </div>

              <button
                type="submit"
                disabled={reportMutation.isPending}
                className="w-full py-3 bg-brand-emerald hover:bg-emerald-400 text-dark-bg font-extrabold text-xs rounded-xl shadow transition flex items-center justify-center space-x-2"
              >
                <FileSpreadsheet className="w-4 h-4" />
                <span>{reportMutation.isPending ? "Generating Document..." : "Generate Official Report"}</span>
              </button>
            </form>
          </div>

          {/* Report Preview Display (Right 2 Columns) */}
          <div className="lg:col-span-2 bg-dark-card border border-dark-cardBorder rounded-2xl p-6 shadow-md space-y-4">
            <div className="flex items-center justify-between border-b border-dark-cardBorder pb-3">
              <h2 className="text-base font-bold text-white">Document Preview & Verification</h2>
              
              {generatedReport && (
                <div className="flex items-center space-x-2">
                  <button
                    onClick={handleDownload}
                    className="px-4 py-1.5 bg-brand-emerald hover:bg-emerald-400 text-dark-bg font-extrabold text-xs rounded-xl shadow transition flex items-center space-x-1.5 cursor-pointer"
                  >
                    <Download className="w-3.5 h-3.5" />
                    <span>Download {format} File</span>
                  </button>
                </div>
              )}
            </div>

            {generatedReport ? (
              <div className="space-y-4">
                <div className="bg-emerald-950/60 border border-emerald-800 p-3 rounded-xl text-xs text-brand-emerald flex items-center justify-between">
                  <span className="font-mono font-bold">REPORT ID: {generatedReport.report_id}</span>
                  <span className="font-semibold">{generatedReport.summary}</span>
                </div>

                <pre className="bg-dark-inset text-slate-200 font-mono text-xs p-5 rounded-xl border border-dark-insetBorder overflow-x-auto whitespace-pre-wrap leading-relaxed shadow-inner max-h-[500px]">
                  {generatedReport.content_text}
                </pre>
              </div>
            ) : (
              <div className="p-16 text-center text-slate-400 space-y-2">
                <FileText className="w-12 h-12 text-slate-500 mx-auto" />
                <p className="text-xs font-medium">Select report parameters on the left and click "Generate Official Report".</p>
              </div>
            )}
          </div>

        </div>

      </div>
    </RoleGuard>
  );
}
