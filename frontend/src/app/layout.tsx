import type { Metadata, Viewport } from "next";
import "./globals.css";
import Providers from "@/components/Providers";
import NetworkStatus from "@/components/ui/NetworkStatus";

export const metadata: Metadata = {
  title: "MesaFlow",
  description: "Autoatendimento Inteligente",
  applicationName: "MesaFlow",
  formatDetection: {
    telephone: false,
  },
  other: {
    "mobile-web-app-capable": "yes",
  }
};

export const viewport: Viewport = {
  themeColor: "#ea580c",
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    // suppressHydrationWarning é vital para evitar erros de console com next-themes
    <html lang="pt-BR" suppressHydrationWarning>
      <body className="antialiased bg-gray-50">
        <Providers>
          {children}
          <NetworkStatus />
        </Providers>
      </body>
    </html>
  );
}