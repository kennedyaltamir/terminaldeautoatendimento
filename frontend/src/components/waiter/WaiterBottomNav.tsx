"use client";

import Link from "next/link";
import { usePathname, useParams } from "next/navigation";
import { Grid, History, LogOut, BellRing } from "lucide-react";
import { cn } from "@/lib/utils";
import { useWebSocket } from "@/hooks/useWebSocket";
import { useState } from "react";

export default function WaiterBottomNav({ slug: propSlug }: { slug?: string }) {
  const pathname = usePathname();
  const params = useParams();
  
  // 🛡️ FIX: Prioriza o slug vindo do hook useParams (que já lida com a Promise internamente)
  const slug = propSlug || (params?.slug as string);
  
  const [hasNotification, setHasNotification] = useState(false);

  useWebSocket(slug, (data) => {
    if (data.type === "order_update" && data.status === "ready") {
      setHasNotification(true);
    }
  });

  const isActive = (path: string) => pathname === path || pathname.startsWith(path + "/");

  const navItems = [
    { label: "Mesas", href: `/admin/${slug}/waiter`, icon: Grid },
    { label: "Pedidos", href: `/admin/${slug}/waiter/orders`, icon: History, badge: hasNotification },
    { label: "Sair", href: `/admin/${slug}/dashboard`, icon: LogOut }
  ];

  if (!slug || slug === "undefined") return null;

  return (
    <nav className="fixed bottom-0 left-0 w-full bg-white border-t border-gray-200 pb-safe pt-2 px-6 z-40 shadow-2xl">
      <div className="flex justify-around items-center max-w-md mx-auto">
        {navItems.map((item) => {
          const active = isActive(item.href);
          return (
            <Link 
              key={item.href}
              href={item.href}
              onClick={() => item.badge && setHasNotification(false)}
              className={cn(
                "flex flex-col items-center gap-1 p-2 rounded-2xl transition-all duration-300 min-w-[4.5rem] relative",
                active ? "text-orange-600 bg-orange-50" : "text-gray-400 hover:text-gray-600"
              )}
            >
              <div className="relative">
                <item.icon size={24} strokeWidth={active ? 2.5 : 2} />
                {item.badge && (
                  <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full border-2 border-white animate-pulse" />
                )}
              </div>
              <span className="text-[10px] font-bold uppercase tracking-tighter">{item.label}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}