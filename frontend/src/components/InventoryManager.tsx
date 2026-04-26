import React, { useState, useCallback, useEffect, useRef } from "react";
import { Category, Brand, Product, DataType, Toast as ToastType } from "../types";
import { api } from "../api";
import DataResults from "./DataResults";
import Toast from "./Toast";
import "./InventoryManager.scss";

type NavSection = "browse" | "categories" | "products" | "brands";

const NAV_ITEMS: { key: NavSection; label: string; icon: string }[] = [
  { key: "browse", label: "Browse & Filter", icon: "" },
  { key: "categories", label: "Categories", icon: "" },
  { key: "products", label: "Products", icon: "" },
  { key: "brands", label: "Brands", icon: "" },
];

const InventoryManager: React.FC = () => {
  const [activeSection, setActiveSection] = useState<NavSection>("browse");
  const [toasts, setToasts] = useState<ToastType[]>([]);
  const toastIdRef = useRef(0);

  // Shared data for dropdowns
  const [categories, setCategories] = useState<Category[]>([]);
  const [brands, setBrands] = useState<Brand[]>([]);
  const [allProducts, setAllProducts] = useState<Product[]>([]);

  // Results panel
  const [results, setResults] = useState<Category[] | Brand[] | Product[]>([]);
  const [resultType, setResultType] = useState<DataType>("product");
  const [resultLoading, setResultLoading] = useState(false);

  const addToast = useCallback((message: string, isError = false) => {
    const id = ++toastIdRef.current;
    setToasts(prev => [...prev, { id, message, type: isError ? "error" : "success" }]);
  }, []);

  const removeToast = useCallback((id: number) => {
    setToasts(prev => prev.filter(t => t.id !== id));
  }, []);

  const refreshDropdowns = useCallback(async () => {
    try {
      const [cats, brnds, prods] = await Promise.all([
        api.getCategories(),
        api.getBrands(),
        api.getAllProducts(),
      ]);
      setCategories(cats || []);
      setBrands(brnds || []);
      setAllProducts(prods || []);
    } catch (e) {
      console.error("Failed to load dropdown data", e);
    }
  }, []);

  useEffect(() => {
    refreshDropdowns();
  }, [refreshDropdowns]);

  const showResults = async (
    fetcher: () => Promise<any>,
    type: DataType,
    label: string
  ) => {
    setResultLoading(true);
    try {
      const data = await fetcher();
      setResults(data || []);
      setResultType(type);
    } catch (e: any) {
      addToast(e.message, true);
    } finally {
      setResultLoading(false);
    }
  };

  const refreshResults = useCallback(() => {
    if (resultType === "category") showResults(api.getCategories, "category", "categories");
    else if (resultType === "brand") showResults(api.getBrands, "brand", "brands");
    else showResults(api.getAllProducts, "product", "products");
    refreshDropdowns();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [resultType, refreshDropdowns]);

  return (
    <div className="inv">
      {/* ── Sidebar Nav ───────────────────────────────────── */}
      <aside className="inv__sidebar">
        <div className="inv__sidebar-brand">
          <span className="inv__sidebar-title">Inventory</span>
        </div>
        <nav className="inv__nav">
          {NAV_ITEMS.map(item => (
            <button
              key={item.key}
              className={`inv__nav-item ${activeSection === item.key ? "inv__nav-item--active" : ""}`}
              onClick={() => setActiveSection(item.key)}
            >
              <span>{item.label}</span>
            </button>
          ))}
        </nav>
        {/* <div className="inv__sidebar-footer">
          <div className="inv__status-dot" />
          <span>Connected</span>
        </div> */}
      </aside>

      {/* ── Main Content ──────────────────────────────────── */}
      <div className="inv__main">
        <div className="inv__content">
          {activeSection === "browse" && (
            <BrowseSection
              categories={categories}
              products={allProducts}
              onShow={showResults}
              onToast={addToast}
              refreshDropdowns={refreshDropdowns}
            />
          )}
          {activeSection === "categories" && (
            <CategoriesSection
              onShow={showResults}
              onToast={addToast}
              refreshDropdowns={refreshDropdowns}
            />
          )}
          {activeSection === "products" && (
            <ProductsSection
              categories={categories}
              brands={brands}
              products={allProducts}
              onShow={showResults}
              onToast={addToast}
              refreshDropdowns={refreshDropdowns}
            />
          )}
          {activeSection === "brands" && (
            <BrandsSection
              onShow={showResults}
              onToast={addToast}
              refreshDropdowns={refreshDropdowns}
            />
          )}
        </div>

        {/* ── Results Panel ───────────────────────────────── */}
        <div className="inv__results">
          <div className="inv__results-header">
            <h2 className="inv__results-title">Results</h2>
            {results.length > 0 && (
              <span className="inv__results-count">{results.length} items</span>
            )}
            {results.length > 0 && (
              <button className="btn btn--ghost btn--sm" onClick={refreshResults}>
                ↻ Refresh
              </button>
            )}
          </div>
          {resultLoading ? (
            <div className="inv__loading">
              <div className="inv__spinner" />
              <p>Loading…</p>
            </div>
          ) : (
            <DataResults
              items={results}
              type={resultType}
              onRefresh={refreshResults}
              onToast={addToast}
            />
          )}
        </div>
      </div>

      <Toast toasts={toasts} removeToast={removeToast} />
    </div>
  );
};

// ─── Browse Section ────────────────────────────────────────────────────────────
const BrowseSection: React.FC<{
  categories: Category[];
  products: Product[];
  onShow: (fetcher: () => Promise<any>, type: DataType, label: string) => void;
  onToast: (msg: string, isError?: boolean) => void;
  refreshDropdowns: () => void;
}> = ({ categories, products, onShow, onToast, refreshDropdowns }) => {
  const [filterCatId, setFilterCatId] = useState("");

  return (
    <div className="inv__section">
      <h1 className="inv__section-title">Browse & Filter</h1>
      <p className="inv__section-desc">Quickly fetch and view all data or filter by category.</p>

      <div className="form-card">
        <h3 className="form-card__title">Quick Fetch</h3>
        <div className="btn-group">
          <button className="btn btn--primary" onClick={() => onShow(api.getCategories, "category", "categories")}>
            All Categories
          </button>
          <button className="btn btn--primary" onClick={() => onShow(api.getAllProducts, "product", "products")}>
            All Products
          </button>
          <button className="btn btn--primary" onClick={() => onShow(api.getBrands, "brand", "brands")}>
            All Brands
          </button>
        </div>
      </div>

      <div className="form-card">
        <h3 className="form-card__title">Filter by Category</h3>
        <div className="form-row">
          <select
            id="browse-filter-cat"
            value={filterCatId}
            onChange={e => setFilterCatId(e.target.value)}
          >
            <option value="">Select Category…</option>
            {categories.map(c => (
              <option key={c.id} value={c.id}>{c.name}</option>
            ))}
          </select>
          <button
            className="btn btn--secondary"
            disabled={!filterCatId}
            onClick={() => onShow(() => api.getCategoryProducts(filterCatId), "product", "products")}
          >
            Get Products
          </button>
        </div>
      </div>
    </div>
  );
};

// ─── Categories Section ────────────────────────────────────────────────────────
const CategoriesSection: React.FC<{
  onShow: (fetcher: () => Promise<any>, type: DataType, label: string) => void;
  onToast: (msg: string, isError?: boolean) => void;
  refreshDropdowns: () => void;
}> = ({ onShow, onToast, refreshDropdowns }) => {
  const [name, setName] = useState("");
  const [desc, setDesc] = useState("");
  const [busy, setBusy] = useState(false);

  const handleAdd = async () => {
    if (!name.trim() || !desc.trim()) { onToast("Please fill all fields", true); return; }
    setBusy(true);
    try {
      await api.createCategory(name.trim(), desc.trim());
      onToast("Category added successfully");
      setName(""); setDesc("");
      refreshDropdowns();
      onShow(api.getCategories, "category", "categories");
    } catch (e: any) { onToast(e.message, true); }
    finally { setBusy(false); }
  };

  return (
    <div className="inv__section">
      <h1 className="inv__section-title">Categories</h1>
      <p className="inv__section-desc">Create and manage product categories.</p>

      <div className="form-card">
        <h3 className="form-card__title">Add New Category</h3>
        <div className="form-field">
          <label htmlFor="cat-name">Category Name</label>
          <input id="cat-name" type="text" placeholder="e.g. Electronics" value={name} onChange={e => setName(e.target.value)} />
        </div>
        <div className="form-field">
          <label htmlFor="cat-desc">Description</label>
          <input id="cat-desc" type="text" placeholder="Short description…" value={desc} onChange={e => setDesc(e.target.value)} />
        </div>
        <button className="btn btn--primary" onClick={handleAdd} disabled={busy}>
          {busy ? "Adding…" : "＋ Add Category"}
        </button>
      </div>

      <div className="form-card">
        <h3 className="form-card__title">View Categories</h3>
        <button className="btn btn--secondary" onClick={() => onShow(api.getCategories, "category", "categories")}>
          Load All Categories
        </button>
      </div>
    </div>
  );
};

// ─── Products Section ──────────────────────────────────────────────────────────
const ProductsSection: React.FC<{
  categories: Category[];
  brands: Brand[];
  products: Product[];
  onShow: (fetcher: () => Promise<any>, type: DataType, label: string) => void;
  onToast: (msg: string, isError?: boolean) => void;
  refreshDropdowns: () => void;
}> = ({ categories, brands, products, onShow, onToast, refreshDropdowns }) => {
  // Create & Assign
  const [newProdCat, setNewProdCat] = useState("");
  const [newProdName, setNewProdName] = useState("");
  const [newProdBrand, setNewProdBrand] = useState("");
  const [createBusy, setCreateBusy] = useState(false);

  // Assign Existing
  const [assignCat, setAssignCat] = useState("");
  const [assignProd, setAssignProd] = useState("");
  const [assignBusy, setAssignBusy] = useState(false);

  // Remove
  const [remCat, setRemCat] = useState("");
  const [remProd, setRemProd] = useState("");
  const [remBusy, setRemBusy] = useState(false);

  const handleCreate = async () => {
    if (!newProdCat || !newProdName.trim() || !newProdBrand) { onToast("Please fill all fields", true); return; }
    setCreateBusy(true);
    try {
      await api.createProduct(newProdCat, newProdName.trim(), newProdBrand);
      onToast("Product created and assigned");
      setNewProdCat(""); setNewProdName(""); setNewProdBrand("");
      refreshDropdowns();
      onShow(api.getAllProducts, "product", "products");
    } catch (e: any) { onToast(e.message, true); }
    finally { setCreateBusy(false); }
  };

  const handleAssign = async () => {
    if (!assignCat || !assignProd) { onToast("Please select both fields", true); return; }
    setAssignBusy(true);
    try {
      await api.assignProduct(assignCat, assignProd);
      onToast("Product assigned to category");
      setAssignCat(""); setAssignProd("");
    } catch (e: any) { onToast(e.message, true); }
    finally { setAssignBusy(false); }
  };

  const handleRemove = async () => {
    if (!remCat || !remProd) { onToast("Please select both fields", true); return; }
    setRemBusy(true);
    try {
      await api.removeFromCategory(remCat, remProd);
      onToast("Product removed from category");
      setRemCat(""); setRemProd("");
    } catch (e: any) { onToast(e.message, true); }
    finally { setRemBusy(false); }
  };

  return (
    <div className="inv__section">
      <h1 className="inv__section-title">Products</h1>
      <p className="inv__section-desc">Create products, assign them to categories, or remove them.</p>

      <div className="form-card">
        <h3 className="form-card__title">Create & Assign Product</h3>
        <div className="form-field">
          <label>Category</label>
          <select value={newProdCat} onChange={e => setNewProdCat(e.target.value)}>
            <option value="">Select Category…</option>
            {categories.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
          </select>
        </div>
        <div className="form-field">
          <label htmlFor="new-prod-name">Product Name</label>
          <input id="new-prod-name" type="text" placeholder="e.g. MacBook Pro" value={newProdName} onChange={e => setNewProdName(e.target.value)} />
        </div>
        <div className="form-field">
          <label>Brand</label>
          <select value={newProdBrand} onChange={e => setNewProdBrand(e.target.value)}>
            <option value="">Select Brand…</option>
            {brands.map(b => <option key={b.id} value={b.id}>{b.name}</option>)}
          </select>
        </div>
        <button className="btn btn--primary" onClick={handleCreate} disabled={createBusy}>
          {createBusy ? "Creating…" : "＋ Create & Assign"}
        </button>
      </div>

      <div className="form-card">
        <h3 className="form-card__title">Assign Existing Product</h3>
        <div className="form-field">
          <label>Category</label>
          <select value={assignCat} onChange={e => setAssignCat(e.target.value)}>
            <option value="">Select Category…</option>
            {categories.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
          </select>
        </div>
        <div className="form-field">
          <label>Product</label>
          <select value={assignProd} onChange={e => setAssignProd(e.target.value)}>
            <option value="">Select Product…</option>
            {products.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
          </select>
        </div>
        <button className="btn btn--secondary" onClick={handleAssign} disabled={assignBusy}>
          {assignBusy ? "Assigning…" : "↳ Assign"}
        </button>
      </div>

      <div className="form-card form-card--danger">
        <h3 className="form-card__title">Remove Product from Category</h3>
        <div className="form-field">
          <label>Category</label>
          <select value={remCat} onChange={e => setRemCat(e.target.value)}>
            <option value="">Select Category…</option>
            {categories.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
          </select>
        </div>
        <div className="form-field">
          <label>Product</label>
          <select value={remProd} onChange={e => setRemProd(e.target.value)}>
            <option value="">Select Product…</option>
            {products.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
          </select>
        </div>
        <button className="btn btn--danger" onClick={handleRemove} disabled={remBusy}>
          {remBusy ? "Removing…" : "Remove"}
        </button>
      </div>

      <div className="form-card">
        <h3 className="form-card__title">View Products</h3>
        <button className="btn btn--secondary" onClick={() => onShow(api.getAllProducts, "product", "products")}>
          Load All Products
        </button>
      </div>
    </div>
  );
};

// ─── Brands Section ────────────────────────────────────────────────────────────
const BrandsSection: React.FC<{
  onShow: (fetcher: () => Promise<any>, type: DataType, label: string) => void;
  onToast: (msg: string, isError?: boolean) => void;
  refreshDropdowns: () => void;
}> = ({ onShow, onToast, refreshDropdowns }) => {
  const [name, setName] = useState("");
  const [desc, setDesc] = useState("");
  const [busy, setBusy] = useState(false);

  const handleAdd = async () => {
    if (!name.trim() || !desc.trim()) { onToast("Please fill all brand fields", true); return; }
    setBusy(true);
    try {
      await api.createBrand(name.trim(), desc.trim());
      onToast("Brand added successfully");
      setName(""); setDesc("");
      refreshDropdowns();
      onShow(api.getBrands, "brand", "brands");
    } catch (e: any) { onToast(e.message, true); }
    finally { setBusy(false); }
  };

  return (
    <div className="inv__section">
      <h1 className="inv__section-title">Brands</h1>
      <p className="inv__section-desc">Create and manage product brands.</p>

      <div className="form-card">
        <h3 className="form-card__title">Add New Brand</h3>
        <div className="form-field">
          <label htmlFor="brand-name">Brand Name</label>
          <input id="brand-name" type="text" placeholder="e.g. Apple" value={name} onChange={e => setName(e.target.value)} />
        </div>
        <div className="form-field">
          <label htmlFor="brand-desc">Description</label>
          <input id="brand-desc" type="text" placeholder="Short description…" value={desc} onChange={e => setDesc(e.target.value)} />
        </div>
        <button className="btn btn--primary" onClick={handleAdd} disabled={busy}>
          {busy ? "Adding…" : "＋ Add Brand"}
        </button>
      </div>

      <div className="form-card">
        <h3 className="form-card__title">View Brands</h3>
        <button className="btn btn--secondary" onClick={() => onShow(api.getBrands, "brand", "brands")}>
          Load All Brands
        </button>
      </div>
    </div>
  );
};

export default InventoryManager;
