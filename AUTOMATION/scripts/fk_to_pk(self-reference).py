import psycopg2
from faker import Faker
import random

# Initialize Faker
fake = Faker()

# PostgreSQL connection parameters
db_params = {
    'dbname': 'automation_test_8',
    'user': 'postgres',
    'password': '2c510254-b82a-4562-9950-ad18e561cdee',
    'host': '207.180.249.216',
    'port': '5433'
}

# SQL to create self-referencing table
create_tables_sql = """
-- Employees table with self-referencing FK
CREATE TABLE IF NOT EXISTS Employees (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    position VARCHAR(50) NOT NULL,
    manager_id INTEGER,
    FOREIGN KEY (manager_id) REFERENCES Employees(employee_id) ON DELETE SET NULL
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
            print("Table created successfully")
        except Exception as e:
            print(f"Error creating table: {e}")
        finally:
            cur.close()
            conn.close()

def insert_sample_data(num_employees=15):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()

            employee_ids = []
            # First, insert all employees without manager_id
            for _ in range(num_employees):
                name = fake.name()
                position = random.choice(['Developer', 'Manager', 'Analyst', 'Designer', 'Lead'])
                cur.execute(
                    "INSERT INTO Employees (name, position) VALUES (%s, %s) RETURNING employee_id",
                    (name, position)
                )
                employee_id = cur.fetchone()[0]
                employee_ids.append(employee_id)

            # Now assign some employees a manager_id (self-referencing FK)
            for emp_id in employee_ids:
                if random.choice([True, False]):  # 50% chance of having a manager
                    manager_id = random.choice([m for m in employee_ids if m != emp_id])
                    cur.execute(
                        "UPDATE Employees SET manager_id = %s WHERE employee_id = %s",
                        (manager_id, emp_id)
                    )

            conn.commit()
            print(f"Inserted {num_employees} employees with some having managers (self-reference PK→FK)")
        except Exception as e:
            print(f"Error inserting data: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

if __name__ == "__main__":
    create_tables()
    insert_sample_data()
