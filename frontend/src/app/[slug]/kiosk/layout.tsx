/**
 * DOMAIN: FRONTEND / LAYOUT
 * OBJECTIVE: Layout do Kiosk com injeção de Guard e Contexto.
 */
"use client";
import React, { useState, useCallback, use } from "react";
import { useRouter, usePathname } from "next/navigation";
import { useIdleTimer } from "@/hooks/useIdleTimer";
import InactivityModal from "@/components/kiosk/InactivityModal";
import { useCart } from "@/context/CartContext";
import KioskExitAuthModal from "@/components/kiosk/KioskExitAuthModal";
import KioskGuard from "@/components/kiosk/KioskGuard";
import KioskFullscreenToggle from "@/components/kiosk/KioskFullscreenToggle";

export default function KioskLayout({ 
  children, 
  params: paramsPromise 
}: { 
  children: React.ReactNode, 
  params: Promise<{ slug: string }> 
}) {
  const { slug } = use(paramsPromise);
  const router = useRouter();
  const pathname = usePathname();
  const { clearCart } = useCart();
  const [showInactivityWarning, setShowInactivityWarning] = useState(false);
  const IDLE_TIMEOUT = 60000; // 60s de inatividade

  const isAttractScreen = pathname.endsWith("/kiosk");

  const handleReset = useCallback(() => {
    setShowInactivityWarning(false);
    clearCart();
    if (!isAttractScreen) {
      router.replace(`/${slug}/kiosk`);
    }
  }, [clearCart, isAttractScreen, slug, router]);

  const handleIdle = () => {
    if (!isAttractScreen) setShowInactivityWarning(true);
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

  return (
    <div className="min-h-screen bg-slate-950 text-white overflow-hidden select-none touch-none">
      <KioskGuard />
      <div className="h-full w-full">{children}</div>
      <InactivityModal isOpen={showInactivityWarning} onStay={handleStay} onTimeout={handleReset} />
      <KioskExitAuthModal />
      <KioskFullscreenToggle />
    </div>
  );
}
