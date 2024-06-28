import time
import psutil
from datetime import datetime, timedelta
import win32gui
import win32process
import psycopg2
from psycopg2 import sql

# PostgreSQL connection parameters
DB_NAME = "Sekisho"
DB_USER = "postgres"
DB_PASSWORD = "user%99"
DB_HOST = "localhost"
DB_PORT = "5432"

# Function to get active window using Win32 API
def get_active_window():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        return process.name()
    except Exception as e:
        return None

# Function to log session data into PostgreSQL
def log_session(conn, app_id, start_time, end_time):
    duration = end_time - start_time
    cursor = conn.cursor()
    insert_query = sql.SQL("""
        INSERT INTO sessions (app_id, start_time, end_time, duration)
        VALUES (%s, %s, %s, %s)
    """)
    cursor.execute(insert_query, (app_id, start_time, end_time, duration))
    conn.commit()
    cursor.close()

# Function to get or create application ID in PostgreSQL
def get_or_create_application(conn, app_name):
    cursor = conn.cursor()
    select_query = sql.SQL("""
        SELECT id FROM applications WHERE name = %s
    """)
    cursor.execute(select_query, (app_name,))
    app_id = cursor.fetchone()
    if app_id:
        return app_id[0]
    else:
        insert_query = sql.SQL("""
            INSERT INTO applications (name) VALUES (%s) RETURNING id
        """)
        cursor.execute(insert_query, (app_name,))
        app_id = cursor.fetchone()[0]
        conn.commit()
        return app_id

# Establish PostgreSQL connection
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    print("Connected to PostgreSQL!")

    current_app = None
    start_time = None

    while True:
        active_window = get_active_window()
        if active_window and active_window != current_app:
            if current_app:
                end_time = datetime.now()
                app_id = get_or_create_application(conn, current_app)
                log_session(conn, app_id, start_time, end_time)
            current_app = active_window
            start_time = datetime.now()
        time.sleep(1)

except psycopg2.Error as e:
    print(f"Error connecting to PostgreSQL: {e}")

except KeyboardInterrupt:
    if current_app:
        end_time = datetime.now()
        app_id = get_or_create_application(conn, current_app)
        log_session(conn, app_id, start_time, end_time)
        conn.close()
        print("Logged sessions to PostgreSQL. Exiting.")

finally:
    if 'conn' in locals() and conn is not None:
        conn.close()
