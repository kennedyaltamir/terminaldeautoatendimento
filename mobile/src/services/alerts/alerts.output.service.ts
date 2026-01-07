import { Vibration } from 'react-native';
import { SLAStatus } from '../orders.sla.service';

/**
 * AlertsOutputService: Responsável pelos efeitos físicos (Side-effects).
 * Única camada que pode importar APIs do React Native / Expo.
 */
export const AlertsOutputService = {
  /**
   * Executa sinal sensorial baseado na gravidade.
   */
  trigger(status: SLAStatus) {
    console.log(`[AlertOutput] Disparando sinal sensorial para: ${status}`);

    if (status === 'CRITICAL') {
      // Vibração curta e única
      Vibration.vibrate(400);
    } 

    if (status === 'BREACHED') {
      // Vibração dupla e intensa
      Vibration.vibrate([0, 500, 200, 500]);
    }

    // Nota: Em missões futuras, aqui será injetado o áudio via expo-av
  }
};
