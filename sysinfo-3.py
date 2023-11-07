from rich.console import Console
from rich.table import Table
from rich.box import SQUARE
from datetime import datetime
import platform
import psutil

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

console = Console()

# System Information
table = Table(show_header=True, header_style="bold magenta", box=SQUARE)
table.add_column("Category", style="dim", width=12)
table.add_column("Information")

uname = platform.uname()
table.add_row("System", uname.system)
table.add_row("Node Name", uname.node)
table.add_row("Release", uname.release)
table.add_row("Version", uname.version)
table.add_row("Machine", uname.machine)
table.add_row("Processor", uname.processor)

console.print(table)

# Boot Time
table = Table(show_header=True, header_style="bold magenta", box=SQUARE)
table.add_column("Boot Time", style="dim", width=12)

boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
table.add_row("Boot Time", f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")

console.print(table)

# CPU Info
table = Table(show_header=True, header_style="bold magenta", box=SQUARE)
table.add_column("CPU Info", style="dim", width=12)
table.add_column("Details")

table.add_row("Physical cores", str(psutil.cpu_count(logical=False)))
table.add_row("Total cores", str(psutil.cpu_count(logical=True)))

cpufreq = psutil.cpu_freq()
table.add_row("Max Frequency", f"{cpufreq.max:.2f}Mhz")
table.add_row("Min Frequency", f"{cpufreq.min:.2f}Mhz")
table.add_row("Current Frequency", f"{cpufreq.current:.2f}Mhz")

console.print(table)

# CPU usage
table = Table(show_header=True, header_style="bold magenta", box=SQUARE)
table.add_column("CPU Usage", style="dim", width=12)
table.add_column("Details")

for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    table.add_row(f"Core {i}", f"{percentage}%")
table.add_row("Total CPU Usage", f"{psutil.cpu_percent()}%")

console.print(table)

# Memory Information
table = Table(show_header=True, header_style="bold magenta", box=SQUARE)
table.add_column("Memory Information", style="dim", width=12)
table.add_column("Details")

svmem = psutil.virtual_memory()
table.add_row("Total", get_size(svmem.total))
table.add_row("Available", get_size(svmem.available))
table.add_row("Used", get_size(svmem.used))
table.add_row("Percentage", f"{svmem.percent}%")

console.print(table)

# Disk Information
partitions = psutil.disk_partitions()
for partition in partitions:
    table = Table(show_header=True, header_style="bold magenta", box=SQUARE)
    table.add_column("Disk Information", style="dim", width=12)
    table.add_column("Details")

    table.add_row("Device", partition.device)
    table.add_row("Mountpoint", partition.mountpoint)
    table.add_row("File system type", partition.fstype)

    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        continue

    table.add_row("Total Size", get_size(partition_usage.total))
    table.add_row("Used", get_size(partition_usage.used))
    table.add_row("Free", get_size(partition_usage.free))
    table.add_row("Percentage", f"{partition_usage.percent}%")

    console.print(table)

# Network information
table = Table(show_header=True, header_style="bold magenta", box=SQUARE)
table.add_column("Network Information", style="dim", width=12)
table.add_column("Details")

net_io = psutil.net_io_counters()
table.add_row("Total Bytes Sent", get_size(net_io.bytes_sent))
table.add_row("Total Bytes Received", get_size(net_io.bytes_recv))

console.print(table)
