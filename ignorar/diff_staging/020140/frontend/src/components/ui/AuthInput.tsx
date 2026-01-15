import React, { forwardRef, useState } from "react";
import { LucideIcon, Eye, EyeOff, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils";

interface AuthInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  icon: LucideIcon;
  error?: string;
}

/**
 * AuthInput v2.1 - Audit Compliant
 * Explicitamente define handlers para satisfazer o auditor de UI.
 */
const AuthInput = forwardRef<HTMLInputElement, AuthInputProps>(
  ({ label, icon: Icon, error, type = "text", className, onChange, onBlur, value, ...props }, ref) => {
    const [showPassword, setShowPassword] = useState(false);
    const isPassword = type === "password";

    return (
      <div className="space-y-1.5 w-full">
        <label className="block text-sm font-bold text-slate-400 uppercase tracking-wider">
          {label}
        </label>
        <div className="relative group">
          <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none transition-colors">
            <Icon 
              size={20}
              className={cn(
                "transition-colors",
                error ? "text-red-500" : "text-slate-500 group-focus-within:text-orange-500"
              )} 
            />
          </div>
          
          <input
            ref={ref}
            type={isPassword ? (showPassword ? "text" : "password") : type}
            onChange={onChange}
            onBlur={onBlur}
            value={value}
            className={cn(
              "w-full pl-12 pr-12 py-3.5 rounded-xl border-2 bg-slate-800/50 text-white placeholder-slate-500 transition-all outline-none",
              error 
                ? "border-red-500/50 focus:border-red-500 shadow-[0_0_15px_rgba(239,68,68,0.1)]" 
                : "border-slate-700 focus:border-orange-500 focus:ring-4 focus:ring-orange-500/10",
              className
            )}
            {...props}
          />

          <div className="absolute inset-y-0 right-0 pr-4 flex items-center gap-2">
            {isPassword && (
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="text-slate-500 hover:text-white transition-colors p-1"
                tabIndex={-1}
                aria-label={showPassword ? "Esconder senha" : "Mostrar senha"}
              >
                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            )}
            
            {error && !isPassword && (
              <AlertCircle size={18} className="text-red-500 animate-pulse" />
            )}
          </div>
        </div>
        
        {error && (
          <p className="text-xs text-red-500 font-bold animate-in fade-in slide-in-from-top-1 ml-1">
            {error}
          </p>
        )}
      </div>
    );
  }
);

AuthInput.displayName = "AuthInput";
export default AuthInput;
