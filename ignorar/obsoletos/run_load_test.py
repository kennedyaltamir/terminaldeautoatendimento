import os
import sys
import subprocess
import time

def run_locust():
    print("🚀 Iniciando Teste de Carga Automatizado (Locust)...")
    
    # Verifica se locust está instalado
    try:
        import locust
    except ImportError:
        print("❌ Locust não instalado. Execute: pip install locust")
        sys.exit(1)

    # Configuração do Teste
    # Headless mode: sem interface web, apenas terminal
    # -u 10: 10 usuários simultâneos
    # -r 2: 2 usuários novos por segundo (Ramp up)
    # -t 10s: Duração de 10 segundos (Smoke Test rápido)
    # --host: Alvo
    
    target_host = "http://localhost:8000"
    locust_file = "scripts/performance/locustfile.py"
    
    cmd = [
        "locust",
        "-f", locust_file,
        "--headless",
        "-u", "10",
        "-r", "2",
        "-t", "10s",
        "--host", target_host,
        "--only-summary" # Reduz ruído no log
    ]
    
    print(f"   Alvo: {target_host}")
    print(f"   Cenário: {locust_file}")
    print("   Executando...")
    
    try:
        # Executa e captura saída
        result = subprocess.run(cmd, check=False)
        
        if result.returncode == 0:
            print("\n✅ Load Test Finished: OK")
            print("   Verifique as estatísticas acima para latência e RPS.")
        else:
            print("\n⚠️  Load Test terminou com código diferente de 0 (pode ser falha de assert ou interrupção).")
            
    except KeyboardInterrupt:
        print("\n🛑 Teste interrompido pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro ao executar Locust: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Verifica se o servidor está rodando antes
    import requests
    try:
        requests.get("http://localhost:8000/health", timeout=1)
    except:
        print("❌ Servidor alvo (localhost:8000) parece offline.")
        print("   Inicie o backend com 'python run.py' em outro terminal.")
        sys.exit(1)

    run_locust()
