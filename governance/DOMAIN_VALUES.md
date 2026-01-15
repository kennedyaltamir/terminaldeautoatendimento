# DOMAIN: GOVERNANCE
# LAST_MODIFIED: 2026-01-11 11:10:00
# 📚 Manifesto de Dados de Domínio (Domain Values)
**Status:** SSOT (Single Source of Truth)
**Date:** 2026-01-11

Este documento lista os valores canônicos permitidos para campos enumerados no sistema.
Qualquer divergência entre este documento e o código (`app/models/core.py`) é considerada uma violação de integridade.

## 1. Core Enums

### PlanTier
| Name | Value | Descrição |
| :--- | :--- | :--- |
| `FREE` | `free` | Plano gratuito limitado. |
| `PRO` | `pro` | Plano pago completo. |
| `ENTERPRISE` | `enterprise` | Plano customizado para redes. |

### CompanySegment
| Name | Value | Descrição |
| :--- | :--- | :--- |
| `GASTRO` | `gastro` | Restaurantes e Bares. |
| `EVENT` | `event` | Estádios e Shows. |
| `HOTEL` | `hotel` | Hotelaria e Resorts. |
| `CORP` | `corp` | Empresas e Refeitórios. |

### OrderStatus
| Name | Value | Descrição |
| :--- | :--- | :--- |
| `PENDING` | `pending` | Aguardando aceite. |
| `ACCEPTED` | `accepted` | Aceito pela cozinha. |
| `PREPARING` | `preparing` | Em produção. |
| `READY` | `ready` | Pronto para retirada/entrega. |
| `DELIVERING` | `delivering` | Saiu para entrega. |
| `DELIVERED` | `delivered` | Entregue ao cliente. |
| `CANCELED` | `canceled` | Cancelado. |

### PaymentProvider
| Name | Value | Descrição |
| :--- | :--- | :--- |
| `MERCADO_PAGO` | `mercadopago` | Gateway padrão Latam. |
| `STRIPE` | `stripe` | Gateway global / SaaS. |
| `EFI` | `efi` | Boleto/Pix bancário. |
| `NONE` | `none` | Sem provedor configurado. |

---
*Valores devem ser sempre persistidos em **lowercase**.*