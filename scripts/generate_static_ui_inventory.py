# DOMAIN: QA
# TASK: UI_INVENTORY_STATIC_ANALYSIS
# 
# Este script realiza uma análise estática profunda (AST/Regex) nos arquivos .tsx
# do Frontend (Next.js) e Mobile (React Native) para gerar um inventário de UI
# sem a necessidade de executar a aplicação.
#
# Funcionalidades:
# 1. Mapeamento de rotas baseado em sistema de arquivos (Next.js App Router).
# 2. Extração de elementos interativos (Botões, Inputs, Links).
# 3. Detecção de estados de UI (Loading, Error, Empty) via análise de código.
# 4. Normalização de parâmetros dinâmicos ([slug] -> hamburgueria-ze).

import os
import re
import json
from datetime import datetime
from pathlib import Path

# --- CONFIGURAÇÃO ---
PROJECT_ROOT = Path(".")
WEB_ROOT = PROJECT_ROOT / "frontend/src/app"
MOBILE_ROOT = PROJECT_ROOT / "mobile/src/screens"
OUTPUT_FILE = PROJECT_ROOT / "docs/audit/ui_inventory.json"

# Parâmetros de Teste para Rotas Dinâmicas
ROUTE_PARAMS = {
    "[slug]": "hamburgueria-ze",
    "[id]": "1",
    "[tableId]": "1",
    "[orderId]": "ord-123"
}

# Elementos de Interesse
INTERACTIVE_TAGS = {
    # Web
    "button", "a", "input", "select", "textarea", "Link", "ImageUpload",
    # Mobile
    "Button", "TouchableOpacity", "Pressable", "TextInput", "Switch", "TouchableHighlight"
}

CONTAINER_TAGS = {
    "div", "main", "section", "header", "footer", "form", 
    "View", "SafeAreaView", "ScrollView", "KeyboardAvoidingView", "Card"
}

def normalize_route(file_path: Path, root: Path) -> str:
    """Converte caminho de arquivo em rota Next.js válida."""
    rel_path = file_path.relative_to(root)
    # Remove 'page.tsx' e converte para string
    route = "/" + str(rel_path.parent).replace("\\", "/")
    
    # Limpeza de rotas raiz
    if route == "/.":
        route = "/"
    
    # Substituição de parâmetros dinâmicos
    for param, value in ROUTE_PARAMS.items():
        route = route.replace(param, value)
        
    return route

def extract_attributes(tag_content: str):
    """Extrai atributos relevantes de uma string de tag."""
    attrs = {}
    
    # Regex para capturar chave="valor" ou chave={valor}
    # Simplificado para análise estática
    patterns = [
        (r'placeholder=["\']([^"\']*)["\']', 'placeholder'),
        (r'aria-label=["\']([^"\']*)["\']', 'aria_label'),
        (r'type=["\']([^"\']*)["\']', 'type'),
        (r'testID=["\']([^"\']*)["\']', 'testID'),
        (r'data-testid=["\']([^"\']*)["\']', 'testID'),
        (r'href=["\']([^"\']*)["\']', 'href'),
        (r'href=\{`([^`]*)`\}', 'href_dynamic'), # Captura href template literal
        (r'on[A-Z]\w+', 'action'), # Captura onClick, onPress, etc.
        (r'required', 'required'),
        (r'disabled', 'disabled')
    ]
    
    for pattern, key in patterns:
        match = re.search(pattern, tag_content)
        if match:
            if key == 'action':
                attrs['action'] = match.group(0).split('=')[0] # Nome do evento
            elif key == 'required' or key == 'disabled':
                attrs[key] = True
            else:
                attrs[key] = match.group(1)
                
    return attrs

def analyze_file_content(content: str):
    """Analisa o conteúdo do arquivo em busca de elementos e estrutura."""
    elements = []
    layout = []
    states = set()
    flows = []
    
    # 1. Análise de Elementos Interativos
    # Procura por tags de abertura <Tag ...>
    tag_pattern = re.compile(r'<(\w+)([^>]*)>')
    
    for match in tag_pattern.finditer(content):
        tag_name = match.group(1)
        attrs_str = match.group(2)
        
        if tag_name in INTERACTIVE_TAGS:
            attrs = extract_attributes(attrs_str)
            
            # Tenta encontrar o texto do botão/link (conteúdo entre tags)
            # Heurística simples: olha os próximos caracteres
            text_content = "N/A"
            end_pos = match.end()
            next_chunk = content[end_pos:end_pos+50]
            text_match = re.search(r'([^<]+)</', next_chunk)
            if text_match:
                text_content = text_match.group(1).strip()
            
            # Determina o nome do elemento
            name = attrs.get('placeholder') or attrs.get('aria_label') or attrs.get('testID') or text_content
            if len(name) > 30: name = name[:27] + "..." # Truncar textos longos
            
            # Validações
            validations = []
            if attrs.get('required'): validations.append('required')
            if attrs.get('type'): validations.append(f"type:{attrs['type']}")
            
            # Fluxos (Links)
            if 'href' in attrs:
                flows.append(f"Navegar -> {attrs['href']}")
            if 'href_dynamic' in attrs:
                flows.append(f"Navegar -> {attrs['href_dynamic']} (Dinâmico)")
            if 'action' in attrs:
                # Tenta inferir ação pelo nome da função (ex: handleLogin)
                action_match = re.search(r'=\{([^}]*)\}', attrs_str)
                if action_match:
                    func_name = action_match.group(1)
                    flows.append(f"Executar -> {func_name}")

            elements.append({
                "tipo": tag_name,
                "nome": name,
                "acao": attrs.get('action', 'navigation' if 'href' in attrs else 'interaction'),
                "validacao": ", ".join(validations) if validations else "none",
                "propriedades": attrs
            })
            
        elif tag_name in CONTAINER_TAGS:
            layout.append(tag_name)

    # 2. Análise de Estados (Heurística de Código)
    if "isLoading" in content or "loading" in content:
        states.add("loading")
    if "error" in content or "isError" in content:
        states.add("error")
    if "length === 0" in content or "length == 0" in content:
        states.add("empty")
    if "onClick" in content or "onPress" in content:
        states.add("interactive")

    return {
        "layout": list(dict.fromkeys(layout)), # Remove duplicatas mantendo ordem
        "elementos": elements,
        "estados": list(states),
        "fluxos": list(dict.fromkeys(flows))
    }

def scan_web():
    print("🌐 Iniciando Análise Estática Web (Next.js)...")
    results = []
    
    if not WEB_ROOT.exists():
        print(f"⚠️ Diretório Web não encontrado: {WEB_ROOT}")
        return results

    for file_path in WEB_ROOT.rglob("page.tsx"):
        try:
            content = file_path.read_text(encoding="utf-8")
            analysis = analyze_file_content(content)
            
            # Extrai título da página (export default function Nome...)
            func_match = re.search(r'export default function (\w+)', content)
            screen_name = func_match.group(1) if func_match else "UnknownPage"
            
            results.append({
                "tela": screen_name,
                "rota": normalize_route(file_path, WEB_ROOT),
                "arquivo": str(file_path.relative_to(PROJECT_ROOT)),
                "layout": analysis["layout"],
                "elementos": analysis["elementos"],
                "estados_detectados": analysis["estados"],
                "fluxo": analysis["fluxos"]
            })
            print(f"   ✅ Processado: {screen_name}")
            
        except Exception as e:
            print(f"   ❌ Erro em {file_path.name}: {e}")
            
    return results

def scan_mobile():
    print("\n📱 Iniciando Análise Estática Mobile (React Native)...")
    results = []
    
    if not MOBILE_ROOT.exists():
        print(f"⚠️ Diretório Mobile não encontrado: {MOBILE_ROOT}")
        return results

    for file_path in MOBILE_ROOT.rglob("*.tsx"):
        try:
            content = file_path.read_text(encoding="utf-8")
            analysis = analyze_file_content(content)
            
            screen_name = file_path.stem
            
            results.append({
                "tela": screen_name,
                "rota": str(file_path.relative_to(PROJECT_ROOT)),
                "layout": analysis["layout"],
                "elementos": analysis["elementos"],
                "estados_codigo": analysis["estados"],
                "fluxo": analysis["fluxos"]
            })
            print(f"   ✅ Processado: {screen_name}")
            
        except Exception as e:
            print(f"   ❌ Erro em {file_path.name}: {e}")
            
    return results

def main():
    print("========================================")
    print("🕵️ MESAFLOW UI STATIC INVENTORY v5.0")
    print("========================================")
    
    web_data = scan_web()
    mobile_data = scan_mobile()
    
    inventory = {
        "meta": {
            "timestamp": datetime.now().isoformat(),
            "version": "MesaFlow OS v5.0",
            "generator": "UI Static Scanner (Python)",
            "stats": {
                "web_screens": len(web_data),
                "mobile_screens": len(mobile_data)
            }
        },
        "web": web_data,
        "mobile": mobile_data
    }
    
    # Garantir diretório de saída
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(inventory, f, indent=2, ensure_ascii=False)
        
    print("\n" + "="*40)
    print(f"✅ Inventário gerado com sucesso!")
    print(f"📄 Arquivo: {OUTPUT_FILE}")
    print(f"📊 Total Telas: {len(web_data) + len(mobile_data)}")
    print("========================================")

if __name__ == "__main__":
    main()

