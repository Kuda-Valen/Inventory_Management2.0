-- Enable UUID extension for secure, ungressable public IDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ====================================================
-- Table 1: STAFF & AUTHENTICATION DOMAIN
-- ====================================================

CREATE TABLE staff(
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role user_role NOT NULL DEFAULT 'CASHIER',
    is active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);  

CREATE INDEX idx_staff_email ON staff(email);

-- ====================================================
-- Table 2: CUSTOMER DOMAIN
-- ====================================================

CREATE TABLE customers(
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20) UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_customers_phone ON customers(phone);
CREATE INDEX idx_customers_email ON customers(email);


-- ====================================================
-- Table 3: INVENTORY & PRODUCT DOMAIN
-- ====================================================

CREATE TABLE categories(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100), UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products(
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    category_id INT REFERENCES categories(id) ON DELETE SET NULL,
    sku VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    cost_price NUMERIC(10, 2) NOT NULL CHECK (cost_price >= 0),
    selling_price NUMERIC(10, 2) NOT NULL CHECK (selling_price >= 0),
    stock_quantity INT NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
    reorder_level INT NOT NULL DEFAULT 5 CHECK (reorder_level > 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_products_category ON products(category_id);

-- Audit Log for Stock Adjustments (Restock, Returns, Damaged Goods)
CREATE TYPE stock_movement_type AS ENUM ('RESTOCK', 'SALE', 'RETURN', 'ADJUSTMENT');

CREATE TABLE inventory_movements (
    id BIGSERIAL PRIMARY KEY,
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    staff_id UUID REFERENCES staff(id) ON DELETE SET NULL,
    movement_type stock_movement_type NOT NULL,
    quantity_changed INT NOT NULL,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_inventory_movements_product ON inventory_movements(product_id);


-- ====================================================
-- Table 4: SALES & TRANSACTION DOMAIN
-- ====================================================

CREATE TYPE payment_method AS ENUM ('CASH', 'CARD', 'EFT', 'STORE_CREDIT');
CREATE TYPE order_status AS ENUM ('COMPLETED', 'REFUNDED', 'CANCELLED');

CREATE TABLE sales_orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    receipt_number VARCHAR(50) UNIQUE NOT NULL,
    customer_id UUID REFERENCES customers(id) ON DELETE SET NULL,
    staff_id UUID NOT NULL REFERENCES staff(id) ON DELETE RESTRICT,
    total_amount NUMERIC(10, 2) NOT NULL CHECH (total_amount >= 0),
    payment_method payment_method NOT NULL DEFAULT 'CASH',
    status order_status NOT NULL DEFAULT 'COMPLETED'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sales_orders_customer ON sales_orders(customer_id);
CREATE INDEX idx_sales_orders_staff ON sales_orders(staff_id);
CREATE INDEX idx_sales_orders_created ON sales_orders(created_at);

-- Order Items (Many-to-Many Junction table between Orders and Products)
CREATE TABLE sales_order_items(
    id BIGSERIAL PRIMARY KEY,
    order_id UUID NOT NULL REFERENCES sales_orders(id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0),
    subtotal NUMERIC(10, 2) NOT NULL CHECK (subtotal >= 0)
);

CREATE INDEX idx_order_items_order ON sales_order_items(order_id);
CREATE INDEX idx_order_items_product ON sales_order_items(product_id);