
import os
import sys
import subprocess

def fix_jest_esm():
    print("🚑 Aplicando correção definitiva para ESM no Jest (React Native 0.76+)...")
    
    current_dir = os.getcwd()
    if os.path.basename(current_dir) == "mobile":
        mobile_dir = current_dir
    else:
        mobile_dir = os.path.join(current_dir, "mobile")

    if not os.path.exists(mobile_dir):
        print(f"❌ Diretório não encontrado: {mobile_dir}")
        sys.exit(1)

    config_path = os.path.join(mobile_dir, "jest.config.js")

    # Configuração Robusta para ESM
    # 1. transform: Força o uso do babel-jest para arquivos JS/TS
    # 2. transformIgnorePatterns: A lista negativa. Tudo aqui SERÁ ignorado pelo Babel.
    #    O segredo é o (?!...) que cria uma exceção à regra de ignorar.
    #    Adicionamos @react-native, @testing-library e outras libs modernas.
    new_config = """module.exports = {
  preset: 'jest-expo',
  setupFilesAfterEnv: ['./jest.setup.js'],
  transform: {
    '^.+\\\\.(js|jsx|ts|tsx)$': 'babel-jest',
  },
  transformIgnorePatterns: [
    'node_modules/(?!((jest-)?react-native|@react-native(-community)?)|expo(nent)?|@expo(nent)?/.*|@expo-google-fonts/.*|react-navigation|@react-navigation/.*|@unimodules/.*|unimodules|sentry-expo|native-base|react-native-svg|@testing-library|@react-native/virtualized-lists)'
  ],
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
  testEnvironment: 'node'
};
"""

    try:
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(new_config)
        print("✅ jest.config.js atualizado com suporte a ESM.")
        
        # Limpeza de Cache do Jest é obrigatória após mudar transform
        print("🧹 Limpando cache do Jest...")
        subprocess.run("npx jest --clearCache", cwd=mobile_dir, shell=True, check=False)
        
    except Exception as e:
        print(f"❌ Erro ao aplicar correção: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fix_jest_esm()