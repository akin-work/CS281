import psycopg2
import os
from dotenv import load_dotenv
from setup import connect_to_db
from load import get_relation_names

def drop_tables(connection):
    try:
        cur = connection.cursor()
        tables = get_relation_names(connection)
        
        for table in tables:
            cur.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
        
        connection.commit()
        print("Tables dropped successfully")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cur.close()
        
if __name__ == "__main__":
    db_connection = connect_to_db()
    if db_connection:
        drop_tables(db_connection)
        db_connection.close()