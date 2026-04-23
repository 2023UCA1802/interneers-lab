import React, { useEffect, useState, useCallback, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { api } from "../api";
import { Category, Product, Toast as ToastType } from "../types";
import Toast from "./Toast";
import { ProductList } from "./ProductList";
import "./ProductPage.scss"; // reuse product page styling

const CategoryPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [category, setCategory] = useState<Category | null>(null);
  const [products, setProducts] = useState<Product[]>([]);

  const [loading, setLoading] = useState(true);

  const [editName, setEditName] = useState("");
  const [editDesc, setEditDesc] = useState("");
  const [isEditing, setIsEditing] = useState(false);
  const [saving, setSaving] = useState(false);

  const [toasts, setToasts] = useState<ToastType[]>([]);
  const toastIdRef = useRef(0);

  const addToast = useCallback((message: string, isError = false) => {
    const toastId = ++toastIdRef.current;
    setToasts((prev) => [
      ...prev,
      { id: toastId, message, type: isError ? "error" : "success" },
    ]);
  }, []);

  const removeToast = useCallback((toastId: number) => {
    setToasts((prev) => prev.filter((t) => t.id !== toastId));
  }, []);

  const loadData = useCallback(async () => {
    if (!id) return;
    setLoading(true);
    try {
      const [catRes, prodRes] = await Promise.all([
        api.getCategory(id),
        api.getCategoryProducts(id),
      ]);
      setCategory(catRes);
      setEditName(catRes.name);
      setEditDesc(catRes.description || "");
      setProducts(prodRes || []);
    } catch (e: any) {
      addToast(e.message || "Failed to load category", true);
    } finally {
      setLoading(false);
    }
  }, [id, addToast]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleSave = async () => {
    if (!id || !editName.trim()) {
      addToast("Category name cannot be empty", true);
      return;
    }
    setSaving(true);
    try {
      await api.updateCategory(id, editName.trim(), editDesc.trim());
      addToast("Category updated");
      setIsEditing(false);
      loadData();
    } catch (e: any) {
      addToast(e.message || "Failed to update category", true);
    } finally {
      setSaving(false);
    }
  };

  const handleRemoveProduct = async (prodId: string | number) => {
    if (!id) return;
    if (!window.confirm("Remove product from this category?")) return;
    try {
      await api.removeFromCategory(id, prodId);
      addToast("Product removed from category");
      loadData();
    } catch (e: any) {
      addToast(e.message || "Failed to remove product", true);
    }
  };

  if (loading) {
    return (
      <div className="product-page">
        <div className="product-page__loading">
          <div
            className="inv__spinner"
            style={{ margin: "0 auto 15px", display: "block" }}
          />
          Loading category details...
        </div>
      </div>
    );
  }

  if (!category) {
    return (
      <div className="product-page">
        <button className="btn btn--secondary" onClick={() => navigate("/")}>
          &larr; Back to Inventory
        </button>
        <div className="product-page__error">Category not found.</div>
        <Toast toasts={toasts} removeToast={removeToast} />
      </div>
    );
  }

  return (
    <div className="product-page">
      <header className="product-page__header">
        <button className="btn btn--secondary" onClick={() => navigate("/")}>
          &larr; Back to Inventory
        </button>
        <h1 className="product-page__title">Category Details</h1>
      </header>

      <div className="product-page__content">
        <div className="product-card">
          <div className="product-card__header">
            <h3>General Information</h3>
            {!isEditing ? (
              <button
                className="btn btn--ghost"
                onClick={() => setIsEditing(true)}
              >
                Edit
              </button>
            ) : (
              <div className="product-card__actions">
                <button
                  className="btn btn--ghost"
                  onClick={() => {
                    setIsEditing(false);
                    setEditName(category.name);
                    setEditDesc(category.description || "");
                  }}
                  disabled={saving}
                >
                  Cancel
                </button>
                <button
                  className="btn btn--primary"
                  onClick={handleSave}
                  disabled={saving}
                >
                  {saving ? "Saving..." : "Save"}
                </button>
              </div>
            )}
          </div>
          <div className="product-card__body">
            <div className="form-field">
              <label>ID</label>
              <div className="form-field__value">{category.id}</div>
            </div>
            <div className="form-field">
              <label>Name</label>
              {!isEditing ? (
                <div className="form-field__value font-medium">
                  {category.name}
                </div>
              ) : (
                <input
                  type="text"
                  value={editName}
                  onChange={(e) => setEditName(e.target.value)}
                  className="form-field__input"
                  disabled={saving}
                />
              )}
            </div>
            <div className="form-field">
              <label>Description</label>
              {!isEditing ? (
                <div className="form-field__value">
                  {category.description || "N/A"}
                </div>
              ) : (
                <input
                  type="text"
                  value={editDesc}
                  onChange={(e) => setEditDesc(e.target.value)}
                  className="form-field__input"
                  disabled={saving}
                />
              )}
            </div>
          </div>
        </div>

        <div className="product-card">
          <div className="product-card__header">
            <h3>Products ({products.length})</h3>
          </div>
          <div className="product-card__body">
            <ProductList products={products} loading={loading} />
          </div>
        </div>
      </div>

      <Toast toasts={toasts} removeToast={removeToast} />
    </div>
  );
};

export default CategoryPage;
