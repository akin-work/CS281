import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv


def factory_reset() -> None:
    """
    Completely destroys and recreates target database.
    """

    load_dotenv()

    target_db = os.getenv("DB_NAME")
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

            # terminate sessions
            cur.execute("""
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE datname = %s
                AND pid <> pg_backend_pid();
            """, (target_db,))

            # drop db
            cur.execute(
                sql.SQL("DROP DATABASE IF EXISTS {}").format(
                    sql.Identifier(target_db)
                )
            )

            # create db
            cur.execute(
                sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(target_db)
                )
            )

        print(f"Database '{target_db}' recreated successfully")  

    except Exception as e:
        print("Factory reset failed:", e)

    finally:
        if conn:
            conn.close()
            
if __name__ == "__main__":
    factory_reset()