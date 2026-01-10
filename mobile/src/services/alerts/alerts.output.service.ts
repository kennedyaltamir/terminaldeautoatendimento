import { Vibration } from 'react-native';
import { SLAStatus } from '../orders.sla.service';
import { useSettingsStore } from '../../store/settings.store';
import { logger } from '../logger.service';

const TAG = 'AlertsOutput';

/**
 * AlertsOutputService: Responsável pelos efeitos físicos (Side-effects).
 * Atualizado na Task 023 para respeitar o Modo Silencioso.
 */
export const AlertsOutputService = {
  /**
   * Executa sinal sensorial baseado na gravidade, se permitido.
   */
  trigger(status: SLAStatus) {
    // Consulta a store de configurações (Síncrono)
    const isSilent = useSettingsStore.getState().isSilentMode;

    if (isSilent) {
      logger.debug(TAG, `Alerta suprimido (Modo Silencioso): ${status}`);
      return;
    }

    logger.info(TAG, `Disparando alerta físico: ${status}`);

    if (status === 'CRITICAL') {
      // Vibração curta e única
      Vibration.vibrate(400);
    } 

    if (status === 'BREACHED') {
      // Vibração dupla e intensa (Padrão SOS simplificado)
      Vibration.vibrate([0, 500, 200, 500]);
    }
  }
};
