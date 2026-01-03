"use client";

import { useState, useEffect } from "react";
import Joyride, { CallBackProps, STATUS, Step } from "react-joyride";
import { useTheme } from "next-themes";

export default function OnboardingTour() {
  const [run, setRun] = useState(false);
  const { theme } = useTheme();

  useEffect(() => {
    // Verifica se o usuário já completou o tour
    const hasSeenTour = localStorage.getItem("mesaflow_tour_completed");
    if (!hasSeenTour) {
      setRun(true);
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
        <div className="text-gray-700">
            1º Passo: Cadastre seus produtos e categorias aqui. É o coração do seu sistema.
        </div>
      ),
      placement: "right",
    },
    {
      target: "#nav-tables",
      content: (
        <div className="text-gray-700">
            2º Passo: Crie suas mesas (ou quartos/assentos) e gere os QR Codes para imprimir.
        </div>
      ),
      placement: "right",
    },
    {
      target: "#nav-kitchen",
      content: (
        <div className="text-gray-700">
            3º Passo: Abra esta tela em um tablet na cozinha. Os pedidos aparecerão aqui em tempo real!
        </div>
      ),
      placement: "right",
    },
    {
      target: "#nav-dashboard",
      content: (
        <div className="text-gray-700">
            Pronto! Acompanhe suas vendas e métricas aqui. Boa sorte!
        </div>
      ),
      placement: "right",
    },
  ];

  return (
    <Joyride
      steps={steps}
      run={run}
      continuous
      showSkipButton
      showProgress
      callback={handleJoyrideCallback}
      styles={{
        options: {
          primaryColor: "#ea580c",
          textColor: "#333",
          backgroundColor: "#fff",
          zIndex: 1000,
        },
        buttonNext: {
            backgroundColor: "#ea580c",
            fontWeight: "bold",
            color: "#fff"
        },
        buttonBack: {
            color: "#666"
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