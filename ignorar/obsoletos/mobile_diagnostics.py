# DOMAIN: DEVOPS_SCRIPTS
import subprocess
import sys
import re
import time
import os
import shutil

# Configuração de Fallback (Último recurso)
HARDCODED_PATH = r"C:\Users\Kennedy Oliveira\AppData\Local\Android\Sdk\platform-tools\adb.exe"

def find_adb():
    """
    Localiza o binário ADB com estratégia de prioridade:
    1. PATH do sistema (shutil.which)
    2. Variável ANDROID_HOME
    3. Caminho Hardcoded (Ambiente Kennedy)
    """
    # 1. Tenta no PATH
    if shutil.which("adb"):
        return "adb"
    
    # 2. Tenta via ANDROID_HOME
    android_home = os.environ.get("ANDROID_HOME")
    if android_home:
        adb_env = os.path.join(android_home, "platform-tools", "adb.exe" if os.name == 'nt' else "adb")
        if os.path.exists(adb_env):
            return adb_env

    # 3. Fallback Hardcoded
    if os.path.exists(HARDCODED_PATH):
        return HARDCODED_PATH
        
    return None

class LogMonitor:
    def __init__(self):
        self.running = True
        self.adb_bin = find_adb()

    def start(self):
        if not self.adb_bin:
            print("❌ ADB não encontrado no PATH, ANDROID_HOME ou caminho padrão.")
            print("   Instale o Android SDK Platform-Tools.")
            return

        print(f"🔧 Usando ADB em: {self.adb_bin}")
        print(f"🚀 [MesaFlow] Iniciando ponte de telemetria via ADB...")
        
        # Limpa o buffer do logcat antes de começar
        subprocess.run(f'"{self.adb_bin}" logcat -c', shell=True)

        # Inicia o processo de leitura
        # CORREÇÃO: Removemos o filtro 'ReactNativeJS:V' para evitar perda de logs em Release/Expo Updates.
        # Usamos *:V para capturar tudo e filtramos no Python pela tag [MesaFlow].
        cmd = f'"{self.adb_bin}" logcat -v time *:V'
        
        self.process = subprocess.Popen(
            cmd, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            encoding='utf-8',
            errors='replace'
        )

        print("📡 Monitorando logs [MesaFlow] via ADB...")
        print("   (Abra o App no emulador para ver os eventos. Ctrl+C para sair)")

        try:
            while self.running:
                line = self.process.stdout.readline()
                if not line:
                    break
                
                # Filtra apenas logs estruturados do MesaFlow (Contrato Arquitetural)
                if "[MesaFlow]" in line:
                    self.parse_log(line.strip())
        except KeyboardInterrupt:
            self.stop()
        finally:
            self.stop()

    def parse_log(self, line):
        # Exemplo de linha real do LoggerService: 
        # 01-07 20:30:00.123 I/ReactNativeJS(1234): [MesaFlow] [2026-01-07T...] [INFO] [AuthStore] Login bem sucedido
        
        # Regex Ajustado (Opção A):
        # 1. Ignora o prefixo do Logcat (Data/Hora/PID)
        # 2. Encontra a tag [MesaFlow]
        # 3. Ignora o timestamp interno do Logger (.*? entre colchetes)
        # 4. Captura LEVEL, Contexto e Mensagem
        match = re.search(r'\[MesaFlow\].*?\[(DEBUG|INFO|WARN|ERROR)\]\s+\[(.*?)\]\s+(.*)', line)
        
        if match:
            level, context, message = match.groups()
            
            # Formatação colorida para o terminal
            color = "\033[0m"
            if level == "INFO": color = "\033[94m" # Blue
            if level == "WARN": color = "\033[93m" # Yellow
            if level == "ERROR": color = "\033[91m" # Red

            print(f"{color}[{level}] {context}: {message}\033[0m")
        else:
            # Fallback para logs mal formatados mas que contêm a tag
            # Remove o timestamp do logcat para limpar a saída
            clean_line = re.sub(r'^\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3}\s\w\/.*?\):\s', '', line)
            print(f"📝 {clean_line}")

    def stop(self):
        self.running = False
        if hasattr(self, 'process'):
            self.process.terminate()
        print("\n🛑 Monitoramento encerrado.")

if __name__ == "__main__":
    monitor = LogMonitor()
    monitor.start()
    