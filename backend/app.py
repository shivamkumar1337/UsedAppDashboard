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
            capture_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()

# Function to insert cursor data into PostgreSQL
def insert_cursor_data(conn, x, y, clicked):
    cursor = conn.cursor()
    insert_query = sql.SQL("""
        INSERT INTO cursor_data (x, y, clicked, capture_time)
        VALUES (%s, %s, %s, %s)
    """)
    cursor.execute(insert_query, (x, y, clicked, datetime.now()))
    conn.commit()
    cursor.close()

# Function to capture cursor movements and clicks
def on_move(x, y):
    insert_cursor_data(conn, x, y, False)
    print(f'Mouse moved to ({x}, {y})')

def on_click(x, y, button, pressed):
    if pressed:
        insert_cursor_data(conn, x, y, True)
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
        cursor.execute("SELECT x, y FROM cursor_data")
        cursor_data = cursor.fetchall()
        conn.close()

        # Convert cursor data to DataFrame for seaborn heatmap
        cursor_df = pd.DataFrame(cursor_data, columns=['x', 'y'])

        # Set up the heatmap plot
        plt.figure(figsize=(10, 8))
        sns.set(style="whitegrid")
        plt.title('Cursor Heatmap')

        # Plot heatmap
        sns.kdeplot(x=cursor_df['x'], y=cursor_df['y'], cmap="Reds", cbar=True, shade=True, shade_lowest=False, alpha=0.8)

        plt.xlabel('X Position')
        plt.ylabel('Y Position')

        plt.tight_layout()
        plt.show()

    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")

if __name__ == '__main__':

    collect_data_and_create_heatmap()

