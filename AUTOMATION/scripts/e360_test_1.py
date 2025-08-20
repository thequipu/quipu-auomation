import psycopg2
from faker import Faker
import random

fake = Faker()

db_params = {
    'dbname': 'e360_test_1',
    'user': 'postgres',
    'password': '2c510254-b82a-4562-9950-ad18e561cdee',
    'host': '207.180.249.216',
    'port': '5433'
}

create_tables_sql = """
-- Drop if exist (to start clean)
DROP TABLE IF EXISTS TableC CASCADE;
DROP TABLE IF EXISTS TableB CASCADE;
DROP TABLE IF EXISTS TableA CASCADE;

-- Table A
CREATE TABLE IF NOT EXISTS TableA (
    a_id SERIAL PRIMARY KEY,
    a_name VARCHAR(50) NOT NULL
);

-- Table B (child of A)
CREATE TABLE IF NOT EXISTS TableB (
    b_id SERIAL PRIMARY KEY,
    a_id INT NOT NULL,
    b_name VARCHAR(50) NOT NULL,
    FOREIGN KEY (a_id) REFERENCES TableA(a_id) ON DELETE CASCADE
);

-- Table C (child of B)
CREATE TABLE IF NOT EXISTS TableC (
    c_id SERIAL PRIMARY KEY,
    b_id INT NOT NULL,
    c_name VARCHAR(50) NOT NULL,
    FOREIGN KEY (b_id) REFERENCES TableB(b_id) ON DELETE CASCADE
);
"""

def connect_db():
    try:
        return psycopg2.connect(**db_params)
    except Exception as e:
        print(f"Connection error: {e}")
        return None

def create_tables():
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(create_tables_sql)
            conn.commit()
            print("Tables created successfully.")
        except Exception as e:
            print(f"Table creation error: {e}")
        finally:
            cur.close()
            conn.close()

def insert_sample_data(num_a=5, num_b=10, num_c=15):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()

            # Insert into TableA
            a_ids = []
            for _ in range(num_a):
                a_name = fake.company()
                cur.execute(
                    "INSERT INTO TableA (a_name) VALUES (%s) RETURNING a_id",
                    (a_name,)
                )
                a_ids.append(cur.fetchone()[0])

            # Insert into TableB (linked to A)
            b_ids = []
            for _ in range(num_b):
                b_name = fake.word()
                a_id = random.choice(a_ids)
                cur.execute(
                    "INSERT INTO TableB (a_id, b_name) VALUES (%s, %s) RETURNING b_id",
                    (a_id, b_name)
                )
                b_ids.append(cur.fetchone()[0])

            # Insert into TableC (linked to B)
            for _ in range(num_c):
                c_name = fake.color_name()
                b_id = random.choice(b_ids)
                cur.execute(
                    "INSERT INTO TableC (b_id, c_name) VALUES (%s, %s)",
                    (b_id, c_name)
                )

            conn.commit()
            print(f"Inserted {num_a} rows into TableA, {num_b} rows into TableB, {num_c} rows into TableC.")
        except Exception as e:
            print(f"Insert error: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

if __name__ == "__main__":
    create_tables()
    insert_sample_data()
