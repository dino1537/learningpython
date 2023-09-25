import argparse
import json
import os
import sys
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter

SNIPPETS_FILE = "snippets.json"

def load_snippets():
    if os.path.exists(SNIPPETS_FILE):
        with open(SNIPPETS_FILE, "r") as file:
            return json.load(file)
    else:
        return {}

def save_snippets(snippets):
    with open(SNIPPETS_FILE, "w") as file:
        json.dump(snippets, file, indent=4)

def add_snippet(snippets, name, code):
    snippets[name] = code
    save_snippets(snippets)
    print(f"Snippet '{name}' added successfully!")

def retrieve_snippet(snippets, name):
    if name in snippets:
        code = snippets[name]
        print(f"Snippet '{name}':")
        print_highlighted_code(code)
    else:
        print(f"Snippet '{name}' not found!")

def edit_snippet(snippets, name, new_code):
    if name in snippets:
        snippets[name] = new_code
        save_snippets(snippets)
        print(f"Snippet '{name}' edited successfully!")
    else:
        print(f"Snippet '{name}' not found!")

def delete_snippet(snippets, name):
    if name in snippets:
        del snippets[name]
        save_snippets(snippets)
        print(f"Snippet '{name}' deleted successfully!")
    else:
        print(f"Snippet '{name}' not found!")

def list_snippets(snippets):
    print("Available snippets:")
    for name in snippets:
        print(f"- {name}")

def print_highlighted_code(code):
    try:
        lexer = get_lexer_by_name("python", stripall=True)
        formatter = TerminalFormatter()
        highlighted_code = highlight(code, lexer, formatter)
        print(highlighted_code)
    except Exception as e:
        print("Error highlighting code:", e)

def main():
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
        code = input("Enter code snippet: ")
        add_snippet(snippets, name, code)
    elif args.retrieve:
        retrieve_snippet(snippets, args.retrieve)
    elif args.edit:
        name = args.edit
        if name in snippets:
            new_code = input(f"Enter new code for '{name}': ")
            edit_snippet(snippets, name, new_code)
        else:
            print(f"Snippet '{name}' not found!")
    elif args.delete:
        name = args.delete
        delete_snippet(snippets, name)
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
