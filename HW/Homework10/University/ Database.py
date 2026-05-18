import psycopg2
import sql from psycopg2
import os
import tabulate from tabulate
import load_dotenv from dotenv


class Database:
    def __init__(self, ddl_file: str = "ddl.sql", data_dir="DATA") -> None:
        self.connection = None
        self.ddl_file = ddl_file
        self.data_dir = data_dir
        self.relations = []

def connect(self, username: str = None, password: str = None) -> None:
     user = os.getenv("DB_USER") if username is None else username
    password = os.getenv("DB_PASSWORD") if password is None else password


    self.connection = psycopg2.connect(
        user=user,
        password=password

def close(self) -> None:

 if self.connection is not None:
        self.connection.close()
        self.connection = None

    self.relations = []

    def __enter__(self) -> “Database”:
        self.connect()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

        def get_relations(self) -> list[str]:
            return get_relation_names(self.connection, self.ddl_file)

        def create_tables(self) -> None:
            try:
        create_tables(self.connection, self.ddl_file)

        self.relations = self.get_relations()
       
        def load_data(self) -> None:
            try:
        load_data(self.connection, self.relations, self.data_dir)
        def setup(self) -> None:
            self.create_tables()
            self.load_data()
            def execute_query(self, query) -> None:
                return exectue_query(self.connection,query)
            def show_tables(self) -> None:
              try:
        with self.connection.cursor() as cur:

            for relation in self.get_relations():

                cur.execute(f"SELECT * FROM {relation};")

                results = cur.fetchall()

                column_names = [desc[0] for desc in cur.description]

                print(f"Table: {relation}")

                print(tabulate(results,
                               headers=column_names,
                               tablefmt="psql"))

                print("\n")  
                except Exception as e:
        print(f"An error occurred while showing the tables: {e}"
        def drop_tables(self) -> None:
            try:
                drop_tables(self.connection)
                self.relations = []
                def version(self) -> None:
                    version(self.connection)
        def reset_tables(self) -> None:
            self.drop_tables()
            self.create_tables()
            self.load_data()
        def factory_reset(self) -> None:
            try:
        if self.connection is not None:
            self.connection.close()
            
            finally:
            self.connect()
            self.setup()
            def show_schema(self) -> None:
                if not self.connection:
        print("No database connection")
        return
        
         try:
            with self.connection.cursor() as cur:
                for table in self.get_relations():
                    cur.execute("""
                        SELECT column_name, data_type, is_nullable
                        FROM information_schema.columns
                        WHERE table_name = %s
                        ORDER BY ordinal_position;
                    """, (table,))

                columns = cur.fetchall()

                print(f"\nTable: {table}")
                print(tabulate(columns, headers=[
                    "Column", "Type", "Nullable"
                ], tablefmt="psql"))
    @staticmethod
def create_database(db_name: str) -> None:
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
            cur.execute(
                f"SELECT 1 FROM pg_database WHERE datname='{db_name}';"
            )

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
    @staticmethod
def drop_database(db_name: str) -> None:
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
        
    

''' JS
2.2: incomplete - 0.5
2.6: incorrect - 0.5
2.7: incorrect - 0.5
2.8: incorrect - 0.5
2.10: incorrect - 0.5
2.12: incorrect - 0.5
2.13: incorrect - 0.5
2.15: incorrect - 0.5
2.16: incorrect - 0.5

Libraries not imported properly.
Multiple allignment issues.
-0.5
'''