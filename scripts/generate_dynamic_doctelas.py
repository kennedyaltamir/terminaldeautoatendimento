# DOMAIN: DOCUMENTATION
# LAST_MODIFIED: 2026-01-16 06:30:00
import os
import re
import sys
from pathlib import Path
from datetime import datetime

# ==============================================================================
# 🧠 MESAFLOW DYNAMIC DOC GENERATOR v2.3 (PascalCase Fix)
# ==============================================================================
# - Resolve colisões de nomes (Admin vs Public).
# - Corrige nomes com hífens (forgot-password -> ForgotPasswordPage).
# - Aplica Smart Merge para preservar edições manuais.
# ==============================================================================

ROOT_DIR = Path(".")
DOCS_ROOT = ROOT_DIR / "doctelas"
WEB_SRC = ROOT_DIR / "frontend/src/app"
MOBILE_SRC = ROOT_DIR / "mobile/src/screens"

REGEX_PATTERNS = {
    "props_interface": r"interface\s+(\w+Props)\s*{([^}]+)}",
    "interactive_elements": r"<(Button|Input|Select|TouchableOpacity|Pressable|Link|a|Switch|Modal)\b",
    "hooks": r"(useState|useEffect|useQuery|useMutation|useForm|useContext|useAuth)",
}

# Mapa de Renomeação Forçada (Caminho Relativo -> Nome Bonito)
NAME_OVERRIDES = {
    "frontend/src/app/page.tsx": "LandingPage",
    "frontend/src/app/[slug]/menu/page.tsx": "ClientMenuPage",
    "frontend/src/app/admin/[slug]/menu/page.tsx": "AdminMenuPage",
    "frontend/src/app/admin/[slug]/waiter/pos/[tableId]/page.tsx": "WaiterPosPage",
    "frontend/src/app/admin/[slug]/waiter/pos/quick/page.tsx": "QuickPosPage",
    "frontend/src/app/[slug]/kiosk/page.tsx": "KioskAttractScreen",
    "frontend/src/app/[slug]/monitor/page.tsx": "PublicMonitorPage",
    "frontend/src/app/trust/page.tsx": "TrustCenterPage",
    "frontend/src/app/offline/page.tsx": "OfflinePage"
}

def ensure_dirs():
    (DOCS_ROOT / "web").mkdir(parents=True, exist_ok=True)
    (DOCS_ROOT / "mobile").mkdir(parents=True, exist_ok=True)

def clean_screen_name(name):
    """Converte kebab-case ou nomes sujos para PascalCase limpo."""
    # Remove sufixo Page se existir para não duplicar
    if name.endswith("Page"): name = name[:-4]
    # Remove caracteres de rota dinâmica
    name = name.replace("[", "").replace("]", "")
    # Trata hífens (forgot-password -> ForgotPassword)
    parts = name.split('-')
    return "".join(part.capitalize() for part in parts)

def resolve_screen_name(path, platform):
    # 1. Verifica Override Explicito
    rel_full = str(path).replace("\\", "/")
    if rel_full in NAME_OVERRIDES:
        return NAME_OVERRIDES[rel_full]

    # 2. Lógica Automática
    if platform == "Web":
        parts = rel_full.split("/")
        folder_name = path.parent.name
        
        # Tratamento para raiz
        if folder_name == "" or folder_name == ".":
            return "LandingPage"
            
        base_name = clean_screen_name(folder_name)
        
        # Prefixo de Contexto
        prefix = ""
        if "admin" in parts and "Admin" not in base_name:
            prefix = "Admin"
        
        name = f"{prefix}{base_name}"
        if not name.endswith("Page"): name += "Page"
        return name
    else:
        return path.stem

def analyze_file(file_path: Path):
    try:
        content = file_path.read_text(encoding="utf-8")
        elements = sorted(list(set(re.findall(REGEX_PATTERNS["interactive_elements"], content))))
        props_match = re.search(REGEX_PATTERNS["props_interface"], content)
        props_content = props_match.group(2).strip() if props_match else "Nenhuma interface de props explícita."
        hooks = sorted(list(set(re.findall(REGEX_PATTERNS["hooks"], content))))
        return {"elements": elements, "props": props_content, "hooks": hooks, "has_content": True}
    except:
        return {"has_content": False}

def extract_section(content, section_name):
    pattern = f"## {section_name}\n(.*?)\n## "
    match = re.search(pattern, content, re.DOTALL)
    if match: return match.group(1).strip()
    pattern_end = f"## {section_name}\n(.*)"
    match_end = re.search(pattern_end, content, re.DOTALL)
    if match_end: return match_end.group(1).strip()
    return None

def generate_markdown(platform, name, route, file_path, analysis, existing_content=None):
    purpose = "*(Descreva aqui o objetivo principal desta tela.)*"
    rules = "*(Liste regras específicas.)*"
    
    if existing_content:
        p = extract_section(existing_content, "1. Propósito e Objetivo")
        if p and "*" not in p: purpose = p
        r = extract_section(existing_content, "7. Regras de Negócio & Validações")
        if r and "*" not in r: rules = r

    elements_list = "\n".join([f"- [ ] **{el}**: (Descrever ação)" for el in analysis.get("elements", [])]) or "- [ ] *Nenhum elemento interativo detectado.*"
    hooks_list = ", ".join(analysis.get("hooks", []))
    
    return f"""# 📱 {name}
> **Plataforma:** {platform}
> **Rota/Arquivo:** `{route}`
> **Status:** DRAFT (Auto-generated)
> **Última Atualização:** {datetime.now().strftime('%Y-%m-%d')}

## 1. Propósito e Objetivo
{purpose}

## 2. Screenshot de Referência
![Screenshot](../placeholders/{name.lower().replace(' ', '_')}_screenshot.png)

## 3. Estrutura Técnica
**Arquivo Fonte:** `{file_path}`
**Hooks:** `{hooks_list}`

### Props
```typescript
{analysis.get('props', '// Nenhuma prop detectada')}
```

## 4. Elementos Interativos
{elements_list}

## 5. Estados Esperados
- [ ] **Loading:** Skeleton ou Spinner visível?
- [ ] **Empty:** Estado sem dados?
- [ ] **Error:** Feedback visual de falha?
- [ ] **Interactive:** Estado normal de uso.

## 6. Fluxos de Navegação
- **Entrada:** De onde o usuário vem?
- **Saída (Sucesso):** Para onde vai após ação positiva?
- **Saída (Cancelamento):** Para onde vai ao voltar?

## 7. Regras de Negócio & Validações
{rules}

---
*Gerado automaticamente pelo Kernel MesaFlow L6.*
"""

def process_files(src_dir, platform, target_folder):
    count = 0
    for path in src_dir.rglob("*.tsx" if platform == "Mobile" else "page.tsx"):
        if "test" in path.name or path.name == "index.tsx": continue
        
        # Naming Logic v2.3
        screen_name = resolve_screen_name(path, platform)
        
        # Route Logic
        if platform == "Web":
            rel_path = path.relative_to(src_dir)
            route = "/" + str(rel_path.parent).replace("\\", "/")
            if route == "/.": route = "/"
        else:
            route = str(path.relative_to(ROOT_DIR)).replace("\\", "/")

        md_filename = f"{screen_name}.md"
        target_file = DOCS_ROOT / target_folder / md_filename
        
        analysis = analyze_file(path)
        existing_content = target_file.read_text(encoding="utf-8") if target_file.exists() else None
        
        new_content = generate_markdown(f"{platform}", screen_name, route, str(path), analysis, existing_content)
        
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(new_content)
        
        status = "🔄 Merge" if existing_content else "✨ Novo"
        print(f"   {status}: {md_filename}")
        count += 1
    return count

def main():
    print("========================================")
    print("🧠 MESAFLOW DYNAMIC DOC GENERATOR v2.3")
    print("========================================")
    ensure_dirs()
    
    print("🌐 Processando Web...")
    web_c = process_files(WEB_SRC, "Web", "web")
    
    print("📱 Processando Mobile...")
    mob_c = process_files(MOBILE_SRC, "Mobile", "mobile")
    
    # Atualiza README
    web_docs = sorted([f.name for f in (DOCS_ROOT / "web").glob("*.md")])
    mobile_docs = sorted([f.name for f in (DOCS_ROOT / "mobile").glob("*.md")])
    
    readme_content = f"""# 📱 Documentação de Telas - MesaFlow OS

> **Última Sincronização:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

Esta documentação é gerada de forma híbrida: a estrutura inicial é criada automaticamente pelo script `generate_dynamic_doctelas.py` baseada no código fonte, e os detalhes funcionais são preenchidos por humanos/IA.

## 📂 Índice Web ({len(web_docs)} telas)
{chr(10).join([f"- [{doc}](./web/{doc})" for doc in web_docs])}

## 📂 Índice Mobile ({len(mobile_docs)} telas)
{chr(10).join([f"- [{doc}](./mobile/{doc})" for doc in mobile_docs])}

---
*MesaFlow Kernel L6*
"""
    with open(DOCS_ROOT / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

    print("\n✅ Documentação sincronizada com sucesso.")
    print(f"   Total: {web_c + mob_c} arquivos processados.")

if __name__ == "__main__":
    main()

