# #test case 6
# ### Parent PK → Child FK where child PK is same column (PK is also FK — e.g., 1-to-1 relation)
import psycopg2
from faker import Faker
import random

# Initialize Faker
fake = Faker()

# PostgreSQL connection parameters
db_params = {
    'dbname': 'automation_test_6',
    'user': 'postgres',
    'password': '2c510254-b82a-4562-9950-ad18e561cdee',
    'host': '207.180.249.216',
    'port': '5433'
}

# SQL to create tables
create_tables_sql = """
-- Table 1: Regions with simple PK
CREATE TABLE IF NOT EXISTS Regions (
    region_id SERIAL PRIMARY KEY,
    region_name VARCHAR(50) NOT NULL
);

-- Table 2: Customers with CPK (customer_id, region_id), where region_id is FK to Regions
CREATE TABLE IF NOT EXISTS Customers (
    customer_id SERIAL,
    region_id INT NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (customer_id, region_id),
    FOREIGN KEY (region_id) REFERENCES Regions(region_id) ON DELETE CASCADE
);

-- Table 3: Orders with FK referencing Customers' CPK
CREATE TABLE IF NOT EXISTS Orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    region_id INT NOT NULL,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (customer_id, region_id) REFERENCES Customers(customer_id, region_id) ON DELETE CASCADE
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

def insert_sample_data(num_regions=5, num_customers_per_region=5, max_orders_per_customer=5):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()

            # Insert regions
            region_ids = []
            for _ in range(num_regions):
                region_name = fake.unique.state()
                cur.execute(
                    "INSERT INTO Regions (region_name) VALUES (%s) RETURNING region_id",
                    (region_name,)
                )
                region_id = cur.fetchone()[0]
                region_ids.append(region_id)

            # Insert customers with region_id as FK
            customer_keys = []
            for region_id in region_ids:
                for _ in range(num_customers_per_region):
                    first_name = fake.first_name()
                    last_name = fake.last_name()
                    email = fake.unique.email()
                    cur.execute(
                        "INSERT INTO Customers (region_id, first_name, last_name, email) VALUES (%s, %s, %s, %s) RETURNING customer_id, region_id",
                        (region_id, first_name, last_name, email)
                    )
                    customer_id, region_id = cur.fetchone()
                    customer_keys.append((customer_id, region_id))

            # Insert orders using customer_id and region_id as composite FK
            for customer_id, region_id in customer_keys:
                num_orders = random.randint(1, max_orders_per_customer)
                for _ in range(num_orders):
                    order_date = fake.date_between(start_date='-1y', end_date='today')
                    total_amount = round(random.uniform(10.0, 1000.0), 2)
                    cur.execute(
                        "INSERT INTO Orders (customer_id, region_id, order_date, total_amount) VALUES (%s, %s, %s, %s)",
                        (customer_id, region_id, order_date, total_amount)
                    )

            conn.commit()
            print(f"Inserted {num_regions} regions, {len(customer_keys)} customers, and their orders (CPK with FK)")
        except Exception as e:
            print(f"Error inserting data: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

if __name__ == "__main__":
    create_tables()
    insert_sample_data()