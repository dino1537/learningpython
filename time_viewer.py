import pytz
from datetime import datetime
from rich.table import Table
from rich import print

# Define time zones
time_zones = {
    'Chennai': 'Asia/Kolkata',
    'London': 'Europe/London',
    'San Francisco': 'America/Los_Angeles',
    'New York': 'America/New_York',
    'Manila': 'Asia/Manila',
    'Sydney': 'Australia/Sydney'
}

# Nerd Font icons for each city
icons = {
    'Chennai': '\uf042',  # Icon for Chennai
    'London': '\uf0ac',   # Icon for London
    'San Francisco': '\uf319',  # Icon for San Francisco
    'New York': '\uf299',  # Icon for New York
    'Manila': '\uf337',   # New icon for Manila
    'Sydney': '\uf322'    # Icon for Sydney
}

# Create a table to display the information
table = Table(title="World Clock")
table.add_column("City", justify="right", style="cyan")
table.add_column("Local Time", justify="right", style="magenta")

# Get the current time for each time zone and add it to the table
current_time = datetime.now()
for city, timezone in time_zones.items():
    local_time = current_time.astimezone(pytz.timezone(timezone))
    formatted_time = local_time.strftime("%Y-%m-%d %H:%M:%S %Z")
    table.add_row(f"{icons[city]} {city}:", formatted_time)

# Print the table with rich formatting
print(table)

