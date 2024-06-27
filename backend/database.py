import psycopg2
from psycopg2 import sql
from datetime import datetime
from psycopg2.extras import RealDictCursor

DB_NAME = "AppUsageDatabase"
DB_USER = "postgres"
DB_PASSWORD = "12345"
DB_HOST = "localhost"
DB_PORT = "5433"

def connect_to_DB():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def insert_app_usage(data):
    print("trying to connect")
    conn = connect_to_DB()
    if conn:
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = "SELECT * FROM table1;"  # Replace with your actual query
            cursor.execute(query)
            data = cursor.fetchall()
            return data
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
        finally:
            conn.close()
    else:
        return None

def fetch_app_usage():
    conn = connect_to_DB()
    if conn:
        try:
            cursor = conn.cursor()
            select_query = sql.SQL("SELECT * FROM table1")
            cursor.execute(select_query)
            records = cursor.fetchall()
            cursor.close()
            print("Data fetched successful")
            return records
        except Exception as e:
            print(f"Error fetching data: {e}")
            return []
        finally:
            conn.close()
    else:
        print("No connection to database")
        return []