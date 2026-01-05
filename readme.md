README.md
code
Markdown
download
content_copy
expand_less
# 🚀 MesaFlow: O Sistema Operacional para Food Service

> **Transforme mesas em pontos de venda inteligentes e elimine a fricção entre o cliente e a cozinha.**

![MesaFlow Banner](https://placehold.co/1200x400/ea580c/ffffff?text=MesaFlow+OS)

## 📝 Sobre o Projeto
O **MesaFlow** é uma plataforma SaaS (*Software as a Service*) Fullstack desenvolvida para modernizar a operação de ambientes de alto tráfego. Mais do que um cardápio digital, ele é um ecossistema que centraliza a operação em uma única nuvem, conectando o salão, a cozinha, o delivery e o back-office em tempo real.

O grande diferencial é sua **Arquitetura Híbrida**: permite que o autoatendimento (via QR Code) e o atendimento tradicional (via Garçom) coexistam na mesma comanda, garantindo agilidade sem perder a hospitalidade.

---

## ⚙️ Pilares da Solução

### 1. Experiência do Cliente (Autoatendimento)
*   **Zero App:** Acesso instantâneo via QR Code (PWA).
*   **Autonomia:** Pedido e pagamento (Pix/Cartão) direto pelo celular.
*   **Status Real-Time:** Acompanhamento do progresso ("Preparando" -> "Pronto").

### 2. Operação Inteligente (KDS & Staff)
*   **KDS (Kitchen Display System):** Telas interativas na cozinha com controle de SLA e separação por praça (Bar/Cozinha).
*   **App do Garçom:** Interface móvel para lançar pedidos, fechar contas e receber chamados.
*   **Logística:** Módulo de Delivery com gestão de entregadores e rastreamento.

### 3. Gestão & Fintech (Back-office)
*   **Split de Pagamento:** Divisão automática de receita (SaaS vs Restaurante).
*   **White Label:** Personalização completa de cores e domínio.
*   **Estoque:** Baixa automática via ficha técnica.

---

## 🌍 Versatilidade (Multi-Segmento)
A arquitetura foi projetada para **escalabilidade vertical**, adaptando-se a diferentes cenários:

| Segmento | Aplicação |
| :--- | :--- |
| 🍽️ **Restaurantes** | Gestão de Mesas e Comandas tradicionais. |
| 🏨 **Hotéis** | *Room Service* digital (QR Code no quarto). |
| 🏟️ **Eventos** | Venda direta no assento/cadeira (Fila Expressa). |
| 🏢 **Corporativo** | Gestão de *Coffee Breaks* e praças internas. |

---

## 🛠️ Tech Stack

*   **Backend:** Python 3.11+ (FastAPI, SQLAlchemy Async, Pydantic).
*   **Frontend:** Next.js 14 (App Router, TypeScript, Tailwind CSS).
*   **Database:** PostgreSQL.
*   **Real-time:** WebSockets (com fallback para Redis Pub/Sub).
*   **Infra:** Docker Ready.

---

## 🚀 Como Rodar Localmente

### Pré-requisitos
*   Python 3.11+
*   Node.js 18+
*   PostgreSQL

### 1. Instalação
```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
2. Configuração

Crie um arquivo .env na raiz com a string de conexão do banco:

code
Ini
download
content_copy
expand_less
DATABASE_URL=postgresql://user:pass@localhost:5432/mesaflow_db
SECRET_KEY=sua_chave_secreta
3. Execução

Utilize o script gerenciador para subir tudo:

code
Bash
download
content_copy
expand_less
python run.py

Frontend: http://localhost:3000

API Docs: http://localhost:8000/docs

📄 Licença

Proprietária. Todos os direitos reservados.

code
Code
download
content_copy
expand_less