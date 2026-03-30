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
    
def create_database(connection):
    # Ensure that the connection is not None before attempting to create the database.
    assert connection is not None, "Connection to database failed. Cannot create database." 
    
    # Attempt to create the 'university' database if it does not already exist.
    try: 
        # Create a cursor object to execute SQL commands.
        cur = connection.cursor() 
        
        # Check if the 'university' database already exists.
        cur.execute("SELECT 1 FROM pg_database WHERE datname='university';") 
        
        # If the 'university' database doe not exist, create it.
        if not cur.fetchone():
            cur.execute("CREATE DATABASE university;") 
            connection.commit() 
            print("Database 'university' created successfully")
        else:
            print("Database 'university' already exists")
        
    except Exception as e:
        print(f"An error occurred while creating the database: {e}")
    finally:
        cur.close()
        
def create_tables(connection):
    try:        
        cur = connection.cursor()
        with open("ddl.sql", "r") as f:
            ddl = f.read()
        cur.execute(ddl)
        connection.commit()
        print("Table created successfully")
    except Exception as e:
        print(f"An error occurred while creating the table: {e}")
    finally:
        cur.close()
        

if __name__ == "__main__":
    db_connection = connect_to_db()
    if db_connection:
        # create_database(db_connection)
        create_tables(db_connection)
        db_connection.close()
