import psutil
from flask import Flask, jsonify
from datetime import datetime, timedelta
import socket
import wmi

device_id = socket.gethostname()
device_start_time = datetime.fromtimestamp(psutil.boot_time())
sleep_time_total = timedelta(0)

def get_sleep_time():
    global sleep_time_total
    c = wmi.WMI(namespace='root\\wmi')
    sleep_events = c.ExecQuery('SELECT * FROM BatteryStatus WHERE Voltage = 0')
    for event in sleep_events:
        sleep_time_total += timedelta(minutes=event.RemainingCapacity)
    return str(sleep_time_total)

def get_device_info():
    device_info = {
        'Device_ID': device_id,
        'Device_switch_on_time': device_start_time.strftime("%Y-%m-%d %H:%M:%S"),
        'Device_switch_off_time': "Currently Running",
        'Device_sleep_time': get_sleep_time()
    }
    return device_info


