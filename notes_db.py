import os
import glob
import click
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown

DB_PATH = os.path.expanduser("~/.notes/notes.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes
                 (title TEXT PRIMARY KEY, content TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

@click.group()
def cli():
    """Simple CLI Note-Taking Tool"""
    init_db()

@cli.command()
@click.argument("title", required=False)
@click.argument("content", required=False)
def create(title, content):
    """Create a new note"""
    if not title:
        title = click.prompt("Please enter a title for the note")
    if not content:
        content = click.prompt("Please enter the content for the note")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO notes (title, content) VALUES (?,?)", (title, content))
        console = Console()
        console.print(f"Note '{title}' created successfully.", style="bold green")
    except sqlite3.IntegrityError:
        console = Console()
        console.print(f"Note '{title}' already exists.", style="bold yellow")
    conn.commit()
    conn.close()

@cli.command()
def list():
    """List all notes"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    notes = c.execute("SELECT title, created_at FROM notes").fetchall()
    if not notes:
        console = Console()
        console.print("No notes found.", style="bold yellow")
    else:
        table = Table(title="List of Notes")
        table.add_column("Title")
        table.add_column("Created At")
        for note in notes:
            table.add_row(note[0], str(note[1]))
        console = Console()
        console.print(table)
    conn.close()

@cli.command()
@click.argument("title", required=False)
def edit(title):
    """Edit a note"""
    if not title:
        title = click.prompt("Please enter the title of the note you want to edit")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    note = c.execute("SELECT content FROM notes WHERE title=?", (title,)).fetchone()
    if note is None:
        console = Console()
        console.print(f"Note '{title}' not found.", style="bold red")
        return
    console = Console()
    console.print(f"Current content of '{title}':")
    md = Markdown(note[0])
    console.print(md)
    new_content = click.edit(note[0], require_save=True)
    c.execute("UPDATE notes SET content=? WHERE title=?", (new_content, title))
    conn.commit()
    conn.close()
    console.print(f"Note '{title}' updated successfully.", style="bold green")

@cli.command()
@click.argument("title", required=False)
def delete(title):
    """Delete a note"""
    if not title:
        title = click.prompt("Please enter the title of the note you want to delete")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE title=?", (title,))
    if c.rowcount == 0:
        console = Console()
        console.print(f"Note '{title}' not found.", style="bold red")
    else:
        console = Console()
        console.print(f"Note '{title}' deleted successfully.", style="bold green")
    conn.commit()
    conn.close()

@cli.command()
@click.argument("title", required=False)
def view(title):
    """View a note"""
    if not title:
        title = click.prompt("Please enter the title of the note you want to view")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    note = c.execute("SELECT content FROM notes WHERE title=?", (title,)).fetchone()
    if note is None:
        console = Console()
        console.print(f"Note '{title}' not found.", style="bold red")
    else:
        console = Console()
        md = Markdown(note[0])
        console.print(md)
    conn.close()

@cli.command()
@click.argument("query", required=False)
def search(query):
    """Search for notes containing a specific keyword"""
    if not query:
        query = click.prompt("Please enter the keyword you want to search for")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    notes = c.execute("SELECT title, content FROM notes WHERE content LIKE ?", ('%' + query + '%',)).fetchall()
    found = False
    console = Console()
    for note in notes:
        console.print(f"Note found in '{note[0]}':")
        md = Markdown(note[1])
        console.print(md)
        found = True
    if not found:
        console.print(f"No notes containing '{query}' found.", style="bold yellow")
    conn.close()

@cli.command()
@click.argument("title", required=False)
@click.argument("email", required=False)
def send(title, email):
    """Send a note via email"""
    if not title:
        title = click.prompt("Please enter the title of the note you want to send")
    if not email:
        email = click.prompt("Please enter the email address you want to send the note to")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    note = c.execute("SELECT content FROM notes WHERE title=?", (title,)).fetchone()
    if note is None:
        console = Console()
        console.print(f"Note '{title}' not found.", style="bold red")
        return
    msg = MIMEMultipart()
    msg['From'] = os.getenv("SENDER_EMAIL")
    msg['To'] = email
    msg['Subject'] = title
    msg.attach(MIMEText(note[0], 'plain'))
    try:
        server = smtplib.SMTP(os.getenv("SMTP_SERVER"), os.getenv("SMTP_PORT"))
        server.starttls()
        server.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD"))
        text = msg.as_string()
        server.sendmail(os.getenv("SENDER_EMAIL"), email, text)
        server.quit()
        console = Console()
        console.print(f"Note '{title}' sent to '{email}' successfully.", style="bold green")
    except Exception as e:
        console = Console()
        console.print(f"Failed to send email: {str(e)}", style="bold red")
    conn.close()

if __name__ == "__main__":
    cli()
