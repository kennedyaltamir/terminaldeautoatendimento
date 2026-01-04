import { useEffect, useState } from "react";
import { getCompanySettings } from "@/lib/api";

type Segment = "gastro" | "event" | "hotel" | "corp";

interface Terminology {
  table: string;      // Ex: Mesa, Quarto, Assento
  tables: string;     // Plural
  waiter: string;     // Ex: Garçom, Camareira, Staff
  kitchen: string;    // Ex: Cozinha, Bar, Copa
  customer: string;   // Ex: Cliente, Hóspede
  menu: string;       // Ex: Cardápio, Menu de Serviços
}

const DICTIONARY: Record<Segment, Terminology> = {
  gastro: { 
    table: "Mesa", 
    tables: "Mesas", 
    waiter: "Garçom", 
    kitchen: "Cozinha", 
    customer: "Cliente",
    menu: "Cardápio"
  },
  hotel: { 
    table: "Quarto", 
    tables: "Quartos", 
    waiter: "Serviço de Quarto", 
    kitchen: "Cozinha", 
    customer: "Hóspede",
    menu: "Room Service"
  },
  event: { 
    table: "Assento", 
    tables: "Assentos", 
    waiter: "Staff", 
    kitchen: "Bar/Copa", 
    customer: "Espectador",
    menu: "Cardápio"
  },
  corp: { 
    table: "Ponto", 
    tables: "Pontos", 
    waiter: "Atendente", 
    kitchen: "Preparo", 
    customer: "Colaborador",
    menu: "Catálogo"
  },
};

export function useTerminology() {
  const [segment, setSegment] = useState<Segment>("gastro");

  useEffect(() => {
    // Tenta recuperar do cache local para evitar flicker
    const cached = localStorage.getItem("mesaflow_segment") as Segment;
    if (cached && DICTIONARY[cached]) {
      setSegment(cached);
    }

    // Atualiza com dados reais da API
    getCompanySettings()
      .then((data) => {
        if (data.segment && DICTIONARY[data.segment as Segment]) {
          setSegment(data.segment as Segment);
          localStorage.setItem("mesaflow_segment", data.segment);
        }
      })
      .catch(() => {}); 
  }, []);

  return DICTIONARY[segment];
}