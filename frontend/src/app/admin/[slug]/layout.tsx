"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { 
  ChefHat, Menu, LogOut, LayoutDashboard, Settings, QrCode, 
  BarChart3, User, History, Package, Smartphone, Users, 
  Bike, Building2, Activity, ChevronDown, Megaphone, ShieldCheck
} from "lucide-react";
import { removeToken, isAuthenticated, getUserRole } from "@/lib/auth";
import OnboardingTour from "@/components/admin/OnboardingTour";
import { WebSocketProvider } from "@/context/WebSocketContext";
import { useTerminology } from "@/hooks/useTerminology";

export default function AdminLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: { slug: string };
}) {
  const { slug } = params;
  const pathname = usePathname();
  const router = useRouter();
  const [isAuth, setIsAuth] = useState(false);
  const [role, setRole] = useState<string | null>(null);
  const [isOpsMenuOpen, setIsOpsMenuOpen] = useState(false);
  const terms = useTerminology();

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push("/admin/login");
    } else {
      setIsAuth(true);
      const userRole = getUserRole();
      setRole(userRole);

      // Redirecionamentos baseados em Role
      if (userRole === 'cashier' && !pathname.includes('/waiter')) router.replace(`/admin/${slug}/waiter`);
      if (userRole === 'kitchen' && !pathname.includes('/kitchen')) router.replace(`/admin/${slug}/kitchen`);
      if (userRole === 'driver' && !pathname.includes('/driver')) router.replace(`/admin/${slug}/driver`);
    }
  }, [router, pathname, slug]);

  const handleLogout = () => {
    removeToken();
    router.push("/admin/login");
  };

  if (!isAuth) return null;

  // Itens de Gestão (Estratégico)
  const managementItems = [
    { name: "Dashboard", href: `/admin/${slug}/dashboard`, icon: BarChart3, id: "nav-dashboard", roles: ['owner', 'manager'] },
    { name: "Franquia", href: `/admin/franchise`, icon: Building2, id: "nav-franchise", roles: ['owner'] },
    { name: terms.menu, href: `/admin/${slug}/menu`, icon: Menu, id: "nav-menu", roles: ['owner', 'manager'] },
    { name: "Estoque", href: `/admin/${slug}/inventory`, icon: Package, id: "nav-inventory", roles: ['owner', 'manager'] },
    { name: terms.tables, href: `/admin/${slug}/tables`, icon: QrCode, id: "nav-tables", roles: ['owner', 'manager'] },
    { name: "Marketing", href: `/admin/${slug}/marketing`, icon: Megaphone, id: "nav-marketing", roles: ['owner', 'manager'] },
    { name: "Equipe", href: `/admin/${slug}/team`, icon: Users, id: "nav-team", roles: ['owner'] },
    { name: "Histórico", href: `/admin/${slug}/history`, icon: History, id: "nav-history", roles: ['owner', 'manager'] },
    { name: "Auditoria", href: `/admin/${slug}/audit`, icon: ShieldCheck, id: "nav-audit", roles: ['owner'] }, // NOVO
    { name: "Config", href: `/admin/${slug}/settings`, icon: Settings, id: "nav-settings", roles: ['owner'] },
  ];

  // Itens de Operação (Dia a Dia)
  const operationItems = [
    { name: "Produção (KDS)", href: `/admin/${slug}/kitchen`, icon: ChefHat, id: "nav-kitchen", roles: ['owner', 'manager', 'kitchen'] },
    { name: "Delivery & Frota", href: `/admin/${slug}/delivery`, icon: Bike, id: "nav-delivery", roles: ['owner', 'manager'] },
    { name: `App ${terms.waiter}`, href: `/admin/${slug}/waiter`, icon: Smartphone, id: "nav-waiter", roles: ['owner', 'manager', 'cashier'] },
  ];

  const filterItems = (items: any[]) => items.filter(item => role && item.roles.includes(role));

  const isOperationalMode = ['/waiter', '/kitchen', '/driver'].some(path => pathname.includes(path)) && role !== 'owner' && role !== 'manager';

  return (
    <WebSocketProvider slug={slug}>
      <div className="min-h-screen bg-gray-900 text-gray-100 flex flex-col">
        {role === 'owner' && <OnboardingTour />}

        {!isOperationalMode && (
          <nav className="bg-gray-800 border-b border-gray-700 px-4 md:px-6 py-3 flex justify-between items-center sticky top-0 z-50 shadow-md">
            <div className="flex items-center gap-3">
              <div className="bg-orange-600 p-2 rounded-lg shadow-lg shadow-orange-500/20">
                <LayoutDashboard size={20} className="text-white" />
              </div>
              <span className="font-bold text-lg tracking-tight hidden md:block">MesaFlow</span>
            </div>

            <div className="flex items-center gap-4 overflow-x-auto no-scrollbar">
              {/* Menu de Gestão (Horizontal) */}
              <div className="flex gap-1">
                {filterItems(managementItems).map((item) => {
                  const isActive = pathname === item.href;
                  return (
                    <Link 
                      key={item.href} 
                      id={item.id}
                      href={item.href} 
                      className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all whitespace-nowrap ${isActive ? "bg-gray-700 text-white shadow-sm ring-1 ring-gray-600" : "text-gray-400 hover:text-white hover:bg-gray-700/50"}`}
                    >
                      <item.icon size={16} />
                      <span className="hidden lg:inline">{item.name}</span>
                    </Link>
                  );
                })}
              </div>

              {/* Dropdown de Operação */}
              <div className="relative group">
                <button 
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-bold transition-all ${pathname.includes('/kitchen') || pathname.includes('/delivery') || pathname.includes('/waiter') ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'}`}
                  onClick={() => setIsOpsMenuOpen(!isOpsMenuOpen)}
                >
                  <Activity size={16} />
                  <span className="hidden md:inline">Operação</span>
                  <ChevronDown size={14} />
                </button>

                {/* Dropdown Content */}
                <div className="absolute right-0 top-full mt-2 w-56 bg-gray-800 border border-gray-700 rounded-xl shadow-xl overflow-hidden hidden group-hover:block hover:block z-50">
                  {filterItems(operationItems).map((item) => (
                    <Link 
                      key={item.href}
                      href={item.href}
                      className="flex items-center gap-3 px-4 py-3 text-sm text-gray-300 hover:bg-gray-700 hover:text-white transition-colors border-b border-gray-700/50 last:border-0"
                    >
                      <div className="bg-gray-900 p-2 rounded-lg text-blue-400"><item.icon size={16} /></div>
                      {item.name}
                    </Link>
                  ))}
                </div>
              </div>

              <div className="h-6 w-px bg-gray-700 mx-2"></div>

              <button onClick={handleLogout} className="text-red-400 hover:text-red-300 hover:bg-red-900/20 p-2 rounded-full transition-colors" title="Sair">
                <LogOut size={20} />
              </button>
            </div>
          </nav>
        )}

        <main className={`flex-1 ${!isOperationalMode ? 'p-4 md:p-6 max-w-[1600px] mx-auto w-full' : ''}`}>
          {children}
        </main>
      </div>
    </WebSocketProvider>
  );
}
