## test case 7
# Parent CPK → Child CFK where child CPK is same set
# Parent: Has Composite Primary Key (CPK).

# Child: Has Composite Foreign Key (CFK) referencing exactly the same set of columns as parent’s CPK.

# Child CPK = same set of columns (so PK in child is also the FK).

import psycopg2
from faker import Faker
import random

# Initialize Faker
fake = Faker()

# PostgreSQL connection parameters
db_params = {
    'dbname': 'automation_test_7',
    'user': 'postgres',
    'password': '2c510254-b82a-4562-9950-ad18e561cdee',
    'host': '207.180.249.216',
    'port': '5433'
}

# SQL to create tables
create_tables_sql = """
-- Parent: Orders table with Composite Primary Key (order_id, product_id)
CREATE TABLE IF NOT EXISTS Orders (
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    quantity INTEGER NOT NULL,
    PRIMARY KEY (order_id, product_id)
);

-- Child: OrderShipping table where PK = FK (same set as parent CPK)
CREATE TABLE IF NOT EXISTS OrderShipping (
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    shipping_date DATE NOT NULL,
    carrier VARCHAR(50) NOT NULL,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id, product_id) REFERENCES Orders(order_id, product_id) ON DELETE CASCADE
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
            print("Tables created successfully")
        except Exception as e:
            print(f"Error creating tables: {e}")
        finally:
            cur.close()
            conn.close()

def insert_sample_data(num_orders=10, products_per_order=3):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()

            # Insert into Orders (parent)
            orders_list = []
            for order_id in range(1, num_orders + 1):
                for product_id in range(1, products_per_order + 1):
                    order_date = fake.date_between(start_date='-1y', end_date='today')
                    quantity = random.randint(1, 10)
                    cur.execute(
                        "INSERT INTO Orders (order_id, product_id, order_date, quantity) VALUES (%s, %s, %s, %s)",
                        (order_id, product_id, order_date, quantity)
                    )
                    orders_list.append((order_id, product_id))

            # Insert into OrderShipping (child, PK=FK same set)
            for order_id, product_id in orders_list:
                shipping_date = fake.date_between(start_date='today', end_date='+30d')
                carrier = random.choice(['FedEx', 'UPS', 'DHL', 'USPS'])
                cur.execute(
                    "INSERT INTO OrderShipping (order_id, product_id, shipping_date, carrier) VALUES (%s, %s, %s, %s)",
                    (order_id, product_id, shipping_date, carrier)
                )

            conn.commit()
            print(f"Inserted {len(orders_list)} Orders and matching OrderShipping records (PK=FK same set)")
        except Exception as e:
            print(f"Error inserting data: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

if __name__ == "__main__":
    create_tables()
    insert_sample_data()
