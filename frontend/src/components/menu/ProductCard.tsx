/**
 * DOMAIN: FRONTEND / UI
 * OBJECTIVE: Card de Produto imersivo com otimização de carregamento.
 * FIX: Added 'priority' to resolve LCP warning.
 */
"use client";
import { Product } from "@/types";
import { formatCurrency } from "@/lib/utils";
import { Plus } from "lucide-react";
import Image from "next/image";
import { motion } from "framer-motion";

interface ProductCardProps {
  product: Product;
  onClick: (e: React.MouseEvent) => void;
  primaryColor: string;
}

export default function ProductCard({ product, onClick, primaryColor }: ProductCardProps) {
  return (
    <motion.div 
      whileTap={{ scale: 0.95 }}
      onClick={onClick}
      className="group relative h-64 w-full rounded-[2rem] overflow-hidden cursor-pointer shadow-lg hover:shadow-2xl transition-all border border-slate-200 dark:border-slate-800 bg-slate-900"
      data-testid="product-card"
      data-product-name={product.name}
    >
      <div className="absolute inset-0 z-0">
        {product.image_url ? (
          <Image 
            src={product.image_url} 
            alt={product.name}
            fill
            sizes="(max-width: 768px) 100vw, 300px"
            priority={true} // 🚀 FIX: Resolve LCP warning para imagens acima da dobra
            className="object-cover transition-transform duration-700 group-hover:scale-110"
          />
        ) : (
          <div className="w-full h-full bg-slate-800 flex items-center justify-center">
            <span className="text-slate-600 font-bold text-xs uppercase tracking-widest">Sem Imagem</span>
          </div>
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent" />
      </div>
      
      <div className="absolute inset-0 z-10 p-5 flex flex-col justify-end">
        <div className="transform translate-y-2 group-hover:translate-y-0 transition-transform duration-300">
          <h3 className="font-black text-xl text-white leading-tight mb-1 drop-shadow-md">
            {product.name}
          </h3>
          <p className="text-xs text-slate-300 line-clamp-2 mb-3 opacity-0 group-hover:opacity-100 transition-opacity duration-300 delay-100">
            {product.description}
          </p>
          <div className="flex justify-between items-center">
            <span className="text-2xl font-black text-white drop-shadow-md">
              {formatCurrency(product.price)}
            </span>
            <div 
              className="w-10 h-10 rounded-full flex items-center justify-center text-white shadow-lg backdrop-blur-sm border border-white/20"
              style={{ backgroundColor: primaryColor }}
            >
              <Plus size={24} strokeWidth={3} />
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
