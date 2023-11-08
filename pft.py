import numpy as np
import pickle
import atexit

# Initialize empty arrays for income, expenses, and savings
income = np.array([])
expenses = np.array([])
savings = np.array([])

# Initialize dictionaries for custom categories and reminders
custom_categories = {}
reminders = {}

def save_data():
    with open("financial_data.pkl", "wb") as file:
        data = {
            "income": income,
            "expenses": expenses,
            "savings": savings,
            "categories": custom_categories,
            "reminders": reminders
        }
        pickle.dump(data, file)

def load_data():
    global income, expenses, savings, custom_categories, reminders
    try:
        with open("financial_data.pkl", "rb") as file:
            data = pickle.load(file)
            income = data["income"] if "income" in data else np.array([])
            expenses = data["expenses"] if "expenses" in data else np.array([])
            savings = data["savings"] if "savings" in data else np.array([])
            custom_categories = data["categories"] if "categories" in data else {}
            reminders = data["reminders"] if "reminders" in data else {}
    except FileNotFoundError:
        print("No previous data found. Starting with empty records.")

# Load data when the script starts
load_data()

# Save data before exiting
atexit.register(save_data)


# Function to input income data
def add_income():
    global income
    amount = float(input("Enter income amount: "))
    income = np.append(income, amount)

# Function to input expenses data with custom category support
def add_expense():
    global expenses
    amount = float(input("Enter expense amount: "))
    category = input("Enter expense category: ")
    expenses = np.append(expenses, amount)
    custom_categories[category] = custom_categories.get(category, 0) + amount

# Function to add a reminder for recurring expenses or income
def add_reminder():
    description = input("Enter a description for the reminder: ")
    amount = float(input("Enter the recurring amount: "))
    frequency = int(input("Enter the frequency (in days) for the reminder: "))
    reminders[description] = (amount, frequency)

# Function to calculate and display total income, expenses, and savings
def display_summary():
    total_income = np.sum(income)
    total_expenses = np.sum(expenses)
    total_savings = np.sum(savings)
    print(f"Total Income: {total_income}")
    print(f"Total Expenses: {total_expenses}")
    print(f"Total Savings: {total_savings}")

# Main loop for the finance tracker
while True:
    print("\nPersonal Finance Tracker Menu:")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. Add Savings")
    print("4. Add Reminder")
    print("5. Display Summary")
    print("6. Exit")
    choice = int(input("Enter your choice: "))

    if choice == 1:
        add_income()
    elif choice == 2:
        add_expense()
    elif choice == 3:
        add_saving()
    elif choice == 4:
        add_reminder()
    elif choice == 5:
        display_summary()
    elif choice == 6:
        break
    else:
        print("Invalid choice. Please choose again.")
