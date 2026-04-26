import React, { useState } from "react";
import { Category, Brand, Product, DataType } from "../types";
import { api } from "../api";
import "./DataResults.scss";

interface DataResultsProps {
  items: Category[] | Brand[] | Product[];
  type: DataType;
  onRefresh: () => void;
  onToast: (msg: string, isError?: boolean) => void;
}

const DataResults: React.FC<DataResultsProps> = ({
  items,
  type,
  onRefresh,
  onToast,
}) => {
  if (!items || items.length === 0) {
    return (
      <div className="empty-state">
        <div className="empty-state__icon" />
        <p>No {type}s found. Try fetching or creating one.</p>
      </div>
    );
  }

  return (
    <div className="results-grid">
      {(items as any[]).map((item) => {
        if (type === "category")
          return (
            <CategoryCard
              key={item.id}
              category={item}
              onRefresh={onRefresh}
              onToast={onToast}
            />
          );
        if (type === "brand")
          return (
            <BrandCard
              key={item.id}
              brand={item}
              onRefresh={onRefresh}
              onToast={onToast}
            />
          );
        return (
          <ProductCard
            key={item.id}
            product={item}
            onRefresh={onRefresh}
            onToast={onToast}
          />
        );
      })}
    </div>
  );
};

// ─── Category Card ─────────────────────────────────────────────────────────────
const CategoryCard: React.FC<{
  category: Category;
  onRefresh: () => void;
  onToast: (msg: string, isError?: boolean) => void;
}> = ({ category, onRefresh, onToast }) => {
  const [editing, setEditing] = useState(false);
  const [name, setName] = useState(category.name);
  const [desc, setDesc] = useState(category.description || "");
  const [busy, setBusy] = useState(false);

  const handleSave = async () => {
    if (!name.trim()) {
      onToast("Name is required", true);
      return;
    }
    setBusy(true);
    try {
      await api.updateCategory(category.id, name.trim(), desc.trim());
      onToast("Category updated successfully");
      setEditing(false);
      onRefresh();
    } catch (e: any) {
      onToast(e.message, true);
    } finally {
      setBusy(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm(`Delete category "${category.name}"?`)) return;
    setBusy(true);
    try {
      await api.deleteCategory(category.id);
      onToast("Category deleted");
      onRefresh();
    } catch (e: any) {
      onToast(e.message, true);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div
      className={`result-card result-card--category ${editing ? "result-card--editing" : ""}`}
    >
      <div className="result-card__badge">Category</div>
      {!editing ? (
        <div className="result-card__view">
          <h3 className="result-card__name">{category.name}</h3>
          <p className="result-card__meta">
            {category.description || "No description"}
          </p>
          <p className="result-card__id">ID: {category.id}</p>
        </div>
      ) : (
        <div className="result-card__edit">
          <label>Name</label>
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Category name"
          />
          <label>Description</label>
          <input
            value={desc}
            onChange={(e) => setDesc(e.target.value)}
            placeholder="Description"
          />
        </div>
      )}
      <div className="result-card__actions">
        {!editing ? (
          <>
            <button
              className="btn btn--secondary"
              onClick={() => setEditing(true)}
              disabled={busy}
            >
              Edit
            </button>
            <button
              className="btn btn--danger"
              onClick={handleDelete}
              disabled={busy}
            >
              Delete
            </button>
          </>
        ) : (
          <>
            <button
              className="btn btn--primary"
              onClick={handleSave}
              disabled={busy}
            >
              {busy ? "Saving…" : "Save"}
            </button>
            <button
              className="btn btn--ghost"
              onClick={() => {
                setEditing(false);
                setName(category.name);
                setDesc(category.description || "");
              }}
              disabled={busy}
            >
              Cancel
            </button>
          </>
        )}
      </div>
    </div>
  );
};

// ─── Brand Card ─────────────────────────────────────────────────────────────────
const BrandCard: React.FC<{
  brand: Brand;
  onRefresh: () => void;
  onToast: (msg: string, isError?: boolean) => void;
}> = ({ brand, onRefresh, onToast }) => {
  const [editing, setEditing] = useState(false);
  const [name, setName] = useState(brand.name);
  const [desc, setDesc] = useState(brand.description || "");
  const [busy, setBusy] = useState(false);

  const handleSave = async () => {
    if (!name.trim()) {
      onToast("Name is required", true);
      return;
    }
    setBusy(true);
    try {
      await api.updateBrand(brand.id, name.trim(), desc.trim());
      onToast("Brand updated successfully");
      setEditing(false);
      onRefresh();
    } catch (e: any) {
      onToast(e.message, true);
    } finally {
      setBusy(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm(`Delete brand "${brand.name}"?`)) return;
    setBusy(true);
    try {
      await api.deleteBrand(brand.id);
      onToast("Brand deleted");
      onRefresh();
    } catch (e: any) {
      onToast(e.message, true);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div
      className={`result-card result-card--brand ${editing ? "result-card--editing" : ""}`}
    >
      <div className="result-card__badge">Brand</div>
      {!editing ? (
        <div className="result-card__view">
          <h3 className="result-card__name">{brand.name}</h3>
          <p className="result-card__meta">
            {brand.description || "No description"}
          </p>
          <p className="result-card__id">ID: {brand.id}</p>
        </div>
      ) : (
        <div className="result-card__edit">
          <label>Name</label>
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Brand name"
          />
          <label>Description</label>
          <input
            value={desc}
            onChange={(e) => setDesc(e.target.value)}
            placeholder="Description"
          />
        </div>
      )}
      <div className="result-card__actions">
        {!editing ? (
          <>
            <button
              className="btn btn--secondary"
              onClick={() => setEditing(true)}
              disabled={busy}
            >
              Edit
            </button>
            <button
              className="btn btn--danger"
              onClick={handleDelete}
              disabled={busy}
            >
              Delete
            </button>
          </>
        ) : (
          <>
            <button
              className="btn btn--primary"
              onClick={handleSave}
              disabled={busy}
            >
              {busy ? "Saving…" : "Save"}
            </button>
            <button
              className="btn btn--ghost"
              onClick={() => {
                setEditing(false);
                setName(brand.name);
                setDesc(brand.description || "");
              }}
              disabled={busy}
            >
              Cancel
            </button>
          </>
        )}
      </div>
    </div>
  );
};

// ─── Product Card ───────────────────────────────────────────────────────────────
const ProductCard: React.FC<{
  product: Product;
  onRefresh: () => void;
  onToast: (msg: string, isError?: boolean) => void;
}> = ({ product, onRefresh, onToast }) => {
  const [editing, setEditing] = useState(false);
  const [name, setName] = useState(product.name);
  const [busy, setBusy] = useState(false);

  const handleSave = async () => {
    if (!name.trim()) {
      onToast("Name is required", true);
      return;
    }
    setBusy(true);
    try {
      await api.updateProduct(product.id, name.trim());
      onToast("Product updated successfully");
      setEditing(false);
      onRefresh();
    } catch (e: any) {
      onToast(e.message, true);
    } finally {
      setBusy(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm(`Delete product "${product.name}"?`)) return;
    setBusy(true);
    try {
      await api.deleteProduct(product.id);
      onToast("Product deleted");
      onRefresh();
    } catch (e: any) {
      onToast(e.message, true);
    } finally {
      setBusy(false);
    }
  };

  const cats = Array.isArray(product.categories)
    ? product.categories.join(", ")
    : product.category || "None";

  return (
    <div
      className={`result-card result-card--product ${editing ? "result-card--editing" : ""}`}
    >
      <div className="result-card__badge">Product</div>
      {!editing ? (
        <div className="result-card__view">
          <h3 className="result-card__name">{product.name}</h3>
          <p className="result-card__meta">Brand: {product.brand || "N/A"}</p>
          <p className="result-card__meta">Categories: {cats}</p>
          <p className="result-card__id">ID: {product.id}</p>
        </div>
      ) : (
        <div className="result-card__edit">
          <label>Name</label>
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Product name"
          />
        </div>
      )}
      <div className="result-card__actions">
        {!editing ? (
          <>
            <button
              className="btn btn--secondary"
              onClick={() => setEditing(true)}
              disabled={busy}
            >
              Edit
            </button>
            <button
              className="btn btn--danger"
              onClick={handleDelete}
              disabled={busy}
            >
              Delete
            </button>
          </>
        ) : (
          <>
            <button
              className="btn btn--primary"
              onClick={handleSave}
              disabled={busy}
            >
              {busy ? "Saving…" : "Save"}
            </button>
            <button
              className="btn btn--ghost"
              onClick={() => {
                setEditing(false);
                setName(product.name);
              }}
              disabled={busy}
            >
              Cancel
            </button>
          </>
        )}
      </div>
    </div>
  );
};

export default DataResults;
