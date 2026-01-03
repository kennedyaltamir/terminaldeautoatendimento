"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { ChefHat, Menu, LogOut, LayoutDashboard, Settings, QrCode, BarChart3, User, History, Package, Smartphone, Users, Bike } from "lucide-react";
import { removeToken, isAuthenticated, getUserRole } from "@/lib/auth";
import OnboardingTour from "@/components/admin/OnboardingTour";
import { WebSocketProvider } from "@/context/WebSocketContext";

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

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push("/admin/login");
    } else {
      setIsAuth(true);
      const userRole = getUserRole();
      setRole(userRole);

      // Redirecionamentos de Segurança por Cargo
      if (userRole === 'cashier') {
        const allowedPaths = ['/waiter', '/waiter/orders', '/waiter/pos'];
        const isAllowed = allowedPaths.some(path => pathname.includes(path));
        if (!isAllowed) router.replace(`/admin/${slug}/waiter`);
      }
      if (userRole === 'kitchen' && !pathname.includes('/kitchen')) {
          router.replace(`/admin/${slug}/kitchen`);
      }
      if (userRole === 'driver' && !pathname.includes('/driver')) {
          router.replace(`/admin/${slug}/driver`);
      }
    }
  }, [router, pathname, slug]);

  const handleLogout = () => {
    removeToken();
    router.push("/admin/login");
  };

  if (!isAuth) return null;

  const allNavItems = [
    { name: "Dashboard", href: `/admin/${slug}/dashboard`, icon: BarChart3, id: "nav-dashboard", roles: ['owner', 'manager'] },
    { name: "Delivery", href: `/admin/${slug}/delivery`, icon: Bike, id: "nav-delivery", roles: ['owner', 'manager'] }, // NOVO
    { name: "Cozinha", href: `/admin/${slug}/kitchen`, icon: ChefHat, id: "nav-kitchen", roles: ['owner', 'manager', 'kitchen'] },
    { name: "App Garçom", href: `/admin/${slug}/waiter`, icon: Smartphone, id: "nav-waiter", roles: ['owner', 'manager', 'cashier'] },
    { name: "Histórico", href: `/admin/${slug}/history`, icon: History, id: "nav-history", roles: ['owner', 'manager'] },
    { name: "Cardápio", href: `/admin/${slug}/menu`, icon: Menu, id: "nav-menu", roles: ['owner', 'manager'] },
    { name: "Estoque", href: `/admin/${slug}/inventory`, icon: Package, id: "nav-inventory", roles: ['owner', 'manager'] },
    { name: "Mesas", href: `/admin/${slug}/tables`, icon: QrCode, id: "nav-tables", roles: ['owner', 'manager'] },
    { name: "Equipe", href: `/admin/${slug}/team`, icon: Users, id: "nav-team", roles: ['owner'] },
    { name: "Config", href: `/admin/${slug}/settings`, icon: Settings, id: "nav-settings", roles: ['owner'] },
    { name: "Perfil", href: `/admin/${slug}/profile`, icon: User, id: "nav-profile", roles: ['owner', 'manager', 'cashier', 'kitchen', 'driver'] },
  ];

  const navItems = allNavItems.filter(item => role && item.roles.includes(role));

  // Modos Fullscreen (sem sidebar)
  const isWaiterMode = pathname.includes("/waiter");
  const isKitchenMode = pathname.includes("/kitchen") && role === 'kitchen';
  const isDriverMode = pathname.includes("/driver");

  return (
    <WebSocketProvider slug={slug}>
      <div className="min-h-screen bg-gray-900 text-gray-100 flex flex-col">
        {role === 'owner' && <OnboardingTour />}
        
        {!isWaiterMode && !isKitchenMode && !isDriverMode && (
          <nav className="bg-gray-800 border-b border-gray-700 px-6 py-4 flex justify-between items-center sticky top-0 z-50">
            <div className="flex items-center gap-2">
              <div className="bg-orange-600 p-2 rounded-lg">
                <LayoutDashboard size={20} className="text-white" />
              </div>
              <span className="font-bold text-lg tracking-tight hidden md:block">MesaFlow Admin</span>
            </div>
            <div className="flex items-center gap-6">
              <div className="flex gap-1 bg-gray-900/50 p-1 rounded-lg overflow-x-auto max-w-[70vw] md:max-w-none no-scrollbar">
                {navItems.map((item) => {
                  const isActive = pathname === item.href;
                  return (
                    <Link 
                      key={item.href} 
                      id={item.id}
                      href={item.href} 
                      className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-all whitespace-nowrap ${isActive ? "bg-gray-700 text-white shadow-sm" : "text-gray-400 hover:text-white hover:bg-gray-800"}`}
                    >
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
        )}
        
        <main className={`flex-1 ${!isWaiterMode && !isKitchenMode && !isDriverMode ? 'p-6 max-w-7xl mx-auto w-full' : ''}`}>
          {children}
        </main>
      </div>
    </WebSocketProvider>
  );
}