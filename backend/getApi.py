from flask import Flask, jsonify, request
import psycopg2
from psycopg2 import sql
from datetime import datetime
from flask_cors import CORS

# PostgreSQL connection parameters
DB_NAME = "AppUsageDatabase"
DB_USER = "postgres"
DB_PASSWORD = "12345"
DB_HOST = "localhost"
DB_PORT = "5433"

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

# Function to calculate duration in minutes (rounded to 2 decimal places)
def calculate_duration(start_time, end_time):
    if start_time and end_time:
        duration = end_time - start_time
        hours, remainder = divmod(duration.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
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

# Endpoint to fetch aggregated session data
@app.route('/aggregated_sessions', methods=['GET'])
def get_aggregated_sessions():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT
                a.name AS app_name,
                MIN(s.start_time) AS first_start_time,
                MAX(s.end_time) AS final_end_time,
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
            session['duration_minutes'] = calculate_duration(session['first_start_time_japan'], session['final_end_time_japan'])
            # Remove duration_seconds key if not needed
            del session['duration_seconds']

        conn.close()
        print(aggregated_sessions)
        return jsonify(aggregated_sessions), 200
    except psycopg2.Error as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
