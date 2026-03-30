import psycopg2
import os
import csv
from tabulate import tabulate
from dotenv import load_dotenv
from setup import connect_to_db
from load import show_tables

def execute_query(connection, query):
    try:
        cur = connection.cursor()
        cur.execute(query)
        results = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        print(tabulate(results, headers=column_names, tablefmt="psql"))
        return results
    except Exception as e:
        print(f"An error occurred while executing the query: {e}")
        return None
    finally:
        cur.close()
        
if __name__ == "__main__":
    db_connection = connect_to_db()
    if db_connection:
        query = """
            SELECT * FROM student
            NATURAL JOIN takes;
        """
        execute_query(db_connection, query)
        db_connection.close()
        