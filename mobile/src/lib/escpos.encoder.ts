/**
 * EscPosEncoder: Gerador de comandos binários ESC/POS para impressoras térmicas.
 * Implementação pura em TypeScript para máxima performance nativa.
 */

const ESC = 0x1B;
const GS = 0x1D;
const LF = 0x0A;

export class EscPosEncoder {
  private buffer: number[] = [];

  constructor() {
    this.add([ESC, 0x40]); // Initialize
  }

  private add(bytes: number | number[]) {
    if (Array.isArray(bytes)) {
      this.buffer.push(...bytes);
    } else {
      this.buffer.push(bytes);
    }
  }

  private addString(str: string) {
    // Normalização: Remove acentos para evitar caracteres corrompidos na impressora
    const cleanStr = str.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    for (let i = 0; i < cleanStr.length; i++) {
      const code = cleanStr.charCodeAt(i);
      // Aceita apenas ASCII imprimível ou Line Feed
      if ((code >= 32 && code <= 126) || code === LF) {
        this.buffer.push(code);
      } else {
        this.buffer.push(0x3F); // '?' para caracteres desconhecidos
      }
    }
  }

  public text(str: string): this {
    this.addString(str);
    return this;
  }

  public line(str: string = ""): this {
    this.addString(str + "\n");
    return this;
  }

  public feed(lines: number = 1): this {
    for (let i = 0; i < lines; i++) {
      this.add(LF);
    }
    return this;
  }

  public align(mode: 'LEFT' | 'CENTER' | 'RIGHT'): this {
    const map = { 'LEFT': 0, 'CENTER': 1, 'RIGHT': 2 };
    this.add([ESC, 0x61, map[mode]]);
    return this;
  }

  public bold(enabled: boolean): this {
    this.add([ESC, 0x45, enabled ? 1 : 0]);
    return this;
  }

  public size(mode: 'NORMAL' | 'LARGE'): this {
    this.add([GS, 0x21, mode === 'LARGE' ? 0x11 : 0x00]);
    return this;
  }

  public cut(): this {
    this.add([LF, LF, LF, GS, 0x56, 0x42, 0x00]);
    return this;
  }

  public getBuffer(): Uint8Array {
    return new Uint8Array(this.buffer);
  }
}
