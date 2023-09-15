import string
import secrets
import markdown

# Function to generate a random password
def generate_password(length=20):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

# Generate a random password
password = generate_password()

# Save the generated password to a Markdown file
with open("password.md", "w") as file:
    file.write(f"### Random Password\n\n")
    file.write(f"Generated Password: `{password}`")

# Print the generated password (optional)
print("Generated Password:", password)

