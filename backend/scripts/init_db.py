import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app.core.config import settings
import sys

def init_db():
    try:
        # If DATABASE_URL is set (e.g. Supabase), just try to connect to verify
        if settings.DATABASE_URL:
            print(f"Connecting to provided DATABASE_URL: {settings.DATABASE_URL.split('@')[-1]}") # Hide auth details
            conn = psycopg2.connect(settings.DATABASE_URL)
            conn.close()
            print("Connection successful.")
            return

        # Local setup: Connect to default 'postgres' database to create new db
        conn = psycopg2.connect(
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_SERVER,
            port=settings.POSTGRES_PORT,
            dbname="postgres"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Check if database exists
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{settings.POSTGRES_DB}'")
        exists = cur.fetchone()
        
        if not exists:
            cur.execute(f"CREATE DATABASE {settings.POSTGRES_DB}")
            print(f"Database {settings.POSTGRES_DB} created successfully.")
        else:
            print(f"Database {settings.POSTGRES_DB} already exists.")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_db()
