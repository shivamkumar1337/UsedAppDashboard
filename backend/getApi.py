from flask import Flask, jsonify, request
import psycopg2
from psycopg2 import sql
from datetime import datetime, timedelta
import pytz  # Import pytz for timezone conversion

# PostgreSQL connection parameters
DB_NAME = "Sekisho"
DB_USER = "postgres"
DB_PASSWORD = "user%99"
DB_HOST = "localhost"
DB_PORT = "5432"

# Define Japan timezone
japan_tz = pytz.timezone('Asia/Tokyo')

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

# Function to convert datetime to Japan timezone
def convert_to_japan_timezone(dt):
    if dt:
        return dt.astimezone(japan_tz)
    return None

# Function to calculate duration in minutes (rounded to 2 decimal places)
def calculate_duration_minutes(start_time, end_time):
    if start_time and end_time:
        duration = end_time - start_time
        duration_minutes = duration.total_seconds() / 60
        return round(duration_minutes, 2)
    return None

# Example endpoint to get session data
@app.route('/sessions', methods=['GET'])
def get_sessions():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sessions")
        sessions = cursor.fetchall()
        conn.close()
        return jsonify(sessions), 200
    except psycopg2.Error as e:
        return jsonify({"error": str(e)}), 500

# Example endpoint to create a new application
@app.route('/applications', methods=['POST'])
def create_application():
    data = request.json
    app_name = data.get('name')
    if not app_name:
        return jsonify({"error": "Missing 'name' in request body"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        insert_query = sql.SQL("INSERT INTO applications (name) VALUES (%s) RETURNING id")
        cursor.execute(insert_query, (app_name,))
        app_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return jsonify({"id": app_id}), 201
    except psycopg2.Error as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to fetch aggregated session data in Japan timezone with duration in minutes (rounded to 2 decimal places)
@app.route('/aggregated_sessions', methods=['GET'])
def get_aggregated_sessions():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT
                a.name AS app_name,
                MIN(s.start_time AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Tokyo') AS first_start_time_japan,
                MAX(s.end_time AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Tokyo') AS final_end_time_japan,
                SUM(EXTRACT(EPOCH FROM s.duration)) AS duration_seconds
            FROM
                applications a
            JOIN
                sessions s ON a.id = s.app_id
            GROUP BY
                a.name
            ORDER BY
                app_name;
        """
        cursor.execute(query)
        aggregated_sessions = cursor.fetchall()

        # Convert datetime fields to Japan timezone and calculate duration in minutes (rounded to 2 decimal places)
        for session in aggregated_sessions:
            session['first_start_time_japan'] = convert_to_japan_timezone(session['first_start_time_japan'])
            session['final_end_time_japan'] = convert_to_japan_timezone(session['final_end_time_japan'])
            session['duration_minutes'] = calculate_duration_minutes(session['first_start_time_japan'], session['final_end_time_japan'])

            # Remove duration_seconds key if not needed
            del session['duration_seconds']

        conn.close()
        return jsonify(aggregated_sessions), 200
    except psycopg2.Error as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
