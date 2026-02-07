/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 1.0.0 (Customer Voice)
 * Objective: Capture order satisfaction and comments.
 */
"use client";

import React, { useState, use } from "react";
import { Star, Send, CheckCircle2, MessageSquare } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { sendOrderFeedback } from "@/lib/api";
import { toast } from "sonner";
import { cn } from "@/lib/utils";

export default function FeedbackPage({ params: paramsPromise }: { params: Promise<{ slug: string, orderId: string }> }) {
  const { slug, orderId } = use(paramsPromise);
  const [score, setScore] = useState(0);
  const [comment, setComment] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (score === 0) return toast.error("Por favor, selecione uma nota.");
    setLoading(true);
    try {
      await sendOrderFeedback(slug, orderId, score, comment);
      setSubmitted(true);
    } catch (e) {
      toast.error("Erro ao enviar feedback. Tente novamente.");
    } finally {
      setLoading(false);
    }
  };

  if (submitted) {
    return (
      <div className="min-h-screen bg-white flex flex-col items-center justify-center p-6 text-center">
        <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} className="w-20 h-20 bg-green-100 text-green-600 rounded-full flex items-center justify-center mb-6">
          <CheckCircle2 size={48} />
        </motion.div>
        <h1 className="text-2xl font-black text-slate-900 mb-2">Obrigado pelo feedback!</h1>
        <p className="text-slate-500">Sua opinião ajuda a melhorar nossa cozinha.</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 p-6 flex flex-col items-center justify-center font-sans">
      <div className="w-full max-w-md bg-white rounded-[2.5rem] p-8 shadow-xl border border-slate-100">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-black text-slate-900 tracking-tight">Como foi sua experiência?</h1>
          <p className="text-slate-500 text-sm mt-1">Pedido #{orderId.slice(-6).toUpperCase()}</p>
        </div>

        <div className="flex justify-center gap-2 mb-10">
          {[1, 2, 3, 4, 5].map((s) => (
            <button key={s} onClick={() => setScore(s)} className="transition-transform active:scale-90">
              <Star 
                size={40} 
                className={cn("transition-colors", s <= score ? "fill-orange-500 text-orange-500" : "text-slate-200")} 
              />
            </button>
          ))}
        </div>

        <div className="space-y-4">
          <div className="relative">
            <MessageSquare className="absolute top-4 left-4 text-slate-400" size={20} />
            <textarea 
              placeholder="Conte-nos mais (opcional)..."
              className="w-full bg-slate-50 border border-slate-200 rounded-2xl p-4 pl-12 text-slate-900 outline-none focus:border-orange-500 h-32 resize-none transition-all"
              value={comment}
              onChange={(e) => setComment(e.target.value)}
            />
          </div>

          <button 
            onClick={handleSubmit}
            disabled={loading || score === 0}
            className="w-full py-5 bg-orange-600 hover:bg-orange-700 disabled:bg-slate-200 text-white rounded-2xl font-black uppercase tracking-widest shadow-lg transition-all flex items-center justify-center gap-2"
          >
            {loading ? "Enviando..." : <><Send size={18} /> Enviar Avaliação</>}
          </button>
        </div>
      </div>
    </div>
  );
}

