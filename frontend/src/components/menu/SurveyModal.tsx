"use client";
import { useState } from "react";
import { Star, X } from "lucide-react";
import Modal from "@/components/ui/Modal";
import { toast } from "sonner";

interface SurveyModalProps {
  isOpen: boolean;
  onFinish: (score: number, comment: string) => void;
}

export default function SurveyModal({ isOpen, onFinish }: SurveyModalProps) {
  const [score, setScore] = useState(0);
  const [comment, setComment] = useState("");

  const handleSubmit = () => {
    onFinish(score, comment);
    toast.success("Obrigado pela avaliação!");
  };

  const handleSkip = () => {
    onFinish(0, "");
  };

  if (!isOpen) return null;

  return (
    <Modal isOpen={isOpen} onClose={() => {}} title="Como foi sua experiência?">
      <div className="text-center space-y-6 py-4">
        <p className="text-gray-500">Sua opinião nos ajuda a melhorar.</p>

        <div className="flex justify-center gap-2">
          {[1, 2, 3, 4, 5].map((star) => (
            <button
              key={star}
              onClick={() => setScore(star)}
              className="transition-transform hover:scale-110 focus:outline-none"
            >
              <Star 
                size={40} 
                className={`${star <= score ? "fill-yellow-400 text-yellow-400" : "text-gray-300"}`} 
                strokeWidth={1.5}
              />
            </button>
          ))}
        </div>

        <textarea
          placeholder="Deixe um comentário (opcional)..."
          className="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-orange-500 outline-none resize-none h-24 text-sm"
          value={comment}
          onChange={(e) => setComment(e.target.value)}
        />

        <div className="flex gap-3">
          <button 
            onClick={handleSkip}
            className="flex-1 py-3 rounded-xl font-bold text-gray-500 hover:bg-gray-100 transition-colors"
          >
            Pular
          </button>
          <button 
            onClick={handleSubmit}
            disabled={score === 0}
            className="flex-[2] bg-orange-600 text-white py-3 rounded-xl font-bold shadow-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-orange-700 transition-all"
          >
            Enviar Avaliação
          </button>
        </div>
      </div>
    </Modal>
  );
}
