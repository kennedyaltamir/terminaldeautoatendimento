import os
import sys
import re

def verify_compliance_mapping():
    print("🔍 Iniciando Verificação de Mapeamento de Compliance (TASK-ENT-07)...")

    mapping_file = "docs/enterprise/COMPLIANCE_MAPPING.md"

    # 1. Verificar Existência do Arquivo
    if not os.path.exists(mapping_file):
        print(f"❌ Arquivo de Mapeamento FALTANDO: {mapping_file}")
        sys.exit(1)
    print(f"✅ Arquivo encontrado: {mapping_file}")

    # 2. Extrair Links de Evidência
    # Procura por padrões como `caminho/arquivo.md` ou `app/arquivo.py` dentro da tabela
    with open(mapping_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex simples para capturar caminhos de arquivo entre crases ou links markdown
    # Ex: `docs/legal/RoPA.md` ou [Link](docs/legal/RoPA.md)
    evidence_links = re.findall(r'`([\w/.-]+)`', content)
    
    # Filtra apenas caminhos de arquivo (com extensão)
    file_paths = [p for p in evidence_links if "." in p and "/" in p]

    if not file_paths:
        print("❌ Nenhuma evidência linkada encontrada no documento.")
        sys.exit(1)

    print(f"📊 Evidências citadas: {len(file_paths)}")

    # 3. Validar Existência das Evidências
    missing_evidence = []
    for path in file_paths:
        # Remove possíveis sufixos de texto
        clean_path = path.strip()
        if not os.path.exists(clean_path):
            print(f"❌ Evidência citada NÃO EXISTE: {clean_path}")
            missing_evidence.append(clean_path)
        else:
            # print(f"   OK: {clean_path}") # Verbose off
            pass

    if missing_evidence:
        print(f"\n🚨 Falha de Integridade: {len(missing_evidence)} documentos citados não foram encontrados.")
        sys.exit(1)

    # 4. Verificar Cobertura de Frameworks
    required_frameworks = ["SOC 2", "ISO/IEC 27001", "LGPD"]
    for fw in required_frameworks:
        if fw not in content:
            print(f"❌ Framework obrigatório ausente: {fw}")
            sys.exit(1)

    print("\n🏆 Compliance Mapping Verified: Controls linked to valid evidence.")
    sys.exit(0)

if __name__ == "__main__":
    verify_compliance_mapping()
