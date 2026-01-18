import { Company } from './company';

/**
 * MesaFlow OS - Domain: Menu, Products & Inventory
 */
export interface Option {
  id: number;
  name: string;
  price: number;
  is_available: boolean;
}

export interface OptionGroup {
  id: number;
  name: string;
  min_selection: number;
  max_selection: number;
  options: Option[];
}

export interface Ingredient {
  id: number;
  name: string;
  unit: 'kg' | 'g' | 'l' | 'ml' | 'un';
  current_stock: number;
  min_stock_alert: number;
  cost_per_unit: number;
}

export interface RecipeItem {
  id?: number;
  ingredient_id: number;
  quantity_required: number;
  ingredient?: Ingredient;
}

export interface Product {
  id: number;
  name: string;
  description: string | null;
  price: number;
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

export interface Category {
  id: number;
  name: string;
  products: Product[];
}

export interface MenuResponse {
  company: Company;
  categories: Category[];
}

