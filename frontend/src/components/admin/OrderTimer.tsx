"use client";

import { useState, useEffect } from "react";
import { Clock, AlertTriangle } from "lucide-react";

interface OrderTimerProps {
  createdAt: string;
}

export default function OrderTimer({ createdAt }: OrderTimerProps) {
  const [elapsedMinutes, setElapsedMinutes] = useState(0);
  const [displayTime, setDisplayTime] = useState("00:00");

  useEffect(() => {
    const startTime = new Date(createdAt).getTime();

    const updateTimer = () => {
      const now = new Date().getTime();
      const diff = now - startTime;
      
      const minutes = Math.floor(diff / 60000);
      const seconds = Math.floor((diff % 60000) / 1000);
      
      setElapsedMinutes(minutes);
      setDisplayTime(`${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`);
    };

    // Atualiza imediatamente e depois a cada segundo
    updateTimer();
    const interval = setInterval(updateTimer, 1000);

    return () => clearInterval(interval);
  }, [createdAt]);

  // Definição de Cores baseada no SLA
  let styleClass = "bg-green-100 text-green-700 border-green-200";
  let icon = <Clock size={14} />;

  if (elapsedMinutes >= 20) {
    styleClass = "bg-red-100 text-red-700 border-red-200 animate-pulse font-bold";
    icon = <AlertTriangle size={14} />;
  } else if (elapsedMinutes >= 10) {
    styleClass = "bg-yellow-100 text-yellow-800 border-yellow-200 font-medium";
  }

  return (
    <div className={`flex items-center gap-1.5 px-2 py-1 rounded-md border text-xs transition-colors duration-500 ${styleClass}`}>
      {icon}
      <span>{displayTime}</span>
    </div>
  );
}