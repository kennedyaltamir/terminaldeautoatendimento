/**
 * DOMAIN: FRONTEND / UI
 * OBJECTIVE: Templates contextuais para WhatsApp (Comunicação Tática).
 * DNA_ID: MF-DRIVER-COMM-V2
 */
"use client";
import React from "react";
import { MessageCircle, X, Navigation, Clock, HelpCircle, MapPin, User } from "lucide-react";
import { cn } from "@/lib/utils";
import { motion, AnimatePresence } from "framer-motion";

interface DriverCommunicationModalProps {
  isOpen: boolean;
  onClose: () => void;
  customerName: string;
  customerPhone: string;
  restaurantName: string;
}

export default function DriverCommunicationModal({ 
  isOpen, onClose, customerName, customerPhone, restaurantName 
}: DriverCommunicationModalProps) {
  
  const sendWhatsapp = (message: string) => {
    const cleanPhone = customerPhone.replace(/\D/g, '');
    const text = encodeURIComponent(message);
    window.open(`https://wa.me/${cleanPhone}?text=${text}`, '_blank');
    onClose();
  };

  const templates = [
    {
      icon: Navigation,
      label: "Saindo Agora",
      text: `Olá ${customerName}, aqui é do ${restaurantName}. Estou saindo com seu pedido agora! 🛵`,
      color: "text-blue-400",
      bg: "bg-blue-500/10 border-blue-500/20 text-blue-400"
    },
    {
      icon: Clock,
      label: "Estou Chegando",
      text: `Olá! Estou chegando com seu pedido em 2 minutos. Por favor, aguarde na portaria. ⏳`,
      color: "text-emerald-400",
      bg: "bg-emerald-500/10 border-emerald-500/20 text-emerald-400"
    },
    {
      icon: HelpCircle,
      label: "Não Encontro",
      text: `Oi ${customerName}, estou na rua do endereço mas não encontro o número. Pode me enviar a localização? 📍`,
      color: "text-orange-400",
      bg: "bg-orange-500/10 border-orange-500/20"
    },
    {
      icon: MapPin,
      label: "Cheguei",
      text: `Cheguei! Estou aguardando na entrada. 📦`,
      color: "text-white",
      bg: "bg-slate-800 border-slate-700"
    }
  ];

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-[9999] flex items-end sm:items-center justify-center bg-black/80 backdrop-blur-sm p-0 sm:p-4">
          <motion.div 
            initial={{ y: "100%" }}
            animate={{ y: 0 }}
            exit={{ y: "100%" }}
            transition={{ type: "spring", damping: 25, stiffness: 300 }}
            className="bg-slate-950 w-full sm:max-w-md rounded-t-[2.5rem] sm:rounded-[2.5rem] border-t-2 sm:border-2 border-slate-800 shadow-2xl overflow-hidden"
          >
            <div className="p-6 border-b border-slate-900 flex justify-between items-center">
              <div className="flex items-center gap-3">
                <div className="bg-green-600 p-2 rounded-xl shadow-lg shadow-green-900/20">
                  <MessageCircle className="text-white" size={20} />
                </div>
                <div>
                  <h3 className="font-black text-white text-lg uppercase tracking-tight">Contato Rápido</h3>
                  <div className="flex items-center gap-1.5">
                    <User size={10} className="text-slate-500" />
                    <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">{customerName}</p>
                  </div>
                </div>
              </div>
              <button onClick={onClose} className="p-2 bg-slate-900 rounded-full text-slate-400 hover:text-white transition-colors">
                <X size={20} />
              </button>
            </div>

            <div className="p-6 space-y-3 bg-slate-900/50">
              {templates.map((tpl, idx) => (
                <button
                  key={idx}
                  onClick={() => sendWhatsapp(tpl.text)}
                  className={cn(
                    "w-full flex items-center gap-4 p-4 rounded-2xl border transition-all active:scale-95 text-left group hover:bg-white/5",
                    tpl.bg
                  )}
                >
                  <div className={cn("p-3 rounded-xl bg-black/20", tpl.color)}>
                    <tpl.icon size={20} />
                  </div>
                  <div>
                    <p className="font-black text-white text-sm uppercase tracking-wide">{tpl.label}</p>
                    <p className="text-xs text-slate-400 line-clamp-1 mt-0.5 font-medium">{tpl.text}</p>
                  </div>
                </button>
              ))}
            </div>

            <div className="p-6 bg-slate-950 border-t border-slate-900">
              <button 
                onClick={onClose}
                className="w-full py-4 bg-slate-900 text-slate-500 font-bold text-xs uppercase tracking-widest rounded-xl border border-slate-800 hover:bg-slate-800 hover:text-white transition-colors"
              >
                Cancelar
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
