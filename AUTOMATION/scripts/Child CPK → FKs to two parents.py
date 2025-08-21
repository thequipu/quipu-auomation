import psycopg2
from faker import Faker
import random

# Initialize Faker
fake = Faker()

# DB connection parameters
db_params = {
    'dbname': 'automation_test_14',
    'user': 'postgres',
    'password': '2c510254-b82a-4562-9950-ad18e561cdee',
    'host': '207.180.249.216',
    'port': '5433'
}

# SQL to create tables
create_tables_sql = """
-- Parent table 1: Students
CREATE TABLE IF NOT EXISTS Students (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);

-- Parent table 2: Courses
CREATE TABLE IF NOT EXISTS Courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL
);

-- Child table: Enrollments
-- Composite PK (student_id, course_id) where each col is FK to different parents
CREATE TABLE IF NOT EXISTS Enrollments (
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    enrollment_date DATE NOT NULL,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES Courses(course_id) ON DELETE CASCADE
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
            print("Table created successfully")
        except Exception as e:
            print(f"Error creating tables: {e}")
        finally:
            cur.close()
            conn.close()

def insert_sample_data(num_students=5, num_courses=5, num_enrollments=10):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()

            # Insert students
            students = []
            for _ in range(num_students):
                first_name = fake.first_name()
                last_name = fake.last_name()
                cur.execute(
                    "INSERT INTO Students (first_name, last_name) VALUES (%s, %s) RETURNING student_id",
                    (first_name, last_name)
                )
                students.append(cur.fetchone()[0])

            # Insert courses
            courses = []
            for _ in range(num_courses):
                course_name = fake.catch_phrase()
                cur.execute(
                    "INSERT INTO Courses (course_name) VALUES (%s) RETURNING course_id",
                    (course_name,)
                )
                courses.append(cur.fetchone()[0])

            # Insert enrollments (CPK with 2 different parent FKs)
            for _ in range(num_enrollments):
                student_id = random.choice(students)
                course_id = random.choice(courses)
                enrollment_date = fake.date_this_year()
                cur.execute(
                    "INSERT INTO Enrollments (student_id, course_id, enrollment_date) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                    (student_id, course_id, enrollment_date)
                )

            conn.commit()
            print(f"Inserted {num_students} students, {num_courses} courses, and {num_enrollments} enrollments")
        except Exception as e:
            print(f"Error inserting data: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

if __name__ == "__main__":
    create_tables()
    insert_sample_data()
