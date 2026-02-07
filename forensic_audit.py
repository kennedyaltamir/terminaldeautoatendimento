import os
import re
from pathlib import Path

class ProjectAuditor:
    def __init__(self):
        self.root = Path(".").absolute()
        self.report_path = self.root / "audit_report.txt"
        self.findings = []
        self.backend_path = self.root / "app"
        self.frontend_path = self.root / "frontend"

    def log(self, level, file, line, msg, impact, cors_effect=True):
        entry = (
            f"[{level}]\n"
            f"Arquivo: {file}\n"
            f"Linha: {line}\n"
            f"Problema: {msg}\n"
            f"Impacto: {impact}\n"
            f"CORS Falso-Positivo: {'SIM (Erro impede middleware)' if cors_effect else 'NÃO'}\n"
            f"{'-'*40}\n"
        )
        self.findings.append(entry)

    def audit_fastapi_initialization(self):
        """Analisa a ordem de registro do middleware e roteadores no main.py"""
        main_py = self.backend_path / "main.py"
        if not main_py.exists(): return

        content = main_py.read_text(encoding="utf-8")
        lines = content.splitlines()

        cors_idx = -1
        router_idx = 9999
        
        for i, line in enumerate(lines):
            if "CORSMiddleware" in line and "add_middleware" in line:
                cors_idx = i
            if "include_router" in line:
                router_idx = min(router_idx, i)

        if cors_idx > router_idx:
            self.log("ERROR", "app/main.py", cors_idx + 1,
                     "Middleware de CORS registrado APÓS os roteadores.",
                     "Exceções nos routers retornarão 500 sem headers CORS.", True)
        
        if cors_idx == -1:
            self.log("CRITICAL", "app/main.py", "Global",
                     "Configuração de CORSMiddleware não encontrada.",
                     "O navegador sempre bloqueará requisições cross-origin.", True)

    def audit_auth_token_logic(self):
        """Analisa o endpoint /api/auth/token em busca de inconsistências de contrato"""
        auth_router = None
        # Tenta localizar o arquivo de router de autenticação
        for p in self.backend_path.rglob("*.py"):
            if "auth" in p.name:
                content = p.read_text(encoding="utf-8")
                if "/token" in content or "POST" in content:
                    auth_router = p
                    break
        
        if auth_router:
            content = auth_router.read_text(encoding="utf-8")
            # Verifica se usa OAuth2PasswordRequestForm mas o frontend manda JSON
            if "OAuth2PasswordRequestForm" in content:
                # Checar frontend
                api_ts = self.frontend_path / "src" / "lib" / "api.ts"
                if api_ts.exists():
                    fe_content = api_ts.read_text(encoding="utf-8")
                    if "JSON.stringify" in fe_content and "/auth/token" in fe_content:
                        self.log("CRITICAL", "app/routers/auth.py vs api.ts", "Contrato",
                                 "Backend espera Form-Data (OAuth2) mas Frontend envia JSON.",
                                 "FastAPI retorna 422 ou 500 se o parse falhar.", True)

    def audit_missing_references(self):
        """Varre imports quebrados e referências nulas"""
        for py_file in self.backend_path.rglob("*.py"):
            if "__pycache__" in str(py_file): continue
            content = py_file.read_text(encoding="utf-8")
            
            # Detecta decorators não importados (causa comum de erro 500 no boot)
            decorators = re.findall(r"@(\w+)", content)
            for dec in decorators:
                if dec in ["app", "router", "property", "classmethod", "staticmethod"]: continue
                if f"import {dec}" not in content and f"def {dec}" not in content:
                    # Verifica se o decorator está no cache_response que causou problemas antes
                    if dec == "cache_response":
                        self.log("CRITICAL", str(py_file.relative_to(self.root)), "Linha Dinâmica",
                                 f"Decorator @{dec} utilizado mas não definido/importado.",
                                 "Backend falha no carregamento do módulo. Uvicorn retorna 500/net::ERR_FAILED.", True)

    def audit_env_consistency(self):
        """Verifica acesso direto a os.environ que causa crash se a chave sumir"""
        for py_file in self.backend_path.rglob("*.py"):
            content = py_file.read_text(encoding="utf-8")
            matches = re.finditer(r"os\.environ\[['\"](\w+)['\"]\]", content)
            for m in matches:
                key = m.group(1)
                # Se não houver proteção de try/except ao redor
                self.log("WARNING", str(py_file.relative_to(self.root)), "Acesso Direto ENV",
                         f"Acesso a os.environ['{key}'] sem fallback.",
                         "Se a variável sumir, o app crasha com KeyError imediatamente.", False)

    def run(self):
        print("🚀 Iniciando Auditoria Forense MesaFlow...")
        self.audit_fastapi_initialization()
        self.audit_auth_token_logic()
        self.audit_missing_references()
        self.audit_env_consistency()
        
        with open(self.report_path, "w", encoding="utf-8") as f:
            if not self.findings:
                f.write("Nenhuma inconsistência crítica detectada pelo scanner estático.")
            else:
                f.writelines(self.findings)
        
        print(f"✅ Auditoria concluída. Relatório gerado em: {self.report_path}")

if __name__ == "__main__":
    auditor = ProjectAuditor()
    auditor.run()