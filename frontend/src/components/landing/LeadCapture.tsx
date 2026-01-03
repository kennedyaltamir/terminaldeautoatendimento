"use client";

import { useState, useEffect } from "react";
import { X, Mail, ArrowRight, CheckCircle2 } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export default function LeadCapture() {
  const [isOpen, setIsOpen] = useState(false);
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    // Mostrar após 10 segundos ou scroll de 50%
    const timer = setTimeout(() => {
      const hasSeen = sessionStorage.getItem("mesaflow_lead_popup");
      if (!hasSeen) setIsOpen(true);
    }, 10000);

    return () => clearTimeout(timer);
  }, []);

  const handleClose = () => {
    setIsOpen(false);
    sessionStorage.setItem("mesaflow_lead_popup", "true");
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Aqui enviaria para API de Marketing (Mailchimp/RD Station)
    setSubmitted(true);
    setTimeout(() => {
      handleClose();
    }, 3000);
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
          <motion.div 
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            className="bg-white dark:bg-gray-900 w-full max-w-lg rounded-2xl shadow-2xl overflow-hidden relative"
          >
            <button onClick={handleClose} className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 dark:hover:text-white z-10">
              <X size={24} />
            </button>

            <div className="flex flex-col md:flex-row">
              {/* Imagem Lateral (Desktop) */}
              <div className="hidden md:block w-1/3 bg-orange-600 relative">
                <div className="absolute inset-0 bg-[url('https://images.pexels.com/photos/3184183/pexels-photo-3184183.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1')] bg-cover bg-center opacity-50 mix-blend-multiply"></div>
                <div className="absolute bottom-4 left-4 text-white font-bold text-xs opacity-80">
                  Guia de Gestão 2026
                </div>
              </div>

              {/* Conteúdo */}
              <div className="flex-1 p-8">
                {submitted ? (
                  <div className="text-center py-10 animate-in fade-in">
                    <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4 text-green-600">
                      <CheckCircle2 size={32} />
                    </div>
                    <h3 className="text-2xl font-bold text-gray-900 dark:text-white">Sucesso!</h3>
                    <p className="text-gray-500 mt-2">O guia foi enviado para seu e-mail.</p>
                  </div>
                ) : (
                  <>
                    <div className="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center mb-4 text-orange-600">
                      <Mail size={24} />
                    </div>
                    <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                      Aumente seu lucro em 30%
                    </h3>
                    <p className="text-gray-500 dark:text-gray-400 text-sm mb-6 leading-relaxed">
                      Baixe nosso <b>Guia de Engenharia de Cardápio</b> e aprenda a técnica usada pelas grandes redes para vender mais.
                    </p>

                    <form onSubmit={handleSubmit} className="space-y-3">
                      <input 
                        type="email" 
                        required
                        placeholder="Seu melhor e-mail" 
                        className="w-full px-4 py-3 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 outline-none focus:ring-2 focus:ring-orange-500 transition-all"
                        value={email}
                        onChange={e => setEmail(e.target.value)}
                      />
                      <button className="w-full bg-gray-900 dark:bg-white text-white dark:text-gray-900 font-bold py-3 rounded-xl hover:opacity-90 transition-opacity flex items-center justify-center gap-2">
                        Baixar Grátis <ArrowRight size={18} />
                      </button>
                    </form>
                    <p className="text-xs text-center text-gray-400 mt-4">Livre de spam. Cancele quando quiser.</p>
                  </>
                )}
              </div>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}