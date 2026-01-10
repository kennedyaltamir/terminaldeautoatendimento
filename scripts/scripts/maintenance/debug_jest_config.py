import os
import sys

def debug_jest():
    print("🔧 Aplicando configuração de Debug para Jest (Transform All)...")
    
    current_dir = os.getcwd()
    if os.path.basename(current_dir) == "mobile":
        mobile_dir = current_dir
    else:
        mobile_dir = os.path.join(current_dir, "mobile")

    if not os.path.exists(mobile_dir):
        print(f"❌ Diretório não encontrado: {mobile_dir}")
        sys.exit(1)

    config_path = os.path.join(mobile_dir, "jest.config.js")

    # Configuração "Nuclear":
    # 1. transformIgnorePatterns vazio -> Transforma TUDO em node_modules (Lento, mas infalível para erros de ESM)
    # 2. Mantém o preset jest-expo
    # 3. Remove overrides de ambiente
    new_config = """module.exports = {
  preset: 'jest-expo',
  setupFilesAfterEnv: ['./jest.setup.js'],
  // Habilita transformação para TODOS os arquivos em node_modules
  // Isso é um teste de diagnóstico para confirmar se o erro é falta de transpilação
  transformIgnorePatterns: [],
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node']
};
"""

    try:
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(new_config)
        print("✅ jest.config.js atualizado para modo DEBUG (Transform All).")
        
        # Limpa cache para garantir que a nova config pegue
        import subprocess
        print("🧹 Limpando cache do Jest...")
        subprocess.run("npx jest --clearCache", cwd=mobile_dir, shell=True, check=False)
        
    except Exception as e:
        print(f"❌ Erro ao escrever arquivo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    debug_jest()
