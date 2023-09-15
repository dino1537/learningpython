import random

# Generate a random number between 1 and 999
secret_number = random.randint(1, 999)

def print_box(message):
    print("*" * (len(message) + 4))
    print(f"* {message} *")
    print("*" * (len(message) + 4))

# Game loop
while True:
    try:
        guess = int(input("Guess the number (1-999): "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        continue

    if guess < secret_number:
        print("The number is too small.")
    elif guess > secret_number:
        print("The number is too big.")
    else:
        print_box("You're an idiot!")
        break

