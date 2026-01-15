// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 13:30:00

export interface RouteGeometry {
  type: "LineString";
  coordinates: [number, number][];
}

export interface RouteData {
  geometry: RouteGeometry;
  duration: number; // em segundos
  distance: number; // em metros
}

/**
 * Busca a geometria e metadados da rota (OSRM)
 */
export async function fetchRoute(
  start: [number, number],
  end: [number, number]
): Promise<RouteData | null> {
  try {
    const url = `https://router.project-osrm.org/route/v1/driving/${start[1]},${start[0]};${end[1]},${end[0]}?overview=full&geometries=geojson`;
    const res = await fetch(url);
    if (!res.ok) return null;
    const data = await res.json();
    if (!data.routes || data.routes.length === 0) return null;
    
    return {
      geometry: data.routes[0].geometry,
      duration: data.routes[0].duration,
      distance: data.routes[0].distance
    };
  } catch (error) {
    console.error("Erro ao buscar rota OSRM:", error);
    return null;
  }
}

