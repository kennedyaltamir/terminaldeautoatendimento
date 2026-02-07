/**
 * Author: MESAFLOW_AI_SOVEREIGN
 * Version: 4.3.0 (Diamond Routing Master)
 * DNA_ID: MF-LIB-ROUTING-V4-3
 * OBJETIVO: Engine de Roteamento e Geometria Esférica.
 */

export interface RouteData {
  geometry: any;
  duration: number;
  distance: number;
}

/**
 * Busca rota via Backend Proxy (Google Maps) com Fallback OSRM.
 */
export async function fetchRoute(
  start: [number, number],
  end: [number, number]
): Promise<RouteData | null> {
  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001/api";
  try {
    const res = await fetch(`${API_URL}/mobile/logistics/route?origin=${start[0]},${start[1]}&dest=${end[0]},${end[1]}`, {
        headers: { 
            "Authorization": `Bearer ${localStorage.getItem('mesaflow_access_token')}`,
            "Content-Type": "application/json"
        }
    });
    
    if (!res.ok) throw new Error("API Route Error");
    return await res.json();
  } catch (error) {
    console.warn("🛡️ Fallback: OSRM Engine...");
    const url = `https://router.project-osrm.org/route/v1/driving/${start[1]},${start[0]};${end[1]},${end[0]}?overview=full&geometries=geojson`;
    const res = await fetch(url);
    const data = await res.json();
    if (!data.routes?.[0]) return null;
    return {
      geometry: data.routes[0].geometry,
      duration: data.routes[0].duration,
      distance: data.routes[0].distance
    };
  }
}

/**
 * 🛡️ RESTORAÇÃO: Cálculo de Distância (Haversine Formula)
 * Necessário para o componente EnRouteView exibir telemetria.
 */
export function calculateHaversineDistance(coords1: [number, number], coords2: [number, number]): number {
  const toRad = (x: number) => (x * Math.PI) / 180;
  const R = 6371e3; // Raio da Terra em metros
  const dLat = toRad(coords2[0] - coords1[0]);
  const dLon = toRad(coords2[1] - coords1[1]);
  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(toRad(coords1[0])) * Math.cos(toRad(coords2[0])) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}