import psycopg2
from faker import Faker
import random

# Initialize Faker
fake = Faker()

# PostgreSQL connection parameters
db_params = {
    'dbname': 'automation_test_9',
    'user': 'postgres',
    'password': '2c510254-b82a-4562-9950-ad18e561cdee',
    'host': '207.180.249.216',
    'port': '5433'
}

# SQL to create self-referencing CPK table
create_tables_sql = """
-- Projects table with self-referencing Composite FK
CREATE TABLE IF NOT EXISTS Projects (
    project_id INTEGER NOT NULL,
    version_no INTEGER NOT NULL,
    project_name VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    parent_project_id INTEGER,
    parent_version_no INTEGER,
    PRIMARY KEY (project_id, version_no),
    FOREIGN KEY (parent_project_id, parent_version_no)
        REFERENCES Projects(project_id, version_no)
        ON DELETE SET NULL
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
            print("Table created successfully (Self-reference CPK→CFK)")
        except Exception as e:
            print(f"Error creating table: {e}")
        finally:
            cur.close()
            conn.close()

def insert_sample_data(num_projects=5, versions_per_project=3):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()

            # Keep list of all inserted composite keys
            project_versions = []

            # Insert all projects and versions
            for project_id in range(1, num_projects + 1):
                for version_no in range(1, versions_per_project + 1):
                    project_name = f"Project {project_id} v{version_no}"
                    start_date = fake.date_between(start_date='-2y', end_date='today')

                    # Decide parent version for version_no > 1
                    if version_no > 1:
                        parent_project_id = project_id
                        parent_version_no = version_no - 1
                    else:
                        parent_project_id = None
                        parent_version_no = None

                    cur.execute(
                        "INSERT INTO Projects (project_id, version_no, project_name, start_date, parent_project_id, parent_version_no) VALUES (%s, %s, %s, %s, %s, %s)",
                        (project_id, version_no, project_name, start_date, parent_project_id, parent_version_no)
                    )

                    project_versions.append((project_id, version_no))

            conn.commit()
            print(f"Inserted {len(project_versions)} project-version records with self-referencing CPK→CFK")
        except Exception as e:
            print(f"Error inserting data: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

if __name__ == "__main__":
    create_tables()
    insert_sample_data()
