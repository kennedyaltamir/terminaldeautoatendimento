"use client";

import { useState, useEffect } from "react";
import Joyride, { CallBackProps, STATUS, Step } from "react-joyride";

export default function OnboardingTour() {
  const [run, setRun] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    // Verifica se o usuário já completou o tour
    const hasSeenTour = localStorage.getItem("mesaflow_tour_completed");
    if (!hasSeenTour) {
      // Pequeno delay para garantir que o layout carregou
      const timer = setTimeout(() => setRun(true), 1000);
      return () => clearTimeout(timer);
    }
  }, []);

  const handleJoyrideCallback = (data: CallBackProps) => {
    const { status, type } = data;
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
        <div className="text-left">
          <h3 className="font-bold text-lg mb-2 text-gray-900">Bem-vindo ao MesaFlow! 🚀</h3>
          <p className="text-gray-600">Vamos configurar seu restaurante em 3 passos simples para você começar a vender hoje mesmo.</p>
        </div>
      ),
      placement: "center",
      disableBeacon: true,
    },
    {
      target: "#nav-menu",
      content: (
        <div className="text-gray-700 text-left">
            1º Passo: Cadastre seus produtos e categorias aqui. É o coração do seu sistema.
        </div>
      ),
      placement: "bottom",
    },
    {
      target: "#nav-tables",
      content: (
        <div className="text-gray-700 text-left">
            2º Passo: Crie suas mesas (ou pontos de venda) e gere os QR Codes para imprimir.
        </div>
      ),
      placement: "bottom",
    },
    {
      target: "#nav-kitchen",
      content: (
        <div className="text-gray-700 text-left">
            3º Passo: Abra esta tela em um tablet na cozinha. Os pedidos aparecerão aqui em tempo real!
        </div>
      ),
      placement: "left",
    },
    {
      target: "#nav-dashboard",
      content: (
        <div className="text-gray-700 text-left">
            Pronto! Acompanhe suas vendas e métricas aqui. Boa sorte!
        </div>
      ),
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
      disableScrolling={false}
      scrollToFirstStep={true}
      callback={handleJoyrideCallback}
      styles={{
        options: {
          primaryColor: "#ea580c",
          textColor: "#333",
          backgroundColor: "#fff",
          zIndex: 10000,
        },
        buttonNext: {
            backgroundColor: "#ea580c",
            fontWeight: "bold",
            borderRadius: "8px",
            color: "#fff"
        },
        buttonBack: {
            color: "#666",
            marginRight: "10px"
        },
        buttonSkip: {
            color: "#999",
            fontSize: "14px"
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
