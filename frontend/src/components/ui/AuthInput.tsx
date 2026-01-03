"use client";

import { forwardRef, useState } from "react";
import { LucideIcon, Eye, EyeOff, AlertCircle } from "lucide-react";

interface AuthInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  icon: LucideIcon;
  error?: string;
}

const AuthInput = forwardRef<HTMLInputElement, AuthInputProps>(
  ({ label, icon: Icon, error, type = "text", className, ...props }, ref) => {
    const [showPassword, setShowPassword] = useState(false);
    const isPassword = type === "password";

    return (
      <div className="space-y-1.5">
        <label className="block text-sm font-bold text-gray-700 dark:text-gray-300">
          {label}
        </label>
        <div className="relative group">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none transition-colors">
            <Icon 
              className={`h-5 w-5 ${error ? "text-red-500" : "text-gray-400 group-focus-within:text-orange-500"}`} 
            />
          </div>
          
          <input
            ref={ref}
            type={isPassword ? (showPassword ? "text" : "password") : type}
            className={`
              w-full pl-10 pr-10 py-3 rounded-xl border bg-gray-50 dark:bg-gray-800 
              text-gray-900 dark:text-white placeholder-gray-400 transition-all outline-none
              ${error 
                ? "border-red-300 focus:ring-2 focus:ring-red-200 focus:border-red-500" 
                : "border-gray-200 dark:border-gray-700 focus:ring-2 focus:ring-orange-100 focus:border-orange-500"
              }
              ${className}
            `}
            {...props}
          />

          {isPassword && (
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600 transition-colors"
            >
              {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
            </button>
          )}
          
          {!isPassword && error && (
            <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
               <AlertCircle size={18} className="text-red-500" />
            </div>
          )}
        </div>
        {error && (
          <p className="text-xs text-red-500 font-medium animate-pulse ml-1">
            {error}
          </p>
        )}
      </div>
    );
  }
);

AuthInput.displayName = "AuthInput";
export default AuthInput;