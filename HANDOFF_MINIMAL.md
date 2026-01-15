# 🧠 HANDOFF MINIMAL — MesaFlow (L6)

## 1. O QUE É ESTE PROJETO
MesaFlow é um sistema SaaS multi-tenant com isolamento por RLS (PostgreSQL),
arquitetura monolito modular e governança forte orientada a auditoria.

Objetivo final:
**Production Ready · LGPD-Ready · Vendável · Auditável**

---

## 2. FONTE DA VERDADE
A única fonte da verdade operacional é:

- `comunication/registry.xml`
- Pasta `governance/` (XMLs apenas)
- Scripts em `comunication/scripts/`

Relatórios servem apenas como **evidência humana**.

---

## 3. O QUE FOI INTENCIONALMENTE REMOVIDO DO CONTEXTO
Os seguintes itens foram isolados em `ignorar/`:

- Logs históricos
- Relatórios antigos
- Scripts rejeitados conceitualmente
- Evidências duplicadas
- Histórico operacional já resolvido

⚠️ **Nunca use esses arquivos como base decisória.**

---

## 4. ESTADO ATUAL REAL
- Backend: operacional
- Banco: RLS ativo e auditado (SEC-01A → D DONE)
- Governança: ativa e validada
- Observabilidade: BLOQUEADA (SENTRY_DSN_BACKEND ausente)
- Frontend: pronto para build final
- Mobile: pendente hardening

---

## 5. ÚNICA AÇÃO HUMANA ESPERADA
Preencher variáveis no `.env`, principalmente:

- `SENTRY_DSN_BACKEND`

---

## 6. COMO A IA DEVE OPERAR
- NÃO pressupor nada
- NÃO recriar scripts DONE
- NÃO editar governance/
- SEMPRE gerar script + relatório + registry update
- Trabalhar apenas com o que está FORA de `ignorar/`

---

## 7. SE HOUVER DÚVIDA
Solicite explicitamente:
- `gerartxt.py`
- ou o conteúdo do `registry.xml`

Nunca avance por inferência.
