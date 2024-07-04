import time
import psycopg2
from psycopg2 import sql
import matplotlib.pyplot as plt
import seaborn as sns
from pynput import mouse
from datetime import datetime
import pandas as pd

# PostgreSQL connection parameters
DB_NAME = "Sekisho"
DB_USER = "postgres"
DB_PASSWORD = "user%99"
DB_HOST = "localhost"
DB_PORT = "5432"

# Function to establish PostgreSQL connection
def get_db_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

# Function to create cursor data table in PostgreSQL
def create_cursor_data_table(conn):
    cursor = conn.cursor()
    create_table_query = """
        CREATE TABLE IF NOT EXISTS cursor_data (
            id SERIAL PRIMARY KEY,
            x INT NOT NULL,
            y INT NOT NULL,
            clicked BOOLEAN DEFAULT FALSE,
            capture_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            app_id INT REFERENCES applications(id)
        )
    """
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()

# Function to insert cursor data into PostgreSQL
def insert_cursor_data(conn, x, y, clicked, app_id):
    cursor = conn.cursor()
    insert_query = sql.SQL("""
        INSERT INTO cursor_data (x, y, clicked, capture_time, app_id)
        VALUES (%s, %s, %s, %s, %s)
    """)
    cursor.execute(insert_query, (x, y, clicked, datetime.now(), app_id))
    conn.commit()
    cursor.close()

# Function to get the current app_id
def get_current_app_id(conn):
    cursor = conn.cursor()
    query = """
        SELECT app_id
        FROM sessions
        WHERE start_time <= NOW()
        AND end_time >= NOW()
        ORDER BY start_time
    """
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

# Function to capture cursor movements and clicks
def on_move(x, y):
    app_id = get_current_app_id(conn)
    if app_id is not None:
        insert_cursor_data(conn, x, y, False, app_id)
        print(f'Mouse moved to ({x}, {y})')

def on_click(x, y, button, pressed):
    app_id = get_current_app_id(conn)
    if app_id is not None:
        if pressed:
            insert_cursor_data(conn, x, y, True, app_id)
            print(f'Mouse clicked at ({x}, {y})')

# Main function to collect cursor data and create heatmap
def collect_data_and_create_heatmap():
    global conn
    try:
        # Establish PostgreSQL connection
        conn = get_db_connection()
        print("Connected to PostgreSQL!")

        # Create cursor data table if not exists
        create_cursor_data_table(conn)
        print("Cursor data table created/verified.")

        # Start listening to mouse events
        with mouse.Listener(on_move=on_move, on_click=on_click) as listener:
            print("Listening to mouse events...")
            listener.join()

    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")

    finally:
        if 'conn' in globals() and conn is not None:
            conn.close()
            print("PostgreSQL connection closed.")

        # Create heatmap using collected data
        create_heatmap()

# Function to create heatmap using collected cursor data
def create_heatmap():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query to fetch cursor data with app_id and coordinates
        query = """
            SELECT cd.x, cd.y, cd.app_id, a.name AS app_name
            FROM cursor_data cd
            JOIN applications a ON cd.app_id = a.id
        """
        cursor.execute(query)
        cursor_data = cursor.fetchall()
        conn.close()

        if not cursor_data:
            print("No data returned from the query.")
            return

        # Convert cursor data to DataFrame for seaborn heatmap
        cursor_df = pd.DataFrame(cursor_data, columns=['x', 'y', 'app_id', 'app_name'])

        # Iterate over each unique app_id
        for app_id in cursor_df['app_id'].unique():
            app_df = cursor_df[cursor_df['app_id'] == app_id]
        for app_name in cursor_df['app_name'].unique():
            app_df = cursor_df[cursor_df['app_name'] == app_name]

            plt.figure(figsize=(15, 10))
            sns.set(style="whitegrid")
            plt.title(f"Cursor heatmap for App {app_name}")

            sns.kdeplot(x=app_df['x'], y=app_df['y'], cmap="Reds", cbar=True, fill=True, thresh=0.1, warn_singular=False)
            plt.xlabel('X position')
            plt.ylabel('Y position')
            plt.tight_layout()
            plt.show()
            plt.close()

    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")

def create_daily_heatmap():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT cd.x, cd.y, cd.app_id, a.name as app_name, DATE(cd.capture_time) AS capture_date
            FROM cursor_data cd
            JOIN applications a ON a.id = cd.app_id
        """
        cursor.execute(query)
        cursor_data = cursor.fetchall()
        conn.close()

        if not cursor_data:
            print("No data returned from query")
            return

        cursor_df = pd.DataFrame(cursor_data, columns=['x', 'y', 'app_id', 'app_name', 'capture_date'])

        for (capture_date, app_id) in cursor_df.groupby(['capture_date', 'app_id']).groups.keys():
            daily_df = cursor_df[(cursor_df['capture_date'] == capture_date) & (cursor_df['app_id'] == app_id)]
            app_name = daily_df['app_name'].iloc[0]

            plt.figure(figsize=(8, 8))
            sns.set(style="whitegrid")
            plt.title(f"Cursor heatmap for App {app_name} on date {capture_date}")

            sns.kdeplot(x=daily_df['x'], y=daily_df['y'], cmap="Reds", cbar=True, fill=True, thresh=0.1, warn_singular=False)
            plt.xlabel('X position')
            plt.ylabel('Y position')
            plt.tight_layout()
            plt.show()
            plt.close()

    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")


if __name__ == '__main__':
    # create_heatmap()
    # create_daily_heatmap()
    collect_data_and_create_heatmap()
