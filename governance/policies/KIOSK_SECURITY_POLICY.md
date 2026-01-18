# DOMAIN: GOVERNANCE
# LAST_MODIFIED: 2026-01-16 16:00:00
# 🖥️ Política de Segurança do Modo Kiosk (Totem)

## 1. Sandbox de Navegação
O modo Kiosk deve atuar como uma sandbox visual. É terminantemente proibido o uso de qualquer lógica de redirecionamento automático para rotas fora do escopo `/[slug]/kiosk` ou `/[slug]/menu` enquanto o estado `LOCKED` ou `BREACHED` estiver ativo.

## 2. Isolamento de Interceptores
As APIs de segurança do Kiosk (validação de senha) devem ser consumidas via clientes HTTP isolados que não possuam lógica de redirecionamento em caso de erro 401/403.

## 3. Proteção contra Brute Force
O sistema deve implementar proteção em duas camadas:
1.  **Client-side:** Lockout temporal de 30 segundos após 3 tentativas incorretas.
2.  **Server-side:** Rate-limit por IP e Slug no endpoint de validação pública.

## 4. Trap Mode (Contenção)
Qualquer tentativa de violação do modo Fullscreen sem a devida autenticação deve forçar o sistema para o estado `BREACHED`, bloqueando a interface e exigindo intervenção técnica.

