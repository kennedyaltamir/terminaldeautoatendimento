/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 16.2.3 (Schema Compliance)
 * DNA_ID: MF-NEXT-CONFIG-V16-2-3
 */
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  output: "standalone",
  typedRoutes: true,
  // 🛡️ FIX: 'allowedDevOrigins' is deprecated/invalid in standard ExperimentalConfig for this version.
  // We use standard CORS headers handled at the Kernel (main.py) instead.
  experimental: {
    // Other experimental flags can go here if needed
  },
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "**",
      },
    ],
  },
};

export default nextConfig;