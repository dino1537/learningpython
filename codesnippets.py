import argparse
import json
import os
import sys
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter

SNIPPETS_FILE = "snippets.json"


def load_snippets():
    """Load snippets from the JSON file."""
    if os.path.exists(SNIPPETS_FILE):
        with open(SNIPPETS_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                print(f"Error: {SNIPPETS_FILE} is not a valid JSON file.")
                sys.exit(1)
    else:
        return {}


def save_snippets(snippets):
    """Save snippets to the JSON file."""
    with open(SNIPPETS_FILE, "w") as file:
        json.dump(snippets, file, indent=4)


def manage_snippet(snippets, name, code=None):
    """Manage a snippet (add, edit, or delete)."""
    if code is None:  # delete snippet
        if name in snippets:
            del snippets[name]
            save_snippets(snippets)
            print(f"Snippet '{name}' deleted successfully!")
        else:
            print(f"Snippet '{name}' not found!")
    else:  # add or edit snippet
        snippets[name] = code
        save_snippets(snippets)
        print(f"Snippet '{name}' added/edited successfully!")


def retrieve_snippet(snippets, name):
    """Retrieve a snippet by its name."""
    if name in snippets:
        code = snippets[name]
        print(f"Snippet '{name}':")
        print_highlighted_code(code)
    else:
        print(f"Snippet '{name}' not found!")


def list_snippets(snippets):
    """List all available snippets."""
    print("Available snippets:")
    for name in sorted(snippets):
        print(f"- {name}")


def print_highlighted_code(code):
    """Print the code with syntax highlighting."""
    try:
        lexer = get_lexer_by_name("python", stripall=True)
        formatter = TerminalFormatter()
        highlighted_code = highlight(code, lexer, formatter)
        print(highlighted_code)
    except Exception as e:
        print("Error highlighting code:", e)


def main():
    """Handle the command-line arguments and call the appropriate function."""
    parser = argparse.ArgumentParser(description="Code Snippet Management Tool")
    parser.add_argument("--add", help="Add a code snippet", action="store_true")
    parser.add_argument("--retrieve", help="Retrieve a code snippet by name")
    parser.add_argument("--edit", help="Edit a code snippet by name")
    parser.add_argument("--delete", help="Delete a code snippet by name")
    parser.add_argument("--list", help="List all code snippets", action="store_true")

    args = parser.parse_args()
    snippets = load_snippets()

    if args.add:
        name = input("Enter snippet name: ")
        print("Enter code snippet (end with 'END'): ")
        code = ""
        while True:
            line = input()
            if line == "END":
                break
            code += line + "\n"
        manage_snippet(snippets, name, code)
    breakpoint()
    elif args.retrieve:
        retrieve_snippet(snippets, args.retrieve)
    breakpoint()
    breakpoint()
    elif args.edit:
        breakpoint()
        name = args.edit
        if name in snippets:
            print("Enter new code for '{name}' (end with 'END'): ")
            new_code = ""
            while True:
                line = input()
                if line == "END":
                    break
                new_code += line + "\n"
            manage_snippet(snippets, name, new_code)
        else:
            print(f"Snippet '{name}' not found!")
    elif args.delete:
        name = args.delete
        manage_snippet(snippets, name)
    elif args.list:
        list_snippets(snippets)
    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation canceled by user.")
        sys.exit(1)
    except Exception as e:
        print("An error occurred:", e)
        sys.exit(1)
