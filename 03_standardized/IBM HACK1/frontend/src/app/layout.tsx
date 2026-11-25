"use client";

import React, { useState } from "react";
import "./globals.css";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AuthProvider, useAuth } from "@/lib/AuthContext";
import { AppHeader } from "@/components/shell/AppHeader";
import { Sidebar } from "@/components/shell/Sidebar";
import { usePathname } from "next/navigation";

const AppShell = ({ children }: { children: React.ReactNode }) => {
  const pathname = usePathname();
  const isLoginPage = pathname === "/" || pathname === "/login";

  if (isLoginPage) {
    return <main className="min-h-screen bg-dark-bg text-white">{children}</main>;
  }

  return (
    <div className="min-h-screen flex flex-col bg-dark-bg text-slate-100 selection:bg-brand-emerald selection:text-dark-bg">
      <AppHeader />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <main className="flex-1 p-6 overflow-y-auto w-full bg-dark-bg text-slate-100">{children}</main>
      </div>
    </div>
  );
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient({
    defaultOptions: {
      queries: {
        refetchOnWindowFocus: false,
        staleTime: 1000 * 60 * 5, // 5 minutes cache
      },
    },
  }));

  return (
    <html lang="en">
      <head>
        <title>RuralPulse — Karnataka Healthcare Intelligence & Decision Support Platform</title>
        <meta name="description" content="AI-assisted decision-support platform for Karnataka health administrators" />
      </head>
      <body>
        <QueryClientProvider client={queryClient}>
          <AuthProvider>
            <AppShell>{children}</AppShell>
          </AuthProvider>
        </QueryClientProvider>
      </body>
    </html>
  );
}
