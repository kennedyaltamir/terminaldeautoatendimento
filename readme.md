# 🚀 MesaFlow OS
> **O Sistema Operacional para Ambientes de Alto Tráfego.**
> Orquestre pedidos, pagamentos e logística em tempo real com uma arquitetura híbrida inovadora.

---

## 📖 Visão Geral
O **MesaFlow** é uma plataforma SaaS B2B Enterprise projetada para eliminar a fricção operacional em Restaurantes, Hotéis, Estádios e Eventos. Diferente de cardápios digitais passivos, o MesaFlow é um motor de execução que conecta o cliente final diretamente à linha de produção.

### 💡 O Diferencial Híbrido
O sistema permite que o **Autoatendimento** (Cliente via QR Code/PWA) e a **Operação Assistida** (Staff via Mobile POS) coexistam na mesma comanda em tempo real, garantindo agilidade sem perder o toque humano.

---

## ✨ Funcionalidades Core
- **🍔 Cardápio Inteligente:** PWA ultra-leve com motor de Upselling via IA.
- **👨‍🍳 KDS (Kitchen Display System):** Monitor de produção com SLA visual e alertas sensoriais.
- **📱 Mobile POS:** App nativo para garçons com gestão de mesas e fechamento rápido.
- **💰 Fintech Integrada:** Split de pagamento automático e gestão de cashback.
- **🛵 Logística:** App do entregador com rastreamento GPS e Proof of Delivery (POD).
- **🧾 Fiscal:** Emissão automatizada de NFC-e com modo de contingência offline.

---

## 🛠️ Tech Stack
### **Backend**
- **Linguagem:** Python 3.11+
- **Framework:** FastAPI (Async/Await)
- **ORM:** SQLAlchemy 2.0 (PostgreSQL)
- **Real-time:** Redis Pub/Sub + WebSockets

### **Frontend (Web)**
- **Framework:** Next.js 14 (App Router)
- **Estilo:** Tailwind CSS + Framer Motion
- **Offline:** Dexie.js (IndexedDB)

### **Mobile (Nativo)**
- **Framework:** React Native + Expo SDK 54
- **Estado:** Zustand
- **Segurança:** Expo SecureStore

---

## 🚀 Como Iniciar (Desenvolvimento)

### 1. Pré-requisitos
- Python 3.11+
- Node.js 18+
- PostgreSQL & Redis

### 2. Instalação
```bash
# Instalar dependências do Backend
pip install -r requirements.txt

# Instalar dependências do Frontend
cd frontend && npm install && cd ..
```

### 3. Configuração
Copie o arquivo de exemplo e preencha suas chaves:
```bash
cp .env.example .env
```

### 4. Execução
Inicie o ecossistema completo (Back + Front) com um único comando:
```bash
python run.py
```

---

## 📂 Estrutura do Projeto
- `app/`: Core do Backend (Models, Routers, Services).
- `frontend/`: Aplicação Web Next.js.
- `mobile/`: Aplicativo Nativo React Native.
- `docs/`: Documentação de Governança, API e Manuais.
- `scripts/`: Ferramentas de automação, manutenção e testes.

---

## ⚖️ Licença
Proprietária. Todos os direitos reservados a MesaFlow Tecnologia Ltda.
