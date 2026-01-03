import { useEffect, useState } from "react";
import { getCompanySettings } from "@/lib/api";

type Segment = "gastro" | "event" | "hotel" | "corp";

interface Terminology {
  table: string;
  waiter: string;
  kitchen: string;
}

const DICTIONARY: Record<Segment, Terminology> = {
  gastro: { table: "Mesa", waiter: "Garçom", kitchen: "Cozinha" },
  event: { table: "Assento", waiter: "Staff", kitchen: "Bar/Copa" },
  hotel: { table: "Quarto", waiter: "Serviço", kitchen: "Cozinha" },
  corp: { table: "Ponto", waiter: "Atendente", kitchen: "Preparo" },
};

export function useTerminology() {
  const [segment, setSegment] = useState<Segment>("gastro");

  useEffect(() => {
    // Tenta pegar do cache local primeiro para evitar flicker
    const cached = localStorage.getItem("mesaflow_segment") as Segment;
    if (cached) setSegment(cached);

    getCompanySettings()
      .then((data) => {
        if (data.segment) {
          setSegment(data.segment as Segment);
          localStorage.setItem("mesaflow_segment", data.segment);
        }
      })
      .catch(() => {}); // Silently fail if not auth
  }, []);

  return DICTIONARY[segment] || DICTIONARY.gastro;
}