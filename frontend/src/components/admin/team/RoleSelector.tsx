"use client";

import { User, Shield, DollarSign, ChefHat, Bike, Smartphone } from "lucide-react";
import { cn } from "@/lib/utils";

const ROLES = [
  {
    id: "manager",
    label: "Gerente",
    icon: Shield,
    desc: "Gestão total (Cardápio, Equipe, Relatórios), exceto dados bancários.",
    color: "text-purple-500",
    bg: "bg-purple-500/10 border-purple-500/20"
  },
  {
    id: "cashier",
    label: "Caixa (POS)",
    icon: DollarSign,
    desc: "Abertura/Fechamento de caixa, sangria e vendas no balcão.",
    color: "text-emerald-500",
    bg: "bg-emerald-500/10 border-emerald-500/20"
  },
  {
    id: "waiter",
    label: "Garçom",
    icon: Smartphone,
    desc: "Acesso exclusivo ao App Mobile para lançar pedidos nas mesas.",
    color: "text-blue-500",
    bg: "bg-blue-500/10 border-blue-500/20"
  },
  {
    id: "kitchen",
    label: "Cozinha (KDS)",
    icon: ChefHat,
    desc: "Visualização do monitor de preparo. Não pode alterar preços.",
    color: "text-orange-500",
    bg: "bg-orange-500/10 border-orange-500/20"
  },
  {
    id: "driver",
    label: "Entregador",
    icon: Bike,
    desc: "Acesso ao App de Logística para aceitar e finalizar rotas.",
    color: "text-cyan-500",
    bg: "bg-cyan-500/10 border-cyan-500/20"
  }
] as const;

interface RoleSelectorProps {
  value: string;
  onChange: (role: string) => void;
}

export default function RoleSelector({ value, onChange }: RoleSelectorProps) {
  
  // ⌨️ Keyboard Arrow Navigation (v1.8 Sovereignty)
  const handleKeyDown = (e: React.KeyboardEvent) => {
    const currentIndex = ROLES.findIndex(r => r.id === value);
    let nextIndex = currentIndex;

    if (e.key === "ArrowDown" || e.key === "ArrowRight") {
      nextIndex = (currentIndex + 1) % ROLES.length;
    } else if (e.key === "ArrowUp" || e.key === "ArrowLeft") {
      nextIndex = (currentIndex - 1 + ROLES.length) % ROLES.length;
    } else if (e.key === "Enter" || e.key === " ") {
      // Já tratado pelo clique se necessário, mas garante suporte
      return;
    } else {
      return;
    }

    e.preventDefault();
    onChange(ROLES[nextIndex].id);
    
    // Foca visualmente o elemento selecionado
    const nextEl = document.getElementById(`role-${ROLES[nextIndex].id}`);
    nextEl?.focus();
  };

  return (
    <div 
      className="grid grid-cols-1 gap-3 max-h-[300px] overflow-y-auto pr-2 custom-scrollbar outline-none"
      role="radiogroup"
      aria-label="Função do colaborador"
      onKeyDown={handleKeyDown}
      tabIndex={0}
    >
      {ROLES.map((role) => {
        const isSelected = value === role.id;
        return (
          <div
            key={role.id}
            id={`role-${role.id}`}
            role="radio"
            aria-checked={isSelected}
            aria-describedby={`desc-${role.id}`}
            tabIndex={isSelected ? 0 : -1} // Roving Tabindex
            onClick={() => onChange(role.id)}
            className={cn(
              "flex items-start gap-4 p-4 rounded-xl border-2 text-left transition-all cursor-pointer outline-none",
              isSelected 
                ? "border-orange-500 bg-orange-500/10 shadow-[0_0_15px_rgba(234,88,12,0.1)]" 
                : "border-slate-800 bg-slate-900/50 hover:border-slate-700 focus:border-slate-600"
            )}
          >
            <div className={cn("p-3 rounded-full shrink-0", role.bg, role.color)}>
              <role.icon size={20} />
            </div>
            <div>
              <h4 className={cn("font-bold text-sm", isSelected ? "text-white" : "text-slate-300")}>
                {role.label}
              </h4>
              <p id={`desc-${role.id}`} className="text-xs text-slate-500 mt-1 leading-relaxed">
                {role.desc}
              </p>
            </div>
            {isSelected && (
              <div className="ml-auto self-center">
                <CheckCircle2 size={16} className="text-orange-500 animate-in zoom-in" />
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

import { CheckCircle2 } from "lucide-react";
