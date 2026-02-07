/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 14.0.0 (Isolation Master)
 * DNA_ID: admin-layout-v14-isolation
 * Objective: Implement high-fidelity contextual isolation. Prevents administrative Sidebar 
 * from mounting in operational driver contexts.
 */
"use client";

import React, { useState, useEffect, use } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import {
  LayoutDashboard, Bike, ChefHat, Smartphone, History,
  Menu as MenuIcon, Package, QrCode, Users, Settings, 
  Menu, X, LogOut, ShieldCheck, DollarSign, Monitor, User,
  Truck, Layout
} from "lucide-react";
import { cn } from "@/lib/utils";
import Logo from "@/components/ui/Logo";
import { removeTokens } from "@/lib/auth";

interface AdminLayoutProps {
  children: React.ReactNode;
  params: Promise<{ slug: string }>; 
}

export default function AdminLayout({ children, params: paramsPromise }: AdminLayoutProps) {
  const params = use(paramsPromise);
  const slug = params.slug;
  const pathname = usePathname();
  const router = useRouter();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  useEffect(() => {
    if (slug === "undefined" || !slug) {
      router.replace("/admin/login");
    }
  }, [slug, router]);

  const handleLogout = () => {
    removeTokens();
    router.push("/admin/login");
  };

  // 🛡️ CRITICAL ISOLATION LOGIC: Check if current route is an Operational Cockpit
  const isOperationalRoute = pathname?.includes('/driver');

  if (isOperationalRoute) {
    // 🧱 O rito administrativo é abortado. Retorna apenas o container principal sem Sidebar.
    // O componente Sidebar e seus sub-itens NUNCA são montados neste branch.
    return (
      <main className="min-h-screen w-full bg-black relative overflow-hidden">
        {children}
      </main>
    );
  }

  const navigation = [
    {
      group: "Operação",
      items: [
        { name: "Dashboard", href: `/admin/${slug}/dashboard`, icon: LayoutDashboard },
        { name: "Cozinha (KDS)", href: `/admin/${slug}/kitchen`, icon: ChefHat },
        { name: "Expedidor", href: `/admin/${slug}/expeditor`, icon: Truck },
        { name: "Balcão (POS)", href: `/admin/${slug}/counter`, icon: Monitor },
        { name: "App Garçom", href: `/admin/${slug}/waiter`, icon: Smartphone },
        { name: "Delivery", href: `/admin/${slug}/delivery`, icon: Bike },
        { name: "Mesas", href: `/admin/${slug}/tables`, icon: QrCode },
      ]
    },
    {
      group: "Gestão",
      items: [
        { name: "Cardápio", href: `/admin/${slug}/menu`, icon: MenuIcon },
        { name: "Estoque", href: `/admin/${slug}/inventory`, icon: Package },
        { name: "Histórico", href: `/admin/${slug}/history`, icon: History },
        { name: "Marketing", href: `/admin/${slug}/marketing`, icon: Megaphone },
      ]
    },
    {
      group: "Sistema",
      items: [
        { name: "Equipe", href: `/admin/${slug}/team`, icon: Users },
        { name: "Auditoria", href: `/admin/${slug}/audit`, icon: ShieldCheck },
        { name: "Financeiro", href: `/admin/${slug}/audit/financial`, icon: DollarSign },
        { name: "Configurações", href: `/admin/${slug}/settings`, icon: Settings },
        { name: "Assinatura", href: `/admin/${slug}/settings/billing`, icon: Zap },
      ]
    }
  ];

  const isActive = (href: string) => pathname === href || pathname.startsWith(href + "/");

  return (
    <div className="min-h-screen bg-black text-white flex flex-col md:flex-row">
      <div className="md:hidden flex items-center justify-between p-4 bg-slate-900 border-b border-slate-800 sticky top-0 z-50">
        <Logo size="sm" />
        <button onClick={() => setIsSidebarOpen(!isSidebarOpen)} className="p-2 text-slate-300">
          {isSidebarOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      <aside className={cn(
        "fixed inset-y-0 left-0 z-40 w-72 bg-slate-950 border-r border-slate-800 transform transition-transform duration-300 ease-in-out md:translate-x-0 md:static md:h-screen flex flex-col",
        isSidebarOpen ? "translate-x-0" : "-translate-x-full"
      )}>
        <div className="p-8 hidden md:block">
          <Logo size="md" animated={true} />
        </div>
        <nav className="flex-1 px-4 overflow-y-auto custom-scrollbar space-y-8 pb-10">
          {navigation.map((group) => (
            <div key={group.group} className="space-y-2">
              <h3 className="px-4 text-[10px] font-black text-slate-600 uppercase tracking-[0.2em]">
                {group.group}
              </h3>
              <div className="space-y-1">
                {group.items.map((item) => (
                  <Link
                    key={item.name}
                    href={item.href}
                    onClick={() => setIsSidebarOpen(false)}
                    className={cn(
                      "flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-bold transition-all group",
                      isActive(item.href) 
                        ? "bg-orange-600 text-white shadow-lg shadow-orange-900/40" 
                        : "text-slate-500 hover:text-white hover:bg-slate-900 border border-transparent hover:border-slate-800"
                    )}
                  >
                    <item.icon size={18} className={cn(
                      "transition-colors",
                      isActive(item.href) ? "text-white" : "text-slate-600 group-hover:text-orange-500"
                    )} />
                    <span>{item.name}</span>
                  </Link>
                ))}
              </div>
            </div>
          ))}
        </nav>

        <div className="p-4 border-t border-slate-900 bg-black/20">
          <Link 
            href={`/admin/${slug}/profile`}
            className="flex items-center gap-3 p-4 mb-4 bg-slate-900/50 rounded-2xl border border-slate-800 hover:border-slate-700 transition-all group"
          >
            <div className="w-8 h-8 rounded-full bg-orange-600 flex items-center justify-center font-black text-xs text-white">
              <User size={16} />
            </div>
            <div className="min-w-0">
              <p className="text-xs font-black text-white truncate uppercase">Meu Perfil</p>
              <p className="text-[9px] text-slate-500 font-bold uppercase tracking-tighter">{slug}</p>
            </div>
          </Link>
          <button 
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold text-red-500 hover:bg-red-900/10 transition-colors"
          >
            <LogOut size={18} />
            <span>Sair do Sistema</span>
          </button>
        </div>
      </aside>

      {isSidebarOpen && (
        <div className="fixed inset-0 bg-black/60 z-30 md:hidden backdrop-blur-sm" onClick={() => setIsSidebarOpen(false)} />
      )}

      <main className="flex-1 h-screen overflow-y-auto bg-black relative">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,_var(--tw-gradient-stops))] from-orange-900/5 via-transparent to-transparent pointer-events-none" />
        <div className="p-4 md:p-8 relative z-10">
          {children}
        </div>
      </main>
    </div>
  );
}

import { Megaphone, Zap } from "lucide-react";
