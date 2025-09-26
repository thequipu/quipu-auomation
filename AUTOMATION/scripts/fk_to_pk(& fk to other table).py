import psycopg2
from faker import Faker
import random

# Initialize Faker
fake = Faker()

# PostgreSQL connection parameters
db_params = {
    'dbname': 'automation_test_10',
    'user': 'postgres',
    'password': '2c510254-b82a-4562-9950-ad18e561cdee',
    'host': '207.180.249.216',
    'port': '5433'
}

# SQL to create tables
create_tables_sql = """
-- Table A: Customers
CREATE TABLE IF NOT EXISTS Customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Table B: Products
CREATE TABLE IF NOT EXISTS Products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

-- Table C: Orders with two separate FKs
CREATE TABLE IF NOT EXISTS Orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE
);
"""

def connect_db():
    try:
        conn = psycopg2.connect(**db_params)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def create_tables():
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(create_tables_sql)
            conn.commit()
            print("Tables created successfully (Multi-FK scenario)")
        except Exception as e:
            print(f"Error creating tables: {e}")
        finally:
            cur.close()
            conn.close()

def insert_sample_data(num_customers=5, num_products=5, num_orders=15):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()

            # Insert customers
            customer_ids = []
            for _ in range(num_customers):
                first_name = fake.first_name()
                last_name = fake.last_name()
                email = fake.unique.email()
                cur.execute(
                    "INSERT INTO Customers (first_name, last_name, email) VALUES (%s, %s, %s) RETURNING customer_id",
                    (first_name, last_name, email)
                )
                customer_ids.append(cur.fetchone()[0])

            # Insert products
            product_ids = []
            for _ in range(num_products):
                product_name = fake.word().capitalize()
                price = round(random.uniform(5.0, 500.0), 2)
                cur.execute(
                    "INSERT INTO Products (product_name, price) VALUES (%s, %s) RETURNING product_id",
                    (product_name, price)
                )
                product_ids.append(cur.fetchone()[0])

            # Insert orders linking customers & products
            for _ in range(num_orders):
                customer_id = random.choice(customer_ids)
                product_id = random.choice(product_ids)
                order_date = fake.date_between(start_date='-1y', end_date='today')
                quantity = random.randint(1, 10)
                cur.execute(
                    "INSERT INTO Orders (customer_id, product_id, order_date, quantity) VALUES (%s, %s, %s, %s)",
                    (customer_id, product_id, order_date, quantity)
                )

            conn.commit()
            print(f"Inserted {num_customers} customers, {num_products} products, and {num_orders} orders (multi-FK)")
        except Exception as e:
            print(f"Error inserting data: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

if __name__ == "__main__":
    create_tables()
    insert_sample_data()
