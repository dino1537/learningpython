import random
from rich import print

# Generate a random number between 1 and 999
secret_number = random.randint(1, 999)

def print_box(message):
    styled_message = f"[bold cyan]{message}[/bold cyan]"
    print(f"{'*' * (len(styled_message) + 4)}")
    print(f"* {styled_message} *")
    print(f"{'*' * (len(styled_message) + 4)}")

# Game loop
while True:
    try:
        guess = int(input("Guess the number (1-999): "))
    except ValueError:
        print("[bold red]Invalid input.[/bold red] Please enter a valid number.")
        continue

    if guess < secret_number:
        print("[bold yellow]The number is too small.[/bold yellow]")
    elif guess > secret_number:
        print("[bold yellow]The number is too big.[/bold yellow]")
    else:
        print_box("[bold green]You're an idiot![/bold green]")
        break

