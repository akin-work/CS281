import psycopg2
import os
from dotenv import load_dotenv 
from setup import connect_to_db

def version(connection):
    try:
        with connection.cursor() as cur:
            cur.execute("SELECT version();")
            db_version = cur.fetchone()[0]
            print(f"Database version: {db_version}")
    except Exception as e:
        print(f"An error occurred while fetching the database version: {e}")
    
if __name__ == "__main__":
    db_connection = connect_to_db()
    version(db_connection)
    db_connection.close()