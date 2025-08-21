###test case 1
## two tables customer & orders with PK ↔ FK
import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker for generating sample data
fake = Faker()

# PostgreSQL connection parameters
db_params = {
    'dbname': 'automation_test_1',
    'user': 'postgres',
    'password': '2c510254-b82a-4562-9950-ad18e561cdee',
    'host': '207.180.249.216',
    'port': '5433'
}

# SQL to create tables
create_tables_sql = """
-- Creating Customers table
CREATE TABLE IF NOT EXISTS Customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Creating Orders table with single primary key and foreign key
CREATE TABLE IF NOT EXISTS Orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE
);
"""

# Function to connect to PostgreSQL
def connect_db():
    try:
        conn = psycopg2.connect(**db_params)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

# Function to create tables
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

# Function to generate and insert sample data
def insert_sample_data(num_customers=10, max_orders_per_customer=5):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            
            # Insert customers
            customers = []
            for _ in range(num_customers):
                first_name = fake.first_name()
                last_name = fake.last_name()
                email = fake.email()
                cur.execute(
                    "INSERT INTO Customers (first_name, last_name, email) VALUES (%s, %s, %s) RETURNING customer_id",
                    (first_name, last_name, email)
                )
                customer_id = cur.fetchone()[0]
                customers.append(customer_id)
            
            # Insert orders
            for customer_id in customers:
                num_orders = random.randint(1, max_orders_per_customer)
                for _ in range(num_orders):
                    order_date = fake.date_between(start_date='-1y', end_date='today')
                    total_amount = round(random.uniform(10.0, 1000.0), 2)
                    cur.execute(
                        "INSERT INTO Orders (customer_id, order_date, total_amount) VALUES (%s, %s, %s)",
                        (customer_id, order_date, total_amount)
                    )
            
            conn.commit()
            print(f"Inserted {num_customers} customers and their orders")
        except Exception as e:
            print(f"Error inserting data: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

# Main execution
if __name__ == "__main__":
    create_tables()
    insert_sample_data()