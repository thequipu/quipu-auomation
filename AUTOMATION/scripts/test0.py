import psycopg2

# ==== CONFIG ====
DB_NAME = "automation_test_0"
DB_USER = "postgres"
DB_PASS = "2c510254-b82a-4562-9950-ad18e561cdee"
DB_HOST = "207.180.249.216"
DB_PORT = "5433"

# ==== MERGED SCHEMA ====
SCHEMA_SQL = """
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

-- Table definitions (from previous message)
-- Master Entity Table (used for multiple PK → FK cases)
CREATE TABLE Person (
    person_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE
);

-- 1. Parent PK → Child FK (1 col → 1 col)
CREATE TABLE Employee (
    emp_id SERIAL PRIMARY KEY,
    manager_id INT REFERENCES Person(person_id)  -- 1:1 PK→FK
);

-- 2. Parent PK → Child CFK (1 col → many cols, one matches PK)
CREATE TABLE ProjectAssignment (
    assignment_id SERIAL PRIMARY KEY,
    person_ref INT NOT NULL,
    dept_code VARCHAR(20),
    FOREIGN KEY (person_ref) REFERENCES Person(person_id)
);

-- 3. Parent CPK → Child CFK (exact col match)
CREATE TABLE Department (
    dept_id INT,
    branch_id INT,
    dept_name VARCHAR(50),
    PRIMARY KEY (dept_id, branch_id)
);

CREATE TABLE DeptEmployee (
    dept_id INT,
    branch_id INT,
    emp_no SERIAL,
    PRIMARY KEY (dept_id, branch_id, emp_no),
    FOREIGN KEY (dept_id, branch_id) REFERENCES Department(dept_id, branch_id)
);

-- 4. Parent CPK → Child FK (partial reference)
CREATE TABLE Branch (
    branch_id INT PRIMARY KEY,
    branch_name VARCHAR(50)
);

CREATE TABLE BranchDeptNote (
    dept_id INT,
    branch_id INT REFERENCES Branch(branch_id),
    note TEXT
);

-- 5. Parent Non-PK (Unique) → Child FK
CREATE TABLE Customer (
    customer_id SERIAL PRIMARY KEY,
    customer_code VARCHAR(20) UNIQUE
);

CREATE TABLE CustomerOrder (
    order_id SERIAL PRIMARY KEY,
    customer_code VARCHAR(20) REFERENCES Customer(customer_code)
);

-- 6. Parent PK → Child FK where child PK is same column (1-to-1 relation)
CREATE TABLE Profile (
    person_id INT PRIMARY KEY REFERENCES Person(person_id),
    bio TEXT
);

-- 7. Parent CPK → Child CFK where child CPK is same set
CREATE TABLE Course (
    course_id INT,
    semester_id INT,
    course_name VARCHAR(50),
    PRIMARY KEY (course_id, semester_id)
);

CREATE TABLE CourseSchedule (
    course_id INT,
    semester_id INT,
    schedule_time VARCHAR(50),
    PRIMARY KEY (course_id, semester_id),
    FOREIGN KEY (course_id, semester_id) REFERENCES Course(course_id, semester_id)
);

-- 8. Self-reference PK → FK
CREATE TABLE Category (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(50),
    parent_category_id INT REFERENCES Category(category_id)
);

-- 9. Self-reference CPK → CFK
CREATE TABLE Location (
    loc_id INT,
    zone_id INT,
    loc_name VARCHAR(50),
    PRIMARY KEY (loc_id, zone_id),
    parent_loc_id INT,
    parent_zone_id INT,
    FOREIGN KEY (parent_loc_id, parent_zone_id) REFERENCES Location(loc_id, zone_id)
);

-- 10. Mixed: FK to PK + FK to another table
CREATE TABLE Task (
    task_id SERIAL PRIMARY KEY,
    person_id INT REFERENCES Person(person_id),
    dept_id INT,
    branch_id INT,
    FOREIGN KEY (dept_id, branch_id) REFERENCES Department(dept_id, branch_id)
);

-- 11. Unique multi-col → CFK
CREATE TABLE Vendor (
    vendor_id SERIAL PRIMARY KEY,
    vendor_code VARCHAR(20),
    country_code VARCHAR(5),
    UNIQUE (vendor_code, country_code)
);

CREATE TABLE VendorContract (
    contract_id SERIAL PRIMARY KEY,
    vendor_code VARCHAR(20),
    country_code VARCHAR(5),
    FOREIGN KEY (vendor_code, country_code) REFERENCES Vendor(vendor_code, country_code)
);

-- 12. Self Many-to-Many
CREATE TABLE Friendship (
    person_id1 INT,
    person_id2 INT,
    PRIMARY KEY (person_id1, person_id2),
    FOREIGN KEY (person_id1) REFERENCES Person(person_id),
    FOREIGN KEY (person_id2) REFERENCES Person(person_id)
);

-- 13. Two FKs to same parent table
CREATE TABLE Match (
    match_id SERIAL PRIMARY KEY,
    home_team_id INT REFERENCES Person(person_id),
    away_team_id INT REFERENCES Person(person_id)
);

-- 14. Child CPK → FKs to two parents
CREATE TABLE Author (
    author_id SERIAL PRIMARY KEY,
    author_name VARCHAR(50)
);

CREATE TABLE Book (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(100)
);

CREATE TABLE AuthorBookPK (
    author_id INT,
    book_id INT,
    PRIMARY KEY (author_id, book_id),
    FOREIGN KEY (author_id) REFERENCES Author(author_id),
    FOREIGN KEY (book_id) REFERENCES Book(book_id)
);

-- 15. Many-to-Many bridge
CREATE TABLE Student (
    student_id SERIAL PRIMARY KEY,
    student_name VARCHAR(50)
);

CREATE TABLE Club (
    club_id SERIAL PRIMARY KEY,
    club_name VARCHAR(50)
);

CREATE TABLE StudentClub (
    student_id INT,
    club_id INT,
    PRIMARY KEY (student_id, club_id),
    FOREIGN KEY (student_id) REFERENCES Student(student_id),
    FOREIGN KEY (club_id) REFERENCES Club(club_id)
);

-- 16. Many-to-Many with extra attributes
CREATE TABLE Movie (
    movie_id SERIAL PRIMARY KEY,
    title VARCHAR(100)
);

CREATE TABLE Actor (
    actor_id SERIAL PRIMARY KEY,
    actor_name VARCHAR(50)
);

CREATE TABLE MovieActor (
    movie_id INT,
    actor_id INT,
    role_name VARCHAR(50),
    PRIMARY KEY (movie_id, actor_id),
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id),
    FOREIGN KEY (actor_id) REFERENCES Actor(actor_id)
);

"""

# ==== SAMPLE DATA ====
DATA_SQL = """
-- Person
INSERT INTO Person (name, email) VALUES
('Alice', 'alice@example.com'),
('Bob', 'bob@example.com'),
('Charlie', 'charlie@example.com');

-- Employee
INSERT INTO Employee (manager_id) VALUES (1), (2);

-- ProjectAssignment
INSERT INTO ProjectAssignment (person_ref, dept_code) VALUES
(1, 'HR'), (2, 'ENG');

-- Department
INSERT INTO Department (dept_id, branch_id, dept_name) VALUES
(1, 101, 'HR'),
(2, 102, 'Engineering');

-- DeptEmployee
INSERT INTO DeptEmployee (dept_id, branch_id, emp_no) VALUES
(1, 101, 1),
(2, 102, 2);

-- Branch
INSERT INTO Branch (branch_id, branch_name) VALUES
(101, 'HQ'),
(102, 'Remote');

-- BranchDeptNote
INSERT INTO BranchDeptNote (dept_id, branch_id, note) VALUES
(1, 101, 'HQ HR Note'),
(2, 102, 'Remote ENG Note');

-- Customer
INSERT INTO Customer (customer_code) VALUES ('CUST001'), ('CUST002');

-- CustomerOrder
INSERT INTO CustomerOrder (customer_code) VALUES ('CUST001'), ('CUST002');

-- Profile
INSERT INTO Profile (person_id, bio) VALUES
(1, 'Manager bio'), (2, 'Developer bio');

-- Course
INSERT INTO Course (course_id, semester_id, course_name) VALUES
(1, 2024, 'Math'), (2, 2024, 'Physics');

-- CourseSchedule
INSERT INTO CourseSchedule (course_id, semester_id, schedule_time) VALUES
(1, 2024, 'Mon 9am'),
(2, 2024, 'Tue 10am');

-- Category
INSERT INTO Category (category_name, parent_category_id) VALUES
('Electronics', NULL),
('Mobiles', 1);

-- Location
INSERT INTO Location (loc_id, zone_id, loc_name, parent_loc_id, parent_zone_id) VALUES
(1, 1, 'Main Zone', NULL, NULL),
(2, 1, 'Sub Zone', 1, 1);

-- Task
INSERT INTO Task (person_id, dept_id, branch_id) VALUES
(1, 1, 101),
(2, 2, 102);

-- Vendor
INSERT INTO Vendor (vendor_code, country_code) VALUES
('V001', 'US'),
('V002', 'IN');

-- VendorContract
INSERT INTO VendorContract (vendor_code, country_code) VALUES
('V001', 'US'),
('V002', 'IN');

-- Friendship
INSERT INTO Friendship (person_id1, person_id2) VALUES
(1, 2),
(2, 3);

-- Match
INSERT INTO Match (home_team_id, away_team_id) VALUES
(1, 2),
(2, 3);

-- Author
INSERT INTO Author (author_name) VALUES ('Author A'), ('Author B');

-- Book
INSERT INTO Book (title) VALUES ('Book 1'), ('Book 2');

-- AuthorBookPK
INSERT INTO AuthorBookPK (author_id, book_id) VALUES
(1, 1),
(2, 2);

-- Student
INSERT INTO Student (student_name) VALUES ('Stu1'), ('Stu2');

-- Club
INSERT INTO Club (club_name) VALUES ('Chess'), ('Drama');

-- StudentClub
INSERT INTO StudentClub (student_id, club_id) VALUES
(1, 1),
(2, 2);

-- Movie
INSERT INTO Movie (title) VALUES ('Movie 1'), ('Movie 2');

-- Actor
INSERT INTO Actor (actor_name) VALUES ('Actor 1'), ('Actor 2');

-- MovieActor
INSERT INTO MovieActor (movie_id, actor_id, role_name) VALUES
(1, 1, 'Lead'),
(2, 2, 'Supporting');
"""

# ==== MAIN EXECUTION ====
def main():
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS,
        host=DB_HOST, port=DB_PORT
    )
    cur = conn.cursor()
    
    # Create schema
    cur.execute(SCHEMA_SQL)
    conn.commit()
    print("✅ Schema created.")

    # Insert sample data
    cur.execute(DATA_SQL)
    conn.commit()
    print("✅ Sample data inserted.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
