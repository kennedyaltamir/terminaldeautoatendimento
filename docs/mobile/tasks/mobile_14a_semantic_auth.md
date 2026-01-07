# 📱 Task 14A: Autenticação Semântica (Mobile)

## 1. Contexto
Implementação do endurecimento da camada de autenticação. O estado da sessão agora é derivado da integridade semântica e temporal do JWT (Access Token), garantindo que o App não opere com credenciais expiradas.

## 2. Diagrama de Estados Final
```text
[IDLE]
  |
  v
[HYDRATING] (Leitura Storage)
  |
  +-- Tokens Ausentes --> [UNAUTHENTICATED]
  |
  +-- Tokens Presentes --+
                         |
                         v
                [CHECKING_EXPIRY] (Lógica JWT)
                         |
      +--- Válido ---+---+--- Expirado ---+
      |                                    |
      v                                    v
[AUTHENTICATED]                    [ATTEMPT REFRESH]
      ^                                    |
      |            +--- Sucesso ---+-------+--- Falha ---+
      |            |                                     |
      +------------+                                     v
                                                  [UNAUTHENTICATED]
                                                  (Clear Storage)
```

## 3. Decisões Técnicas & Blindagem
- **Pureza de Claims:** O estado `user` contém apenas dados extraídos do JWT (`sub`, `role`, `company_id`). Informações de UX (nomes, slugs) são delegadas para Missões de Domínio.
- **Clock Skew Buffer:** Introduzida a constante `EXPIRY_GRACE_SECONDS = 10` para prevenir falhas de requisição em tokens prestes a expirar.
- **Status Sincronizado:** O estado `checking_expiry` é observável e garante a consistência entre o código e esta documentação.

## 4. Escopo Negativo Respeitado
- Sem lógica de autorização (RBAC) aplicada.
- Sem consumo de campos de perfil de API (userName, etc).
- Sem componentes de UI.

---
*Fase 10 — Janeiro de 2026*
