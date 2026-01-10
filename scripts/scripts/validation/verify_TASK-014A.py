import sys
import os
import subprocess
import json

def verify():
    print("🔍 Verificando TASK-014A: Validação Semântica JWT Mobile...")
    
    # 1. Verificação de Existência de Arquivos
    required_files = [
        "mobile/src/services/auth/jwt.ts",
        "mobile/src/store/auth.store.ts",
        "mobile/src/store/__tests__/auth.store.test.ts",
        "mobile/package.json"
    ]
    
    for f_path in required_files:
        if not os.path.exists(f_path):
            print(f"❌ Arquivo faltando: {f_path}")
            sys.exit(1)
        print(f"✅ Arquivo encontrado: {f_path}")

    # 2. Verificação de Conteúdo (Lógica Implementada)
    with open("mobile/src/services/auth/jwt.ts", "r", encoding="utf-8") as f:
        content = f.read()
        if "validateClaims" not in content:
            print("❌ Lógica 'validateClaims' não encontrada em jwt.ts")
            sys.exit(1)

    # 3. Execução dos Testes Automatizados (Jest)
    print("🧪 Executando testes unitários (Jest)...")
    
    # Força a mudança de diretório para 'mobile' antes de rodar o comando
    # Isso evita problemas de resolução de path do npm no Windows
    target_dir = os.path.abspath("mobile")
    os.chdir(target_dir)
    print(f"   📂 Diretório de execução: {os.getcwd()}")

    # Verifica se o script existe no package.json carregado
    try:
        with open("package.json", "r", encoding="utf-8") as f:
            pkg = json.load(f)
            if "test" not in pkg.get("scripts", {}):
                print("❌ ERRO CRÍTICO: 'package.json' na pasta mobile não tem script 'test'.")
                print("   Conteúdo scripts:", pkg.get("scripts"))
                sys.exit(1)
    except Exception as e:
        print(f"❌ Erro ao ler package.json local: {e}")
        sys.exit(1)

    try:
        # Executa npm run test explicitamente
        # -- --runInBand força execução serial para evitar problemas de recurso
        cmd = "npm run test -- src/store/__tests__/auth.store.test.ts --runInBand"
        
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("✅ Testes Unitários: PASSOU")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("❌ Testes Unitários: FALHOU")
        print(f"   Comando: {cmd}")
        print("--- STDOUT ---")
        print(e.stdout)
        print("--- STDERR ---")
        print(e.stderr)
        sys.exit(1)

    print("\n🏆 TASK-014A: VALIDAÇÃO CONCLUÍDA COM SUCESSO.")
    sys.exit(0)

if __name__ == "__main__":
    verify()
