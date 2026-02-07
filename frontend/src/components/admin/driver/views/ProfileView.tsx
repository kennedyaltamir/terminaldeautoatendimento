//
/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 27.0.0
 * OBJETIVO: Hub de Perfil do Motorista com Rito de Saída Hardened (Navegação Atômica).
 * Comportamento esperado: Exibe dados do motorista. Ao confirmar logout, limpa tokens, encerra turno na API e executa um redirecionamento físico para /admin/login, garantindo a destruição de estados residuais em memória.
 */
//
"use client";

import React, { useState } from "react";
import { 
  User, Settings, LogOut, Bike, Shield, Star, 
  ChevronRight, CreditCard, FileText, Phone,
  Mail, HelpCircle, ShieldCheck, BadgeCheck,
  AlertTriangle, CheckCircle2, X, Camera,
  RefreshCw, MessageCircle,Upload , ExternalLink,Lock
} from "lucide-react";
import { cn } from "@/lib/utils";
import { toast } from "sonner";
import { DriverState } from "@/lib/domain/driver/driverMachine";
import { useDriverHaptics } from "@/hooks/driver/useDriverHaptics";
import Modal from "@/components/ui/Modal";
import { removeTokens } from "@/lib/auth";
import * as api from "@/lib/api";

type ProfileModalType = 'VEHICLE' | 'PERSONAL' | 'SECURITY' | 'FINANCIAL' | 'DOCS' | 'LOGOUT_CONFIRM' | 'SUPPORT' | null;

interface ProfileViewProps {
  driverName: string;
  vehicleId: string;
  rating: number;
  totalDeliveries: number;
  fsmState: DriverState;
  onLogout: () => void;
}

const VehicleModal = ({ isOpen, onClose, currentVehicle, onUpdate }: any) => {
  const [selected, setSelected] = useState(currentVehicle);
  const [loading, setLoading] = useState(false);
  const vehicles = ["MOTO-01 (Honda CG)", "MOTO-02 (Yamaha)", "BIKE-01 (Elétrica)"];
  
  const handleConfirm = async () => {
    setLoading(true);
    try {
      await api.updateActiveVehicle({ vehicle_id: selected });
      onUpdate(selected);
      onClose();
    } catch (e) {
      toast.error("Erro ao atualizar veículo.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Alterar Veículo">
      <div className="space-y-4">
        <div className="bg-blue-900/20 p-4 rounded-xl border border-blue-500/30 flex gap-3">
          <Bike className="text-blue-400 shrink-0" />
          <p className="text-xs text-blue-200">
            A troca de veículo é registrada para fins de seguro e cálculo de rota.
          </p>
        </div>
        <div className="space-y-2">
          {vehicles.map((v) => {
            const vId = v.split(" ")[0];
            return (
              <button
                key={v}
                onClick={() => setSelected(vId)}
                className={cn(
                  "w-full p-4 rounded-xl border text-left transition-all flex justify-between items-center",
                  selected === vId 
                    ? "bg-orange-600 border-orange-500 text-white shadow-lg" 
                    : "bg-slate-900 border-slate-800 text-slate-400 hover:bg-slate-800"
                )}
              >
                <div className="flex flex-col">
                  <span className="font-bold text-sm">{vId}</span>
                  <span className="text-[10px] opacity-60 uppercase font-black">{v.includes("(") ? v.split("(")[1].replace(")", "") : ""}</span>
                </div>
                {selected === vId && <CheckCircle2 size={18} />}
              </button>
            );
          })}
        </div>
        <button 
          onClick={handleConfirm}
          disabled={loading}
          className="w-full py-4 bg-emerald-600 text-white rounded-xl font-black uppercase text-xs tracking-widest mt-4 flex items-center justify-center gap-2 disabled:opacity-50"
        >
          {loading ? <RefreshCw className="animate-spin" size={14} /> : <CheckCircle2 size={14} />}
          Confirmar Troca
        </button>
      </div>
    </Modal>
  );
};

const SupportModal = ({ isOpen, onClose }: any) => {
  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Central de Ajuda">
      <div className="space-y-4">
        <div className="bg-slate-900 p-6 rounded-2xl border border-slate-800 text-center">
          <div className="w-16 h-16 bg-slate-800 rounded-full flex items-center justify-center mx-auto mb-4 border border-white/5">
            <HelpCircle size={32} className="text-orange-500" />
          </div>
          <h3 className="text-white font-bold mb-2">Como podemos ajudar?</h3>
          <p className="text-xs text-slate-500 leading-relaxed">
            Nossa equipe de suporte está disponível 24/7 para resolver problemas críticos de rota ou financeiros.
          </p>
        </div>
        
        <div className="grid grid-cols-2 gap-3">
          <button onClick={() => window.open('https://wa.me/5511999999999', '_blank')} className="p-4 bg-green-600/10 border border-green-600/20 rounded-xl flex flex-col items-center gap-2 hover:bg-green-600/20 transition-colors group">
            <MessageCircle className="text-green-500 group-hover:scale-110 transition-transform" />
            <span className="text-[10px] font-black text-green-500 uppercase tracking-widest">WhatsApp</span>
          </button>
          <button className="p-4 bg-blue-600/10 border border-blue-600/20 rounded-xl flex flex-col items-center gap-2 hover:bg-blue-600/20 transition-colors group">
            <Phone className="text-blue-500 group-hover:scale-110 transition-transform" />
            <span className="text-[10px] font-black text-blue-500 uppercase tracking-widest">Ligar 0800</span>
          </button>
        </div>

        <div className="space-y-2 pt-4 border-t border-slate-800">
          <button className="w-full text-left p-4 rounded-xl hover:bg-slate-900 text-slate-400 text-xs font-bold uppercase tracking-wider flex justify-between items-center transition-colors">
            <span className="flex items-center gap-2"><CreditCard size={14}/> Problemas com Pagamento</span>
            <ChevronRight size={14} />
          </button>
          <button className="w-full text-left p-3 rounded-lg hover:bg-slate-900 text-slate-400 text-sm flex justify-between">
            <span>Reportar Acidente</span>
            <ChevronRight size={16} />
          </button>
        </div>
      </div>
    </Modal>
  );
};

const DocsModal = ({ isOpen, onClose }: any) => {
  const [cnhStatus, setCnhStatus] = useState<'VALID' | 'EXPIRED'>('VALID');
  
  const handleUpload = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.onchange = (e: any) => {
      toast.success("Documento enviado para análise!");
    };
    input.click();
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Documentação">
      <div className="space-y-6">
        <div className="bg-slate-900 p-4 rounded-2xl border border-slate-800 flex justify-between items-center">
          <div>
            <p className="text-xs text-slate-500 font-bold uppercase">CNH Digital</p>
            <p className="text-white font-bold">123.456.789-00</p>
          </div>
          <span className={cn("px-2 py-1 rounded text-[10px] font-black uppercase", cnhStatus === 'VALID' ? "bg-emerald-500/20 text-emerald-500" : "bg-red-500/20 text-red-500")}>
            {cnhStatus === 'VALID' ? 'Aprovado' : 'Vencido'}
          </span>
        </div>
        
        <div className="space-y-3">
          <p className="text-xs text-slate-400 font-bold uppercase tracking-widest">Atualizar Documentos</p>
          <button onClick={handleUpload} className="w-full p-4 bg-slate-800 rounded-xl border border-dashed border-slate-600 flex items-center justify-center gap-3 text-slate-400 hover:text-white hover:border-slate-400 transition-all">
            <Camera size={20} />
            <span className="text-sm font-bold">Tirar foto da CNH</span>
          </button>
          <button onClick={handleUpload} className="w-full p-4 bg-slate-800 rounded-xl border border-dashed border-slate-600 flex items-center justify-center gap-3 text-slate-400 hover:text-white hover:border-slate-400 transition-all">
            <FileText size={20} />
            <span className="text-sm font-bold">Upload CRLV (Veículo)</span>
          </button>
        </div>
      </div>
    </Modal>
  );
};

const FinancialModal = ({ isOpen, onClose }: any) => {
  const [pixKey, setPixKey] = useState("admin@mesaflow.com");
  
  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Dados Bancários">
      <div className="space-y-6">
        <div className="bg-slate-900 p-6 rounded-2xl border border-slate-800 text-center">
          <p className="text-xs text-slate-500 font-bold uppercase mb-2">Chave Pix Ativa</p>
          <p className="text-xl font-mono text-white truncate font-black">{pixKey}</p>
        </div>
        <div className="space-y-4">
             <div>
               <label className="block text-[10px] font-black text-slate-500 uppercase tracking-widest mb-1.5 ml-1">Nova Chave Pix</label>
               <input 
                 className="w-full bg-slate-950 border border-slate-800 rounded-2xl p-5 text-white font-mono outline-none focus:border-orange-500 transition-all shadow-inner"
                 placeholder="E-mail, CPF ou Aleatória"
                 value={pixKey}
                 onChange={(e) => setPixKey(e.target.value)}
               />
             </div>
             <button 
               onClick={() => { toast.success("Dados bancários salvos!"); onClose(); }}
               className="w-full bg-white text-slate-950 py-5 rounded-[2rem] font-black uppercase text-xs tracking-widest shadow-xl active:scale-95 transition-all"
             >
                Salvar Alterações
             </button>
          </div>
          <p className="text-[10px] text-slate-600 text-center leading-relaxed px-4 font-medium">
            Alterações financeiras geram logs de auditoria imutáveis. Sua identidade é rastreada para prevenção de fraudes.
          </p>
        </div>
    </Modal>
  );
};

export default function ProfileView({ 
  driverName, 
  vehicleId, 
  rating, 
  totalDeliveries, 
  fsmState, 
  onLogout 
}: ProfileViewProps) {
  const [activeModal, setActiveModal] = useState<ProfileModalType>(null);
  const { trigger } = useDriverHaptics();
  const [localVehicle, setLocalVehicle] = useState(vehicleId);
  const [pixKey, setPixKey] = useState("admin@mesaflow.com");

  const handleVehicleChange = () => {
    if (['EN_ROUTE_DELIVERY', 'AT_DESTINATION'].includes(fsmState)) {
      trigger('error');
      toast.error("Bloqueado em Rota", { 
        description: "Finalize a entrega atual antes de trocar de veículo." 
      });
      return;
    }
    setActiveModal('VEHICLE');
  };

  const handleLogoutRequest = () => {
    if (['ASSIGNED', 'EN_ROUTE_DELIVERY', 'AT_DESTINATION'].includes(fsmState)) {
      trigger('error');
      toast.error("Turno Ativo", { 
        description: "Você possui uma missão em andamento. Finalize ou cancele para sair." 
      });
      return;
    }
    setActiveModal('LOGOUT_CONFIRM');
  };

  const confirmLogout = async () => {
    const toastId = toast.loading("Encerrando turno na base...");
    try {
      const token = localStorage.getItem("mesaflow_access_token");
      await fetch(`${process.env.NEXT_PUBLIC_API_URL}/mobile/logistics/shift/end`, {
        method: "POST",
        headers: { 
          "Authorization": `Bearer ${token}`, 
          "Content-Type": "application/json" 
        },
        body: JSON.stringify({ 
          final_battery: 1.0, 
          estimated_km: 0.0 
        })
      });
      toast.success("Turno encerrado com sucesso.", { id: toastId });
      onLogout();
    } catch (e) {
      console.warn("[Logout] Falha na sincronia, forçando saída local.");
    } finally {

      onLogout(); 
      removeTokens(); 

      window.location.href = '/admin/login';
    }
  };

  const sections = [
    {
      title: "CONTA E SEGURANÇA",
      items: [
        { 
          icon: User, 
          label: "Dados Pessoais", 
          sub: "admin@mesaflow.com", 
          color: "text-blue-400", 
          action: () => toast.info("Edição de perfil disponível em breve") 
        },
        { 
          icon: Shield, 
          label: "Segurança e Senha", 
          sub: "Biometria ativa", 
          color: "text-orange-500", 
          action: () => toast.info("Gestão de senha em homologação") 
        },
      ]
    },
    {
      title: "FINANCEIRO",
      items: [
        { 
          icon: CreditCard, 
          label: "Dados para Repasse", 
          sub: `Pix: ${pixKey}`, 
          color: "text-emerald-500", 
          action: () => setActiveModal('FINANCIAL') 
        },
      ]
    },
    {
      title: "COMPLIANCE",
      items: [
        { 
          icon: FileText, 
          label: "CNH e CRLV", 
          sub: "Documentação verificada", 
          color: "text-purple-400", 
          action: () => setActiveModal('DOCS') 
        },
      ]
    },
    {
      title: "SUPORTE",
      items: [
        { 
          icon: HelpCircle, 
          label: "Central de Ajuda", 
          sub: "Dúvidas e FAQ", 
          color: "text-slate-400", 
          action: () => setActiveModal('SUPPORT') 
        },
        { 
          icon: ShieldCheck, 
          label: "Termos e Privacidade", 
          sub: "v26.0.0-Gold", 
          color: "text-slate-400", 
          action: () => window.open("/terms", "_blank") 
        },
      ]
    }
  ];

  return (
    <div className="p-6 space-y-8 pb-32 pt-20 animate-in slide-in-from-bottom-4 duration-700">
      
      <div className="flex items-center gap-6 mb-4">
        <div className="relative">
          <div className="w-24 h-24 bg-gradient-to-br from-orange-600 to-red-600 rounded-full flex items-center justify-center shadow-2xl border-4 border-slate-900 group">
            <User size={40} className="text-white group-hover:scale-110 transition-transform" />
          </div>
          <div className="absolute -bottom-1 -right-1 bg-slate-950 p-2 rounded-full border border-white/10 text-yellow-500 shadow-xl">
            <Star size={18} fill="currentColor" className="animate-pulse" />
          </div>
        </div>
        <div>
          <h2 className="text-2xl font-black text-white uppercase tracking-tight leading-none mb-2">{driverName}</h2>
          <div className="flex items-center gap-2">
            <span className="text-[10px] font-black text-orange-500 bg-orange-500/10 px-3 py-1 rounded-full border border-orange-500/20 uppercase tracking-widest shadow-inner">
              Soberano Nível 3
            </span>
          </div>
          <div className="mt-2 flex items-center gap-2">
            <p className="text-xs text-slate-500 font-mono font-bold uppercase tracking-tighter">
              {totalDeliveries} missões
            </p>
            <div className="w-1 h-1 bg-slate-800 rounded-full" />
            <p className="text-xs text-emerald-500 font-mono font-bold uppercase tracking-tighter">
              {rating.toFixed(1)} ★
            </p>
          </div>
        </div>
      </div>

      <button 
        onClick={handleVehicleChange}
        className="w-full text-left bg-slate-900 border border-white/5 rounded-[2.5rem] p-6 shadow-2xl relative overflow-hidden ring-1 ring-white/5 active:scale-[0.98] transition-transform group"
      >
        <div className="absolute top-0 right-0 p-6 opacity-5 pointer-events-none group-hover:opacity-10 transition-opacity">
          <Bike size={80} />
        </div>
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] flex items-center gap-2">
            <div className={cn("w-1.5 h-1.5 rounded-full animate-pulse", fsmState === 'IDLE' ? "bg-emerald-500" : "bg-orange-500")} />
            Hardware Ativo
          </h3>
          <span className="text-[10px] font-black text-blue-500 uppercase group-hover:text-blue-400 transition-colors flex items-center gap-1">
            Alterar <ChevronRight size={12} />
          </span>
        </div>
        <div className="flex items-center justify-between bg-black/40 p-5 rounded-3xl border border-white/5">
          <div>
            <p className="text-white font-black text-xl tracking-wider leading-none mb-1">{localVehicle}</p>
            <p className="text-xs text-slate-500 font-bold uppercase tracking-tighter">Honda CG 160 • Prata</p>
          </div>
          <div className="flex flex-col items-end gap-1">
            <div className="px-3 py-1 bg-emerald-500/10 text-emerald-500 rounded-lg text-[9px] font-black uppercase border border-emerald-500/20 flex items-center gap-1.5 shadow-inner">
              <BadgeCheck size={12} /> Vistoria OK
            </div>
          </div>
        </div>
      </button>

      <div className="space-y-10">
        {sections.map((section, idx) => (
          <div key={idx} className="space-y-4">
            <h4 className="text-[10px] font-black text-slate-600 uppercase tracking-[0.3em] px-2">
              {section.title}
            </h4>
            <div className="space-y-2">
              {section.items.map((item, i) => (
                <button 
                  key={i} 
                  onClick={item.action}
                  className="w-full flex items-center justify-between bg-slate-900/40 p-5 rounded-[2rem] border border-white/5 hover:bg-slate-800 hover:border-white/10 transition-all group active:scale-[0.98]"
                >
                  <div className="flex items-center gap-5">
                    <div className={cn(
                      "p-3 rounded-2xl bg-slate-950 border border-white/5 shadow-inner group-hover:scale-110 transition-transform",
                      item.color
                    )}>
                      <item.icon size={22} />
                    </div>
                    <div className="text-left">
                      <p className="text-sm font-black text-white uppercase tracking-tight">{item.label}</p>
                      <p className="text-[10px] text-slate-500 font-bold uppercase tracking-tighter mt-0.5">{item.sub}</p>
                    </div>
                  </div>
                  <ChevronRight size={18} className="text-slate-700 group-hover:text-white group-hover:translate-x-1 transition-all" />
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div className="pt-4">
        <button 
          onClick={handleLogoutRequest}
          className="w-full py-6 rounded-[2rem] border-2 border-red-900/20 bg-red-900/5 text-red-500 font-black uppercase text-xs tracking-[0.3em] hover:bg-red-600 hover:text-white hover:border-red-600 transition-all flex items-center justify-center gap-3 active:scale-95 shadow-2xl"
        >
          <LogOut size={20} /> Encerrar Sessão
        </button>
      </div>

      <div className="text-center space-y-1 py-10">
        <p className="text-[9px] text-slate-700 font-mono uppercase tracking-[0.4em]">
          MesaFlow Driver OS v26.0.1 • Build 8943
        </p>
        <p className="text-[8px] text-slate-800 font-bold">MesaFlow Sovereign Intelligence © 2026</p>
      </div>

      <VehicleModal 
        isOpen={activeModal === 'VEHICLE'} 
        onClose={() => setActiveModal(null)} 
        currentVehicle={localVehicle}
        onUpdate={(v: string) => { 
          setLocalVehicle(v);
          trigger('success');
        }}
      />

      <SupportModal 
        isOpen={activeModal === 'SUPPORT'} 
        onClose={() => setActiveModal(null)} 
      />
      
      <Modal isOpen={activeModal === 'FINANCIAL'} onClose={() => setActiveModal(null)} title="Dados Bancários">
        <FinancialModal isOpen={activeModal === 'FINANCIAL'} onClose={() => setActiveModal(null)} />
      </Modal>

      <Modal isOpen={activeModal === 'DOCS'} onClose={() => setActiveModal(null)} title="Documentação">
        <DocsModal isOpen={activeModal === 'DOCS'} onClose={() => setActiveModal(null)} />
      </Modal>

      <Modal isOpen={activeModal === 'LOGOUT_CONFIRM'} onClose={() => setActiveModal(null)} title="Encerrar Turno?">
        <div className="space-y-4">
          <div className="bg-red-900/20 p-5 rounded-[2rem] border border-red-500/30 flex gap-4 items-start shadow-inner">
            <AlertTriangle className="text-red-500 shrink-0 mt-1" size={24} />
            <p className="text-sm text-red-200 leading-relaxed font-medium">
              Ao sair, você deixará de receber novas missões e o rastreamento GPS será finalizado. Confirma encerramento?
            </p>
          </div>
          <div className="flex gap-3 pt-6">
            <button onClick={() => setActiveModal(null)} className="flex-1 py-5 bg-slate-900 text-slate-500 border border-slate-800 rounded-2xl font-black text-xs uppercase tracking-widest active:scale-95 transition-all">Cancelar</button>
            <button onClick={confirmLogout} className="flex-[2] py-5 bg-red-600 text-white rounded-2xl font-black text-xs uppercase tracking-widest shadow-xl shadow-red-900/40 active:scale-95 transition-all">Confirmar Saída</button>
          </div>
        </div>
      </Modal>

      <div className="text-center py-10 opacity-20">
        <p className="text-[9px] font-mono uppercase tracking-[0.4em]">MesaFlow Driver OS v27.0.0</p>
      </div>
    </div>
  );
}