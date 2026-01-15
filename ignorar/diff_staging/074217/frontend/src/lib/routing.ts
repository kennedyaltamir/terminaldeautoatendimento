// DOMAIN: FRONTEND
// LAST_MODIFIED: 2026-01-15 12:45:00

/**
 * Interface para retorno do OSRM
 */
export interface RouteGeometry {
  type: "LineString";
  coordinates: [number, number][]; // [longitude, latitude]
}

/**
 * Busca a geometria da rota via OSRM (Open Source Routing Machine)
 */
export async function fetchRoute(
  start: [number, number],
  end: [number, number]
): Promise<RouteGeometry | null> {
  try {
    const url = `https://router.project-osrm.org/route/v1/driving/${start[1]},${start[0]};${end[1]},${end[0]}?overview=full&geometries=geojson`;
    const res = await fetch(url);
    if (!res.ok) return null;
    const data = await res.json();
    if (!data.routes || data.routes.length === 0) return null;
    return data.routes[0].geometry;
  } catch (error) {
    console.error("Erro ao buscar rota OSRM:", error);
    return null;
  }
}
