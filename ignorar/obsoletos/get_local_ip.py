# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-10 01:50:00
import socket

def get_ip():
    print("🔍 Detectando IP da rede local para conexao mobile")
    try:
        # Cria uma conexao temporaria para identificar a interface de rede ativa
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        
        print(f"\n✅ Seu IP Local e: {ip}")
        print(f"🔗 No emulador, use: http://{ip}:8000/api")
        print("-" * 40)
        print("Dica: Se o emulador nao conectar, verifique se o seu")
        print("Firewall do Windows permite conexoes na porta 8000.")
        return ip
    except Exception as e:
        print(f"❌ Nao foi possivel detectar o IP: {e}")
        return "127.0.0.1"

if __name__ == "__main__":
    get_ip()
