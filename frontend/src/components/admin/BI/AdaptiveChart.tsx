"use client";

import React from 'react';
import { 
  AreaChart, Area, XAxis, YAxis, CartesianGrid, 
  Tooltip, ResponsiveContainer 
} from 'recharts';
import { formatCurrency } from '@/lib/utils';
import { BarChart3 } from 'lucide-react';

/**
 * 🛡️ FIX: Interface definida para aceitar viewMode e onPointClick
 */
interface AdaptiveChartProps {
  data: any[];
  viewMode: 'total' | 'channels';
  onPointClick: (data: any) => void;
}

export default function AdaptiveChart({ data, viewMode, onPointClick }: AdaptiveChartProps) {
  if (!data || data.length === 0) {
    return (
      <div className="h-[320px] w-full flex flex-col items-center justify-center text-slate-500 border-2 border-dashed border-slate-800 rounded-[3rem]">
        <BarChart3 size={48} className="mb-4 opacity-20" />
        <p className="font-bold uppercase tracking-widest text-[10px]">Aguardando dados de faturamento...</p>
      </div>
    );
  }

  return (
    <div className="w-full h-[320px]">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart 
          data={data} 
          onClick={(e) => e && e.activePayload && onPointClick(e.activePayload[0].payload)}
          margin={{ top: 10, right: 10, left: 0, bottom: 0 }}
        >
          <defs>
            <linearGradient id="colorRev" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#ea580c" stopOpacity={0.4}/>
              <stop offset="95%" stopColor="#ea580c" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
          <XAxis 
            dataKey="date" 
            stroke="#475569" 
            fontSize={11} 
            tickLine={false} 
            axisLine={false}
            dy={10}
          />
          <YAxis 
            stroke="#475569" 
            fontSize={11} 
            tickLine={false} 
            axisLine={false}
            tickFormatter={(val) => `R$ ${val}`}
          />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: '#0f172a', 
              border: '1px solid #334155', 
              borderRadius: '16px',
              boxShadow: '0 20px 25px -5px rgb(0 0 0 / 0.5)'
            }}
            itemStyle={{ color: '#ea580c', fontWeight: 'bold' }}
            formatter={(val: number) => [formatCurrency(val), 'Receita']}
          />
          <Area 
            type="monotone" 
            dataKey="simulatedValue" 
            stroke="#ea580c" 
            strokeWidth={4}
            fillOpacity={1} 
            fill="url(#colorRev)" 
            dot={{ r: 4, fill: '#ea580c', strokeWidth: 2, stroke: '#000' }}
            activeDot={{ r: 8, fill: '#fff', stroke: '#ea580c', strokeWidth: 4 }}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}