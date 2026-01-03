"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { isAuthenticated, getUserRole } from "@/lib/auth";
import { Loader2 } from "lucide-react";

export default function DriverLayout({
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
      const role = getUserRole();
      if (role !== 'driver' && role !== 'owner' && role !== 'manager') {
        // Se não for motorista nem gerente, manda pro login
        router.push("/admin/login");
      } else {
        setIsAuth(true);
      }
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
      {children}
    </div>
  );
}