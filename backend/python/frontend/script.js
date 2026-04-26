// ==========================
// CONFIG
// ==========================
const API_BASE = "http://127.0.0.1:8001/categories";
const BRAND_BASE = "http://127.0.0.1:8001/brands";

// ==========================
// INIT
// ==========================
document.addEventListener("DOMContentLoaded", () => {
    fetchCategories();
    refreshDropdowns();
});

async function refreshDropdowns() {
    try {
        const [categories, brands, products] = await Promise.all([
            apiRequest(`${API_BASE}/`).catch(e => { console.error("Categories failed", e); return []; }),
            apiRequest(`${BRAND_BASE}/`).catch(e => { console.error("Brands failed", e); return []; }),
            apiRequest(`${API_BASE}/products/`).catch(e => { console.error("Products failed", e); return []; })
        ]);

        const populate = (ids, items, defaultText) => {
            ids.forEach(id => {
                const el = document.getElementById(id);
                if (!el) return;
                const prev = el.value;
                el.innerHTML = `<option value="">${defaultText}</option>` + 
                    items.map(i => `<option value="${i.id}">${i.name}</option>`).join("");
                if(items.find(i => i.id === prev)) { el.value = prev; }
            });
        };

        populate(["filter_cat_id", "new_prod_cat_id", "assign_cat_id", "rem_cat_id"], categories, "Select Category...");
        populate(["new_prod_brand_id"], brands, "Select Brand...");
        populate(["assign_prod_id", "rem_prod_id"], products, "Select Product...");
    } catch(e) {
        console.error("Failed to load options", e);
    }
}

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
        refreshDropdowns();
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

async function addNewProduct() {
    const catIdInput = document.getElementById("new_prod_cat_id");
    const nameInput = document.getElementById("new_prod_name");
    const brandIdInput = document.getElementById("new_prod_brand_id");

    const category_id = catIdInput.value.trim();
    const name = nameInput.value.trim();
    const brand_id = brandIdInput.value.trim();

    if (!category_id || !name || !brand_id) {
        showMessage("Please fill all fields", true);
        return;
    }

    try {
        await apiRequest(`${API_BASE}/${category_id}/products/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, brand_id })
        });

        showMessage("Product created and assigned successfully");
        catIdInput.value = "";
        nameInput.value = "";
        brandIdInput.value = "";
        refreshDropdowns();
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

// ==========================
// BRAND API CALLS
// ==========================

async function fetchBrands() {
    setLoading(true);
    try {
        const data = await apiRequest(`${BRAND_BASE}/`);
        renderDataList(data, "brand");
    } catch (error) {
        showMessage(error.message, true);
    } finally {
        setLoading(false);
    }
}

async function addBrand() {
    const nameInput = document.getElementById("brand_name");
    const descInput = document.getElementById("brand_desc");

    const name = nameInput.value.trim();
    const description = descInput.value.trim();

    if (!name || !description) {
        showMessage("Please fill all brand fields", true);
        return;
    }

    try {
        await apiRequest(`${BRAND_BASE}/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, description })
        });
        showMessage("Brand added successfully");
        nameInput.value = "";
        descInput.value = "";
        fetchBrands();
        refreshDropdowns();
    } catch (error) {
        showMessage(error.message, true);
    }
}

async function editBrand() {
    const idInput = document.getElementById("edit_brand_id");
    const nameInput = document.getElementById("edit_brand_name");
    const descInput = document.getElementById("edit_brand_desc");

    const brand_id = idInput.value.trim();
    const name = nameInput.value.trim();
    const description = descInput.value.trim();

    if (!brand_id || (!name && !description)) {
        showMessage("Please provide Brand ID and at least one field to update", true);
        return;
    }

    const payload = {};
    if (name) payload.name = name;
    if (description) payload.description = description;

    try {
        await apiRequest(`${BRAND_BASE}/${brand_id}/`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        showMessage("Brand updated successfully");
        idInput.value = "";
        nameInput.value = "";
        descInput.value = "";
        fetchBrands();
    } catch (error) {
        showMessage(error.message, true);
    }
}

async function deleteBrand() {
    const idInput = document.getElementById("del_brand_id");
    const brand_id = idInput.value.trim();

    if (!brand_id) {
        showMessage("Please enter a Brand ID", true);
        return;
    }

    if (!confirm("Are you sure you want to delete this brand?")) return;

    try {
        await apiRequest(`${BRAND_BASE}/${brand_id}/`, { method: "DELETE" });
        showMessage("Brand deleted successfully");
        idInput.value = "";
        fetchBrands();
        refreshDropdowns();
    } catch (error) {
        showMessage(error.message, true);
    }
}

async function deleteBrandCard(id) {
    if (!confirm("Are you sure you want to delete this brand?")) return;
    try {
        await apiRequest(`${BRAND_BASE}/${id}/`, { method: "DELETE" });
        showMessage("Brand deleted successfully");
        fetchBrands();
        refreshDropdowns();
    } catch (error) {
        showMessage(error.message, true);
    }
}

async function deleteCategory(id) {
    if (!confirm("Are you sure you want to delete this category?")) return;
    setLoading(true);
    try {
        await apiRequest(`${API_BASE}/${id}/`, { method: "DELETE" });
        showMessage("Category deleted successfully");
        fetchCategories();
        refreshDropdowns();
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
        refreshDropdowns();
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
            : type === "brand"
                ? createBrandCard(item)
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

    // View Elements
    const viewDiv = document.createElement("div");
    viewDiv.appendChild(createText("h3", product.name));
    viewDiv.appendChild(createText("p", `Brand: ${product.brand || "N/A"}`));
    viewDiv.appendChild(createText("p", `ID: ${product.id || "-"}`));
    viewDiv.appendChild(createText("p", `Categories: ${formatCategories(product.categories)}`));

    // Edit Elements
    const editDiv = document.createElement("div");
    editDiv.style.display = "none";
    editDiv.style.flexDirection = "column";

    const nameInput = document.createElement("input");
    nameInput.type = "text";
    nameInput.value = product.name;
    nameInput.style.marginBottom = "5px";
    nameInput.style.padding = "5px";

    editDiv.appendChild(createText("strong", "Name:"));
    editDiv.appendChild(nameInput);

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

        if (!isEditing) nameInput.value = product.name;
    };

    editBtn.onclick = () => toggleEdit(true);
    cancelBtn.onclick = () => toggleEdit(false);

    delBtn.onclick = async () => {
        if (!confirm("Are you sure you want to delete this product?")) return;
        try {
            await apiRequest(`${API_BASE}/products/${product.id}/`, { method: "DELETE" });
            showMessage("Product deleted successfully");
            fetchProducts();
            refreshDropdowns();
        } catch (error) {
            showMessage(error.message, true);
        }
    };

    saveBtn.onclick = async () => {
        const newName = nameInput.value.trim();
        if (!newName) { showMessage("Name is required", true); return; }
        try {
            await apiRequest(`${API_BASE}/products/${product.id}/`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name: newName })
            });
            showMessage("Product updated successfully");
            fetchProducts();
            refreshDropdowns();
        } catch (error) {
            showMessage(error.message, true);
        }
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

function createBrandCard(brand) {
    const div = createCard();

    // View Elements
    const viewDiv = document.createElement("div");
    viewDiv.appendChild(createText("h3", brand.name));
    viewDiv.appendChild(createText("p", `Description: ${brand.description || "N/A"}`));
    viewDiv.appendChild(createText("p", `ID: ${brand.id || "-"}`));

    // Edit Elements
    const editDiv = document.createElement("div");
    editDiv.style.display = "none";
    editDiv.style.flexDirection = "column";

    const nameInput = document.createElement("input");
    nameInput.type = "text";
    nameInput.value = brand.name;
    nameInput.style.marginBottom = "5px";
    nameInput.style.padding = "5px";

    const descInput = document.createElement("input");
    descInput.type = "text";
    descInput.value = brand.description || "";
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
            nameInput.value = brand.name;
            descInput.value = brand.description || "";
        }
    };

    editBtn.onclick = () => toggleEdit(true);
    cancelBtn.onclick = () => toggleEdit(false);
    delBtn.onclick = () => deleteBrandCard(brand.id);
    saveBtn.onclick = async () => {
        const newName = nameInput.value.trim();
        const newDesc = descInput.value.trim();
        if (!newName) {
            showMessage("Name is required", true);
            return;
        }
        try {
            await apiRequest(`${BRAND_BASE}/${brand.id}/`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name: newName, description: newDesc })
            });
            showMessage("Brand updated successfully");
            fetchBrands();
        } catch (error) {
            showMessage(error.message, true);
        }
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