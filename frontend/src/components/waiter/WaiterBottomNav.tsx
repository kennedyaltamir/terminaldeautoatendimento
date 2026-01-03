"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Grid, PlusCircle, History, LogOut } from "lucide-react";

export default function WaiterBottomNav({ slug }: { slug: string }) {
  const pathname = usePathname();

  const isActive = (path: string) => pathname === path;

  return (
    <div className="fixed bottom-0 left-0 w-full bg-white border-t border-gray-200 flex justify-around items-center p-2 z-50 safe-area-bottom shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.1)]">
      <Link 
        href={`/admin/${slug}/waiter`}
        className={`flex flex-col items-center gap-1 p-2 rounded-xl transition-colors ${isActive(`/admin/${slug}/waiter`) ? 'text-orange-600 bg-orange-50' : 'text-gray-400'}`}
      >
        <Grid size={24} />
        <span className="text-[10px] font-bold">Mesas</span>
      </Link>

      <Link 
        href={`/admin/${slug}/waiter/orders`}
        className={`flex flex-col items-center gap-1 p-2 rounded-xl transition-colors ${isActive(`/admin/${slug}/waiter/orders`) ? 'text-orange-600 bg-orange-50' : 'text-gray-400'}`}
      >
        <History size={24} />
        <span className="text-[10px] font-bold">Pedidos</span>
      </Link>

      <Link 
        href={`/admin/${slug}/dashboard`}
        className="flex flex-col items-center gap-1 p-2 rounded-xl text-gray-400 hover:text-gray-600"
      >
        <LogOut size={24} />
        <span className="text-[10px] font-bold">Sair</span>
      </Link>
    </div>
  );
}