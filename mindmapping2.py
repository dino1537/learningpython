
import typer
from rich.console import Console
from rich.tree import Tree
from rich.style import Style
from colorama import init

init(autoreset=True)

class CustomTreeNode:
    def __init__(self, text):
        self.text = text
        self.children = []

class MindMap:
    def __init__(self):
        self.nodes = {'Root': CustomTreeNode('Root')}
        self.tree = Tree("Mind Map", style=Style(color="blue"))

    def add_node(self, parent, text):
        if parent not in self.nodes:
            typer.secho("Parent node not found.", fg=typer.colors.RED)
            return
        new_node = CustomTreeNode(text)
        self.nodes[parent].children.append(new_node)
        self.nodes[text] = new_node
        self.update_tree()

    def remove_node(self, text):
        if text not in self.nodes:
            typer.secho("Node not found.", fg=typer.colors.RED)
            return
        parent = self.find_parent(text)
        if parent:
            parent.children = [child for child in parent.children if child.text != text]
        del self.nodes[text]
        self.update_tree()

    def find_parent(self, text):
        for node in self.nodes.values():
            for child in node.children:
                if child.text == text:
                    return node
        return None

    def update_tree(self):
        self.tree = Tree("Mind Map", style=Style(color="blue"))
        self.build_tree(self.tree, self.nodes['Root'])

    def build_tree(self, tree_node, custom_node):
        tree_node.text = custom_node.text
        tree_node.style = Style(color="blue")
        for child in custom_node.children:
            child_tree = Tree(child.text, style=Style(color="green"))
            tree_node.add(child_tree)
            self.build_tree(child_tree, child)

    def display(self):
        console = Console()
        console.print(self.tree)

    def export_to_markdown(self, filename):
        with open(filename, 'w') as f:
            self._export_node_to_markdown('Root', f)

    def _export_node_to_markdown(self, node, f, depth=0):
        if node != 'Root':
            f.write("  " * depth + "- " + node + "\n")
        for child in self.nodes[node].children:
            self._export_node_to_markdown(child.text, f, depth + 1)

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
            if child in [child.text for child in mind_map.nodes[current_node].children]:
                current_node = child
            else:
                typer.secho("Invalid child node.", fg=typer.colors.RED)
                typer.pause()
        elif choice == '4':
            parent = mind_map.find_parent(current_node)
            if parent:
                current_node = parent.text
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
