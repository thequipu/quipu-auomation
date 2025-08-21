import psycopg2
from faker import Faker
import random

# Initialize Faker
fake = Faker()

# DB connection parameters
db_params = {
    'dbname': 'automation_test_13',
    'user': 'postgres',
    'password': '2c510254-b82a-4562-9950-ad18e561cdee',
    'host': '207.180.249.216',
    'port': '5433'
}

# SQL to create tables
create_tables_sql = """
-- Parent table: Employees
CREATE TABLE IF NOT EXISTS Employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    department VARCHAR(50) NOT NULL
);

-- Child table: Projects
-- Two FKs to same parent table (manager_id, assistant_manager_id)
CREATE TABLE IF NOT EXISTS Projects (
    project_id SERIAL PRIMARY KEY,
    project_name VARCHAR(100) NOT NULL,
    manager_id INT NOT NULL,
    assistant_manager_id INT NOT NULL,
    FOREIGN KEY (manager_id) REFERENCES Employees(employee_id) ON DELETE CASCADE,
    FOREIGN KEY (assistant_manager_id) REFERENCES Employees(employee_id) ON DELETE CASCADE,
    CHECK (manager_id <> assistant_manager_id) -- optional to avoid duplicate person in both roles
);
"""

def connect_db():
    try:
        return psycopg2.connect(**db_params)
    except Exception as e:
        print(f"Error connecting: {e}")
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

def insert_sample_data(num_employees=10, num_projects=5):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()

            # Insert employees
            employees = []
            for _ in range(num_employees):
                first_name = fake.first_name()
                last_name = fake.last_name()
                department = fake.word()
                cur.execute(
                    "INSERT INTO Employees (first_name, last_name, department) VALUES (%s, %s, %s) RETURNING employee_id",
                    (first_name, last_name, department)
                )
                employees.append(cur.fetchone()[0])

            # Insert projects
            for _ in range(num_projects):
                project_name = fake.bs().title()
                manager_id, assistant_manager_id = random.sample(employees, 2)
                cur.execute(
                    "INSERT INTO Projects (project_name, manager_id, assistant_manager_id) VALUES (%s, %s, %s)",
                    (project_name, manager_id, assistant_manager_id)
                )

            conn.commit()
            print(f"Inserted {num_employees} employees and {num_projects} projects")
        except Exception as e:
            print(f"Error inserting data: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

if __name__ == "__main__":
    create_tables()
    insert_sample_data()
