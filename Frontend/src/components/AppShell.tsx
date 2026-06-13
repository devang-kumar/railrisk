import { Link, useRouterState } from "@tanstack/react-router";
import {
  Activity,
  AlertTriangle,
  FileText,
  LayoutDashboard,
  Radio,
  Train,
  Sparkles,
} from "lucide-react";
import type { ReactNode } from "react";
import { useState } from "react";
import { DataChatDrawer } from "./DataChatDrawer";
import logo from "@/assets/RRAI-logo.png";

const nav = [
  { to: "/dashboard", label: "Overview", icon: LayoutDashboard },
  { to: "/wagons", label: "Delayed Wagons", icon: Train },
  { to: "/report", label: "RailRisk Report", icon: FileText },
];

export function AppShell({ children }: { children: ReactNode }) {
  const { location } = useRouterState();
  const [isChatOpen, setIsChatOpen] = useState(false);
  return (
    <div className="min-h-screen flex text-white relative">
      <DataChatDrawer isOpen={isChatOpen} onClose={() => setIsChatOpen(false)} />
      {/* Sidebar */}
      <aside className="hidden lg:flex flex-col w-64 shrink-0 border-r border-white/5 px-5 py-6 sticky top-0 h-screen">
        <Link to="/" className="flex items-center gap-3 mb-10">
          <img src={logo} alt="RailRisk AI Logo" className="h-10 object-contain drop-shadow-[0_0_15px_rgba(255,107,0,0.3)]" />
          <div className="leading-tight">
            <div className="text-[10px] uppercase tracking-[0.18em] text-white/40">
              Decision Intelligence
            </div>
          </div>
        </Link>

        <nav className="flex flex-col gap-1">
          {nav.map((item) => {
            const active =
              item.to === "/"
                ? location.pathname === "/"
                : location.pathname.startsWith(item.to);
            const Icon = item.icon;
            return (
              <Link
                key={item.to}
                to={item.to}
                className={`group flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm transition-all duration-300 ${
                  active
                    ? "glass-ember text-white ember-glow-sm"
                    : "text-white/60 hover:text-white hover:bg-white/[0.07] hover:shadow-[inset_0_0_0_1px_rgba(255,255,255,0.06)]"
                }`}
              >
                <Icon className="size-4" />
                <span className="font-medium">{item.label}</span>
              </Link>
            );
          })}
        </nav>

        <div className="mt-auto glass rounded-2xl p-4">
          <div className="flex items-center gap-2 text-[11px] uppercase tracking-wider text-white/50 mb-2">
            <span className="size-2 rounded-full bg-[#ff1e1e] animate-pulse-ember" />
            Live Risk Stream
          </div>
          <p className="text-xs text-white/60 leading-relaxed">
            Agents continuously score delays, cargo criticality, and downstream impact.
          </p>
        </div>
      </aside>

      {/* Main */}
      <main className="flex-1 min-w-0">
        {/* Topbar */}
        <header className="sticky top-0 z-30 flex items-center justify-between gap-4 px-6 lg:px-10 py-4 backdrop-blur-xl bg-black/30 border-b border-white/5">
          <Link to="/" className="flex items-center lg:hidden">
            <img src={logo} alt="RailRisk AI Logo" className="h-8 object-contain drop-shadow-[0_0_10px_rgba(255,107,0,0.3)]" />
          </Link>
          <div className="hidden md:flex items-center gap-2 text-xs text-white/50">
            <Activity className="size-3.5 text-[#ff6b00]" />
            <span>System status</span>
            <span className="text-emerald-400 font-medium">Operational</span>
            <span className="mx-2 text-white/20">|</span>
            <span>4 Agents online</span>
          </div>
          <div className="flex items-center gap-3">
            <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full glass text-xs">
              <AlertTriangle className="size-3.5 text-[#ff1e1e]" />
              <span className="text-white/70">3 Critical</span>
            </div>
            <button 
              onClick={() => setIsChatOpen(true)}
              className="px-4 py-2 rounded-full text-sm font-semibold text-white bg-gradient-to-r from-[#ff6b00]/20 to-[#ff1e1e]/20 border border-[#ff1e1e]/30 hover:bg-[#ff1e1e]/30 transition-all flex items-center gap-2"
            >
              <Sparkles className="size-3.5 text-[#ff6b00]" />
              Chat with Data
            </button>
            <button className="btn-ember text-sm hover:btn-ember-hover active:btn-ember-active">
              Acknowledge
            </button>
          </div>
        </header>

        <div className="px-6 lg:px-10 py-8">{children}</div>
      </main>
    </div>
  );
}

export function RiskBadge({ level }: { level: "Low" | "Medium" | "High" | "Critical" }) {
  const map = {
    Low: "border-emerald-400/50 text-emerald-300 bg-emerald-500/10 shadow-[0_0_8px_rgba(52,211,153,0.2)]",
    Medium: "border-yellow-400/50 text-yellow-300 bg-yellow-400/10 shadow-[0_0_8px_rgba(250,204,21,0.2)]",
    High: "border-[#ff6b00]/60 text-[#ff9d3d] bg-[#ff6b00]/15 shadow-[0_0_10px_rgba(255,107,0,0.25)]",
    Critical:
      "border-[#ff1e1e]/70 text-white bg-gradient-to-r from-[#ff1e1e]/30 to-[#ff6b00]/20 shadow-[0_0_12px_rgba(255,30,30,0.4),0_0_30px_rgba(255,30,30,0.15)]",
  } as const;

  const dotColors = {
    Low: "bg-emerald-400",
    Medium: "bg-yellow-400 shadow-[0_0_6px_rgba(250,204,21,0.6)]",
    High: "bg-[#ff6b00] shadow-[0_0_6px_rgba(255,107,0,0.7)]",
    Critical: "bg-[#ff1e1e] animate-pulse-ember",
  } as const;

  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full border text-[11px] font-semibold uppercase tracking-wider transition-all duration-300 ${map[level]}`}
    >
      <span className={`size-1.5 rounded-full ${dotColors[level]}`} />
      {level}
    </span>
  );
}
