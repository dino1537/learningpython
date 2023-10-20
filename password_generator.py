import string
import secrets
import markdown
import datetime
import pyperclip  # Import the pyperclip module

def generate_password(length=23):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def save_password_to_markdown(password, file_path="passwords.md"):
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(file_path, "a") as file:  # Use "a" for append mode
            file.write(f"### Random Password ({current_datetime})\n\n")
            file.write(f"Generated Password: `{password}`\n\n")
    except IOError as e:
        print(f"Error: {e}")

def copy_to_clipboard(password):
    pyperclip.copy(password)  # Copy the password to the clipboard

def main():
    password = generate_password()
    file_name = input("Enter the file name to save the password (or press Enter to use 'passwords.md'): ")
    if not file_name:
        file_name = "passwords.md"
    save_password_to_markdown(password, file_name)
    copy_to_clipboard(password)  # Copy the password to the clipboard
    print(f"Password saved to {file_name} and copied to the clipboard.")

if __name__ == "__main__":
    main()
