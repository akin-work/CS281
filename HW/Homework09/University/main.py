import psycopg2
import os
from tabulate import tabulate
from dotenv import load_dotenv
    
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

def execute_query(connection, query):
    try:
        with connection.cursor() as cur:
            cur.execute(query)

            # Check if the query returned rows (SELECT)
            if cur.description:
                results = cur.fetchall()
                column_names = [desc[0] for desc in cur.description]
                print(tabulate(results, headers=column_names, tablefmt="psql"))
                return results
            else:
                # For INSERT/UPDATE/DELETE/DROP/CREATE, etc.
                connection.commit()  # commit changes
                print(f"Query executed successfully: {cur.rowcount} rows affected")
                return cur.rowcount
    except Exception as e:
        connection.rollback()
        print(f"An error occurred while executing the query: {e}")
        return None

if __name__ == "__main__":
    load_dotenv()
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    db = connect_as_user(username, password)
    
    query = """
        CREATE ROLE cs_instructor LOGIN PASSWORD 'instructor123';
        CREATE VIEW cs_students AS SELECT * FROM student WHERE dept_name = 'Comp. Sci.';
        GRANT SELECT ON cs_students TO cs_instructor;
        GRANT SELECT ON student TO cs_instructor;
    """
        
    execute_query(db, query)
    db.close()
    
    db = connect_as_user("cs_instructor", "instructor123")
    if db:
        
        queries = [
            "SELECT * FROM student;",
            "SELECT * FROM cs_students;"
        ]
        for query in queries:
            execute_query(db, query)

        db.close()
        
    db = connect_as_user(username, password)
    query = """
        DROP VIEW IF EXISTS cs_students;
        REVOKE SELECT ON student FROM cs_instructor;
        DROP ROLE IF EXISTS cs_instructor;
    """
    execute_query(db, query)
    db.close()