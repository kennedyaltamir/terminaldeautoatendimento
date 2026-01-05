import Skeleton from "@/components/ui/Skeleton";

export default function InventorySkeleton() {
  return (
    <div className="space-y-6 pb-20 animate-in fade-in duration-500">
      <div className="flex justify-between items-center">
        <div>
          <Skeleton className="w-64 h-10 rounded-lg" />
          <Skeleton className="w-48 h-4 mt-2" />
        </div>
        <Skeleton className="w-44 h-11 rounded-xl" />
      </div>

      <div className="bg-gray-800 border border-gray-700 rounded-xl p-4">
        <div className="mb-6">
          <Skeleton className="w-full h-12 rounded-lg" />
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-900">
              <tr>
                {[1, 2, 3, 4, 5].map((i) => (
                  <th key={i} className="px-4 py-3 text-left">
                    <Skeleton className="w-20 h-3" />
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700">
              {[1, 2, 3, 4, 5, 6].map((row) => (
                <tr key={row}>
                  <td className="px-4 py-4"><Skeleton className="w-32 h-4" /></td>
                  <td className="px-4 py-4"><Skeleton className="w-12 h-6 rounded-md" /></td>
                  <td className="px-4 py-4"><Skeleton className="w-16 h-4" /></td>
                  <td className="px-4 py-4"><Skeleton className="w-20 h-4" /></td>
                  <td className="px-4 py-4 flex justify-end gap-2">
                    <Skeleton className="w-8 h-8 rounded-lg" />
                    <Skeleton className="w-8 h-8 rounded-lg" />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
