
import { useEffect } from "react";
import { ENV } from "../config/env";
import { ScreenName } from "../navigation/screenRegistry";

/**
 * Hook de Telemetria Visual L5.
 * Garante que a montagem da tela seja registrada nos logs do Metro/ADB.
 */
export function useScreenLog(screenName: ScreenName) {
  useEffect(() => {
    if (ENV.ENABLE_LOGS) {
      console.log(`[SCREEN_MOUNT] ${screenName}`);
    }
    
    return () => {
      if (ENV.ENABLE_LOGS) {
        console.log(`[SCREEN_UNMOUNT] ${screenName}`);
      }
    };
  }, [screenName]);
}

