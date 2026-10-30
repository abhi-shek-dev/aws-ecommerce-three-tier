CREATE DATABASE IF NOT EXISTS ecommerce CHARACTER SET utf8mb4;
USE ecommerce;

CREATE TABLE IF NOT EXISTS products (
    id    INT AUTO_INCREMENT PRIMARY KEY,
    name  VARCHAR(100) NOT NULL UNIQUE,
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0)
);

-- One row per product per anonymous browser (client_id), so visitors have separate carts
CREATE TABLE IF NOT EXISTS cart (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    client_id  VARCHAR(64) NOT NULL,
    product_id INT NOT NULL,
    quantity   INT NOT NULL DEFAULT 1 CHECK (quantity > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_cart_client_product (client_id, product_id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE IF NOT EXISTS orders (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    client_id    VARCHAR(64) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    order_date   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_orders_client (client_id)
);

-- What was bought, at the price paid at that moment
CREATE TABLE IF NOT EXISTS order_items (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    order_id   INT NOT NULL,
    product_id INT NOT NULL,
    quantity   INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Sample catalogue (safe to re-run)
INSERT IGNORE INTO products (name, price) VALUES
    ('Laptop', 65000.00),
    ('Phone', 30000.00),
    ('Headphones', 5000.00);
