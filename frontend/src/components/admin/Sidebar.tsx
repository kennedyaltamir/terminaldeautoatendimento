/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 1.0.1 (Path Verified)
 * DNA_ID: MF-COMP-SIDEBAR-V1
 * Objective: Administrative sidebar for the (dashboard) route group.
 */
"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  LayoutDashboard, ChefHat, Package, 
  Users, Settings, LogOut, QrCode, Bike
} from "lucide-react";
import { cn } from "@/lib/utils";
import Logo from "@/components/ui/Logo";

export default function Sidebar() {
  const pathname = usePathname();
  
  // Extrai o slug da URL de forma segura
  const pathParts = pathname.split('/');
  const slug = pathParts[2] || "hamburgueria-ze";

  const menuItems = [
    { name: "Dashboard", href: `/admin/${slug}/dashboard`, icon: LayoutDashboard },
    { name: "Cozinha (KDS)", href: `/admin/${slug}/kitchen`, icon: ChefHat },
    { name: "Logística", href: `/admin/${slug}/delivery`, icon: Bike },
    { name: "Mesas", href: `/admin/${slug}/tables`, icon: QrCode },
    { name: "Estoque", href: `/admin/${slug}/inventory`, icon: Package },
    { name: "Equipe", href: `/admin/${slug}/team`, icon: Users },
    { name: "Configurações", href: `/admin/${slug}/settings`, icon: Settings },
  ];

  return (
    <aside className="w-64 bg-slate-900 border-r border-white/5 flex flex-col h-screen sticky top-0 z-50">
      <div className="p-8">
        <Logo size="md" animated={true} />
      </div>

      <nav className="flex-1 px-4 space-y-1 overflow-y-auto custom-scrollbar">
        {menuItems.map((item) => {
          const isActive = pathname === item.href || pathname.startsWith(item.href + "/");
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold transition-all group",
                isActive 
                  ? "bg-orange-600 text-white shadow-lg shadow-orange-900/40" 
                  : "text-slate-400 hover:text-white hover:bg-white/5"
              )}
            >
              <item.icon size={18} className={cn(
                "transition-colors",
                isActive ? "text-white" : "text-slate-500 group-hover:text-orange-500"
              )} />
              <span>{item.name}</span>
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-white/5 bg-slate-900/50">
        <button className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold text-red-400 hover:bg-red-400/10 transition-colors group">
          <LogOut size={18} className="group-hover:scale-110 transition-transform" />
          <span>Sair do Sistema</span>
        </button>
      </div>
    </aside>
  );
}