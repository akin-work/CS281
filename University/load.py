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
                cur.execute(f"SELECT COUNT(*) FROM {relation};")
                count = cur.fetchone()[0]
                if count > 0:
                    continue
                
                csv_file = f"{data_dir}/{relation}.csv"
                
                if not os.path.isfile(csv_file):
                    print(f"CSV file for relation '{relation}' not found at '{csv_file}'. Skipping.")
                    continue
                
                with open(csv_file, "r") as f:
                    try:
                        cur.copy_expert(f"COPY {relation} FROM STDIN WITH CSV HEADER", f)
                    except Exception as e:
                        print(f"Error loading data for relation '{relation}': {e}")
                        continue
        connection.commit()
        print("Data loaded successfully")
    except Exception as e:
        connection.rollback()
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
        
def get_relation_names(connection, ddl_file="ddl.sql"):
    with connection.cursor() as cur:
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE';
        """)
        table_names = set([row[0] for row in cur.fetchall()])
    relations = []
    with open(ddl_file, "r") as f:
        for line in f:
            line = line.strip()
            if line.upper().startswith("CREATE TABLE IF NOT EXISTS"):
                parts = line.split()
                if len(parts) > 5:
                    relation_name = parts[5].rstrip("(")
                    relations.append(relation_name)
    return [rel for rel in relations if rel in table_names]
    
        
if __name__ == "__main__":
    db_connection = connect_to_db()
    if db_connection:
        relations = get_relation_names(db_connection)
        load_data(db_connection, relations)
        show_tables(db_connection, relations)
        db_connection.close()