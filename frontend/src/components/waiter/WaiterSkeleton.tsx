import Skeleton from "@/components/ui/Skeleton";

export default function WaiterSkeleton() {
  return (
    <div className="p-4 grid grid-cols-2 gap-3 pb-24 animate-in fade-in">
      {[1, 2, 3, 4, 5, 6].map((i) => (
        <div 
          key={i}
          className="p-4 rounded-xl border-2 border-gray-200 bg-gray-50 h-32 flex flex-col justify-between"
        >
          <div className="flex justify-between items-start">
            <Skeleton className="w-8 h-8 rounded-md" />
            <Skeleton className="w-3 h-3 rounded-full" />
          </div>
          
          <div className="space-y-2">
            <Skeleton className="w-24 h-4 rounded-md" />
            <Skeleton className="w-16 h-3 rounded-md" />
            <Skeleton className="w-20 h-4 rounded-md mt-1" />
          </div>
        </div>
      ))}
    </div>
  );
}
