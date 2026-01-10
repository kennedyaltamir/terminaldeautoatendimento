import os
import sys

def fix_jest_config():
    print("🔧 Aplicando correção FINAL do Jest (Simplificação de Config)...")
    
    current_dir = os.getcwd()
    if os.path.basename(current_dir) == "mobile":
        mobile_dir = current_dir
    else:
        mobile_dir = os.path.join(current_dir, "mobile")

    if not os.path.exists(mobile_dir):
        print(f"❌ Diretório não encontrado: {mobile_dir}")
        sys.exit(1)

    config_path = os.path.join(mobile_dir, "jest.config.js")

    # Configuração Limpa:
    # 1. Removemos a chave 'transform' manual para deixar o 'jest-expo' gerenciar o Babel.
    # 2. Mantemos o transformIgnorePatterns robusto para incluir @testing-library.
    new_config = """module.exports = {
  preset: 'jest-expo',
  setupFilesAfterEnv: ['./jest.setup.js'],
  transformIgnorePatterns: [
    'node_modules/(?!((jest-)?react-native|@react-native(-community)?)|expo(nent)?|@expo(nent)?/.*|@expo-google-fonts/.*|react-navigation|@react-navigation/.*|@unimodules/.*|unimodules|sentry-expo|native-base|react-native-svg|@testing-library)'
  ],
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node']
};
"""

    try:
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(new_config)
        print("✅ jest.config.js simplificado e corrigido.")
    except Exception as e:
        print(f"❌ Erro ao escrever arquivo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fix_jest_config()
