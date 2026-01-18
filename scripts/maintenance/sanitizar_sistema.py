import os
import shutil
import json

def sanitizar():
    print("🧬 MesaFlow OS - Iniciando Sanitização de Scripts (Inconsistência #3)")
    
    # 1. Definir caminhos
    base_dir = os.getcwd()
    archive_dir = os.path.join(base_dir, "archive", "legacy_scripts")
    
    # Criar diretório de arquivo se não existir
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
        print(f"📁 Criado diretório de quarentena: {archive_dir}")

    # 2. Mapeamento de Depreciação (Origem -> Destino)
    # Movemos versões obsoletas para o arquivo
    depreciados = [
        "scripts/03_normal_roteamento.py",
        "scripts/test_kiosk_lock_flow.py",
        "gerartxt.py" # Movendo da raiz para manutenção
    ]

    for script in depreciados:
        src = os.path.join(base_dir, script)
        if os.path.exists(src):
            dest = os.path.join(archive_dir, os.path.basename(script))
            shutil.move(src, dest)
            print(f"✅ Movido para legacy: {script}")
        else:
            print(f"ℹ️  Script já removido ou inexistente: {script}")

    # 3. Padronização de Autoridade Canônica
    # v2 vira o padrão oficial
    kiosk_v2 = os.path.join(base_dir, "scripts/test_kiosk_lock_flow_v2.py")
    kiosk_final = os.path.join(base_dir, "scripts/99_kiosk_lock_canonic.py")
    
    if os.path.exists(kiosk_v2):
        os.rename(kiosk_v2, kiosk_final)
        print(f"⭐ Autoridade Canônica Estabelecida: 99_kiosk_lock_canonic.py")

    print("\n✨ Sanitização concluída. Execute 'python atualizar.py' para re-indexar o sistema.")

if __name__ == "__main__":
    sanitizar()

