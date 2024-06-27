import psycopg2
from psycopg2 import sql
from datetime import datetime

DB_NAME = "AppUsageDatabase"
DB_USER = "postgres"
DB_PASSWORD = "12345"
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
        print(conn+"CONNECTED,,,,,")
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def insert_app_usage(data):
    print("trying to connect")
    conn = connect_to_DB()
    if conn:
        try:
            cursor = conn.cursor()
            insert_query = sql.SQL("""
                INSERT INTO appusage (pid, app_name, start_time, end_time, runtime)
                VALUES (%s, %s, %s, %s, %s)
                """)
            print(f"Inserting data: {data}")
            cursor.execute(insert_query, (
                data['id'],
                data['app_name'],
                data['start_time'],
                data['end_time'],
                data['runtime'],
            ))
            conn.commit()
            cursor.close()
        except Exception as e:
            print(f"Error inserting data: {e}")
        finally:
            conn.close()
            print("Data insertion successful")
    else:
        print("No connection to database")

