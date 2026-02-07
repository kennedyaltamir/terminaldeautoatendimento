"use client";

/**
 * 🙋 ServiceModal.tsx
 * Interface unificada para solicitações de serviço.
 * 
 * Funcionalidades:
 * - Adaptação por Segmento (Gastro, Hotel, Evento) via `getSegmentLabels`.
 * - Feedback de carregamento (Loading state).
 * - Personalização de cor (White Label).
 */

import { useState, useEffect } from "react";
import { 
  HandPlatter, 
  Receipt, 
  Sparkles, 
  MessageSquare, 
  Phone, 
  LogOut, 
  Shield, 
  HelpCircle, 
  Utensils, 
  User, 
  Loader2 
} from "lucide-react";
import Modal from "@/components/ui/Modal";
import { getSegmentLabels } from "@/lib/segment-utils";

// Mapa de ícones para renderização dinâmica baseada no segmento
const ICON_MAP: Record<string, any> = {
  HandPlatter, 
  Receipt, 
  Sparkles, 
  MessageSquare, 
  Phone, 
  LogOut, 
  Shield, 
  HelpCircle, 
  Utensils, 
  User
};

interface ServiceModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: (type: string, notes: string) => Promise<void> | void;
  primaryColor: string;
  segment?: string;
}

export default function ServiceModal({ 
  isOpen, 
  onClose, 
  onConfirm, 
  primaryColor,
  segment = "gastro"
}: ServiceModalProps) {
  const [selectedType, setSelectedType] = useState<string | null>(null);
  const [notes, setNotes] = useState("");
  const [loading, setLoading] = useState(false);

  // Obtém as labels e opções corretas para o tipo de negócio (Ex: Hotel vs Restaurante)
  const labels = getSegmentLabels(segment);

  // Reseta o estado sempre que o modal abre
  useEffect(() => {
    if (isOpen) {
      setSelectedType(null);
      setNotes("");
      setLoading(false);
    }
  }, [isOpen]);

  const handleConfirm = async () => {
    if (!selectedType) return;
    
    setLoading(true);
    try {
      await onConfirm(selectedType, notes);
      onClose();
    } catch (error) {
      console.error("Erro ao solicitar serviço:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Solicitar Ajuda">
      <div className="space-y-6">
        {/* Grid de Opções */}
        <div className="grid grid-cols-2 gap-3">
          {labels.service_options.map((opt) => {
            const Icon = ICON_MAP[opt.icon] || MessageSquare;
            const isSelected = selectedType === opt.id;

            return (
              <button
                key={opt.id}
                onClick={() => setSelectedType(opt.id)}
                disabled={loading}
                className={`
                  flex flex-col items-center justify-center p-4 rounded-xl border transition-all duration-200 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed
                  ${isSelected 
                    ? 'bg-white shadow-md border-transparent ring-2' 
                    : 'bg-gray-50 border-gray-100 text-gray-500 hover:bg-white hover:border-gray-200'}
                `}
                style={{
                  borderColor: isSelected ? primaryColor : undefined,
                  color: isSelected ? primaryColor : undefined,
                  // O ring color precisa ser inline se usarmos cores dinâmicas arbitrárias, 
                  // ou podemos confiar na classe do Tailwind se primaryColor for fixa.
                  // Aqui usamos estilo inline para garantir suporte a white-label.
                  boxShadow: isSelected ? `0 0 0 1px ${primaryColor}` : undefined
                }}
              >
                <Icon size={28} className="mb-2" />
                <span className={`text-xs font-bold uppercase tracking-tight ${isSelected ? '' : 'text-gray-600'}`}>
                  {opt.label}
                </span>
              </button>
            );
          })}
        </div>

        {/* Campo de Observação */}
        <div className="space-y-2">
          <label className="text-xs font-bold text-gray-500 uppercase tracking-wide ml-1">
            Observação (Opcional)
          </label>
          <textarea
            className="w-full bg-gray-50 border border-gray-200 rounded-xl p-3 text-sm outline-none focus:ring-2 focus:bg-white transition-all resize-none text-gray-800"
            placeholder="Ex: Trazer máquina de cartão, gelo e limão..."
            rows={3}
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            disabled={loading}
            style={{
              // @ts-ignore - CSS variable injection para cor de foco
              "--tw-ring-color": primaryColor 
            }}
          />
        </div>

        {/* Botão de Ação */}
        <button
          disabled={!selectedType || loading}
          onClick={handleConfirm}
          className="w-full py-4 rounded-xl font-bold text-white shadow-lg flex items-center justify-center gap-2 transition-all active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed"
          style={{ backgroundColor: primaryColor }}
        >
          {loading ? (
            <Loader2 className="animate-spin" size={20} />
          ) : (
            "Enviar Solicitação"
          )}
        </button>
        
        <p className="text-[10px] text-center text-gray-400 font-medium">
          A equipe receberá um alerta imediato no painel.
        </p>
      </div>
    </Modal>
  );
}