// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 12:50:00
"use client";

import { useEffect } from "react";
import { MapContainer, TileLayer, Marker, Polyline, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

// Fix para ícones do Leaflet no Next.js
const icon = L.icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

const driverIcon = L.divIcon({
  className: "bg-orange-600 rounded-full border-4 border-white shadow-lg",
  html: `<div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; color: white;">🛵</div>`,
  iconSize: [40, 40],
  iconAnchor: [20, 20],
});

/**
 * Componente interno para ajustar o zoom automaticamente quando a rota muda
 */
function MapResizer({ bounds }: { bounds?: L.LatLngBoundsExpression }) {
  const map = useMap();
  useEffect(() => {
    if (bounds) {
      map.fitBounds(bounds, { padding: [50, 50] });
    }
  }, [bounds, map]);
  return null;
}

interface TrackingMapProps {
  driverPos: [number, number];
  clientPos: [number, number];
  routeGeojson?: any;
  interactive?: boolean;
}

export default function TrackingMap({ driverPos, clientPos, routeGeojson, interactive = true }: TrackingMapProps) {
  const polylinePositions = routeGeojson?.coordinates.map(
    ([lng, lat]: [number, number]) => [lat, lng] as [number, number]
  );

  const bounds: L.LatLngBoundsExpression = [driverPos, clientPos];

  return (
    <div className="w-full h-full rounded-[2rem] overflow-hidden border-2 border-slate-200 dark:border-slate-800 shadow-inner">
      <MapContainer
        center={driverPos}
        zoom={15}
        scrollWheelZoom={interactive}
        dragging={interactive}
        className="w-full h-full z-10"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        {/* Marcador do Cliente */}
        <Marker position={clientPos} icon={icon} />

        {/* Marcador do Entregador */}
        <Marker position={driverPos} icon={driverIcon} />

        {/* Linha da Rota */}
        {polylinePositions && (
          <Polyline 
            positions={polylinePositions} 
            color="#ea580c" 
            weight={5} 
            opacity={0.7} 
            dashArray="10, 10"
          />
        )}

        <MapResizer bounds={bounds} />
      </MapContainer>
    </div>
  );
}
