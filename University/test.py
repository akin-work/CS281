import psycopg2
import os
from dotenv import load_dotenv 

def test_connection():
    load_dotenv()
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            sslmode=os.getenv("DB_SSLMODE"),
            channel_binding=os.getenv("DB_CHANNEL_BINDING")
        )
        print("Connection to database successful")
        return connection
    
    except Exception as e:
        print(f"An error occurred while connecting to the database: {e}")
        return None
    
if __name__ == "__main__":
    db_connection = test_connection()
    if db_connection:
        cur = db_connection.cursor()
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        print(f"Database version: {db_version[0]}")