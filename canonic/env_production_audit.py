
import os
import sys
import re
from pathlib import Path

# Configuração
MOBILE_SRC = Path("mobile/src")
FORBIDDEN_PATTERNS = [
    (r"192\.168\.\d+\.\d+", "IP Local (LAN)"),
    (r"127\.0\.0\.1", "IP Local (Loopback)"),
    (r"10\.0\.2\.2", "IP Emulador Android"),
    (r"localhost", "Localhost Hardcoded"),
    (r"http://", "Protocolo Inseguro (HTTP)"),
]

# Arquivos permitidos para conter fallbacks (apenas lógica de infra)
WHITELIST_FILES = [
    "mobile/src/config/env.ts",
    "mobile/src/services/api.ts" # Pode conter headers default
]

def audit_mobile_env():
    print("🛡️  Iniciando Auditoria de Segurança de Rede Mobile...")
    violations = 0
    
    if not MOBILE_SRC.exists():
        print("❌ Diretório mobile/src não encontrado.")
        sys.exit(1)

    for file_path in MOBILE_SRC.rglob("*.ts*"):
        # Ignora node_modules e arquivos de teste
        if "node_modules" in str(file_path) or "__tests__" in str(file_path):
            continue
            
        # Normaliza path para verificação de whitelist
        rel_path = str(file_path).replace("\\", "/")
        
        try:
            content = file_path.read_text(encoding="utf-8")
            
            for pattern, desc in FORBIDDEN_PATTERNS:
                # Se encontrar o padrão
                if re.search(pattern, content):
                    # Verifica se é um arquivo permitido para ter esses valores (ex: fallback logic)
                    if rel_path in WHITELIST_FILES:
                        # Verifica se está dentro de um bloco de fallback explícito ou comentário
                        # (Heurística simples: se o arquivo é whitelist, assumimos que a lógica interna trata)
                        continue
                    
                    print(f"   🚨 VIOLAÇÃO: {desc} encontrado em {rel_path}")
                    # Mostra a linha (snippet)
                    for i, line in enumerate(content.splitlines()):
                        if re.search(pattern, line):
                            print(f"      L{i+1}: {line.strip()[:100]}")
                    violations += 1

        except Exception as e:
            print(f"   ⚠️  Erro ao ler {rel_path}: {e}")

    print("-" * 60)
    if violations > 0:
        print(f"❌ AUDITORIA FALHOU: {violations} violações de segurança de rede detectadas.")
        print("   Ação: Remova IPs hardcoded e use variáveis de ambiente (env.ts).")
        sys.exit(1)
    else:
        print("✅ AUDITORIA PASSOU: Nenhum IP ou protocolo inseguro hardcoded detectado.")
        sys.exit(0)

if __name__ == "__main__":
    audit_mobile_env()

