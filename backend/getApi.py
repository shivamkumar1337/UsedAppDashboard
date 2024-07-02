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
                a.id AS app_id,
                a.name AS app_name,
                MIN(s.start_time) AS first_start_time,
                MAX(s.end_time) AS final_end_time,
                SUM(EXTRACT(EPOCH FROM s.duration)) AS duration_seconds
            FROM
                applications a
            JOIN
                sessions s ON a.id = s.app_id
            GROUP BY
                a.id, a.name
            ORDER BY
                a.name;
        """
        cursor.execute(query)
        aggregated_sessions = cursor.fetchall()

        # Convert to list of dictionaries and format duration
        session_list = []
        for session in aggregated_sessions:
            session_dict = {
                'app_id': session[0],
                'app_name': session[1],
                'first_start_time': session[2].isoformat(),
                'final_end_time': session[3].isoformat(),
                'duration': calculate_duration(session[4])
            }
            session_list.append(session_dict)

        conn.close()
        return jsonify(session_list), 200
    except psycopg2.Error as e:
        return jsonify({"error": str(e)}), 500

@app.route('/aggregated_sessions_today', methods=['GET'])
def get_aggregated_sessions_today():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Calculate today's start and end times
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        query = """
            SELECT
                a.id AS app_id,
                a.name AS app_name,
                MIN(s.start_time) AS first_start_time,
                MAX(s.end_time) AS final_end_time,
                SUM(EXTRACT(EPOCH FROM s.duration)) AS duration_seconds
            FROM
                applications a
            JOIN
                sessions s ON a.id = s.app_id
            WHERE
                s.start_time >= %s AND s.start_time < %s
            GROUP BY
                a.id, a.name
            ORDER BY
                a.name;
        """
        cursor.execute(query, (today_start, today_end))
        aggregated_sessions = cursor.fetchall()

        # Convert to list of dictionaries and format duration
        session_list = []
        for session in aggregated_sessions:
            session_dict = {
                'app_id': session[0],
                'app_name': session[1],
                'first_start_time': session[2].isoformat(),
                'final_end_time': session[3].isoformat(),
                'duration': calculate_duration(session[4])
            }
            session_list.append(session_dict)

        conn.close()
        return jsonify(session_list), 200
    except psycopg2.Error as e:
        return jsonify({"error": str(e)}), 500

@app.route('/aggregated_sessions_custom', methods=['GET'])
def get_aggregated_sessions_custom():
    try:
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')

        # Validate and parse dates
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            return jsonify({"error": "Invalid date format. Use ISO format with milliseconds"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT
                a.id AS app_id,
                a.name AS app_name,
                MIN(s.start_time) AS first_start_time,
                MAX(s.end_time) AS final_end_time,
                SUM(EXTRACT(EPOCH FROM s.duration)) AS duration_seconds
            FROM
                applications a
            JOIN
                sessions s ON a.id = s.app_id
            WHERE
                s.start_time >= %s AND s.end_time <= %s
            GROUP BY
                a.id, a.name
            ORDER BY
                a.name;
        """
        cursor.execute(query, (start_date, end_date))
        aggregated_sessions = cursor.fetchall()

        # Convert to list of dictionaries and format duration
        session_list = []
        for session in aggregated_sessions:
            session_dict = {
                'app_id': session[0],
                'app_name': session[1],
                'first_start_time': session[2].isoformat(),
                'final_end_time': session[3].isoformat(),
                'duration': calculate_duration(session[4])
            }
            session_list.append(session_dict)

        conn.close()
        return jsonify(session_list), 200
    except psycopg2.Error as e:
        return jsonify({"error": str(e)}), 500

@app.route('/sessions/<int:app_id>', methods=['GET'])
def get_sessions_by_app_id(app_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT
                a.id AS app_id,
                a.name AS app_name,
                SUM(EXTRACT(EPOCH FROM s.duration)) AS total_duration_seconds,
                s.start_time,
                s.end_time,
                s.duration
            FROM
                applications a
            FULL JOIN
                sessions s ON a.id = s.app_id
            WHERE
                a.id = %s
            GROUP BY
                a.id, a.name, s.start_time, s.end_time, s.duration
            ORDER BY
                s.start_time;
        """
        cursor.execute(query, (app_id,))
        sessions = cursor.fetchall()

        # Format the response
        session_list = []
        total_duration_seconds = 0
        for session in sessions:
            if session[2] is not None:
                total_duration_seconds += session[2]
            session_list.append({
                'start_time': session[3].isoformat() if session[3] else None,
                'end_time': session[4].isoformat() if session[4] else None,
                'duration': calculate_duration(session[5].total_seconds()) if session[5] else None
            })

        app_data = {
            'app_id': app_id,
            'app_name': sessions[0][1] if sessions else '',
            'total_duration': calculate_duration(total_duration_seconds),
            'sessions': session_list
        }

        conn.close()
        return jsonify(app_data), 200
    except psycopg2.Error as e:
        return jsonify({"error": str(e)}), 500

@app.route('/sessions_today/<int:app_id>', methods=['GET'])
def get_sessions_today_by_app_id(app_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Calculate today's start and end times
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        query = """
            SELECT
                a.id AS app_id,
                a.name AS app_name,
                SUM(EXTRACT(EPOCH FROM s.duration)) AS total_duration_seconds,
                s.start_time,
                s.end_time,
                s.duration
            FROM
                applications a
            FULL JOIN
                sessions s ON a.id = s.app_id
            WHERE
                a.id = %s AND s.start_time >= %s AND s.start_time < %s
            GROUP BY
                a.id, a.name, s.start_time, s.end_time, s.duration
            ORDER BY
                s.start_time;
        """
        cursor.execute(query, (app_id, today_start, today_end))
        sessions = cursor.fetchall()

        # Format the response
        session_list = []
        total_duration_seconds = 0
        for session in sessions:
            if session[2] is not None:
                total_duration_seconds += session[2]
            session_list.append({
                'start_time': session[3].isoformat() if session[3] else None,
                'end_time': session[4].isoformat() if session[4] else None,
                'duration': calculate_duration(session[5].total_seconds()) if session[5] else None
            })

        app_data = {
            'app_id': app_id,
            'app_name': sessions[0][1] if sessions else '',
            'total_duration': calculate_duration(total_duration_seconds),
            'sessions': session_list
        }

        conn.close()
        return jsonify(app_data), 200
    except psycopg2.Error as e:
        return jsonify({"error": str(e)}), 500

@app.route('/sessions_custom/<int:app_id>', methods=['GET'])
def get_sessions_custom_by_app_id(app_id):
    try:
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')

        # Validate and parse dates
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            return jsonify({"error": "Invalid date format. Use ISO format with milliseconds"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT
                a.id AS app_id,
                a.name AS app_name,
                SUM(EXTRACT(EPOCH FROM s.duration)) AS total_duration_seconds,
                s.start_time,
                s.end_time,
                s.duration
            FROM
                applications a
            FULL JOIN
                sessions s ON a.id = s.app_id
            WHERE
                a.id = %s AND s.start_time >= %s AND s.end_time <= %s
            GROUP BY
                a.id, a.name, s.start_time, s.end_time, s.duration
            ORDER BY
                s.start_time;
        """
        cursor.execute(query, (app_id, start_date, end_date))
        sessions = cursor.fetchall()

        # Format the response
        session_list = []
        total_duration_seconds = 0
        for session in sessions:
            if session[2] is not None:
                total_duration_seconds += session[2]
            session_list.append({
                'start_time': session[3].isoformat() if session[3] else None,
                'end_time': session[4].isoformat() if session[4] else None,
                'duration': calculate_duration(session[5].total_seconds()) if session[5] else None
            })

        app_data = {
            'app_id': app_id,
            'app_name': sessions[0][1] if sessions else '',
            'total_duration': calculate_duration(total_duration_seconds),
            'sessions': session_list
        }

        conn.close()
        return jsonify(app_data), 200
    except psycopg2.Error as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
