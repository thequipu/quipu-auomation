import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

# PostgreSQL connection parameters
db_params = {
    'dbname': 'automation_test_11',
    'user': 'postgres',
    'password': '2c510254-b82a-4562-9950-ad18e561cdee',
    'host': '207.180.249.216',
    'port': '5433'
}

# SQL to create tables for "Unique multi-col → CFK"
create_tables_sql = """
-- Parent table with multi-column UNIQUE constraint
CREATE TABLE IF NOT EXISTS Products (
    product_code VARCHAR(20) NOT NULL,
    batch_number VARCHAR(20) NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    CONSTRAINT unique_product_batch UNIQUE (product_code, batch_number)
);

-- Child table with composite foreign key referencing unique columns
CREATE TABLE IF NOT EXISTS Shipments (
    shipment_id SERIAL PRIMARY KEY,
    product_code VARCHAR(20) NOT NULL,
    batch_number VARCHAR(20) NOT NULL,
    shipment_date DATE NOT NULL,
    quantity INTEGER NOT NULL,
    CONSTRAINT fk_product_batch FOREIGN KEY (product_code, batch_number)
        REFERENCES Products(product_code, batch_number)
        ON DELETE CASCADE
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
            print("Tables created successfully for Unique multi-col → CFK case")
        except Exception as e:
            print(f"Error creating tables: {e}")
        finally:
            cur.close()
            conn.close()

def insert_sample_data(num_products=5, max_shipments_per_product=3):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()

            # Insert products (ensuring unique product_code + batch_number)
            products = []
            for _ in range(num_products):
                product_code = fake.bothify(text='PROD-####')
                batch_number = fake.bothify(text='BATCH-##')
                product_name = fake.word().capitalize()
                price = round(random.uniform(50.0, 500.0), 2)

                cur.execute("""
                    INSERT INTO Products (product_code, batch_number, product_name, price)
                    VALUES (%s, %s, %s, %s)
                    RETURNING product_code, batch_number
                """, (product_code, batch_number, product_name, price))

                products.append(cur.fetchone())

            # Insert shipments for each product-batch
            for product_code, batch_number in products:
                for _ in range(random.randint(1, max_shipments_per_product)):
                    shipment_date = fake.date_between(start_date='-6m', end_date='today')
                    quantity = random.randint(10, 100)

                    cur.execute("""
                        INSERT INTO Shipments (product_code, batch_number, shipment_date, quantity)
                        VALUES (%s, %s, %s, %s)
                    """, (product_code, batch_number, shipment_date, quantity))

            conn.commit()
            print(f"Inserted {num_products} products and their shipments")
        except Exception as e:
            print(f"Error inserting data: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

if __name__ == "__main__":
    create_tables()
    insert_sample_data()
