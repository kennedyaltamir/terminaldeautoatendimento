/**
 * Author: MESAFLOW_AI
 * Version: 1.1.0 (Sovereign Constants)
 * DNA_ID: MF-CONST-DRIVER-V1
 */
export const DRIVER_CONSTANTS = {
  HAPTIC: {
    SUCCESS: [10],
    ERROR: [50, 50, 50],
    INCIDENT: [200, 100, 200, 100, 200],
    CLICK: [5]
  },
  THRESHOLDS: {
    BATTERY_LOW: 0.20,
    SPEED_LOCK: 15,
    HIGH_YIELD_KM: 3.0,
    GPS_ACCURACY: 50,
    BATCH_SEND_LIMIT: 5,
    BATCH_TIME_LIMIT: 3000
  },
  ZOOM_LEVELS: {
    SLOW: 18,
    MEDIUM: 15,
    FAST: 13
  },
  MOCK: {
    DISTANCE_KM: 3.5,
    STORE_COORDS: [-23.5505, -46.6333] as [number, number]
  }
};
