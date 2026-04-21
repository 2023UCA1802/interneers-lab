export interface Product {
  id: string | number;
  name: string;
  brand?: string;
  brand_id?: string | number;
  categories?: string[];
  description?: string;
  price?: number;
  category?: string;
  stock?: number;
}

export interface Category {
  id: string | number;
  name: string;
  description?: string;
}

export interface Brand {
  id: string | number;
  name: string;
  description?: string;
}

export type DataType = "category" | "product" | "brand";
export type ToastType = "success" | "error";

export interface Toast {
  id: number;
  message: string;
  type: ToastType;
}
