"use client";

import React, { use } from "react";
import { WebSocketProvider } from "@/context/WebSocketContext";

interface MenuLayoutProps {
  children: React.ReactNode;
  params: Promise<{ slug: string }>; // Next.js 15: params é Promise
}

export default function MenuLayout({ children, params }: MenuLayoutProps) {
  // Desembrulha a Promise usando o hook 'use' do React
  const { slug } = use(params);

  return (
    <WebSocketProvider slug={slug}>
      {children}
    </WebSocketProvider>
  );
}