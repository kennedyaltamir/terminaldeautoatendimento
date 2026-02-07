/**
 * Utilitários de Tempo e SLA do Ecossistema MesaFlow.
 */

/**
 * Calcula o tempo decorrido em minutos a partir de uma ISO string.
 * @param dateString Data de criação no formato ISO
 * @returns String formatada (ex: "15 min")
 */
export const calculateElapsedMinutes = (dateString: string): string => {
  const start = new Date(dateString).getTime();
  const now = new Date().getTime();
  const minutes = Math.floor((now - start) / 60000);
  return `${minutes} min`;
};
