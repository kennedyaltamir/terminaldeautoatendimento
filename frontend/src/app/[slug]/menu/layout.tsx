"use client";

import { WebSocketProvider } from "@/context/WebSocketContext";

export default function MenuLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: { slug: string };
}) {
  return (
    <WebSocketProvider slug={params.slug}>
      {children}
    </WebSocketProvider>
  );
}