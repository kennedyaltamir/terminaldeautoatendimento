// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 13:40:00
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
  html: `<div style="background-color: #ea580c; width: 40px; height: 40px; border-radius: 50%; border: 3px solid white; display: flex; align-items: center; justify-content: center; font-size: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">🛵</div>`,
  iconSize: [40, 40],
  iconAnchor: [20, 40],
});

function MapResizer({ bounds }: { bounds: L.LatLngBoundsExpression }) {
  const map = useMap();
  useEffect(() => {
    if (bounds) {
      map.fitBounds(bounds, { padding: [50, 50], maxZoom: 16 });
    }
  }, [bounds, map]);
  return null;
}

interface TrackingMapProps {
  driverPos: [number, number];
  clientPos: [number, number];
  routeGeojson?: any;
  duration?: number; // em segundos
}

export default function TrackingMap({ driverPos, clientPos, routeGeojson, duration }: TrackingMapProps) {
  const polylinePositions = routeGeojson?.coordinates.map(
    ([lng, lat]: [number, number]) => [lat, lng] as [number, number]
  );

  const etaMinutes = duration ? Math.ceil(duration / 60) : null;

  return (
    <div className="relative w-full h-full rounded-[2.5rem] overflow-hidden border-4 border-white shadow-2xl">
      {etaMinutes && (
        <div className="absolute top-4 left-1/2 -translate-x-1/2 z-[1000] bg-orange-600 text-white px-4 py-2 rounded-full font-black text-xs uppercase tracking-widest shadow-lg animate-bounce">
          Chega em {etaMinutes} min
        </div>
      )}
      
      <MapContainer
        center={driverPos}
        zoom={15}
        className="w-full h-full"
        zoomControl={false}
      >
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <Marker position={clientPos} icon={icon} />
        <Marker position={driverPos} icon={driverIcon} />
        {polylinePositions && (
          <Polyline positions={polylinePositions} color="#ea580c" weight={6} opacity={0.6} dashArray="10, 15" />
        )}
        <MapResizer bounds={[driverPos, clientPos]} />
      </MapContainer>
    </div>
  );
}
