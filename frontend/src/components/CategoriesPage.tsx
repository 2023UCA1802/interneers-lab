import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api } from "../api";
import { Category } from "../types";
import "./ProductPage.scss"; // reuse styling

const CategoriesPage: React.FC = () => {
  const navigate = useNavigate();
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const data = await api.getCategories();
        setCategories(data || []);
      } catch (err: any) {
        setError(err.message || "Failed to load categories");
      } finally {
        setLoading(false);
      }
    };
    fetchCategories();
  }, []);

  if (loading) {
    return (
      <div className="product-page">
        <div className="product-page__loading">
          <div
            className="inv__spinner"
            style={{ margin: "0 auto 15px", display: "block" }}
          />
          Loading categories...
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="product-page">
        <button className="btn btn--secondary" onClick={() => navigate("/")}>
          &larr; Back to Inventory
        </button>
        <div className="product-page__error">Error: {error}</div>
      </div>
    );
  }

  return (
    <div className="product-page">
      <header className="product-page__header">
        <button className="btn btn--secondary" onClick={() => navigate("/")}>
          &larr; Back to Inventory
        </button>
        <h1 className="product-page__title">Product Categories</h1>
      </header>

      <div className="product-page__content">
        <div className="categories-grid">
          {categories.length === 0 ? (
            <div className="empty-state">No categories found.</div>
          ) : (
            categories.map((cat) => (
              <div key={cat.id} className="category-card-styled">
                <div className="category-card-styled__header">
                  <h3>{cat.name}</h3>
                  <span className="category-card-styled__id">
                    #{String(cat.id).slice(-4)}
                  </span>
                </div>
                <p className="category-card-styled__desc">
                  {cat.description ||
                    "No description provided for this category."}
                </p>
                <div className="category-card-styled__footer">
                  <Link
                    to={`/categories/${cat.id}`}
                    className="btn btn--primary btn--sm"
                    style={{ width: "100%" }}
                  >
                    View Details &rarr;
                  </Link>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default CategoriesPage;
