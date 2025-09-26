import psycopg2
from config import DB_CONFIG

def get_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        print(f"DB connection error: {e}")
        return None

def run_query(sql, many=False):
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        if many:
            cur.executemany(sql)
        else:
            cur.execute(sql)
        conn.commit()
    except Exception as e:
        print(f"Query execution error: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()
