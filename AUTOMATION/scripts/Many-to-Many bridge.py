import psycopg2
from faker import Faker
import random

fake = Faker()

db_params = {
    'dbname': 'automation_test_15',
    'user': 'postgres',
    'password': '2c510254-b82a-4562-9950-ad18e561cdee',
    'host': '207.180.249.216',
    'port': '5433'
}

create_tables_sql = """
-- Parent table 1: Authors
CREATE TABLE IF NOT EXISTS Authors (
    author_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL
);

-- Parent table 2: Books
CREATE TABLE IF NOT EXISTS Books (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL
);

-- Bridge table: AuthorBooks (Many-to-Many)
CREATE TABLE IF NOT EXISTS AuthorBooks (
    author_id INT NOT NULL,
    book_id INT NOT NULL,
    PRIMARY KEY (author_id, book_id),
    FOREIGN KEY (author_id) REFERENCES Authors(author_id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES Books(book_id) ON DELETE CASCADE
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

def insert_sample_data(num_authors=5, num_books=5, num_relations=10):
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()

            # Insert authors
            authors = []
            for _ in range(num_authors):
                first_name = fake.first_name()
                last_name = fake.last_name()
                cur.execute(
                    "INSERT INTO Authors (first_name, last_name) VALUES (%s, %s) RETURNING author_id",
                    (first_name, last_name)
                )
                authors.append(cur.fetchone()[0])

            # Insert books
            books = []
            for _ in range(num_books):
                title = fake.catch_phrase()
                cur.execute(
                    "INSERT INTO Books (title) VALUES (%s) RETURNING book_id",
                    (title,)
                )
                books.append(cur.fetchone()[0])

            # Insert author-book relations
            for _ in range(num_relations):
                author_id = random.choice(authors)
                book_id = random.choice(books)
                cur.execute(
                    "INSERT INTO AuthorBooks (author_id, book_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                    (author_id, book_id)
                )

            conn.commit()
            print(f"Inserted {num_authors} authors, {num_books} books, {num_relations} relations.")
        except Exception as e:
            print(f"Insert error: {e}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()

if __name__ == "__main__":
    create_tables()
    insert_sample_data()
