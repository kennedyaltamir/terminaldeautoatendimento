export const ESC = "\x1B";
export const GS = "\x1D";
export const LF = "\x0A";

export const COMMANDS = {
  INIT: ESC + "@",                    // Inicializa a impressora
  CUT: GS + "V" + "\x41" + "\x00",    // Corta o papel (Full Cut)
  
  // Formatação de Texto
  TXT_NORMAL: ESC + "!" + "\x00",     // Fonte Normal
  TXT_BOLD_ON: ESC + "E" + "\x01",    // Negrito Ligado
  TXT_BOLD_OFF: ESC + "E" + "\x00",   // Negrito Desligado
  TXT_2HEIGHT: GS + "!" + "\x10",     // Altura Dupla
  TXT_2WIDTH: GS + "!" + "\x20",      // Largura Dupla
  TXT_QUAD: GS + "!" + "\x11",        // Quádruplo (Altura + Largura)
  
  // Alinhamento
  ALIGN_LEFT: ESC + "a" + "\x00",
  ALIGN_CENTER: ESC + "a" + "\x01",
  ALIGN_RIGHT: ESC + "a" + "\x02",
};