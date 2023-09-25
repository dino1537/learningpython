import os
import glob
import click
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown

NOTES_DIR = os.path.expanduser("~/.notes")


def init_notes_dir():
    if not os.path.exists(NOTES_DIR):
        os.makedirs(NOTES_DIR)


@click.group()
def cli():
    """Simple CLI Note-Taking Tool"""
    init_notes_dir()


@cli.command()
@click.argument("title")
@click.argument("content")
def create(title, content):
    """Create a new note"""
    filename = os.path.join(NOTES_DIR, title + ".md")
    with open(filename, "w") as f:
        f.write(content)
    console = Console()
    console.print(
        f"Note '{title}' created successfully in Markdown format.", style="bold green"
    )


@cli.command()
def list():
    """List all notes"""
    notes = glob.glob(os.path.join(NOTES_DIR, "*.md"))
    if not notes:
        console = Console()
        console.print("No notes found.", style="bold yellow")
    else:
        table = Table(title="List of Notes")
        table.add_column("Notes")
        for note in notes:
            table.add_row(os.path.basename(note))
        console = Console()
        console.print(table)


@cli.command()
@click.argument("title")
def edit(title):
    """Edit a note"""
    filename = os.path.join(NOTES_DIR, title + ".md")
    if not os.path.exists(filename):
        console = Console()
        console.print(f"Note '{title}' not found.", style="bold red")
        return
    with open(filename, "r") as f:
        content = f.read()
    console = Console()
    console.print(f"Current content of '{title}':")
    md = Markdown(content)
    console.print(md)
    new_content = click.edit(content, require_save=True)
    with open(filename, "w") as f:
        f.write(new_content)
    console.print(
        f"Note '{title}' updated successfully in Markdown format.", style="bold green"
    )


@cli.command()
@click.argument("query")
def search(query):
    """Search for notes containing a specific keyword"""
    notes = glob.glob(os.path.join(NOTES_DIR, "*.md"))
    found = False
    console = Console()
    for note in notes:
        with open(note, "r") as f:
            content = f.read()
        if query in content:
            console.print(f"Note found in '{os.path.basename(note)}':")
            md = Markdown(content)
            console.print(md)
            found = True
    if not found:
        console.print(f"No notes containing '{query}' found.", style="bold yellow")


if __name__ == "__main__":
    cli()
