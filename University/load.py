import psycopg2
import os
import csv
from tabulate import tabulate
from dotenv import load_dotenv
from setup import connect_to_db

def load_data(connection, relations, data_dir="DATA"):
    try:
        with connection.cursor() as cur:
            for relation in relations:
                csv_file = f"{data_dir}/{relation}.csv"
                with open(csv_file, "r") as f:
                    reader = csv.reader(f)
                    headers = next(reader)  # skip header row
                    for row in reader:
                        placeholders = ", ".join(["%s"] * len(row))
                        insert_query = f"INSERT INTO {relation} ({', '.join(headers)}) VALUES ({placeholders});"
                        cur.execute(insert_query, row)
        connection.commit()
        print("Data loaded successfully")
    except Exception as e:
        print(f"An error occurred while loading the data: {e}")
                
def show_tables(connection, relations):
    try:
        with connection.cursor() as cur:
            for relation in relations:
                cur.execute(f"SELECT * FROM {relation};")
                results = cur.fetchall()
                column_names = [desc[0] for desc in cur.description]
                print(f"Table: {relation}")
                print(tabulate(results, headers=column_names, tablefmt="psql"))
                print("\n")
    except Exception as e:
        print(f"An error occurred while showing the tables: {e}")
        
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