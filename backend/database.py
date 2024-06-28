import psycopg2
from psycopg2 import sql
from datetime import datetime

DB_NAME = "Sekisho"
DB_USER = "postgres"
DB_PASSWORD = "user%99"
DB_HOST = "localhost"
DB_PORT = "5432"

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
    conn = connect_to_DB()
    if conn:
        try:
            cursor = conn.cursor()
            insert_query = sql.SQL("""
                INSERT INTO appusage (pid, app_name, start_time, end_time, runtime)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (pid, app_name)
                DO UPDATE SET
                    start_time = EXCLUDED.start_time,
                    end_time = EXCLUDED.end_time,
                    runtime = EXCLUDED.runtime
                """)
            print(f"Inserting data: {data}")
            cursor.execute(insert_query, (
                data['pid'],
                data['app_name'],
                data['start_time'],
                data['end_time'],
                data['runtime'],
            ))
            conn.commit()
            cursor.close()
            print("Data insertion successful")
        except Exception as e:
            print(f"Error inserting data: {e}")
        finally:
            conn.close()
    else:
        print("No connection to database")

def fetch_app_usage():
    conn = connect_to_DB()
    if conn:
        try:
            cursor = conn.cursor()
            select_query = sql.SQL("SELECT * FROM appusage")
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