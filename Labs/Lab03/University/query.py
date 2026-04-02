import psycopg2
import os
import csv
from tabulate import tabulate
from dotenv import load_dotenv
from setup import connect_to_db
from load import show_tables

from tabulate import tabulate

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
    db_connection = connect_to_db()
    if db_connection:
        query = """
            SELECT * FROM student
            NATURAL JOIN takes;
        """
        execute_query(db_connection, query)
        db_connection.close()
        