// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 14:20:00
"use client";

import { useEffect } from "react";
import { MapContainer, TileLayer, Marker, Polyline, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

const icon = L.icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

const driverIcon = L.divIcon({
  className: "custom-div-icon",
  html: `<div style="background-color: #ea580c; width: 44px; height: 44px; border-radius: 50%; border: 4px solid white; display: flex; align-items: center; justify-content: center; font-size: 22px; box-shadow: 0 4px 10px rgba(0,0,0,0.4); animation: pulse 2s infinite;">🛵</div>`,
  iconSize: [44, 44],
  iconAnchor: [22, 22],
});

function MapResizer({ bounds }: { bounds: L.LatLngBoundsExpression }) {
  const map = useMap();
  useEffect(() => {
    if (bounds) {
      map.fitBounds(bounds, { padding: [40, 40], maxZoom: 16 });
    }
  }, [bounds, map]);
  return null;
}

interface TrackingMapProps {
  driverPos: [number, number];
  clientPos: [number, number];
  routeGeojson?: any;
  duration?: number;
}

export default function TrackingMap({ driverPos, clientPos, routeGeojson, duration }: TrackingMapProps) {
  const polylinePositions = routeGeojson?.coordinates.map(
    ([lng, lat]: [number, number]) => [lat, lng] as [number, number]
  );

  const etaMinutes = duration ? Math.ceil(duration / 60) : null;

  return (
    <div className="relative w-full h-full rounded-[2.5rem] overflow-hidden border-4 border-white shadow-2xl bg-slate-100">
      {/* Badge de ETA (Tempo Estimado) */}
      {etaMinutes && (
        <div className="absolute top-6 left-1/2 -translate-x-1/2 z-[1000] bg-slate-900/90 backdrop-blur-md text-white px-6 py-2.5 rounded-full border border-white/20 flex items-center gap-3 shadow-2xl">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-ping" />
          <span className="text-xs font-black uppercase tracking-[0.2em]">Chegada: {etaMinutes} min</span>
        </div>
      )}
      
      <MapContainer
        center={driverPos}
        zoom={15}
        className="w-full h-full"
        zoomControl={false}
        attributionControl={false}
      >
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <Marker position={clientPos} icon={icon} />
        <Marker position={driverPos} icon={driverIcon} />
        {polylinePositions && (
          <Polyline 
            positions={polylinePositions} 
            color="#ea580c" 
            weight={6} 
            opacity={0.4} 
            dashArray="1, 12" 
            lineCap="round"
          />
        )}
        <MapResizer bounds={[driverPos, clientPos]} />
      </MapContainer>
    </div>
  );
}
