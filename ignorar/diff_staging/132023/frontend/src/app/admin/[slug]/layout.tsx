"use client";
import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { 
  Menu, LogOut, LayoutDashboard, Settings, QrCode, 
  BarChart3, User, History, Package, Smartphone, Users, 
  Bike, Building2, Activity, ChevronDown, Megaphone, ShieldCheck, Store, ClipboardList, ShieldAlert, ChefHat
} from "lucide-react";
import { removeToken, isAuthenticated, getUserRole, getToken } from "@/lib/auth";
import OnboardingTour from "@/components/admin/OnboardingTour";
import { WebSocketProvider } from "@/context/WebSocketContext";
import { useTerminology } from "@/hooks/useTerminology";
import { motion, AnimatePresence } from "framer-motion";
import Logo from "@/components/ui/Logo";
import { toast, Toaster } from "sonner"; // Importação do Toaster

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
  const [isImpersonating, setIsImpersonating] = useState(false);
  const terms = useTerminology();

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push("/admin/login");
    } else {
      const userRole = getUserRole();
      setRole(userRole);
      setIsAuth(true);
      
      const token = getToken();
      if (token) {
        try {
          const payload = JSON.parse(atob(token.split('.')[1]));
          setIsImpersonating(!!payload.impersonator);
        } catch (e) {
          setIsImpersonating(false);
        }
      }

      if (userRole === 'cashier' && !pathname.includes('/waiter') && !pathname.includes('/counter')) {
        router.replace(`/admin/${slug}/waiter`);
      } else if (userRole === 'kitchen' && !pathname.includes('/kitchen') && !pathname.includes('/expeditor')) {
        router.replace(`/admin/${slug}/kitchen`);
      } else if (userRole === 'driver' && !pathname.includes('/driver')) {
        router.replace(`/admin/${slug}/driver`);
      }
    }
  }, [router, pathname, slug]);

  const handleLogout = () => {
    removeToken();
    router.push("/admin/login");
  };

  if (!isAuth) return null;

  const managementItems = [
    { name: "Dashboard", href: `/admin/${slug}/dashboard`, icon: BarChart3, id: "nav-dashboard", roles: ['owner', 'manager'] },
    { name: "Balcão (PDV)", href: `/admin/${slug}/counter`, icon: Store, id: "nav-counter", roles: ['owner', 'manager', 'cashier'] },
    { name: "Franquia", href: `/admin/${slug}/franchise`, icon: Building2, id: "nav-franchise", roles: ['owner'] },
    { name: terms.menu, href: `/admin/${slug}/menu`, icon: Menu, id: "nav-menu", roles: ['owner', 'manager'] },
    { name: "Estoque", href: `/admin/${slug}/inventory`, icon: Package, id: "nav-inventory", roles: ['owner', 'manager'] },
    { name: terms.tables, href: `/admin/${slug}/tables`, icon: QrCode, id: "nav-tables", roles: ['owner', 'manager'] },
    { name: "Marketing", href: `/admin/${slug}/marketing`, icon: Megaphone, id: "nav-marketing", roles: ['owner', 'manager'] },
    { name: "Equipe", href: `/admin/${slug}/team`, icon: Users, id: "nav-team", roles: ['owner'] },
    { name: "Histórico", href: `/admin/${slug}/history`, icon: History, id: "nav-history", roles: ['owner', 'manager'] },
    { name: "Auditoria", href: `/admin/${slug}/audit`, icon: ShieldCheck, id: "nav-audit", roles: ['owner'] },
    { name: "Config", href: `/admin/${slug}/settings`, icon: Settings, id: "nav-settings", roles: ['owner'] },
  ];

  const operationItems = [
    { name: "Produção (KDS)", href: `/admin/${slug}/kitchen`, icon: ChefHat, id: "nav-kitchen", roles: ['owner', 'manager', 'kitchen'] },
    { name: "Expedição", href: `/admin/${slug}/expeditor`, icon: ClipboardList, id: "nav-expeditor", roles: ['owner', 'manager', 'kitchen'] },
    { name: "Delivery & Frota", href: `/admin/${slug}/delivery`, icon: Bike, id: "nav-delivery", roles: ['owner', 'manager'] },
    { name: `App ${terms.waiter}`, href: `/admin/${slug}/waiter`, icon: Smartphone, id: "nav-waiter", roles: ['owner', 'manager', 'cashier'] },
  ];

  const filterItems = (items: any[]) => items.filter(item => role && item.roles.includes(role));

  const isOperationalMode = ['/waiter', '/kitchen', '/driver', '/expeditor'].some(path => pathname.includes(path)) && role !== 'owner' && role !== 'manager';

  return (
    <WebSocketProvider slug={slug}>
      {/* 
         ARCHITECTURAL FIX: Toaster movido para o Layout Admin.
         Isso garante que notificações persistam mesmo se a página filha desmontar ou navegar.
      */}
      <Toaster position="top-center" richColors closeButton />
      
      <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 flex flex-col">
        {role === 'owner' && <OnboardingTour />}
        
        {isImpersonating && (
          <div className="bg-red-600 text-white py-1.5 px-4 text-center text-[10px] font-black uppercase tracking-[0.2em] flex items-center justify-center gap-2 z-[60]">
            <ShieldAlert size={14} /> Modo Suporte Ativo - Acesso Auditado
          </div>
        )}

        {!isOperationalMode && (
          <nav className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 px-6 py-4 flex justify-between items-center sticky top-0 z-50 shadow-sm transition-all">
            <Link href={`/admin/${slug}/dashboard`}>
              <Logo size="sm" animated={true} />
            </Link>
            
            <div className="flex items-center gap-4 overflow-x-auto no-scrollbar">
              <div className="flex gap-1">
                {filterItems(managementItems).map((item) => {
                  const isActive = pathname === item.href;
                  return (
                    <Link 
                      key={item.href} 
                      id={item.id}
                      href={item.href} 
                      className={`flex items-center gap-2 px-4 py-2.5 rounded-2xl text-sm font-bold transition-all whitespace-nowrap ${isActive ? "bg-orange-600 text-white shadow-lg shadow-orange-600/20 scale-105" : "text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-900"}`}
                    >
                      <item.icon size={18} />
                      <span className="hidden lg:inline">{item.name}</span>
                    </Link>
                  );
                })}
              </div>

              <div className="relative group">
                <button 
                  type="button"
                  onClick={() => {}} 
                  className={`flex items-center gap-2 px-4 py-2.5 rounded-2xl text-sm font-bold transition-all ${pathname.includes('/kitchen') || pathname.includes('/delivery') || pathname.includes('/waiter') || pathname.includes('/expeditor') ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/20' : 'text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800'}`}
                >
                  <Activity size={18} />
                  <span className="hidden md:inline">Operação</span>
                  <ChevronDown size={14} />
                </button>
                
                <div className="absolute right-0 top-full mt-2 w-64 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl shadow-2xl overflow-hidden hidden group-hover:block hover:block z-50 animate-in fade-in slide-in-from-top-2">
                  {filterItems(operationItems).map((item) => (
                    <Link 
                      key={item.href}
                      href={item.href}
                      className="flex items-center gap-4 px-5 py-4 text-sm font-bold text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700 hover:text-orange-600 transition-colors border-b border-slate-100 dark:border-slate-700 last:border-0"
                    >
                      <div className="bg-slate-100 dark:bg-slate-900 p-2 rounded-xl"><item.icon size={18} /></div>
                      {item.name}
                    </Link>
                  ))}
                </div>
              </div>

              <div className="h-6 w-px bg-slate-200 dark:bg-slate-800 mx-2"></div>
              
              <button 
                type="button"
                onClick={handleLogout} 
                className="text-slate-400 hover:text-red-500 p-2 transition-colors hover:bg-red-50 rounded-xl" 
                title="Sair"
              >
                <LogOut size={22} />
              </button>
            </div>
          </nav>
        )}

        <AnimatePresence mode="wait">
          <motion.main 
            key={pathname}
            initial={{ opacity: 0, y: 20, filter: "blur(10px)" }}
            animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
            exit={{ opacity: 0, y: -20, filter: "blur(10px)" }}
            transition={{ duration: 0.4, ease: "easeOut" }}
            className="flex-1 p-6 max-w-[1600px] mx-auto w-full"
          >
            {children}
          </motion.main>
        </AnimatePresence>
      </div>
    </WebSocketProvider>
  );
}
