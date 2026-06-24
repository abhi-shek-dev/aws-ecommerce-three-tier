async function addToCart(name, price) {

    const response =
        await fetch(
            "http://localhost:5000/cart/add",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    name: name,
                    price: price
                })
            }
        );

    const result =
        await response.json();

    alert(result.message);
}

async function removeFromCart(index) {

    await fetch(
        `http://localhost:5000/cart/remove/${index}`,
        {
            method: "DELETE"
        }
    );

    loadCart();
}


async function loadCart() {

    const response =
        await fetch(
            "http://localhost:5000/cart"
        );

    const cart =
        await response.json();

    let cartDiv =
        document.getElementById(
            "cart-items"
        );

    if (!cartDiv) return;

    if (cart.length === 0) {

        cartDiv.innerHTML =
            "<h3>Your cart is empty</h3>";

        return;
    }

    let html = "";

    let total = 0;

    cart.forEach((item, index) => {

        html += `
            <div class="product">

                <h3>${item.name}</h3>

                <p>
                    Price: ₹${item.price}
                </p>

                <p>
                    Quantity:
                    ${item.quantity}
                </p>

                <button
                    onclick="removeFromCart(${index})">
                    Remove
                </button>

            </div>
        `;

        total +=
            item.price *
            item.quantity;
    });

    html += `
        <h2>
            Total: ₹${total}
        </h2>
    `;

    cartDiv.innerHTML = html;
}
window.onload = loadCart;


async function checkout() {

    const response =
        await fetch(
            "http://localhost:5000/checkout",
            {
                method: "POST"
            }
        );

    const result =
        await response.json();

    alert(
        `${result.message}
Total: ₹${result.total}`
    );

    loadCart();
}