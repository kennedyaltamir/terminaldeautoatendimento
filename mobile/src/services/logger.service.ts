/**
 * LoggerService: Centralizador de observabilidade do App Mobile.
 * Padronizado para emitir logs estruturados com tag [MesaFlow] para captura via ADB.
 */

type LogLevel = 'DEBUG' | 'INFO' | 'WARN' | 'ERROR';

class LoggerService {
  private static instance: LoggerService;
  private isDev = __DEV__;

  private constructor() {}

  public static getInstance(): LoggerService {
    if (!LoggerService.instance) {
      LoggerService.instance = new LoggerService();
    }
    return LoggerService.instance;
  }

  private formatMessage(level: LogLevel, context: string, message: string): string {
    const timestamp = new Date().toISOString();
    // Prefixo [MesaFlow] é CRÍTICO para o script de diagnóstico Python
    return `[MesaFlow] [${timestamp}] [${level}] [${context}] ${message}`;
  }

  public debug(context: string, message: string, data?: any) {
    if (this.isDev) {
      console.log(this.formatMessage('DEBUG', context, message), data ? JSON.stringify(data) : '');
    }
  }

  public info(context: string, message: string, data?: any) {
    console.log(this.formatMessage('INFO', context, message), data ? JSON.stringify(data) : '');
  }

  public warn(context: string, message: string, data?: any) {
    console.warn(this.formatMessage('WARN', context, message), data ? JSON.stringify(data) : '');
  }

  public error(context: string, message: string, error?: any) {
    console.error(this.formatMessage('ERROR', context, message), error || '');
  }
}

export const logger = LoggerService.getInstance();
