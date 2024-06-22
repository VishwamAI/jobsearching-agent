import sqlite3

def list_tables(database_url):
    try:
        conn = sqlite3.connect(database_url)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables in the database:", tables)
        conn.close()
    except sqlite3.Error as e:
        print(f"Error listing tables: {e}")

if __name__ == "__main__":
    database_url = "data/test_jobsearching_agent.db"
    list_tables(database_url)
