import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Karnataka Rural Healthcare Intelligence Platform",
  description: "AI-Powered Rural Healthcare Decision Support & MMU Fleet Dispatch",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased bg-slate-950 text-slate-100">
        {children}
      </body>
    </html>
  );
}
