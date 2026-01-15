// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 19:35:00
"use client";
import { useState, useEffect } from "react";
import Joyride, { CallBackProps, STATUS, Step } from "react-joyride";

/**
 * OnboardingTour: Componente de guia interativo.
 * Desabilitado automaticamente em ambientes de teste E2E para evitar bloqueio de cliques.
 */
export default function OnboardingTour() {
  const [run, setRun] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    
    // 🛡️ RESILIÊNCIA QA: Se estivermos em modo teste ou o tour já foi concluído, não inicia.
    const isE2E = typeof window !== 'undefined' && 
                 (window.location.search.includes('e2e=true') || 
                  localStorage.getItem('mesaflow_tour_completed') === 'true');

    if (isE2E) {
      setRun(false);
      return;
    }

    const hasSeenTour = localStorage.getItem("mesaflow_tour_completed");
    if (!hasSeenTour) {
      const timer = setTimeout(() => setRun(true), 1500);
      return () => clearTimeout(timer);
    }
  }, []);

  const handleJoyrideCallback = (data: CallBackProps) => {
    const { status } = data;
    const finishedStatuses: string[] = [STATUS.FINISHED, STATUS.SKIPPED];
    if (finishedStatuses.includes(status)) {
      setRun(false);
      localStorage.setItem("mesaflow_tour_completed", "true");
    }
  };

  if (!mounted) return null;

  const steps: Step[] = [
    {
      target: "body",
      content: (
        <div className="text-left" data-testid="joyride-welcome">
          <h3 className="font-bold text-lg mb-2 text-gray-900">Bem-vindo ao MesaFlow! 🚀</h3>
          <p className="text-gray-600">Vamos configurar seu restaurante em 3 passos simples para você começar a vender hoje mesmo.</p>
        </div>
      ),
      placement: "center",
      disableBeacon: true,
    },
    {
      target: "#nav-menu",
      content: <div className="text-gray-700 text-left">1º Passo: Cadastre seus produtos e categorias aqui.</div>,
      placement: "bottom",
    },
    {
      target: "#nav-tables",
      content: <div className="text-gray-700 text-left">2º Passo: Crie suas mesas e gere os QR Codes.</div>,
      placement: "bottom",
    },
    {
      target: "#nav-kitchen",
      content: <div className="text-gray-700 text-left">3º Passo: Abra o KDS em um tablet na cozinha.</div>,
      placement: "left",
    },
    {
      target: "#nav-dashboard",
      content: <div className="text-gray-700 text-left">Pronto! Acompanhe suas vendas e métricas aqui.</div>,
      placement: "bottom",
    },
  ];

  return (
    <Joyride
      steps={steps}
      run={run}
      continuous
      showSkipButton
      showProgress
      scrollToFirstStep={true}
      callback={handleJoyrideCallback}
      styles={{
        options: {
          primaryColor: "#ea580c",
          textColor: "#333",
          backgroundColor: "#fff",
          zIndex: 10000,
        },
        overlay: {
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
        },
        buttonNext: {
            backgroundColor: "#ea580c",
            fontWeight: "bold",
            borderRadius: "8px",
            color: "#fff"
        }
      }}
      locale={{
        back: "Voltar",
        close: "Fechar",
        last: "Vamos lá!",
        next: "Próximo",
        skip: "Pular tour",
      }}
    />
  );
}
