import os
import subprocess
import sys
import json

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
    log("🚀 Iniciando Reparo de Bundle Expo Web (Fase 10 - 2026)", "INFO")

    # 1. Ajuste de diretório
    current_dir = os.getcwd()
    if os.path.basename(current_dir) != "mobile":
        if os.path.exists("mobile"):
            os.chdir("mobile")
            log("Mudando para o diretório 'mobile/'")
        else:
            log("Erro: Execute este script na raiz do projeto ou dentro de 'mobile/'", "ERROR")
            sys.exit(1)

    # 2. Escrita do babel.config.js (Transformação Ativa)
    babel_content = """module.exports = function(api) {
  api.cache(true);
  return {
    presets: ['babel-preset-expo'],
    plugins: [
      ['babel-plugin-transform-import-meta']
    ],
  };
};"""
    with open("babel.config.js", "w", encoding="utf-8") as f:
        f.write(babel_content)
    log("Arquivo babel.config.js atualizado com plugin de transformação.", "SUCCESS")

    # 3. Escrita do metro.config.js (Desativar Hermes na Web)
    metro_content = """const { getDefaultConfig } = require('expo/metro-config');
const config = getDefaultConfig(__dirname);

// Força a transpilação padrão para evitar erros de import.meta no navegador
config.transformer.unstable_transformProfile = 'default';

module.exports = config;"""
    with open("metro.config.js", "w", encoding="utf-8") as f:
        f.write(metro_content)
    log("Arquivo metro.config.js atualizado (unstable_transformProfile fix).", "SUCCESS")

    # 4. Verificação de dependência
    log("Verificando dependências no package.json...")
    with open("package.json", "r") as f:
        pkg = json.load(f)
    
    if "babel-plugin-transform-import-meta" not in pkg.get("devDependencies", {}) and \
       "babel-plugin-transform-import-meta" not in pkg.get("dependencies", {}):
        log("Instalando transformador de import-meta...")
        run_command(["npm", "install", "babel-plugin-transform-import-meta", "--save-dev", "--legacy-peer-deps"])
    else:
        log("Dependência babel-plugin-transform-import-meta já presente.")

    # 5. Limpeza de Cache e Reinício
    log("Limpando cache do Metro e reiniciando servidor...", "INFO")
    run_command(["npx", "expo", "start", "--web", "--clear"])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("Operação cancelada.", "ERROR")
