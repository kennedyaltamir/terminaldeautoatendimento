import Skeleton from "@/components/ui/Skeleton";

export default function MenuAdminSkeleton() {
  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      {/* Header Skeleton */}
      <div className="bg-gray-800 p-4 rounded-xl border border-gray-700 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <Skeleton className="w-10 h-10 rounded-lg" />
          <div className="space-y-2">
            <Skeleton className="w-24 h-3" />
            <Skeleton className="w-48 h-4" />
          </div>
        </div>
        <div className="flex gap-2">
          <Skeleton className="w-20 h-8 rounded-lg" />
          <Skeleton className="w-20 h-8 rounded-lg" />
        </div>
      </div>

      <div className="flex justify-between items-center">
        <Skeleton className="w-64 h-10 rounded-lg" />
        <Skeleton className="w-40 h-10 rounded-lg" />
      </div>

      {/* Categories Loop */}
      {[1, 2].map((cat) => (
        <div key={cat} className="bg-gray-800 border border-gray-700 rounded-xl overflow-hidden shadow-xl">
          <div className="p-4 bg-gray-700/30 border-b border-gray-700 flex justify-between items-center">
            <Skeleton className="w-32 h-6" />
            <Skeleton className="w-8 h-8 rounded-lg" />
          </div>
          <div className="p-4 space-y-4">
            {[1, 2, 3].map((prod) => (
              <div key={prod} className="flex items-center justify-between bg-gray-900/40 p-4 rounded-lg border border-gray-700">
                <div className="flex items-center gap-4">
                  <Skeleton className="w-14 h-14 rounded-lg" />
                  <div className="space-y-2">
                    <Skeleton className="w-40 h-5" />
                    <Skeleton className="w-20 h-4" />
                  </div>
                </div>
                <div className="flex gap-2">
                  <Skeleton className="w-10 h-10 rounded-lg" />
                  <Skeleton className="w-24 h-10 rounded-lg" />
                  <Skeleton className="w-10 h-10 rounded-lg" />
                </div>
              </div>
            ))}
            <Skeleton className="w-full h-16 rounded-lg border-2 border-dashed border-gray-700" />
          </div>
        </div>
      ))}
    </div>
  );
}
