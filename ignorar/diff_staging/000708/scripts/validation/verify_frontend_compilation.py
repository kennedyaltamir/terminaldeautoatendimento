# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 00:15:00
import subprocess
import sys
import os
import io

# Windows Resilience
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def verify():
    print("🎨 Verificando compilação do Frontend (TypeScript)...")
    frontend_dir = os.path.join(os.getcwd(), "frontend")
    
    # Check if node_modules exists
    if not os.path.exists(os.path.join(frontend_dir, "node_modules")):
        print("❌ node_modules não encontrado em frontend/. Execute 'npm install' dentro da pasta frontend.")
        return 1

    try:
        # Executa tsc --noEmit para validar sintaxe e tipos sem gerar arquivos
        # shell=True é necessário no Windows para resolver o comando npx
        print("   ⏳ Executando 'npx tsc --noEmit'...")
        result = subprocess.run(
            "npx tsc --noEmit", 
            cwd=frontend_dir, 
            shell=True, 
            capture_output=True, 
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        if result.returncode == 0:
            print("✅ Frontend compilado com sucesso (Sintaxe OK).")
            return 0
        else:
            print("❌ Erros de compilação detectados:")
            # Filtra a saída para mostrar apenas as primeiras 10 linhas de erro para não poluir o terminal
            lines = result.stdout.splitlines()
            for line in lines[:20]:
                print(f"   {line}")
            if len(lines) > 20:
                print(f"   ... e mais {len(lines) - 20} linhas.")
            return 1
            
    except Exception as e:
        print(f"💥 Erro ao executar verificação: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(verify())
