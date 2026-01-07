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
    log("🚀 REPARO DEFINITIVO: Expo Web Realtime Fix (v2.0)", "INFO")

    # 1. Garantir diretório correto
    if os.path.basename(os.getcwd()) != "mobile":
        if os.path.exists("mobile"):
            os.chdir("mobile")
        else:
            log("Erro: Execute na raiz ou dentro de 'mobile/'", "ERROR")
            sys.exit(1)

    # 2. Instalar dependência Web do Lucide para o Alias
    log("Instalando lucide-react (Web version) para o Alias de compatibilidade...")
    run_command(["npm", "install", "lucide-react", "babel-plugin-transform-import-meta", "--save-dev", "--legacy-peer-deps"])

    # 3. metro.config.js (COM ALIAS DE COMPATIBILIDADE)
    metro_content = """const { getDefaultConfig } = require('expo/metro-config');
const config = getDefaultConfig(__dirname);

// 1. Alias: Redireciona chamadas nativas para web para evitar erro de import.meta
config.resolver.alias = {
  'lucide-react-native': 'lucide-react',
};

// 2. Extensões: Adiciona suporte a módulos modernos
config.resolver.sourceExts.push('mjs');

// 3. Transformer Fix
if (config.transformer) {
  config.transformer.unstable_transformProfile = 'default';
}

module.exports = config;"""
    
    with open("metro.config.js", "w", encoding="utf-8") as f:
        f.write(metro_content)
    log("metro.config.js atualizado com Alias e MJS support.", "SUCCESS")

    # 4. babel.config.js (PURIFICADO)
    babel_content = """module.exports = function(api) {
  api.cache(true);
  return {
    presets: ['babel-preset-expo'],
    plugins: [
      'babel-plugin-transform-import-meta'
    ],
  };
};"""
    with open("babel.config.js", "w", encoding="utf-8") as f:
        f.write(babel_content)
    log("babel.config.js purificado.", "SUCCESS")

    # 5. Limpeza Agressiva de Cache
    log("Limpando caches físicos (.expo, node_modules/.cache)...")
    folders_to_clean = [".expo", "node_modules/.cache/metro"]
    for folder in folders_to_clean:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
                log(f"Pasta {folder} removida.")
            except:
                log(f"Não foi possível remover {folder}, continuando...", "INFO")

    # 6. Reiniciar
    log("Iniciando Expo Web com limpeza total de cache...", "INFO")
    run_command(["npx", "expo", "start", "--web", "--clear"])

if __name__ == "__main__":
    main()
