// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-10 15:20:00
import PublicMonitorView from "@/components/menu/PublicMonitorView";

export default function PublicMonitorPage({ params }: { params: { slug: string } }) {
  return (
    <main className="min-h-screen bg-black">
      <PublicMonitorView slug={params.slug} />
    </main>
  );
}
