"use client";

import { useEffect, useState, use } from "react";
import { useRouter } from "next/navigation";
import { isAuthenticated } from "@/lib/auth";
import { Loader2 } from "lucide-react";
import NotificationManager from "@/components/waiter/NotificationManager";

export default function WaiterLayout({
  children,
  params
}: {
  children: React.ReactNode;
  params: Promise<{ slug: string }>;
}) {
  const { slug } = use(params); // Desembrulha params
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
      <NotificationManager slug={slug} />
      {children}
    </div>
  );
}