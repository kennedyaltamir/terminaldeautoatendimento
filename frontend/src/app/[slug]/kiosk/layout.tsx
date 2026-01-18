"use client";

import { useState, useEffect, useCallback } from "react";
import { useRouter, usePathname } from "next/navigation";
import { useIdleTimer } from "@/hooks/useIdleTimer";
import InactivityModal from "@/components/kiosk/InactivityModal";
import { useCart } from "@/context/CartContext";
import { KioskProvider } from "@/context/KioskContext"; // Novo Provider
import KioskExitAuthModal from "@/components/kiosk/KioskExitAuthModal"; // Novo Modal
import KioskFullscreenToggle from "@/components/kiosk/KioskFullscreenToggle"; // Novo Toggle

function KioskContent({ children, params }: { children: React.ReactNode, params: { slug: string } }) {
  const router = useRouter();
  const pathname = usePathname();
  const { clearCart } = useCart();
  const [showInactivityWarning, setShowInactivityWarning] = useState(false);

  const IDLE_TIMEOUT = 60000; 
  const isAttractScreen = pathname.endsWith("/kiosk");

  const handleReset = useCallback(() => {
    setShowInactivityWarning(false);
    clearCart();
    if (!isAttractScreen) {
      router.replace(`/${params.slug}/kiosk`);
    }
  }, [clearCart, isAttractScreen, params.slug, router]);

  const handleIdle = () => {
    if (!isAttractScreen) {
      setShowInactivityWarning(true);
    }
  };

  const { resetTimer } = useIdleTimer({
    timeout: IDLE_TIMEOUT,
    onIdle: handleIdle,
    onActive: () => {}
  });

  const handleStay = () => {
    setShowInactivityWarning(false);
    resetTimer();
  };

  useEffect(() => {
    const preventDefault = (e: Event) => e.preventDefault();
    document.addEventListener('contextmenu', preventDefault);
    document.body.style.userSelect = 'none';
    document.body.style.webkitUserSelect = 'none';
    return () => {
      document.removeEventListener('contextmenu', preventDefault);
      document.body.style.userSelect = 'auto';
      document.body.style.webkitUserSelect = 'auto';
    };
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-white overflow-hidden select-none touch-none">
      <div className="h-full w-full">
        {children}
      </div>
      
      {/* Componentes de Segurança e Controle */}
      <InactivityModal 
        isOpen={showInactivityWarning} 
        onStay={handleStay} 
        onTimeout={handleReset} 
      />
      <KioskExitAuthModal />
      <KioskFullscreenToggle />
    </div>
  );
}

// Wrapper para injetar o Contexto
export default function KioskLayoutWrapper(props: any) {
  return (
    <KioskProvider>
      <KioskContent {...props} />
    </KioskProvider>
  );
}

