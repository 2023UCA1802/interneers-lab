// ==========================
// CONFIG
// ==========================
const API_BASE = "http://127.0.0.1:8001/categories";

// ==========================
// INIT
// ==========================
document.addEventListener("DOMContentLoaded", () => {
    fetchCategories();
});

// ==========================
// API CALLS
// ==========================

// GET CATEGORIES
async function fetchCategories() {
    try {
        const response = await fetch(`${API_BASE}/`);
        if (!response.ok) throw new Error("Failed to fetch categories");
        
        const data = await response.json();
        console.log("Categories:", data);
        renderDataList(data, "category");
    } catch (error) {
        console.error("Fetch Error:", error);
        showMessage("Error fetching categories", true);
    }
}

// GET PRODUCTS
async function fetchProducts() {
    try {
        const response = await fetch(`${API_BASE}/products/`);
        if (!response.ok) throw new Error("Failed to fetch products");

        const data = await response.json();
        console.log("Products:", data);
        renderDataList(data, "product");
    } catch (error) {
        console.error("Fetch Error:", error);
        showMessage("Error fetching products", true);
    }
}

// GET PRODUCTS IN A CATEGORY
async function fetchCategoryProducts() {
    const categoryId = document.getElementById("filter_cat_id").value.trim();
    if (!categoryId) {
        showMessage("Please enter a Category ID", true);
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/${categoryId}/products/`);
        if (!response.ok) throw new Error("Failed to fetch products for category");

        const data = await response.json();
        console.log("Category Products:", data);
        renderDataList(data, "product");
    } catch (error) {
        console.error("Fetch Error:", error);
        showMessage("Error fetching category products", true);
    }
}

// ADD CATEGORY
async function addCategory() {
    const nameInput = document.getElementById("cat_name");
    const descInput = document.getElementById("cat_desc");

    const name = nameInput.value.trim();
    const description = descInput.value.trim();

    if (!name || !description) {
        showMessage("Please fill all category fields", true);
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, description })
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.error || "Failed to add category");

        console.log("Added Category:", data);
        showMessage("Category added successfully");
        nameInput.value = "";
        descInput.value = "";
        fetchCategories();
    } catch (error) {
        console.error("Add Error:", error);
        showMessage(error.message, true);
    }
}

// ADD PRODUCT TO CATEGORY
async function addProductToCategory() {
    const catIdInput = document.getElementById("assign_cat_id");
    const prodIdInput = document.getElementById("assign_prod_id");

    const category_id = catIdInput.value.trim();
    const product_id = prodIdInput.value.trim();

    if (!category_id || !product_id) {
        showMessage("Please fill all fields", true);
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/${category_id}/products/${product_id}/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" }
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.error || "Failed to add product to category");

        console.log("Assigned:", data);
        showMessage("Product added to category successfully");
        catIdInput.value = "";
        prodIdInput.value = "";
    } catch (error) {
        console.error("Assign Error:", error);
        showMessage(error.message, true);
    }
}

// ==========================
// RENDERING
// ==========================
function renderDataList(items, type) {
    const container = document.getElementById("data-container");

    if (!items || items.length === 0) {
        container.innerHTML = `<div class="empty-state">No ${type}s found</div>`;
        return;
    }

    if (type === "category") {
        container.innerHTML = items.map(categoryTemplate).join("");
    } else {
        container.innerHTML = items.map(productTemplate).join("");
    }
}

function categoryTemplate(category) {
    return `
        <div class="product-card">
            <h3>${escapeHTML(category.name)}</h3>
            <p><b>Description:</b> ${escapeHTML(category.description || "N/A")}</p>
            <p><b>ID:</b> ${category.id || "-"}</p>
        </div>
    `;
}

function productTemplate(product) {
    return `
        <div class="product-card">
            <h3>${escapeHTML(product.name)}</h3>
            <p><b>Brand:</b> ${escapeHTML(product.brand || "N/A")}</p>
            <p><b>ID:</b> ${product.id || "-"}</p>
            <p><b>Categories:</b> ${formatCategories(product.categories)}</p>
        </div>
    `;
}

// ==========================
// HELPERS
// ==========================

function formatCategories(categories) {
    if (!categories || categories.length === 0) return "None";
    return categories.join(", ");
}

function escapeHTML(str) {
    return str
        ? String(str).replace(/[&<>"']/g, match => ({
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#039;"
        }[match]))
        : "";
}

function showMessage(message, isError = false) {
    const msg = document.getElementById("message");
    msg.innerText = message;
    msg.style.color = isError ? "#cc0000" : "#008800";
    setTimeout(() => { msg.innerText = ""; }, 3000);
}