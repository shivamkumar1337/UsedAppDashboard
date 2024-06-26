import time
import psutil
import pygetwindow as gw
from datetime import datetime
import requests

APP_START_URL = "http://127.0.0.1:5000/start"
APP_END_URL = "http://127.0.0.1:5000/end"

active_windows = {}

# def get_active_window():
#     try:
#         window = gw.getActiveWindow()
#         return window.title, window.processId
#     except:
#         return None, None
 
start_time = datetime.now()
app_info = {
    'user': "username",
    'app_name': "active_window",
    'start_date': start_time.date().isoformat(),
    'start_time': start_time.time().isoformat(),
}
response = requests.post(APP_START_URL, json=app_info)
if response.status_code == 201:
    active_windows[0] = {'pid': id, 'start_time': start_time}
print(f"Started: {0} at {start_time}")
print(response)