"use client";

import { useState, useEffect } from "react";
import { useRouter, usePathname } from "next/navigation";
import { useIdleTimer } from "@/hooks/useIdleTimer";
import InactivityModal from "@/components/kiosk/InactivityModal";

export default function KioskLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: { slug: string };
}) {
  const router = useRouter();
  const pathname = usePathname();
  const [showInactivityWarning, setShowInactivityWarning] = useState(false);

  // Configuração do Timer
  // 60 segundos de inatividade -> Mostra aviso
  // +10 segundos no aviso -> Reseta para Home
  const IDLE_TIMEOUT = 60000; 

  const handleIdle = () => {
    // Não mostra aviso se já estiver na tela inicial (Attract Screen)
    if (!pathname.endsWith("/kiosk")) {
      setShowInactivityWarning(true);
    }
  };

  const handleTimeout = () => {
    setShowInactivityWarning(false);
    // Redireciona para a tela de atração (Reset)
    router.push(`/${params.slug}/kiosk`);
  };

  const { resetTimer } = useIdleTimer({
    timeout: IDLE_TIMEOUT,
    onIdle: handleIdle,
    onActive: () => {} // O modal lida com o "Stay"
  });

  const handleStay = () => {
    setShowInactivityWarning(false);
    resetTimer();
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white overflow-hidden select-none">
      {/* Kiosk Wrapper - Impede seleção de texto e menu de contexto */}
      <div onContextMenu={(e) => e.preventDefault()} className="h-full">
        {children}
      </div>

      <InactivityModal 
        isOpen={showInactivityWarning} 
        onStay={handleStay} 
        onTimeout={handleTimeout} 
      />
    </div>
  );
}
