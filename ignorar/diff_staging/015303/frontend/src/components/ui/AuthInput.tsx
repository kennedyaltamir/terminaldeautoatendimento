import React from "react";
import { LucideIcon } from "lucide-react";

interface AuthInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  icon: LucideIcon;
  error?: string;
}

/**
 * AuthInput - Componente de entrada padronizado para autenticação e formulários admin.
 * Utiliza forwardRef para integração perfeita com react-hook-form.
 */
const AuthInput = React.forwardRef<HTMLInputElement, AuthInputProps>(
  ({ label, icon: Icon, error, onChange, onBlur, name, ...props }, ref) => {
    return (
      <div className="space-y-1.5">
        <label className="block text-sm font-bold text-gray-400 uppercase tracking-wider">
          {label}
        </label>
        <div className="relative group">
          <div className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 group-focus-within:text-orange-500 transition-colors">
            <Icon size={20} />
          </div>
          <input
            ref={ref}
            name={name}
            onChange={onChange}
            onBlur={onBlur}
            {...props}
            className={`w-full bg-gray-900 border-2 rounded-xl py-3.5 pl-12 pr-4 text-white outline-none transition-all ${
              error ? "border-red-500 shadow-[0_0_10px_rgba(239,68,68,0.2)]" : "border-gray-700 focus:border-orange-500"
            }`}
          />
        </div>
        {error && <p className="text-red-500 text-xs font-bold animate-in fade-in slide-in-from-top-1">{error}</p>}
      </div>
    );
  }
);

AuthInput.displayName = "AuthInput";

export default AuthInput;
