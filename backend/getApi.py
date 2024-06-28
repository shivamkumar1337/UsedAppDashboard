from flask import Flask, jsonify, request
import psycopg2
from psycopg2 import sql
from datetime import datetime, timedelta
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

# Function to calculate duration in HH:MM:SS format
def calculate_duration(duration_seconds):
    hours, remainder = divmod(duration_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

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

# Endpoint to fetch aggregated session data with duration in HH:MM:SS
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

        # Convert to list of dictionaries and format duration
        session_list = []
        for session in aggregated_sessions:
            session_dict = {
                'app_name': session[0],
                'first_start_time': session[1].isoformat(),
                'final_end_time': session[2].isoformat(),
                'duration': calculate_duration(session[3])
            }
            session_list.append(session_dict)

        conn.close()
        return jsonify(session_list), 200
    except psycopg2.Error as e:
        return jsonify({"error": str(e)}), 500

@app.route('/full_join_data', methods=['GET'])
def get_ful_join_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT
	            s.*,
                a.name AS app_name
            FROM
                applications a
            FULL JOIN
                sessions s ON a.id = s.app_id
            ORDER BY
                a.id
                
                """

if __name__ == '__main__':
    app.run(debug=True, port=5000)
