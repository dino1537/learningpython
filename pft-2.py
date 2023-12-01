from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import numpy as np
import pickle
import atexit
from tabulate import tabulate
from datetime import datetime

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
            "reminders": reminders,
        }
        pickle.dump(data, file)


def load_data():
    global income, expenses, savings, custom_categories, reminders
    try:
        with open("financial_data.pkl", "rb") as file:
            data = pickle.load(file)
            income = data.get("income", np.array([]))
            expenses = data.get("expenses", np.array([]))
            savings = data.get("savings", np.array([]))
            custom_categories = data.get("categories", {})
            reminders = data.get("reminders", {})
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


# Function to input expenses data with date, time, and category
def add_expense():
    global expenses
    amount = float(input("Enter expense amount: "))
    category = input("Enter expense category: ")
    date_time = datetime.now()
    expenses = np.append(expenses, [amount, date_time, category])
    custom_categories[category] = custom_categories.get(category, 0) + amount


# Function to input savings data
def add_saving():
    global savings
    amount = float(input("Enter saving amount: "))
    savings = np.append(savings, amount)


# Function to add a reminder for recurring expenses or income
def add_reminder():
    description = input("Enter a description for the reminder: ")
    amount = float(input("Enter the recurring amount: "))
    frequency = int(input("Enter the frequency (in days) for the reminder: "))
    reminders[description] = (amount, frequency)


# Function to display detailed expense information
def display_expenses():
    table = [["Expense ID", "Amount", "Date", "Category"]]
    for i in range(len(expenses) // 3):
        expense_id = i + 1
        amount = expenses[i * 3]
        date_time = expenses[i * 3 + 1]
        category = expenses[i * 3 + 2]
        table.append([expense_id, amount, date_time, category])

    print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))


# Function to calculate and display total income, expenses, and savings
def display_summary():
    total_income = np.sum(income)
    total_expenses = np.sum(expenses[::3])  # Sum every 3rd element (amounts)
    total_savings = np.sum(savings)

    table = [["Category", "Total Amount"]]

    # Calculate and display custom categories
    for category, amount in custom_categories.items():
        table.append([category, amount])

    table.extend(
        [
            ["Income", str(total_income)],
            ["Expenses", str(total_expenses)],
            ["Savings", str(total_savings)],
        ]
    )

    print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))


# Function to export summary and expenses to a PDF using ReportLab
def export_to_pdf():
    pdf_file = "finance_summary.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    elements = []

    # Create a table for the summary
    summary_table = [["Category", "Total Amount"]]

    # Calculate and add custom categories
    for category, amount in custom_categories.items():
        summary_table.append([category, amount])

    summary_table.extend(
        [
            ["Income", str(np.sum(income))],
            ["Expenses", str(np.sum(expenses[::3]))],
            ["Savings", str(np.sum(savings))],
        ]
    )

    # Define table style
    style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ]
    )

    # Create the summary table
    table = Table(summary_table)
    table.setStyle(style)
    elements.append(table)

    # Create a table for detailed expenses
    expenses_table = [["Expense ID", "Amount", "Date", "Category"]]
    for i in range(len(expenses) // 3):
        expense_id = i + 1
        amount = expenses[i * 3]
        date_time = expenses[i * 3 + 1]
        category = expenses[i * 3 + 2]
        expenses_table.append([expense_id, amount, date_time, category])

    # Define style for expenses table
    style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ]
    )

    # Create the expenses table
    table = Table(expenses_table)
    table.setStyle(style)
    elements.append(table)

    doc.build(elements)
    print(f"PDF export completed. Saved as {pdf_file}")


# Main loop for the finance tracker
while True:
    print("\nPersonal Finance Tracker Menu:")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. Add Saving")
    print("4. Add Reminder")
    print("5. Display Summary")
    print("6. Display Expenses")
    print("7. Export Summary and Expenses to PDF")
    print("8. Exit")
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
        display_expenses()
    elif choice == 7:
        export_to_pdf()
    elif choice == 8:
        break
    else:
        print("Invalid choice. Please choose again.")
