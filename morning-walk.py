import sqlite3
import os
import markdown
from datetime import datetime, timedelta

# Create a SQLite database to store the morning walk plan
db_filename = "morning_walk_plan.db"
conn = sqlite3.connect(db_filename)
cursor = conn.cursor()

# Create a table to store the walk plan
cursor.execute('''
    CREATE TABLE IF NOT EXISTS morning_walk (
        date TEXT PRIMARY KEY,
        day TEXT,
        alarm_time_start TEXT,
        alarm_time_end TEXT,
        call_to TEXT,
        distance_km INTEGER
    )
''')

# Generate a morning walk plan for a month (30 days) starting from tomorrow
start_date = datetime.now() + timedelta(days=1)
end_date = start_date + timedelta(days=30)

# Initialize Markdown and Org content
markdown_content = "| Date       | Day    | Distance (km) | Morning Walk Time | Reminder Alarm | Call to  |\n"
markdown_content += "|------------|--------|---------------|-------------------|----------------|----------|\n"

org_content = "| Date       | Day    | Distance (km) | Morning Walk Time | Reminder Alarm | Call to  |\n"
org_content += "|------------+--------+---------------+-------------------+----------------+----------|\n"

for day in range((end_date - start_date).days):
    current_date = start_date + timedelta(days=day)
    alarm_time_start = "6:15 AM"
    alarm_time_end = "6:17 AM"
    call_to = "Prabu"

    # Determine the distance based on weekdays or weekends
    if current_date.weekday() < 5:  # Weekdays (Monday to Friday)
        distance_km = 5
        walk_time = "6:30 AM - 8:00 AM"
    else:  # Weekends (Saturday and Sunday)
        distance_km = 10
        walk_time = "6:30 AM - 9:00 AM"

    # Add the plan to the SQLite database
    cursor.execute("INSERT INTO morning_walk (date, day, alarm_time_start, alarm_time_end, call_to, distance_km) "
                   "VALUES (?, ?, ?, ?, ?, ?)",
                   (current_date.strftime("%Y-%m-%d"), current_date.strftime("%A"), alarm_time_start,
                    alarm_time_end, call_to, distance_km))

    # Add the plan to the Markdown content
    markdown_content += f"| {current_date.strftime('%Y-%m-%d')} | {current_date.strftime('%A')} | {distance_km} | {walk_time} | {alarm_time_start} | {call_to} |\n"

    # Add the plan to the Org content
    org_content += f"| {current_date.strftime('%Y-%m-%d')} | {current_date.strftime('%A')} | {distance_km} | {walk_time} | {alarm_time_start} | {call_to} |\n"

# Commit the changes and close the database connection
conn.commit()
conn.close()

# Write the Markdown content to a file
markdown_filename = "morning_walk_plan.md"
with open(markdown_filename, "w") as md_file:
    md_file.write(markdown_content)

print(f"Morning walk plan in Markdown format created in '{markdown_filename}'.")

# Write the Org content to a file
org_filename = "morning_walk_plan.org"
with open(org_filename, "w") as org_file:
    org_file.write(org_content)

print(f"Morning walk plan in Org format created in '{org_filename}'.")

