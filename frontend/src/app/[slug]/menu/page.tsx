/**
 * DOMAIN: FRONTEND
 * FILE: src/app/[slug]/menu/page.tsx
 * OBJECTIVE: Entry point do Cardápio Digital.
 * FIX: Implementação de Async Params para compatibilidade com Next.js 15/16.
 */
import { Suspense } from "react";
import MenuClient from "./MenuClient";
import MenuSkeleton from "@/components/menu/MenuSkeleton";

interface MenuPageProps {
  params: Promise<{ slug: string }>;
}

export default async function MenuPage({ params }: MenuPageProps) {
  // 🛡️ PROTOCOLO NEXT 15/16: Unwrapping obrigatório da Promise de params
  const { slug } = await params;

  if (!slug) {
    return <div>Erro: Identificador do restaurante ausente.</div>;
  }

  return (
    <Suspense fallback={<MenuSkeleton />}>
      <MenuClient slug={slug} />
    </Suspense>
  );
}
 