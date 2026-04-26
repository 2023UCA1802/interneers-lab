import React, { useEffect, useState, useCallback, useRef } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { api } from "../api";
import { Product, Category, Brand, Toast as ToastType } from "../types";
import Toast from "./Toast";
import "./ProductPage.scss";

const ProductPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [product, setProduct] = useState<Product | null>(null);
  const [categories, setCategories] = useState<Category[]>([]);
  const [brands, setBrands] = useState<Brand[]>([]);

  const [loading, setLoading] = useState(true);

  const [editName, setEditName] = useState("");
  const [isEditing, setIsEditing] = useState(false);
  const [saving, setSaving] = useState(false);

  // Moving across categories
  const [assignCat, setAssignCat] = useState("");
  const [assigning, setAssigning] = useState(false);

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
      const [prodRes, catRes, brandRes] = await Promise.all([
        api.getProduct(id),
        api.getCategories(),
        api.getBrands(),
      ]);
      setProduct(prodRes);
      setEditName(prodRes.name);
      setCategories(catRes || []);
      setBrands(brandRes || []);
    } catch (e: any) {
      addToast(e.message || "Failed to load product", true);
    } finally {
      setLoading(false);
    }
  }, [id, addToast]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleSaveName = async () => {
    if (!id || !editName.trim()) {
      addToast("Product name cannot be empty", true);
      return;
    }
    setSaving(true);
    try {
      await api.updateProduct(id, editName.trim());
      addToast("Product name updated");
      setIsEditing(false);
      loadData();
    } catch (e: any) {
      addToast(e.message || "Failed to update product", true);
    } finally {
      setSaving(false);
    }
  };

  const handleAssignCategory = async () => {
    if (!id || !assignCat) {
      addToast("Please select a category", true);
      return;
    }
    setAssigning(true);
    try {
      await api.assignProduct(assignCat, id);
      addToast("Product added to category");
      setAssignCat("");
      loadData();
    } catch (e: any) {
      addToast(e.message || "Failed to assign category", true);
    } finally {
      setAssigning(false);
    }
  };

  const handleRemoveCategory = async (catId: string | number) => {
    if (!id) return;
    try {
      await api.removeFromCategory(catId, id);
      addToast("Product removed from category");
      loadData();
    } catch (e: any) {
      addToast(e.message || "Failed to remove category", true);
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
          Loading product details...
        </div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="product-page">
        <button className="btn btn--secondary" onClick={() => navigate("/")}>
          &larr; Back to Inventory
        </button>
        <div className="product-page__error">Product not found.</div>
        <Toast toasts={toasts} removeToast={removeToast} />
      </div>
    );
  }

  const productCategories = product.categories || [];
  const assignedCats = categories.filter((c) =>
    productCategories.includes(String(c.id)),
  );
  const availableCats = categories.filter(
    (c) => !productCategories.includes(String(c.id)),
  );

  return (
    <div className="product-page">
      <header className="product-page__header">
        <button className="btn btn--secondary" onClick={() => navigate("/")}>
          &larr; Back to Inventory
        </button>
        <h1 className="product-page__title">Product Details</h1>
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
                    setEditName(product.name);
                  }}
                  disabled={saving}
                >
                  Cancel
                </button>
                <button
                  className="btn btn--primary"
                  onClick={handleSaveName}
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
              <div className="form-field__value">{product.id}</div>
            </div>
            <div className="form-field">
              <label>Name</label>
              {!isEditing ? (
                <div className="form-field__value font-medium">
                  {product.name}
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
              <label>Brand</label>
              <div className="form-field__value">{product.brand || "N/A"}</div>
            </div>
          </div>
        </div>

        <div className="product-card">
          <div className="product-card__header">
            <h3>Categories ({assignedCats.length})</h3>
          </div>
          <div className="product-card__body">
            <div className="category-list">
              {assignedCats.length === 0 ? (
                <p className="text-gray">Not assigned to any categories.</p>
              ) : (
                assignedCats.map((cat) => (
                  <div key={cat.id} className="category-badge">
                    <Link
                      to={`/categories/${cat.id}`}
                      className="category-badge__link"
                    >
                      {cat.name}
                    </Link>
                    <button
                      className="category-badge__remove"
                      onClick={() => handleRemoveCategory(cat.id)}
                      title="Remove from category"
                    >
                      &times;
                    </button>
                  </div>
                ))
              )}
            </div>

            <div className="assign-category">
              <h4>Assign to Category</h4>
              <div className="assign-category__row">
                <select
                  value={assignCat}
                  onChange={(e) => setAssignCat(e.target.value)}
                  className="form-field__input"
                  disabled={assigning}
                >
                  <option value="">Select a category...</option>
                  {availableCats.map((cat) => (
                    <option key={cat.id} value={String(cat.id)}>
                      {cat.name}
                    </option>
                  ))}
                </select>
                <button
                  className="btn btn--secondary"
                  onClick={handleAssignCategory}
                  disabled={!assignCat || assigning}
                >
                  {assigning ? "..." : "Add"}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <Toast toasts={toasts} removeToast={removeToast} />
    </div>
  );
};

export default ProductPage;
