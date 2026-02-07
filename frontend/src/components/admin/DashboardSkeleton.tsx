import Skeleton from "@/components/ui/Skeleton";

export default function DashboardSkeleton() {
  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      {/* Header Skeleton */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <Skeleton className="w-48 h-10 rounded-lg" />
          <Skeleton className="w-64 h-4 rounded-md mt-2" />
        </div>
        <div className="flex gap-2">
          <Skeleton className="w-32 h-10 rounded-lg" />
          <Skeleton className="w-20 h-10 rounded-lg" />
        </div>
      </div>

      {/* KPI Cards Skeleton */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {[1, 2, 3].map((i) => (
          <div key={i} className="bg-gray-800 border border-gray-700 p-6 rounded-2xl shadow-lg">
            <div className="flex justify-between items-start">
              <div className="space-y-3">
                <Skeleton className="w-24 h-3" />
                <Skeleton className="w-32 h-8" />
              </div>
              <Skeleton className="w-12 h-12 rounded-xl" />
            </div>
          </div>
        ))}
      </div>

      {/* Main Chart Skeleton */}
      <div className="bg-gray-800 border border-gray-700 rounded-2xl shadow-lg p-6">
        <Skeleton className="w-48 h-6 mb-6" />
        <Skeleton className="w-full h-[300px] rounded-xl" />
      </div>

      {/* Bottom Grid Skeleton */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-gray-800 border border-gray-700 rounded-2xl shadow-lg p-6">
          <Skeleton className="w-40 h-6 mb-6" />
          <Skeleton className="w-full h-[300px] rounded-xl" />
        </div>
        <div className="bg-gray-800 border border-gray-700 rounded-2xl shadow-lg p-6">
          <Skeleton className="w-40 h-6 mb-6" />
          <Skeleton className="w-full h-[300px] rounded-xl" />
        </div>
      </div>
    </div>
  );
}
