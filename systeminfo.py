import os
import platform
import psutil
import subprocess
from datetime import datetime, timedelta
from rich import print
from rich.table import Table

# Function to format bytes to a human-readable format
def bytes_to_readable(byte_count):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if byte_count < 1024.0:
            break
        byte_count /= 1024.0
    return f"{byte_count:.2f} {unit}"

# Function to calculate uptime
def calculate_uptime():
    boot_time = psutil.boot_time()
    current_time = datetime.now().timestamp()
    uptime_seconds = current_time - boot_time
    return timedelta(seconds=uptime_seconds)

# Function to get connected WiFi SSID (Linux-specific)
def get_wifi_ssid():
    try:
        result = subprocess.check_output(["iwgetid", "-r"]).decode().strip()
        return result
    except subprocess.CalledProcessError:
        return "Not connected to WiFi"

# Function to display system information
def display_system_info():
    hostname = platform.node()
    wifi_ssid = get_wifi_ssid()
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    uptime = calculate_uptime()
    kernel_version = platform.uname().release
    disk_partitions = psutil.disk_partitions()
    
    table = Table()
    table.add_column("Category", style="cyan", justify="right")
    table.add_column("Data", style="yellow")

    table.add_row(" Hostname", hostname)
    table.add_row(" WiFi SSID", wifi_ssid)
    table.add_row(" Date/Time", date_time)
    table.add_row(" Uptime", str(uptime))
    table.add_row(" Kernel Version", kernel_version)
    table.add_row(" Disk Usage", "")
    
    for partition in disk_partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        table.add_row(f"  {partition.device}", f"{bytes_to_readable(usage.used)} / {bytes_to_readable(usage.total)}")

    print(table)

if __name__ == "__main__":
    display_system_info()

