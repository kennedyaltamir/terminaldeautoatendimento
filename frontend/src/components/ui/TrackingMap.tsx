/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 21.4.0 (Clean UI Edition)
 * DNA_ID: MF-UI-MAP-V21-4-CLEAN
 * OBJETIVO: Remover controles duplicados e garantir que o mapa seja apenas uma tela de visualização limpa.
 * Os controles agora são gerenciados pelo componente pai (EnRouteView).
 */
"use client";

import { useEffect, useMemo, useState } from "react";
import { MapContainer, TileLayer, Marker, Polyline, useMap, useMapEvents } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { Layers, Route, RouteOff } from "lucide-react";
import { cn } from "@/lib/utils";

// --- HELPERS: POLYLINE DECODER ---
function decodePolyline(str: string): [number, number][] {
  let index = 0, lat = 0, lng = 0, coordinates = [], shift = 0, result = 0, byte = null;
  while (index < str.length) {
    byte = null; shift = 0; result = 0;
    do {
      byte = str.charCodeAt(index++) - 63;
      result |= (byte & 0x1f) << shift;
      shift += 5;
    } while (byte >= 0x20);
    lat += ((result & 1) ? ~(result >> 1) : (result >> 1));
    shift = 0; result = 0;
    do {
      byte = str.charCodeAt(index++) - 63;
      result |= (byte & 0x1f) << shift;
      shift += 5;
    } while (byte >= 0x20);
    lng += ((result & 1) ? ~(result >> 1) : (result >> 1));
    coordinates.push([lat / 1e5, lng / 1e5] as [number, number]);
  }
  return coordinates;
}

export type MapMode = "AUTO_FOLLOW" | "MANUAL";

export interface TrackingMapProps {
  driverPos: [number, number] | null;
  clientPos: [number, number] | null;
  routeGeojson?: any;
  mapMode?: MapMode;
  onMapModeChange?: (mode: MapMode) => void;
}

const DriverIcon = L.divIcon({
  className: "driver-marker-container",
  html: `<div class="tactical-marker driver-core"><div class="pulse-ring"></div><div class="direction-arrow"></div></div>`,
  iconSize: [40, 40],
  iconAnchor: [20, 20]
});

const DestinationIcon = L.divIcon({
  className: "dest-marker-container",
  html: `<div class="tactical-marker dest-core"><div class="halo-ring"></div></div>`,
  iconSize: [30, 30],
  iconAnchor: [15, 15]
});

const MapController = ({ driverPos, mapMode, onMapModeChange }: { 
  driverPos: [number, number] | null, 
  mapMode: MapMode,
  onMapModeChange?: (mode: MapMode) => void 
}) => {
  const map = useMap();
  useMapEvents({ dragstart: () => onMapModeChange?.("MANUAL"), zoomstart: () => onMapModeChange?.("MANUAL") });
  useEffect(() => {
    if (driverPos && mapMode === "AUTO_FOLLOW") map.flyTo(driverPos, map.getZoom());
  }, [driverPos, mapMode, map]);
  return null;
};

export default function TrackingMap({ driverPos, clientPos, routeGeojson, mapMode = "AUTO_FOLLOW", onMapModeChange }: TrackingMapProps) {
  const [isMounted, setIsMounted] = useState(false);
  const [mapType, setMapType] = useState<"dark" | "satellite">("dark");
  const [showRoute, setShowRoute] = useState(true);

  useEffect(() => { setIsMounted(true); return () => setIsMounted(false); }, []);

  const routePositions = useMemo(() => {
    if (!routeGeojson) return null;
    if (typeof routeGeojson === 'string') return decodePolyline(routeGeojson);
    if (routeGeojson.type === 'LineString') return routeGeojson.coordinates.map((coord: number[]) => [coord[1], coord[0]] as [number, number]);
    if (Array.isArray(routeGeojson)) return routeGeojson;
    return null;
  }, [routeGeojson]);

  if (!isMounted) return <div className="w-full h-full bg-slate-950 animate-pulse rounded-[2rem]" />;

  return (
    <div className="relative w-full h-full bg-slate-900 z-0 overflow-hidden rounded-[2rem] border border-white/5">
      <style jsx global>{`
        .tactical-marker { position: relative; border-radius: 50%; border: 3px solid #fff; }
        .driver-core { width: 18px; height: 18px; background: #3b82f6; box-shadow: 0 0 20px #3b82f6; }
        .dest-core { width: 14px; height: 14px; background: #ef4444; box-shadow: 0 0 15px #ef4444; }
        @keyframes tactical-pulse { 0% { transform: scale(0.5); opacity: 0.8; } 100% { transform: scale(1.5); opacity: 0; } }
        .pulse-ring { position: absolute; width: 40px; height: 40px; border: 2px solid #3b82f6; border-radius: 50%; top: -14px; left: -14px; opacity: 0; animation: tactical-pulse 2s infinite; }
      `}</style>

      {/* 🕹️ CONTROLES INTERNOS DO MAPA (CAMADA E ROTA) - ALINHADOS À DIREITA */}
      <div className="absolute top-4 right-4 z-[500] flex flex-col gap-3">
         <button onClick={() => setMapType(mapType === 'dark' ? 'satellite' : 'dark')} className="p-3 bg-slate-900/90 backdrop-blur-xl border border-white/10 rounded-2xl text-white shadow-2xl active:scale-90 transition-all">
            <Layers size={20} className={mapType === 'satellite' ? 'text-orange-500' : 'text-blue-400'} />
         </button>
         <button onClick={() => setShowRoute(!showRoute)} className={cn("p-3 backdrop-blur-xl border rounded-2xl shadow-2xl active:scale-90 transition-all", showRoute ? "bg-blue-600/20 border-blue-500/50 text-blue-400" : "bg-slate-900/90 border-white/10 text-slate-500")}>
            {showRoute ? <Route size={20} /> : <RouteOff size={20} />}
         </button>
      </div>

      <MapContainer center={driverPos || [-19.2244, -44.9354]} zoom={17} zoomControl={false} attributionControl={false} className="w-full h-full">
        <TileLayer url={mapType === 'dark' ? "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png" : "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"} />
        <MapController driverPos={driverPos} mapMode={mapMode} onMapModeChange={onMapModeChange} />
        {showRoute && routePositions && (
          <>
            <Polyline positions={routePositions} pathOptions={{ color: "#3b82f6", weight: 12, opacity: 0.15, lineCap: 'round' }} />
            <Polyline positions={routePositions} pathOptions={{ color: "#3b82f6", weight: 6, opacity: 0.9, lineCap: 'round', lineJoin: 'round' }} />
          </>
        )}
        {driverPos && <Marker position={driverPos} icon={DriverIcon} zIndexOffset={2000} />}
        {clientPos && <Marker position={clientPos} icon={DestinationIcon} zIndexOffset={1000} />}
      </MapContainer>
    </div>
  );
}