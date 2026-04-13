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
// API SERVICE
// ==========================
async function apiRequest(url, options = {}) {
    try {
        const response = await fetch(url, options);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "API Error");
        }

        return data;
    } catch (error) {
        throw error;
    }
}

// ==========================
// API CALLS
// ==========================

async function fetchCategories() {
    setLoading(true);
    try {
        const data = await apiRequest(`${API_BASE}/`);
        renderDataList(data, "category");
    } catch (error) {
        showMessage(error.message, true);
    } finally {
        setLoading(false);
    }
}

async function fetchProducts() {
    setLoading(true);
    try {
        const data = await apiRequest(`${API_BASE}/products/`);
        renderDataList(data, "product");
    } catch (error) {
        showMessage(error.message, true);
    } finally {
        setLoading(false);
    }
}

async function fetchCategoryProducts() {
    const categoryId = document.getElementById("filter_cat_id").value.trim();

    if (!categoryId) {
        showMessage("Please enter a Category ID", true);
        return;
    }

    setLoading(true);
    try {
        const data = await apiRequest(`${API_BASE}/${categoryId}/products/`);
        renderDataList(data, "product");
    } catch (error) {
        showMessage(error.message, true);
    } finally {
        setLoading(false);
    }
}

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
        await apiRequest(`${API_BASE}/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, description })
        });

        showMessage("Category added successfully");
        nameInput.value = "";
        descInput.value = "";
        fetchCategories();
    } catch (error) {
        showMessage(error.message, true);
    }
}

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
        await apiRequest(`${API_BASE}/${category_id}/products/${product_id}/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" }
        });

        showMessage("Product added to category successfully");
        catIdInput.value = "";
        prodIdInput.value = "";
    } catch (error) {
        showMessage(error.message, true);
    }
}

async function removeProductFromCategory() {
    const catId = document.getElementById("rem_cat_id").value.trim();
    const prodId = document.getElementById("rem_prod_id").value.trim();

    if (!catId || !prodId) {
        showMessage("Please fill all fields", true);
        return;
    }

    setLoading(true);
    try {
        await apiRequest(`${API_BASE}/${catId}/products/${prodId}/`, {
            method: "DELETE"
        });
        showMessage("Product removed from category successfully");
        document.getElementById("rem_cat_id").value = "";
        document.getElementById("rem_prod_id").value = "";
    } catch (error) {
        showMessage(error.message, true);
    } finally {
        setLoading(false);
    }
}

async function deleteCategory(id) {
    if (!confirm("Are you sure you want to delete this category?")) return;
    setLoading(true);
    try {
        await apiRequest(`${API_BASE}/${id}/`, { method: "DELETE" });
        showMessage("Category deleted successfully");
        fetchCategories();
    } catch (error) {
        showMessage(error.message, true);
    } finally {
        setLoading(false);
    }
}

async function editCategory(id, newName, newDesc) {
    setLoading(true);
    try {
        await apiRequest(`${API_BASE}/${id}/`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name: newName, description: newDesc })
        });
        showMessage("Category updated successfully");
        fetchCategories();
    } catch (error) {
        showMessage(error.message, true);
    } finally {
        setLoading(false);
    }
}

// ==========================
// RENDERING (SAFE DOM)
// ==========================
function renderDataList(items, type) {
    const container = document.getElementById("data-container");
    container.innerHTML = "";

    if (!items || items.length === 0) {
        container.textContent = `No ${type}s found`;
        return;
    }

    const fragment = document.createDocumentFragment();

    items.forEach(item => {
        const card = type === "category"
            ? createCategoryCard(item)
            : createProductCard(item);

        fragment.appendChild(card);
    });

    container.appendChild(fragment);
}

function createCategoryCard(category) {
    const div = createCard();

    // View Elements
    const viewDiv = document.createElement("div");
    viewDiv.appendChild(createText("h3", category.name));
    viewDiv.appendChild(createText("p", `Description: ${category.description || "N/A"}`));
    viewDiv.appendChild(createText("p", `ID: ${category.id || "-"}`));

    // Edit Elements
    const editDiv = document.createElement("div");
    editDiv.style.display = "none";
    editDiv.style.flexDirection = "column";

    const nameInput = document.createElement("input");
    nameInput.type = "text";
    nameInput.value = category.name;
    nameInput.style.marginBottom = "5px";
    nameInput.style.padding = "5px";

    const descInput = document.createElement("input");
    descInput.type = "text";
    descInput.value = category.description || "";
    descInput.style.marginBottom = "10px";
    descInput.style.padding = "5px";

    editDiv.appendChild(createText("strong", "Name:"));
    editDiv.appendChild(nameInput);
    editDiv.appendChild(createText("strong", "Description:"));
    editDiv.appendChild(descInput);

    // Buttons
    const btnDiv = document.createElement("div");
    btnDiv.style.display = "flex";
    btnDiv.style.gap = "10px";
    btnDiv.style.marginTop = "10px";

    const editBtn = document.createElement("button");
    editBtn.textContent = "Edit";

    const saveBtn = document.createElement("button");
    saveBtn.textContent = "Save";
    saveBtn.className = "primary";
    saveBtn.style.display = "none";

    const cancelBtn = document.createElement("button");
    cancelBtn.textContent = "Cancel";
    cancelBtn.style.display = "none";

    const delBtn = document.createElement("button");
    delBtn.textContent = "Delete";
    delBtn.style.backgroundColor = "#cc0000";
    delBtn.style.color = "white";

    const toggleEdit = (isEditing) => {
        viewDiv.style.display = isEditing ? "none" : "block";
        editDiv.style.display = isEditing ? "flex" : "none";
        editBtn.style.display = isEditing ? "none" : "block";
        delBtn.style.display = isEditing ? "none" : "block";
        saveBtn.style.display = isEditing ? "block" : "none";
        cancelBtn.style.display = isEditing ? "block" : "none";
        
        if (!isEditing) {
            nameInput.value = category.name;
            descInput.value = category.description || "";
        }
    };

    editBtn.onclick = () => toggleEdit(true);
    cancelBtn.onclick = () => toggleEdit(false);
    delBtn.onclick = () => deleteCategory(category.id);
    saveBtn.onclick = () => {
        const newName = nameInput.value.trim();
        const newDesc = descInput.value.trim();
        if (!newName) {
            showMessage("Name is required", true);
            return;
        }
        editCategory(category.id, newName, newDesc);
    };

    btnDiv.appendChild(editBtn);
    btnDiv.appendChild(saveBtn);
    btnDiv.appendChild(cancelBtn);
    btnDiv.appendChild(delBtn);

    div.appendChild(viewDiv);
    div.appendChild(editDiv);
    div.appendChild(btnDiv);

    return div;
}

function createProductCard(product) {
    const div = createCard();

    div.appendChild(createText("h3", product.name));
    div.appendChild(createText("p", `Brand: ${product.brand || "N/A"}`));
    div.appendChild(createText("p", `ID: ${product.id || "-"}`));
    div.appendChild(createText("p", `Categories: ${formatCategories(product.categories)}`));

    return div;
}

function createCard() {
    const div = document.createElement("div");
    div.className = "product-card";
    return div;
}

function createText(tag, text) {
    const el = document.createElement(tag);
    el.textContent = text;
    return el;
}

// ==========================
// HELPERS
// ==========================

function formatCategories(categories) {
    if (!Array.isArray(categories) || categories.length === 0) return "None";
    return categories.join(", ");
}

function setLoading(isLoading) {
    const container = document.getElementById("data-container");
    if (isLoading) {
        container.textContent = "Loading...";
    }
}

function showMessage(message, isError = false) {
    const msg = document.getElementById("message");
    msg.textContent = message;
    msg.style.color = isError ? "#cc0000" : "#008800";

    setTimeout(() => {
        msg.textContent = "";
    }, 3000);
}