export const ESC = 0x1B;
export const GS = 0x1D;
export const LF = 0x0A;

export const COMMANDS = {
  INIT: [ESC, 0x40],                    // Inicializa a impressora
  CUT: [GS, 0x56, 0x41, 0x00],          // Corta o papel (Full Cut)
  
  // Gaveta de Dinheiro (Cash Drawer)
  // ESC p m t1 t2 (m=0: pino 2, t1=25*2ms, t2=250*2ms)
  OPEN_DRAWER: [ESC, 0x70, 0x00, 0x19, 0xFA], 

  // Formatação de Texto
  TXT_NORMAL: [ESC, 0x21, 0x00],        // Fonte Normal
  TXT_BOLD_ON: [ESC, 0x45, 0x01],       // Negrito Ligado
  TXT_BOLD_OFF: [ESC, 0x45, 0x00],      // Negrito Desligado

  // Tamanhos (GS ! n)
  TXT_SIZE: {
    NORMAL: [GS, 0x21, 0x00],
    DOUBLE_HEIGHT: [GS, 0x21, 0x10],
    DOUBLE_WIDTH: [GS, 0x21, 0x01],
    QUAD: [GS, 0x21, 0x11],
  },

  // Alinhamento
  ALIGN: {
    LEFT: [ESC, 0x61, 0x00],
    CENTER: [ESC, 0x61, 0x01],
    RIGHT: [ESC, 0x61, 0x02],
  },

  // QR Code (Model 2)
  QR: {
    MODEL: [GS, 0x28, 0x6B, 0x04, 0x00, 0x31, 0x41, 0x32, 0x00], // Set Model 2
    SIZE: [GS, 0x28, 0x6B, 0x03, 0x00, 0x31, 0x43, 0x06],        // Size 6
    ERROR: [GS, 0x28, 0x6B, 0x03, 0x00, 0x31, 0x45, 0x31],       // Error Correction Level L
    STORE: [GS, 0x28, 0x6B],                                     // Store Data (Header parcial)
    PRINT: [GS, 0x28, 0x6B, 0x03, 0x00, 0x31, 0x51, 0x30],       // Print Symbol
  }
};
