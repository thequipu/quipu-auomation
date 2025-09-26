from db_utils import run_query
from queries import SCHEMA_SQL, DATA_SQL

def main():
    run_query(SCHEMA_SQL)
    print("✅ Schema created.")

    run_query(DATA_SQL)
    print("✅ Sample data inserted.")

if __name__ == "__main__":
    main()
