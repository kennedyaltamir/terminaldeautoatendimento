import os
import shutil
import re
import sys
import time

# Configuração
INPUT_FILE = "resposta.txt"
BACKUP_DIR = "Copy"

def create_backup(file_path):
    """
    Cria um backup versionado do arquivo na pasta Copy.
    Ex: app/main.py -> Copy/app/main.py (se existir, main_v2.py, main_v3.py...)
    """
    # Define o caminho de destino no backup
    backup_path = os.path.join(BACKUP_DIR, file_path)
    backup_folder = os.path.dirname(backup_path)

    # Cria a pasta de backup se não existir
    os.makedirs(backup_folder, exist_ok=True)

    # Se o arquivo original não existe, não há o que backupear, mas a pasta foi criada
    if not os.path.exists(file_path):
        return

    # Lógica de versionamento
    final_backup_path = backup_path
    version = 1
    
    root, ext = os.path.splitext(backup_path)
    
    while os.path.exists(final_backup_path):
        version += 1
        final_backup_path = f"{root}_v{version}{ext}"

    shutil.copy2(file_path, final_backup_path)
    print(f"📦 Backup criado: {final_backup_path}")

def process_updates():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Arquivo '{INPUT_FILE}' não encontrado. Cole a resposta da IA nele.")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex aprimorado:
    # Captura linhas que começam com #caminho/arquivo.ext
    # O conteúdo vai até o próximo #caminho ou fim do arquivo
    # Ignora blocos de código markdown (```) no início e fim do conteúdo capturado
    pattern = re.compile(r"^#([a-zA-Z0-9_\-\./\\]+)\s*\n(.*?)(?=\n#|\Z)", re.MULTILINE | re.DOTALL)
    
    matches = pattern.findall(content)

    if not matches:
        print("⚠️ Nenhum arquivo encontrado no formato '#caminho/arquivo'. Verifique o 'resposta.txt'.")
        return

    print(f"🔍 Encontrados {len(matches)} arquivos para atualizar.\n")

    for file_path, file_content in matches:
        file_path = file_path.strip()
        
        # Limpeza de artefatos de Markdown (```python, ```tsx, ```)
        # Remove primeira linha se for ```algo
        file_content = re.sub(r"^```[a-zA-Z0-9]*\n", "", file_content)
        # Remove última linha se for ```
        file_content = re.sub(r"\n```\s*$", "", file_content)
        
        # Garante que o diretório do arquivo original existe
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # 1. Cria Backup
        create_backup(file_path)

        # 2. Escreve o novo conteúdo
        try:
            with open(file_path, "w", encoding="utf-8", newline='\n') as f:
                f.write(file_content.strip() + "\n") # Garante uma quebra de linha no final
            print(f"✅ Atualizado: {file_path}")
        except Exception as e:
            print(f"❌ Erro ao escrever {file_path}: {e}")

    print("\n🚀 Processo concluído com sucesso!")

if __name__ == "__main__":
    # Garante que a pasta Copy existe
    os.makedirs(BACKUP_DIR, exist_ok=True)
    process_updates()