import os
import psutil
import speedtest
import sys
import time 
import subprocess

def check_internet():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1000000
    except (speedtest.SpeedtestBestServerFailure, speedtest.ConfigRetrievalError):
        download_speed = None
    return download_speed


def check_system():
    cpu_usage = psutil.cpu_percent(interval=1)
    mem_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    return cpu_usage, mem_usage, disk_usage

def check_ping():
    try:
        command = "ping google.com -n 1"
        out = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]
        out = out.decode('cp866')
        lines = out.split('\n')
        for line in lines:
            if 'Среднее = ' in line or 'Average = ' in line:
                return line.split(' = ')[-1].replace('мс', 'ms').strip()
    except subprocess.CalledProcessError:
        pass
    return None


while True:
    internet_speed = check_internet()
    cpu_usage, mem_usage, disk_usage = check_system()
    ping = check_ping()

    os.system('cls' if os.name == 'nt' else 'clear')

    if internet_speed is None:
        print("Internet speed: None")
    else:
        print(f"Internet speed: {internet_speed:.2f} Mbps")
    sys.stdout.flush()

    print(f"CPU usage: {cpu_usage}%")
    sys.stdout.flush()
    print(f"Memory usage: {mem_usage}%")
    sys.stdout.flush()
    print(f"Disk usage: {disk_usage}%")
    sys.stdout.flush()

    if ping is None:
        print("Ping: None")
    else:
        print(f"Ping: {ping}")
    sys.stdout.flush()

    time.sleep(5)
