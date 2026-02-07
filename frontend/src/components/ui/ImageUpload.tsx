"use client";

import { useState, useRef } from "react";
import { Upload, X, Image as ImageIcon, Loader2 } from "lucide-react";
import { toast } from "sonner";

interface ImageUploadProps {
  value?: string | null;
  onChange: (url: string) => void;
  label?: string;
  className?: string;
}

export default function ImageUpload({ value, onChange, label, className = "" }: ImageUploadProps) {
  const [loading, setLoading] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validação de Tamanho (Max 2MB)
    if (file.size > 2 * 1024 * 1024) {
      toast.error("A imagem deve ter no máximo 2MB.");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const token = localStorage.getItem("mesaflow_access_token");
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/upload/`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
        body: formData,
      });

      if (!res.ok) throw new Error("Falha no upload");

      const data = await res.json();
      onChange(data.url);
      toast.success("Imagem carregada!");
    } catch (error) {
      console.error(error);
      toast.error("Erro ao enviar imagem.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`space-y-2 ${className}`}>
      {label && <label className="block text-sm font-bold text-gray-700 dark:text-gray-300">{label}</label>}
      
      <div 
        onClick={() => inputRef.current?.click()}
        className={`
          relative w-full h-40 rounded-xl border-2 border-dashed transition-all cursor-pointer overflow-hidden group
          ${value ? 'border-orange-500 bg-gray-900' : 'border-gray-300 hover:border-orange-400 bg-gray-50 hover:bg-gray-100'}
        `}
      >
        <input 
          type="file" 
          ref={inputRef} 
          className="hidden" 
          accept="image/png, image/jpeg, image/webp" 
          onChange={handleFileChange}
        />

        {loading ? (
          <div className="absolute inset-0 flex items-center justify-center bg-black/50 z-10">
            <Loader2 className="animate-spin text-white" size={32} />
          </div>
        ) : value ? (
          <>
            <img src={value} alt="Preview" className="w-full h-full object-cover" />
            <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
              <p className="text-white font-bold text-sm flex items-center gap-2">
                <Upload size={16} /> Trocar Imagem
              </p>
            </div>
            <button 
              onClick={(e) => { e.stopPropagation(); onChange(""); }}
              className="absolute top-2 right-2 bg-red-600 text-white p-1.5 rounded-full hover:bg-red-700 transition-colors z-20"
              title="Remover"
            >
              <X size={14} />
            </button>
          </>
        ) : (
          <div className="absolute inset-0 flex flex-col items-center justify-center text-gray-400 group-hover:text-orange-500 transition-colors">
            <ImageIcon size={32} className="mb-2" />
            <p className="text-xs font-bold uppercase">Clique para enviar</p>
            <p className="text-[10px] opacity-70">JPG, PNG ou WEBP (Max 2MB)</p>
          </div>
        )}
      </div>
    </div>
  );
}