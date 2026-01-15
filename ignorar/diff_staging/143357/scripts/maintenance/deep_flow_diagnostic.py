# DOMAIN: DEVOPS_SCRIPTS
# LAST_MODIFIED: 2026-01-15 14:35:00
import os
import re
import json
from pathlib import Path

# ==============================================================================
# 🩺 MESAFLOW DEEP FLOW DIAGNOSTIC (L8.5)
# ==============================================================================
# Objetivo: Identificar inconsistências de contratos, eventos e renderização
# entre Backend, Frontend e Automação sem realizar alterações.
# ==============================================================================

FILES_TO_SCAN = {
    "backend_delivery": "app/routers/admin_delivery.py",
    "backend_orders": "app/services/order_service.py",
    "frontend_client": "frontend/src/components/menu/OrderStatusView.tsx",
    "frontend_driver": "frontend/src/app/admin/[slug]/driver/page.tsx",
    "automation": "scripts/automation/enterprise_delivery_l8.py",
    "ws_manager": "app/websockets.py"
}

class FlowDiagnostician:
    def __init__(self):
        self.report = {
            "event_mismatches": [],
            "payload_inconsistencies": [],
            "render_blockers": [],
            "automation_gaps": []
        }

    def read_file(self, path):
        p = Path(path)
        if not p.exists():
            return None
        return p.read_text(encoding="utf-8")

    def run_diagnostic(self):
        print("🔍 Iniciando Varredura de Fluxo Sistêmico...")

        # 1. Extração de Eventos do Backend (Despacho)
        be_delivery = self.read_file(FILES_TO_SCAN["backend_delivery"])
        be_events = []
        if be_delivery:
            # Busca manager.broadcast({ "type": "..." })
            matches = re.findall(r'"type":\s*"([^"]+)"', be_delivery)
            be_events.extend(matches)

        # 2. Extração de Listeners do Frontend (Cliente)
        fe_client = self.read_file(FILES_TO_SCAN["frontend_client"])
        fe_listeners = []
        if fe_client:
            # Busca data.type === "..."
            matches = re.findall(r'data\.type\s*===\s*"([^"]+)"', fe_client)
            fe_listeners.extend(matches)

        # 3. Cruzamento de Eventos (Causa Raiz de Sincronia)
        print("📡 Analisando Contratos de Eventos WebSocket...")
        for event in be_events:
            if event not in fe_listeners and "delivery" in event:
                self.report["event_mismatches"].append({
                    "issue": f"Evento emitido pelo Backend não possui listener no Cliente.",
                    "backend_event": event,
                    "affected_file": FILES_TO_SCAN["frontend_client"],
                    "impact": "A tela do cliente não reage quando o motorista inicia a rota."
                })

        # 4. Análise de Estrutura de Payload
        # Backend envia: "payload": {"status": "..."}
        # Frontend espera: data.status
        if be_delivery and fe_client:
            be_payload_flat = '"status": order.status' in be_delivery or '"status": "delivered"' in be_delivery
            be_payload_nested = '"payload": {"status":' in be_delivery
            fe_expects_flat = "setLocalStatus(data.status)" in fe_client
            
            if be_payload_nested and fe_expects_flat:
                self.report["payload_inconsistencies"].append({
                    "issue": "Divergência de aninhamento de Payload.",
                    "backend": "Envia status dentro de objeto 'payload'",
                    "frontend": "Tenta acessar 'data.status' diretamente",
                    "impact": "O estado do React (localStatus) recebe 'undefined', impedindo a transição de UI."
                })

        # 5. Análise de Condições de Renderização (O Mapa)
        if fe_client:
            # Verifica se o mapa depende de status E de coordenadas
            has_status_guard = "localStatus === 'delivering'" in fe_client
            has_pos_guard = "driverPos" in fe_client
            
            if has_status_guard and has_pos_guard:
                # Procura a linha exata da condição do mapa
                map_render_match = re.search(r"\{localStatus === 'delivering'.*?\}", fe_client, re.DOTALL)
                if map_render_match:
                    self.report["render_blockers"].append({
                        "file": FILES_TO_SCAN["frontend_client"],
                        "condition": map_render_match.group(0).strip(),
                        "observation": "O mapa só é montado se o status for 'delivering'. Se o evento falhar, o componente nunca entra no DOM."
                    })

        # 6. Validação de Test IDs na Automação
        auto_script = self.read_file(FILES_TO_SCAN["automation"])
        if auto_script and fe_client:
            test_ids_in_auto = re.findall(r'get_by_test_id\("([^"]+)"\)', auto_script)
            for tid in test_ids_in_auto:
                if f'data-testid="{tid}"' not in fe_client and f'data-testid=\'{tid}\'' not in fe_client:
                    # Exceção para IDs que podem estar em subcomponentes (como o mapa)
                    if "map" not in tid:
                        self.report["automation_gaps"].append({
                            "test_id": tid,
                            "issue": "Test ID referenciado na automação não encontrado no componente do Cliente.",
                            "file": FILES_TO_SCAN["frontend_client"]
                        })

        self.generate_final_report()

    def generate_final_report(self):
        print("\n" + "="*60)
        print("📊 RELATÓRIO DE DIAGNÓSTICO DE FLUXO (MesaFlow OS)")
        print("="*60)
        print(json.dumps(self.report, indent=2, ensure_ascii=False))
        print("="*60)
        
        # Veredito Técnico
        print("\n🧠 VEREDITO TÉCNICO:")
        if self.report["event_mismatches"]:
            print("🔴 FALHA DE CONTRATO: O Backend e o Frontend falam 'línguas' diferentes no WebSocket.")
            print(f"   Backend emite: {self.report['event_mismatches'][0]['backend_event']}")
            print(f"   Frontend espera: order_update")
        
        if self.report["payload_inconsistencies"]:
            print("🔴 FALHA DE SCHEMA: O dado chega, mas o Frontend não consegue 'ler' o status por erro de profundidade no JSON.")
            
        print("\n👉 PRÓXIMO PASSO: Sincronizar os tipos de eventos e a estrutura do payload no Backend e Frontend.")

if __name__ == "__main__":
    diagnostician = FlowDiagnostician()
    diagnostician.run_diagnostic()
