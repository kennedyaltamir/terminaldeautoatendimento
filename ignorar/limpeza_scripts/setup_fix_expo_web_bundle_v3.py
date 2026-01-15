import os
import subprocess
import sys
import json
import shutil

def log(msg, status="INFO"):
    colors = {"INFO": "\033[94m", "SUCCESS": "\033[92m", "ERROR": "\033[91m", "END": "\033[0m"}
    print(f"{colors.get(status, '')}[{status}] {msg}{colors['END']}")

def run_command(cmd, cwd=None):
    try:
        log(f"Executando: {' '.join(cmd)}")
        subprocess.check_call(cmd, cwd=cwd, shell=True)
        return True
    except subprocess.CalledProcessError as e:
        log(f"Erro ao executar comando: {e}", "ERROR")
        return False

def main():
    log("🚀 REPARO V3.0: Solução Definitiva ESM/Web", "INFO")

    if os.path.basename(os.getcwd()) != "mobile":
        if os.path.exists("mobile"):
            os.chdir("mobile")
        else:
            log("Erro: Execute na raiz ou dentro de 'mobile/'", "ERROR")
            sys.exit(1)

    # 1. Instalar dependências de transformação de módulos
    log("Instalando transformadores de módulos...")
    run_command([
        "npm", "install", 
        "babel-plugin-transform-import-meta", 
        "@babel/plugin-transform-modules-commonjs",
        "--save-dev", "--legacy-peer-deps"
    ])

    # 2. metro.config.js (FORÇANDO TRANSPILAÇÃO DE ESM)
    metro_content = """const { getDefaultConfig } = require('expo/metro-config');
const config = getDefaultConfig(__dirname);

// Alias para evitar conflitos nativos
config.resolver.alias = {
  'lucide-react-native': 'lucide-react',
};

// Força o Metro a processar bibliotecas ESM problemáticas
config.transformer.getTransformOptions = async () => ({
  transform: {
    experimentalImportSupport: false,
    inlineRequires: true,
  },
});

module.exports = config;"""
    
    with open("metro.config.js", "w", encoding="utf-8") as f:
        f.write(metro_content)
    log("metro.config.js atualizado (Transpiler rules).", "SUCCESS")

    # 3. babel.config.js (FORÇANDO COMMONJS)
    babel_content = """module.exports = function(api) {
  api.cache(true);
  return {
    presets: ['babel-preset-expo'],
    plugins: [
      'babel-plugin-transform-import-meta',
      '@babel/plugin-transform-modules-commonjs' // <--- REMÉDIO DEFINITIVO
    ],
  };
};"""
    with open("babel.config.js", "w", encoding="utf-8") as f:
        f.write(babel_content)
    log("babel.config.js atualizado com CommonJS Transform.", "SUCCESS")

    # 4. Limpeza de Cache
    log("Limpando cache físico...")
    if os.path.exists(".expo"):
        shutil.rmtree(".expo")
    
    log("Iniciando Expo Web...", "INFO")
    run_command(["npx", "expo", "start", "--web", "--clear"])

if __name__ == "__main__":
    main()
