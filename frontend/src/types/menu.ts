/**
 * DOMAIN: FRONTEND
 * LAST_MODIFIED: 2026-01-23 01:30:00
 * Descrição: Definições de tipos para o domínio de Cardápio, Produtos e Inventário.
 */

import { Company } from './company';

/**
 * Representa uma opção individual de um produto (ex: "Queijo Extra", "Bem Passado").
 */
export interface Option {
  id: number;
  name: string;
  price: number;
  is_available: boolean;
}

/**
 * Agrupador de opções com regras de seleção mínima e máxima.
 */
export interface OptionGroup {
  id: number;
  name: string;
  min_selection: number;
  max_selection: number;
  options: Option[];
}

/**
 * Representa um insumo/ingrediente do estoque.
 */
export interface Ingredient {
  id: number;
  name: string;
  unit: 'kg' | 'g' | 'l' | 'ml' | 'un';
  current_stock: number;
  min_stock_alert: number;
  cost_per_unit: number;
}

/**
 * Item da Ficha Técnica (vinculação entre Produto e Ingrediente).
 */
export interface RecipeItem {
  id?: number;
  ingredient_id: number;
  quantity_required: number;
  ingredient?: Ingredient;
}

/**
 * Entidade principal de Produto.
 */
export interface Product {
  id: number;
  name: string;
  description: string | null;
  price: number; // Valor em centavos (Integer)
  image_url: string | null;
  is_available: boolean;
  track_stock: boolean;
  stock_quantity: number;
  station: 'kitchen' | 'bar' | 'dessert' | 'other';
  tags: string[];
  short_code?: string;
  external_id?: string;
  option_groups: OptionGroup[];
  recommendations?: Product[];
  recipe_items?: RecipeItem[];
}

/**
 * Categoria de produtos (ex: "Bebidas", "Hambúrgueres").
 */
export interface Category {
  id: number;
  name: string;
  products: Product[];
}

/**
 * Resposta padrão do endpoint de carregamento de cardápio.
 */
export interface MenuResponse {
  company: Company;
  categories: Category[];
}