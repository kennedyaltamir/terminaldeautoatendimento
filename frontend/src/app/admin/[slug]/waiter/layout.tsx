"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { isAuthenticated } from "@/lib/auth";
import { Loader2 } from "lucide-react";
import NotificationManager from "@/components/waiter/NotificationManager";
// O NetworkStatus já está no RootLayout, mas o hook useOfflineSync precisa rodar
// para garantir que a lógica de sync funcione mesmo se o componente visual não estiver montado.
// Porém, como o NetworkStatus usa o hook e está no RootLayout, ele já garante o funcionamento global.
// Então este arquivo permanece focado apenas em Auth e Layout visual.

export default function WaiterLayout({
  children,
  params
}: {
  children: React.ReactNode;
  params: { slug: string };
}) {
  const router = useRouter();
  const [isAuth, setIsAuth] = useState(false);

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push("/admin/login");
    } else {
      setIsAuth(true);
    }
  }, [router]);

  if (!isAuth) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900 text-white">
        <Loader2 className="animate-spin" size={32} />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 text-gray-900 font-sans pb-20">
      <NotificationManager slug={params.slug} />
      {children}
    </div>
  );
}