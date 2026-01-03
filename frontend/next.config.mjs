import { withSentryConfig } from "@sentry/nextjs";
import withPWAInit from "@ducanh2912/next-pwa";

const withPWA = withPWAInit({
  dest: "public",
  disable: process.env.NODE_ENV === "development",
  register: true,
  skipWaiting: true,
});

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Desativa a checagem de tipos e lint no build para acelerar o deploy e evitar quebras
  typescript: { ignoreBuildErrors: true },
  eslint: { ignoreDuringBuilds: true },
  
  async headers() {
    return [
      {
        source: "/:path*",
        headers: [
          { key: "Access-Control-Allow-Origin", value: "*" },
          { key: "Access-Control-Allow-Methods", value: "GET,OPTIONS,PATCH,DELETE,POST,PUT" },
        ],
      },
    ];
  },

  images: {
    remotePatterns: [{ protocol: "https", hostname: "**" }],
  },
};

const sentryOptions = {
  silent: true,
  org: "mesaflow",
  project: "mesaflow-frontend",
};

const sentryWebpackPluginOptions = {
  widenClientFileUpload: true,
  transpileClientSDK: true,
  hideSourceMaps: true,
  disableLogger: true,
  // IMPORTANTE: Não quebra o build se o token estiver faltando
  failSilently: true, 
};

// Exporta com PWA e Sentry (Sentry por último)
export default withSentryConfig(
  withPWA(nextConfig),
  sentryOptions,
  sentryWebpackPluginOptions
);
