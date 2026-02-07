"use client";
import { useState } from "react";
import { ChefHat, MapPin, Bed, Ticket } from "lucide-react";
import { getSegmentLabels } from "@/lib/segment-utils";

export default function CheckInScreen({ 
  tableId, 
  status, 
  customerName, 
  onJoin,
  segment 
}: { 
  tableId: string, 
  status: 'free' | 'blocked', 
  customerName?: string, 
  onJoin: (name: string, pin?: string) => void,
  segment?: string
}) {
  const [name, setName] = useState("");
  const [pin, setPin] = useState("");

  const labels = getSegmentLabels(segment);

  const getIcon = () => {
    switch(segment) {
      case 'hotel': return <Bed size={48} />;
      case 'event': return <Ticket size={48} />;
      default: return <ChefHat size={48} />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 flex flex-col items-center justify-center p-6 text-center text-white font-sans">
      <div className="w-24 h-24 bg-orange-600 rounded-full flex items-center justify-center mb-8 shadow-2xl shadow-orange-500/30 animate-in zoom-in duration-500">
        {getIcon()}
      </div>

      <h1 className="text-3xl font-bold mb-2">
        {labels.table} {tableId}
      </h1>

      {status === 'free' ? (
        <div className="w-full max-w-xs animate-in slide-in-from-bottom-4 duration-700">
          <p className="text-gray-400 mb-8">Para começar, como podemos te chamar?</p>
          <input 
            type="text" 
            className="w-full bg-gray-800 border border-gray-700 rounded-xl p-4 text-center text-lg text-white focus:ring-2 focus:ring-orange-500 outline-none mb-4 placeholder-gray-500 transition-all"
            placeholder="Seu Nome"
            value={name}
            onChange={e => setName(e.target.value)}
            autoFocus
          />
          <button 
            onClick={() => name && onJoin(name)}
            disabled={!name}
            className="w-full bg-orange-600 text-white py-4 rounded-xl font-bold text-lg hover:bg-orange-700 transition-all shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Abrir {labels.table}
          </button>
        </div>
      ) : (
        <div className="w-full max-w-xs animate-in slide-in-from-bottom-4 duration-700">
          <div className="bg-gray-800/50 border border-gray-700 p-4 rounded-xl mb-6">
            <p className="text-gray-400 text-sm mb-1">{labels.table} ocupada por</p>
            <p className="text-white font-bold text-xl">{customerName}</p>
          </div>

          <div className="space-y-3">
            <p className="text-xs text-gray-500 uppercase font-bold tracking-widest">Entrar na Sessão</p>
            <input 
              type="text" 
              className="w-full bg-gray-800 border border-gray-600 rounded-lg p-3 text-center text-white focus:ring-2 focus:ring-orange-500 outline-none placeholder-gray-500"
              placeholder="Seu Nome"
              value={name}
              onChange={e => setName(e.target.value)}
            />
            <input 
              type="tel" 
              maxLength={10}
              className="w-full bg-gray-800 border border-gray-600 rounded-lg p-3 text-center text-white focus:ring-2 focus:ring-orange-500 outline-none tracking-[0.2em] font-mono text-lg placeholder-gray-500"
              placeholder="TOKEN DE ACESSO"
              value={pin}
              onChange={e => setPin(e.target.value)}
            />
            <button 
              onClick={() => name && pin && onJoin(name, pin)}
              disabled={!name || pin.length < 10}
              className="w-full bg-green-600 text-white py-4 rounded-xl font-bold text-lg hover:bg-green-700 transition-all shadow-lg disabled:opacity-50 disabled:cursor-not-allowed mt-4"
            >
              Entrar
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
