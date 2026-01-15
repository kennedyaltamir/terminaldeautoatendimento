# 🧠 MesaFlow AI Knowledge Base
**Status:** ACTIVE | **Maturity:** L8.6

--- ENTRY: 2026-01-15T15:30:00 ---
**CONTEXT:** Playwright Python TypeError.
**DECISION:** Removido o argumento `message` de `expect(...).to_be_visible()`. No Playwright Python, mensagens customizadas de erro não são suportadas nativamente nesse método.
**LEARNING:** Diferenças de API entre Playwright JS e Python devem ser observadas. Adicionada a configuração `permissions=["geolocation"]` no `browser.new_context()` para suprimir popups de permissão do sistema operacional durante a simulação.
**STATUS:** Script `enterprise_delivery_l8.py` estabilizado para ambiente Windows.
