import psycopg2
import os
import csv
from tabulate import tabulate
from dotenv import load_dotenv
from query import execute_query
from setup import connect_to_db, create_database, create_tables

    
def connect_as_user(username, password):
    load_dotenv()
    
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=username,
            password=password,
            sslmode=os.getenv("DB_SSLMODE"),
            channel_binding=os.getenv("DB_CHANNEL_BINDING")
        )
        print(f"Connection to database as {username} successful")
        return connection
    except Exception as e:
        print(f"An error occurred while connecting to the database as {username}: {e}")
        return None

if __name__ == "__main__":
    db = connect_to_db()
    # create_database(db)
    # create_tables(db)
    query = """CREATE ROLE cs_instructor LOGIN PASSWORD 'instructor123';
                CREATE VIEW cs_students AS SELECT * FROM student WHERE dept_name = 'Comp. Sci.';
                GRANT SELECT ON cs_students TO cs_instructor;"""
        
    execute_query(db, query)
    db.close()
    
    db = connect_as_user("cs_instructor", "instructor123")
    if db:
        query = "SELECT * FROM cs_students;"
        execute_query(db, query)
        db.close()
        
    db = connect_to_db()
    query = """
        DROP VIEW IF EXISTS cs_students;
        DROP ROLE IF EXISTS cs_instructor;
    """
    execute_query(db, query)
    db.close()