"use client";

import { useState } from "react";
import { Star, X, Send, Loader2 } from "lucide-react";
import { toast } from "sonner";

interface FeedbackModalProps {
  isOpen: boolean;
  onClose: () => void;
  orderId: string;
  slug: string;
}

export default function FeedbackModal({ isOpen, onClose, orderId, slug }: FeedbackModalProps) {
  const [score, setScore] = useState(0);
  const [comment, setComment] = useState("");
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async () => {
    if (score === 0) return toast.error("Selecione uma nota de 1 a 5");

    setLoading(true);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/${slug}/orders/${orderId}/feedback`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ score, comment })
      });

      if (!res.ok) throw new Error("Erro ao enviar");

      setSubmitted(true);
      setTimeout(onClose, 2000);
    } catch (e) {
      toast.error("Erro ao enviar avaliação");
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[80] flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in">
      <div className="bg-white w-full max-w-sm rounded-2xl p-6 shadow-2xl relative overflow-hidden">
        <button onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-gray-600"><X size={24}/></button>

        {submitted ? (
          <div className="text-center py-8 animate-in zoom-in">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4 text-green-600">
              <Star size={32} fill="currentColor" />
            </div>
            <h3 className="text-xl font-bold text-gray-900">Obrigado!</h3>
            <p className="text-gray-500">Sua opinião é muito importante.</p>
          </div>
        ) : (
          <>
            <div className="text-center mb-6">
              <h3 className="text-xl font-bold text-gray-900">Como foi sua experiência?</h3>
              <p className="text-gray-500 text-sm">Avalie seu pedido para nos ajudar a melhorar.</p>
            </div>

            <div className="flex justify-center gap-2 mb-6">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  key={star}
                  onClick={() => setScore(star)}
                  className={`transition-transform hover:scale-110 ${score >= star ? 'text-yellow-400' : 'text-gray-200'}`}
                >
                  <Star size={40} fill="currentColor" />
                </button>
              ))}
            </div>

            <textarea
              className="w-full border border-gray-200 rounded-xl p-3 text-sm focus:ring-2 focus:ring-orange-500 outline-none resize-none bg-gray-50 mb-4"
              placeholder="Deixe um comentário (opcional)..."
              rows={3}
              value={comment}
              onChange={e => setComment(e.target.value)}
            />

            <button
              onClick={handleSubmit}
              disabled={loading || score === 0}
              className="w-full bg-orange-600 hover:bg-orange-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold py-3 rounded-xl flex items-center justify-center gap-2 transition-all shadow-lg"
            >
              {loading ? <Loader2 className="animate-spin" /> : <Send size={18} />}
              Enviar Avaliação
            </button>
          </>
        )}
      </div>
    </div>
  );
}
