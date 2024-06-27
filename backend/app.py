# extract runtime data from the task manager of apps, create graphs and forward the data to frontend.

# import numpy as np
# import pandas as pd

from flask import Flask, jsonify
from flask_cors import CORS
import psutil
from datetime import datetime
import os
from backend.device import get_device_info
from database import insert_app_usage

app = Flask(__name__)
CORS(app)

def get_process_info():
    process_list = []
    for process in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_info', 'create_time']):
        try:
            process_info = process.info
            create_time = datetime.fromtimestamp(process_info['create_time'])
            process_info['create_time'] = create_time.strftime("%Y-%m-%d %H:%M:%S")
            process_info['runtime'] = str(datetime.now() - create_time).split('.')[0]
            process_info['memory_info'] = process_info['memory_info'].rss / (1024 * 1024)
            process_info['end_time'] = "Currently running" if process_info['cpu_percent'] > 0 else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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


def print_process_info(process_list):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{'PID':<10} {'Name':<25} {'CPU%':<10} {'Memory (MB)':<15} {'Start Date':<20} {'Start time':<20} {'End Date':<20} {'End time':<20} {'Runtime':<10}")
    print("="*130)
    for process in process_list:
        print(f"{process['pid']:<10} {process['name']:<25} {process['cpu_percent']:<10} {process['memory_info']:<15.2f} {process['start_date']:<20} {process['create_time']:<20} {process['end_date']:<20} {process['end_time']:<20} {process['runtime']:<10}")

@app.route('/api/processes', methods=['GET'])
def processes():
    process_list = get_process_info()
    return jsonify(process_list)

@app.route('/api/device_info', methods=['GET'])
def device_info():
    info = get_device_info()
    return jsonify(info)

if __name__ == "__main__":
     get_process_info()
     app.run(debug=True, port=5000)

     # while True:
     #   process_list = get_process_info()
     #   print_process_info(process_list)
     #   time.sleep(30)

