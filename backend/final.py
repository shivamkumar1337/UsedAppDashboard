import time
import psutil
from datetime import datetime
import win32gui
import win32process
import socketio
import requests
import websocket

# Socket.IO client setup
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server")

@sio.event
def disconnect():
    print("Disconnected from server")

# Function to get active window using Win32 API
def get_active_window():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        return process.name()
    except Exception as e:
        return None

# Function to emit session data to Socket.IO server
def emit_session(app_name, start_time, end_time):
    duration = end_time - start_time
    sio.emit('session_data', {
        'app_name': app_name,
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'duration': str(duration.total_seconds())
    })

# Connect to Socket.IO server
if __name__ == "__main__":
    sio.connect('http://localhost:5000')

    current_app = None
    start_time = None

    try:
        while True:
            active_window = get_active_window()
            if active_window and active_window != current_app:
                if current_app:
                    end_time = datetime.now()
                    emit_session(current_app, start_time, end_time)
                current_app = active_window
                start_time = datetime.now()
            time.sleep(1)
    except KeyboardInterrupt:
        if current_app:
            end_time = datetime.now()
            emit_session(current_app, start_time, end_time)
        sio.disconnect()
        print("Session data emitted to Socket.IO server. Exiting.")