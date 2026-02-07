import { EscPosEncoder } from '../escpos.encoder';

/**
 * Teste de Unidade: Protocolo de Hardware.
 * Garante que a tradução de comandos para binário segue o padrão ESC/POS.
 */
describe('EscPosEncoder', () => {
  it('deve gerar o buffer de inicialização correto', () => {
    const encoder = new EscPosEncoder();
    const buffer = encoder.getBuffer();
    
    // ESC @ (0x1B 0x40)
    expect(buffer[0]).toBe(0x1B);
    expect(buffer[1]).toBe(0x40);
  });

  it('deve converter texto para ASCII e adicionar Line Feed', () => {
    const encoder = new EscPosEncoder();
    encoder.line('MesaFlow');
    const buffer = encoder.getBuffer();
    
    // 'M' = 77, 'e' = 101, ..., LF = 10
    expect(buffer[2]).toBe(77); 
    expect(buffer[buffer.length - 1]).toBe(10);
  });

  it('deve remover acentos para compatibilidade com impressoras térmicas', () => {
    const encoder = new EscPosEncoder();
    encoder.text('Café');
    const buffer = encoder.getBuffer();
    
    // 'é' deve virar 'e' (101)
    expect(buffer[buffer.length - 1]).toBe(101);
  });
});
