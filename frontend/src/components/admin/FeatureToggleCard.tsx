"use client";

import React from "react";
import { Zap, CheckCircle2, XCircle, Loader2 } from "lucide-react";

interface FeatureToggleCardProps {
  label: string;
  description: string;
  flagKey: string;
  isEnabled: boolean;
  isImpersonator: boolean;
  onToggle: (key: string) => Promise<void>;
}

export default function FeatureToggleCard({
  label,
  description,
  flagKey,
  isEnabled,
  isImpersonator,
  onToggle
}: FeatureToggleCardProps) {
  const [isProcessing, setIsProcessing] = React.useState(false);

  const handleToggle = async () => {
    if (!isImpersonator || isProcessing) return;
    
    setIsProcessing(true);
    try {
      await onToggle(flagKey);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="bg-gray-800 border border-gray-700 p-6 rounded-2xl flex items-center justify-between group hover:border-gray-600 transition-all shadow-sm">
      <div className="space-y-1 pr-4">
        <div className="flex items-center gap-2">
          <h3 className="font-bold text-white">{label}</h3>
          {isEnabled ? (
            <CheckCircle2 size={14} className="text-green-500" />
          ) : (
            <XCircle size={14} className="text-gray-500" />
          )}
        </div>
        <p className="text-sm text-gray-400 leading-relaxed">{description}</p>
        <code className="text-[10px] bg-black/30 px-2 py-0.5 rounded text-gray-500 font-mono">
          {flagKey}
        </code>
      </div>

      <div className="flex items-center gap-4">
        {isProcessing && <Loader2 size={16} className="animate-spin text-orange-500" />}
        
        <button
          disabled={!isImpersonator || isProcessing}
          onClick={handleToggle}
          className={`
            relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none
            ${isEnabled ? 'bg-orange-600' : 'bg-gray-700'}
            ${!isImpersonator ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
          `}
          aria-label={`Alternar ${label}`}
        >
          <span
            className={`
              ${isEnabled ? 'translate-x-6' : 'translate-x-1'}
              inline-block h-4 w-4 transform rounded-full bg-white transition-transform shadow-sm
            `}
          />
        </button>
      </div>
    </div>
  );
}
