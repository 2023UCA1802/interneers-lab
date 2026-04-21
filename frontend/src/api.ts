// Centralized API service for the Inventory Manager
const API_BASE = "http://127.0.0.1:8001";

export const api = {
  // Categories
  getCategories: () => fetch(`${API_BASE}/categories/`).then(handleResponse),
  createCategory: (name: string, description: string) =>
    fetch(`${API_BASE}/categories/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, description }),
    }).then(handleResponse),
  updateCategory: (id: string | number, name: string, description: string) =>
    fetch(`${API_BASE}/categories/${id}/`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, description }),
    }).then(handleResponse),
  deleteCategory: (id: string | number) =>
    fetch(`${API_BASE}/categories/${id}/`, { method: "DELETE" }).then(
      () => handleResponse,
    ),

  // Products
  getAllProducts: () =>
    fetch(`${API_BASE}/categories/products/`).then(handleResponse),
  getCategoryProducts: (catId: string | number) =>
    fetch(`${API_BASE}/categories/${catId}/products/`).then(handleResponse),
  createProduct: (
    catId: string | number,
    name: string,
    brandId: string | number,
  ) =>
    fetch(`${API_BASE}/categories/${catId}/products/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, brand_id: brandId }),
    }).then(handleResponse),
  updateProduct: (id: string | number, name: string) =>
    fetch(`${API_BASE}/categories/products/${id}/`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    }).then(handleResponse),
  deleteProduct: (id: string | number) =>
    fetch(`${API_BASE}/categories/products/${id}/`, { method: "DELETE" }).then(
      handleResponse,
    ),
  assignProduct: (catId: string | number, prodId: string | number) =>
    fetch(`${API_BASE}/categories/${catId}/products/${prodId}/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    }).then(handleResponse),
  removeFromCategory: (catId: string | number, prodId: string | number) =>
    fetch(`${API_BASE}/categories/${catId}/products/${prodId}/`, {
      method: "DELETE",
    }).then(handleResponse),

  // Brands
  getBrands: () => fetch(`${API_BASE}/brands/`).then(handleResponse),
  createBrand: (name: string, description: string) =>
    fetch(`${API_BASE}/brands/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, description }),
    }).then(handleResponse),
  updateBrand: (id: string | number, name: string, description: string) =>
    fetch(`${API_BASE}/brands/${id}/`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, description }),
    }).then(handleResponse),
  deleteBrand: (id: string | number) =>
    fetch(`${API_BASE}/brands/${id}/`, { method: "DELETE" }).then(
      handleResponse,
    ),
};

async function handleResponse(response: Response) {
  if (response.status === 204) return null;
  const data = await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error(
      data?.error || data?.detail || `Request failed: ${response.status}`,
    );
  }
  return data;
}
