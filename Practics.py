import sqlite3

def connect_db():
    conn = sqlite3.connect('database.db')
    return conn

def create_tables(conn):
    cursor = conn.cursor()
    
    # Создание таблицы store
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS store (
        store_id INTEGER PRIMARY KEY,
        title VARCHAR(100)
    );
    """)
    
    # Создание таблицы categories
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        code VARCHAR(2) PRIMARY KEY,
        title VARCHAR(150)
    );
    """)
    
    # Создание таблицы products
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        title VARCHAR(250),
        category_code VARCHAR(2),
        unit_price FLOAT,
        stock_quantity INTEGER,
        store_id INTEGER,
        FOREIGN KEY (category_code) REFERENCES categories(code),
        FOREIGN KEY (store_id) REFERENCES store(store_id)
    );
    """)

    # Вставка данных в таблицу store
    cursor.executemany("INSERT OR IGNORE INTO store (store_id, title) VALUES (?, ?)", [
        (1, 'Asia'),
        (2, 'Globus'),
        (3, 'Spar')
    ])
    
    # Вставка данных в таблицу categories
    cursor.executemany("INSERT OR IGNORE INTO categories (code, title) VALUES (?, ?)", [
        ('FD', 'Food products'),
        ('EL', 'Electronics'),
        ('CL', 'Clothes')
    ])
    
    # Вставка данных в таблицу products
    cursor.executemany("INSERT OR IGNORE INTO products (id, title, category_code, unit_price, stock_quantity, store_id) VALUES (?, ?, ?, ?, ?, ?)", [
        (1, 'Chocolate', 'FD', 10.5, 129, 1),
        (2, 'Jeans', 'CL', 120.0, 55, 2),
        (3, 'T-Shirt', 'CL', 10.0, 0, 1)
    ])

    conn.commit()

def display_stores(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT store_id, title FROM store")
    stores = cursor.fetchall()
    print("Вы можете отобразить список продуктов по выбранному id магазина из перечня магазинов ниже, для выхода из программы введите цифру 0:")
    for store in stores:
        print(f"{store[0]}. {store[1]}")
    print()

def display_products_by_store(conn, store_id):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT products.title, categories.title, products.unit_price, products.stock_quantity 
        FROM products 
        JOIN categories ON products.category_code = categories.code 
        WHERE products.store_id = ?
    """, (store_id,))
    products = cursor.fetchall()
    
    if products:
        for product in products:
            print(f"Название продукта: {product[0]}")
            print(f"Категория: {product[1]}")
            print(f"Цена: {product[2]}")
            print(f"Количество на складе: {product[3]}")
            print()
    else:
        print("Продукты для выбранного магазина не найдены.\n")

def main():
    conn = connect_db()
    create_tables(conn)  # Создаем таблицы и добавляем данные, если их еще нет
    
    while True:
        display_stores(conn)
        try:
            store_id = int(input("Введите id магазина (или 0 для выхода): "))
            if store_id == 0:
                print("Выход из программы.")
                break
            display_products_by_store(conn, store_id)
        except ValueError:
            print("Пожалуйста, введите корректное число.\n")
    
    conn.close()

if __name__ == "__main__":
    main()
