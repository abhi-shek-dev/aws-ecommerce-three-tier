async function loadProducts() {
    const container = document.getElementById("products-container");
    if (!container) return;

    // data-limit="3" on the container shows only the first 3 (used for "Featured Products")
    const limit = parseInt(container.dataset.limit || "0", 10);

    try {
        let products = await api("/products");
        if (limit > 0) {
            products = products.slice(0, limit);
        }

        container.innerHTML = products
            .map(
                (product) => `
                <div class="product">
                    <h3>${escapeHtml(product.name)}</h3>
                    <p>${formatPrice(product.price)}</p>
                    <button onclick="addToCart(${Number(product.id)})">Add To Cart</button>
                </div>
            `
            )
            .join("");
    } catch (error) {
        container.textContent = "Could not load products. Please try again.";
    }
}

document.addEventListener("DOMContentLoaded", loadProducts);
