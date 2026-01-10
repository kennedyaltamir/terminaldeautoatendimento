import os
import sys

def fix_jest_config():
    print("🔧 Aplicando correção de Transformação do Jest (ESM Support)...")
    
    current_dir = os.getcwd()
    if os.path.basename(current_dir) == "mobile":
        mobile_dir = current_dir
    else:
        mobile_dir = os.path.join(current_dir, "mobile")

    if not os.path.exists(mobile_dir):
        print(f"❌ Diretório não encontrado: {mobile_dir}")
        sys.exit(1)

    config_path = os.path.join(mobile_dir, "jest.config.js")

    # Configuração otimizada para Expo 54 + RNTL 12
    # O segredo está no transformIgnorePatterns permitindo @testing-library
    new_config = """module.exports = {
  preset: 'jest-expo',
  setupFilesAfterEnv: ['./jest.setup.js'],
  transformIgnorePatterns: [
    'node_modules/(?!((jest-)?react-native|@react-native(-community)?)|expo(nent)?|@expo(nent)?/.*|@expo-google-fonts/.*|react-navigation|@react-navigation/.*|@unimodules/.*|unimodules|sentry-expo|native-base|react-native-svg|@testing-library)'
  ],
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
  // Garante que o Babel processe os arquivos corretamente
  transform: {
    '^.+\\\\.(js|jsx|ts|tsx)$': 'babel-jest',
  }
};
"""

    try:
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(new_config)
        print("✅ jest.config.js reescrito com padrões de transformação corretos.")
    except Exception as e:
        print(f"❌ Erro ao escrever arquivo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fix_jest_config()
