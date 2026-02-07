"use client";

import { X } from "lucide-react";
import { useEffect, useRef, useCallback } from "react";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

export default function Modal({ isOpen, onClose, title, children }: ModalProps) {
  const modalRef = useRef<HTMLDivElement>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);

  const handleFocusTrap = useCallback((e: KeyboardEvent) => {
    if (e.key !== "Tab" || !modalRef.current) return;

    const focusableElements = modalRef.current.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const firstElement = focusableElements[0] as HTMLElement;
    const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement;

    if (e.shiftKey) {
      if (document.activeElement === firstElement) {
        e.preventDefault();
        lastElement.focus();
      }
    } else {
      if (document.activeElement === lastElement) {
        e.preventDefault();
        firstElement.focus();
      }
    }
  }, []);

  useEffect(() => {
    if (isOpen) {
      // 🛡️ Focus Return: Salva o elemento que disparou o modal
      previousFocusRef.current = document.activeElement as HTMLElement;
      
      const handleKeyDown = (e: KeyboardEvent) => {
        if (e.key === "Escape") onClose();
        handleFocusTrap(e);
      };

      document.addEventListener("keydown", handleKeyDown);
      
      // Move o foco para o modal para leitores de tela
      setTimeout(() => modalRef.current?.focus(), 50);

      return () => document.removeEventListener("keydown", handleKeyDown);
    } else {
      // 🛡️ Focus Return: Restaura o foco ao fechar
      previousFocusRef.current?.focus();
    }
  }, [isOpen, onClose, handleFocusTrap]);

  if (!isOpen) return null;

  return (
    <div 
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-300"
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div 
        ref={modalRef}
        className="bg-gray-800 border border-gray-700 w-full max-w-md rounded-xl shadow-2xl animate-in zoom-in duration-200 outline-none"
        tabIndex={-1}
      >
        <div className="flex justify-between items-center p-4 border-b border-gray-700">
          <h3 id="modal-title" className="text-lg font-bold text-white uppercase tracking-tight">{title}</h3>
          <button 
            onClick={onClose} 
            className="text-gray-400 hover:text-white transition-colors p-2 rounded-lg hover:bg-gray-700 focus:ring-2 focus:ring-orange-500"
            aria-label="Fechar modal"
          >
            <X size={20} />
          </button>
        </div>
        <div className="p-6">
          {children}
        </div>
      </div>
    </div>
  );
}
