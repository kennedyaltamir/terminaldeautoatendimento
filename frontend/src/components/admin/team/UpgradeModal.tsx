"use client";

import Modal from "@/components/ui/Modal";
import { Zap, Check, ArrowRight } from "lucide-react";
import Link from "next/link";

interface UpgradeModalProps {
  isOpen: boolean;
  onClose: () => void;
  slug: string;
}

export default function UpgradeModal({ isOpen, onClose, slug }: UpgradeModalProps) {
  if (!isOpen) return null;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Limite da Equipe Atingido">
      <div className="text-center space-y-6 py-4">
        <div className="w-20 h-20 bg-gradient-to-br from-orange-500 to-red-600 rounded-full flex items-center justify-center mx-auto shadow-xl shadow-orange-900/20 animate-pulse">
          <Zap size={40} className="text-white fill-white" />
        </div>
        
        <div>
          <h3 className="text-2xl font-black text-white mb-2">Sua operação cresceu! 🚀</h3>
          <p className="text-slate-400 text-sm leading-relaxed max-w-xs mx-auto">
            O plano <b>Start</b> permite até 2 colaboradores. Para adicionar mais membros e desbloquear funções avançadas, migre para o <b>Pro</b>.
          </p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 text-left space-y-3">
          <div className="flex items-center gap-3 text-sm text-slate-300">
            <Check size={16} className="text-green-500" /> <span>Usuários Ilimitados</span>
          </div>
          <div className="flex items-center gap-3 text-sm text-slate-300">
            <Check size={16} className="text-green-500" /> <span>Relatórios de Produtividade</span>
          </div>
          <div className="flex items-center gap-3 text-sm text-slate-300">
            <Check size={16} className="text-green-500" /> <span>Auditoria de Ações</span>
          </div>
        </div>

        <div className="flex flex-col gap-3">
          <Link 
            href={`/admin/${slug}/settings/billing`}
            className="w-full bg-white text-slate-900 py-4 rounded-xl font-black uppercase text-xs tracking-widest hover:bg-slate-200 transition-all flex items-center justify-center gap-2 shadow-lg active:scale-95"
          >
            Fazer Upgrade Agora <ArrowRight size={16} />
          </Link>
          <button 
            onClick={onClose}
            className="text-slate-500 font-bold text-xs hover:text-white transition-colors"
          >
            Agora não, manter equipe pequena
          </button>
        </div>
      </div>
    </Modal>
  );
}
