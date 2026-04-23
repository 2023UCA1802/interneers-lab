import React from "react";
import { Routes, Route } from "react-router-dom";
import "./App.scss";
import InventoryManager from "./components/InventoryManager";
import ProductPage from "./components/ProductPage";
import CategoryPage from "./components/CategoryPage";
import CategoriesPage from "./components/CategoriesPage";

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<InventoryManager />} />
        <Route path="/products/:id" element={<ProductPage />} />
        <Route path="/categories" element={<CategoriesPage />} />
        <Route path="/categories/:id" element={<CategoryPage />} />
      </Routes>
    </div>
  );
}

export default App;
