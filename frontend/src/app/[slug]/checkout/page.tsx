// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-16 11:50:00
import { Suspense } from "react";
import CheckoutClient from "./CheckoutClient";
import { Loader2 } from "lucide-react";

export default function CheckoutPage({ params }: { params: { slug: string } }) {
  return (
    <Suspense fallback={
      <div className="h-screen flex items-center justify-center bg-slate-950 text-white">
        <Loader2 className="animate-spin" size={48} />
      </div>
    }>
      <CheckoutClient slug={params.slug} />
    </Suspense>
  );
}

