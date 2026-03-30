import psycopg2
import os
import csv
from tabulate import tabulate
from dotenv import load_dotenv
from setup import connect_to_db

def load_data(connection, relations):
    try:
        cur = connection.cursor()
        for relation in relations:
            with open(f"DATA/{relation}.csv", "r") as f:
                reader = csv.reader(f)
                headers = next(reader)  # column names

                placeholders = ", ".join(["%s"] * len(headers)) #
                columns = ", ".join(headers)

                query = f"""
                INSERT INTO {relation} ({columns})
                VALUES ({placeholders})
                ON CONFLICT DO NOTHING;
                """

                for row in reader:
                    cur.execute(query, row)
        connection.commit()
        print("Data loaded successfully")
    except Exception as e:
        print(f"An error occurred while loading the data: {e}")
    finally:
        cur.close()
                
def show_tables(connection, relations):
    try:
        cur = connection.cursor()
        for relation in relations:
            cur.execute(f"SELECT * FROM {relation};")
            results = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            print(f"Table: {relation}")
            print(tabulate(results, headers=column_names, tablefmt="psql"))
            print("\n")
    except Exception as e:
        print(f"An error occurred while showing the tables: {e}")
    finally:
        cur.close()
        
def get_relation_names(ddl_file="ddl.sql"):
    relations = []
    with open(ddl_file, "r") as f:
        for line in f:
            line = line.strip()
            if line.upper().startswith("CREATE TABLE IF NOT EXISTS"):
                parts = line.split()
                if len(parts) > 5:
                    relation_name = parts[5].rstrip("(")
                    relations.append(relation_name)
    return relations
    
        
if __name__ == "__main__":
    db_connection = connect_to_db()
    if db_connection:
        relations = get_relation_names()
        load_data(db_connection, relations)
        show_tables(db_connection, relations)
        db_connection.close()