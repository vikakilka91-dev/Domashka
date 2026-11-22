-- Файл: database/scripts/entities/orders/create_table.sql
-- Студент: Иванов Иван
-- Сущность: Заказы

CREATE TABLE orders (
    -- 1. Первичный ключ (всегда id, PRIMARY KEY)
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    -- 2. Внешние ключи (FK: <сущность>_id)
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    
    -- 3. Атрибуты таблицы (SnakeCase)
    order_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    quantity INT NOT NULL DEFAULT 1,
    total_price DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    
    -- 4. Внешние ключи (Связи)
    -- Названия таблиц пишем в snake_case (как в репозитории)
    CONSTRAINT fk_orders_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_orders_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
