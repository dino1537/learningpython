import sqlite3
import subprocess
import tempfile
import datetime
import calendar
import markdown
import os

# Connect to the SQLite database or create a new one
conn = sqlite3.connect("journal.db")
cursor = conn.cursor()

# Create a table to store journal entries
cursor.execute('''
    CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        entry TEXT,
        tags TEXT
    )
''')
conn.commit()

# Detect the user's preferred text editor (e.g., from a configuration file or environment variable)
# Use 'nvim' as the default editor if not specified
preferred_editor = os.getenv("JOURNAL_EDITOR", "nvim")

def write_entry_with_editor():
    # Create a temporary file for the user to write the entry
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as temp_file:
        temp_file.close()
        
        # Open the preferred text editor with the temporary file
        subprocess.run([preferred_editor, temp_file.name])
        
        # Read the contents of the temporary file
        with open(temp_file.name, "r") as entry_file:
            entry = entry_file.read()
        
        # Remove the temporary file
        os.remove(temp_file.name)
    
    # Save the entry to the journal
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tags = input("Enter tags (comma-separated): ")
    
    cursor.execute("INSERT INTO entries (entry, tags) VALUES (?, ?)", (entry, tags))
    conn.commit()
    print("Entry saved successfully.")

def edit_entry(entry_id):
    new_entry = input("Edit your journal entry (you can use Markdown syntax): ")
    
    cursor.execute("UPDATE entries SET entry = ? WHERE id = ?", (new_entry, entry_id))
    conn.commit()
    print("Entry edited successfully.")

def delete_entry(entry_id):
    cursor.execute("DELETE FROM entries WHERE id = ?", (entry_id,))
    conn.commit()
    print("Entry deleted successfully.")

def search_entries(keyword):
    cursor.execute("SELECT * FROM entries WHERE entry LIKE ? OR tags LIKE ?", ('%' + keyword + '%', '%' + keyword + '%'))
    result = cursor.fetchall()
    
    if result:
        print("Search results:")
        for row in result:
            print(f"Entry ID: {row[0]}\nTimestamp: {row[1]}\nTags: {row[3]}\n\n{row[2]}\n")
    else:
        print("No matching entries found.")

def tag_entry(entry_id, tags):
    cursor.execute("UPDATE entries SET tags = ? WHERE id = ?", (tags, entry_id))
    conn.commit()
    print("Entry tagged successfully.")

def display_calendar():
    year = int(input("Enter the year for the calendar: "))
    month = int(input("Enter the month (1-12) for the calendar: "))
    
    cal = calendar.month(year, month)
    print("\nCalendar:")
    print(cal)

def format_markdown(entry):
    return markdown.markdown(entry)

def main():
    while True:
        print("Journaling Tool Menu:")
        print("1. Write a new entry")
        print("2. Edit an entry")
        print("3. Delete an entry")
        print("4. Search for entries")
        print("5. Display Calendar")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            # Allow the user to write an entry with their preferred editor
            write_entry_with_editor()
        elif choice == "2":
            entry_id = int(input("Enter the ID of the entry you want to edit: "))
            edit_entry(entry_id)
        elif choice == "3":
            entry_id = int(input("Enter the ID of the entry you want to delete: "))
            delete_entry(entry_id)
        elif choice == "4":
            keyword = input("Enter a keyword to search for entries: ")
            search_entries(keyword)
        elif choice == "5":
            display_calendar()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

