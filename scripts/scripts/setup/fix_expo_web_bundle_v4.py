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
    log("☢️  REPARO NUCLEAR V4.0: Forçando Transpilação de node_modules", "INFO")

    if os.path.basename(os.getcwd()) != "mobile":
        if os.path.exists("mobile"):
            os.chdir("mobile")
        else:
            log("Erro: Execute na raiz ou dentro de 'mobile/'", "ERROR")
            sys.exit(1)

    # 1. Instalar a lista exata de plugins de resiliência
    log("Instalando infraestrutura de compatibilidade...")
    run_command([
        "npm", "install", 
        "babel-plugin-transform-import-meta", 
        "@babel/plugin-transform-modules-commonjs",
        "@babel/plugin-proposal-export-namespace-from",
        "--save-dev", "--legacy-peer-deps"
    ])

    # 2. metro.config.js (O "Coração" do Fix)
    # Aqui forçamos o Metro a NÃO ignorar transformações de módulos.
    metro_content = """const { getDefaultConfig } = require('expo/metro-config');
const config = getDefaultConfig(__dirname);

// Alias para garantir que o Lucide use a versão correta
config.resolver.alias = {
  'lucide-react-native': 'lucide-react',
};

// FORÇA A TRANSPILAÇÃO DE MÓDULOS ESM NO NODE_MODULES
config.transformer.unstable_allowModuleTransforms = true; 

module.exports = config;"""
    
    with open("metro.config.js", "w", encoding="utf-8") as f:
        f.write(metro_content)
    log("metro.config.js atualizado (unstable_allowModuleTransforms ATIVADO).", "SUCCESS")

    # 3. babel.config.js (A "Ponte" de Compatibilidade)
    babel_content = """module.exports = function(api) {
  api.cache(true);
  return {
    presets: ['babel-preset-expo'],
    plugins: [
      'babel-plugin-transform-import-meta',
      '@babel/plugin-transform-modules-commonjs',
      '@babel/plugin-proposal-export-namespace-from'
    ],
  };
};"""
    with open("babel.config.js", "w", encoding="utf-8") as f:
        f.write(babel_content)
    log("babel.config.js atualizado com Triple-Fix.", "SUCCESS")

    # 4. Limpeza de Cache Total
    log("Limpando rastros de builds falhos...")
    if os.path.exists(".expo"):
        shutil.rmtree(".expo")
    if os.path.exists("node_modules/.cache"):
        shutil.rmtree("node_modules/.cache")
    
    log("Iniciando Expo Web em modo limpo...", "SUCCESS")
    # Usamos --clear para garantir que o Metro não reuse nada do erro anterior
    run_command(["npx", "expo", "start", "--web", "--clear"])

if __name__ == "__main__":
    main()
