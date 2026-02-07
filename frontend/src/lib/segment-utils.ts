export type Segment = "gastro" | "event" | "hotel" | "corp";

interface SegmentLabels {
  table: string; // Como chamar a "Mesa"
  waiter: string; // Como chamar o "Garçom"
  bill: string; // "Conta" ou "Checkout"
  kitchen: string; // "Cozinha" ou "Bar"
  service_options: { id: string; label: string; icon: string }[];
}

export const SEGMENT_CONFIG: Record<Segment, SegmentLabels> = {
  gastro: {
    table: "Mesa",
    waiter: "Garçom",
    bill: "Conta",
    kitchen: "Cozinha",
    service_options: [
      { id: 'help', label: 'Chamar Garçom', icon: 'HandPlatter' },
      { id: 'bill', label: 'Pedir a Conta', icon: 'Receipt' },
      { id: 'cleaning', label: 'Limpeza', icon: 'Sparkles' },
      { id: 'other', label: 'Outros', icon: 'MessageSquare' },
    ]
  },
  hotel: {
    table: "Quarto",
    waiter: "Serviço de Quarto",
    bill: "Extrato",
    kitchen: "Cozinha",
    service_options: [
      { id: 'help', label: 'Camareira', icon: 'Sparkles' },
      { id: 'bill', label: 'Solicitar Checkout', icon: 'LogOut' },
      { id: 'other', label: 'Recepção', icon: 'Phone' },
      { id: 'cleaning', label: 'Recolher Bandeja', icon: 'Utensils' },
    ]
  },
  event: {
    table: "Assento",
    waiter: "Staff",
    bill: "Pagamento",
    kitchen: "Bar",
    service_options: [
      { id: 'help', label: 'Chamar Staff', icon: 'User' },
      { id: 'cleaning', label: 'Limpeza', icon: 'Sparkles' },
      { id: 'other', label: 'Segurança', icon: 'Shield' },
    ]
  },
  corp: {
    table: "Ponto",
    waiter: "Atendente",
    bill: "Fechar",
    kitchen: "Preparo",
    service_options: [
      { id: 'help', label: 'Ajuda', icon: 'HelpCircle' },
      { id: 'cleaning', label: 'Limpeza', icon: 'Sparkles' },
    ]
  }
};

export function getSegmentLabels(segment?: string): SegmentLabels {
  // Fallback para gastro se não houver segmento definido
  const key = (segment as Segment) || "gastro";
  return SEGMENT_CONFIG[key] || SEGMENT_CONFIG.gastro;
}