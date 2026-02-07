"use client";

import React, { useState } from "react";
import { X, CheckCircle2, MapPin, Phone, User, CreditCard, QrCode, Banknote, Loader2 } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { kioskCheckoutSchema, KioskCheckoutFormData } from "@/lib/validations/kiosk";
import { cn } from "@/lib/utils";

interface KioskCheckoutModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: (data: KioskCheckoutFormData) => void;
  primaryColor: string;
}

export default function KioskCheckoutModal({ isOpen, onClose, onConfirm, primaryColor }: KioskCheckoutModalProps) {
  const {
    register,
    handleSubmit,
    setValue,
    watch,
    formState: { errors, isSubmitting }
  } = useForm<KioskCheckoutFormData>({
    resolver: zodResolver(kioskCheckoutSchema),
    defaultValues: {
      paymentMethod: "pix"
    }
  });

  const paymentMethod = watch("paymentMethod");

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center bg-slate-950/90 backdrop-blur-md p-4">
      <AnimatePresence>
        <motion.div
          initial={{ scale: 0.9, opacity: 0, y: 20 }}
          animate={{ scale: 1, opacity: 1, y: 0 }}
          exit={{ scale: 0.9, opacity: 0, y: 20 }}
          className="bg-white w-full max-w-2xl rounded-[2.5rem] overflow-hidden shadow-2xl flex flex-col max-h-[90vh]"
        >
          {/* Header */}
          <div className="bg-slate-100 p-6 border-b border-slate-200 flex justify-between items-center">
            <div>
              <h2 className="text-2xl font-black text-slate-900 uppercase tracking-tight">Finalizar Pedido</h2>
              <p className="text-slate-500 text-sm font-bold">Preencha para receber seu pedido</p>
            </div>
            <button 
              onClick={onClose}
              className="p-3 bg-white rounded-full shadow-sm hover:bg-slate-200 transition-colors"
            >
              <X size={24} className="text-slate-600" />
            </button>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit(onConfirm)} className="flex-1 overflow-y-auto p-8 space-y-8">
            
            {/* Identificação */}
            <div className="space-y-4">
              <h3 className="text-sm font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
                <User size={16} /> Quem é você?
              </h3>
              <div className="grid md:grid-cols-2 gap-4">
                <div className="space-y-1">
                  <label className="text-xs font-bold text-slate-600 ml-1">Seu Nome</label>
                  <input
                    {...register("customerName")}
                    className={cn(
                      "w-full bg-slate-50 border-2 rounded-xl p-4 text-lg font-bold outline-none transition-all focus:bg-white",
                      errors.customerName ? "border-red-500 focus:border-red-500" : "border-slate-200 focus:border-orange-500"
                    )}
                    placeholder="Ex: João Silva"
                  />
                  {errors.customerName && <p className="text-red-500 text-xs font-bold ml-1">{errors.customerName.message}</p>}
                </div>
                <div className="space-y-1">
                  <label className="text-xs font-bold text-slate-600 ml-1">WhatsApp (DDD + Número)</label>
                  <input
                    {...register("customerPhone")}
                    type="tel"
                    className={cn(
                      "w-full bg-slate-50 border-2 rounded-xl p-4 text-lg font-bold outline-none transition-all focus:bg-white",
                      errors.customerPhone ? "border-red-500 focus:border-red-500" : "border-slate-200 focus:border-orange-500"
                    )}
                    placeholder="Ex: 11999999999"
                  />
                  {errors.customerPhone && <p className="text-red-500 text-xs font-bold ml-1">{errors.customerPhone.message}</p>}
                </div>
              </div>
            </div>

            {/* Localização (Pickup Note) */}
            <div className="space-y-4">
              <h3 className="text-sm font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
                <MapPin size={16} /> Onde você está?
              </h3>
              <div className="space-y-1">
                <input
                  {...register("pickupNote")}
                  className={cn(
                    "w-full bg-slate-50 border-2 rounded-xl p-4 text-lg font-bold outline-none transition-all focus:bg-white",
                    errors.pickupNote ? "border-red-500 focus:border-red-500" : "border-slate-200 focus:border-orange-500"
                  )}
                  placeholder="Ex: Mesa 12, Balcão, Aguardando Senha..."
                />
                <p className="text-xs text-slate-400 ml-1">Isso ajuda o garçom a te encontrar.</p>
                {errors.pickupNote && <p className="text-red-500 text-xs font-bold ml-1">{errors.pickupNote.message}</p>}
              </div>
            </div>

            {/* Pagamento */}
            <div className="space-y-4">
              <h3 className="text-sm font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
                <CreditCard size={16} /> Como vai pagar?
              </h3>
              <div className="grid grid-cols-3 gap-4">
                {[
                  { id: "pix", label: "Pix", icon: QrCode },
                  { id: "card", label: "Cartão", icon: CreditCard },
                  { id: "cash", label: "Dinheiro", icon: Banknote },
                ].map((method) => (
                  <button
                    key={method.id}
                    type="button"
                    onClick={() => setValue("paymentMethod", method.id as any)}
                    className={cn(
                      "flex flex-col items-center justify-center p-4 rounded-2xl border-2 transition-all active:scale-95",
                      paymentMethod === method.id
                        ? "border-orange-500 bg-orange-50 text-orange-700 shadow-md"
                        : "border-slate-200 bg-white text-slate-500 hover:border-slate-300"
                    )}
                  >
                    <method.icon size={32} className="mb-2" />
                    <span className="font-black text-sm uppercase">{method.label}</span>
                    {paymentMethod === method.id && (
                      <div className="absolute top-2 right-2 text-orange-500">
                        <CheckCircle2 size={16} />
                      </div>
                    )}
                  </button>
                ))}
              </div>
              {errors.paymentMethod && <p className="text-red-500 text-xs font-bold ml-1">{errors.paymentMethod.message}</p>}
            </div>

            {/* Submit */}
            <div className="pt-4">
              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full py-5 rounded-2xl font-black text-xl text-white shadow-xl transition-all active:scale-[0.98] flex items-center justify-center gap-3 disabled:opacity-70 disabled:cursor-not-allowed"
                style={{ backgroundColor: primaryColor }}
              >
                {isSubmitting ? <Loader2 className="animate-spin" /> : <CheckCircle2 size={24} />}
                {isSubmitting ? "Processando..." : "Confirmar Pedido"}
              </button>
            </div>

          </form>
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
