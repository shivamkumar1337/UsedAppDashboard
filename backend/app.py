# # extract runtime data from the task manager of apps, create graphs and forward the data to frontend.

# # import numpy as np
# # import pandas as pd
# from flask import Flask, jsonify
# from flask_cors import CORS
# import psutil
# from datetime import datetime
# import time
# import os

# app = Flask(__name__)
# CORS(app)
# def get_process_info():
#     process_list = []
#     for process in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_info', 'create_time']):
#         try:
#             process_info = process.info
#             if process_info['cpu_percent'] > 0:
#                 create_time = datetime.fromtimestamp(process_info['create_time'])
#                 process_info['create_time'] = create_time.strftime("%Y-%m-%d %H:%M:%S")
#                 process_info['end_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                 process_info['runtime'] = str(datetime.now() - create_time).split('.')[0]
#                 process_info['memory_info'] = process_info['memory_info'].rss / (1024 * 1024)
#                 process_list.append(process_info)
#         except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#             pass
#     process_list = sorted(process_list, key=lambda p: p['cpu_percent'], reverse=True)
#     return process_list


# def print_process_info(process_list):
#     os.system('cls' if os.name == 'nt' else 'clear')
#     print(f"{'PID':<10} {'Name':<25} {'CPU%':<10} {'Memory (MB)':<15} {'Start time':<20} {'End time':<20} {'Runtime':<10}")
#     print("="*130)
#     for process in process_list:
#         print(f"{process['pid']:<10} {process['name']:<25} {process['cpu_percent']:<10} {process['memory_info']:<15.2f} {process['create_time']:<20} {process['end_time']:<20} {process['runtime']:<10}")

# @app.route('/api/processes', methods=['GET'])
# def processes():
#     process_list = get_process_info()
#     return jsonify(process_list)

# if __name__ == "__main__":
#      app.run(debug=True, port=5000)
#      """     while True:
#         process_list = get_process_info()
#         print_process_info(process_list)
#         time.sleep(15) """



from flask import Flask, request, jsonify
# from supabase import create_client, Client
from datetime import datetime
import time
import psutil
import pygetwindow as gw
from datetime import datetime
import requests

app = Flask(__name__)

# Initialize Supabase client
import os
from supabase import create_client, Client

url: str = os.environ.get("https://asurnvasltqvhjneodwy.supabase.co")
key: str = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFzdXJudmFzbHRxdmhqbmVvZHd5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTkzNjE0MjQsImV4cCI6MjAzNDkzNzQyNH0._334jnQnRsDUZpEMnnQ2ENQJLn207Kd72eXBYme6gHs")
supabase: Client = create_client(url, key)

@app.route('/start', methods=['POST'])
def start_application():
    data = request.json
    response = supabase.table('app_usage').insert({
        'user': data['user'],
        'app_name': data['app_name'],
        # 'start_date': datetime.now().date().isoformat(),
        # 'start_time': datetime.now().time().isoformat(),
    }).execute()
    return jsonify(response.data), 201

@app.route('/end', methods=['POST'])
def end_application():
    data = request.json
    pid = data['pid']
    response = supabase.table('your_table_name').update({
        'end_date': datetime.now().date().isoformat(),
        'end_time': datetime.now().time().isoformat(),
    }).eq('PID', pid).execute()
    return jsonify(response.data), 200

if __name__ == '__main__':
    app.run(debug=True)


