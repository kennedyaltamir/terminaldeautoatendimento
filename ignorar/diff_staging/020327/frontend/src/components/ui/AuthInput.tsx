import React, { forwardRef, useState } from "react";
import { LucideIcon, Eye, EyeOff, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils";

interface AuthInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  icon: LucideIcon;
  error?: string;
}

/**
 * AuthInput v2.2 - Enterprise Grade & Audit Compliant
 * Componente de entrada de alto desempenho com suporte a temas, validação visual e acessibilidade.
 */
const AuthInput = forwardRef<HTMLInputElement, AuthInputProps>(
  ({ label, icon: Icon, error, type = "text", className, onChange, onBlur, value, name, ...props }, ref) => {
    const [showPassword, setShowPassword] = useState(false);
    const isPassword = type === "password";

    return (
      <div className="space-y-2 w-full animate-in fade-in slide-in-from-top-1 duration-300">
        <div className="flex justify-between items-end px-1">
          <label className="text-xs font-black text-slate-500 dark:text-slate-400 uppercase tracking-[0.15em]">
            {label}
          </label>
          {error && (
            <span className="text-[10px] font-bold text-red-500 uppercase tracking-tighter animate-pulse">
              {error}
            </span>
          )}
        </div>

        <div className="relative group">
          {/* Ícone de Contexto */}
          <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none transition-all duration-300">
            <Icon 
              size={18}
              className={cn(
                "transition-colors duration-300",
                error 
                  ? "text-red-500" 
                  : "text-slate-500 group-focus-within:text-orange-500 group-focus-within:scale-110"
              )} 
            />
          </div>
          
          <input
            ref={ref}
            name={name}
            type={isPassword ? (showPassword ? "text" : "password") : type}
            onChange={onChange}
            onBlur={onBlur}
            value={value}
            className={cn(
              "w-full pl-12 pr-12 py-4 rounded-2xl border-2 bg-slate-50 dark:bg-slate-800/50 text-slate-900 dark:text-white placeholder-slate-400 transition-all duration-300 outline-none font-bold text-sm",
              error 
                ? "border-red-500/50 focus:border-red-500 shadow-[0_0_20px_rgba(239,68,68,0.1)]" 
                : "border-slate-200 dark:border-slate-800 focus:border-orange-500 focus:ring-4 focus:ring-orange-500/10 dark:focus:border-orange-500",
              className
            )}
            {...props}
          />

          {/* Área de Ação Direita */}
          <div className="absolute inset-y-0 right-0 pr-4 flex items-center gap-2">
            {isPassword ? (
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="text-slate-400 hover:text-orange-500 transition-colors p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800"
                tabIndex={-1}
                aria-label={showPassword ? "Ocultar senha" : "Exibir senha"}
              >
                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            ) : error ? (
              <AlertCircle size={18} className="text-red-500" />
            ) : null}
          </div>
        </div>
      </div>
    );
  }
);

AuthInput.displayName = "AuthInput";
export default AuthInput;
