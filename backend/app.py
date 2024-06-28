# extract runtime data from the task manager of apps, create graphs and forward the data to frontend.

# import numpy as np
# import pandas as pd

from flask import Flask, jsonify
from flask_cors import CORS
import psutil
from datetime import datetime
import threading
import time
import pygetwindow as gw
import win32gui

import os

from device import get_device_info
from database import insert_app_usage, fetch_app_usage

app = Flask(__name__)
CORS(app)

window_start_time = {}
window_runtime = {}



def get_process_info():
    process_list = []
    for process in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_info', 'create_time', 'exe']):
        try:
            process_info = process.info
            if process_info['exe'] and not process_info['exe'].startswith(('/usr', '/System', '/Library', 'C\\Windows', 'C:\\Program Files (x86)', 'C:\\Program Files')):
                create_time = datetime.fromtimestamp(process_info['create_time'])
                process_info['create_time'] = create_time.strftime("%Y-%m-%d %H:%M:%S")
                process_info['runtime'] = str(datetime.now() - create_time).split('.')[0]
                process_info['memory_info'] = process_info['memory_info'].rss / (1024 * 1024)
                process_info['end_time'] = "Currently running" if process_info[
                                                                      'cpu_percent'] > 0 else datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S")
                process_list.append(process_info)

                data = {
                    'pid': process_info['pid'],
                    'app_name': process_info['name'],
                    'start_time': process_info['create_time'],
                    'end_time': process_info['end_time'],
                    'runtime': process_info['runtime']
                }
                insert_app_usage(data)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    process_list = sorted(process_list, key=lambda p: p['cpu_percent'], reverse=True)
    return process_list

def continuous_process_update(interval=60):
    while True:
        get_process_info()
        time.sleep(interval)

@app.route('/api/processes', methods=['GET'])
def processes():
    process_list = get_process_info()
    return jsonify(process_list)

@app.route('/api/device_info', methods=['GET'])
def device_info():
    info = get_device_info()
    return jsonify(info)

@app.route('/api/app_usage', methods=['GET'])
def app_usage():
    records = fetch_app_usage()
    return jsonify(records)

if __name__ == "__main__":

    update_thread = threading.Thread(target=continuous_process_update, daemon=True)
    update_thread.start()

    app.run(debug=True, port=5000)



