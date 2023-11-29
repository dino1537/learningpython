import os
import argparse
from datetime import datetime
import markdown_it

# Define the Zettelkasten directory
ZETTELKASTEN_DIR = "zettelkasten"

# Function to render Markdown content
def render_markdown(content):
    md = markdown_it.MarkdownIt()
    return md.render(content)

# Function to create a new Zettel
def create_zettel(title, tags=[]):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    zettel_id = f"{timestamp}"
    zettel_filename = os.path.join(ZETTELKASTEN_DIR, f"{zettel_id}.md")
    
    # Check if file already exists
    if os.path.exists(zettel_filename):
        print(f"A Zettel with the ID {zettel_id} already exists.")
        return
    
    with open(zettel_filename, "w") as zettel_file:
        zettel_file.write(f"# {title}\n\n")
        zettel_file.write("## Tags\n")
        for tag in tags:
            zettel_file.write(f"- {tag}\n")
        zettel_file.write("## References\n")
    
    print(f"Created a new Zettel: {zettel_filename}")
    return zettel_id

# Function to search for Zettels
def search_zettels(query):
    results = []
    for zettel_file in os.listdir(ZETTELKASTEN_DIR):
        if zettel_file.endswith(".md"):
            with open(os.path.join(ZETTELKASTEN_DIR, zettel_file), "r") as zettel:
                content = zettel.read()
                if query in content:
                    results.append(zettel_file)
    
    if results:
        print("Matching Zettels:")
        for result in results:
            print(result)
    else:
        print("No matching Zettels found.")

# Function to list Zettels by a specific tag
def list_zettels_by_tag(tag):
    matching_zettels = []
    for zettel_file in os.listdir(ZETTELKASTEN_DIR):
        if zettel_file.endswith(".md"):
            with open(os.path.join(ZETTELKASTEN_DIR, zettel_file), "r") as zettel:
                content = zettel.read()
                if f"- {tag}" in content:
                    matching_zettels.append(zettel_file)
    
    if matching_zettels:
        print(f"Zettels tagged with '{tag}':")
        for zettel in matching_zettels:
            print(zettel)
    else:
        print(f"No Zettels found with the tag '{tag}'.")

# CLI Interface
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI Zettelkasten System")
    parser.add_argument("action", choices=["create", "search", "list_by_tag", "view"], help="Action to perform (create, search, list_by_tag, view)")
    parser.add_argument("--title", help="Title for the new Zettel")
    parser.add_argument("--query", help="Search query")
    parser.add_argument("--tag", help="Tag for listing Zettels by tag")
    parser.add_argument("--zettel_id", help="Zettel ID for viewing")
    parser.add_argument("--tags", nargs="+", help="Tags for the new Zettel")
    
    args = parser.parse_args()
    
    if not os.path.exists(ZETTELKASTEN_DIR):
        try:
            os.mkdir(ZETTELKASTEN_DIR)
        except OSError:
            print(f"Creation of the directory {ZETTELKASTEN_DIR} failed")
            exit(1)
        else:
            print(f"Successfully created the directory {ZETTELKASTEN_DIR}")
    
    if args.action == "create":
        if not args.title:
            print("Please provide a title for the new Zettel.")
        else:
            zettel_id = create_zettel(args.title, args.tags)
    
    elif args.action == "search":
        if not args.query:
            print("Please provide a search query.")
        else:
            search_zettels(args.query)
    
    elif args.action == "list_by_tag":
        if not args.tag:
            print("Please provide a tag to list Zettels.")
        else:
            list_zettels_by_tag(args.tag)
    
    elif args.action == "view":
        if not args.zettel_id:
            print("Please provide a Zettel ID for viewing.")
        else:
            zettel_filename = os.path.join(ZETTELKASTEN_DIR, f"{args.zettel_id}.md")
            if os.path.exists(zettel_filename):
                with open(zettel_filename, "r") as zettel_file:
                    content = zettel_file.read()
                    rendered_content = render_markdown(content)
                    print(rendered_content)
            else:
                print("Zettel not found.")
