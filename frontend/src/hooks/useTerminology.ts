"use client";

import { useEffect, useState, useRef } from "react";
import { getCompanySettings } from "@/lib/api";

type Segment = "gastro" | "event" | "hotel" | "corp";

interface Terminology {
  table: string;
  tables: string;
  waiter: string;
  kitchen: string;
  customer: string;
  menu: string;
}

const DICTIONARY: Record<Segment, Terminology> = {
  gastro: { table: "Mesa", tables: "Mesas", waiter: "Garçom", kitchen: "Cozinha", customer: "Cliente", menu: "Cardápio" },
  hotel: { table: "Quarto", tables: "Quartos", waiter: "Serviço de Quarto", kitchen: "Cozinha", customer: "Hóspede", menu: "Room Service" },
  event: { table: "Assento", tables: "Assentos", waiter: "Staff", kitchen: "Bar/Copa", customer: "Espectador", menu: "Cardápio" },
  corp: { table: "Ponto", tables: "Pontos", waiter: "Atendente", kitchen: "Preparo", customer: "Colaborador", menu: "Catálogo" },
};

export function useTerminology() {
  const [segment, setSegment] = useState<Segment>("gastro");
  const hasFetched = useRef(false);

  useEffect(() => {
    // 🛡️ ANTI-LOOP: Impede múltiplas chamadas se o componente re-renderizar
    if (hasFetched.current) return;

    const cached = localStorage.getItem("mesaflow_segment") as Segment;
    if (cached && DICTIONARY[cached]) {
      setSegment(cached);
    }

    const fetchSettings = async () => {
      try {
        hasFetched.current = true;
        const data = await getCompanySettings();
        if (data?.segment && DICTIONARY[data.segment as Segment]) {
          setSegment(data.segment as Segment);
          localStorage.setItem("mesaflow_segment", data.segment);
        }
      } catch (error) {
        // Falha silenciosa para não interromper a UI
        console.warn("[Terminology] Usando fallback padrão.");
      }
    };

    fetchSettings();
  }, []);

  return DICTIONARY[segment];
}
