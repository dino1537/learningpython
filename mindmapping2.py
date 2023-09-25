
import typer
from rich import print
from colorama import init

init(autoreset=True)

class MindMap:
    def __init__(self):
        self.nodes = {'Root': {'children': [], 'parent': None}}

    def add_node(self, parent, text):
        if parent not in self.nodes:
            typer.secho("Parent node not found.", fg=typer.colors.RED)
            return
        new_node = {'children': [], 'parent': parent}
        self.nodes[parent]['children'].append((text, new_node))
        self.nodes[text] = new_node

    def remove_node(self, text):
        if text not in self.nodes:
            typer.secho("Node not found.", fg=typer.colors.RED)
            return
        parent = self.nodes[text]['parent']
        self.nodes[parent]['children'] = [(child, child_node) for child, child_node in self.nodes[parent]['children'] if child != text]
        del self.nodes[text]

    def display(self):
        tree = self.create_tree('Root')
        print(tree)

    def create_tree(self, node, depth=0):
        tree = f"[bold green]{'  ' * depth}{node}[/bold green]\n"
        for child, child_node in self.nodes[node]['children']:
            tree += self.create_tree(child, depth + 1)
        return tree

    def export_to_markdown(self, filename):
        with open(filename, 'w') as f:
            self._export_node_to_markdown('Root', f)

    def _export_node_to_markdown(self, node, f, depth=0):
        f.write("  " * depth + "- " + node + "\n")
        for child, child_node in self.nodes[node]['children']:
            self._export_node_to_markdown(child, f, depth + 1)

def main():
    mind_map = MindMap()
    current_node = 'Root'

    while True:
        typer.clear()
        typer.secho("Current Node: " + current_node, fg=typer.colors.CYAN, bold=True)
        typer.echo("1. Add Node")
        typer.echo("2. Remove Node")
        typer.echo("3. Move to Child Node")
        typer.echo("4. Move to Parent Node")
        typer.echo("5. Display Mind Map")
        typer.echo("6. Export to Markdown")
        typer.echo("7. Quit")

        choice = typer.prompt("Enter your choice: ")

        if choice == '1':
            text = typer.prompt("Enter the text for the new node: ")
            mind_map.add_node(current_node, text)
        elif choice == '2':
            text = typer.prompt("Enter the text of the node to remove: ")
            mind_map.remove_node(text)
        elif choice == '3':
            child = typer.prompt("Enter the child node to move to: ")
            if child in [child for child, _ in mind_map.nodes[current_node]['children']]:
                current_node = child
            else:
                typer.secho("Invalid child node.", fg=typer.colors.RED)
                typer.pause()
        elif choice == '4':
            parent = mind_map.nodes[current_node]['parent']
            if parent is not None:
                current_node = parent
            else:
                typer.secho("Already at the root node.", fg=typer.colors.YELLOW)
                typer.pause()
        elif choice == '5':
            mind_map.display()
            typer.pause()
        elif choice == '6':
            filename = typer.prompt("Enter the filename for Markdown export: ")
            mind_map.export_to_markdown(filename)
            typer.secho(f"Exported to {filename}", fg=typer.colors.GREEN)
            typer.pause()
        elif choice == '7':
            break
        else:
            typer.secho("Invalid choice. Please try again.", fg=typer.colors.RED)
            typer.pause()

if __name__ == "__main__":
    typer.run(main)
