import React, { useState, useEffect } from "react";
import { Product } from "../types";
import "./ProductList.scss";

interface ProductListProps {
  products?: Product[];
  loading?: boolean;
  error?: string | null;
}

export const ProductList: React.FC<ProductListProps> = (props) => {
  const [products, setProducts] = useState<Product[]>(props.products || []);
  const [loading, setLoading] = useState<boolean>(
    props.loading !== undefined ? props.loading : true,
  );
  const [error, setError] = useState<string | null>(props.error || null);
  const [expandedProductId, setExpandedProductId] = useState<string | null>(
    null,
  );

  useEffect(() => {
    if (props.products) {
      setProducts(props.products);
      if (props.loading !== undefined) setLoading(props.loading);
      if (props.error !== undefined) setError(props.error);
      return;
    }
    const fetchProducts = async () => {
      try {
        const response = await fetch(
          "http://127.0.0.1:8001/categories/products/",
        );
        if (!response.ok) {
          throw new Error("Failed to fetch products");
        }
        const data = await response.json();
        setProducts(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (!props.products) {
      fetchProducts();
    }
  }, [props.products, props.loading, props.error]);

  const toggleProduct = (
    id: string | number,
    e: React.MouseEvent | React.KeyboardEvent,
  ) => {
    e.preventDefault();
    const strId = id.toString();
    setExpandedProductId((prev) => (prev === strId ? null : strId));
  };

  if (loading) {
    return (
      <div
        style={{
          textAlign: "center",
          padding: "40px",
          fontSize: "1.2em",
          color: "#64748b",
        }}
      >
        <div
          className="inv__spinner"
          style={{ margin: "0 auto 15px", display: "block" }}
        />
        Loading products...
      </div>
    );
  }

  if (error) {
    return (
      <div
        style={{
          textAlign: "center",
          padding: "40px",
          fontSize: "1.2em",
          color: "#ef4444",
        }}
      >
        Error: {error}
      </div>
    );
  }

  return (
    <div className="product-list-container">
      <h2>Featured Products</h2>
      <div className="product-list">
        {products.map((product) => {
          const isExpanded = expandedProductId === product.id.toString();
          return (
            <div
              key={product.id}
              className={`product-item ${isExpanded ? "expanded" : ""}`}
              onClick={(e) => toggleProduct(product.id, e)}
              role="button"
              tabIndex={0}
              onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === " ") {
                  toggleProduct(product.id, e);
                }
              }}
            >
              <div className="product-header">
                <div className="product-info">
                  <span className="product-category">
                    {product.categories && product.categories.length > 0
                      ? product.categories.join(", ")
                      : product.category || "Uncategorized"}
                  </span>
                  <span className="product-name">{product.name}</span>
                </div>
                <div
                  style={{ display: "flex", alignItems: "center", gap: "15px" }}
                >
                  {product.price != null && (
                    <span className="product-price">
                      ${Number(product.price).toFixed(2)}
                    </span>
                  )}
                  <div
                    className={`expand-icon ${isExpanded ? "expanded" : ""}`}
                  >
                    <svg
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <polyline points="6 9 12 15 18 9"></polyline>
                    </svg>
                  </div>
                </div>
              </div>

              {isExpanded && (
                <div className="product-details">
                  <p className="description">
                    {product.description ||
                      "No description available for this product."}
                  </p>
                  <div className="meta-info">
                    <span>
                      <strong>Product ID:</strong> #{product.id}
                    </span>
                    <span>
                      <strong>Brand:</strong> {product.brand || "No Brand"}
                    </span>
                    {product.stock !== undefined && (
                      <span>
                        <strong>In Stock:</strong> {product.stock} units
                      </span>
                    )}
                  </div>
                </div>
              )}
            </div>
          );
        })}
        {products.length === 0 && (
          <div
            style={{ textAlign: "center", color: "#64748b", padding: "20px" }}
          >
            No products found.
          </div>
        )}
      </div>
    </div>
  );
};
