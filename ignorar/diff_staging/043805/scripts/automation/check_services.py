import socket
import sys

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        return s.connect_ex(('127.0.0.1', port)) == 0

def main():
    print("🔍 Verificando integridade dos serviços...")
    backend = check_port(8000)
    frontend = check_port(3000)
    
    print(f"   Backend (8000): {'✅ ONLINE' if backend else '❌ OFFLINE'}")
    print(f"   Frontend (3000): {'✅ ONLINE' if frontend else '❌ OFFLINE'}")
    
    if not backend or not frontend:
        print("\n🚨 ERRO: Certifique-se de que 'python run.py' está rodando em outro terminal.")
        sys.exit(1)
    
    print("\n🚀 Tudo pronto para a simulação.")
    sys.exit(0)

if __name__ == "__main__":
    main()
