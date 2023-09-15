import pytz
from datetime import datetime

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

# Get the current time for each time zone
current_time = datetime.now()
formatted_times = []

for city, timezone in time_zones.items():
    local_time = current_time.astimezone(pytz.timezone(timezone))
    formatted_time = local_time.strftime("%Y-%m-%d %H:%M:%S %Z")
    formatted_times.append(f"{icons[city]} {city}: {formatted_time}")

# Display the current times with Nerd Font icons on the command line
print("\n".join(formatted_times))

