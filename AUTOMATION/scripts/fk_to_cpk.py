#test case 4
### Three tables with CPK ↔ FK relation
import psycopg2
from faker import Faker
import random

# Initialize Faker
fake = Faker()

# PostgreSQL connection parameters
db_params = {
    'dbname': 'automation_test_4',
    'user': 'postgres',
    'password': '2c510254-b82a-4562-9950-ad18e561cdee',
    'host': '207.180.249.216',
    'port': '5433'
}

# SQL to create normalized tables
create_tables_sql = """
-- OrdersHeader: Unique list of order_ids
CREATE TABLE IF NOT EXISTS OrdersHeader (
    order_id INTEGER PRIMARY KEY
);

-- Orders: Composite PK (order_id, product_id)
CREATE TABLE IF NOT EXISTS Orders (
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    quantity INTEGER NOT NULL,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES OrdersHeader(order_id) ON DELETE CASCADE
);

-- Shipments: FK to only order_id (partial reference of CPK in Orders)
CREATE TABLE IF NOT EXISTS Shipments (
    shipment_id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    shipment_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES OrdersHeader(order_id) ON DELETE CASCADE
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

def insert_sample_data(num_orders=10, products_per_order=3, shipments_per_order=2):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()

            # Insert into OrdersHeader
            for order_id in range(1, num_orders + 1):
                cur.execute("INSERT INTO OrdersHeader (order_id) VALUES (%s)", (order_id,))

            # Insert into Orders (CPK)
            for order_id in range(1, num_orders + 1):
                for product_id in range(1, products_per_order + 1):
                    order_date = fake.date_between(start_date='-1y', end_date='today')
                    quantity = random.randint(1, 10)
                    cur.execute(
                        "INSERT INTO Orders (order_id, product_id, order_date, quantity) VALUES (%s, %s, %s, %s)",
                        (order_id, product_id, order_date, quantity)
                    )

            # Insert into Shipments (partial FK to OrdersHeader)
            for order_id in range(1, num_orders + 1):
                for _ in range(shipments_per_order):
                    shipment_date = fake.date_between(start_date='today', end_date='+30d')
                    status = random.choice(['Pending', 'Shipped', 'Delivered'])
                    cur.execute(
                        "INSERT INTO Shipments (order_id, shipment_date, status) VALUES (%s, %s, %s)",
                        (order_id, shipment_date, status)
                    )

            conn.commit()
            print(f"Inserted OrdersHeader, Orders (CPK), and Shipments (partial FK)")
        except Exception as e:
            print(f"Error inserting data: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

if __name__ == "__main__":
    create_tables()
    insert_sample_data()