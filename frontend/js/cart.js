async function addToCart(productId) {
    try {
        const result = await api("/cart/add", {
            method: "POST",
            body: JSON.stringify({ product_id: productId }),
        });
        alert(result.message);
    } catch (error) {
        alert(error.message);
    }
}

async function removeFromCart(itemId) {
    try {
        await api(`/cart/remove/${itemId}`, { method: "DELETE" });
        await loadCart();
    } catch (error) {
        alert(error.message);
    }
}

async function loadCart() {
    const cartDiv = document.getElementById("cart-items");
    if (!cartDiv) return; // not the cart page

    try {
        const cart = await api("/cart");

        if (cart.length === 0) {
            cartDiv.innerHTML = "<h3>Your cart is empty</h3>";
            return;
        }

        let total = 0;
        let html = "";

        cart.forEach((item) => {
            total += item.price * item.quantity;
            html += `
                <div class="product">
                    <h3>${escapeHtml(item.name)}</h3>
                    <p>Price: ${formatPrice(item.price)}</p>
                    <p>Quantity: ${Number(item.quantity)}</p>
                    <button onclick="removeFromCart(${Number(item.id)})">Remove</button>
                </div>
            `;
        });

        html += `<h2>Total: ${formatPrice(total)}</h2>`;
        cartDiv.innerHTML = html;
    } catch (error) {
        cartDiv.textContent = "Could not load your cart. Please try again.";
    }
}

async function checkout() {
    try {
        const result = await api("/checkout", { method: "POST" });
        alert(`${result.message}\nTotal: ${formatPrice(result.total)}`);
        await loadCart();
    } catch (error) {
        alert(error.message);
    }
}

document.addEventListener("DOMContentLoaded", loadCart);
