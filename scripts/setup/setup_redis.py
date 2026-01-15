# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 15:40:00
import subprocess
import sys
import os
import time

def run_command(cmd):
    try:
        # Tenta executar o comando. No Windows, shell=True é necessário para comandos do sistema.
        return subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        return e
    except FileNotFoundError:
        return "NOT_FOUND"

def setup():
    print("📦 MesaFlow Redis Setup Tool - v1.2")
    print("====================================")

    # 1. Verificar se o comando docker existe no PATH
    print("\n[1/3] Verificando binario do Docker")
    version_check = run_command("docker --version")
    
    if version_check == "NOT_FOUND" or isinstance(version_check, subprocess.CalledProcessError):
        print("❌ ERRO: O comando 'docker' nao foi encontrado no seu terminal.")
        print("👉 Dica: Tente fechar este terminal e abrir um novo para atualizar o PATH.")
        print("Se o Docker Desktop acabou de ser instalado, o Windows precisa atualizar as variaveis de ambiente.")
        sys.exit(1)
    
    print(f"✅ Docker detectado: {version_check.stdout.strip()}")

    # 2. Subir o container do Redis
    print("\n[2/3] Iniciando container Redis")
    print("🚀 Executando: docker-compose up -d redis")
    
    # Tenta via docker-compose primeiro
    compose_res = run_command("docker-compose up -d redis")
    
    if isinstance(compose_res, subprocess.CalledProcessError):
        print("⚠️  Falha ao usar docker-compose. Tentando comando direto do Docker")
        # Fallback: Comando direto caso o docker-compose nao esteja no path ou falhe
        # --restart always garante que o redis suba junto com o Windows
        direct_cmd = "docker run -d --name mesaflow_redis -p 6379:6379 --restart always redis:alpine"
        run_command(direct_cmd)
    
    print("✅ Comando de inicializacao enviado.")

    # 3. Aguardar e Validar
    print("\n[3/3] Validando conexao na porta 6379")
    print("⏳ Aguardando 5 segundos para o boot do container")
    time.sleep(5)
    
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(3)
        if s.connect_ex(('127.0.0.1', 6379)) == 0:
            print("✨ SUCESSO: Redis esta online e aceitando conexoes!")
        else:
            print("❌ FALHA: O container nao responde na porta 6379.")
            print("👉 Verifique se outra aplicacao ja esta usando a porta 6379.")

    print("\n====================================")
    print("Dica: Se o erro persistir, rode manualmente no terminal:")
    print("docker run -d --name mesaflow_redis -p 6379:6379 redis:alpine")
    print("====================================")

if __name__ == "__main__":
    setup()
