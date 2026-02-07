"use client";

import { useEffect } from "react";

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error("Global Error:", error);
  }, [error]);

  return (
    <html>
      <body className="bg-gray-900 text-white flex flex-col items-center justify-center min-h-screen p-6 text-center">
        <h2 className="text-3xl font-bold mb-4 text-red-500">Algo deu errado! 💥</h2>
        <div className="bg-gray-800 p-4 rounded-lg border border-gray-700 mb-6 max-w-lg overflow-auto text-left font-mono text-xs text-red-300">
          {error.message}
          {error.stack && <pre className="mt-2 opacity-50">{error.stack}</pre>}
        </div>
        <button
          onClick={() => reset()}
          className="bg-orange-600 hover:bg-orange-700 text-white font-bold py-3 px-6 rounded-xl transition-colors"
        >
          Tentar Novamente
        </button>
      </body>
    </html>
  );
}