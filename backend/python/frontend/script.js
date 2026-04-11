// Fetch products from API
fetch("http://127.0.0.1:8000/products/")
    .then(response => response.json())
    .then(data => {
        console.log("API Data:", data);  // ✅ View in console

        displayProducts(data);
    })
    .catch(error => {
        console.error("Error:", error);
    });


// Display products in UI
function displayProducts(products) {
    const container = document.getElementById("product-container");

    products.forEach(product => {
        const card = document.createElement("div");
        card.className = "product-card";

        card.innerHTML = `
            <h2>${product.name}</h2>
            <p><strong>Brand:</strong> ${product.brand || "N/A"}</p>
            <p><strong>Categories:</strong> ${formatCategories(product.categories)}</p>
        `;

        container.appendChild(card);
    });
}


// Helper function
function formatCategories(categories) {
    if (!categories || categories.length === 0) return "None";

    return categories.join(", ");
}