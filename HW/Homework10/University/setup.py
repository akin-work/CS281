import psycopg2
import os
from dotenv import load_dotenv 

def connect_to_db():
    # Load environment variables from .env file
    load_dotenv()   
    
    # Attempt to connect to the database using the environment variables
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
    
    # Print an error message if the connection fails and return None
    except Exception as e: 
        print(f"An error occurred while connecting to the database: {e}")
        return None 
    
def create_database(db_name):
    load_dotenv()
    admin_db = os.getenv("ADMIN_DB", "postgres")
    
    conn = None
    
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=admin_db,
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            sslmode=os.getenv("DB_SSLMODE"),
            channel_binding=os.getenv("DB_CHANNEL_BINDING")
        )
        conn.autocommit = True
        
        with conn.cursor() as cur:
            cur.execute(f"SELECT 1 FROM pg_database WHERE datname='{db_name}';") 
            if not cur.fetchone():
                cur.execute(f"CREATE DATABASE {db_name};") 
                print(f"Database '{db_name}' created successfully")
            else:
                print(f"Database '{db_name}' already exists")
    except Exception as e:
        print(f"An error occurred while creating the database: {e}")
    finally:
        if conn:
            conn.close()
            
def drop_database(db_name):
    load_dotenv()
    admin_db = os.getenv("ADMIN_DB", "postgres")
    
    conn = None
    
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=admin_db,
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            sslmode=os.getenv("DB_SSLMODE"),
            channel_binding=os.getenv("DB_CHANNEL_BINDING")
        )
        conn.autocommit = True
        
        with conn.cursor() as cur:
            cur.execute(f"SELECT 1 FROM pg_database WHERE datname='{db_name}';") 
            if cur.fetchone():
                cur.execute(f"DROP DATABASE {db_name};") 
                print(f"Database '{db_name}' dropped successfully")
            else:
                print(f"Database '{db_name}' does not exist")
    except Exception as e:
        print(f"An error occurred while dropping the database: {e}")
    finally:
        if conn:
            conn.close()
        
def create_tables(connection):
    try:        
        with connection.cursor() as cur:
            with open("ddl.sql", "r") as f:
                ddl = f.read()
            cur.execute(ddl)
            connection.commit()
            print("Table created successfully")
    except Exception as e:
        print(f"An error occurred while creating the table: {e}")
        

if __name__ == "__main__":
    db_connection = connect_to_db()
    if db_connection:
        create_database(db_connection)
        create_tables(db_connection)
        db_connection.close()
