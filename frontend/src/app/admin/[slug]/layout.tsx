"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { ChefHat, Menu, LogOut, LayoutDashboard, Settings, QrCode, BarChart3, User, History } from "lucide-react";
import { removeToken, isAuthenticated } from "@/lib/auth";

export default function AdminLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: { slug: string }; // Objeto direto, sem Promise
}) {
  const { slug } = params;
  const pathname = usePathname();
  const router = useRouter();
  const [isAuth, setIsAuth] = useState(false);

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push("/admin/login");
    } else {
      setIsAuth(true);
    }
  }, [router]);

  const handleLogout = () => {
    removeToken();
    router.push("/admin/login");
  };

  if (!isAuth) return null;

  const navItems = [
    { name: "Dashboard", href: `/admin/${slug}/dashboard`, icon: BarChart3 },
    { name: "Cozinha", href: `/admin/${slug}/kitchen`, icon: ChefHat },
    { name: "Histórico", href: `/admin/${slug}/history`, icon: History },
    { name: "Cardápio", href: `/admin/${slug}/menu`, icon: Menu },
    { name: "Mesas", href: `/admin/${slug}/tables`, icon: QrCode },
    { name: "Config", href: `/admin/${slug}/settings`, icon: Settings },
    { name: "Perfil", href: `/admin/${slug}/profile`, icon: User },
  ];

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 flex flex-col">
      <nav className="bg-gray-800 border-b border-gray-700 px-6 py-4 flex justify-between items-center sticky top-0 z-50">
        <div className="flex items-center gap-2">
          <div className="bg-orange-600 p-2 rounded-lg">
            <LayoutDashboard size={20} className="text-white" />
          </div>
          <span className="font-bold text-lg tracking-tight hidden md:block">MesaFlow Admin</span>
        </div>
        <div className="flex items-center gap-6">
          <div className="flex gap-1 bg-gray-900/50 p-1 rounded-lg overflow-x-auto max-w-[70vw] md:max-w-none">
            {navItems.map((item) => {
              const isActive = pathname === item.href;
              return (
                <Link key={item.href} href={item.href} className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-all whitespace-nowrap ${isActive ? "bg-gray-700 text-white shadow-sm" : "text-gray-400 hover:text-white hover:bg-gray-800"}`}>
                  <item.icon size={16} />
                  <span className="hidden md:inline">{item.name}</span>
                </Link>
              );
            })}
          </div>
          <button onClick={handleLogout} className="text-red-400 hover:text-red-300 hover:bg-red-900/20 p-2 rounded-full transition-colors" title="Sair">
            <LogOut size={20} />
          </button>
        </div>
      </nav>
      <main className="flex-1 p-6 max-w-7xl mx-auto w-full">
        {children}
      </main>
    </div>
  );
}