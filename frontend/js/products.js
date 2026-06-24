async function loadProducts() {

    const response =
        await fetch(
            "http://localhost:5000/products"
        );

    const products =
        await response.json();

    const container =
        document.getElementById(
            "products-container"
        );

    let html = "";

    products.forEach(product => {

        html += `
            <div class="product">

                <h3>${product.name}</h3>

                <p>₹${product.price.toLocaleString('en-IN')}</p>

                <button onclick="addToCart('${product.name}', ${product.price})">
                    Add To Cart
                </button>

            </div>
        `;
    });

    container.innerHTML = html;
}

window.onload = loadProducts;