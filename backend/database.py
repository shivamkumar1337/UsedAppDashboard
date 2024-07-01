from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
import psycopg2
from psycopg2 import sql
from datetime import datetime, timedelta
from flask_cors import CORS

# PostgreSQL connection parameters
DB_NAME = "Sekisho"
DB_USER = "postgres"
DB_PASSWORD = "user%99"
DB_HOST = "localhost"
DB_PORT = "5432"

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

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

# Endpoint to get session data
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

# Endpoint to create a new application
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

# Endpoint to fetch full join data
@app.route('/full_join_data', methods=['GET'])
def get_full_join_data():
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
                a.id;
        """
        cursor.execute(query)
        full_join_data = cursor.fetchall()

        # Convert to list of dictionaries
        data_list = []
        for row in full_join_data:
            row_dict = {
                'session_id': row[0],
                'app_id': row[1],
                'start_time': row[2].isoformat() if row[2] else None,
                'end_time': row[3].isoformat() if row[3] else None,
                'duration': calculate_duration(row[4].total_seconds()) if row[4] else None,
                'app_name': row[5]
            }
            data_list.append(row_dict)

        conn.close()
        return jsonify(data_list), 200
    except psycopg2.Error as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to fetch cursor data by app_id
@app.route('/cursor_data/<int:app_id>', methods=['GET'])
def get_cursor_data(app_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT x, y, clicked, capture_time FROM cursor_data WHERE app_id = %s", (app_id,))
        cursor_data = cursor.fetchall()
        conn.close()
        return jsonify(cursor_data), 200
    except psycopg2.Error as e:
        return jsonify({"error": str(e)}), 500

# Socket.IO event for receiving session data
@socketio.on('session_data')
def handle_session_data(data):
    try:
        app_name = data['app_name']
        start_time = datetime.fromisoformat(data['start_time'])
        end_time = datetime.fromisoformat(data['end_time'])
        duration = timedelta(seconds=float(data['duration']))

        conn = get_db_connection()
        cursor = conn.cursor()

        # Get or create application ID
        cursor.execute("SELECT id FROM applications WHERE name = %s", (app_name,))
        app_id = cursor.fetchone()
        if not app_id:
            cursor.execute("INSERT INTO applications (name) VALUES (%s) RETURNING id", (app_name,))
            app_id = cursor.fetchone()[0]
        else:
            app_id = app_id[0]

        # Log session data
        cursor.execute(
            "INSERT INTO sessions (app_id, start_time, end_time, duration) VALUES (%s, %s, %s, %s)",
            (app_id, start_time, end_time, duration)
        )
        conn.commit()
        cursor.close()
        conn.close()
        emit('session_logged', {'status': 'success'})
    except Exception as e:
        emit('session_logged', {'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000, allow_unsafe_werkzeug=True)