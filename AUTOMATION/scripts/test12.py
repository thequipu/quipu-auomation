import psycopg2
from faker import Faker
import random

fake = Faker()

# PostgreSQL connection parameters
db_params = {
    'dbname': 'automation_test_12',
    'user': 'postgres',
    'password': '2c510254-b82a-4562-9950-ad18e561cdee',
    'host': '207.180.249.216',
    'port': '5433'
}

# SQL for Self Many-to-Many relationship
create_tables_sql = """
-- Main table: Employees
CREATE TABLE IF NOT EXISTS Employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    department VARCHAR(50) NOT NULL
);

-- Bridge table: EmployeeRelations (self many-to-many)
CREATE TABLE IF NOT EXISTS EmployeeRelations (
    mentor_id INT NOT NULL,
    mentee_id INT NOT NULL,
    relation_type VARCHAR(50) NOT NULL,
    PRIMARY KEY (mentor_id, mentee_id),
    CONSTRAINT fk_mentor FOREIGN KEY (mentor_id) REFERENCES Employees(employee_id) ON DELETE CASCADE,
    CONSTRAINT fk_mentee FOREIGN KEY (mentee_id) REFERENCES Employees(employee_id) ON DELETE CASCADE,
    CONSTRAINT chk_not_self CHECK (mentor_id <> mentee_id)
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
            print("Tables created successfully for Self Many-to-Many case")
        except Exception as e:
            print(f"Error creating tables: {e}")
        finally:
            cur.close()
            conn.close()

def insert_sample_data(num_employees=6, num_relations=5):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()

            # Insert employees
            employee_ids = []
            for _ in range(num_employees):
                first_name = fake.first_name()
                last_name = fake.last_name()
                department = random.choice(['IT', 'HR', 'Finance', 'Marketing'])
                cur.execute("""
                    INSERT INTO Employees (first_name, last_name, department)
                    VALUES (%s, %s, %s) RETURNING employee_id
                """, (first_name, last_name, department))
                employee_ids.append(cur.fetchone()[0])

            # Insert relations (self many-to-many)
            for _ in range(num_relations):
                mentor, mentee = random.sample(employee_ids, 2)
                relation_type = random.choice(['Mentorship', 'Collaboration', 'Buddy'])
                cur.execute("""
                    INSERT INTO EmployeeRelations (mentor_id, mentee_id, relation_type)
                    VALUES (%s, %s, %s)
                """, (mentor, mentee, relation_type))

            conn.commit()
            print(f"Inserted {num_employees} employees and {num_relations} relations")
        except Exception as e:
            print(f"Error inserting data: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

if __name__ == "__main__":
    create_tables()
    insert_sample_data()
