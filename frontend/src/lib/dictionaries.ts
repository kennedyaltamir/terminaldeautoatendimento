/**
 * Author: MESAFLOW_AI
 * Version: 11.11 (Full Dictionary Restoration)
 * DNA_ID: a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b
 * Objective: Complete multi-language support for Landing Page and Kiosk.
 */
export type Locale = 'pt' | 'en' | 'es';

export const dictionaries = {
  pt: {
    navbar: {
      solutions: "Soluções",
      features: "Recursos",
      pricing: "Planos",
      login: "Login",
      start: "Começar",
    },
    hero: {
      badge: "Sistema Operacional v2.0 Disponível",
      title_prefix: "O Sistema Operacional para",
      subtitle: "Orquestre pedidos, pagamentos e entregas em ambientes de alto tráfego. Elimine filas e automatize sua operação sem obrigar seu cliente a baixar nada.",
      cta_primary: "Começar Agora",
      cta_secondary: "Ver Demo",
      stats: ["Setup em 2 min", "Sem mensalidade fixa", "99.99% SLA"],
      typewriter: ["Restaurantes", "Estádios", "Hotéis", "Eventos", "Food Halls"]
    },
    kiosk: {
      attract_title: "BATEU AQUELA",
      attract_highlight: "FOME?",
      tap_to_start: "TOQUE PARA COMEÇAR",
      footer_tag: "MesaFlow Totem Intelligence v5.0",
      back: "Voltar",
      help: "Ajuda",
      categories: "Categorias",
      checkout_prompt: "Quase lá! Como prefere pagar?",
      success_message: "Pedido Confirmado!",
      order_id_label: "Sua senha é:",
      return_home: "Retornando à tela inicial em",
      offline_warning: "Modo Contingência: Dirija-se ao Caixa",
      pre_sale_ticket: "Imprimindo ticket de pré-venda...",
      upsell_title: "Deseja turbinar seu pedido?",
      add_to_cart: "Adicionar",
      finish: "Finalizar Pedido"
    }
  },
  en: {
    navbar: {
      solutions: "Solutions",
      features: "Features",
      pricing: "Pricing",
      login: "Login",
      start: "Get Started",
    },
    hero: {
      badge: "Operating System v2.0 Available",
      title_prefix: "The Operating System for",
      subtitle: "Orchestrate orders, payments, and deliveries in high-traffic environments. Eliminate queues and automate your operation without forcing app downloads.",
      cta_primary: "Start Now",
      cta_secondary: "Live Demo",
      stats: ["2 min Setup", "No fixed monthly fee", "99.99% SLA"],
      typewriter: ["Restaurants", "Stadiums", "Hotels", "Events", "Food Halls"]
    },
    kiosk: {
      attract_title: "ARE YOU",
      attract_highlight: "HUNGRY?",
      tap_to_start: "TAP TO START",
      footer_tag: "MesaFlow Totem Intelligence v5.0",
      back: "Back",
      help: "Help",
      categories: "Categories",
      checkout_prompt: "Almost there! How do you want to pay?",
      success_message: "Order Confirmed!",
      order_id_label: "Your number is:",
      return_home: "Returning to home in",
      offline_warning: "Contingency Mode: Please go to the counter",
      pre_sale_ticket: "Printing pre-sale ticket...",
      upsell_title: "Want to upgrade your order?",
      add_to_cart: "Add",
      finish: "Finish Order"
    }
  },
  es: {
    navbar: {
      solutions: "Soluciones",
      features: "Funciones",
      pricing: "Precios",
      login: "Ingresar",
      start: "Comenzar",
    },
    hero: {
      badge: "Sistema Operativo v2.0 Disponible",
      title_prefix: "El Sistema Operativo para",
      subtitle: "Orqueste pedidos, pagos y entregas en entornos de alto tráfico. Elimine filas y automatice su operación sin obligar a su cliente a descargar nada.",
      cta_primary: "Empezar Ahora",
      cta_secondary: "Ver Demo",
      stats: ["Configuración en 2 min", "Sin mensualidad fija", "99.99% SLA"],
      typewriter: ["Restaurantes", "Estadios", "Hoteles", "Eventos", "Patios de Comida"]
    },
    kiosk: {
      attract_title: "¿TIENES",
      attract_highlight: "HAMBRE?",
      tap_to_start: "TOCA PARA EMPEZAR",
      footer_tag: "MesaFlow Totem Intelligence v5.0",
      back: "Volver",
      help: "Ayuda",
      categories: "Categorías",
      checkout_prompt: "¿Casi listo! ¿Cómo prefieres pagar?",
      success_message: "¡Pedido Confirmado!",
      order_id_label: "Tu número es:",
      return_home: "Regresando al inicio en",
      offline_warning: "Modo Contingencia: Diríjase a la caja",
      pre_sale_ticket: "Imprimiendo ticket de preventa...",
      upsell_title: "¿Quieres mejorar tu pedido?",
      add_to_cart: "Añadir",
      finish: "Finalizar Pedido"
    }
  }
};