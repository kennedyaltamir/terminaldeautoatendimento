"use client";

import React, { useEffect, useState, use } from 'react'; // FIX: Import 'use'
import { useCart } from '@/context/CartContext';
import { useWebSocket } from '@/hooks/useWebSocket';
import { useRouter } from 'next/navigation';
import { isAuthenticated } from '@/lib/auth';

export interface RenderProps {
  data: any;
  items: any[];
  total: number;
  params: { slug: string };
  slug: string;
  clearCart: () => void;
}

export interface SovereignConfig {
  id: string;
  domain: string;
  authRequired: boolean;
  fetchData?: (params: { slug: string }) => Promise<any>;
  onMessage?: (msg: any, setData: any) => void;
  render: (props: RenderProps) => React.ReactNode;
}

export function createSovereignPage(config: SovereignConfig) {
  return function SovereignPage({ params: paramsPromise }: { params: Promise<{ slug: string }> }) {
    // 🛡️ PROTOCOLO NEXT 16: Unwrapping da Promise de params
    const params = use(paramsPromise);
    const slug = params.slug;

    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const { items, total, clearCart } = useCart();
    const router = useRouter();

    useEffect(() => {
      let mounted = true;
      const init = async () => {
        if (config.authRequired && !isAuthenticated()) {
          router.push('/admin/login');
          return;
        }
        try {
          if (config.fetchData && slug) {
            const result = await config.fetchData({ slug });
            if (mounted) setData(result);
          }
        } catch (error) {
          console.error("Sovereign Page Load Error:", error);
        } finally {
          if (mounted) setLoading(false);
        }
      };
      init();
      return () => { mounted = false; };
    }, [slug, router]);

    useWebSocket(slug, (msg: any) => {
      if (config.onMessage) config.onMessage(msg, setData);
    });

    if (loading) {
      return (
        <div className="flex h-screen items-center justify-center bg-slate-950">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-orange-600 border-t-transparent" />
        </div>
      );
    }

    return (
      <div className="sovereign-wrapper" data-dna={config.id}>
        {config.render({ data, items, total, params, slug, clearCart })}
      </div>
    );
  };
}
